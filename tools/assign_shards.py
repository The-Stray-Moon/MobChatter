"""Assign remaining unique-dialogue batches to disjoint shards.

Writes data/dialogue/unique/shards.json: {"s01": ["u0789", ...], ...} plus a
reservation file for the local qwen runner, so agent shards and the local model
never write the same batch.

    python tools/assign_shards.py --agents 64 --local 96
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import unique_dialogue as ud

UNIQUE = ud.UNIQUE
SHARDS = UNIQUE / "shards.json"
LOCAL = UNIQUE / "local_assignment.json"

# Batches with the most mobs first: they are the slowest, so start them early.
def ordered_batches() -> list[str]:
    plan = ud.load_plan()
    _, remaining = ud.covered()
    weight: dict[str, int] = {}
    for batch, _ in remaining:
        weight[batch] = weight.get(batch, 0) + 1
    return sorted(weight, key=lambda b: (-weight[b], b))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agents", type=int, default=64)
    parser.add_argument("--local", type=int, default=0,
                        help="batches reserved for the local qwen runner")
    args = parser.parse_args()

    batches = ordered_batches()
    local = batches[: args.local]
    rest = batches[args.local:]
    shards: dict[str, list[str]] = {}
    for index in range(args.agents):
        shards[f"s{index + 1:02d}"] = rest[index::args.agents]
    shards = {name: items for name, items in shards.items() if items}

    SHARDS.write_text(json.dumps(shards, ensure_ascii=False, indent=1), encoding="utf-8")
    LOCAL.write_text(json.dumps({"batches": local}, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    counts = [len(v) for v in shards.values()]
    print(f"batches total={len(batches)} local={len(local)} agents={len(shards)} "
          f"min={min(counts)} max={max(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
