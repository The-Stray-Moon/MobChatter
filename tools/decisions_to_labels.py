"""Convert compact decision files into label JSONL.

Decision line format:  <index> <Y|N> [P] [| evidence]
Example:               45 Y P | Copper Golem, Crab, Glare
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import DATA_DIR  # noqa: E402


def main() -> int:
    queue_dir = DATA_DIR / "review"
    mapping = json.loads((queue_dir / "queue_map.json").read_text(encoding="utf-8"))
    decisions: dict[int, dict] = {}

    for path in sorted(queue_dir.glob("decisions_*.txt")):
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            index_text, rest = line.split(None, 1)
            index = int(index_text)
            verdict, _, tail = rest.partition("|")
            parts = verdict.split()
            decisions[index] = {
                "key": mapping[str(index)],
                "adds_new_mob": parts[0].upper() == "Y",
                "primary": "P" in parts[1:],
                "evidence": tail.strip(),
                "confidence": 0.9 if parts[0].upper() == "N" else (0.9 if "P" in parts[1:] else 0.6),
            }

    out = queue_dir / "labels.jsonl"
    with out.open("w", encoding="utf-8") as handle:
        for index in sorted(decisions):
            entry = decisions[index]
            handle.write(
                json.dumps(
                    {
                        "key": entry["key"],
                        "adds_new_mob": entry["adds_new_mob"],
                        "primary": entry["primary"],
                        "mobs": [],
                        "evidence": entry["evidence"],
                        "confidence": entry["confidence"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    yes = sum(1 for d in decisions.values() if d["adds_new_mob"])
    print(f"wrote {len(decisions)} labels to {out} ({yes} positives)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
