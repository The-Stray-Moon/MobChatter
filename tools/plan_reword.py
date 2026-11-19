"""Plan the cross-mob duplicate rewrite.

Builds a work list of "reword this line in this mob" items and shards it by
batch file, so each agent owns whole batches and concurrent runs never write the
same JSON file.

    python tools/plan_reword.py --shards 64
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import unique_dialogue as ud

WORK = ud.UNIQUE / "reword_work.json"
SHARDS = ud.UNIQUE / "reword_shards.json"


def occurrences() -> dict[str, list[dict]]:
    seen: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(ud.UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for entry in data.get("mobs", []):
            scenarios = entry.get("scenarios") or {}
            for scenario, value in scenarios.items():
                if scenario == "hurt" and isinstance(value, dict):
                    groups = [("hurt.generic", value.get("generic") or [])]
                    groups += [("hurt." + damage, lines)
                               for damage, lines in (value.get("by_damage") or {}).items()]
                elif isinstance(value, list):
                    groups = [(scenario, value)]
                elif isinstance(value, dict):
                    groups = [(scenario, value.get("lines") or [])]
                else:
                    continue
                for key, lines in groups:
                    for line in lines:
                        if isinstance(line, dict) and line.get("zh"):
                            seen[line["zh"]].append({
                                "batch": path.stem, "mob_id": entry["mob_id"],
                                "scenario": key,
                            })
    return seen


def main() -> int:
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--shards", type=int, default=64)
    args = parser.parse_args()

    seen = occurrences()
    per_batch: dict[str, list[dict]] = defaultdict(list)
    duplicates = 0
    for zh, places in seen.items():
        if len(places) < 2:
            continue
        duplicates += len(places) - 1
        for place in places[1:]:
            per_batch[place["batch"]].append({"old_zh": zh, **place})

    work = [item for batch in sorted(per_batch) for item in per_batch[batch]]
    WORK.write_text(json.dumps(work, ensure_ascii=False, indent=1), encoding="utf-8")

    # Greedy balance by item count, but never split one batch across shards.
    ordered = sorted(per_batch.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    shards: list[dict] = [{"items": [], "batches": []} for _ in range(args.shards)]
    for batch, items in ordered:
        target = min(shards, key=lambda s: len(s["items"]))
        target["items"].extend(items)
        target["batches"].append(batch)

    payload = {}
    for index, shard in enumerate(shards, 1):
        if not shard["items"]:
            continue
        payload[f"r{index:02d}"] = {
            "batches": sorted(shard["batches"]),
            "items": shard["items"],
        }
    SHARDS.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    counts = [len(v["items"]) for v in payload.values()]
    print(f"duplicate rows={duplicates} batches={len(per_batch)} "
          f"shards={len(payload)} min={min(counts)} max={max(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
