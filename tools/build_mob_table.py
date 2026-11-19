"""Merge per-mod mob research files into the final mob table.

Reads data/mobs/*.json (one file per mod rank), writes:
  output/mob_descriptions.csv
  output/mob_descriptions.json
  output/mob_index.json
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import DATA_DIR, OUTPUT_DIR  # noqa: E402

REQUIRED = ("mob_id", "name_en", "description_zh", "source")
ALLOWED_SOURCES = {"vanilla", "mod_body", "wiki", "jar_data"}
LEGACY_SOURCES = {"mcmod"}
COLUMNS = [
    "mod_rank", "mod_name", "mod_url", "mob_id", "name_en", "name_zh",
    "description_zh", "source", "source_url", "confidence", "notes",
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    tmp = path.with_name(path.name + ".new")
    with tmp.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    _replace(tmp, path)


def write_json(path: Path, data) -> None:
    tmp = path.with_name(path.name + ".new")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    _replace(tmp, path)


def _replace(tmp: Path, target: Path) -> None:
    try:
        tmp.replace(target)
    except PermissionError:
        print(f"warning: {target.name} is locked; new content left at {tmp.name}")


def main() -> int:
    files = sorted((DATA_DIR / "mobs").glob("*.json"))
    if not files:
        print("no data/mobs/*.json")
        return 1

    rows: list[dict] = []
    index: dict[str, dict] = {}
    errors: list[str] = []
    legacy_count = 0

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        rank = data.get("rank")
        mod = data.get("mod", path.stem)
        mod_url = data.get("mod_url", "")
        mobs = data.get("mobs") or []
        index[str(rank)] = {
            "mod": mod,
            "mod_url": mod_url,
            "mob_count": len(mobs),
            "mobs": [m.get("mob_id") for m in mobs],
        }
        for mob in mobs:
            missing = [field for field in REQUIRED if not mob.get(field)]
            if missing:
                errors.append(f"{path.name}: mob missing {missing}: {mob.get('name_en')}")
                continue
            if mob.get("source") not in ALLOWED_SOURCES | LEGACY_SOURCES:
                errors.append(f"{path.name}: disallowed source '{mob.get('source')}': {mob.get('mob_id')}")
                continue
            if mob.get("source") in LEGACY_SOURCES:
                legacy_count += 1
            rows.append(
                {
                    "mod_rank": rank,
                    "mod_name": mod,
                    "mod_url": mod_url,
                    "mob_id": mob.get("mob_id", ""),
                    "name_en": mob.get("name_en", ""),
                    "name_zh": mob.get("name_zh", ""),
                    "description_zh": mob.get("description_zh", ""),
                    "source": mob.get("source", ""),
                    "source_url": mob.get("source_url", ""),
                    "confidence": mob.get("confidence", ""),
                    "notes": mob.get("notes", ""),
                }
            )

    rows.sort(key=lambda r: (int(r["mod_rank"] or 0), r["name_en"].lower()))
    # Keep the highest-confidence row when a rank repeats a mob id.
    deduped: dict[tuple, dict] = {}
    for row in rows:
        key = (row["mod_rank"], row["mob_id"])
        current = deduped.get(key)
        if current is None or float(row["confidence"] or 0) > float(current["confidence"] or 0):
            deduped[key] = row
    rows = sorted(deduped.values(), key=lambda r: (int(r["mod_rank"] or 0), r["name_en"].lower()))

    # Keep the relationship index consistent with the deduplicated table.
    for rank, info in index.items():
        rank_rows = [row for row in rows if str(row["mod_rank"]) == rank]
        info["mob_count"] = len(rank_rows)
        info["mobs"] = [row["mob_id"] for row in rank_rows]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT_DIR / "mob_descriptions.csv", COLUMNS, rows)
    write_json(OUTPUT_DIR / "mob_descriptions.json", rows)
    write_json(OUTPUT_DIR / "mob_index.json", index)

    by_rank = {str(r["mod_rank"]): r for r in rows}
    summary_rows = []
    source_counter = {}
    for rank, info in index.items():
        counts = {}
        for row in rows:
            if str(row["mod_rank"]) == rank:
                counts[row["source"]] = counts.get(row["source"], 0) + 1
        source_counter[rank] = counts
        summary_rows.append(
            {
                "mod_rank": rank,
                "mod_name": info["mod"],
                "mod_url": info["mod_url"],
                "mob_count": info["mob_count"],
                "vanilla": counts.get("vanilla", 0),
                "mod_body": counts.get("mod_body", 0),
                "wiki": counts.get("wiki", 0),
                "mcmod": counts.get("mcmod", 0),
                "jar_data": counts.get("jar_data", 0),
            }
        )
    summary_rows.sort(key=lambda r: int(r["mod_rank"] or 0))
    write_csv(
        OUTPUT_DIR / "mod_mob_summary.csv",
        ["mod_rank", "mod_name", "mod_url", "mob_count", "vanilla", "mod_body", "wiki", "mcmod", "jar_data"],
        summary_rows,
    )

    empty = sum(1 for r in rows if not r["description_zh"].strip())
    print(f"mods: {len(index)} | mobs: {len(rows)} | empty descriptions: {empty} | errors: {len(errors)} | legacy mcmod: {legacy_count}")
    for error in errors[:10]:
        print("  ", error)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
