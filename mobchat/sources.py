from __future__ import annotations

import html
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .http import HttpClient, HttpError

MODRINTH = "https://api.modrinth.com/v2"
CURSEFORGE = "https://api.curseforge.com/v1"

CF_GAME_ID = 432
CF_CLASS_MODS = 6
CF_LOADER_FORGE = 1


def modrinth_headers(cfg: dict) -> dict:
    token = (cfg.get("modrinth") or {}).get("token")
    return {"Authorization": token} if token else {}


# --------------------------------------------------------------------------- #
# Modrinth
# --------------------------------------------------------------------------- #

def fetch_modrinth_facets(
    http: HttpClient, cfg: dict, facets: list, wanted: int, label: str = "modrinth", log=print
) -> list[dict]:
    page_size = int(cfg["modrinth"]["page_size"])
    hits: list[dict] = []
    offset = 0
    total = None
    while len(hits) < wanted:
        data = http.get_json(
            f"{MODRINTH}/search",
            headers=modrinth_headers(cfg),
            params={
                "facets": json.dumps(facets, separators=(",", ":")),
                "index": "downloads",
                "limit": page_size,
                "offset": offset,
            },
        )
        total = data.get("total_hits", total)
        page = data.get("hits") or []
        if not page:
            break
        hits.extend(page)
        offset += len(page)
        log(f"  {label} search: {len(hits)}/{min(wanted, total or 0)} (total_hits={total})")
        if total is not None and offset >= total:
            break
    return hits[:wanted]


def fetch_modrinth(http: HttpClient, cfg: dict, log=print) -> list[dict]:
    facets = [["project_type:mod"], ["versions:1.20.1"], ["categories:forge"]]
    return fetch_modrinth_facets(
        http, cfg, facets, int(cfg["modrinth"]["max_projects"]), "modrinth", log
    )


def fetch_modrinth_category(
    http: HttpClient, cfg: dict, category: str, wanted: int, log=print
) -> list[dict]:
    facets = [
        ["project_type:mod"],
        ["versions:1.20.1"],
        ["categories:forge"],
        [f"categories:{category}"],
    ]
    return fetch_modrinth_facets(http, cfg, facets, wanted, f"modrinth[{category}]", log)


def verify_modrinth(http: HttpClient, hits: list[dict], cfg: dict, log=print) -> list[dict]:
    """Keep only projects that really ship a Forge file for 1.20.1."""
    workers = 12

    def work(hit: dict) -> dict:
        try:
            versions = http.get_json(
                f"{MODRINTH}/project/{hit['project_id']}/version",
                headers=modrinth_headers(cfg),
                params={
                    "game_versions": json.dumps(["1.20.1"]),
                    "loaders": json.dumps(["forge"]),
                },
            )
        except HttpError as exc:
            return {**hit, "verified": False, "verify_error": str(exc)[:200]}
        downloads_1_20_1 = sum(int(v.get("downloads") or 0) for v in versions)
        newest = max((v.get("date_published") or "" for v in versions), default="")
        return {
            **hit,
            "verified": bool(versions),
            "files_1_20_1_forge": len(versions),
            "downloads_1_20_1_forge": downloads_1_20_1,
            "newest_1_20_1_forge": newest,
        }

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(work, hit) for hit in hits]
        for i, future in enumerate(as_completed(futures), 1):
            results.append(future.result())
            if i % 200 == 0:
                log(f"  modrinth verify: {i}/{len(hits)}")
    order = {hit["project_id"]: i for i, hit in enumerate(hits)}
    results.sort(key=lambda r: order.get(r["project_id"], 0))
    return results


# --------------------------------------------------------------------------- #
# CurseForge
# --------------------------------------------------------------------------- #

def curseforge_headers(cfg: dict) -> dict:
    key = (cfg["curseforge"].get("api_key") or "").strip()
    if not key:
        raise RuntimeError(
            "CurseForge 需要 API Key：到 https://console.curseforge.com/ 申请后填入 config.json "
            "的 curseforge.api_key（或用环境变量 CURSEFORGE_API_KEY）。"
        )
    return {"x-api-key": key}


