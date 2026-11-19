"""Build a compact review queue for manual (agent) classification.

Prefilter is deliberately generous: any strong mob word in the name/summary, or
membership in the Modrinth "mobs" category. Output is split into chunks small
enough to read in one pass.

Usage: python tools/make_review_queue.py [--limit 900] [--chunk 250]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import DATA_DIR  # noqa: E402

STRONG = {
    "mob", "mobs", "creature", "creatures", "animal", "animals", "monster", "monsters",
    "boss", "bosses", "beast", "beasts", "pet", "pets", "dragon", "dragons", "npc",
    "wildlife", "fauna", "bestiary", "digimon", "yokai", "kaiju", "dinosaur",
    "zombie", "skeleton", "spider", "slime", "golem", "demon", "undead", "wyvern",
    "goblin", "orc", "fairy", "vampire", "werewolf", "mermaid", "griffin", "phoenix",
    "insect", "bugs", "fish", "birds", "shark", "whale", "snake", "lizard", "frog",
    "butterfly", "rabbit", "fox", "wolf", "wolves", "bear", "deer", "horse", "cow",
    "chicken", "sheep", "goat", "crab", "turtle", "penguin", "owl", "bat", "cats",
    "dogs", "tameable", "tame", "breed", "spawn egg", "mobs.",
}

EXCLUDE_CATEGORIES = {"optimization", "library", "management", "storage", "technology",
                      "equipment", "decoration", "transportation"}


def tokens(text: str) -> set[str]:
    ascii_text = unicodedata.normalize("NFKD", (text or "").lower()).encode("ascii", "ignore").decode()
    words = set(re.findall(r"[a-z][a-z'-]+", ascii_text))
    return {w[:-1] if len(w) > 3 and w.endswith("s") else w for w in words}


def matches(item: dict) -> bool:
    cats = {str(c).lower() for c in (item.get("categories") or [])}
    name_tokens = tokens(item.get("name"))
    summary_tokens = tokens(item.get("summary"))
    hits = (name_tokens | summary_tokens) & STRONG
    if hits:
        return True
    if "mobs" in cats and not (cats & EXCLUDE_CATEGORIES):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=900)
    parser.add_argument("--chunk", type=int, default=250)
    args = parser.parse_args()

    candidates = json.loads((DATA_DIR / "candidates.json").read_text(encoding="utf-8"))
    selected = [c for c in candidates if matches(c)]
    selected.sort(key=lambda c: -int(c.get("downloads_total") or 0))
    selected = selected[: args.limit]

    out_dir = DATA_DIR / "review"
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.glob("queue_*.txt"):
        stale.unlink()

    mapping = {}
    for start in range(0, len(selected), args.chunk):
        chunk = selected[start : start + args.chunk]
        lines = []
        for offset, item in enumerate(chunk, start + 1):
            key = f"{item['source']}:{item['source_id']}"
            mapping[str(offset)] = key
            summary = re.sub(r"\s+", " ", item.get("summary") or "")[:190]
            cats = ",".join((item.get("categories") or [])[:4])
            lines.append(
                f"#{offset}|{int(item.get('downloads_total') or 0)}|{item.get('name')}|{summary}|{cats}"
            )
        path = out_dir / f"queue_{start // args.chunk + 1:02d}.txt"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"{path.name}: {len(lines)} items")

    (out_dir / "queue_map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"total queued: {len(selected)} of {len(candidates)} candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
