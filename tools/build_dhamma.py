# Build dhamma-corpus.js from Dhamma discussion caption files (videos/<id>.json with t, cat, dur, s).
# Usage: python3 -I tools/build_dhamma.py <caption dir> dhamma-corpus.js
import json, glob, os, sys, re
src, dst = sys.argv[1], sys.argv[2]
vids, segs = [], []
for f in sorted(glob.glob(os.path.join(src, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    s = [x for x in d['s'] if x[2] and not re.fullmatch(r'\[.*\]|\(.*\)', x[2])]
    if len(s) < 20: continue
    words = sum(len(x[2].split()) for x in s)
    span = max(1.0, (s[-1][0] + s[-1][1]) - s[0][0])
    vi = len(vids)
    # Same row shape as the main corpus; accent, category and level are fixed for these talks.
    vids.append([d['id'], d['t'], 'International Dhamma Discussions', 'dhamma', 'INTL', 'a', int(d.get('dur') or span), round(words / span * 60), 'B2'])
    for st, du, tx in s:
        segs.append([vi, st, du, re.sub(r'\s+', ' ', tx)])
with open(dst, 'w', encoding='utf-8') as o:
    o.write('window.DHAMMA_CORPUS=')
    json.dump({'v': vids, 's': segs}, o, ensure_ascii=False, separators=(',', ':'))
    o.write(';\n')
print(len(vids), 'talks', len(segs), 'lines', os.path.getsize(dst) // 1024, 'KB')
