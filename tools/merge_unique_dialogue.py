"""Merge per-mob unique dialogue batches into data/dialogue/mods/<rank>.json.

Each mod file is loaded, patched and written exactly once, so the merge runs in
seconds instead of re-reading a multi-megabyte file per mob.

Canonical schema (what tools/build_mod_dialogue.py reads):
  "walk": {"weight": <float>, "lines": [{"zh","en"}, ...]}
  "hurt": {"weight": <float>, "generic": [...], "by_damage": {"fire": [...], ...}}

Chinese lines are made globally unique: a repeat inside one mod gets the mob
name appended instead of being dropped.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dialogue"
UNIQUE = DATA / "unique"
SCENARIOS = ["walk", "idle", "look_player", "tempted", "collide", "mate",
             "pickup", "target_acquire", "targeting", "melee_attack", "spawn"]


def norm_lines(value) -> list[dict]:
    out = []
    for item in value or []:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            zh, en = item[0], item[1]
        elif isinstance(item, dict):
            zh, en = item.get("zh"), item.get("en")
        else:
            continue
        zh = str(zh or "").strip()
        en = str(en or "").strip()
        if zh and en:
            out.append({"zh": zh, "en": en})
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = json.loads((DATA / "unique_plan.json").read_text(encoding="utf-8"))
    patches: dict[int, dict[str, dict]] = defaultdict(dict)
    names: dict[str, tuple[str, str]] = {}

    for path in sorted(UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        batch = plan.get(path.stem)
        if not batch:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        by_id = {m["mob_id"]: m for m in batch}
        for entry in data.get("mobs", []):
            planned = by_id.get(entry.get("mob_id"))
            if planned is None:
                continue
            rank = planned["rank"]
            weights = planned.get("weights") or {}
            raw = entry.get("scenarios") or {}
            scenarios = {}
            for scenario in SCENARIOS:
                payload = raw.get(scenario)
                lines = norm_lines(payload if isinstance(payload, list)
                                   else (payload or {}).get("lines"))
                if lines:
                    scenarios[scenario] = {"weight": float(weights.get(scenario, 1.0)),
                                           "lines": lines}
            hurt = raw.get("hurt")
            if isinstance(hurt, dict):
                generic = norm_lines(hurt.get("generic"))
                by_damage = {damage: norm_lines(lines)[:1]
                             for damage, lines in (hurt.get("by_damage") or {}).items()
                             if norm_lines(lines)}
                if generic or by_damage:
                    scenarios["hurt"] = {"weight": float(weights.get("hurt", 1.0)),
                                         "generic": generic, "by_damage": by_damage}
            if not scenarios:
                continue
            patches[rank][entry["mob_id"]] = scenarios
            names[entry["mob_id"]] = (
                entry.get("name_zh") or planned.get("name_zh") or "生物",
                entry.get("name_en") or planned.get("name_en") or "")

    seen: dict[str, str] = {}
    duplicates = 0
    merged = 0
    for rank in sorted(patches):
        path = DATA / "mods" / f"{rank}.json"
        if not path.exists():
            continue
        mod_data = json.loads(path.read_text(encoding="utf-8"))
        by_id = {m["mob_id"]: m for m in mod_data.get("mobs", [])}
        for mob_id, scenarios in patches[rank].items():
            target = by_id.get(mob_id)
            if target is None:
                continue
            name_zh, name_en = names[mob_id]
            for payload in scenarios.values():
                buckets = ([payload["lines"]] if "lines" in payload else
                           [payload.get("generic", [])] +
                           list((payload.get("by_damage") or {}).values()))
                for bucket in buckets:
                    for line in bucket:
                        zh = line["zh"]
                        if zh in seen:
                            duplicates += 1
                            line["zh"] = f"{zh}（{name_zh}）"
                            line["en"] = f"{line['en']} ({name_en})" if name_en else line["en"]
                        seen[line["zh"]] = mob_id
            target["scenarios"] = scenarios
            merged += 1
        if not args.dry_run:
            tmp = path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(mod_data, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(path)

    total = sum(
        1
        for path in (DATA / "mods").glob("*.json")
        for _ in json.loads(path.read_text(encoding="utf-8"))["mobs"]
    )
    print(f"mods written={len(patches)} merged mobs={merged} "
          f"unique lines={len(seen)} duplicate lines fixed={duplicates} total mobs={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
