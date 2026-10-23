# Keep the Dhamma section up to date. Run by .github/workflows/update-dhamma.yml every few hours.
#  1. List the newest clips of the verified Ajahn Sujin channels and add new ones to dhamma.js.
#  2. Fetch English captions for clips that are not in the corpus yet (newest and short clips first),
#     within a time budget so a single run stays short and polite to YouTube.
#  3. Rebuild dhamma-shards.js and dhamma-corpus-*.js from the existing shards plus the new captions.
# Usage (repository root): python3 -I tools/update_dhamma.py [--limit 40] [--minutes 50] [--caps-dir DIR] [--no-fetch]
import argparse, collections, glob, html, json, os, re, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANNELS = [  # (url, category or None to classify by title)
    ('https://www.youtube.com/channel/UC0gJW7nCHv_4Sv1CF0UTwWQ/videos', 'คลิปสั้น Studying Dhamma'),
    ('https://www.youtube.com/@IntlDhammaDiscussions/streams', None),
    ('https://www.youtube.com/@IntlDhammaDiscussions/videos', None),
]
PRIORITY = {'คลิปสั้น Studying Dhamma': 0, 'สนทนาธรรม (อังกฤษ)': 1, 'International': 1, 'สหายธรรมต่างชาติ (มศพ.)': 1}
PER_SHARD = 60
YTDLP = [sys.executable, '-m', 'yt_dlp']

def classify(t):
    l = t.lower()
    if 'chinese' in l or re.search(r'[一-鿿]', t): return 'จีน–อังกฤษ'
    if 'viet' in l: return 'เวียดนาม–อังกฤษ'
    if 'india' in l or 'hindi' in l or 'nepal' in l: return 'อินเดีย / เนปาล'
    if 'khmer' in l or 'cambod' in l: return 'ไทย–เขมร'
    if 'international' in l: return 'International'
    return 'สนทนาธรรม (อังกฤษ)'

def read_js(path, prefix_re):
    if not os.path.exists(path): return None
    txt = open(path, encoding='utf-8').read()
    return json.loads(re.sub(prefix_re, '', txt, count=1).rstrip().rstrip(';'))

def list_new(known, depth):
    found = []
    for url, cat in CHANNELS:
        r = subprocess.run(YTDLP + ['--flat-playlist', '--playlist-end', str(depth), '--print', '%(id)s|%(duration)s|%(title)s', url],
                           capture_output=True, text=True, timeout=600)
        for line in r.stdout.splitlines():
            p = line.split('|', 2)
            if len(p) < 3 or not p[0] or p[0] in known: continue
            try: d = int(float(p[1]))
            except ValueError: d = 0
            if d and d < 120 and cat is None: continue
            known.add(p[0]); found.append([p[0], p[2].strip(), d, cat or classify(p[2])])
    return found

