"""Compose per-mob dialogue from archetype banks + per-mob profiles.

Outputs:
  data/dialogue/mods/<rank>.json   nested, one file per mod
  output/mob_dialogue.csv          flat, one row per line
  output/mob_dialogue_index.json   counts per mod / scenario

Source priority is not relevant here: lines are composed from the banks written
by the research swarm, with placeholders filled from each mob's own data.
"""
from __future__ import annotations

import csv
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import DATA_DIR, OUTPUT_DIR  # noqa: E402

BASE = 10
BANK_SIZE = 20
DAMAGE_FALLBACK = {
    "generic": "疼。",
    "fire": "烫！",
    "fall": "摔得够呛。",
    "drown": "喘不上气。",
    "explosion": "被炸飞了。",
    "projectile": "中箭了。",
    "magic": "这股力量不对。",
    "starvation": "饿得发昏。",
    "lightning": "被雷劈了。",
    "void": "在往下掉。",
}

VANILLA_ARCHETYPE = {
    "allay": "passive_pet", "armadillo": "passive_herbivore", "axolotl": "aquatic",
    "bat": "flying", "bee": "flying", "blaze": "hostile_ranged", "bogged": "undead",
    "breeze": "hostile_melee", "camel": "passive_herbivore", "camel_husk": "undead",
    "cat": "passive_pet", "cave_spider": "insect_arthropod", "chicken": "passive_herbivore",
    "cod": "aquatic", "copper_golem": "golem_construct", "cow": "passive_herbivore",
    "creaking": "plant_nature", "creeper": "hostile_melee", "dolphin": "aquatic",
    "donkey": "passive_herbivore", "drowned": "undead", "elder_guardian": "boss",
    "ender_dragon": "boss", "enderman": "end", "endermite": "insect_arthropod",
    "evoker": "illager", "fox": "passive_pet", "frog": "aquatic",
    "ghast": "nether", "giant": "hostile_melee", "glow_squid": "aquatic",
    "goat": "passive_herbivore", "guardian": "hostile_ranged", "happy_ghast": "flying",
    "hoglin": "nether", "horse": "passive_herbivore", "husk": "undead",
    "illusioner": "illager", "iron_golem": "golem_construct", "killer_bunny": "hostile_melee",
    "llama": "passive_herbivore", "magma_cube": "slime_gel", "mooshroom": "passive_herbivore",
    "mule": "passive_herbivore", "nautilus": "aquatic", "ocelot": "passive_pet",
    "panda": "passive_herbivore", "parched": "undead", "parrot": "passive_pet",
    "phantom": "undead", "pig": "passive_herbivore", "piglin": "nether",
    "piglin_brute": "nether", "pillager": "illager", "polar_bear": "hostile_melee",
    "pufferfish": "aquatic", "rabbit": "passive_herbivore", "ravager": "illager",
    "salmon": "aquatic", "sheep": "passive_herbivore", "shulker": "end",
    "silverfish": "insect_arthropod", "skeleton": "undead", "skeleton_horse": "undead",
    "slime": "slime_gel", "sniffer": "passive_herbivore", "snow_golem": "golem_construct",
    "spider": "insect_arthropod", "squid": "aquatic", "stray": "undead",
    "strider": "nether", "tadpole": "aquatic", "trader_llama": "passive_herbivore",
    "tropical_fish": "aquatic", "turtle": "aquatic", "vex": "flying",
    "villager": "npc_villager", "vindicator": "illager", "wandering_trader": "npc_villager",
    "warden": "boss", "witch": "illager", "wither": "boss",
    "wither_skeleton": "undead", "wolf": "passive_pet", "zoglin": "nether",
    "zombie": "undead", "zombie_horse": "undead", "zombie_nautilus": "aquatic",
    "zombie_villager": "undead", "zombified_piglin": "nether",
}

