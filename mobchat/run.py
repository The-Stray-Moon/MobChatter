from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from .build import build
from .classify import classify_items, llm_available
from .config import CACHE_DIR, DATA_DIR, LOG_DIR, OUTPUT_DIR, RAW_DIR, Tee, load_config
from .http import HttpClient, HttpError
from .sources import (
    fetch_curseforge,
    fetch_modrinth,
    fetch_modrinth_category,
    normalize_curseforge,
    normalize_modrinth,
    verify_curseforge,
    verify_modrinth,
)

CANDIDATES_PATH = DATA_DIR / "candidates.json"
CLASSIFIED_PATH = DATA_DIR / "classified.json"
META_PATH = DATA_DIR / "run_meta.json"


def make_http(cfg: dict) -> HttpClient:
    return HttpClient(
        cache_dir=CACHE_DIR,
        user_agent=cfg["http"]["user_agent"],
        min_interval=float(cfg["http"]["min_interval"]),
        ttl_hours=float(cfg["http"]["cache_ttl_hours"]),
    )


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_candidates() -> list[dict]:
    return load_json(CANDIDATES_PATH, [])


def _upsert(existing: list[dict], rows: list[dict]) -> list[dict]:
    by_key = {(row["source"], row["source_id"]): row for row in existing}
    for row in rows:
        by_key[(row["source"], row["source_id"])] = row
    return sorted(by_key.values(), key=lambda r: -int(r.get("downloads_total") or 0))


def cmd_fetch(cfg: dict, args, log) -> int:
    http = make_http(cfg)
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    candidates = load_candidates()
    before = len(candidates)
    collected: list[dict] = []

    if "modrinth" in sources:
        log(f"[fetch] Modrinth: top {cfg['modrinth']['max_projects']} by downloads "
            f"(facet: 1.20.1 + forge + mod)")
        try:
            hits = fetch_modrinth(http, cfg, log=log)
            save_json(RAW_DIR / "modrinth_search.json", hits)
            category = (cfg["modrinth"].get("category") or "").strip()
            category_max = int(cfg["modrinth"].get("category_max") or 0)
            if category and category_max:
                extra = fetch_modrinth_category(http, cfg, category, category_max, log=log)
                save_json(RAW_DIR / f"modrinth_category_{category}.json", extra)
                seen = {hit["project_id"] for hit in hits}
                added = [hit for hit in extra if hit["project_id"] not in seen]
                hits.extend(added)
                log(f"[fetch] Modrinth: +{len(added)} projects from category '{category}' (deduped)")
            log(f"[fetch] Modrinth: verifying Forge files for 1.20.1 on {len(hits)} projects")
            verified = verify_modrinth(http, hits, cfg, log=log)
            save_json(RAW_DIR / "modrinth_verified.json", verified)
            rows = [normalize_modrinth(h) for h in verified if h.get("verified")]
            log(f"[fetch] Modrinth: {len(rows)}/{len(hits)} projects have a Forge 1.20.1 file")
            collected.extend(rows)
        except HttpError as exc:
            log(f"[fetch] Modrinth failed: {exc}")

    if "curseforge" in sources:
        if not (cfg["curseforge"].get("api_key") or "").strip():
            log("[fetch] CurseForge skipped: no API key in config.json (curseforge.api_key)")
        else:
            log(f"[fetch] CurseForge: top {cfg['curseforge']['max_mods']} by total downloads "
                f"(gameVersion=1.20.1, modLoaderType=Forge, classId=6)")
            try:
                mods = fetch_curseforge(http, cfg, log=log)
                save_json(RAW_DIR / "curseforge_search.json", mods)
                limit = int(cfg["curseforge"]["max_verify"])
                to_verify = mods[:limit]
                log(f"[fetch] CurseForge: verifying 1.20.1 Forge files on {len(to_verify)} mods")
                verified = verify_curseforge(http, to_verify, cfg, log=log)
                save_json(RAW_DIR / "curseforge_verified.json", verified)
                rows = [normalize_curseforge(m) for m in verified if m.get("verified")]
                log(f"[fetch] CurseForge: {len(rows)}/{len(to_verify)} mods have a Forge 1.20.1 file")
                collected.extend(rows)
            except (HttpError, RuntimeError) as exc:
                log(f"[fetch] CurseForge failed: {exc}")

    if not collected and before == 0:
        log("[fetch] no candidates collected; nothing to do")
        return 2

    candidates = _upsert(candidates, collected)
    save_json(CANDIDATES_PATH, candidates)
    log(f"[fetch] candidates on disk: {before} -> {len(candidates)}")
    return 0


