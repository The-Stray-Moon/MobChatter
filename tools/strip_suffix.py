"""Strip disambiguation suffixes that leaked into the source batches.

The merge step used to append "（生物名）" to repeated Chinese lines, and the
intra-mob dedupe appended "（scenario）". After restoring batches from
`data/dialogue/mods`, those suffixes became part of the source text.

Only a trailing parenthetical that names a known mob, the generic fallback
"生物", or a scenario key is removed, so genuine parentheses survive. Nested
names such as "（地狱男爵（2016版））" are matched greedily.

    python tools/strip_suffix.py [--write]
"""
from __future__ import annotations

import argparse
import json
import re
import sys

import unique_dialogue as ud

SCENARIOS = set(ud.SCENARIOS) | {"hurt"}
FALLBACK = {"生物", "受伤", "creature"}

ZH = re.compile(r"^(.*)（(.+)）\s*$")
EN_PAREN = re.compile(r"^(.*?)\s*\((.+)\)\s*$")
EN_DASH = re.compile(r"^(.*?)\s*—\s*(.+?),\s*([\w.]+)\s*$")


def known_names() -> tuple[set[str], set[str]]:
    zh, en = set(), set()
    for mobs in ud.load_plan().values():
        for mob in mobs:
            if mob.get("name_zh"):
                zh.add(mob["name_zh"].strip())
            if mob.get("name_en"):
                en.add(mob["name_en"].strip())
    return zh, en


def _suffix_sets(names: set[str]) -> tuple[set[str], set[str]]:
    zh = {f"（{token}）" for token in names}
    zh |= {f"（{token}）" for token in FALLBACK}
    zh |= {f"（{token}）" for token in SCENARIOS}
    en = {f" ({token})" for token in names}
    en |= {f" ({token})" for token in FALLBACK}
    en |= {f" ({token})" for token in SCENARIOS}
    return zh, en


def strip_zh(text: str, suffixes: set[str]) -> str:
    while True:
        hit = None
        for index, char in enumerate(text):
            if char == "（" and text[index:] in suffixes:
                hit = index
                break
        if hit is None:
            match = ZH.match(text)
            if not match:
                return text
            suffix = match.group(2).strip()
            if suffix in SCENARIOS or suffix.startswith("hurt."):
                text = match.group(1).rstrip()
                continue
            return text
        text = text[:hit].rstrip()


def strip_en(text: str, suffixes: set[str]) -> str:
    while True:
        hit = None
        for index, char in enumerate(text):
            if char == " " and text[index:] in suffixes:
                hit = index
                break
        if hit is not None:
            text = text[:hit].rstrip()
            continue
        match = EN_DASH.match(text)
        if match and (match.group(3).strip() in SCENARIOS
                      or match.group(3).strip().startswith("hurt.")):
            text = match.group(1).rstrip()
            continue
        return text


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args()

    zh_names, en_names = known_names()
    zh_suffixes, en_suffixes = _suffix_sets(zh_names | en_names)
    touched = changed = 0
    for path in sorted(ud.UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        hits = 0
        for entry in data.get("mobs", []):
            for value in (entry.get("scenarios") or {}).values():
                groups = []
                if isinstance(value, dict) and "generic" in value:
                    groups.append(value.get("generic") or [])
                    groups.extend((value.get("by_damage") or {}).values())
                elif isinstance(value, list):
                    groups.append(value)
                elif isinstance(value, dict):
                    groups.append(value.get("lines") or [])
                for group in groups:
                    for line in group:
                        if not isinstance(line, dict):
                            continue
                        zh = strip_zh(line.get("zh", ""), zh_suffixes)
                        en = strip_en(line.get("en", ""), en_suffixes)
                        if zh != line.get("zh") or en != line.get("en"):
                            hits += 1
                            if options.write:
                                line["zh"], line["en"] = zh, en
        if hits:
            touched += 1
            changed += hits
            if options.write:
                tmp = path.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
                tmp.replace(path)
    print(f"lines stripped={changed} batches={touched} written={options.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