RULES = [
    ("boss", ("boss", "首领", "之王", "女王", "king", "queen", "lord", "titan", "world boss")),
    ("horror_stalker", ("horror", "stalker", "恐怖", "dweller", "scp", "creepy", "nightmare", "anomaly", "entity", "实体")),
    ("dragon", ("dragon", "wyvern", "drake", "龙", "飞龙")),
    ("digimon", ("digimon", "数码兽", "数码宝贝")),
    ("pokemon", ("pokemon", "宝可梦", "精灵宝可梦")),
    ("prehistoric", ("dinosaur", "prehistoric", "jurassic", "mammoth", "恐龙", "史前", "猛犸", "古生物")),
    ("aquatic", ("fish", "shark", "squid", "whale", "dolphin", "aquatic", "ocean", "sea", "鱼", "鲨", "鲸", "鱿", "海", "水母", "蟹", "虾")),
    ("flying", ("bird", "bat", "bee", "moth", "butterfly", "wasp", "鸟", "蝠", "蜂", "蝶", "蛾", "翼")),
    ("insect_arthropod", ("spider", "insect", "bug", "ant", "beetle", "scorpion", "蛛", "虫", "蚁", "蝎", "蜈蚣")),
    ("plant_nature", ("plant", "mushroom", "tree", "flower", "fungus", "vine", "草", "菌", "花", "树", "藤", "苔")),
    ("undead", ("zombie", "skeleton", "undead", "ghost", "wraith", "revenant", "尸", "骷髅", "亡灵", "幽", "鬼")),
    ("nether", ("nether", "piglin", "blaze", "ghast", "hoglin", "下界", "猪灵", "烈焰", "恶魂", "疣猪")),
    ("end", ("enderman", "shulker", "endermite", "末影", "末地", "潜影")),
    ("illager", ("pillager", "illager", "vindicator", "evoker", "ravager", "灾厄", "掠夺", "唤魔", "卫道")),
    ("golem_construct", ("golem", "construct", "傀儡", "构造体")),
    ("mechanical_tech", ("mech", "robot", "machine", "drone", "cyborg", "机甲", "机器", "机械", "无人机", "炮台")),
    ("magic_spirit", ("spirit", "demon", "familiar", "magic", "fairy", "灵", "魔", "妖", "使魔", "召唤")),
    ("slime_gel", ("slime", "gel", "ooze", "史莱姆", "黏液", "胶")),
    ("joke_meme", ("meme", "brain rot", "joke", "funny", "梗", "脑腐", "搞笑")),
    ("npc_villager", ("villager", "trader", "merchant", "npc", "村民", "商人", "旅商", "守卫")),
    ("humanoid_warrior", ("knight", "soldier", "warrior", "guard", "archer", "samurai", "ninja", "骑士", "士兵", "战士", "卫兵", "武士", "忍者", "弓手")),
    ("passive_pet", ("pet", "tame", "companion", "宠物", "伙伴", "驯服")),
]

HOSTILE_HINTS = (
    "hostile", "enemy", "monster", "attack", "aggressive", "敌对", "攻击", "怪物",
    "危险", "凶", "boss", "首领", "猎杀", "追击",
)

SOUNDS = {
    "passive_herbivore": "哞", "passive_pet": "呜", "aquatic": "咕噜", "flying": "扑棱",
    "hostile_melee": "低吼", "hostile_ranged": "嘶声", "undead": "咔哒", "nether": "呼哧",
    "end": "嗡鸣", "illager": "嘿", "boss": "轰鸣", "golem_construct": "吱呀",
    "horror_stalker": "低语", "dragon": "龙吟", "insect_arthropod": "窸窣",
    "plant_nature": "沙沙", "npc_villager": "嗯", "mechanical_tech": "滴滴",
    "magic_spirit": "呢喃", "prehistoric": "低鸣", "pokemon": "呜哇",
    "digimon": "嘀", "humanoid_warrior": "哼", "slime_gel": "啪叽", "joke_meme": "哈",
}