def fetch_curseforge(http: HttpClient, cfg: dict, log=print) -> list[dict]:
    headers = curseforge_headers(cfg)
    page_size = int(cfg["curseforge"]["page_size"])
    wanted = int(cfg["curseforge"]["max_mods"])
    mods: list[dict] = []
    index = 0
    total = None
    while len(mods) < wanted:
        if index + page_size > 10000:
            log("  curseforge search: reached API pagination cap (index 10000)")
            break
        data = http.get_json(
            f"{CURSEFORGE}/mods/search",
            headers=headers,
            params={
                "gameId": CF_GAME_ID,
                "classId": CF_CLASS_MODS,
                "gameVersion": "1.20.1",
                "modLoaderType": CF_LOADER_FORGE,
                "sortField": 6,  # TotalDownloads
                "sortOrder": "desc",
                "pageSize": page_size,
                "index": index,
            },
        )
        total = (data.get("pagination") or {}).get("totalCount", total)
        page = data.get("data") or []
        if not page:
            break
        mods.extend(page)
        index += len(page)
        log(f"  curseforge search: {len(mods)}/{min(wanted, total or 0)} (total_count={total})")
        if total is not None and index >= total:
            break
    return mods[:wanted]


def verify_curseforge(http: HttpClient, mods: list[dict], cfg: dict, log=print) -> list[dict]:
    headers = curseforge_headers(cfg)
    workers = 6

    def work(mod: dict) -> dict:
        try:
            data = http.get_json(
                f"{CURSEFORGE}/mods/{mod['id']}/files",
                headers=headers,
                params={"gameVersion": "1.20.1", "modLoaderType": CF_LOADER_FORGE, "pageSize": 50},
            )
        except HttpError as exc:
            return {**mod, "verified": False, "verify_error": str(exc)[:200]}
        files = data.get("data") or []
        newest = max((f.get("fileDate") or "" for f in files), default="")
        return {
            **mod,
            "verified": bool(files),
            "files_1_20_1_forge": len(files),
            "newest_1_20_1_forge": newest,
        }

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(work, mod) for mod in mods]
        for i, future in enumerate(as_completed(futures), 1):
            results.append(future.result())
            if i % 100 == 0:
                log(f"  curseforge verify: {i}/{len(mods)}")
    order = {mod["id"]: i for i, mod in enumerate(mods)}
    results.sort(key=lambda r: order.get(r["id"], 0))
    return results


# --------------------------------------------------------------------------- #
# Normalisation
# --------------------------------------------------------------------------- #

_TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    return html.unescape(_TAG_RE.sub(" ", text or "")).strip()


def normalize_modrinth(hit: dict) -> dict:
    return {
        "source": "modrinth",
        "source_id": hit["project_id"],
        "slug": hit.get("slug"),
        "name": hit.get("title"),
        "summary": hit.get("description") or "",
        "url": f"https://modrinth.com/mod/{hit.get('slug')}",
        "downloads_total": int(hit.get("downloads") or 0),
        "downloads_1_20_1_forge": int(hit.get("downloads_1_20_1_forge") or 0),
        "follows": int(hit.get("follows") or 0),
        "categories": hit.get("categories") or [],
        "authors": [hit["author"]] if hit.get("author") else [],
        "date_modified": hit.get("date_modified"),
        "newest_1_20_1_forge": hit.get("newest_1_20_1_forge"),
        "verified_1_20_1_forge": bool(hit.get("verified")),
    }


def normalize_curseforge(mod: dict) -> dict:
    links = mod.get("links") or {}
    categories = mod.get("categories") or []
    return {
        "source": "curseforge",
        "source_id": str(mod["id"]),
        "slug": mod.get("slug"),
        "name": mod.get("name"),
        "summary": strip_html(mod.get("summary") or ""),
        "url": links.get("websiteUrl") or f"https://www.curseforge.com/minecraft/mc-mods/{mod.get('slug')}",
        "downloads_total": int(mod.get("downloadCount") or 0),
        "downloads_1_20_1_forge": None,
        "follows": None,
        "categories": [c.get("name") for c in categories if c.get("name")],
        "authors": [a.get("name") for a in (mod.get("authors") or []) if a.get("name")],
        "date_modified": mod.get("dateModified"),
        "newest_1_20_1_forge": mod.get("newest_1_20_1_forge"),
        "verified_1_20_1_forge": bool(mod.get("verified")),
    }
