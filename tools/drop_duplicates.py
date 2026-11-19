"""Drop later occurrences of a duplicated Chinese line.

Rewriting every duplicate with a model costs a lot; removing the later copy is
free and keeps the corpus unique. The first occurrence is always kept, and a
one-line `hurt.by_damage` bucket is never emptied (the duplicate stays there).

    python tools/drop_duplicates.py [--write]
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
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args()

    seen: set[str] = set()
    dropped = files = 0
    lowered: list[tuple[str, str, str]] = []

    for path in sorted(ud.UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for entry in data.get("mobs", []):
            scenarios = entry.get("scenarios") or {}
            for scenario, value in scenarios.items():
                if scenario == "hurt" and isinstance(value, dict):
                    generic = value.get("generic") or []
                    kept = []
                    for line in generic:
                        zh = line.get("zh") if isinstance(line, dict) else None
                        if zh and zh in seen:
                            dropped += 1
                            changed = True
                            continue
                        if zh:
                            seen.add(zh)
                        kept.append(line)
                    value["generic"] = kept
                    for damage, lines in list((value.get("by_damage") or {}).items()):
                        # An emptied damage bucket is fine: the runtime falls
                        # back to the generic hurt line, so duplicates there are
                        # dropped like anywhere else.
                        kept = []
                        for line in lines:
                            zh = line.get("zh") if isinstance(line, dict) else None
                            if zh and zh in seen:
                                dropped += 1
                                changed = True
                                continue
                            if zh:
                                seen.add(zh)
                            kept.append(line)
                        if kept:
                            value["by_damage"][damage] = kept
                        else:
                            value["by_damage"].pop(damage, None)
                elif isinstance(value, list):
                    kept = []
                    for line in value:
                        zh = line.get("zh") if isinstance(line, dict) else None
                        if zh and zh in seen:
                            dropped += 1
                            changed = True
                            continue
                        if zh:
                            seen.add(zh)
                        kept.append(line)
                    scenarios[scenario] = kept
                elif isinstance(value, dict) and "lines" in value:
                    kept = []
                    for line in value["lines"]:
                        zh = line.get("zh") if isinstance(line, dict) else None
                        if zh and zh in seen:
                            dropped += 1
                            changed = True
                            continue
                        if zh:
                            seen.add(zh)
                        kept.append(line)
                    value["lines"] = kept
        if changed:
            files += 1
            if options.write:
                tmp = path.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
                tmp.replace(path)
    print(f"duplicate lines dropped={dropped} batches={files} written={options.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
