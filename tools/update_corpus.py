# Add new general clips once a week. Run by .github/workflows/update-corpus.yml.
#  1. Rebuild per-clip records from the published data.js and data-*.js (no raw caption files are kept).
#  2. List the newest clips of the channels in tools/channels.tsv, accents and categories with the fewest clips first.
#  3. Keep only clips that suit a classroom: 1–20 minutes, embeddable, not age-restricted, no violent or adult words in
#     the title, few bleeped words, mostly speech (not music), English captions (hand-made ones preferred).
#  4. Keep the corpus under --max clips by dropping auto-captioned clips from the biggest groups, fastest speech first.
#  5. Rebuild data.js with tools/build_data.py; the workflow then runs tools/count_lessons.js.
# Usage (repository root): python3 -I tools/update_corpus.py [--limit 80] [--minutes 240] [--per-channel 3] [--max 3000]
# On the owner's Windows computer (tools/windows/run.bat) the work is split in two so a long night of collecting never
# conflicts with other commits: --save-dir DIR only collects new clips into DIR, then, after pulling the latest main,
# --merge-dir DIR merges them into the published corpus and rebuilds.
import argparse, collections, html, json, os, random, re, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['PYTHONUTF8'] = '1'  # yt-dlp output holds emoji and Thai; Windows consoles default to other code pages
RUN = dict(capture_output=True, text=True, encoding='utf-8', errors='replace')
YTDLP = [sys.executable, '-m', 'yt_dlp']
PROBE = 'UF8uR6Z6KLc'  # a TED talk that always has captions: if it has none either, YouTube is blocking us
EN = ['en', 'en-US', 'en-GB', 'en-AU', 'en-CA', 'en-IE', 'en-NZ']
# Titles with these words are skipped: the site is used with school students.
UNSUITABLE = re.compile(r"\b(murder\w*|kill(ed|ing|s|er)?|shoot(ing|er)s?|shot dead|stab(bed|bing|s)?|rape[ds]?|raping|rapist|sex\w*|porn\w*|drugs?|"
                        r"cocaine|heroin|overdose|suicide|terror\w*|massacre|beheaded|abuse[ds]?|naked|nude|explicit|"
                        r"war crimes?|bomb(ing|ed)?|gore|horror|graphic)\b", re.I)
BLEEP = re.compile(r'\[\s*_+\s*\]|\*\*+|\bf\*+|\bs\*+t')

def read_js(path, prefix_re):
    if not os.path.exists(path): return None
    txt = open(path, encoding='utf-8').read()
    return json.loads(re.sub(prefix_re, '', txt, count=1).rstrip().rstrip(';'))

sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_data

def load_records():
    return build_data.load_docs(ROOT)

class CaptionRateLimited(Exception):
    def __init__(self, retry_after=0):
        super().__init__('HTTP 429: YouTube is limiting caption requests')
        self.retry_after = retry_after


class StopCollection(Exception):
    pass


def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            from email.utils import parsedate_to_datetime
            value = (e.headers or {}).get('Retry-After', '')
            try:
                retry_after = max(0, float(value))
            except (TypeError, ValueError):
                try: retry_after = max(0, parsedate_to_datetime(value).timestamp() - time.time())
                except (TypeError, ValueError, OverflowError): retry_after = 0
            raise CaptionRateLimited(retry_after) from e
        raise


def captions_with_backoff(vid, info, wait_minutes, deadline):
    # Pause the entire collector, then refresh this clip's expiring caption URL.
    for attempt in range(4):
        try:
            return captions(info)
        except CaptionRateLimited as e:
            print('rate limited', vid, str(e), flush=True)
            if wait_minutes <= 0 or attempt == 3:
                raise StopCollection('caption rate limit persists; keeping collected clips for publishing') from e
            delay = max(wait_minutes * 60 * (2 ** attempt), e.retry_after)
            if time.time() + delay >= deadline:
                raise StopCollection('not enough collection time left to wait; keeping collected clips for publishing') from e
            print('pausing collection for', round(delay / 60, 2), 'minutes; retry', attempt + 1, 'of 3', flush=True)
            time.sleep(delay)
            if time.time() >= deadline:
                raise StopCollection('collection time limit reached after waiting') from e
            info = info_of(vid)
            if not has_tracks(info):
                raise StopCollection('caption metadata unavailable after waiting; retry on the next run')

