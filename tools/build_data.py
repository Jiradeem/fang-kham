# Build the general corpus for the site (format 2: append-only parts plus a word index).
#   data.js        window.CORPUS = {fmt: 2, parts: [[file, clips, lines], …], clips, lines, accs, sets, quiz, top, cuts, removed}
#   data-pNNNN.js  (window.CORPUS_PARTS = …)[n] = {v: [[id, title, channel, cat, acc, cap, dur, wpm, level], …],
#                                                  s: [[clipIndexInPart, start, dur, text], …]}
#   data-i-X.js    (window.CORPUS_IDX = …)['X'] = {token: [part numbers] or 0 (= in most parts)}, X = first letter
# The page loads part 1 at once and other parts only when a search needs them (the index says which parts hold a word).
# Published parts are never rewritten: new clips go into new parts and removed clips are listed in `removed`,
# so nightly commits stay small and the repository does not balloon.
# Usage: python3 -I tools/build_data.py <caption dir> data.js     full rebuild of everything (renumbers the parts)
#        tools/update_corpus.py calls append() for new clips.
import json, glob, os, sys, re, collections

PART_LINES = 20000   # about 1 MB per part
COMMON = 0.5         # a token found in more than half of the parts is marked 0 in the index
FIRST = {'learning': 0, 'kids': 0, 'ted': 1, 'documentary': 1}

SETS = {
    'คำเชื่อมประโยค': ['however', 'therefore', 'although', 'even though', 'moreover', 'meanwhile', 'instead', 'otherwise', 'in fact',
                      'on the other hand', 'as a result', 'for example', 'for instance', 'after all', 'whereas', 'unless',
                      'eventually', 'besides', 'anyway', 'in addition', 'despite', 'so that', 'as long as', 'whether'],
    'Phrasal verbs': ['figure out', 'give up', 'come up with', 'find out', 'turn out', 'look forward to', 'pick up', 'run out of',
                      'end up', 'carry on', 'set up', 'put off', 'deal with', 'point out', 'go through', 'work out', 'get rid of',
                      'show up', 'bring up', 'look after', 'take off', 'come across', 'break down', 'catch up', 'look into',
                      'hold on', 'move on', 'sort out', 'turn down', 'get along'],
    'สำนวนพูดทั่วไป': ['you know', 'i mean', 'kind of', 'sort of', 'to be honest', 'of course', 'i guess', 'pretty much',
                       'at the end of the day', 'it depends', 'makes sense', "i'm not sure", 'as well', 'by the way',
                       'no way', 'oh my god', 'all right', 'come on', 'i think so', 'not really', 'fair enough', 'to be fair',
                       'at least', 'right now', 'in a way'],
    'คำในข่าว': ['according to', 'government', 'announced', 'investigation', 'election', 'crisis', 'economy', 'minister',
                 'policy', 'reported', 'officials', 'residents', 'impact', 'significant', 'climate', 'conflict', 'community',
                 'authorities', 'police', 'prime minister', 'president', 'budget', 'inflation', 'protest', 'emergency'],
    'คำบอกความรู้สึก': ['excited', 'worried', 'amazing', 'terrible', 'frustrated', 'surprised', 'grateful', 'nervous', 'proud',
                       'scared', 'annoyed', 'disappointed', 'thrilled', 'embarrassed', 'confused', 'relieved', 'lonely',
                       'jealous', 'exhausted', 'curious', 'anxious', 'delighted'],
    'ทักทายและมารยาท': ['how are you', 'nice to meet you', 'thank you so much', 'what do you think', 'i appreciate',
                        "i'm sorry", 'excuse me', 'welcome', 'cheers', 'good morning', 'good luck', 'take care',
                        'congratulations', 'see you', 'no problem', "you're welcome", 'please', 'pardon'],
}

