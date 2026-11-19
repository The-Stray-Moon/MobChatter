"""Replace one existing line of one mob with a new line.

The merge step keeps Chinese lines globally unique by appending the mob name,
which is visible in game for lines shared by many creatures. This tool lets an
author replace such a line at its source so the merge has nothing to disambiguate.

    python tools/reword_unique.py apply <payload.json>

Payload: [{"batch":"u0003","mob_id":"minecraft:cat","old_zh":"...",
           "zh":"...","en":"..."}]
"""
from __future__ import annotations

import argparse
import json
import sys

import unique_dialogue as ud


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["apply"])
    parser.add_argument("path")
    args = parser.parse_args()

    items = json.loads(open(args.path, encoding="utf-8").read())
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
                print(f"REJECT {batch} {item['mob_id']}: mob missing")
                failed += 1
                continue
            old = item["old_zh"]
            new = {"zh": item["zh"].strip(), "en": item["en"].strip()}
            if not new["zh"] or not new["en"]:
                print(f"REJECT {item['mob_id']}: empty replacement")
                failed += 1
                continue
            hit = False
            scenarios = entry.get("scenarios") or {}
            # A scenario key scopes the replacement to that bucket; without it
            # every occurrence in the mob is replaced, which merges two lines
            # into one text and creates a duplicate.
            wanted = item.get("scenario")
            for scenario, value in scenarios.items():
                groups = []
                if scenario == "hurt" and isinstance(value, dict):
                    if wanted in (None, "hurt", "hurt.generic"):
                        groups.append(("hurt.generic", value.get("generic") or []))
                    for damage, lines in (value.get("by_damage") or {}).items():
                        if wanted in (None, "hurt", "hurt." + damage):
                            groups.append(("hurt." + damage, lines))
                elif isinstance(value, list):
                    if wanted in (None, scenario):
                        groups.append((scenario, value))
                elif isinstance(value, dict) and "lines" in value:
                    if wanted in (None, scenario):
                        groups.append((scenario, value["lines"]))
                for key, group in groups:
                    for index, line in enumerate(group):
                        if isinstance(line, dict) and line.get("zh") == old:
                            group[index] = dict(new)
                            hit = True
            if not hit:
                print(f"REJECT {batch} {item['mob_id']}: line not found {old[:20]!r}")
                failed += 1
            else:
                changed += 1
        if changed:
            tmp = path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(path)
        print(f"OK {batch} replaced={changed}/{len(batch_items)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