def info_of(vid):
    p = subprocess.run(YTDLP + ['-J', '--skip-download', '--no-warnings', '--ignore-no-formats-error', '--extractor-args',
                                'youtube:player_client=web_embedded', 'https://www.youtube.com/watch?v=' + vid],
                       timeout=180, **RUN)
    return json.loads(p.stdout or 'null')

def has_tracks(info): return bool(info and (info.get('subtitles') or info.get('automatic_captions')))

def blocked_now():
    try: return not has_tracks(info_of(PROBE))
    except Exception: return True

def pick(tracks, langs):
    for l in langs:
        for f in tracks.get(l) or []:
            if f.get('ext') == 'json3': return f['url']
    return None

def captions(info):
    subs = info.get('subtitles') or {}
    url = pick(subs, EN + sorted(k for k in subs if k.startswith('en-') and k not in EN)); kind = 'm'
    if not url: url = pick(info.get('automatic_captions') or {}, ['en-orig', 'en']); kind = 'a'
    if not url: return None, None
    segs = []
    for ev in fetch_json(url).get('events', []):
        if 'segs' not in ev: continue
        t = ''.join(s.get('utf8', '') for s in ev['segs']).replace('\n', ' ').strip()
        if t: segs.append([round(ev['tStartMs'] / 1000, 2), round(ev.get('dDurationMs', 0) / 1000, 2), html.unescape(t)])
    return segs, kind