SOUNDS_EN = {
    "passive_herbivore": "moo", "passive_pet": "whine", "aquatic": "blub", "flying": "flap",
    "hostile_melee": "growl", "hostile_ranged": "hiss", "undead": "click", "nether": "huff",
    "end": "hum", "illager": "hey", "boss": "rumble", "golem_construct": "creak",
    "horror_stalker": "whisper", "dragon": "roar", "insect_arthropod": "skitter",
    "plant_nature": "rustle", "npc_villager": "hm", "mechanical_tech": "beep",
    "magic_spirit": "murmur", "prehistoric": "low rumble", "pokemon": "waha",
    "digimon": "beep", "humanoid_warrior": "huff", "slime_gel": "splat", "joke_meme": "ha",
}
MOTIFS_EN = {
    "passive_herbivore": "fodder", "passive_pet": "collar", "aquatic": "scales", "flying": "feathers",
    "hostile_melee": "claws", "hostile_ranged": "arrows", "undead": "bones", "nether": "flames",
    "end": "purple particles", "illager": "banner", "boss": "throne", "golem_construct": "iron blocks",
    "horror_stalker": "shadow", "dragon": "scales", "insect_arthropod": "carapace",
    "plant_nature": "petals", "npc_villager": "shelves", "mechanical_tech": "gears",
    "magic_spirit": "runes", "prehistoric": "fossils", "pokemon": "Poké Ball",
    "digimon": "data", "humanoid_warrior": "sword", "slime_gel": "goo", "joke_meme": "meme",
}
FOODS_EN = {
    "passive_herbivore": "grass", "passive_pet": "jerky", "aquatic": "small fish", "flying": "nectar",
    "hostile_melee": "raw meat", "hostile_ranged": "bread", "undead": "rotten flesh", "nether": "gold nuggets",
    "end": "chorus fruit", "illager": "bread", "boss": "offerings", "golem_construct": "iron ingots",
    "horror_stalker": "fear", "dragon": "prey", "insect_arthropod": "leaves",
    "plant_nature": "sunlight", "npc_villager": "bread", "mechanical_tech": "batteries",
    "magic_spirit": "incense", "prehistoric": "fern leaves", "pokemon": "berries",
    "digimon": "data", "humanoid_warrior": "rations", "slime_gel": "sugar", "joke_meme": "snacks",
}
HABITATS_EN = {
    "passive_herbivore": "meadow", "passive_pet": "village", "aquatic": "water", "flying": "sky",
    "hostile_melee": "the dark", "hostile_ranged": "high ground", "undead": "shadows", "nether": "the Nether",
    "end": "the End", "illager": "camp", "boss": "lair", "golem_construct": "village",
    "horror_stalker": "darkness", "dragon": "mountains", "insect_arthropod": "undergrowth",
    "plant_nature": "woods", "npc_villager": "village", "mechanical_tech": "factory",
    "magic_spirit": "altar", "prehistoric": "wilds", "pokemon": "the wilds",
    "digimon": "the digital world", "humanoid_warrior": "battlefield", "slime_gel": "caves", "joke_meme": "the internet",
}
PREY_EN = {"hostile": "you", "passive": "bugs"}
MOTIFS = {
    "passive_herbivore": "草料", "passive_pet": "项圈", "aquatic": "鳞片", "flying": "羽毛",
    "hostile_melee": "爪子", "hostile_ranged": "箭矢", "undead": "骨头", "nether": "火苗",
    "end": "紫色粒子", "illager": "旗帜", "boss": "王座", "golem_construct": "铁块",
    "horror_stalker": "影子", "dragon": "鳞甲", "insect_arthropod": "甲壳",
    "plant_nature": "花瓣", "npc_villager": "货架", "mechanical_tech": "齿轮",
    "magic_spirit": "符文", "prehistoric": "化石", "pokemon": "精灵球",
    "digimon": "数据", "humanoid_warrior": "佩剑", "slime_gel": "黏液", "joke_meme": "梗",
}

FOODS = {
    "passive_herbivore": "草", "passive_pet": "肉干", "aquatic": "小鱼", "flying": "花蜜",
    "hostile_melee": "生肉", "hostile_ranged": "面包", "undead": "腐肉", "nether": "金粒",
    "end": "紫颂果", "illager": "面包", "boss": "供品", "golem_construct": "铁锭",
    "horror_stalker": "恐惧", "dragon": "猎物", "insect_arthropod": "叶子",
    "plant_nature": "阳光", "npc_villager": "面包", "mechanical_tech": "电池",
    "magic_spirit": "香火", "prehistoric": "蕨叶", "pokemon": "树果",
    "digimon": "数据", "humanoid_warrior": "干粮", "slime_gel": "糖", "joke_meme": "零食",
}

