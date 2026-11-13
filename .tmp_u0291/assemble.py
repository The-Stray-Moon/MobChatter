# -*- coding: utf-8 -*-
import json, glob, re, sys
from pathlib import Path

ROOT = Path('.')
ORDER = ["walk", "idle", "look_player", "tempted", "collide", "mate", "pickup",
         "target_acquire", "targeting", "melee_attack", "spawn"]
HURT = ["generic", "fire", "fall", "drown", "explosion", "projectile", "magic",
        "starvation", "lightning", "void"]
plan = {m["mob_id"]: m for m in json.load(open('data/dialogue/unique_plan.json', encoding='utf-8'))["u0291"]}

def expect(w):
    return 10 + min(4, max(0, round(10 * (w - 1))))

mobs = []
problems = []
for i in range(1, 5):
    d = json.load(open(f'.tmp_u0291/m{i}.json', encoding='utf-8'))
    mid = d["mob_id"]
    w = plan[mid]["weights"]
    out = {"mob_id": mid, "scenarios": {}}
    for s in ORDER:
        lines = d[s]
        if len(lines) != expect(w[s]):
            problems.append(f"{mid} {s} count {len(lines)} != {expect(w[s])}")
        out["scenarios"][s] = lines
    hurt = {}
    for k in HURT:
        lines = d["hurt"][k]
        if k == "generic":
            if len(lines) != expect(w["hurt"]):
                problems.append(f"{mid} hurt.generic {len(lines)}")
        elif len(lines) != 1:
            problems.append(f"{mid} hurt.{k} {len(lines)}")
        hurt[k] = lines
    out["scenarios"]["hurt"] = hurt
    mobs.append(out)

zh_re = re.compile(r'[\u4e00-\u9fff]')
for m in mobs:
    for s, v in m["scenarios"].items():
        groups = [("generic", v["generic"])] + [(k, v[k]) for k in HURT if k != "generic"] if s == "hurt" else [(s, v)]
        for name, lines in groups:
            for ln in lines:
                z, e = ln["zh"], ln["en"]
                n = len(zh_re.findall(z))
                if not (6 <= n <= 20):
                    problems.append(f"{m['mob_id']} {name} zh chars {n}: {z}")
                if not (4 <= len(e.split()) <= 14):
                    problems.append(f"{m['mob_id']} {name} en words {len(e.split())}: {e}")

# cross-batch duplicate check (not reading banks)
seen = {}
for f in sorted(glob.glob('data/dialogue/unique/u*.json')):
    if f.endswith('u0291.json'):
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    for mm in d["mobs"]:
        for s, v in mm["scenarios"].items():
            gs = [("generic", v["generic"])] + [(k, v[k]) for k in v if k != "generic"] if s == "hurt" else [(s, v)]
            for name, lines in gs:
                for ln in lines:
                    if not isinstance(ln, dict):
                        continue
                    seen.setdefault(ln.get("zh", ""), mm["mob_id"])
for m in mobs:
    for s, v in m["scenarios"].items():
        gs = [("generic", v["generic"])] + [(k, v[k]) for k in v if k != "generic"] if s == "hurt" else [(s, v)]
        for name, lines in gs:
            for ln in lines:
                if ln["zh"] in seen:
                    problems.append(f"DUP {ln['zh']} vs {seen[ln['zh']]}")

if problems:
    print("\n".join(problems))
    sys.exit(1)

total = sum(len(v["generic"]) + sum(len(v[k]) for k in HURT if k != "generic")
            if s == "hurt" else len(v)
            for m in mobs for s, v in m["scenarios"].items())

lines = ['{"batch": "u0291", "mobs": [']
for mi, m in enumerate(mobs):
    lines.append('{"mob_id": %s, "scenarios": {' % json.dumps(m["mob_id"]))
    parts = []
    for s in ORDER + ["hurt"]:
        key = json.dumps(s)
        if s == "hurt":
            h = m["scenarios"]["hurt"]
            hparts = ['"generic": ' + json.dumps(h["generic"], ensure_ascii=False)]
            for k in HURT[1:]:
                hparts.append(json.dumps(k) + ': ' + json.dumps(h[k], ensure_ascii=False))
            parts.append(key + ": {\n" + ",\n".join(hparts) + "\n}")
        else:
            body = ",\n".join(json.dumps(x, ensure_ascii=False) for x in m["scenarios"][s])
            parts.append(key + ": [\n" + body + "\n]")
    lines.append(",\n".join(parts) + "\n}" + ("," if mi < len(mobs) - 1 else ""))
lines.append("]}")
Path('data/dialogue/unique/u0291.json').write_text("\n".join(lines) + "\n", encoding='utf-8')

chk = json.load(open('data/dialogue/unique/u0291.json', encoding='utf-8'))
assert len(chk["mobs"]) == 4
print("ok", len(chk["mobs"]), "mobs", total, "lines")
