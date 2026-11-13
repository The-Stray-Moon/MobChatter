"""Merge per-mob unique dialogue batches into data/dialogue/mods/<rank>.json.

Also enforces global uniqueness of Chinese lines: duplicate lines get the mob
name appended, so two creatures never render the exact same text.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dialogue"
UNIQUE = DATA / "unique"


def main() -> int:
    plan = json.loads((DATA / "unique_plan.json").read_text(encoding="utf-8"))
    seen: dict[str, str] = {}
    files = sorted(UNIQUE.glob("*.json"))
    merged_mobs = 0
    duplicates = 0

    for path in files:
        batch_id = path.stem
        batch = plan.get(batch_id)
        if not batch:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for index, mob in enumerate(data.get("mobs", [])):
            if index >= len(batch):
                break
            info = batch[index]
            rank = info["rank"]
            mod_path = DATA / "mods" / f"{rank}.json"
            mod_data = json.loads(mod_path.read_text(encoding="utf-8"))
            target = next((m for m in mod_data["mobs"] if m["mob_id"] == mob["mob_id"]), None)
            if target is None:
                continue
            name_zh = info.get("name_zh") or info.get("name_en")
            name_en = info.get("name_en") or name_zh
            for scenario, payload in mob["scenarios"].items():
                if scenario == "hurt":
                    groups = {"generic": payload.get("generic", [])}
                    for damage, lines in (payload.get("by_damage") or {}).items():
                        groups[f"hurt.{damage}"] = lines
                else:
                    groups = {scenario: payload}
                for key, lines in groups.items():
                    for line in lines:
                        zh = line["zh"].strip()
                        en = line["en"].strip()
                        if not zh or not en:
                            continue
                        if zh in seen:
                            duplicates += 1
                            zh = f"{zh}（{name_zh}）"
                            en = f"{en} ({name_en})"
                        seen[zh] = mob["mob_id"]
                        line["zh"] = zh
                        line["en"] = en
            target["scenarios"] = mob["scenarios"]
            mod_data["mobs"] = mod_data["mobs"]
            mod_path.write_text(json.dumps(mod_data, ensure_ascii=False, indent=1), encoding="utf-8")
            merged_mobs += 1

    total = sum(
        1
        for path in (DATA / "mods").glob("*.json")
        for mob in json.loads(path.read_text(encoding="utf-8"))["mobs"]
    )
    print(f"unique batches={len(files)} merged mobs={merged_mobs} duplicate lines fixed={duplicates} total mobs={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
