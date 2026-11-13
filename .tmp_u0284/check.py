import json, glob
mine = json.load(open('.tmp_u0284/u0284.json', encoding='utf-8'))
out = []
def groups(name, payload):
    if name == 'hurt':
        yield 'generic', payload['generic']
        for d, v in payload.items():
            if d != 'generic':
                yield d, v
    else:
        yield name, payload
zh = {}
for m in mine['mobs']:
    for name, payload in m['scenarios'].items():
        for k, lines in groups(name, payload):
            for ln in lines:
                zh.setdefault(ln['zh'], []).append(m['mob_id'])
for k, v in zh.items():
    if len(v) > 1:
        out.append('DUP-IN-BATCH %r %s' % (k, v))
for f in glob.glob('data/dialogue/unique/u*.json'):
    if f.endswith('u0284.json'):
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    for m in d.get('mobs', []):
        for name, payload in m['scenarios'].items():
            for k, lines in groups(name, payload):
                for ln in lines:
                    if isinstance(ln, dict) and ln.get('zh') in zh:
                        out.append('CROSS %s %r owner=%s' % (f, ln['zh'], zh[ln['zh']]))
lines = sum(len(l) for m in mine['mobs'] for name,p in m['scenarios'].items() for k,l in groups(name,p))
out.append('LINES %d' % lines)
open('.tmp_u0284/issues.txt','w',encoding='utf-8').write('\n'.join(out))
