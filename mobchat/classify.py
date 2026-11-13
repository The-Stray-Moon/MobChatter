from __future__ import annotations

import json
import re
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

from .http import HttpClient, HttpError
from .sources import CURSEFORGE, MODRINTH, curseforge_headers, modrinth_headers, strip_html

SYSTEM_PROMPT = """你是 Minecraft 模组数据标注员。任务：判断每个模组是否"新增了原版没有的生物/实体(mob)"。

规则：
1. 只依据给出的名称、摘要、描述文本判断，不得依据模型记忆补充事实。证据不足时 adds_new_mob=false 且 confidence<=0.3。
2. "新增生物"指新的怪物、动物、Boss、NPC、神话/幻想生物等可生成、可交互的实体。
   - 仅修改原版生物（换皮、调数值、加变种）不算。
   - 只新增方块/物品/装备/武器/结构/法术/维度/机制，没有新生物，不算。
3. 生物群系、维度、科技、魔法类模组如果顺带加入了新生物：adds_new_mob=true 且 primary=false。
4. 纯粹以新增生物为核心内容的模组：primary=true。
5. evidence 必须逐字摘自给定文本（不超过 25 个单词），不得改写或翻译。找不到依据就留空。
6. mobs 只列出文本中明确写出的生物名称，没有就给空数组，禁止编造。

严格输出 JSON，格式：
{"results":[{"i":0,"adds_new_mob":true,"primary":false,"mobs":["..."],"evidence":"...","confidence":0.9}]}
confidence 为 0-1 的小数。results 必须覆盖所有输入项，i 与输入编号一致。"""

MOB_KEYWORDS = {
    "mob", "creature", "animal", "monster", "boss", "beast", "dragon", "pet", "npc",
    "pokemon", "digimon", "yokai", "kaiju", "dinosaur", "dino", "insect", "bird",
    "fish", "wildlife", "fauna", "bestiary", "wyvern", "goblin", "orc", "fairy",
    "slime", "golem", "demon", "undead", "spider", "zombie", "skeleton", "raven",
    "golem", "phoenix", "griffin", "mermaid", "vampire", "werewolf", "alien",
}

# Categories that signal a utility/library mod rather than a content mod.
UTILITY_CATEGORIES = {
    "optimization", "library", "management", "storage", "technology",
    "equipment", "decoration", "transportation", "utility",
}


def llm_available(cfg: dict) -> bool:
    llm = cfg["llm"]
    return bool(
        (llm.get("base_url") or "").strip()
        and (llm.get("api_key") or "").strip()
        and (llm.get("model") or "").strip()
    )


# --------------------------------------------------------------------------- #
# Heuristic fallback (used only when no LLM is configured)
# --------------------------------------------------------------------------- #

def _stem_tokens(text: str) -> set[str]:
    ascii_text = unicodedata.normalize("NFKD", (text or "").lower()).encode("ascii", "ignore").decode()
    tokens = set(re.findall(r"[a-z][a-z'-]+", ascii_text))
    return {token[:-1] if len(token) > 3 and token.endswith("s") else token for token in tokens}


def heuristic_label(item: dict) -> dict:
    title_tokens = _stem_tokens(item.get("name"))
    summary_tokens = _stem_tokens(item.get("summary"))
    categories = {str(c).lower() for c in (item.get("categories") or [])}

    title_hits = sorted(title_tokens & MOB_KEYWORDS)
    body_hits = sorted((title_tokens | summary_tokens) & MOB_KEYWORDS)
    utility = bool(categories & UTILITY_CATEGORIES)

    adds = bool(title_hits) or (bool(body_hits) and not utility)
    if title_hits:
        confidence = 0.45
    elif body_hits and not utility:
        confidence = 0.3
    else:
        confidence = 0.1
    return {
        "adds_new_mob": adds,
        "primary": bool(title_hits),
        "mobs": [],
        "evidence": ", ".join(title_hits or body_hits[:5]),
        "confidence": confidence,
        "method": "heuristic",
    }


# --------------------------------------------------------------------------- #
# LLM transport
# --------------------------------------------------------------------------- #

def _chat(cfg: dict, messages: list[dict], json_mode: bool) -> str:
    llm = cfg["llm"]
    url = llm["base_url"].rstrip("/") + "/chat/completions"
    body = {"model": llm["model"], "messages": messages, "temperature": 0}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {llm['api_key']}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=float(llm.get("timeout") or 180)) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["choices"][0]["message"]["content"]


