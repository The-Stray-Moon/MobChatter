"""Build the runtime dialogue resource from the resource-pack source tree.

Reads ``dialogue-pack/assets/<namespace>/mobchatter/dialogue/**/*.json`` (the
JSON patch format documented in ``docs/DIALOGUE_RESOURCE_PACKS.md``) and writes
an XZ-compressed JSON map:
  { "modid:entity": { "walk": [["zh","en"], ...], "hurt.fire": [...] } }

Output: common/src/main/resources/assets/mobchatter/dialogue.json.xz
"""
from __future__ import annotations

import argparse
import json
import lzma
import os
import re
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dialogue-pack"
OUT = ROOT / "common" / "src" / "main" / "resources" / "assets" / "mobchatter" / "dialogue.json.xz"

SCENARIOS = {
    "walk", "idle", "look_player", "hurt", "tempted", "collide", "mate", "pickup",
    "target_acquire", "targeting", "melee_attack", "spawn", "hurt.fire", "hurt.fall",
    "hurt.drown", "hurt.explosion", "hurt.projectile", "hurt.magic", "hurt.starvation",
    "hurt.lightning", "hurt.void",
}
ENTITY_ID = re.compile(r"[a-z0-9_.-]+:[a-z0-9_./-]+")


def fail(path: Path, message: str) -> None:
    raise SystemExit(f"{path}: {message}")


def apply_patch(path: Path, target: dict[str, list[list[str]]],
                data: dict) -> dict[str, list[list[str]]]:
    if not isinstance(data, dict):
        fail(path, "expected object")
    unknown = set(data) - {"format_version", "mode", "scenarios"}
    if unknown:
        fail(path, f"unknown fields: {', '.join(sorted(unknown))}")
    version = data.get("format_version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        fail(path, "format_version must be 1")
    mode = data.get("mode", "merge")
    if mode not in ("merge", "replace"):
        fail(path, "mode must be merge or replace")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, dict):
        fail(path, "scenarios must be an object")

    result = {} if mode == "replace" else {key: list(value) for key, value in target.items()}
    for scenario, change in scenarios.items():
        if scenario not in SCENARIOS:
            fail(path, f"unknown scenario: {scenario}")
        if not isinstance(change, dict):
            fail(path, f"scenarios.{scenario}: expected object")
        unknown = set(change) - {"operation", "lines"}
        if unknown:
            fail(path, f"scenarios.{scenario}: unknown fields: {', '.join(sorted(unknown))}")
        operation = change.get("operation")
        if operation == "disable":
            if "lines" in change:
                fail(path, f"scenarios.{scenario}.lines: not allowed for disable")
            result[scenario] = []
            continue
        if operation not in ("append", "replace"):
            fail(path, f"scenarios.{scenario}.operation: expected append, replace or disable")
        lines = change.get("lines")
        if not isinstance(lines, list) or not lines:
            fail(path, f"scenarios.{scenario}.lines: expected non-empty array")
        pairs: list[list[str]] = []
        if operation == "append":
            pairs.extend(result.get(scenario, []))
        seen = {(pair[0], pair[1]) for pair in pairs}
        for index, line in enumerate(lines):
            if not isinstance(line, dict) or set(line) != {"zh", "en"}:
                fail(path, f"scenarios.{scenario}.lines[{index}]: expected zh and en")
            zh, en = line["zh"], line["en"]
            if not isinstance(zh, str) or not zh.strip() or not isinstance(en, str) or not en.strip():
                fail(path, f"scenarios.{scenario}.lines[{index}]: expected non-empty strings")
            if (zh, en) not in seen:
                pairs.append([zh, en])
                seen.add((zh, en))
        result[scenario] = pairs
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=SRC, help="resource-pack source directory")
    parser.add_argument("--out", type=Path, default=OUT, help="output XZ file")
    args = parser.parse_args()

    merged: dict[str, dict[str, list[list[str]]]] = {}
    for path in sorted(args.src.glob("assets/*/mobchatter/dialogue/**/*.json")):
        parts = path.relative_to(args.src).parts
        namespace = parts[1]
        entity_id = f"{namespace}:{'/'.join(parts[4:])[:-5]}"
        if not ENTITY_ID.fullmatch(entity_id):
            fail(path, f"invalid entity id: {entity_id}")
        data = json.loads(path.read_text(encoding="utf-8"))
        merged[entity_id] = apply_patch(path, merged.get(entity_id, {}), data)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(merged, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    fd, temp_name = tempfile.mkstemp(prefix=args.out.name + ".", suffix=".tmp", dir=args.out.parent)
    os.close(fd)
    temp = Path(temp_name)
    try:
        with lzma.open(temp, "wb", format=lzma.FORMAT_XZ, preset=6) as handle:
            handle.write(raw)
        for attempt in range(20):
            try:
                os.replace(temp, args.out)
                break
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.25)
    finally:
        if temp.exists():
            temp.unlink()
    total = sum(len(v) for m in merged.values() for v in m.values())
    print(f"mobs={len(merged)} entries={total} raw={len(raw)/1024/1024:.1f}MiB "
          f"xz={args.out.stat().st_size/1024/1024:.1f}MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
