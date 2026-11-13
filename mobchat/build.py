from __future__ import annotations

import csv
import difflib
import json
import time
import unicodedata
from pathlib import Path

from .config import DATA_DIR

CSV_FIELDS = [
    "rank",
    "name",
    "summary",
    "intro_zh",
    "primary_type",
    "mob_count_named",
    "mobs",
    "downloads_total",
    "downloads_1_20_1_forge",
    "popularity_source",
    "sources",
    "url",
    "url_modrinth",
    "url_curseforge",
    "confidence",
    "method",
    "evidence",
    "categories",
    "authors",
    "last_updated",
    "verified_1_20_1_forge",
]

MERGE_THRESHOLD = 0.92
REVIEW_THRESHOLD = 0.85


def normalize_name(name: str) -> str:
    text = unicodedata.normalize("NFKD", (name or "").lower()).replace("&", " and ")
    return "".join(ch for ch in text if ch.isalnum())


def _merge_two(left: dict, right: dict) -> dict:
    merged = dict(left)
    merged["sources"] = sorted(set(left["sources"]) | set(right["sources"]))
    merged["source_ids"] = {**left["source_ids"], **right["source_ids"]}
    merged["urls"] = {**left.get("urls", {}), **right.get("urls", {})}
    merged["aliases"] = sorted(set(left.get("aliases", [])) | set(right.get("aliases", [])) | {right.get("name")})
    merged["downloads_total"] = max(int(left.get("downloads_total") or 0), int(right.get("downloads_total") or 0))
    known = [v for v in (left.get("downloads_1_20_1_forge"), right.get("downloads_1_20_1_forge")) if v is not None]
    merged["downloads_1_20_1_forge"] = max(known) if known else None
    merged["categories"] = sorted(set(left.get("categories") or []) | set(right.get("categories") or []))
    merged["authors"] = sorted(set(left.get("authors") or []) | set(right.get("authors") or []))
    merged["last_updated"] = max([v for v in (left.get("date_modified"), right.get("date_modified")) if v] or [""])

    primary, secondary = (
        (left, right)
        if int(left.get("downloads_total") or 0) >= int(right.get("downloads_total") or 0)
        else (right, left)
    )
    merged["popularity_source"] = primary["source"]
    merged["url"] = primary.get("url")
    for field in ("summary", "verified_1_20_1_forge"):
        merged[field] = primary.get(field) or secondary.get(field)
    return merged


def dedupe(rows: list[dict], near_duplicate_log: Path | None = None) -> list[dict]:
    """Merge the same mod listed on both platforms.

    Stage 1: exact normalised-name buckets. Stage 2: fuzzy comparison inside a
    block keyed by the first two characters. Pairs between REVIEW_THRESHOLD and
    MERGE_THRESHOLD are not merged automatically, they land in a review CSV.
    """
    buckets: dict[str, list[dict]] = {}
    keyless: list[dict] = []
    for row in rows:
        key = normalize_name(row.get("name") or "")
        row["sources"] = [row["source"]]
        row["source_ids"] = {row["source"]: row["source_id"]}
        row["urls"] = {row["source"]: row.get("url")}
        row["aliases"] = row.get("aliases") or []
        row["popularity_source"] = row.get("popularity_source") or row["source"]
        if not key:
            keyless.append(row)
            continue
        buckets.setdefault(key, []).append(row)

    merged_rows: list[dict] = []
    for group in buckets.values():
        per_source: dict[str, list[dict]] = {}
        for row in group:
            per_source.setdefault(row["source"], []).append(row)
        if len(per_source) == 1:
            merged_rows.extend(group)
            continue
        # Only merge across platforms; extra same-name rows from one platform stay separate.
        representatives: list[dict] = []
        for items in per_source.values():
            representatives.append(items[0])
            merged_rows.extend(items[1:])
        current = representatives[0]
        for other in representatives[1:]:
            current = _merge_two(current, other)
        merged_rows.append(current)

    for row in merged_rows:
        row["_key"] = normalize_name(row.get("name") or "")

    blocks: dict[str, list[dict]] = {}
    for row in merged_rows:
        blocks.setdefault(row["_key"][:2], []).append(row)

    reviews: list[dict] = []
    final: list[dict] = []
    for block_rows in blocks.values():
        remaining = list(block_rows)
        index = 0
        while index < len(remaining):
            left = remaining[index]
            cursor = index + 1
            while cursor < len(remaining):
                right = remaining[cursor]
                ratio = difflib.SequenceMatcher(None, left["_key"], right["_key"]).ratio()
                same_source = bool(set(left["sources"]) & set(right["sources"]))
                if not same_source and ratio >= MERGE_THRESHOLD:
                    left = _merge_two(left, right)
                    left["_key"] = normalize_name(left.get("name") or "")
                    reviews.append(
                        {
                            "name_a": left.get("name"),
                            "name_b": right.get("name"),
                            "ratio": round(ratio, 3),
                            "action": "merged",
                            "url_a": left.get("url"),
                            "url_b": right.get("url"),
                        }
                    )
                    del remaining[cursor]
                else:
                    prefix_related = (
                        len(left["_key"]) >= 6
                        and (right["_key"].startswith(left["_key"]) or left["_key"].startswith(right["_key"]))
                    )
                    if ratio >= REVIEW_THRESHOLD or prefix_related:
                        reviews.append(
                            {
                                "name_a": left.get("name"),
                                "name_b": right.get("name"),
                                "ratio": round(ratio, 3),
                                "action": "review",
                                "url_a": left.get("url"),
                                "url_b": right.get("url"),
                            }
                        )
                    cursor += 1
            remaining[index] = left
            index += 1
        final.extend(remaining)

    final.extend(keyless)

    for row in final:
        row.pop("_key", None)

    if near_duplicate_log and reviews:
        near_duplicate_log.parent.mkdir(parents=True, exist_ok=True)
        with near_duplicate_log.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=["name_a", "name_b", "ratio", "action", "url_a", "url_b"]
            )
            writer.writeheader()
            writer.writerows(sorted(reviews, key=lambda r: -r["ratio"]))

    return final