def suitable(segs):
    """Mostly speech, enough of it, and hardly any bleeped words."""
    if len(segs) < 20: return 'too short'
    music = sum(1 for s in segs if re.fullmatch(r'\s*(\[.*\]|\(.*\)|♪.*)\s*', s[2]))
    if music > 0.3 * len(segs): return 'mostly music'
    if sum(1 for s in segs if BLEEP.search(s[2])) > 2: return 'bleeped words'
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=80, help='new clips to add in one run')
    ap.add_argument('--minutes', type=float, default=240)
    ap.add_argument('--per-channel', type=int, default=3)
    ap.add_argument('--depth', type=int, default=15, help='newest clips to look at per channel')
    ap.add_argument('--max', type=int, default=30000, help='largest corpus to keep')
    ap.add_argument('--save-dir', help='only collect: write new clips (and newly skipped ids) to this folder')
    ap.add_argument('--merge-dir', help='only merge: add the clips saved in this folder to the corpus and rebuild')
    ap.add_argument('--wait-when-blocked', type=float, default=0, help='minutes to wait and retry when YouTube blocks (0 = stop)')
    a = ap.parse_args()
    start = time.time()
    skip_path = os.path.join(ROOT, 'tools', 'corpus-skip.json')
    skip = set(json.load(open(skip_path))) if os.path.exists(skip_path) else set()
    recs = load_records()
    published = set(recs)
    # A clip put on the skip list by hand (e.g. reported as unsuitable) also leaves the corpus.
    removed = [v for v in recs if v in skip]
    for v in removed: del recs[v]
    print(len(recs), 'clips published;', len(skip), 'on the skip list;', len(removed), 'removed by the skip list', flush=True)
    saved = {}
    for d in [a.save_dir, a.merge_dir]:
        if not d: continue
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f == 'skip.json': skip.update(json.load(open(os.path.join(d, f))))
            elif f.endswith('.json'):
                r = json.load(open(os.path.join(d, f), encoding='utf-8')); saved[r['id']] = r
    if a.merge_dir:
        new = {k: r for k, r in saved.items() if k not in recs and k not in skip}
        recs.update(new)
        print(len(new), 'clips merged from', a.merge_dir, flush=True)
        return finish(a, recs, published, skip, skip_path, removed)
    known = set(recs) | set(saved)
    room = a.max - len(known)
    if room <= 0:
        print('the corpus is full (', a.max, 'clips ). Raise --max once search runs on a server (step 3).'); return
    a.limit = min(a.limit, room)

    # Everyday speech first (films, series, real conversations, cartoons; see build_data.TIER), then teaching, TV and
    # documentaries, then interviews, TED and news. Within a tier, accents and categories with the fewest clips go first.
    acc_n = collections.Counter(r['acc'] for r in recs.values()); cat_n = collections.Counter(r['cat'] for r in recs.values())
    chans = [l.rstrip('\n').split('\t') for l in open(os.path.join(ROOT, 'tools', 'channels.tsv'), encoding='utf-8') if l.strip()]
    random.shuffle(chans)
    chans.sort(key=lambda c: (build_data.TIER.get(c[1], 1), acc_n[c[2]] + cat_n[c[1]]))

    added, strikes, blocks, stop = 0, 0, 0, False
    unsure = []  # clips with no caption tracks; skipped for good only once YouTube is known not to be blocking us
    for handle, cat, acc in chans:
        if stop or added >= a.limit or time.time() - start > a.minutes * 60: break
        r = subprocess.run(YTDLP + ['--flat-playlist', '--playlist-end', str(a.depth), '--print', '%(id)s\t%(duration)s\t%(title)s',
                                    'https://www.youtube.com/' + handle + '/videos'], timeout=600, **RUN)
        got = 0
        for row in r.stdout.splitlines():
            if got >= a.per_channel or added >= a.limit or time.time() - start > a.minutes * 60: break
            p = row.split('\t', 2)
            if len(p) < 3 or p[0] in known or p[0] in skip: continue
            vid, title = p[0], p[2]
            try: dur = float(p[1])
            except ValueError: continue
            if not 60 <= dur <= 1200: continue
            if UNSUITABLE.search(title): skip.add(vid); print('skip (title)', vid, title[:60], flush=True); continue
            try:
                info = info_of(vid)
                if not has_tracks(info):
                    strikes += 1
                    if info: unsure.append(vid)
                    if strikes >= 4:
                        if blocked_now():
                            unsure.clear(); blocks += 1
                            if not a.wait_when_blocked or blocks > 3: print('blocked by YouTube, stopping this run', flush=True); stop = True; break
                            print('blocked by YouTube, waiting', a.wait_when_blocked, 'minutes', flush=True); time.sleep(a.wait_when_blocked * 60); strikes = 0
                            continue
                        skip.update(unsure); unsure.clear(); strikes = 0
                    continue
                strikes = blocks = 0
                skip.update(unsure); unsure.clear()
                if info.get('playable_in_embed') is False or (info.get('age_limit') or 0) > 0 or info.get('availability') not in (None, 'public'):
                    skip.add(vid); continue
                segs, kind = captions_with_backoff(vid, info, a.wait_when_blocked, start + a.minutes * 60)
            except StopCollection as e:
                print('stopping collection:', str(e), flush=True); stop = True; break
            except Exception as e:
                detail = re.sub(r'https?://\S+', '[URL]', str(e))[:300]
                print('error', vid, type(e).__name__, detail, flush=True); time.sleep(10); continue
            why = 'no English captions' if not segs else suitable(segs)
            if why: skip.add(vid); print('skip (' + why + ')', vid, flush=True); continue
            rec = {'id': vid, 't': info.get('title') or title, 'ch': info.get('channel') or handle, 'cat': cat, 'acc': acc,
                   'cap': kind, 'dur': dur, 's': segs}
            known.add(vid)
            if a.save_dir:
                json.dump(rec, open(os.path.join(a.save_dir, vid + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
                json.dump(sorted(skip), open(os.path.join(a.save_dir, 'skip.json'), 'w'), indent=0)
            else: recs[vid] = rec
            got += 1; added += 1
            print('ok', added, vid, acc, cat, kind, len(segs), flush=True); time.sleep(6)

    if a.save_dir:
        json.dump(sorted(skip), open(os.path.join(a.save_dir, 'skip.json'), 'w'), indent=0)
        print('clips collected this run:', added, '| waiting in', a.save_dir, ':', len(saved) + added); return
    finish(a, recs, published, skip, skip_path, removed)

def finish(a, recs, published, skip, skip_path, removed):
    # Stay under the size limit: drop auto-captioned clips from the biggest accent/category groups, fastest speech first.
    drop = []
    while len(recs) > a.max:
        groups = collections.Counter((r['acc'], r['cat']) for r in recs.values() if r['cap'] == 'a')
        if not groups: break
        g = groups.most_common(1)[0][0]
        victim = max((r for r in recs.values() if r['cap'] == 'a' and (r['acc'], r['cat']) == g), key=lambda r: r.get('wpm') or 0)
        del recs[victim['id']]; drop.append(victim['id'])
    json.dump(sorted(skip), open(skip_path, 'w'), indent=0)
    new = [r for k, r in recs.items() if k not in published]
    gone = [k for k in list(removed) + drop if k in published]
    if not new and not gone: print('no new clips this run'); return
    build_data.append(ROOT, new, gone)
    print('clips added this run:', len(new), '| removed:', len(gone), '| total', len(recs))

if __name__ == '__main__':
    main()