HABITATS = {
    "passive_herbivore": "草地", "passive_pet": "村庄", "aquatic": "水里", "flying": "天空",
    "hostile_melee": "暗处", "hostile_ranged": "高地", "undead": "阴影", "nether": "下界",
    "end": "末地", "illager": "营地", "boss": "巢穴", "golem_construct": "村庄",
    "horror_stalker": "黑暗", "dragon": "山峰", "insect_arthropod": "草丛",
    "plant_nature": "林地", "npc_villager": "村庄", "mechanical_tech": "工厂",
    "magic_spirit": "祭坛", "prehistoric": "荒野", "pokemon": "野外",
    "digimon": "数据世界", "humanoid_warrior": "战场", "slime_gel": "洞穴", "joke_meme": "网络",
}

THEME_RULES = [
    ("horror_stalker", ("恐怖", "horror", "诡异", "惊悚", "灵异", "异常", "dweller")),
    ("magic_spirit", ("魔法", "法术", "magic", "spell", "奥术", "符文", "召唤", "仪式")),
    ("mechanical_tech", ("机械", "科技", "machine", "tech", "机甲", "工厂", "机器人", "自动化")),
    ("prehistoric", ("史前", "恐龙", "prehistoric", "化石", "古生物", "侏罗纪")),
    ("aquatic", ("海洋", "水下", "aquatic", "深海", "水族", "钓鱼")),
    ("nether", ("下界", "nether", "地狱")),
    ("end", ("末地", " end ", "虚空", "末影")),
    ("undead", ("亡灵", "undead", "僵尸", "骷髅", "尸")),
    ("humanoid_warrior", ("战争", "军队", "骑士", "soldier", "阵营", "战士", "中世纪")),
    ("plant_nature", ("自然", "植物", "森林", "农业", "farming", "生态")),
    ("dragon", ("龙", "dragon", "飞龙")),
    ("slime_gel", ("史莱姆", "粘液", "黏液", "slime")),
]
THEME_FALLBACK = {"horror_stalker", "magic_spirit", "mechanical_tech", "prehistoric", "dragon", "slime_gel"}
THEME_HABITAT = {"horror_stalker": "黑暗", "magic_spirit": "祭坛", "mechanical_tech": "工厂",
                 "prehistoric": "荒野", "aquatic": "水里", "nether": "下界", "end": "末地",
                 "undead": "阴影", "humanoid_warrior": "战场", "plant_nature": "林地",
                 "dragon": "山峰", "slime_gel": "洞穴"}
THEME_HABITAT_EN = {"horror_stalker": "darkness", "magic_spirit": "altar", "mechanical_tech": "factory",
                    "prehistoric": "wilds", "aquatic": "water", "nether": "the Nether", "end": "the End",
                    "undead": "shadows", "humanoid_warrior": "battlefield", "plant_nature": "woods",
                    "dragon": "mountains", "slime_gel": "caves"}
THEME_MOTIF = {"horror_stalker": "阴影", "magic_spirit": "符文", "mechanical_tech": "齿轮",
               "prehistoric": "化石", "aquatic": "鳞片", "nether": "火焰", "end": "紫色粒子",
               "undead": "骨头", "humanoid_warrior": "佩剑", "plant_nature": "花瓣",
               "dragon": "鳞甲", "slime_gel": "黏液"}
THEME_MOTIF_EN = {"horror_stalker": "shadow", "magic_spirit": "runes", "mechanical_tech": "gears",
                  "prehistoric": "fossils", "aquatic": "scales", "nether": "flames", "end": "purple particles",
                  "undead": "bones", "humanoid_warrior": "sword", "plant_nature": "petals",
                  "dragon": "scales", "slime_gel": "goo"}
THEME_WEIGHTS = {
    "horror_stalker": {"look_player": 0.3, "targeting": 0.2, "spawn": 0.2},
    "magic_spirit": {"target_acquire": 0.2, "targeting": 0.2},
    "mechanical_tech": {"targeting": 0.2, "melee_attack": 0.2},
    "prehistoric": {"walk": 0.2, "spawn": 0.2},
    "aquatic": {"walk": 0.2},
    "humanoid_warrior": {"targeting": 0.2, "melee_attack": 0.2},
}
MOTIF_WORDS = ("鳞片", "羽毛", "骨头", "爪子", "牙齿", "角", "尾巴", "翅膀", "外壳", "皮毛",
               "火焰", "冰", "雷", "毒", "影子", "齿轮", "花瓣", "宝石", "矿石", "旗帜",
               "王座", "箭", "盾", "剑", "触手", "眼睛", "孢子", "黏液", "符文", "铃铛",
               "面具", "藤蔓", "甲壳", "獠牙")


