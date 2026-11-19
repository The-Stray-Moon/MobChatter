"""Shared helpers for per-mob unique dialogue.

`context` prints everything an author (agent or local model) needs for one
batch, including the module introduction; `validate` checks a written batch
against the required scenario counts; `status` reports progress against the
plan. Batches are the only unit written to disk.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dialogue"
UNIQUE = DATA / "unique"
PLAN = DATA / "unique_plan.json"
INTROS = DATA / "mod_intros.json"

SCENARIOS = ["walk", "idle", "look_player", "tempted", "collide", "mate",
             "pickup", "target_acquire", "targeting", "melee_attack", "spawn"]
DAMAGE = ["fire", "fall", "drown", "explosion", "projectile", "magic",
          "starvation", "lightning", "void"]
CJK = re.compile(r"[\u3400-\u9fff]")
def required_counts(mob: dict) -> dict:
    """Line count per scenario: 10 plus the archetype weight bonus, capped at 20."""
    weights = mob.get("weights") or {}
    return {
        s: 10 + max(0, min(10, round(10 * (float(weights.get(s, 1.0)) - 1))))
        for s in SCENARIOS + ["hurt"]
    }


def expected_total(mob: dict) -> int:
    counts = required_counts(mob)
    return sum(counts[s] for s in SCENARIOS) + counts["hurt"] + len(DAMAGE)


def load_plan() -> dict:
    return json.loads(PLAN.read_text(encoding="utf-8"))


def load_intros() -> dict:
    return json.loads(INTROS.read_text(encoding="utf-8")) if INTROS.exists() else {}


def context_for(batch: str, mob: dict, intros: dict) -> dict:
    rank = int(mob["rank"])
    return {
        "batch": batch,
        "mob_id": mob["mob_id"],
        "rank": rank,
        "name_zh": mob.get("name_zh") or "",
        "name_en": mob.get("name_en") or "",
        "archetype": mob.get("archetype") or "",
        "mod": mob.get("mod") or "",
        "mod_intro": intros.get(str(rank), ""),
        "description": mob.get("description") or "",
        "counts": required_counts(mob),
    }


def batch_context(batch: str) -> dict:
    plan = load_plan()
    intros = load_intros()
    return {
        "batch": batch,
        "mobs": [context_for(batch, m, intros) for m in plan.get(batch, [])],
    }


def _lines(value, key: str, errors: list[str]) -> list[dict]:
    if not isinstance(value, list):
        errors.append(f"{key}: not a list")
        return []
    out = []
    for item in value:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            zh, en = item[0], item[1]
        elif isinstance(item, dict):
            zh, en = item.get("zh"), item.get("en")
        else:
            errors.append(f"{key}: bad line {item!r}")
            continue
        zh, en = str(zh or "").strip(), str(en or "").strip()
        if not zh or not en:
            errors.append(f"{key}: empty line")
            continue
        if "\ufffd" in zh or "\ufffd" in en:
            errors.append(f"{key}: corrupt line {zh[:20]!r}")
            continue
        if not CJK.search(zh):
            errors.append(f"{key}: no Chinese in {zh[:20]!r}")
            continue
        if not re.search(r"[A-Za-z]", en):
            errors.append(f"{key}: no English in {en[:20]!r}")
            continue
        out.append({"zh": zh, "en": en})
    return out


def validate_mob(mob: dict, entry: dict, strict: bool = True) -> list[str]:
    """Strict mode requires the exact planned counts and all 9 damage lines.

    Legacy batches written before the plan was fixed may carry fewer lines and
    a generic-only hurt block; those are reported but not treated as failures.
    """
    errors: list[str] = []
    counts = required_counts(mob)
    scenarios = entry.get("scenarios")
    if not isinstance(scenarios, dict):
        return ["scenarios missing"]
    seen: set[str] = set()

    def expect(actual: int, wanted: int, key: str) -> None:
        if strict and actual != wanted:
            errors.append(f"{key}: {actual}/{wanted} lines")
        elif not strict and actual < 8:
            errors.append(f"{key}: only {actual} lines")

    for scenario in SCENARIOS:
        lines = _lines(scenarios.get(scenario), scenario, errors)
        expect(len(lines), counts[scenario], scenario)
        for line in lines:
            if line["zh"] in seen:
                errors.append(f"{scenario}: duplicate {line['zh'][:16]!r}")
            seen.add(line["zh"])
    hurt = scenarios.get("hurt")
    if not isinstance(hurt, dict):
        errors.append("hurt missing")
        return errors
    generic = _lines(hurt.get("generic"), "hurt.generic", errors)
    expect(len(generic), counts["hurt"], "hurt.generic")
    for line in generic:
        if line["zh"] in seen:
            errors.append(f"hurt.generic: duplicate {line['zh'][:16]!r}")
        seen.add(line["zh"])
    by_damage = hurt.get("by_damage")
    if not isinstance(by_damage, dict):
        if strict:
            errors.append("hurt.by_damage missing")
        return errors
    for damage in DAMAGE:
        value = by_damage.get(damage)
        if value is None and not strict:
            # Lenient mode accepts a missing damage line: the runtime falls
            # back to the generic hurt bucket.
            continue
        lines = _lines(value, f"hurt.{damage}", errors)
        if strict and len(lines) != 1:
            errors.append(f"hurt.{damage}: {len(lines)}/1 lines")
        for line in lines:
            if line["zh"] in seen:
                errors.append(f"hurt.{damage}: duplicate {line['zh'][:16]!r}")
            seen.add(line["zh"])
    return errors


def validate_batch(batch: str, strict: bool = True) -> list[str]:
    path = UNIQUE / f"{batch}.json"
    if not path.exists():
        return [f"{batch}.json missing"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"invalid JSON: {exc}"]
    plan = {m["mob_id"]: m for m in load_plan().get(batch, [])}
    errors: list[str] = []
    entries = data.get("mobs") or []
    if not entries:
        errors.append("no mobs")
    for entry in entries:
        mob = plan.get(entry.get("mob_id"))
        if mob is None:
            errors.append(f"unknown mob {entry.get('mob_id')}")
            continue
        for problem in validate_mob(mob, entry, strict):
            errors.append(f"{entry.get('mob_id')}: {problem}")
    return errors


def covered() -> tuple[dict, list[tuple[str, dict]]]:
    """Return mob_id -> ranks already written, and remaining (batch, mob) pairs."""
    plan = load_plan()
    have: dict[str, set] = {}
    for path in UNIQUE.glob("u*.json"):
        if not path.stem[1:].isdigit():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for entry in data.get("mobs") or []:
            have.setdefault(entry.get("mob_id"), set()).add(entry.get("rank"))
    remaining = []
    for batch, mobs in plan.items():
        for mob in mobs:
            ranks = have.get(mob["mob_id"], set())
            if mob["rank"] in ranks or None in ranks:
                continue
            remaining.append((batch, mob))
    return have, remaining


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["context", "validate", "status", "shards"])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--count", type=int, default=64)
    parser.add_argument("--skip", type=int, default=0)
    parser.add_argument("--out", default="")
    parser.add_argument("--legacy", action="store_true",
                        help="validate pre-plan batches leniently (>=8 lines, hurt.by_damage optional)")
    args = parser.parse_args()

    if args.command == "context":
        payload = [batch_context(name) for name in args.names]
        if len(payload) == 1:
            payload = payload[0]
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return 0

    if args.command == "validate":
        failed = 0
        for name in args.names:
            errors = validate_batch(name, strict=not args.legacy)
            if errors:
                failed += 1
                print(f"FAIL {name}")
                for error in errors[:20]:
                    print(f"  {error}")
            else:
                print(f"OK {name}")
        return 1 if failed else 0

    if args.command == "status":
        _, remaining = covered()
        batches = sorted({batch for batch, _ in remaining})
        print(f"remaining mobs={len(remaining)} batches={len(batches)}")
        if batches:
            print("first=" + " ".join(batches[:8]))
            print("last=" + " ".join(batches[-4:]))
        return 0

    if args.command == "shards":
        # Emit a checklist of the mobs still missing per shard. Batches hold
        # several mobs, so sharding whole batches would strand partially
        # written files; agents get exact (batch, mob_id) pairs instead.
        _, remaining = covered()
        reserve_path = UNIQUE / "local_assignment.json"
        reserved = set()
        if reserve_path.exists():
            reserved = set(json.loads(reserve_path.read_text(encoding="utf-8"))["batches"])
        remaining = [(b, m) for b, m in remaining if b not in reserved]
        weight: dict[str, int] = {}
        for batch, _ in remaining:
            weight[batch] = weight.get(batch, 0) + 1
        batches = sorted(weight, key=lambda b: (-weight[b], b))[args.skip:]
        shards = {f"s{index + 1:02d}": batches[index::args.count]
                  for index in range(args.count)}
        shards = {name: items for name, items in shards.items() if items}
        per_batch: dict[str, list[str]] = {}
        for batch, mob in remaining:
            per_batch.setdefault(batch, []).append(mob["mob_id"])
        payload = {"shards": shards,
                   "mobs": {batch: per_batch.get(batch, []) for batch in batches}}
        if args.out:
            target = Path(args.out)
            target.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                              encoding="utf-8")
        print(json.dumps({"shards": len(shards), "batches": len(batches),
                          "out": args.out}, ensure_ascii=False))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
