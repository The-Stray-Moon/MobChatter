# -*- coding: utf-8 -*-
import json, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
src = open('.tmp_u0206_build.py', encoding='utf-8').read()
head = src.split('ORDER = [')[0]
head = head.replace("sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')", "")
ns = {}
exec(head, ns)
data = ns['data']

mine = {}
for mid, scs in data.items():
    for sc, items in scs.items():
        groups = [items] if isinstance(items, list) else items.values()
        for g in groups:
            for zh, en in g:
                mine[zh] = (mid, sc, en)

hits = {}
for f in glob.glob('data/dialogue/unique/u*.json'):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    for mob in d.get('mobs', []):
        for sc, items in mob.get('scenarios', {}).items():
            groups = [items] if isinstance(items, list) else items.values()
            for g in groups:
                for line in g:
                    if not isinstance(line, dict):
                        continue
                    if line.get('zh') in mine:
                        hits.setdefault(line['zh'], []).append(f)

print('collisions', len(hits))
for k, v in hits.items():
    print('%s | %s | %s' % (mine[k][0], mine[k][1], k))