def mod_theme(intro: str) -> str:
    text = (intro or "").lower()
    for archetype, words in THEME_RULES:
        if any(word in text for word in words):
            return archetype
    return ""


def motif_of(row: dict, archetype: str, theme: str) -> tuple[str, str]:
    desc = row.get("description_zh", "")
    for word in MOTIF_WORDS:
        if word in desc:
            return word, MOTIFS_EN.get(archetype, "shape")
    if theme:
        return THEME_MOTIF.get(theme, MOTIFS.get(archetype, "身影")), THEME_MOTIF_EN.get(theme, MOTIFS_EN.get(archetype, "shape"))
    return MOTIFS.get(archetype, "身影"), MOTIFS_EN.get(archetype, "shape")


PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


def load_banks() -> dict[str, dict]:
    banks = {}
    for path in (DATA_DIR / "dialogue" / "banks").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        banks[data["archetype"]] = data["lines"]
    return banks


def classify(row: dict, theme: str = "") -> str:
    mob_id = row["mob_id"]
    if mob_id.startswith("minecraft:"):
        return VANILLA_ARCHETYPE.get(mob_id.split(":", 1)[1], "passive_herbivore")
    if row["mod_name"] == "Pixelmon":
        return "pokemon"
    if row["mod_name"] == "The Digimod":
        return "digimon"
    text = f"{row['name_en']} {row['description_zh']}".lower()
    for archetype, words in RULES:
        if any(word in text for word in words):
            return archetype
    animal_hints = ("牛", "羊", "猪", "鸡", "兔", "鱼", "鸟", "猫", "狗", "马", "动物", "家畜",
                    "cow", "sheep", "pig", "chicken", "rabbit", "fish", "bird")
    if theme in THEME_FALLBACK and len(row.get("description_zh", "")) < 70 and not any(h in text for h in animal_hints):
        return theme
    if any(word in text for word in HOSTILE_HINTS):
        return "hostile_melee"
    return "passive_herbivore"


def habitat_of(row: dict, archetype: str, theme: str = "") -> str:
    desc = row["description_zh"]
    for word in ("森林", "沙漠", "丛林", "沼泽", "雪原", "山地", "洞穴", "海洋", "河流", "下界", "末地", "平原", "草原", "恶地", "深暗之域"):
        if word in desc:
            return word
    return THEME_HABITAT.get(theme) or HABITATS.get(archetype, "野外")


def profile(row: dict, archetype: str, theme: str = "") -> dict:
    name_zh = row.get("name_zh") or row.get("name_en") or row["mob_id"]
    motif_zh, motif_en = motif_of(row, archetype, theme)
    hostile = archetype in ("hostile_melee", "hostile_ranged", "boss", "horror_stalker", "dragon", "illager", "undead", "nether", "end", "mechanical_tech")
    return {
        "name_zh": name_zh,
        "name_en": row.get("name_en") or name_zh,
        "sound_zh": SOUNDS.get(archetype, "声响"),
        "sound_en": SOUNDS_EN.get(archetype, "sound"),
        "habitat_zh": habitat_of(row, archetype, theme),
        "habitat_en": THEME_HABITAT_EN.get(theme) or HABITATS_EN.get(archetype, "the wilds"),
        "food_zh": FOODS.get(archetype, "食物"),
        "food_en": FOODS_EN.get(archetype, "food"),
        "prey_zh": "你" if hostile else "小虫",
        "prey_en": PREY_EN["hostile"] if hostile else PREY_EN["passive"],
        "motif_zh": motif_zh,
        "motif_en": motif_en,
    }


def fill(text: str, prof: dict, lang: str) -> str:
    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key == "name":
            return prof[f"name_{lang}"]
        if key == "name_en":
            return prof["name_en"]
        return prof.get(f"{key}_{lang}") or prof.get(key) or prof["name_zh"]

    return PLACEHOLDER_RE.sub(repl, text)


def pick(rng: random.Random, pool: list[dict], count: int) -> list[dict]:
    if count <= 0:
        return []
    if count <= len(pool):
        return rng.sample(pool, count)
    return pool + [pool[rng.randrange(len(pool))] for _ in range(count - len(pool))]



