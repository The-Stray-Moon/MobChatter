import json, re, glob, sys

plan = json.load(open('data/dialogue/unique_plan.json', encoding='utf-8'))
batch = 'u0329'
d = json.load(open('data/dialogue/unique/u0329.json', encoding='utf-8'))
pms = {m['mob_id']: m for m in plan[batch]}
CJK = re.compile(r'[\u4e00-\u9fff]')

def zh_len(s):
    return len(CJK.findall(s))

def word_count(s):
    return len(re.findall(r"[A-Za-z0-9'’\-]+", s))

problems = []
seen_zh, seen_en = {}, {}
total = 0
for m in d['mobs']:
    pm = pms[m['mob_id']]
    w = pm['weights']
    for s, v in m['scenarios'].items():
        if s == 'hurt':
            for k, arr in v.items():
                exp = 10 if k == 'generic' else 1
                if len(arr) != exp:
                    problems.append(('count', m['mob_id'], 'hurt.' + k, len(arr), exp))
                for line in arr:
                    total += 1
                    check(m['mob_id'], s, line)
        else:
            exp = 10 + max(0, min(4, round(10 * (w[s] - 1))))
            if len(v) != exp:
                problems.append(('count', m['mob_id'], s, len(v), exp))
            for line in v:
                total += 1
                check(m['mob_id'], s, line)

def check(mid, s, line):
    z, e = line['zh'], line['en']
    if not (6 <= zh_len(z) <= 20):
        problems.append(('zhlen', mid, s, z, zh_len(z)))
    if not (4 <= word_count(e) <= 14):
        problems.append(('enlen', mid, s, e, word_count(e)))
    if z in seen_zh:
        problems.append(('dupzh', mid, s, z, seen_zh[z]))
    if e in seen_en:
        problems.append(('dupen', mid, s, e, seen_en[e]))
    seen_zh[z] = (mid, s)
    seen_en[e] = (mid, s)

# duplicate check against previously delivered files
older = {}
for f in glob.glob('data/dialogue/unique/u0*.json'):
    if f.endswith('u0329.json'):
        continue
    try:
        od = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    for m in od.get('mobs', []):
        sc = m.get('scenarios', {})
        for s, v in sc.items():
            items = [x for arr in v.values() for x in arr] if s == 'hurt' else v
            for line in items:
                older.setdefault(line['zh'], f)
                older.setdefault(line['en'], f)
for k in list(seen_zh) + list(seen_en):
    if k in older:
        problems.append(('crossdup', k, older[k]))

print('total lines', total)
for p in problems:
    print(p)
