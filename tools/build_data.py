# Build data.js for the site from collected caption files.
import json, glob, os, sys, re, collections
src, dst = sys.argv[1], sys.argv[2]

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

vids, segs = [], []
for f in sorted(glob.glob(os.path.join(src, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    s = [x for x in d['s'] if x[2] and not re.fullmatch(r'\[.*\]|\(.*\)|♪.*', x[2])]
    if len(s) < 5: continue
    words = sum(len(x[2].split()) for x in s)
    span = max(1.0, (s[-1][0] + s[-1][1]) - s[0][0])
    wpm = round(words / span * 60)
    vi = len(vids)
    vids.append([d['id'], d['t'], d['ch'], d['cat'], d['acc'], d['cap'], round(d['dur']), wpm])
    for st, du, tx in s:
        segs.append([vi, st, du, re.sub(r'\s+', ' ', tx)])

# Word frequency across the whole corpus, used for level estimates and quiz word choice.
tok = lambda t: re.findall(r"[a-z]+(?:'[a-z]+)?", t.lower().replace('’', "'"))
freq = collections.Counter(w for s in segs for w in tok(s[3]))
rank = {w: i for i, (w, _) in enumerate(freq.most_common())}

# Level estimate per clip: share of less common words plus speaking speed, split by percentile.
per = collections.defaultdict(list)
for s in segs: per[s[0]].extend(tok(s[3]))
score = []
for vi, v in enumerate(vids):
    ws = per[vi] or ['a']
    rare = sum(1 for w in ws if rank.get(w, 99999) > 2500) / len(ws)
    score.append(rare * 100 + (v[7] - 150) / 6)
order = sorted(range(len(vids)), key=lambda i: score[i])
cuts = [(0.10, 'A2'), (0.35, 'B1'), (0.70, 'B2'), (1.01, 'C1')]
for pos, vi in enumerate(order):
    frac = pos / max(1, len(order))
    vids[vi].append(next(l for c, l in cuts if frac < c))

# Topic word sets: keep only items heard in at least 3 lines.
def count(phrase):
    body = re.escape(phrase).replace("'", "['’]").replace(r'\ ', r'[\s,.\-–—]+')
    rx = re.compile(r"(^|[^a-z0-9'’])" + body + r"(?=$|[^a-z0-9'’])", re.I)
    return sum(1 for s in segs if rx.search(s[3]))
sets = {}
for name, items in SETS.items():
    kept = [[w, n, ''] for w in items if (n := count(w)) >= 3]
    if kept: sets[name] = {'d': '', 'w': kept}
for name, (desc, items) in NOTED_SETS.items():
    kept = [[w, n, note] for w, note in items if (n := count(w)) >= 2]
    if kept: sets[name] = {'d': desc, 'w': kept}

# Quiz candidates: mid-frequency content words (not the commonest few hundred, not one-offs).
STOP = set('that this with have from they what there were their about would could should which them then than when been your just like know think really going people because those these other into some very also only'.split())
# Skip names and places: words that are mostly written with a capital letter mid-sentence.
lower = collections.Counter(w for s in segs for w in re.findall(r"(?<![.!?]\s)\b[a-z]+\b", s[3]))
quiz = sorted(w for w, n in freq.items() if 300 <= rank[w] <= 6000 and n >= 4 and len(w) >= 4 and w.isalpha()
              and w not in STOP and lower[w] >= 0.8 * n)

with open(dst, 'w', encoding='utf-8') as o:
    o.write('window.CORPUS=')
    json.dump({'v': vids, 's': segs, 'sets': sets, 'quiz': quiz}, o, ensure_ascii=False, separators=(',', ':'))
    o.write(';\n')
print(len(vids), 'videos', len(segs), 'lines', os.path.getsize(dst) // 1024, 'KB',
      '| levels', collections.Counter(v[8] for v in vids), '| sets', {k: len(v['w']) for k, v in sets.items()}, '| quiz words', len(quiz))