def _label_for(row: dict, labels: dict[str, dict]) -> dict | None:
    for source, source_id in (row.get("source_ids") or {}).items():
        label = labels.get(f"{source}:{source_id}")
        if label:
            return label
    return None


def _csv_row(row: dict) -> dict:
    out = dict(row)
    for field in ("sources", "categories", "authors", "aliases"):
        if isinstance(out.get(field), list):
            out[field] = "; ".join(str(v) for v in out[field])
    return out


def build(candidates: list[dict], labels: dict[str, dict], cfg: dict, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = dedupe(candidates, output_dir / "merge_review.csv")

    intro_path = DATA_DIR / "intro_zh.json"
    intros = json.loads(intro_path.read_text(encoding="utf-8")) if intro_path.exists() else {}

    min_conf = float(cfg["output"]["min_confidence"])
    excluded = {
        normalize_name(name) for name in (cfg["output"].get("exclude") or []) if name
    }
    selected: list[dict] = []
    for row in rows:
        keys = [normalize_name(row.get("name") or "")]
        keys += [normalize_name(alias) for alias in (row.get("aliases") or [])]
        if excluded and any(key in excluded for key in keys if key):
            continue
        label = _label_for(row, labels)
        if not label or not label.get("adds_new_mob"):
            continue
        is_model = label.get("method") in ("llm", "agent-manual")
        if is_model and float(label.get("confidence") or 0) < min_conf:
            continue
        enriched = dict(row)
        enriched.update(
            {
                "summary": row.get("summary") or "",
                "intro_zh": intros.get(row.get("name") or "", ""),
                "primary_type": "纯生物模组" if label.get("primary") else "混合/顺带新增生物",
                "mobs": "; ".join(label.get("mobs") or []),
                "mob_count_named": len(label.get("mobs") or []),
                "evidence": label.get("evidence") or "",
                "confidence": round(float(label.get("confidence") or 0), 3),
                "method": label.get("method"),
                "url_modrinth": (row.get("urls") or {}).get("modrinth"),
                "url_curseforge": (row.get("urls") or {}).get("curseforge"),
                "last_updated": row.get("last_updated") or row.get("date_modified"),
            }
        )
        selected.append(enriched)

    selected.sort(key=lambda r: (-int(r.get("downloads_total") or 0), r.get("name") or ""))
    top_n = int(cfg["output"]["top_n"])
    top = selected if top_n <= 0 else selected[:top_n]
    for rank, row in enumerate(top, 1):
        row["rank"] = rank

    csv_path = output_dir / f"top{len(top)}_mob_mods.csv"
    json_path = output_dir / f"top{len(top)}_mob_mods.json"
    all_csv_path = output_dir / "all_candidates.csv"

    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(_csv_row(row) for row in top)
    json_path.write_text(json.dumps(top, ensure_ascii=False, indent=2), encoding="utf-8")

    with all_csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "rank", "name", "sources", "downloads_total", "adds_new_mob",
                "primary_type", "confidence", "method", "url",
            ],
            extrasaction="ignore",
        )
        writer.writeheader()
        for rank, row in enumerate(selected, 1):
            writer.writerow(_csv_row({**row, "rank": rank}))

    summary = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "candidates_after_verify": len(candidates),
        "merged_after_dedupe": len(rows),
        "mob_mods_found": len(selected),
        "exported": len(top),
        "output_csv": str(csv_path),
        "output_json": str(json_path),
        "near_duplicate_review": str(output_dir / "merge_review.csv")
        if (output_dir / "merge_review.csv").exists()
        else None,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
