"""Build the runtime dialogue resource for the mod.

Reads data/dialogue/mods/*.json and writes an XZ-compressed JSON map:
  { "modid:entity": { "walk": [["zh","en"], ...], "hurt.fire": [...] } }

Output: common/src/main/resources/assets/mobchatter/dialogue.json.xz
"""
from __future__ import annotations

import json
import lzma
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "dialogue" / "mods"
OUT = ROOT / "common" / "src" / "main" / "resources" / "assets" / "mobchatter" / "dialogue.json.xz"


def main() -> int:
    merged: dict[str, dict[str, list[list[str]]]] = {}
    for path in sorted(SRC.glob("*.json"), key=lambda p: int(p.stem)):
        data = json.loads(path.read_text(encoding="utf-8"))
        for mob in data.get("mobs", []):
            mob_id = mob["mob_id"]
            target = merged.setdefault(mob_id, {})
            for scenario, payload in mob.get("scenarios", {}).items():
                if scenario == "hurt":
                    buckets = {"hurt": payload.get("generic", [])}
                    for damage, lines in (payload.get("by_damage") or {}).items():
                        buckets[f"hurt.{damage}"] = lines
                else:
                    # mods/*.json from build_dialogue.py use {"lines": [...]};
                    # unique batches merged by merge_unique_dialogue.py keep the
                    # same shape, but tolerate a bare list from older files.
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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(merged, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    with lzma.open(OUT, "wb", format=lzma.FORMAT_XZ, preset=6) as handle:
        handle.write(raw)
    total = sum(len(v) for m in merged.values() for v in m.values())
    print(f"mobs={len(merged)} entries={total} raw={len(raw)/1024/1024:.1f}MiB xz={OUT.stat().st_size/1024/1024:.1f}MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
