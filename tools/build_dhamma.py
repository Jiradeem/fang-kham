# Build the Dhamma corpus as shards the browser loads on demand.
# Usage: python3 -I tools/build_dhamma.py <caption dir> <output dir>
# Writes dhamma-shards.js (the index) and one dhamma-corpus-<key>.js per shard:
#   short          = "Studying Dhamma with Ajahn Sujin" excerpts (manual English captions)
#   <year>-<part>  = long discussions grouped by the year in their title, at most PER_SHARD talks each
import json, glob, os, sys, re, collections
src, out = sys.argv[1], sys.argv[2]
PER_SHARD = 60
groups = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(src, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    s = [x for x in d['s'] if x[2] and not re.fullmatch(r'\[.*\]|\(.*\)', x[2])]
    if len(s) < 5: continue
    if d.get('cat', '').startswith('คลิปสั้น'): key = 'short'
    else:
        y = re.findall(r'20\d\d', d.get('t', ''))
        key = y[-1] if y else 'other'
    groups[key].append((d, s))
index = []
def write(key, label, items):
    vids, segs = [], []
    for d, s in items:
        words = sum(len(x[2].split()) for x in s)
        span = max(1.0, (s[-1][0] + s[-1][1]) - s[0][0])
        vi = len(vids)
        vids.append([d['id'], d['t'], 'Ajahn Sujin · ' + d.get('cat', ''), 'dhamma', 'INTL', 'm' if d.get('manual') else 'a',
                     int(d.get('dur') or span), round(words / span * 60), 'B2'])
        segs += [[vi, st, du, re.sub(r'\s+', ' ', tx)] for st, du, tx in s]
    fn = 'dhamma-corpus-' + key + '.js'
    with open(os.path.join(out, fn), 'w', encoding='utf-8') as o:
        o.write('(window.DHAMMA_SHARDS=window.DHAMMA_SHARDS||{})[' + json.dumps(key) + ']=')
        json.dump({'v': vids, 's': segs}, o, ensure_ascii=False, separators=(',', ':'))
        o.write(';\n')
    index.append([key, label, len(vids), len(segs), os.path.getsize(os.path.join(out, fn)) // 1024])
if groups.get('short'): write('short', 'คลิปสั้น (ซับคนพิมพ์)', groups.pop('short'))
for year in sorted(groups, key=lambda y: (y == 'other', -int(y) if y.isdigit() else 0)):
    items = sorted(groups[year], key=lambda x: x[0].get('t', ''))
    parts = [items[i:i + PER_SHARD] for i in range(0, len(items), PER_SHARD)]
    for n, part in enumerate(parts, 1):
        label = (year if year != 'other' else 'ไม่ระบุปี') + (' ชุด ' + str(n) if len(parts) > 1 else '')
        write(year + '-' + str(n), label, part)
keep = {k for k, *_ in index}
for f in glob.glob(os.path.join(out, 'dhamma-corpus-*.js')):
    if os.path.basename(f)[len('dhamma-corpus-'):-3] not in keep: os.remove(f)
with open(os.path.join(out, 'dhamma-shards.js'), 'w', encoding='utf-8') as o:
    o.write('window.DHAMMA_SHARD_INDEX=' + json.dumps(index, ensure_ascii=False) + ';\n')
for row in index: print(row)