def fetch_json(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(60 * (i + 1)); continue
            raise
    raise RuntimeError('429')

def captions(vid):
    p = subprocess.run(YTDLP + ['-J', '--skip-download', '--no-warnings', '--ignore-no-formats-error', '--extractor-args',
                                'youtube:player_client=web_embedded', 'https://www.youtube.com/watch?v=' + vid], capture_output=True, text=True, timeout=180)
    info = json.loads(p.stdout or 'null')
    if not info: return None, 'blocked'
    manual = (info.get('subtitles') or {}).get('en') or []
    tracks = manual or (info.get('automatic_captions') or {}).get('en-orig') or (info.get('automatic_captions') or {}).get('en') or []
    url = next((f['url'] for f in tracks if f.get('ext') == 'json3'), None)
    if not url: return None, 'nocaps'
    segs = []
    for ev in fetch_json(url).get('events', []):
        if 'segs' not in ev: continue
        t = ''.join(s.get('utf8', '') for s in ev['segs']).replace('\n', ' ').strip()
        if t: segs.append([round(ev['tStartMs'] / 1000, 2), round(ev.get('dDurationMs', 0) / 1000, 2), html.unescape(t)])
    return {'s': segs, 'manual': bool(manual)}, 'ok'

def load_records():
    """Rebuild per-clip records from the published shards, so no raw caption files need to be kept."""
    recs = {}
    index = read_js(os.path.join(ROOT, 'dhamma-shards.js'), r'^window\.DHAMMA_SHARD_INDEX=') or []
    for key, *_ in index:
        part = read_js(os.path.join(ROOT, 'dhamma-corpus-%s.js' % key), r'^\(window\.DHAMMA_SHARDS=window\.DHAMMA_SHARDS\|\|\{\}\)\[[^\]]*\]=')
        if not part: continue
        by = collections.defaultdict(list)
        for vi, st, du, tx in part['s']: by[vi].append([st, du, tx])
        for vi, v in enumerate(part['v']):
            recs[v[0]] = {'id': v[0], 't': v[1], 'cat': v[2].split(' · ', 1)[-1], 'dur': v[6], 'manual': v[5] == 'm', 's': by[vi]}
    return recs

def write_shards(recs):
    groups = collections.defaultdict(list)
    for d in recs.values():
        s = [x for x in d['s'] if x[2] and not re.fullmatch(r'\[.*\]|\(.*\)', x[2])]
        if len(s) < 5: continue
        if d['cat'].startswith('คลิปสั้น'): key = 'short'
        else:
            y = re.findall(r'20\d\d', d['t']); key = y[-1] if y else 'other'
        groups[key].append((d, s))
    index = []
    def write(key, label, items):
        vids, segs = [], []
        for d, s in items:
            words = sum(len(x[2].split()) for x in s); span = max(1.0, (s[-1][0] + s[-1][1]) - s[0][0])
            vi = len(vids)
            vids.append([d['id'], d['t'], 'Ajahn Sujin · ' + d['cat'], 'dhamma', 'INTL', 'm' if d.get('manual') else 'a',
                         int(d.get('dur') or span), round(words / span * 60), 'B2'])
            segs += [[vi, st, du, re.sub(r'\s+', ' ', tx)] for st, du, tx in s]
        fn = 'dhamma-corpus-%s.js' % key
        with open(os.path.join(ROOT, fn), 'w', encoding='utf-8') as o:
            o.write('(window.DHAMMA_SHARDS=window.DHAMMA_SHARDS||{})[' + json.dumps(key) + ']=')
            json.dump({'v': vids, 's': segs}, o, ensure_ascii=False, separators=(',', ':')); o.write(';\n')
        index.append([key, label, len(vids), len(segs), os.path.getsize(os.path.join(ROOT, fn)) // 1024])
    if groups.get('short'): write('short', 'คลิปสั้น (ซับคนพิมพ์)', sorted(groups.pop('short'), key=lambda x: x[0]['t']))
    for year in sorted(groups, key=lambda y: (y == 'other', -int(y) if y.isdigit() else 0)):
        items = sorted(groups[year], key=lambda x: x[0]['t'])
        parts = [items[i:i + PER_SHARD] for i in range(0, len(items), PER_SHARD)]
        for n, part in enumerate(parts, 1):
            write(year + '-' + str(n), (year if year != 'other' else 'ไม่ระบุปี') + (' ชุด ' + str(n) if len(parts) > 1 else ''), part)
    keep = {k for k, *_ in index}
    for f in glob.glob(os.path.join(ROOT, 'dhamma-corpus-*.js')):
        if os.path.basename(f)[len('dhamma-corpus-'):-3] not in keep: os.remove(f)
    with open(os.path.join(ROOT, 'dhamma-shards.js'), 'w', encoding='utf-8') as o:
        o.write('window.DHAMMA_SHARD_INDEX=' + json.dumps(index, ensure_ascii=False) + ';\n')
    return index

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=40)
    ap.add_argument('--minutes', type=float, default=50)
    ap.add_argument('--depth', type=int, default=60, help='how many newest clips to check per channel tab')
    ap.add_argument('--caps-dir', help='extra folder of <id>.json caption files to merge (from tools/collect_dhamma_captions.py)')
    ap.add_argument('--no-fetch', action='store_true')
    a = ap.parse_args()
    start = time.time()
    clips = read_js(os.path.join(ROOT, 'dhamma.js'), r'^window\.DHAMMA=') or []
    known = {c[0] for c in clips}
    recs = load_records()
    if a.caps_dir:
        for f in glob.glob(os.path.join(a.caps_dir, '*.json')):
            d = json.load(open(f, encoding='utf-8'))
            if d['id'] not in recs: recs[d['id']] = {'id': d['id'], 't': d['t'], 'cat': d.get('cat', ''), 'dur': d.get('dur', 0), 'manual': d.get('manual', False), 's': d['s']}
    new = [] if a.no_fetch else list_new(known, a.depth)
    clips = new + clips
    print(len(new), 'new clips listed;', len(clips), 'in total;', len(recs), 'with captions', flush=True)
    todo = [c for c in clips if c[0] not in recs]
    todo.sort(key=lambda c: (PRIORITY.get(c[3], 2), c[0] not in {n[0] for n in new}))
    got = 0
    for vid, title, dur, cat in ([] if a.no_fetch else todo):
        if got >= a.limit or time.time() - start > a.minutes * 60: break
        try:
            res, status = captions(vid)
        except Exception as e:
            print('error', vid, type(e).__name__, flush=True); time.sleep(10); continue
        if status == 'blocked': print('blocked by YouTube, stopping this run', flush=True); break
        if res is None: print(status, vid, flush=True); continue
        recs[vid] = {'id': vid, 't': title, 'cat': cat, 'dur': dur, 'manual': res['manual'], 's': res['s']}
        got += 1; print('ok', got, vid, len(res['s']), flush=True); time.sleep(4)
    with open(os.path.join(ROOT, 'dhamma.js'), 'w', encoding='utf-8') as o:
        o.write('window.DHAMMA=' + json.dumps(clips, ensure_ascii=False, separators=(',', ':')) + ';\n')
    index = write_shards(recs)
    print('captions added this run:', got, '| shards:', len(index), '| clips searchable:', sum(r[2] for r in index), 'of', len(clips))

if __name__ == '__main__':
    main()
