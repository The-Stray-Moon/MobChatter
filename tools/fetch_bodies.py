"""Fetch full project bodies for the mods on the current list (cached on disk)."""
from __future__ import annotations

import csv
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import CACHE_DIR, DATA_DIR, load_config  # noqa: E402
from mobchat.http import HttpClient  # noqa: E402
from mobchat.sources import MODRINTH  # noqa: E402


def clean_markdown(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text or "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#>*`|]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> int:
    cfg = load_config()
    http = HttpClient(CACHE_DIR, cfg["http"]["user_agent"], min_interval=0.2)

    rows = list(csv.DictReader(open(ROOT / "output" / "top308_mob_mods.csv", encoding="utf-8-sig")))
    candidates = json.loads((DATA_DIR / "candidates.json").read_text(encoding="utf-8"))
    by_name = {c["name"]: c for c in candidates if c["source"] == "modrinth"}
    targets = [(r["name"], by_name[r["name"]]["source_id"]) for r in rows if r["name"] in by_name]
    print(f"{len(rows)} rows, {len(targets)} resolvable")

    out_path = DATA_DIR / "mod_bodies.json"
    bodies = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}

    def work(pair):
        name, pid = pair
        if name in bodies:
            return name, bodies[name]
        try:
            project = http.get_json(f"{MODRINTH}/project/{pid}")
        except Exception as exc:  # noqa: BLE001
            return name, {"error": str(exc)[:120]}
        return name, {
            "slug": project.get("slug"),
            "title": project.get("title"),
            "body": clean_markdown(project.get("body") or "")[:4000],
        }

    workers = 10
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(work, pair) for pair in targets]
        for future in as_completed(futures):
            name, value = future.result()
            bodies[name] = value
            done += 1
            if done % 50 == 0:
                print(f"  fetched {done}/{len(targets)}")

    out_path.write_text(json.dumps(bodies, ensure_ascii=False, indent=1), encoding="utf-8")
    errors = [n for n, v in bodies.items() if isinstance(v, dict) and v.get("error")]
    short = [n for n, v in bodies.items() if isinstance(v, dict) and len(v.get("body") or "") < 80]
    print(f"saved {len(bodies)} entries; errors={len(errors)}; short/no-body={len(short)}")
    if short[:5]:
        print("short examples:", short[:5])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
