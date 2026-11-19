"""Plan per-mob unique dialogue generation.

Writes data/dialogue/unique_plan.json: batches of 4 mobs with the context an
agent needs (name, description, archetype, per-scenario weights).
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BATCH_SIZE = 4


def load_build_dialogue():
    spec = importlib.util.spec_from_file_location("bd", ROOT / "tools" / "build_dialogue.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    bd = load_build_dialogue()
    archetypes_data = json.loads((DATA / "dialogue" / "archetypes.json").read_text(encoding="utf-8"))
    archetypes = {a["id"]: a for a in archetypes_data["archetypes"]}
    intro = {}
    with (ROOT / "output" / "top308_mob_mods.csv").open(encoding="utf-8-sig") as handle:
        for rec in csv.DictReader(handle):
            intro[int(rec["rank"])] = rec.get("intro_zh") or rec.get("summary") or ""

    rows = list(csv.DictReader(open(ROOT / "output" / "mob_descriptions.csv", encoding="utf-8-sig")))
    batches = []
    current = []
    for row in rows:
        rank = int(row["mod_rank"])
        theme = bd.mod_theme(intro.get(rank, ""))
        archetype = bd.classify(row, theme)
        weights = dict(archetypes[archetype]["weights"])
        weights = {k: bd.weight_of(row, archetype, k, archetypes, theme) for k in weights}
        current.append(
            {
                "mob_id": row["mob_id"],
                "name_en": row["name_en"],
                "name_zh": row["name_zh"],
                "description": row["description_zh"],
                "mod": row["mod_name"],
                "rank": rank,
                "archetype": archetype,
                "weights": weights,
            }
        )
        if len(current) >= BATCH_SIZE:
            batches.append(current)
            current = []
    if current:
        batches.append(current)

    plan = {}
    for index, batch in enumerate(batches, 1):
        plan[f"u{index:04d}"] = batch
    out = DATA / "dialogue" / "unique_plan.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"batches={len(plan)} mobs={sum(len(b) for b in plan.values())} size={out.stat().st_size/1024/1024:.1f}MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