def _extract_json(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    start = min((i for i in (text.find("{"), text.find("[")) if i >= 0), default=-1)
    if start < 0:
        raise ValueError("no JSON object in model output")
    end = max(text.rfind("}"), text.rfind("]"))
    return json.loads(text[start : end + 1])


def _parse_results(raw: str, expected: list[int]) -> dict[int, dict]:
    data = _extract_json(raw)
    if isinstance(data, dict):
        data = data.get("results", data.get("items", []))
    parsed: dict[int, dict] = {}
    for entry in data if isinstance(data, list) else []:
        try:
            idx = int(entry.get("i"))
        except (TypeError, ValueError):
            continue
        if idx not in expected:
            continue
        parsed[idx] = {
            "adds_new_mob": bool(entry.get("adds_new_mob")),
            "primary": bool(entry.get("primary")),
            "mobs": [str(m) for m in (entry.get("mobs") or [])][:12],
            "evidence": str(entry.get("evidence") or "").strip()[:300],
            "confidence": max(0.0, min(1.0, float(entry.get("confidence") or 0))),
            "method": "llm",
        }
    return parsed


def _item_payload(index: int, item: dict) -> dict:
    payload = {"i": index, "name": item.get("name")}
    if item.get("summary"):
        payload["summary"] = item["summary"][:600]
    if item.get("categories"):
        payload["categories"] = item["categories"][:12]
    if item.get("description"):
        payload["description"] = item["description"][:2500]
    return payload


def _classify_batch(cfg: dict, items: list[dict], indexes: list[int]) -> dict[int, dict]:
    payload = [_item_payload(i, items[i]) for i in indexes]
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "待判定模组（JSON 数组，字段 i 为编号）：\n"
            + json.dumps(payload, ensure_ascii=False)
            + "\n只输出 JSON。",
        },
    ]
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            return _parse_results(_chat(cfg, messages, bool(cfg["llm"].get("json_mode"))), set(indexes))
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt == 1 and len(indexes) > 4:
                break
    if len(indexes) > 4:
        mid = len(indexes) // 2
        merged = _classify_batch(cfg, items, indexes[:mid])
        merged.update(_classify_batch(cfg, items, indexes[mid:]))
        return merged
    raise RuntimeError(f"LLM batch failed: {last_error}")


# --------------------------------------------------------------------------- #
# Description fetch for ambiguous items
# --------------------------------------------------------------------------- #

def fetch_description(http: HttpClient, cfg: dict, item: dict) -> str:
    try:
        if item["source"] == "modrinth":
            project = http.get_json(f"{MODRINTH}/project/{item['source_id']}", headers=modrinth_headers(cfg))
            return (project.get("body") or "")[:4000]
        headers = curseforge_headers(cfg)
        mod = http.get_json(f"{CURSEFORGE}/mods/{item['source_id']}", headers=headers)
        return strip_html((mod.get("data") or {}).get("description") or "")[:4000]
    except (HttpError, RuntimeError):
        return ""


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #

def classify_items(
    http: HttpClient,
    cfg: dict,
    items: list[dict],
    existing: dict[str, dict] | None = None,
    log=print,
) -> dict[str, dict]:
    """Classify items in rank order. Returns {key: label} for every item."""
    existing = dict(existing or {})
    labels: dict[str, dict] = {}
    pending: list[dict] = []

    for item in items:
        key = f"{item['source']}:{item['source_id']}"
        if key in existing:
            labels[key] = existing[key]
        else:
            item["_key"] = key
            pending.append(item)

    if not pending:
        log("  classify: everything already cached")
        return labels

    if not llm_available(cfg):
        log("  classify: no LLM configured -> heuristic keyword labelling")
        for item in pending:
            labels[item["_key"]] = heuristic_label(item)
        return labels

    batch_size = max(1, int(cfg["llm"]["batch_size"]))
    concurrency = max(1, int(cfg["llm"]["concurrency"]))
    batches = [list(range(i, min(i + batch_size, len(pending)))) for i in range(0, len(pending), batch_size)]
    log(f"  classify: {len(pending)} items in {len(batches)} batches (model={cfg['llm']['model']})")

    failed: list[dict] = []
    done = 0
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {
            pool.submit(_classify_batch, cfg, pending, batch): batch for batch in batches
        }
        for future in as_completed(futures):
            batch = futures[future]
            try:
                result = future.result()
            except RuntimeError as exc:
                log(f"  classify: batch failed ({len(batch)} items): {exc}")
                failed.extend(pending[i] for i in batch)
                continue
            for idx in batch:
                key = pending[idx]["_key"]
                if idx in result:
                    labels[key] = result[idx]
                else:
                    failed.append(pending[idx])
            done += len(batch)
            if done % 200 < batch_size:
                log(f"  classify: {done}/{len(pending)}")

    for item in failed:
        labels[item["_key"]] = heuristic_label(item) | {"method": "heuristic-fallback"}

    # Second pass: low-confidence negatives get the full description.
    budget = int(cfg["llm"].get("max_body_fetch") or 0)
    ambiguous = [
        item for item in pending
        if budget > 0
        and not labels[item["_key"]]["adds_new_mob"]
        and labels[item["_key"]]["confidence"] < 0.7
        and labels[item["_key"]]["method"].startswith("llm")
    ]
    if ambiguous and budget > 0:
        selected = ambiguous[:budget]
        log(f"  classify: fetching full descriptions for {len(selected)} ambiguous items")
        for i, item in enumerate(selected, 1):
            body = fetch_description(http, cfg, item)
            if body:
                item["description"] = body
            if i % 50 == 0:
                log(f"  classify: description fetch {i}/{len(selected)}")
        retry_indexes = list(range(len(selected)))
        retry_batches = [
            retry_indexes[i : i + batch_size] for i in range(0, len(retry_indexes), batch_size)
        ]
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = {
                pool.submit(_classify_batch, cfg, selected, batch): batch for batch in retry_batches
            }
            for future in as_completed(futures):
                batch = futures[future]
                try:
                    result = future.result()
                except RuntimeError:
                    continue
                for idx in batch:
                    if idx in result:
                        labels[selected[idx]["_key"]] = result[idx]

    return labels
