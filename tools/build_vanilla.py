"""Build the vanilla mob table for Minecraft 26.1 from the official client jar
and the Chinese Minecraft Wiki API.

Writes data/mobs/0.json (rank 0) and data/vanilla/profiles.json.
"""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
VANILLA = DATA / "vanilla"
UA = "MobChatter/1.0 (local research script)"

MOBS = [
    "allay", "armadillo", "axolotl", "bat", "bee", "blaze", "bogged", "breeze",
    "camel", "camel_husk", "cat", "cave_spider", "chicken", "cod", "copper_golem",
    "cow", "creaking", "creeper", "dolphin", "donkey", "drowned", "elder_guardian",
    "ender_dragon", "enderman", "endermite", "evoker", "fox", "frog", "ghast", "giant",
    "glow_squid", "goat", "guardian", "happy_ghast", "hoglin", "horse", "husk",
    "illusioner", "iron_golem", "killer_bunny", "llama", "magma_cube", "mooshroom",
    "mule", "nautilus", "ocelot", "panda", "parched", "parrot", "phantom", "pig",
    "piglin", "piglin_brute", "pillager", "polar_bear", "pufferfish", "rabbit",
    "ravager", "salmon", "sheep", "shulker", "silverfish", "skeleton",
    "skeleton_horse", "slime", "sniffer", "snow_golem", "spider", "squid", "stray",
    "strider", "tadpole", "trader_llama", "tropical_fish", "turtle", "vex",
    "villager", "vindicator", "wandering_trader", "warden", "witch", "wither",
    "wither_skeleton", "wolf", "zoglin", "zombie", "zombie_horse", "zombie_nautilus",
    "zombie_villager", "zombified_piglin",
]


def api(params: dict) -> dict:
    url = "https://zh.minecraft.wiki/api.php?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:
            time.sleep(1 + attempt)
    return {}


def zh_page_for(name: str) -> tuple[str, str]:
    result = api({"action": "query", "list": "search", "srsearch": name, "format": "json", "srlimit": 3})
    hits = (result.get("query") or {}).get("search") or []
    for hit in hits:
        title = hit.get("title", "")
        if title and not any(x in title for x in ("消歧义", "分类", "模板")):
            return title, hit.get("snippet", "")
    return "", ""


def zh_extract(title: str) -> str:
    result = api({"action": "query", "titles": title, "prop": "extracts", "explaintext": 1, "format": "json", "redirects": 1})
    pages = (result.get("query") or {}).get("pages") or {}
    for page in pages.values():
        return page.get("extract", "") or ""
    return ""


def first_sentences(text: str, limit: int = 3, max_chars: int = 220) -> str:
    text = re.sub(r"==+[^=]+==+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[。！？])", text)
    out = "".join(parts[:limit]).strip()
    if len(out) > max_chars:
        out = out[:max_chars].rstrip("，。；、") + "。"
    return out


def main() -> int:
    entities = json.loads((VANILLA / "entities.json").read_text(encoding="utf-8"))
    en_map = {key.split(".")[-1]: name for key, name in entities["en"].items()}
    rows, profiles = [], {}
    for mob_id in MOBS:
        en = en_map.get(mob_id)
        if not en:
            print("skip (no lang):", mob_id)
            continue
        title, _ = zh_page_for(en)
        text = zh_extract(title) if title else ""
        desc = first_sentences(text)
        if not desc:
            desc = f"{en} 是 Minecraft 26.1 加入的生物。"
        rows.append(
            {
                "mob_id": f"minecraft:{mob_id}",
                "name_en": en,
                "name_zh": title,
                "description_zh": desc,
                "source": "vanilla",
                "source_url": f"https://zh.minecraft.wiki/w/{urllib.parse.quote(title)}" if title else "https://minecraft.wiki/",
                "confidence": 0.9 if text else 0.5,
                "notes": "Minecraft 26.1 原版生物；中文名与简介取自中文 Minecraft Wiki。",
            }
        )
        profiles[f"minecraft:{mob_id}"] = {"en": en, "zh": title, "desc": desc}
        print(f"{mob_id:>16} -> {title or '?'} | {desc[:40]}")
        time.sleep(0.35)

    (DATA / "mobs").mkdir(parents=True, exist_ok=True)
    (DATA / "mobs" / "0.json").write_text(
        json.dumps(
            {"rank": 0, "mod": "Minecraft 26.1", "mod_url": "https://www.minecraft.net/", "mobs": rows},
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    (VANILLA / "profiles.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"vanilla mobs: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