def weight_of(row: dict, archetype: str, scenario: str, archetypes: dict, theme: str = "") -> float:
    weight = float(archetypes[archetype]["weights"].get(scenario, 1.0))
    text = f"{row['name_en']} {row['description_zh']}".lower()
    if any(k in text for k in ("boss", "首领", "之王", "king", "queen")):
        if scenario in ("spawn", "target_acquire", "targeting"):
            weight += 0.4
    if any(k in text for k in ("tame", "驯服", "宠物", "pet", "companion")):
        if scenario in ("look_player", "tempted"):
            weight += 0.4
    if any(k in text for k in ("群居", "成群", "herd", "pack", "school")):
        if scenario in ("collide", "walk"):
            weight += 0.2
    if any(k in text for k in ("夜间", "夜行", "nocturnal", "night")):
        if scenario == "idle":
            weight += 0.2
    if any(k in text for k in ("骑乘", "mount", "ride")):
        if scenario in ("walk", "spawn"):
            weight += 0.2
    weight += THEME_WEIGHTS.get(theme, {}).get(scenario, 0.0)
    return round(weight, 2)

def compose_mod(rank: int, mod: str, mobs: list[dict], banks: dict, archetypes: dict, mod_intro: str = "") -> tuple[dict, list[dict]]:
    out_mobs, flat = [], []
    theme = mod_theme(mod_intro)
    for row in mobs:
        archetype = classify(row, theme)
        bank = banks.get(archetype)
        if not bank:
            archetype = "passive_herbivore"
            bank = banks[archetype]
        prof = profile(row, archetype, theme)
        weights = archetypes[archetype]["weights"]
        scenarios_out = {}
        for scenario, spec in bank.items():
            if scenario == "hurt":
                continue
            weight = weight_of(row, archetype, scenario, archetypes, theme)
            rng = random.Random(f"{row['mob_id']}:{scenario}")
            extra_count = min(len(spec) - BASE, max(0, round(BASE * (weight - 1))))
            chosen = pick(rng, spec, BASE + extra_count)
            base, extra = chosen[:BASE], chosen[BASE:]
            lines = []
            for kind, group in (("base", base), ("extra", extra)):
                for line in group:
                    lines.append(
                        {
                            "zh": fill(line["zh"], prof, "zh"),
                            "en": fill(line["en"], prof, "en"),
                            "kind": kind,
                            "weight": weight,
                        }
                    )
            scenarios_out[scenario] = {"weight": weight, "lines": lines}
            for index, line in enumerate(lines):
                flat.append(
                    {
                        "mod_rank": rank,
                        "mod_name": mod,
                        "mob_key": f"{rank}:{row['mob_id']}",
                        "mob_id": row["mob_id"],
                        "name_en": row["name_en"],
                        "name_zh": row.get("name_zh", ""),
                        "archetype": archetype,
                        "scenario": scenario,
                        "damage_type": "",
                        "line_index": index,
                        "kind": line["kind"],
                        "weight": weight,
                        "text_zh": line["zh"],
                        "text_en": line["en"],
                    }
                )
        hurt_spec = bank.get("hurt") or {}
        w_hurt = weight_of(row, archetype, "hurt", archetypes, theme)
        rng = random.Random(f"{row['mob_id']}:hurt")
        generic_pool = hurt_spec.get("generic", [])
        extra_count = min(len(generic_pool) - BASE, max(0, round(BASE * (w_hurt - 1))))
        chosen = pick(rng, generic_pool, BASE + extra_count)
        base, extra = chosen[:BASE], chosen[BASE:]
        generic_lines = []
        for kind, group in (("base", base), ("extra", extra)):
            for line in group:
                generic_lines.append({"zh": fill(line["zh"], prof, "zh"), "en": fill(line["en"], prof, "en"), "kind": kind, "weight": w_hurt})
        by_damage = {}
        damage_pools = {k: v for k, v in hurt_spec.items() if k != "generic" and isinstance(v, list)}
        for damage_type, pool in damage_pools.items():
            line = pool[rng.randrange(len(pool))]
            entry = {"zh": fill(line["zh"], prof, "zh"), "en": fill(line["en"], prof, "en"), "kind": "type", "weight": w_hurt}
            by_damage[damage_type] = [entry]
            generic_lines.append(entry)
            flat.append(
                {
                    "mod_rank": rank,
                    "mod_name": mod,
                    "mob_key": f"{rank}:{row['mob_id']}",
                        "mob_id": row["mob_id"],
                    "name_en": row["name_en"],
                    "name_zh": row.get("name_zh", ""),
                    "archetype": archetype,
                    "scenario": "hurt",
                    "damage_type": damage_type,
                    "line_index": len(generic_lines) - 1,
                    "kind": "type",
                    "weight": w_hurt,
                    "text_zh": entry["zh"],
                    "text_en": entry["en"],
                }
            )
        for damage_type, spec_lines in (("generic", generic_lines),):
            for index, line in enumerate(spec_lines):
                if line["kind"] == "type":
                    continue
                flat.append(
                    {
                        "mod_rank": rank,
                        "mod_name": mod,
                        "mob_key": f"{rank}:{row['mob_id']}",
                        "mob_id": row["mob_id"],
                        "name_en": row["name_en"],
                        "name_zh": row.get("name_zh", ""),
                        "archetype": archetype,
                        "scenario": "hurt",
                        "damage_type": damage_type,
                        "line_index": index,
                        "kind": line["kind"],
                        "weight": w_hurt,
                        "text_zh": line["zh"],
                        "text_en": line["en"],
                    }
                )
        scenarios_out["hurt"] = {"weight": w_hurt, "generic": generic_lines[: len(generic_lines) - len(by_damage)], "by_damage": by_damage}
        out_mobs.append(
            {
                "mob_key": f"{rank}:{row['mob_id']}",
                        "mob_id": row["mob_id"],
                "name_en": row["name_en"],
                "name_zh": row.get("name_zh", ""),
                "archetype": archetype,
                "scenarios": scenarios_out,
            }
        )
    return {"rank": rank, "mod": mod, "mobs": out_mobs}, flat


