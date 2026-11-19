"""Clean artifacts left by the local model before the merge runs.

The local qwen runner produced a few lines where the Chinese half was a literal
echo of an English prompt word (for example "whisper" with 中文 "低语"). Those
read as placeholders in game, so every affected line is either repaired in place
or dropped when the Chinese text carries no meaning.

Also drops lines that fail the basic shape check (any Chinese, some English).

    python tools/clean_unique.py [--write]
"""
from __future__ import annotations

import argparse
import json
import re
import sys

import unique_dialogue as ud

# English tokens the model sometimes echoed literally into the Chinese slot.
ECHOES = {
    "whisper": "低语", "Whisper": "低语", "growl": "低吼", "hiss": "嘶声",
    "roar": "咆哮", "snarl": "低吼", "chirp": "鸣叫", "screech": "尖啸",
}
CJK = re.compile(r"[\u3400-\u9fff]")


def clean_scenarios(scenarios: dict) -> int:
    removed = 0

    def fix(lines):
        nonlocal removed
        out = []
        for line in lines or []:
            if isinstance(line, (list, tuple)) and len(line) >= 2:
                # Batches written before write_unique.py stored pairs as arrays.
                zh, en = line[0], line[1]
                ordinal = True
            elif isinstance(line, dict):
                zh, en = line.get("zh"), line.get("en")
                ordinal = False
            else:
                removed += 1
                continue
            zh = str(zh or "").strip()
            en = str(en or "").strip()
            if not zh or not en or "\ufffd" in zh or "\ufffd" in en:
                removed += 1
                continue
            if not CJK.search(zh):
                # A Chinese slot without any Chinese character is an echo of
                # the prompt; translate the obvious tokens, otherwise drop it.
                replaced = None
                for token, word in ECHOES.items():
                    if token.lower() in zh.lower():
                        replaced = word
                        break
                if replaced is None:
                    removed += 1
                    continue
                zh = replaced
            out.append({"zh": zh, "en": en})
        return out

    for scenario in list(scenarios):
        payload = scenarios[scenario]
        if scenario == "hurt":
            if not isinstance(payload, dict):
                continue
            payload["generic"] = fix(payload.get("generic"))
            for damage, lines in list((payload.get("by_damage") or {}).items()):
                cleaned = fix(lines)[:1]
                if cleaned:
                    payload["by_damage"][damage] = cleaned
                else:
                    payload["by_damage"].pop(damage, None)
        elif isinstance(payload, list):
            scenarios[scenario] = fix(payload)
        elif isinstance(payload, dict) and "lines" in payload:
            payload["lines"] = fix(payload["lines"])
    return removed


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args()

    touched = removed_total = 0
    for path in sorted(ud.UNIQUE.glob("u*.json")):
        if not path.stem[1:].isdigit():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        removed = 0
        for entry in data.get("mobs", []):
            removed += clean_scenarios(entry.get("scenarios") or {})
        if removed:
            touched += 1
            removed_total += removed
            if options.write:
                tmp = path.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
                tmp.replace(path)
    print(f"batches touched={touched} lines removed={removed_total} written={options.write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
