"""Generate per-mob unique dialogue with local Ollama qwen2.5.

Each mob is generated in 3 small requests (scenario groups) to avoid truncated
JSON. Resumable: valid data/dialogue/unique/<batch>.json files are skipped.
Progress goes to data/dialogue/ollama.log only.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dialogue"
UNIQUE = DATA / "unique"
PLAN = DATA / "unique_plan.json"
LOG = DATA / "ollama.log"
OLLAMA = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5:7b"

GROUPS = [
    ["walk", "idle", "look_player"],
    ["tempted", "collide", "mate"],
    ["pickup", "target_acquire", "targeting"],
    ["melee_attack", "spawn"],
]
DAMAGE = ["fire", "fall", "drown", "explosion", "projectile", "magic",
          "starvation", "lightning", "void"]


def log(line: str) -> None:
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(time.strftime("%Y-%m-%d %H:%M:%S ") + line + "\n")


def extra_for(weights: dict, scenario: str) -> int:
    return max(0, min(4, round(10 * (float(weights.get(scenario, 1.0)) - 1))))


def base_prompt(mob: dict) -> str:
    return (
        f"生物：{mob['name_zh']} / {mob['name_en']}\n"
        f"类别：{mob['archetype']}\n"
        f"设定：{(mob.get('description') or '')[:450]}\n"
        "要求：每句必须体现该生物的外形、叫声、食物、栖息地、习性、掉落、攻击或驯服方式；"
        "禁止通用废话，禁止与其他生物共用句子。中文6-20字，英文4-14词。\n"
    )


def prompt_group(mob: dict, group: list[str]) -> str:
    keys = ", ".join(group)
    return (
        "你是 Minecraft 生物台词作者。" + base_prompt(mob)
        + f"为这些情景各写 10 句中英对照台词：{keys}。\n"
        "严格输出 JSON 对象，键为情景名，值为 [{\"zh\":\"\",\"en\":\"\"}] 数组，"
        "每个键恰好 10 句，不要省略任何键。\n"
    )


def prompt_hurt(mob: dict) -> str:
    types = ", ".join(DAMAGE)
    return (
        "你是 Minecraft 生物台词作者。" + base_prompt(mob)
        + "写受伤台词：\"generic\" 10 句通用受伤；"
        + f"{types} 每种各 1 句，必须听得出受伤原因。\n"
        "严格输出 JSON：{\"generic\":[{\"zh\":\"\",\"en\":\"\"}],\"fire\":[...],...}，包含全部 9 个伤害键。\n"
    )


def call_ollama(prompt: str) -> dict:
    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.85, "num_ctx": 3072, "num_predict": 2000},
    }
    request = urllib.request.Request(
        OLLAMA, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=900) as response:
        return json.loads(json.loads(response.read())["response"])


def clean_lines(raw) -> list[dict]:
    out, seen = [], set()
    if not isinstance(raw, list):
        return out
    for item in raw:
        if not isinstance(item, dict):
            continue
        zh = str(item.get("zh", "")).strip()
        en = str(item.get("en", "")).strip()
        if not zh or not en or zh in seen:
            continue
        if len(zh) < 4 or len(en.split()) < 2:
            continue
        seen.add(zh)
        out.append({"zh": zh, "en": en})
    return out


def generate_group(mob: dict, group: list[str]) -> dict | None:
    for attempt in range(3):
        try:
            data = call_ollama(prompt_group(mob, group))
        except Exception as exc:  # noqa: BLE001
            log(f"ERR {mob['mob_id']} group {type(exc).__name__}")
            continue
        result = {}
        for key in group:
            lines = clean_lines(data.get(key))
            if len(lines) < 8:
                break
            result[key] = lines[: 10 + extra_for(mob.get("weights", {}), key)]
        if len(result) == len(group):
            return result
    return None


def generate_hurt(mob: dict) -> dict | None:
    for attempt in range(3):
        try:
            data = call_ollama(prompt_hurt(mob))
        except Exception:  # noqa: BLE001
            continue
        generic = clean_lines(data.get("generic"))
        if len(generic) < 8:
            continue
        by_damage = {damage: clean_lines(data.get(damage))[:1] for damage in DAMAGE}
        return {"generic": generic[:10], "by_damage": by_damage}
    return None


def generate_mob(mob: dict) -> dict | None:
    scenarios = {}
    for group in GROUPS:
        part = generate_group(mob, group)
        if not part:
            log(f"FAIL {mob['mob_id']} group={'/'.join(group)}")
            return None
        scenarios.update(part)
    hurt = generate_hurt(mob)
    if not hurt:
        log(f"FAIL {mob['mob_id']} hurt")
        return None
    scenarios["hurt"] = hurt
    return {
        "mob_id": mob["mob_id"],
        "rank": mob["rank"],
        "name_en": mob["name_en"],
        "name_zh": mob["name_zh"],
        "scenarios": scenarios,
    }


def valid_file(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return bool(data.get("mobs")) and all(m.get("scenarios") for m in data["mobs"])
    except Exception:  # noqa: BLE001
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--max-batches", type=int, default=0)
    args = parser.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    UNIQUE.mkdir(parents=True, exist_ok=True)

    todo = []
    for batch_id, mobs in plan.items():
        path = UNIQUE / f"{batch_id}.json"
        if path.exists() and valid_file(path):
            continue
        if path.exists():
            path.unlink()
        todo.append((batch_id, mobs))
    if args.max_batches:
        todo = todo[: args.max_batches]

    log(f"START batches={len(todo)} concurrency={args.concurrency} model={MODEL}")
    print(f"batches={len(todo)}", flush=True)

    def work(item):
        batch_id, mobs = item
        generated = [generate_mob(dict(mob)) for mob in mobs]
        generated = [m for m in generated if m]
        if not generated:
            log(f"EMPTY {batch_id}")
            return 0
        (UNIQUE / f"{batch_id}.json").write_text(
            json.dumps({"batch": batch_id, "mobs": generated}, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        log(f"OK {batch_id} {len(generated)}/{len(mobs)}")
        return len(generated)

    done_mobs = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(work, item) for item in todo]
        for index, future in enumerate(as_completed(futures), 1):
            done_mobs += future.result()
            if index % 10 == 0:
                print(f"batches {index}/{len(todo)} mobs {done_mobs}", flush=True)
    log(f"DONE batches={len(todo)} mobs={done_mobs}")
    print(f"done mobs={done_mobs}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
