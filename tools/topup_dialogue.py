"""Append only the missing lines of a scenario, keeping existing text.

Top-up work happens after a batch was already written with 8-10 lines per
scenario while the plan asks for up to 20. Rewriting whole mobs would throw
away good lines and risk losing author intent, so this tool merges new lines
into the existing list and rewrites the file only when nothing is lost.

    python tools/topup_dialogue.py show  <batch> <mob_id>
    python tools/topup_dialogue.py apply <payload.json>
    python tools/topup_dialogue.py status

Payload for `apply` is a list of dicts:
    [{"batch":"u0710","mob_id":"aoa3:zarg",
      "scenarios":{"walk":[{"zh","en"}], "hurt":{"generic":[...]}}}]
Every scenario given is appended to the existing one; lines whose Chinese text
already exists in that mob are skipped, so re-running is safe.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import unique_dialogue as ud


def norm(value) -> list[dict]:
    out = []
    for item in value or []:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            zh, en = item[0], item[1]
        elif isinstance(item, dict):
            zh, en = item.get("zh"), item.get("en")
        else:
            continue
        zh, en = str(zh or "").strip(), str(en or "").strip()
        if zh and en:
            out.append({"zh": zh, "en": en})
    return out


def shortfall(mob: dict, entry: dict) -> dict:
    counts = ud.required_counts(mob)
    scenarios = entry.get("scenarios") or {}
    missing: dict[str, int] = {}
    for scenario in ud.SCENARIOS:
        have = len(scenarios.get(scenario) or [])
        if have < counts[scenario]:
            missing[scenario] = counts[scenario] - have
    hurt = scenarios.get("hurt")
    if isinstance(hurt, dict):
        have = len(hurt.get("generic") or [])
        if have < counts["hurt"]:
            missing["hurt.generic"] = counts["hurt"] - have
    return missing


def apply_one(batch: str, mob_id: str, incoming: dict) -> str:
    path = ud.UNIQUE / f"{batch}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    plan = {m["mob_id"]: m for m in ud.load_plan().get(batch, [])}
    mob = plan.get(mob_id)
    if mob is None:
        return f"REJECT unknown mob {mob_id} in {batch}"
    entry = next((m for m in data.get("mobs", []) if m.get("mob_id") == mob_id), None)
    if entry is None:
        return f"REJECT {mob_id} not present in {batch}.json"
    counts = ud.required_counts(mob)
    scenarios = entry.setdefault("scenarios", {})
    added = 0
    for scenario, value in incoming.items():
        if scenario == "hurt":
            hurt = scenarios.get("hurt")
            if not isinstance(hurt, dict):
                hurt = {"generic": [], "by_damage": {}}
                scenarios["hurt"] = hurt
            if isinstance(value, dict):
                for line in norm(value.get("generic")):
                    if len(hurt.setdefault("generic", [])) < counts["hurt"] and \
                            line["zh"] not in {l["zh"] for l in hurt["generic"]}:
                        hurt["generic"].append(line)
                        added += 1
                for damage, lines in (value.get("by_damage") or {}).items():
                    bucket = hurt.setdefault("by_damage", {}).setdefault(damage, [])
                    if bucket:
                        continue
                    for line in norm(lines)[:1]:
                        bucket.append(line)
                        added += 1
            continue
        if scenario not in counts:
            continue
        bucket = scenarios.setdefault(scenario, [])
        if not isinstance(bucket, list):
            continue
        existing = {line["zh"] for line in bucket if isinstance(line, dict)}
        for line in norm(value):
            if len(bucket) >= counts[scenario]:
                break
            if line["zh"] in existing:
                continue
            bucket.append(line)
            existing.add(line["zh"])
            added += 1
    problems = ud.validate_mob(mob, entry, strict=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    if problems:
        return f"PARTIAL {batch} {mob_id} added={added} still: " + "; ".join(problems[:4])
    return f"OK {batch} {mob_id} added={added}"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["show", "apply", "status"])
    parser.add_argument("args", nargs="*")
    options = parser.parse_args()

    if options.command == "status":
        work = json.loads((ud.UNIQUE / "topup.json").read_text(encoding="utf-8"))
        todo = []
        for item in work:
            path = ud.UNIQUE / f"{item['batch']}.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            entry = next((m for m in data["mobs"] if m["mob_id"] == item["mob_id"]), None)
            plan = {m["mob_id"]: m for m in ud.load_plan().get(item["batch"], [])}
            if entry and plan.get(item["mob_id"]):
                left = shortfall(plan[item["mob_id"]], entry)
                if left:
                    todo.append({**item, "missing": left})
        print(f"remaining mobs={len(todo)} lines={sum(sum(v.values()) for v in (t['missing'] for t in todo))}")
        (ud.UNIQUE / "topup.json").write_text(json.dumps(todo, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
        return 0

    if options.command == "show":
        batch, mob_id = options.args
        data = json.loads((ud.UNIQUE / f"{batch}.json").read_text(encoding="utf-8"))
        plan = {m["mob_id"]: m for m in ud.load_plan().get(batch, [])}
        entry = next((m for m in data["mobs"] if m["mob_id"] == mob_id), None)
        if entry is None:
            print(f"not found: {batch} {mob_id}")
            return 1
        mob = plan[mob_id]
        payload = {
            "batch": batch, "mob_id": mob_id, "rank": mob["rank"],
            "name_zh": mob.get("name_zh") or "", "name_en": mob.get("name_en") or "",
            "mod": mob.get("mod") or "",
            "mod_intro": ud.load_intros().get(str(mob["rank"]), ""),
            "description": mob.get("description") or "",
            "archetype": mob.get("archetype") or "",
            "counts": ud.required_counts(mob),
            "missing": shortfall(mob, entry),
            "existing": {scenario: [line["zh"] for line in (value if isinstance(value, list)
                                                           else value.get("lines", []))]
                         for scenario, value in (entry.get("scenarios") or {}).items()
                         if scenario != "hurt"},
        }
        hurt = (entry.get("scenarios") or {}).get("hurt")
        if isinstance(hurt, dict):
            payload["existing"]["hurt.generic"] = [l["zh"] for l in hurt.get("generic", [])]
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return 0

    path = Path(options.args[0])
    items = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = [items]
    failed = 0
    for item in items:
        result = apply_one(item["batch"], item["mob_id"], item.get("scenarios") or {})
        print(result)
        if not result.startswith("OK"):
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