# Sets with a Thai explanation card; each item is [phrase, Thai note].
NOTED_SETS = {
    'เสียงเชื่อมแบบเจ้าของภาษา': ('เจ้าของภาษาพูดเร็วจนคำติดกัน คนไทยจึงฟังไม่ทัน ฟังให้ชินกับรูปย่อเหล่านี้ แต่เวลาเขียนงานทางการให้ใช้รูปเต็ม', [
        ['gonna', 'มาจาก going to = กำลังจะ'], ['wanna', 'มาจาก want to = อยากจะ'], ['gotta', 'มาจาก got to / have got to = ต้อง'],
        ['kinda', 'มาจาก kind of = ค่อนข้าง, ประมาณว่า'], ['sorta', 'มาจาก sort of = ประมาณว่า'], ['lemme', 'มาจาก let me = ขอฉัน…'],
        ['gimme', 'มาจาก give me = ให้ฉัน'], ['dunno', "มาจาก don't know = ไม่รู้"], ['ya', 'มาจาก you = คุณ'],
        ['going to', 'ฟังดี ๆ หลายคนพูดเร็วจนเป็น gonna'], ['want to', 'มักพูดเร็วเป็น wanna'], ['have to', 'ออกเสียงเชื่อมเป็น แฮฟทะ'],
        ['a lot of', 'พูดเชื่อมเป็น อะลอทเทิฟ / alotta'], ['out of', 'พูดเชื่อมเป็น เอาเทิฟ / outta'], ['kind of', 'พูดเชื่อมเป็น kinda'],
        ['did you', 'เสียง d + y เชื่อมกันเป็น ดิดจู'], ['would you', 'เสียง d + y เชื่อมกันเป็น วุดจู'], ['what do you', 'พูดเร็วเป็น วัดดะยะ / whaddaya'],
        ['should have', "พูดเร็วเป็น should've (ชุดเดิฟ)"], ['could have', "พูดเร็วเป็น could've"], ["'cause", 'มาจาก because = เพราะ'],
        ["y'all", 'มาจาก you all = พวกคุณ (สำเนียงอเมริกันใต้)'], ['ain\'t', "มาจาก am not / isn't / haven't (ภาษาพูด ไม่เป็นทางการ)"]]),
    'ไวยากรณ์: Present perfect': ('have/has + V3 ใช้เมื่อเรื่องเริ่มในอดีตและยังเกี่ยวกับตอนนี้ หรือเป็นประสบการณ์ ภาษาไทยไม่มีรูปนี้ คนไทยจึงมักใช้ past simple แทน', [
        ['have been', 'เป็น/อยู่มาตลอดจนถึงตอนนี้'], ['has been', 'เป็น/อยู่มาตลอดจนถึงตอนนี้ (ประธานเอกพจน์)'], ['have you ever', 'คุณเคย…ไหม (ถามประสบการณ์)'],
        ["i've never", 'ฉันไม่เคย…เลย'], ['have already', 'ทำไปแล้ว'], ['has already', 'ทำไปแล้ว'], ["haven't", 'ยังไม่ได้…'],
        ['have done', 'ได้ทำไปแล้ว'], ['has changed', 'เปลี่ยนไปแล้ว (และยังเป็นแบบนั้นอยู่)'], ['for years', 'มาหลายปีแล้ว (ใช้คู่กับ present perfect บ่อย)'],
        ['so far', 'จนถึงตอนนี้'], ['just been', 'เพิ่ง…มา']]),
    'ไวยากรณ์: อดีต (used to / was -ing)': ('used to + V1 = เคยทำเป็นประจำในอดีต แต่ตอนนี้ไม่แล้ว · was/were + V-ing = กำลังทำอยู่ ณ ตอนนั้นในอดีต', [
        ['used to', 'เคย…(แต่ตอนนี้ไม่แล้ว)'], ['i used to', 'ฉันเคย…'], ["didn't use to", 'แต่ก่อนไม่เคย…'], ['was going to', 'ตั้งใจว่าจะ…(แต่ไม่ได้ทำ)'],
        ['was trying to', 'กำลังพยายาม…อยู่ตอนนั้น'], ['were talking', 'กำลังคุยกันอยู่ตอนนั้น'], ['was working', 'กำลังทำงานอยู่ตอนนั้น'],
        ['when i was', 'ตอนที่ฉัน…'], ['had been', 'ได้…มาก่อนหน้านั้นแล้ว (past perfect)'], ['had never', 'ไม่เคย…มาก่อนเลย (ก่อนเหตุการณ์ในอดีต)']]),
    'ไวยากรณ์: อนาคต': ('will = ตัดสินใจตอนพูด/คาดการณ์ · be going to = วางแผนไว้แล้ว/มีสัญญาณ · be about to = กำลังจะเกิดในไม่ช้า', [
        ['will be', 'จะเป็น/จะอยู่'], ["i'll", 'ฉันจะ… (มักตัดสินใจตอนพูด)'], ["won't", 'จะไม่…'], ["we're going to", 'พวกเราจะ… (มีแผนแล้ว)'],
        ['is going to', 'จะ… (มีแผน/มีสัญญาณ)'], ['about to', 'กำลังจะ…ในไม่ช้า'], ['will have', 'จะได้…แล้ว (future perfect)'],
        ['in the future', 'ในอนาคต'], ['next year', 'ปีหน้า'], ['is likely to', 'มีแนวโน้มว่าจะ…']]),
    'ไวยากรณ์: ประโยคเงื่อนไข (If)': ('If + present, will = เป็นไปได้จริง · If + past, would = สมมติตอนนี้ (if I were…) · If + had V3, would have = สมมติอดีตที่ไม่ได้เกิด', [
        ['if you want', 'ถ้าคุณต้องการ… (เป็นไปได้จริง)'], ['if i were', 'ถ้าฉันเป็น… (สมมติ ใช้ were กับทุกประธาน)'], ['if i had', 'ถ้าฉันมี/ถ้าฉันได้…'],
        ['would have', 'คงจะ…ไปแล้ว (สมมติอดีต)'], ['would be', 'คงจะเป็น… (สมมติ)'], ['i would', 'ฉันคงจะ…'], ['unless', 'ถ้าไม่…, เว้นแต่'],
        ['as long as', 'ตราบใดที่'], ['what if', 'ถ้าเกิดว่า…ล่ะ'], ['even if', 'ถึงแม้ว่า…ก็ตาม (สมมติ)'], ['in case', 'เผื่อว่า']]),
    'ไวยากรณ์: Modal + have (คาดเดาอดีต)': ('should have = ควรจะ…(แต่ไม่ได้ทำ) · could have = อาจจะ…ได้ · must have = ต้อง…แน่ ๆ · might have = อาจจะ…', [
        ['should have', 'ควรจะ…(แต่ไม่ได้ทำ) — เสียดาย/ติ'], ["shouldn't have", 'ไม่น่า…เลย'], ['could have', 'อาจจะ…ได้ (แต่ไม่ได้ทำ)'],
        ['must have', 'ต้อง…แน่ ๆ (มั่นใจ)'], ['might have', 'อาจจะ…ก็ได้ (ไม่แน่ใจ)'], ["can't have", 'ไม่มีทางที่จะ…'], ['would have been', 'คงจะเป็น…ไปแล้ว']]),
    'ไวยากรณ์: Passive (ถูกกระทำ)': ('be + V3 ใช้เมื่อสนใจผู้ถูกกระทำมากกว่าผู้ทำ ภาษาไทยใช้ "ถูก/โดน" น้อยกว่า คนไทยจึงมักลืมใช้ passive', [
        ['was born', 'เกิด (ใช้ passive เสมอ)'], ['was told', 'ถูกบอกว่า / ได้รับแจ้งว่า'], ['were told', 'ถูกบอกว่า (พหูพจน์)'], ['been told', 'ได้รับแจ้งมาแล้ว'],
        ['was made', 'ถูกทำขึ้น'], ['is called', 'ถูกเรียกว่า / ชื่อว่า'], ['was called', 'ถูกเรียกว่า / ชื่อว่า (อดีต)'], ['is used', 'ถูกใช้'],
        ['were killed', 'ถูกฆ่า/เสียชีวิต (พบบ่อยในข่าว)'], ['was arrested', 'ถูกจับกุม (ข่าว)'], ['is expected to', 'คาดว่าจะ… (ข่าว)'], ['being', 'กำลังถูก… (is being + V3)']]),
}


