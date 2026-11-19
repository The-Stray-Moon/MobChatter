"""Convert legacy flat hurt blocks into the nested by_damage shape.

Early batches stored `hurt` as {"generic": [...], "fire": [...], ...} while the
runtime and merge step expect {"generic": [...], "by_damage": {"fire": [...]}}.
The damage lines already exist in those files, so this is a pure reshape.

    python tools/normalize_unique.py [--write]
"""
from __future__ import annotations

import argparse
import json
import sys

import unique_dialogue as ud


def norm(lines) -> list[dict]:
    out = []
    for item in lines or []:
        if isinstance(item, dict) and item.get("zh") and item.get("en"):
            out.append({"zh": item["zh"], "en": item["en"]})
        elif isinstance(item, (list, tuple)) and len(item) >= 2 and item[0] and item[1]:
            out.append({"zh": item[0], "en": item[1]})
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args()

    converted = files = 0
    for path in sorted(ud.UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        touched = False
        for entry in data.get("mobs", []):
            hurt = (entry.get("scenarios") or {}).get("hurt")
            if not isinstance(hurt, dict) or hurt.get("by_damage"):
                continue
            by_damage = {}
            for damage in ud.DAMAGE:
                lines = norm(hurt.get(damage))
                if lines:
                    by_damage[damage] = lines[:1]
            for damage in ud.DAMAGE:
                hurt.pop(damage, None)
            hurt["by_damage"] = by_damage
            converted += 1
            touched = True
        if touched:
            files += 1
            if options.write:
                tmp = path.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
                tmp.replace(path)
    print(f"legacy hurt blocks converted={converted} files={files} written={options.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
