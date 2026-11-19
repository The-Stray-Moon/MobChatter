"""Generate per-mob unique dialogue with local Ollama qwen2.5.

Each mob is generated in scenario groups (one request per group) so the model
never has to emit a huge single response. Requests carry the mod name and the
mod introduction alongside the mob, so lines stay tied to the mod's setting.

Only batches reserved in data/dialogue/unique/local_assignment.json are
touched, so this runner never collides with agent-written shards. Batch files
are merge-on-write and validated before they land.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import unique_dialogue as ud

DATA = Path(__file__).resolve().parent.parent / "data" / "dialogue"
UNIQUE = DATA / "unique"
RESERVED = UNIQUE / "local_assignment.json"
LOG = DATA / "local-qwen.log"
OLLAMA = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")

GROUPS = [["walk", "idle"], ["look_player", "tempted"], ["collide", "mate"],
          ["pickup", "target_acquire"], ["targeting", "melee_attack"], ["spawn"]]
DAMAGE = ud.DAMAGE
DAMAGE_ZH = {"fire": "火焰", "fall": "摔落", "drown": "溺水", "explosion": "爆炸",
             "projectile": "投射物", "magic": "魔法", "starvation": "饥饿",
             "lightning": "雷击", "void": "虚空"}


def log(line: str) -> None:
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(time.strftime("%Y-%m-%d %H:%M:%S ") + line + "\n")


def call(prompt: str, num_predict: int = 1200) -> dict | None:
    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0.9, "top_p": 0.95, "num_ctx": 4096,
                    "num_predict": num_predict},
    }
    request = urllib.request.Request(
        OLLAMA, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.loads(json.loads(response.read())["response"])
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
        return None


def who(ctx: dict) -> str:
    name = ctx["name_zh"] or ctx["name_en"]
    return (f"模组：{ctx['mod']}\n模组简介：{ctx['mod_intro']}\n"
            f"生物：{name} / {ctx['name_en']}（{ctx['mob_id']}）\n"
            f"生物简介：{ctx['description']}\n类别：{ctx['archetype']}\n")


def pick_lines(raw, count: int) -> list[dict]:
    out, seen = [], set()
    if not isinstance(raw, list):
        return out
    for item in raw:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            zh, en = item[0], item[1]
        elif isinstance(item, dict):
            zh, en = item.get("zh"), item.get("en")
        else:
            continue
        zh, en = str(zh or "").strip(), str(en or "").strip()
        if not zh or not en or zh in seen or "\ufffd" in zh or "\ufffd" in en:
            continue
        if len(zh) < 3 or len(en.split()) < 2:
            continue
        seen.add(zh)
        out.append({"zh": zh, "en": en})
        if len(out) >= count:
            break
    return out


def top_up(ctx: dict, scenario: str, have: list[dict], count: int,
           hint: str = "") -> list[dict]:
    """Ask only for the lines still missing for one scenario.

    A 7B model regularly stops one or two lines short of ten, so retrying the
    whole group wastes time; this fills the gap and rejects duplicates.
    """
    attempts = 0
    while len(have) < count and attempts < 4:
        attempts += 1
        missing = count - len(have)
        prompt = (
            "你是 Minecraft 生物头顶台词作者。" + who(ctx)
            + f"情景：{scenario}{hint}\n"
            f"只输出 JSON 对象 {{\"lines\": [[\"中文\",\"English\"], ...]}}，lines 恰好 {missing + 1} 项。"
            "每句中文 6-22 字，英文意思一致，句子之间不得重复，"
            "也不要和这些已有句子重复：" + json.dumps([l["zh"] for l in have], ensure_ascii=False)
            + "\n不要解释，不要 Markdown。\n"
        )
        data = call(prompt, num_predict=900)
        extra = pick_lines(data.get("lines") if isinstance(data, dict) else None, missing + 1)
        seen = {line["zh"] for line in have}
        for line in extra:
            if line["zh"] in seen:
                continue
            seen.add(line["zh"])
            have.append(line)
            if len(have) >= count:
                break
    return have


def gen_group(ctx: dict, group: list[str], need: dict) -> dict | None:
    keys = "、".join(group)
    counts = "、".join(f"{key}={need[key]}" for key in group)
    prompt = (
        "你是 Minecraft 生物头顶台词作者。" + who(ctx)
        + "要求：以该生物第一人称写简短、有个性的中英对照台词。"
        "必须体现上面两份简介里明确写出的外形、习性、环境、机制、攻击或掉落；"
        "简介没写的食物、驯服、繁殖、掉落、弱点不要编造。"
        "所有中文句子互不重复，也不要只是把名字重复一遍。"
        f"为以下情景写台词，句数：{counts}。\n"
        "只输出合法 JSON 对象，键为情景名，值为 [[\"中文\",\"English\"], ...] 列表，"
        "不要解释，不要 Markdown。\n"
    )
    result: dict[str, list[dict]] = {}
    for _ in range(2):
        data = call(prompt, num_predict=1600)
        if not isinstance(data, dict):
            continue
        for key in group:
            lines = pick_lines(data.get(key), need[key])
            if len(lines) > len(result.get(key, [])):
                result[key] = lines
        if all(len(result.get(key, [])) >= need[key] for key in group):
            return result
    for key in group:
        result[key] = top_up(ctx, key, result.get(key, []), need[key])
    if all(len(result[key]) >= need[key] for key in group):
        return {key: result[key][: need[key]] for key in group}
    missing = "、".join(f"{key}={len(result.get(key, []))}/{need[key]}" for key in group)
    log(f"SHORT {ctx['mob_id']} group {missing}")
    return None


def gen_hurt(ctx: dict, need: dict) -> dict | None:
    """Two small requests: generic lines, then nine flat damage pairs.

    A single combined request makes a 7B model collapse generic into one pair,
    so the two parts are asked for separately and zipped by fixed order.
    """
    count = need["hurt"]
    generic_prompt = (
        "你是 Minecraft 生物头顶台词作者。" + who(ctx)
        + f"只输出 JSON 对象 {{\"lines\": [[\"中文\",\"English\"], ...]}}，lines 至少 {count} 项，"
        "内容是该生物通用受伤时说的话（挨打、掉血、被击退），不区分伤害原因。"
        "每句中文不少于 6 个字且互不重复，英文是一个完整短句。不要解释，不要 Markdown。\n"
    )
    generic: list[dict] = []
    for _ in range(2):
        data = call(generic_prompt, num_predict=1400)
        lines = pick_lines(data.get("lines") if isinstance(data, dict) else None, count)
        if len(lines) > len(generic):
            generic = lines
        if len(generic) >= count:
            break
    if len(generic) < count:
        generic = top_up(ctx, "hurt.generic", generic, count, "（通用受伤）")
    if len(generic) < count:
        log(f"SHORT {ctx['mob_id']} hurt.generic {len(generic)}/{count}")
        return None
    generic = generic[:count]

    order = "、".join(f"{index + 1}.{DAMAGE_ZH[d]}" for index, d in enumerate(DAMAGE))
    damage_prompt = (
        "你是 Minecraft 生物头顶台词作者。" + who(ctx)
        + f"只输出 JSON 对象 {{\"lines\": [[\"中文\",\"English\"], ...]}}，lines 恰好 {len(DAMAGE)} 项，"
        f"依次对应这些受伤原因：{order}。"
        "每句要能听出对应原因，同时仍符合该生物设定；中文互不重复。"
        "不要解释，不要 Markdown。\n"
    )
    for _ in range(4):
        data = call(damage_prompt, num_predict=1400)
        lines = pick_lines(data.get("lines") if isinstance(data, dict) else None, len(DAMAGE))
        if len(lines) < len(DAMAGE):
            log(f"SHORT {ctx['mob_id']} hurt.damage {len(lines)}/{len(DAMAGE)}")
            continue
        return {"generic": generic,
                "by_damage": {damage: [lines[index]] for index, damage in enumerate(DAMAGE)}}
    return None


def generate(ctx: dict) -> dict | None:
    need = {key: min(value, 10) if key != "hurt" else min(value, 10)
            for key, value in ctx["counts"].items()}
    scenarios: dict = {}
    for group in GROUPS:
        part = gen_group(ctx, group, need)
        if not part:
            log(f"FAIL {ctx['mob_id']} group={'/'.join(group)}")
            return None
        scenarios.update(part)
    hurt = gen_hurt(ctx, need)
    if not hurt:
        log(f"FAIL {ctx['mob_id']} hurt")
        return None
    scenarios["hurt"] = hurt
    return {"mob_id": ctx["mob_id"], "rank": ctx["rank"], "name_en": ctx["name_en"],
            "name_zh": ctx["name_zh"], "scenarios": scenarios}


def write_entry(batch: str, entry: dict) -> None:
    path = UNIQUE / f"{batch}.json"
    data = {"batch": batch, "mobs": []}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data.setdefault("batch", batch)
            data.setdefault("mobs", [])
        except Exception:  # noqa: BLE001
            return
    data["mobs"] = [m for m in data["mobs"]
                    if not (m.get("mob_id") == entry["mob_id"]
                            and m.get("rank") in (None, entry["rank"]))]
    data["mobs"].append(entry)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def reserved_batches() -> set[str]:
    if not RESERVED.exists():
        return set()
    return set(json.loads(RESERVED.read_text(encoding="utf-8")).get("batches", []))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--batch", default="")
    args = parser.parse_args()

    plan = ud.load_plan()
    intros = ud.load_intros()
    reserve = reserved_batches()
    if args.batch:
        reserve = {args.batch}
    _, remaining = ud.covered()
    todo = [(batch, mob) for batch, mob in remaining if batch in reserve]
    if args.limit:
        todo = todo[: args.limit]
    log(f"START workers={args.workers} mobs={len(todo)} model={MODEL}")
    print(f"queued mobs={len(todo)}", flush=True)
    written = failed = 0

    def work(item):
        batch, mob = item
        ctx = ud.context_for(batch, mob, intros)
        entry = generate(ctx)
        if not entry:
            return "fail"
        problems = ud.validate_mob(mob, entry, strict=False)
        if problems:
            log(f"INVALID {mob['mob_id']} {'; '.join(problems[:4])}")
            return "fail"
        write_entry(batch, entry)
        return "ok"

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for index, result in enumerate(pool.map(work, todo), 1):
            written += result == "ok"
            failed += result == "fail"
            if index % 5 == 0:
                print(f"[{index}/{len(todo)}] ok={written} fail={failed}", flush=True)
    log(f"DONE ok={written} fail={failed}")
    print(f"done ok={written} fail={failed}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
