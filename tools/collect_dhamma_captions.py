# Fetch English auto captions (json3, word timing kept) for the English-only Dhamma discussions.
import json, os, subprocess, sys, time, urllib.request, html
yt, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(src, encoding='utf-8').read()
items = json.loads(raw) if src.endswith('.json') else json.loads(raw.split('=', 1)[1].rstrip().rstrip(';'))
def fetch(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(90 * (i + 1)); continue
            raise
    raise RuntimeError('429')
ok = 0
for vid, title, dur, cat in items:
    fn = os.path.join(out, vid + '.json')
    if os.path.exists(fn): ok += 1; continue
    try:
        p = subprocess.run([yt, '-J', '--skip-download', '--no-warnings', '--ignore-no-formats-error', '--extractor-args',
                            'youtube:player_client=web_embedded', f'https://www.youtube.com/watch?v={vid}'], capture_output=True, text=True, timeout=180)
        info = json.loads(p.stdout or 'null')
        if not info: print('blocked', vid, flush=True); time.sleep(60); continue
        tracks = (info.get('subtitles') or {}).get('en') or (info.get('automatic_captions') or {}).get('en-orig') or (info.get('automatic_captions') or {}).get('en') or []
        url = next((f['url'] for f in tracks if f.get('ext') == 'json3'), None)
        if not url: print('nocaps', vid, flush=True); continue
        j = fetch(url)
        segs = []
        for ev in j.get('events', []):
            if 'segs' not in ev: continue
            t = ''.join(s.get('utf8', '') for s in ev['segs']).replace('\n', ' ').strip()
            if t: segs.append([round(ev['tStartMs'] / 1000, 2), round(ev.get('dDurationMs', 0) / 1000, 2), html.unescape(t)])
        json.dump({'id': vid, 't': title, 'cat': cat, 'dur': dur, 'manual': bool((info.get('subtitles') or {}).get('en')), 's': segs}, open(fn, 'w', encoding='utf-8'), ensure_ascii=False)
        ok += 1; print('ok', ok, vid, len(segs), flush=True); time.sleep(4)
    except Exception as e:
        print('err', vid, type(e).__name__, str(e)[:80], flush=True); time.sleep(10)
print('done', ok, 'of', len(items), flush=True)
