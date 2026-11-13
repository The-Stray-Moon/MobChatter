import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'data/dialogue/unique/u0320.json'
d = json.load(open(path, encoding='utf-8'))

plan = json.load(open('data/dialogue/unique_plan.json', encoding='utf-8'))
W = {m['mob_id']: m['weights'] for m in plan['u0320']}


def j(o):
    return json.dumps(o, ensure_ascii=False)


lines = ['{"batch": "u0320", "mobs": [']
for mi, m in enumerate(d['mobs']):
    w = W[m['mob_id']]
    lines.append('  {"mob_id": %s, "scenarios": {' % j(m['mob_id']))
    keys = list(m['scenarios'].keys())
    for ki, k in enumerate(keys):
        comma = ',' if ki != len(keys) - 1 else ''
        v = m['scenarios'][k]
        if k != 'hurt':
            lines.append('    "%s": [' % k)
            for ii, s in enumerate(v):
                c = ',' if ii != len(v) - 1 else ''
                lines.append('      %s%s' % (j(s), c))
            lines.append('    ]' + comma)
        else:
            lines.append('    "hurt": {')
            hk = list(v.keys())
            for hi, kk in enumerate(hk):
                c = ',' if hi != len(hk) - 1 else ''
                arr = v[kk]
                if kk == 'generic':
                    lines.append('      "generic": [')
                    for ii, s in enumerate(arr):
                        cc = ',' if ii != len(arr) - 1 else ''
                        lines.append('        %s%s' % (j(s), cc))
                    lines.append('      ]' + c)
                else:
                    lines.append('      "%s": [%s]%s' % (kk, j(arr[0]), c))
            lines.append('    }' + comma)
    lines.append('  }}' + (',' if mi != len(d['mobs']) - 1 else ''))
lines.append(']}')
text = '\n'.join(lines) + '\n'

assert json.loads(text) == d

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

n = 0
for m in d['mobs']:
    for k, v in m['scenarios'].items():
        if k == 'hurt':
            for arr in v.values():
                n += len(arr)
        else:
            n += len(v)
print('ok', len(d['mobs']), n)
