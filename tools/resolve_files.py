"""Resolve the 1.20.1 Forge artifact for every mod on the list."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import CACHE_DIR, DATA_DIR, load_config  # noqa: E402
from mobchat.http import HttpClient  # noqa: E402
from mobchat.sources import MODRINTH, modrinth_headers  # noqa: E402


def main() -> int:
    cfg = load_config()
    http = HttpClient(CACHE_DIR, cfg["http"]["user_agent"], min_interval=0.2)
    rows = list(csv.DictReader(open(ROOT / "output" / "top308_mob_mods.csv", encoding="utf-8-sig")))
    candidates = json.loads((DATA_DIR / "candidates.json").read_text(encoding="utf-8"))
    ids = {c["name"]: c["source_id"] for c in candidates if c["source"] == "modrinth"}

    out: dict[str, dict] = {}
    for i, row in enumerate(rows, 1):
        name = row["name"]
        pid = ids.get(name)
        if not pid:
            continue
        versions = http.get_json(
            f"{MODRINTH}/project/{pid}/version",
            headers=modrinth_headers(cfg),
            params={"game_versions": json.dumps(["1.20.1"]), "loaders": json.dumps(["forge"])},
        )
        if not versions:
            continue
        latest = max(versions, key=lambda v: v.get("date_published") or "")
        files = latest.get("files") or []
        primary = next((f for f in files if f.get("primary")), files[0] if files else None)
        if not primary:
            continue
        out[name] = {
            "project_id": pid,
            "version": latest.get("version_number"),
            "filename": primary.get("filename"),
            "url": primary.get("url"),
            "size": primary.get("size"),
            "downloads": row["downloads_total"],
        }
        if i % 50 == 0:
            print(f"  resolved {i}/{len(rows)}")

    (DATA_DIR / "mod_files.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    sizes = sorted((v["size"] or 0, n) for n, v in out.items())
    total = sum(s for s, _ in sizes)
    print(f"resolved {len(out)} mods; total size {total/1024/1024:.0f} MiB")
    print("largest:", [(n, round(s / 1024 / 1024, 1)) for s, n in sizes[-8:]])
    for limit in (10, 30, 80):
        picked = [(s, n) for s, n in sizes if s <= limit * 1024 * 1024]
        print(f"<= {limit} MiB: {len(picked)} mods, {sum(s for s,_ in picked)/1024/1024:.0f} MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