def cmd_classify(cfg: dict, args, log) -> int:
    http = make_http(cfg)
    candidates = load_candidates()
    if not candidates:
        log("[classify] data/candidates.json is empty; run `fetch` first")
        return 2
    candidates.sort(key=lambda r: -int(r.get("downloads_total") or 0))
    existing = load_json(CLASSIFIED_PATH, {})
    if args.no_ai:
        cfg["llm"] = {**cfg["llm"], "api_key": ""}
    if not llm_available(cfg):
        log("[classify] LLM not configured -> keyword heuristic only. "
            "Fill llm.base_url / llm.api_key / llm.model in config.json for real classification.")
    labels = classify_items(http, cfg, candidates, existing=existing, log=log)
    merged = {**existing, **labels}
    save_json(CLASSIFIED_PATH, merged)
    hits = sum(1 for v in merged.values() if v.get("adds_new_mob"))
    log(f"[classify] labelled {len(merged)} projects, {hits} judged to add new mobs")
    return 0


def cmd_build(cfg: dict, args, log) -> int:
    candidates = load_candidates()
    labels = load_json(CLASSIFIED_PATH, {})
    if not candidates:
        log("[build] no candidates; run `fetch` first")
        return 2
    if not labels:
        log("[build] no labels; run `classify` first")
        return 2
    summary = build(candidates, labels, cfg, OUTPUT_DIR)
    log("[build] " + json.dumps(summary, ensure_ascii=False))
    return 0


def cmd_all(cfg: dict, args, log) -> int:
    code = cmd_fetch(cfg, args, log)
    if code != 0:
        return code
    code = cmd_classify(cfg, args, log)
    if code != 0:
        return code
    return cmd_build(cfg, args, log)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Collect the most downloaded 1.20.1 Forge mods that add new mobs.")
    parser.add_argument("--config", default=None, help="path to config.json")
    parser.add_argument("--no-ai", action="store_true", help="skip the LLM, use keyword heuristic")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="search + verify 1.20.1 Forge availability")
    p_fetch.add_argument("--sources", default="modrinth,curseforge")
    p_fetch.add_argument("--max-modrinth", type=int)
    p_fetch.add_argument("--max-curseforge", type=int)
    p_fetch.add_argument("--no-ai", action="store_true", help=argparse.SUPPRESS)

    p_classify = sub.add_parser("classify", help="LLM-judge whether each mod adds new mobs")
    p_classify.add_argument("--no-ai", action="store_true", help="keyword heuristic only")

    p_build = sub.add_parser("build", help="dedupe, rank, export")
    p_build.add_argument("--no-ai", action="store_true", help=argparse.SUPPRESS)

    p_all = sub.add_parser("all", help="fetch -> classify -> build")
    p_all.add_argument("--sources", default="modrinth,curseforge")
    p_all.add_argument("--max-modrinth", type=int)
    p_all.add_argument("--max-curseforge", type=int)
    p_all.add_argument("--no-ai", action="store_true", help="keyword heuristic only")

    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    if getattr(args, "max_modrinth", None):
        cfg["modrinth"]["max_projects"] = args.max_modrinth
    if getattr(args, "max_curseforge", None):
        cfg["curseforge"]["max_mods"] = args.max_curseforge

    log = Tee(LOG_DIR / f"run-{time.strftime('%Y%m%d-%H%M%S')}.log")
    log(f"=== {' '.join(sys.argv[1:]) or 'all'} @ {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    creds = cfg.get("_credentials", {})
    log(
        f"[auth] curseforge={'key loaded' if creds.get('curseforge') else 'missing'} | "
        f"modrinth={'token loaded' if creds.get('modrinth') else 'anonymous'} | "
        f"llm={'configured' if creds.get('llm') else 'not configured'}"
    )
    commands = {"fetch": cmd_fetch, "classify": cmd_classify, "build": cmd_build, "all": cmd_all}
    try:
        code = commands[args.command](cfg, args, log)
    except KeyboardInterrupt:
        log("interrupted")
        code = 130
    finally:
        meta = {
            "last_command": args.command,
            "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "config": {
                k: ({**v, "api_key": "***"} if isinstance(v, dict) and v.get("api_key") else v)
                for k, v in cfg.items()
                if not k.startswith("_")
            },
            "candidates": len(load_candidates()),
            "classified": len(load_json(CLASSIFIED_PATH, {})),
        }
        save_json(META_PATH, meta)
        log.close()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
