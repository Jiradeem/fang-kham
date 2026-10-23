import json, os, sys, subprocess, time, urllib.request, html
base = os.path.dirname(os.path.abspath(sys.argv[1]))
out = os.path.join(base, 'videos'); os.makedirs(out, exist_ok=True)
per = int(sys.argv[2]); ytdlp = sys.argv[3]; only = sys.argv[4:]
opener = urllib.request.build_opener()
def fetch(url):
    for i in range(3):
        try:
            with opener.open(url, timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(60 * (i + 1)); continue
            raise
    raise RuntimeError('429')
def segs_from(j):
    res = []
    for ev in j.get('events', []):
        if 'segs' not in ev: continue
        t = ''.join(s.get('utf8', '') for s in ev['segs']).replace('\n', ' ').strip()
        if not t: continue
        res.append([round(ev['tStartMs'] / 1000, 2), round(ev.get('dDurationMs', 0) / 1000, 2), html.unescape(t)])
    return res
def pick(tracks, langs):
    for l in langs:
        for k in tracks:
            if k == l:
                for f in tracks[k]:
                    if f.get('ext') == 'json3': return f['url']
    return None
for line in open(sys.argv[1], encoding='utf-8'):
    h, cat, acc = line.rstrip('\n').split('\t')
    if only and h not in only: continue
    lst = subprocess.run([ytdlp, '--flat-playlist', '--playlist-end', str(per * 3), '--print', '%(id)s\t%(duration)s',
                          f'https://www.youtube.com/{h}/videos'], capture_output=True, text=True, timeout=300).stdout.splitlines()
    got = skipped = 0
    for row in lst:
        if got >= per: break
        try: vid, dur = row.split('\t'); dur = float(dur)
        except ValueError: continue
        if not (45 <= dur <= 1500): continue
        fn = os.path.join(out, vid + '.json')
        if os.path.exists(fn): got += 1; continue
        try:
            p = subprocess.run([ytdlp, '-J', '--skip-download', '--no-warnings', '--ignore-no-formats-error', '--extractor-args', 'youtube:player_client=web_embedded', f'https://www.youtube.com/watch?v={vid}'],
                               capture_output=True, text=True, timeout=120)
            info = json.loads(p.stdout or "null")
            if not info:
                skipped += 1; print("  bot-check", vid, flush=True); time.sleep(45); continue
            if info.get('playable_in_embed') is False or info.get('age_limit', 0) > 0 or info.get('availability') not in (None, 'public'):
                skipped += 1; continue
            en = ['en', 'en-US', 'en-GB', 'en-AU', 'en-CA', 'en-IE', 'en-NZ']
            url = pick(info.get('subtitles') or {}, en); kind = 'm'
            if not url: url = pick(info.get('automatic_captions') or {}, ['en-orig', 'en']); kind = 'a'
            if not url: skipped += 1; continue
            segs = segs_from(fetch(url))
        except Exception as e:
            skipped += 1; print('  skip', vid, type(e).__name__, str(e)[:80], flush=True); time.sleep(5); continue
        if len(segs) < 5: skipped += 1; continue
        json.dump({'id': vid, 't': info.get('title'), 'ch': info.get('channel') or h, 'cat': cat, 'acc': acc, 'cap': kind,
                   'dur': dur, 'date': info.get('upload_date'), 's': segs}, open(fn, 'w', encoding='utf-8'), ensure_ascii=False)
        got += 1; time.sleep(3)
    print(f'{h}\t{cat}\t{acc}\tgot={got}\tskipped={skipped}', flush=True)
