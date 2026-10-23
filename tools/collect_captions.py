# Collect English caption files from the channels in a TSV (handle, category, accent).
# Usage: python3 -I tools/collect_captions.py tools/channels.tsv <clips per channel> <path to yt-dlp> [handles…]
# Writes <TSV folder>/videos/<id>.json and skips clips already there. When YouTube rate-limits (no answer, or
# several clips in a row with no caption tracks while a known clip has none either), it pauses and tries again.
import json, os, sys, subprocess, time, urllib.request, html
PAUSE = int(os.environ.get('PAUSE_MIN', '15')) * 60
PROBE = 'UF8uR6Z6KLc'  # a TED talk that always has captions: if it has none either, YouTube is blocking us
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
def info_of(vid):
    p = subprocess.run([ytdlp, '-J', '--skip-download', '--no-warnings', '--ignore-no-formats-error', '--extractor-args', 'youtube:player_client=web_embedded', f'https://www.youtube.com/watch?v={vid}'],
                       capture_output=True, text=True, timeout=120)
    return json.loads(p.stdout or 'null')
def blocked_now():
    try: i = info_of(PROBE)
    except Exception: return True
    return not (i and (i.get('subtitles') or i.get('automatic_captions')))
for line in open(sys.argv[1], encoding='utf-8'):
    h, cat, acc = line.rstrip('\n').split('\t')
    if only and h not in only: continue
    lst = subprocess.run([ytdlp, '--flat-playlist', '--playlist-end', str(per * 3), '--print', '%(id)s\t%(duration)s',
                          f'https://www.youtube.com/{h}/videos'], capture_output=True, text=True, timeout=300).stdout.splitlines()
    got = skipped = 0
    empty, tries = 0, {}
    queue = list(lst)
    while queue:
        row = queue.pop(0)
        if got >= per: break
        try: vid, dur = row.split('\t'); dur = float(dur)
        except ValueError: continue
        if not (45 <= dur <= 1500): continue
        fn = os.path.join(out, vid + '.json')
        if os.path.exists(fn): got += 1; continue
        try:
            info = info_of(vid)
            if info and not (info.get('subtitles') or info.get('automatic_captions')): empty += 1
            else: empty = 0
            if (not info or empty >= 4) and tries.get(vid, 0) < 2:
                if blocked_now():
                    tries[vid] = tries.get(vid, 0) + 1
                    print('  rate-limited at', vid, '- pausing', PAUSE // 60, 'min', flush=True)
                    time.sleep(PAUSE); empty = 0; queue.insert(0, row); continue
                if empty >= 8: print('  no captions on this channel, moving on', flush=True); break
            if not info: skipped += 1; continue
            if info.get('playable_in_embed') is False or info.get('age_limit', 0) > 0 or info.get('availability') not in (None, 'public'):
                skipped += 1; continue
            en = ['en', 'en-US', 'en-GB', 'en-AU', 'en-CA', 'en-IE', 'en-NZ']
            subs = info.get('subtitles') or {}
            # Hand-made English tracks are sometimes named like "en-eEY6OEpapPo"; accept those too.
            url = pick(subs, en + sorted(k for k in subs if k.startswith('en-') and k not in en)); kind = 'm'
            if not url: url = pick(info.get('automatic_captions') or {}, ['en-orig', 'en']); kind = 'a'
            if not url: skipped += 1; continue
            segs = segs_from(fetch(url))
        except Exception as e:
            skipped += 1; print('  skip', vid, type(e).__name__, str(e)[:80], flush=True); time.sleep(5); continue
        if len(segs) < 5: skipped += 1; continue
        json.dump({'id': vid, 't': info.get('title'), 'ch': info.get('channel') or h, 'cat': cat, 'acc': acc, 'cap': kind,
                   'dur': dur, 'date': info.get('upload_date'), 's': segs}, open(fn, 'w', encoding='utf-8'), ensure_ascii=False)
        got += 1; time.sleep(6)
    print(f'{h}\t{cat}\t{acc}\tgot={got}\tskipped={skipped}', flush=True)
