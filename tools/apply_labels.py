"""Merge manually produced labels into data/classified.json.

Labels file format (one JSON object per line):
{"key":"modrinth:xxxx","adds_new_mob":true,"primary":true,"mobs":["X"],"evidence":"...","confidence":0.9}

Usage: python tools/apply_labels.py [path/to/labels.jsonl]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import DATA_DIR  # noqa: E402

CLASSIFIED = DATA_DIR / "classified.json"
CANDIDATES = DATA_DIR / "candidates.json"


def main() -> int:
    labels_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR / "review" / "labels.jsonl"
    labels: dict[str, dict] = {}
    for raw in labels_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        entry = json.loads(line)
        key = entry.pop("key")
        labels[key] = {
            "adds_new_mob": bool(entry.get("adds_new_mob")),
            "primary": bool(entry.get("primary")),
            "mobs": [str(m) for m in (entry.get("mobs") or [])][:12],
            "evidence": str(entry.get("evidence") or "")[:300],
            "confidence": float(entry.get("confidence") or 0.9),
            "method": "agent-manual",
        }

    valid_keys = {
        f"{c['source']}:{c['source_id']}"
        for c in json.loads(CANDIDATES.read_text(encoding="utf-8"))
    }
    unknown = sorted(set(labels) - valid_keys)
    if unknown:
        print(f"warning: {len(unknown)} labels do not match any candidate, e.g. {unknown[:3]}")

    existing = json.loads(CLASSIFIED.read_text(encoding="utf-8")) if CLASSIFIED.exists() else {}
    existing.update({k: v for k, v in labels.items() if k in valid_keys})
    CLASSIFIED.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

    positives = sum(1 for v in existing.values() if v.get("adds_new_mob"))
    print(f"applied {len(labels)} manual labels; {len(existing)} total labels; {positives} positives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