def main() -> int:
    archetypes_data = json.loads((DATA_DIR / "dialogue" / "archetypes.json").read_text(encoding="utf-8"))
    archetypes = {a["id"]: a for a in archetypes_data["archetypes"]}
    banks = load_banks()
    missing = sorted(set(archetypes) - set(banks))
    if missing:
        print("missing banks:", missing)
        return 2

    intro_map = {}
    with (OUTPUT_DIR / "top313_mob_mods.csv").open(encoding="utf-8-sig") as handle:
        for rec in csv.DictReader(handle):
            intro_map[int(rec["rank"])] = rec.get("intro_zh") or rec.get("summary") or ""

    rows = list(csv.DictReader(open(OUTPUT_DIR / "mob_descriptions.csv", encoding="utf-8-sig")))
    grouped: dict[int, list[dict]] = {}
    mod_names: dict[int, str] = {}
    for row in rows:
        rank = int(row["mod_rank"])
        grouped.setdefault(rank, []).append(row)
        mod_names[rank] = row["mod_name"]

    out_dir = DATA_DIR / "dialogue" / "mods"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "mob_dialogue.csv"
    tmp = csv_path.with_name(csv_path.name + ".new")
    fields = ["mod_rank", "mod_name", "mob_key", "mob_id", "name_en", "name_zh", "archetype", "scenario",
              "damage_type", "line_index", "kind", "weight", "text_zh", "text_en"]
    total_lines = 0
    total_mobs = 0
    index = {}
    with tmp.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rank in sorted(grouped):
            mod_json, flat = compose_mod(rank, mod_names[rank], grouped[rank], banks, archetypes, intro_map.get(rank, ""))
            (out_dir / f"{rank}.json").write_text(json.dumps(mod_json, ensure_ascii=False, indent=1), encoding="utf-8")
            writer.writerows(flat)
            total_lines += len(flat)
            total_mobs += len(grouped[rank])
            index[str(rank)] = {
                "mod": mod_names[rank],
                "mob_count": len(grouped[rank]),
                "line_count": len(flat),
            }
    try:
        tmp.replace(csv_path)
    except PermissionError:
        print(f"warning: {csv_path.name} locked; new content at {tmp.name}")
    (OUTPUT_DIR / "mob_dialogue_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"mods: {len(index)} | mobs: {total_mobs} | lines: {total_lines}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
