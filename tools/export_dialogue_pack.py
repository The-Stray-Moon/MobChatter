"""Export the packed dialogue library as a resource-pack source tree.

Writes ``dialogue-pack/pack.mcmeta`` and one JSON file per entity following the
patch format documented in ``docs/DIALOGUE_RESOURCE_PACKS.md``::

    dialogue-pack/assets/<namespace>/mobchatter/dialogue/<path>.json

Each entity file is self-contained (``mode: replace``), so it can be edited as
ordinary JSON, zipped as a resource pack, or packed back into
``assets/mobchatter/dialogue.json.xz`` by ``tools/build_mod_dialogue.py``.
"""
from __future__ import annotations

import argparse
import json
import lzma
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XZ = ROOT / "common" / "src" / "main" / "resources" / "assets" / "mobchatter" / "dialogue.json.xz"
MODS = ROOT / "data" / "dialogue" / "mods"
OUT = ROOT / "dialogue-pack"

# Stable scenario order for readable diffs; unknown scenarios go last, sorted.
SCENARIO_ORDER = [
    "walk", "idle", "look_player", "hurt", "tempted", "collide", "mate", "pickup",
    "target_acquire", "targeting", "melee_attack", "spawn",
    "hurt.fire", "hurt.fall", "hurt.drown", "hurt.explosion", "hurt.projectile",
    "hurt.magic", "hurt.starvation", "hurt.lightning", "hurt.void",
]
SCENARIO_RANK = {name: index for index, name in enumerate(SCENARIO_ORDER)}
ENTITY_ID = re.compile(r"[a-z0-9_.-]+:[a-z0-9_./-]+")

PACK_META = {
    "pack": {
        "pack_format": 15,
        "description": "MobChatter built-in dialogue source (development pack; adjust pack_format for other MC versions)",
    }
}


def load_xz() -> dict[str, dict[str, list[list[str]]]]:
    with lzma.open(XZ, "rb") as handle:
        return json.loads(handle.read())


def load_mods() -> dict[str, dict[str, list[list[str]]]]:
    merged: dict[str, dict[str, list[list[str]]]] = {}
    for path in sorted(MODS.glob("*.json"), key=lambda p: int(p.stem)):
        data = json.loads(path.read_text(encoding="utf-8"))
        for mob in data.get("mobs", []):
            target = merged.setdefault(mob["mob_id"], {})
            for scenario, payload in mob.get("scenarios", {}).items():
                if scenario == "hurt":
                    buckets = {"hurt": payload.get("generic", [])}
                    for damage, lines in (payload.get("by_damage") or {}).items():
                        buckets[f"hurt.{damage}"] = lines
                else:
                    buckets = {scenario: payload if isinstance(payload, list)
                               else payload.get("lines", [])}
                for key, lines in buckets.items():
                    pairs = target.setdefault(key, [])
                    seen = {(p[0], p[1]) for p in pairs}
                    for line in lines:
                        pair = [line["zh"], line["en"]]
                        if (pair[0], pair[1]) not in seen:
                            pairs.append(pair)
                            seen.add((pair[0], pair[1]))
    return merged


def entity_path(entity_id: str) -> Path:
    namespace, path = entity_id.split(":", 1)
    return Path("assets") / namespace / "mobchatter" / "dialogue" / f"{path}.json"


def render(entity_id: str, scenarios: dict[str, list[list[str]]]) -> str:
    names = sorted(scenarios, key=lambda name: (SCENARIO_RANK.get(name, len(SCENARIO_ORDER)), name))
    out = [
        "{",
        "  \"format_version\": 1,",
        "  \"mode\": \"replace\",",
        "  \"scenarios\": {",
    ]
    for index, name in enumerate(names):
        out.append(f"    {json.dumps(name, ensure_ascii=False)}: {{")
        lines = scenarios[name]
        if not lines:
            out.append("      \"operation\": \"disable\"")
        else:
            out.append("      \"operation\": \"replace\",")
            out.append("      \"lines\": [")
            for line_index, pair in enumerate(lines):
                line = json.dumps({"zh": pair[0], "en": pair[1]}, ensure_ascii=False)
                out.append(f"        {line}{',' if line_index + 1 < len(lines) else ''}")
            out.append("      ]")
        out.append(f"    }}{',' if index + 1 < len(names) else ''}")
    out.append("  }")
    out.append("}")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("xz", "mods"), default="xz",
                        help="read the shipped XZ (default) or the pipeline mods/*.json")
    parser.add_argument("--out", type=Path, default=OUT, help="output pack directory")
    args = parser.parse_args()

    entities = load_mods() if args.source == "mods" else load_xz()

    out = args.out
    expected: set[Path] = set()
    for entity_id, scenarios in entities.items():
        if not ENTITY_ID.fullmatch(entity_id):
            raise SystemExit(f"invalid entity id: {entity_id}")
        unknown = set(scenarios) - set(SCENARIO_RANK)
        if unknown:
            raise SystemExit(f"{entity_id}: unknown scenarios: {', '.join(sorted(unknown))}")
        relative = entity_path(entity_id)
        expected.add(relative)
        path = out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(entity_id, scenarios), encoding="utf-8", newline="\n")

    assets = out / "assets"
    stale = 0
    if assets.is_dir():
        for path in assets.rglob("*.json"):
            relative = path.relative_to(out)
            if relative not in expected:
                path.unlink()
                stale += 1
    meta = out / "pack.mcmeta"
    if not meta.exists():
        meta.parent.mkdir(parents=True, exist_ok=True)
        meta.write_text(json.dumps(PACK_META, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")

    total = sum(len(lines) for scenarios in entities.values() for lines in scenarios.values())
    print(f"source={args.source} entities={len(entities)} lines={total} "
          f"files={len(expected)} removed={stale} out={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