tok = lambda t: re.findall(r"[a-z]+(?:'[a-z]+)?", t.lower().replace('’', "'"))
STOP = set('that this with have from they what there were their about would could should which them then than when been your just like know think really going people because those these other into some very also only'.split())

def read_js(path, prefix_re):
    if not os.path.exists(path): return None
    txt = open(path, encoding='utf-8').read()
    return json.loads(re.sub(prefix_re, '', txt, count=1).rstrip().rstrip(';'))

PART_RE = r'^\(window\.CORPUS_PARTS=window\.CORPUS_PARTS\|\|\{\}\)\[\d+\]='

def load_docs(root):
    """Every published clip as {id, t, ch, cat, acc, cap, dur, wpm, level, s}, removed clips left out. Reads format 1 and 2."""
    man = read_js(os.path.join(root, 'data.js'), r'^window\.CORPUS=')
    if not man: return {}
    docs = {}
    if man.get('fmt') == 2:
        removed = set(man.get('removed') or [])
        for fn, *_ in man['parts']:
            part = read_js(os.path.join(root, fn), PART_RE)
            by = collections.defaultdict(list)
            for vi, st, du, tx in part['s']: by[vi].append([st, du, tx])
            for vi, v in enumerate(part['v']):
                if v[0] in removed: continue
                docs[v[0]] = {'id': v[0], 't': v[1], 'ch': v[2], 'cat': v[3], 'acc': v[4], 'cap': v[5], 'dur': v[6], 'wpm': v[7], 'level': v[8], 's': by[vi]}
        return docs
    lines = list(man.get('s') or [])
    for i, (fn, _) in enumerate(man.get('parts') or []):
        lines += read_js(os.path.join(root, fn), PART_RE) or []
    by = collections.defaultdict(list)
    for vi, st, du, tx in lines: by[vi].append([st, du, tx])
    for vi, v in enumerate(man['v']):
        docs[v[0]] = {'id': v[0], 't': v[1], 'ch': v[2], 'cat': v[3], 'acc': v[4], 'cap': v[5], 'dur': v[6], 'wpm': v[7], 'level': v[8], 's': by[vi]}
    return docs

