"""Extract the entity inventory (and data-driven facts) from a mod jar.

Usage:
    python tools/mob_inventory.py --rank 1
    python tools/mob_inventory.py --range 1-8

Writes data/inventory/<rank>.json and caches the jar in data/jars/<project_id>.jar.
Entity inventory comes from assets/*/lang/en_us.json + zh_cn.json, which reflect
every entity the mod registers (including projectiles, which are flagged).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mobchat.config import CACHE_DIR, DATA_DIR, load_config  # noqa: E402
from mobchat.http import HttpClient  # noqa: E402

JARS = DATA_DIR / "jars"
INVENTORY = DATA_DIR / "inventory"
ROWS = ROOT / "output" / "top313_mob_mods.csv"

PROJECTILE_HINTS = (
    "arrow", "projectile", "fireball", "snowball", "egg", "boat", "minecart",
    "tnt", "item", "orb", "beam", "missile", "hook", "bullet", "laser", "shulker_bullet",
    "fishing_bobber", "eye_of_ender", "potion", "experience", "lightning", "area_effect",
    "particle", "tombstone", "gravestone", "sign", "painting", "leash", "camera",
)


def load_rows() -> dict[int, dict]:
    with ROWS.open(encoding="utf-8-sig") as handle:
        return {int(row["rank"]): row for row in csv.DictReader(handle)}


def load_candidates() -> dict[str, dict]:
    rows = json.loads((DATA_DIR / "candidates.json").read_text(encoding="utf-8"))
    return {row["name"]: row for row in rows}


def latest_forge_file(http: HttpClient, project_id: str) -> dict:
    versions = http.get_json(
        f"https://api.modrinth.com/v2/project/{project_id}/version",
        params={"game_versions": json.dumps(["1.20.1"]), "loaders": json.dumps(["forge"])},
    )
    if not versions:
        raise RuntimeError(f"no 1.20.1 forge version for {project_id}")
    version = versions[0]
    files = [f for f in version.get("files", []) if f.get("primary")] or version.get("files", [])
    return files[0]


def download(url: str, dest: Path, log=print) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    log(f"    downloading {dest.name} ...")
    request = urllib.request.Request(url, headers={"User-Agent": "MobChatter/1.0"})
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(request, timeout=600) as response, tmp.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    tmp.replace(dest)
    return dest


def read_lang(zf: zipfile.ZipFile, suffix: str) -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in zf.namelist():
        if not name.startswith("assets/") or not name.endswith(f"lang/{suffix}.json"):
            continue
        try:
            merged.update(json.loads(zf.read(name).decode("utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
    return merged


def extract(rank: int, row: dict, candidate: dict, http: HttpClient, log=print) -> dict:
    project_id = candidate["source_id"]
    jar = JARS / f"{project_id}.jar"
    file_info = latest_forge_file(http, project_id)
    download(file_info["url"], jar, log=log)

    with zipfile.ZipFile(jar) as zf:
        en = read_lang(zf, "en_us")
        zh = read_lang(zf, "zh_cn")
        names = zf.namelist()
        loot = {
            Path(n).stem
            for n in names
            if re.search(r"loot_tables?/entities/", n) and n.endswith(".json")
        }
        modid = None
        for n in names:
            if n.endswith("META-INF/mods.toml"):
                text = zf.read(n).decode("utf-8", "replace")
                match = re.search(r'modId\s*=\s*"([^"]+)"', text)
                if match:
                    modid = match.group(1)
                    break

    entities = []
    for key, en_name in en.items():
        if not key.startswith("entity."):
            continue
        short = key.split(".")[-1]
        entities.append(
            {
                "key": key,
                "id": short,
                "en": en_name,
                "zh": zh.get(key, ""),
                "loot_table": short if short in loot else "",
                "projectile": any(hint in short.lower() or hint in key.lower() for hint in PROJECTILE_HINTS),
            }
        )
    entities.sort(key=lambda e: e["en"].lower())
    return {
        "rank": rank,
        "mod": row["name"],
        "slug": candidate.get("slug"),
        "project_id": project_id,
        "source_url": candidate.get("url"),
        "jar": str(jar),
        "jar_size": file_info.get("size"),
        "modid": modid,
        "entity_count": len(entities),
        "mob_count": sum(1 for e in entities if not e["projectile"]),
        "entities": entities,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", type=int)
    parser.add_argument("--range", help="e.g. 1-8")
    args = parser.parse_args()

    cfg = load_config()
    http = HttpClient(CACHE_DIR, cfg["http"]["user_agent"], min_interval=0.1)
    rows = load_rows()
    candidates = load_candidates()

    if args.rank:
        targets = [args.rank]
    elif args.range:
        start, end = (int(x) for x in args.range.split("-"))
        targets = list(range(start, end + 1))
    else:
        parser.error("need --rank or --range")

    INVENTORY.mkdir(parents=True, exist_ok=True)
    for rank in targets:
        row = rows.get(rank)
        if not row:
            print(f"rank {rank}: not in list")
            continue
        candidate = candidates.get(row["name"])
        if not candidate:
            print(f"rank {rank}: no candidate for {row['name']}")
            continue
        out = INVENTORY / f"{rank}.json"
        if out.exists():
            print(f"rank {rank}: cached -> {out}")
            continue
        print(f"rank {rank}: {row['name']}")
        try:
            data = extract(rank, row, candidate, http, log=print)
        except Exception as exc:  # noqa: BLE001
            print(f"    FAILED: {exc}")
            continue
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"    mobs={data['mob_count']} entities={data['entity_count']} -> {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
