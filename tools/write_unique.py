"""Write one mob's dialogue into its unique batch, with validation.

Used by agent-authored shards and by the local model runner. Input is JSON on
stdin: {"batch": "u0123", "mob_id": "mod:id", "scenarios": {...}} where
scenarios uses either arrays of ["zh","en"] or arrays of {"zh","en"}.

Exit code 0 on save, 1 when rejected; rejection prints the offending scenario
and count so the author can fix just that part.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import unique_dialogue as ud


def write_entry(batch: str, entry: dict) -> None:
    path = ud.UNIQUE / f"{batch}.json"
    data = {"batch": batch, "mobs": []}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            raise SystemExit(f"refusing to overwrite unreadable {path.name}")
        data.setdefault("batch", batch)
        data.setdefault("mobs", [])
    data["mobs"] = [m for m in data["mobs"]
                    if not (m.get("mob_id") == entry["mob_id"]
                            and m.get("rank") in (None, entry["rank"]))]
    data["mobs"].append(entry)
    data["mobs"].sort(key=lambda m: m.get("rank") or 0)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    items = payload if isinstance(payload, list) else [payload]
    failed = 0
    for item in items:
        batch = item["batch"]
        mob_id = item["mob_id"]
        plan = {m["mob_id"]: m for m in ud.load_plan().get(batch, [])}
        mob = plan.get(mob_id)
        if mob is None:
            print(f"REJECT unknown mob {mob_id} in {batch}")
            failed += 1
            continue
        entry = {"mob_id": mob_id, "rank": mob["rank"],
                 "name_en": mob.get("name_en") or "", "name_zh": mob.get("name_zh") or "",
                 "scenarios": item["scenarios"]}
        problems = ud.validate_mob(mob, entry, strict=False)
        if problems:
            print(f"REJECT {mob_id}")
            for problem in problems[:20]:
                print(f"  {problem}")
            failed += 1
            continue
        write_entry(batch, entry)
        counts = ud.required_counts(mob)
        total = sum(len(entry["scenarios"].get(s, [])) for s in ud.SCENARIOS)
        total += len(entry["scenarios"].get("hurt", {}).get("generic", []))
        total += sum(len(v) for v in
                     entry["scenarios"].get("hurt", {}).get("by_damage", {}).values())
        print(f"OK {batch} {mob_id} lines={total} "
              f"target={sum(counts.values()) + len(ud.DAMAGE)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
