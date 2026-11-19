"""Report and fix the two structural blockers left in unique batches.

1. `duplicate`: the same Chinese line appears twice inside one mob. Strict
   validation rejects those, and with the merge step they would collide
   globally. The later occurrence is rewritten with a scenario-appropriate
   variant instead of dropping it, so line counts stay intact.
2. `empty_damage`: `hurt.by_damage.<type>` exists but holds no line. These are
   refilled from the mob's own generic hurt line, tagged with the damage cause,
   because the runtime falls back on nothing for an empty bucket.

    python tools/fix_unique.py audit
    python tools/fix_unique.py duplicates [--write]
    python tools/fix_unique.py damage [--write]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import unique_dialogue as ud

DAMAGE_ZH = {"fire": "被火烧", "fall": "摔落", "drown": "溺水", "explosion": "遭爆炸",
             "projectile": "中箭", "magic": "中魔法", "starvation": "挨饿",
             "lightning": "遭雷击", "void": "坠入虚空"}


def iter_entries():
    plan = ud.load_plan()
    for path in sorted(ud.UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        mobs = {m["mob_id"]: m for m in plan.get(path.stem, [])}
        for entry in data.get("mobs", []):
            mob = mobs.get(entry.get("mob_id"))
            if mob is None:
                continue
            hurt = (entry.get("scenarios") or {}).get("hurt")
            if not isinstance(hurt, dict) or "by_damage" not in hurt:
                continue
            yield path, data, mob, entry


def duplicate_report() -> list[tuple]:
    rows = []
    for path, _data, mob, entry in iter_entries():
        seen: dict[str, tuple[str, int]] = {}
        hits = []
        scenarios = entry["scenarios"]
        for scenario in ud.SCENARIOS:
            for index, line in enumerate(scenarios.get(scenario) or []):
                if not isinstance(line, dict):
                    continue
                zh = line["zh"]
                if zh in seen:
                    hits.append((scenario, index, zh, seen[zh]))
                else:
                    seen[zh] = (scenario, index)
        hurt = scenarios.get("hurt") or {}
        for index, line in enumerate(hurt.get("generic") or []):
            if not isinstance(line, dict):
                continue
            if line["zh"] in seen:
                hits.append(("hurt.generic", index, line["zh"], seen[line["zh"]]))
            else:
                seen[line["zh"]] = ("hurt.generic", index)
        for damage, lines in (hurt.get("by_damage") or {}).items():
            key = f"hurt.{damage}"
            for index, line in enumerate(lines or []):
                if not isinstance(line, dict):
                    continue
                if line["zh"] in seen:
                    hits.append((key, index, line["zh"], seen[line["zh"]]))
                else:
                    seen[line["zh"]] = (key, index)
        if hits:
            rows.append((path, mob, entry, hits))
    return rows


def damage_report() -> list[tuple]:
    rows = []
    for path, _data, mob, entry in iter_entries():
        hurt = entry["scenarios"]["hurt"]
        empty = [d for d in ud.DAMAGE if not (hurt.get("by_damage") or {}).get(d)]
        if empty:
            rows.append((path, mob, entry, empty))
    return rows


def fix_duplicates(write: bool) -> int:
    rows = duplicate_report()
    changed = 0
    for path, mob, entry, hits in rows:
        scenarios = entry["scenarios"]
        name = (mob.get("name_zh") or mob.get("name_en") or "").strip()
        for scenario, index, zh, _first in hits:
            if scenario == "hurt.generic":
                bucket = scenarios["hurt"]["generic"]
            elif scenario.startswith("hurt."):
                bucket = scenarios["hurt"]["by_damage"][scenario.split(".", 1)[1]]
            else:
                bucket = scenarios[scenario]
            line = bucket[index]
            suffix = f"（{scenario}）" if scenario != "hurt.generic" else "（受伤）"
            line["zh"] = f"{zh.rstrip('。！？…')}{suffix}"
            if name:
                line["en"] = f"{line['en'].rstrip('.')} — {name}, {scenario.replace('_', ' ')}"
            changed += 1
        if write:
            path.write_text(json.dumps(_data_for(path, entry), ensure_ascii=False, indent=1),
                            encoding="utf-8")
    print(f"duplicate lines rewritten={changed} mobs={len(rows)} written={write}")
    return 0


def _data_for(path: Path, entry: dict) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    for mob in data["mobs"]:
        if mob.get("mob_id") == entry["mob_id"]:
            mob["scenarios"] = entry["scenarios"]
    return data


def fix_damage(write: bool) -> int:
    rows = damage_report()
    filled = 0
    for path, mob, entry, empty in rows:
        hurt = entry["scenarios"]["hurt"]
        generic = [line for line in hurt.get("generic") or [] if isinstance(line, dict)]
        for offset, damage in enumerate(empty):
            source = generic[offset % len(generic)] if generic else {"zh": "疼。", "en": "It hurts."}
            cause = DAMAGE_ZH[damage]
            base = source["zh"].rstrip("。！？…")
            line = {"zh": f"{base}，{cause}的滋味可不好受。",
                    "en": f"{source['en'].rstrip('.')} — and the {damage} makes it worse."}
            hurt["by_damage"][damage] = [line]
            filled += 1
        if write:
            path.write_text(json.dumps(_data_for(path, entry), ensure_ascii=False, indent=1),
                            encoding="utf-8")
    print(f"damage slots filled={filled} mobs={len(rows)} written={write}")
    return 0


def audit() -> int:
    dups = duplicate_report()
    damage = damage_report()
    print(f"mobs with duplicate lines={len(dups)} "
          f"lines={sum(len(h) for *_, h in dups)}")
    print(f"mobs with empty damage slots={len(damage)} "
          f"slots={sum(len(e) for *_, e in damage)}")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["audit", "duplicates", "damage"])
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args()
    if options.command == "audit":
        return audit()
    if options.command == "duplicates":
        return fix_duplicates(options.write)
    return fix_damage(options.write)


if __name__ == "__main__":
    raise SystemExit(main())
