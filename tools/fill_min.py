"""Append lines until every scenario reaches the eight-line floor.

Cheaper than a full rewrite: the callers only supply the missing lines, and this
only enforces the floor (>=8 per scenario), not the weight-derived target.

Payload (list): [{"batch":"u0003","mob_id":"minecraft:cat",
                  "scenarios":{"walk":[{"zh","en"}], "hurt":{"generic":[...]}}}]
"""
from __future__ import annotations

import json
import sys

import unique_dialogue as ud

FLOOR = 8


def shortfall(entry: dict) -> dict:
    missing = {}
    scenarios = entry.get("scenarios") or {}
    for scenario in ud.SCENARIOS:
        have = len(scenarios.get(scenario) or [])
        if have < FLOOR:
            missing[scenario] = FLOOR - have
    hurt = scenarios.get("hurt") or {}
    have = len(hurt.get("generic") or [])
    if have < FLOOR:
        missing["hurt.generic"] = FLOOR - have
    return missing


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    items = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    if isinstance(items, dict):
        items = [items]

    by_batch: dict[str, list[dict]] = {}
    for item in items:
        by_batch.setdefault(item["batch"], []).append(item)

    failed = 0
    for batch, batch_items in by_batch.items():
        path = ud.UNIQUE / f"{batch}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        by_id = {m.get("mob_id"): m for m in data.get("mobs", [])}
        changed = 0
        for item in batch_items:
            entry = by_id.get(item["mob_id"])
            if entry is None:
                print(f"REJECT {batch} {item['mob_id']}: missing")
                failed += 1
                continue
            scenarios = entry.setdefault("scenarios", {})
            added = 0
            for scenario, lines in (item.get("scenarios") or {}).items():
                if scenario == "hurt":
                    hurt = scenarios.setdefault("hurt", {"generic": [], "by_damage": {}})
                    bucket = hurt.setdefault("generic", [])
                    existing = {line["zh"] for line in bucket}
                    for line in lines:
                        zh = str(line.get("zh") or "").strip()
                        en = str(line.get("en") or "").strip()
                        if zh and en and zh not in existing:
                            bucket.append({"zh": zh, "en": en})
                            existing.add(zh)
                            added += 1
                    continue
                bucket = scenarios.setdefault(scenario, [])
                existing = {line["zh"] for line in bucket if isinstance(line, dict)}
                for line in lines:
                    zh = str(line.get("zh") or "").strip()
                    en = str(line.get("en") or "").strip()
                    if zh and en and zh not in existing:
                        bucket.append({"zh": zh, "en": en})
                        existing.add(zh)
                        added += 1
            left = shortfall(entry)
            if left:
                print(f"PARTIAL {batch} {item['mob_id']} added={added} still={left}")
                failed += 1
            else:
                changed += 1
                print(f"OK {batch} {item['mob_id']} added={added}")
        if changed:
            tmp = path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(path)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