def speech(d):
    return [[st, du, re.sub(r'\s+', ' ', tx)] for st, du, tx in d['s'] if tx and not re.fullmatch(r'\[.*\]|\(.*\)|♪.*', tx)]

def wpm_of(s):
    words = sum(len(x[2].split()) for x in s)
    return round(words / max(1.0, (s[-1][0] + s[-1][1]) - s[0][0]) * 60)

def score(s, wpm, top):
    ws = [w for x in s for w in tok(x[2])] or ['a']
    return sum(1 for w in ws if w not in top) / len(ws) * 100 + (wpm - 150) / 6

def level_of(sc, cuts):
    for c, l in zip(cuts, ['A2', 'B1', 'B2']):
        if sc < c: return l
    return 'C1'

def phrase_re(phrase):
    body = re.escape(phrase).replace("'", "['’]").replace(r'\ ', r'[\s,.\-–—]+')
    return re.compile(r"(^|[^a-z0-9'’])" + body + r"(?=$|[^a-z0-9'’])", re.I)

def count_in(phrase, lines):
    rx = phrase_re(phrase)
    return sum(1 for t in lines if rx.search(t))

def set_counts(lines):
    """Counts for every set item (kept with low counts too, so later appends can add to them)."""
    out = {}
    for name, items in SETS.items():
        out[name] = {'d': '', 'w': [[w, count_in(w, lines), ''] for w in items]}
    for name, (desc, items) in NOTED_SETS.items():
        out[name] = {'d': desc, 'w': [[w, count_in(w, lines), note] for w, note in items]}
    return out

def chunk(rows):
    parts, cur, n = [], [], 0
    for r in rows:
        cur.append(r); n += len(r[1])
        if n >= PART_LINES: parts.append(cur); cur, n = [], 0
    if cur: parts.append(cur)
    return parts

def write_part(root, n, rows):
    fn = 'data-p%04d.js' % n
    v, s = [], []
    for i, (vrow, lines) in enumerate(rows):
        v.append(vrow); s += [[i, st, du, tx] for st, du, tx in lines]
    with open(os.path.join(root, fn), 'w', encoding='utf-8') as o:
        o.write('(window.CORPUS_PARTS=window.CORPUS_PARTS||{})[' + str(n) + ']=')
        json.dump({'v': v, 's': s}, o, ensure_ascii=False, separators=(',', ':')); o.write(';\n')
    return [fn, len(v), len(s)]

def part_tokens(rows):
    return {w for _, lines in rows for x in lines for w in tok(x[2])}

def write_index(root, where, nparts):
    shards = collections.defaultdict(dict)
    for w, ps in where.items():
        key = w[0] if 'a' <= w[0] <= 'z' else '_'
        shards[key][w] = 0 if len(ps) > COMMON * nparts and nparts > 4 else sorted(ps)
    for old in glob.glob(os.path.join(root, 'data-i-*.js')): os.remove(old)
    for key, m in shards.items():
        with open(os.path.join(root, 'data-i-' + key + '.js'), 'w', encoding='utf-8') as o:
            o.write('(window.CORPUS_IDX=window.CORPUS_IDX||{})[' + json.dumps(key) + ']=')
            json.dump(m, o, ensure_ascii=False, separators=(',', ':')); o.write(';\n')

def read_index(root):
    where = {}
    for f in glob.glob(os.path.join(root, 'data-i-*.js')):
        for w, ps in read_js(f, r'^\(window\.CORPUS_IDX=window\.CORPUS_IDX\|\|\{\}\)\[[^\]]*\]=').items():
            where[w] = ps
    return where

def write_manifest(root, man):
    with open(os.path.join(root, 'data.js'), 'w', encoding='utf-8') as o:
        o.write('window.CORPUS=')
        json.dump(man, o, ensure_ascii=False, separators=(',', ':')); o.write(';\n')

