from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CACHE_DIR = DATA_DIR / "cache"
LOG_DIR = DATA_DIR / "logs"
OUTPUT_DIR = ROOT / "output"

DEFAULTS: dict = {
    "modrinth": {
        "max_projects": 3000,
        "page_size": 100,
        "category": "mobs",
        "category_max": 1500,
    },
    "curseforge": {
        "api_key": "",
        "max_mods": 2000,
        "page_size": 50,
        "max_verify": 1200,
    },
    "llm": {
        "base_url": "",
        "api_key": "",
        "model": "",
        "batch_size": 20,
        "concurrency": 4,
        "timeout": 180,
        "json_mode": False,
        "max_body_fetch": 150,
    },
    "http": {
        "min_interval": 0.2,
        "cache_ttl_hours": 168,
        "user_agent": "MobChatter/1.0 (local mod-collection script)",
    },
    "output": {
        "top_n": 0,
        "min_confidence": 0.5,
        "exclude": [],
    },
}


def _merge(dst: dict, src: dict) -> None:
    for key, value in src.items():
        if isinstance(value, dict) and isinstance(dst.get(key), dict):
            _merge(dst[key], value)
        else:
            dst[key] = value


def load_env_file(path: Path) -> dict[str, str]:
    """Parse KEY=VALUE pairs. Values are never logged."""
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        values[key] = value.strip().strip('"').strip("'")
    return values


def apply_env(cfg: dict, env: dict[str, str]) -> dict:
    """Fill empty config fields from .env / process environment. Never prints secrets."""
    merged_env = {**env, **{k: v for k, v in os.environ.items() if k not in env}}

    def pick(*names):
        for name in names:
            value = merged_env.get(name)
            if value:
                return value
        return None

    curseforge_key = pick("CURSEFORGE_TOKEN", "CURSEFORGE_API_KEY")
    if curseforge_key and not cfg["curseforge"].get("api_key"):
        cfg["curseforge"]["api_key"] = curseforge_key

    modrinth_token = pick("MODRINTH_TOKEN", "MODRINTH_API_TOKEN")
    if modrinth_token:
        cfg.setdefault("modrinth", {})["token"] = modrinth_token

    llm_key = pick("LLM_API_KEY", "OPENAI_API_KEY", "MOONSHOT_API_KEY", "DEEPSEEK_API_KEY", "DASHSCOPE_API_KEY")
    if llm_key and not cfg["llm"].get("api_key"):
        cfg["llm"]["api_key"] = llm_key
        if not cfg["llm"].get("base_url"):
            cfg["llm"]["base_url"] = pick("LLM_BASE_URL", "OPENAI_BASE_URL", "OPENAI_API_BASE") or ""
        if not cfg["llm"].get("model"):
            cfg["llm"]["model"] = pick("LLM_MODEL", "OPENAI_MODEL") or ""

    cfg["_credentials"] = {
        "curseforge": bool(cfg["curseforge"].get("api_key")),
        "modrinth": bool(cfg.get("modrinth", {}).get("token")),
        "llm": bool(cfg["llm"].get("api_key") and cfg["llm"].get("base_url") and cfg["llm"].get("model")),
    }
    return cfg


def load_config(path: str | Path | None = None) -> dict:
    cfg = json.loads(json.dumps(DEFAULTS))
    cfg_path = Path(path) if path else ROOT / "config.json"
    if cfg_path.exists():
        _merge(cfg, json.loads(cfg_path.read_text(encoding="utf-8")))
    cfg = apply_env(cfg, load_env_file(ROOT / ".env"))
    for directory in (DATA_DIR, RAW_DIR, CACHE_DIR, LOG_DIR, OUTPUT_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    return cfg


class Tee:
    """Print to console and append to a log file at the same time."""

    def __init__(self, log_path: Path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.log_path.open("a", encoding="utf-8")

    def __call__(self, message: str = "") -> None:
        line = str(message)
        print(line, flush=True)
        self._fh.write(line + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()
