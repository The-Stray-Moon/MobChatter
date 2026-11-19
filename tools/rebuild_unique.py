"""Rebuild unique batch entries from data/dialogue/mods after a bad cleanup.

`mods/<rank>.json` is written by the merge step and still holds every line, so
it is the authoritative copy when a unique batch lost data. This restores just
the mobs that are missing or shorter in `unique/`, leaving healthy batches
untouched.

    python tools/rebuild_unique.py [--write]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import unique_dialogue as ud

DATA = Path(__file__).resolve().parent.parent / "data" / "dialogue"
MODS = DATA / "mods"
UNIQUE = DATA / "unique"


def count(scenarios: dict) -> int:
    total = 0
    for key, value in scenarios.items():
        if key == "hurt" and isinstance(value, dict):
            total += len(value.get("generic") or [])
            total += sum(len(v) for v in (value.get("by_damage") or {}).values())
        elif isinstance(value, dict):
            total += len(value.get("lines") or [])
        elif isinstance(value, list):
            total += len(value)
    return total


def from_mods(scenarios: dict) -> dict:
    """Convert the {"weight","lines"} schema back to unique-batch shape."""
    out: dict = {}
    for key, value in scenarios.items():
        if key == "hurt" and isinstance(value, dict):
            out["hurt"] = {
                "generic": [dict(line) for line in value.get("generic") or []],
                "by_damage": {damage: [dict(line) for line in lines]
                              for damage, lines in (value.get("by_damage") or {}).items()},
            }
        elif isinstance(value, dict) and "lines" in value:
            out[key] = [dict(line) for line in value["lines"]]
        elif isinstance(value, list):
            out[key] = [dict(line) if isinstance(line, dict) else line for line in value]
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args()

    plan = ud.load_plan()
    mods_cache: dict[int, dict] = {}
    restored = written = 0

    for batch, mobs in plan.items():
        path = UNIQUE / f"{batch}.json"
        data = {"batch": batch, "mobs": []}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
        present = {m.get("mob_id"): m for m in data.get("mobs", [])}
        changed = False
        for mob in mobs:
            mob_id = mob["mob_id"]
            rank = mob["rank"]
            if rank not in mods_cache:
                mod_path = MODS / f"{rank}.json"
                if not mod_path.exists():
                    continue
                mods_cache[rank] = json.loads(mod_path.read_text(encoding="utf-8"))
            source = next((m for m in mods_cache[rank].get("mobs", [])
                           if m["mob_id"] == mob_id), None)
            if source is None:
                continue
            want = count(source.get("scenarios") or {})
            have = count((present.get(mob_id) or {}).get("scenarios") or {})
            if have >= want:
                continue
            entry = {"mob_id": mob_id, "rank": rank,
                     "name_en": mob.get("name_en") or "",
                     "name_zh": mob.get("name_zh") or "",
                     "scenarios": from_mods(source.get("scenarios") or {})}
            data["mobs"] = [m for m in data["mobs"] if m.get("mob_id") != mob_id]
            data["mobs"].append(entry)
            data["mobs"].sort(key=lambda m: (m.get("rank") or 0, m.get("mob_id") or ""))
            present[mob_id] = entry
            restored += 1
            changed = True
        if changed:
            written += 1
            if options.write:
                tmp = path.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
                tmp.replace(path)
    print(f"mobs restored={restored} batches={written} written={options.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