def full(root, docs):
    """Rebuild everything from a list of clip records."""
    docs = sorted(docs, key=lambda d: (d['cap'] != 'm', FIRST.get(d['cat'], 2), d['id']))
    rows = []
    for d in docs:
        s = speech(d)
        if len(s) < 5: continue
        rows.append(([d['id'], d['t'], d['ch'], d['cat'], d['acc'], d['cap'], int(round(d['dur'] or 0)), wpm_of(s)], s))
    lines = [x[2] for _, s in rows for x in s]
    freq = collections.Counter(w for t in lines for w in tok(t))
    ranked = [w for w, _ in freq.most_common()]
    top = set(ranked[:2500]); rank = {w: i for i, w in enumerate(ranked)}
    scores = sorted(score(s, v[7], top) for v, s in rows)
    cuts = [scores[int(f * (len(scores) - 1))] for f in (0.10, 0.35, 0.70)] if scores else [0, 0, 0]
    for v, s in rows: v.append(level_of(score(s, v[7], top), cuts))
    lower = collections.Counter(w for t in lines for w in re.findall(r"(?<![.!?]\s)\b[a-z]+\b", t))
    quiz = sorted(w for w, n in freq.items() if 300 <= rank[w] <= 6000 and n >= 4 and len(w) >= 4 and w.isalpha()
                  and w not in STOP and lower[w] >= 0.8 * n)
    for old in glob.glob(os.path.join(root, 'data-*.js')): os.remove(old)
    parts, where = [], collections.defaultdict(set)
    for n, prow in enumerate(chunk(rows), 1):
        parts.append(write_part(root, n, prow))
        for w in part_tokens(prow): where[w].add(n)
    write_index(root, where, len(parts))
    accs = collections.Counter(v[4] for v, _ in rows)
    man = {'fmt': 2, 'parts': parts, 'clips': len(rows), 'lines': len(lines), 'accs': accs, 'sets': set_counts(lines),
           'quiz': quiz, 'top': sorted(top), 'cuts': cuts, 'removed': []}
    write_manifest(root, man)
    print(len(rows), 'clips', len(lines), 'lines in', len(parts), 'parts |', len(where), 'index words |',
          sum(os.path.getsize(os.path.join(root, p[0])) for p in parts) // 1024, 'KB |', collections.Counter(v[8] for v, _ in rows))

def append(root, new_docs, removed_ids=()):
    """Add new clips as new parts and list removed clips; published parts stay as they are."""
    man = read_js(os.path.join(root, 'data.js'), r'^window\.CORPUS=')
    if not man or man.get('fmt') != 2:
        docs = load_docs(root); docs.update({d['id']: d for d in new_docs})
        for r in removed_ids: docs.pop(r, None)
        return full(root, list(docs.values()))
    top, cuts = set(man['top']), man['cuts']
    rows = []
    for d in sorted(new_docs, key=lambda d: (d['cap'] != 'm', FIRST.get(d['cat'], 2), d['id'])):
        s = speech(d)
        if len(s) < 5: continue
        wpm = wpm_of(s)
        rows.append(([d['id'], d['t'], d['ch'], d['cat'], d['acc'], d['cap'], int(round(d['dur'] or 0)), wpm, level_of(score(s, wpm, top), cuts)], s))
    published = set()
    for fn, *_ in man['parts']:
        published.update(v[0] for v in read_js(os.path.join(root, fn), PART_RE)['v'])
    removed = set(man.get('removed') or []) | (set(removed_ids) & published)
    where = {w: set(ps) if ps else None for w, ps in read_index(root).items()}
    first = len(man['parts']) + 1
    for n, prow in enumerate(chunk(rows), first):
        man['parts'].append(write_part(root, n, prow))
        for w in part_tokens(prow):
            if w not in where: where[w] = set()
            if where[w] is not None: where[w].add(n)
    nparts = len(man['parts'])
    # tokens already marked "in most parts" (None) stay that way; give them every part number so write_index keeps the 0
    write_index(root, {w: (ps if ps is not None else set(range(1, nparts + 1))) for w, ps in where.items()}, nparts)
    new_lines = [x[2] for _, s in rows for x in s]
    for name, st in man['sets'].items():
        for item in st['w']: item[1] += count_in(item[0], new_lines)
    man['removed'] = sorted(removed)
    accs = collections.Counter(man['accs']); accs.update(v[4] for v, _ in rows)
    man['accs'] = accs
    man['clips'] = man['clips'] + len(rows); man['lines'] = man['lines'] + len(new_lines)
    write_manifest(root, man)
    print('appended', len(rows), 'clips in', nparts - first + 1, 'new parts | removed', len(removed), '| total', man['clips'] - len(removed), 'clips')

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    full(os.path.dirname(os.path.abspath(dst)), [json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(src, '*.json'))])
