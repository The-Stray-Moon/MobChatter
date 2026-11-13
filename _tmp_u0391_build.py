import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _tmp_u0391_data as D

ROOT = Path(__file__).resolve().parent
plan = json.loads((ROOT / "data/dialogue/unique_plan.json").read_text(encoding="utf-8"))
batch = plan["u0391"]
DATA = {"hybrid_aquatic:herring": D.HER, "hybrid_aquatic:horseshoe_crab": D.CRAB,
        "hybrid_aquatic:hound_shark": D.SHARK, "hybrid_aquatic:john_dory": D.DORY}
ORDER = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
         "target_acquire", "targeting", "melee_attack", "spawn", "hurt"]
DAMAGE = ["fire", "fall", "drown", "explosion", "projectile", "magic", "starvation", "lightning", "void"]

errors = []
seen = {}
total = 0
mobs = []
for entry in batch:
    mid = entry["mob_id"]
    data = DATA[mid]
    scen = {}
    for key in ORDER:
        if key == "hurt":
            blob = data["hurt"]
            assert set(blob) == set(DAMAGE) | {"generic"}, (mid, set(blob))
            hurt = {}
            for dk in ["generic"] + DAMAGE:
                pairs = blob[dk]
                want = 10 if dk == "generic" else 1
                if len(pairs) != want:
                    errors.append((mid, dk, len(pairs), want))
                hurt[dk] = [{"zh": z, "en": e} for z, e in pairs]
            scen["hurt"] = hurt
        else:
            pairs = data[key]
            want = 10 + min(4, max(0, round(10 * (entry["weights"][key] - 1))))
            if len(pairs) != want:
                errors.append((mid, key, len(pairs), want))
            scen[key] = [{"zh": z, "en": e} for z, e in pairs]
    mobs.append({"mob_id": mid, "scenarios": scen})

for mob in mobs:
    for key, val in mob["scenarios"].items():
        groups = val.items() if key == "hurt" else [("", val)]
        for sub, pairs in groups:
            for p in pairs:
                total += 1
                zh, en = p["zh"], p["en"]
                if not (6 <= len(zh) <= 20):
                    errors.append((mob["mob_id"], key, sub, "zh-len", len(zh), zh))
                if not (4 <= len(en.split()) <= 14):
                    errors.append((mob["mob_id"], key, sub, "en-words", len(en.split()), en))
                for text in (zh, en):
                    if text in seen:
                        errors.append(("dup", seen[text], mob["mob_id"], key, text))
                    seen[text] = mob["mob_id"]

out = {"batch": "u0391", "mobs": mobs}
(ROOT / "data/dialogue/unique/u0391.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("total", total)
for e in errors:
    print("ERR", e)
print("errors", len(errors))
