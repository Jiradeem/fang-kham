# ฟังคำจริง (fang-kham)

A YouGlish-style listening site for Thai learners of English: search a word or phrase (in English or Thai) and hear it in real YouTube clips from official channels, with accents, levels and practice tools.

- Live site: https://jiradeem.github.io/fang-kham/ (GitHub Pages, branch `main`, folder `/`)
- Owner: an English teacher in Thailand who uses it for self-study and with students from A1 to C1. Talk to the owner in Thai, plainly; they are not a programmer.
- Pushing to `main` updates the live site within 1–2 minutes. No build step on GitHub; `data.js` is committed.

## Start here (handoff for the next session)
Status on 2026-10-23: 1,221 general clips (268,016 lines) from 60+ official channels, 2,554 Dhamma clips (119 with searchable captions), two weekly GitHub Actions workflows set up; the general one was tried once and YouTube blocked GitHub (see item 1).

About the owner (follow these):
- English teacher (not a researcher, not a nursing teacher for this project). Their own site is https://dreamenglishlearning.com (on Netlify; its code is not in this repo). Contact on the site: LINE @154yrgoe and dreamenglishlearningthai@gmail.com (already in the About box).
- Keep the name "ฟังคำจริง". The owner asked twice about renaming and cancelled both times: do not rename.
- When the owner is discussing or asking "should we…?", explain and recommend, then wait for "ทำ / ปรับ / ก / ข …" before changing anything. Answer in Thai, short, with a recommendation.
- Before every push: test with Playwright through `python3 -m http.server` (desktop 1366, phone 390, light and dark), then tell the owner what changed in plain Thai.
- Gratitude to Ajahn Sujin: the gold card on the Dhamma page, the gold card in the About box, and a gold line under the player while a Dhamma clip plays (owner's choice "ข"). Name spelling: ท่านอาจารย์สุจินต์ บริหารวนเขตต์.

Waiting for the owner:
1. **Result of the first GitHub run (2026-10-23, run 39971839183): YouTube blocked GitHub's runner within 10 seconds** (the PROBE clip had no caption tracks). So the weekly workflows will most likely add nothing; they stop safely and change no data. Clips must be collected from a Claude Code session (works; ~450 clips per 2-hour background command) or from the owner's home computer. Options were being discussed with the owner; nothing decided yet. Do not schedule 4 runs a day on GitHub.
   **Decision (owner chose "ข"): collect on the owner's Windows 11 computer every night.** `tools/windows/setup.bat` (one-time: installs Git, Python 3.12, Node LTS with winget; clones to `%USERPROFILE%\fang-kham`; venv with yt-dlp + yt-dlp-ejs; GitHub sign-in through Git Credential Manager; registers the Task Scheduler job "fang-kham clips" daily 23:00 with WakeToRun/StartWhenAvailable). `tools/windows/run.bat` → `tools/home_run.py`: sync to origin/main, `update_corpus.py --save-dir home-clips --limit 600 --minutes 420 --per-channel 15 --depth 120 --wait-when-blocked 20`, sync again, `--merge-dir home-clips`, `count_lessons.js`, commit, push (retries; clips stay in `home-clips/` until a push succeeds). The job resets the clone to origin/main at the start, so pushing script changes to `main` updates the home computer automatically. Log: `%USERPROFILE%\fang-kham\collect.log`. Installed on the owner's PC (user `Lenovo`) on 2026-10-24; the first run started 10:57 Thai time. `run.bat` relaunches itself with `conhost.exe --headless` so no window appears (the owner asked for it to run fully in the background); if nightly runs ever stop appearing in `collect.log`, check that first. Collecting stops when the corpus reaches `--max` (now 30,000).
2. Add a "ฟังคำจริง" link on the main site (menu "คลังสื่อ", function `mediaDropdown()`): a prepared copy of the main site's index.html was made in the previous session but is not in this repo; the owner may do it with their own tools.
3. Visitor counter (GoatCounter) needs a code from the owner's sign-up; permission e-mail to the Baan Dhamma foundation was offered, not written.

Agreed plan for growing the corpus (the owner asked for "as many clips as possible, as fast as possible", without paying):
- Step 1: daily runs (see above). Also add more TED / TED-Ed clips (licence CC BY-NC-ND, hand-made captions); 262 TED/TED-Ed talks were added on 2026-10-23 (150 per channel collected; TED now ~170, TED-Ed ~170).
- Step 2 (done 2026-10-24, instead of Cloudflare): parts load only when a search needs them (format 2 above). The cap is now 30,000 clips (`--max`).
- Step 3 (Cloudflare Workers + D1) was replaced by step 2: the owner asked for more than 3,000 clips, and on-demand parts give that with no account, token or server. Revisit a server only if the repository gets close to 1 GB (about 50,000+ clips) or searches for common phrases load too many parts on phones.
- Do not use proxies or IP rotation to get around YouTube limits. The YouTube Data API cannot download other channels' captions.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app: markup, CSS tokens (light and dark), and one inline script. No framework. |
| `data.js`, `data-1.js` … `data-N.js` | The general corpus (format below), generated by `tools/build_data.py`. Do not edit by hand. |
| `thai.js` | `THAI_EN` (Thai word or phrase → English options, ~218 entries), `THAI_WORD_TIPS` and `thaiTips()` (pronunciation warnings for Thai speakers). Edit by hand. |
| `curriculum.js` | Two tables of contents: `book` = the owner's speaking course "คิดเป็นไทย พูดเป็นอังกฤษ" (volumes 1–3, 115 lessons) and `grammar` = the owner's A1–A2 grammar syllabus (140 lessons). Each lesson is `[number, Thai title, structure, 'phrase|phrase']`; opening a lesson searches every phrase at once. Edit by hand, then run `node tools/count_lessons.js`. |
| `counts.js` | Lines found per lesson (`course-volumeIndex-lessonNumber`), generated by `tools/count_lessons.js`. |
| `dhamma.js` | `[videoId, title, durationSec, category]` for 2,554 English Dhamma clips of Ajahn Sujin: all of @IntlDhammaDiscussions (streams + videos), "Studying Dhamma with Ajahn Sujin" (UC0gJW7nCHv_4Sv1CF0UTwWQ) and the English/Hindi playlists of the Thai foundation channel; the Alan Weller channel was left out because its videos do not say they are Ajahn Sujin's. From the official channel @IntlDhammaDiscussions (Baan Dhamma / มูลนิธิศึกษาและเผยแพร่พระพุทธศาสนา, dhammahome.com/en). Shown in the "ฟังธรรมะ" tab with a plain YouTube embed; not part of the word corpus. |
| `dhamma-shards.js`, `dhamma-corpus-<key>.js` | The Dhamma corpus, split so the browser fetches only what the learner selects (`#shardBar`): `short` = "Studying Dhamma with Ajahn Sujin" excerpts (manual English captions), then long discussions by year in chunks of 60 talks. Rows have the same shape as `CORPUS`; selected shards are merged into `window.DHAMMA_CORPUS` and the search view switches `C` to it (`useCorpus`). Built by `tools/build_dhamma.py <caption dir> .` from captions fetched by `tools/collect_dhamma_captions.py tools/dhamma-queue.json` (2,554 clips in priority order; it skips files that already exist, so it can be resumed in any session). |
| `dhamma-glossary-core.js` | `DHAMMA_CORE`: ~70 key terms `[term, Thai, gloss, 'variants']`. Variants include the misspellings YouTube auto captions really produce (citta → jitta, rupa → ruper, kusala → kusula); check new ones by counting tokens in the captions. |
| `dhamma-glossary.js` | `DHAMMA_GLOSSARY`: 461 `[term, definition]` pairs parsed from dhammahome.com's Glossary of Pali Terms (article-en topics 124–148). |
| `tools/collect_captions.py` | Collects caption files from the channels listed in a TSV into `<TSV folder>/videos/<id>.json` (pauses when YouTube rate-limits). |
| `tools/build_data.py` | Turns a folder of caption files into `data.js` + `data-*.js`; also holds the topic and grammar word sets with Thai notes. |
| `tools/update_corpus.py` | Weekly job: rebuilds records from the published files, adds new suitable clips, filters, rebuilds. Its `load_records()`, `UNSUITABLE` and `suitable()` are reused when merging a manual collection. |
| `tools/channels.tsv` | `handle<TAB>category<TAB>accent` for every channel used (89). |
| `tools/corpus-skip.json` | Clip ids never to add again (unsuitable, no captions, or removed on request). |
| `img/owl-192.png` | Dreamy Owl logo from the owner's main site. |

### `data.js` format (format 2, since 2026-10-24)
- `data.js` = `window.CORPUS = {fmt: 2, parts: [[file, clips, lines], …], clips, lines, accs, sets, quiz, top, cuts, removed}` (about 80 KB).
- `data-pNNNN.js` = one part of about 20,000 lines (~1 MB): `{v: [clip rows], s: [[clipIndexInPart, start, dur, text], …]}`. **Parts are append-only**: `build_data.append()` writes new clips into new parts and never rewrites published ones, so nightly commits stay small. Removed clips are listed in `removed` and skipped by the page.
- `data-i-X.js` = word index by first letter: `{token: [part numbers]}` or `0` when the token is in more than half of the parts.
- The page loads part 1 at once (hand-made captions and the learning/kids channels sort first). A search looks up its words in the index, loads the parts that hold them three at a time, best parts first, until it has about 80 clips, then shows "ค้นเพิ่มในคลัง (อีก N ชุด)". Loaded parts join `MAIN`, so the open clip never restarts. Stats show the totals from `data.js`.
- `sets` keeps every item with its count (low counts too, so appends can add to them); the page shows items heard at least 3 times (2 for sets with a Thai note). `top` (2,500 commonest words) and `cuts` fix the level of new clips without re-levelling old ones. A full rebuild (`python3 -I tools/build_data.py <caption dir> data.js`) recomputes everything and renumbers the parts; avoid it unless needed, it rewrites every part.
- `counts.js` also stores `LESSON_PARTS` and `LESSON_KEY`; `count_lessons.js` only reads parts added since, unless the curriculum changed or `--full` is given.
- `v[i] = [videoId, title, channel, category, accent, captionKind('m' manual | 'a' auto), durationSec, wordsPerMinute, level]`
- `s[j] = [videoIndex, startSec, durSec, text]`, sorted by video then time.
- `sets[name] = {d: Thai description, w: [[phrase, lineCount, Thai note], ...]}`
- `quiz` = mid-frequency lowercase words used for the fill-in-the-blank quiz.
- Categories: movie, series, tv, interview, documentary, ted, news, conversation, learning (BBC Learning English…), kids (Sesame Street, Peppa Pig, Bluey…). Accents: US, UK, AUS, CAN, IRL, SCO, NZ (assigned by the channel's country, not per speaker).
- Level (A2–C1) is an estimate from speaking speed and the share of less common words, split by percentile. Native media has almost no A1 material; the site says so.

## Features in `index.html`
Search (English regex with word boundaries; Thai via `THAI_EN`, then free machine translation as fallback), filters (accent, category, speed, level), YouTube IFrame player that jumps to the line, subtitle strip with prev/next lines, approximate word-by-word highlight, Thai translation of the current line, controls and keyboard shortcuts (N P R B K L H T S), dictionary panel (dictionaryapi.dev, Wiktionary fallback) with "จุดที่คนไทยมักพลาด" tips, practice tabs (speak along with scoring via Web Speech API, continuous shadowing, dictation, write your own sentence, fill-in-the-blank quiz, minimal-pairs game), word sets, nearby words, notebook with spaced review (1·3·7·14·30 days), daily goal with streak. Learning system: a "แนะนำในคลิปนี้" guide per clip (sentences worth learning, connectors, Dhamma terms, useful words, each with a ☆ save), a notebook with filters and CSV export, spaced review (1·3·7·14·30 days) whose word cards change form with the box (choose the Thai meaning → fill the gap from the clip → produce the English from Thai), lesson progress ticks and bars in both courses, a Dhamma word of the day, "lessons from the latest discussions", and backup/restore of all `fk.*` localStorage keys as a JSON file to move between devices (notes are merged). Notebook, stats and review live in `localStorage` per browser; there is no server or login.

## Automatic general-clip updates
`.github/workflows/update-corpus.yml` runs `tools/update_corpus.py` every Wednesday 03:23 UTC (and by hand from the Actions tab). It rebuilds the clip records from the published `data.js` + `data-*.js`, lists the newest clips of the channels in `tools/channels.tsv` (accents and categories with the fewest clips first, at most 3 per channel, 80 per run), keeps only classroom-suitable clips (1–20 min, embeddable, not age-restricted, no violent/adult words in the title, at most 2 bleeped lines, mostly speech, English captions with hand-made ones preferred), keeps the corpus under 3,000 clips by dropping auto-captioned clips from the biggest groups (fastest speech first), rebuilds `data.js` and recounts lessons. Rejected clips go to `tools/corpus-skip.json`; adding a clip id there by hand also removes it from the corpus on the next run.
Teachers can hide an unsuitable clip with "🚫 ซ่อนคลิปนี้" under the player (per browser, `fk.hidden`); "คัดลอกรายการเพื่อส่งผู้ดูแล" in the filter box copies the ids to send to the owner, who adds them to `tools/corpus-skip.json`.

## Automatic Dhamma updates
`.github/workflows/update-dhamma.yml` runs `tools/update_dhamma.py` once a week on Tuesday 03:17 UTC (the owner asked for weekly checks), after the discussions are held on Saturday (International, India), Sunday (Chinese–English, Vietnamese–English) and Monday (English); it can also be started by hand from the Actions tab. Each run lists the newest clips of the two verified Ajahn Sujin channels, adds them to `dhamma.js`, fetches captions for up to 400 clips within 5 hours (short clips and English talks first), rebuilds the shards from the published shard files and commits.

Only clips where English is really spoken are kept: hand-made English captions, or YouTube speech recognition in English (`en-orig`). A plain `en` caption track alone is a machine translation; many "สตรีมแบบสดของ dhamma home" streams are Thai (`th-orig`). Rejected ids go to `tools/dhamma-skip.json` and disappear from `dhamma.js`. Streams whose title says nothing are listed as "ไลฟ์ (ยังไม่ตรวจภาษา)" until checked. The Alan Weller channel is not included (its videos do not say they are Ajahn Sujin's).

No raw caption files are stored; the shards are the source. If YouTube blocks GitHub's runners the log says "blocked by YouTube" and the run stops; then run the same script from a Claude Code session (`--caps-dir` merges captions collected elsewhere).

## Rebuilding or extending the corpus
The published `data.js` + `data-*.js` are the source; no raw caption files are kept (the old `corpus-videos.tgz` was removed). To add clips from a Claude Code session (Network access: Full):

```bash
python3 -m venv .venv && .venv/bin/pip install yt-dlp yt-dlp-ejs
mkdir -p work && printf '@TED\tted\tUS\n' > work/channels.tsv       # handle, category, accent
.venv/bin/python -I tools/collect_captions.py work/channels.tsv 100 .venv/bin/yt-dlp   # writes work/videos/<id>.json; run it in the background (2-hour limit per command)
```
Then merge with the published corpus, apply the classroom filters and rebuild (this is what the previous session did):
```python
import sys, json, glob; sys.path.insert(0, 'tools'); import update_corpus as u
recs = u.load_records()                                   # published clips
for f in glob.glob('work/videos/*.json'): d = json.load(open(f)); recs[d['id']] = d
skip = set(json.load(open('tools/corpus-skip.json')))
# drop: id in skip, u.UNSUITABLE.search(title), or u.suitable(segs) in ('mostly music', 'bleeped words'); add dropped ids to skip
# write the kept records to a folder, then: python3 -I tools/build_data.py <folder> data.js && node tools/count_lessons.js
```
Always `git fetch origin main && git reset --hard FETCH_HEAD` in a clean clone before copying files in, because the workflows commit to `main` too.

What we learned while collecting:
- From cloud IPs, YouTube answers normal requests with "Sign in to confirm you're not a bot". `yt-dlp` with `--extractor-args youtube:player_client=web_embedded --ignore-no-formats-error` still works, and it only returns videos whose owners allow embedding, which is exactly what the site needs. `youtube-transcript-api` was blocked.
- Caption files are fetched as `json3`; manual English captions are preferred, auto captions are the fallback.
- Channels that gave nothing (embedding disabled or no captions): @1NewsNZ, @7NEWS, @BBCThree, @VOALearningEnglish (no caption tracks at all), @TEDxTalks, @TheLateShow, @nbcsnl, @GQ. Few clips: @FallonTonight, @VanityFair, @jubilee, @PeppaPigOfficial (7), @LastWeekTonight (5).
- Of the 54 channels added on 2026-10-23, only the first 24 in the list were collected before time ran out; the weekly job will reach the rest.
- YouTube rate-limits one machine after a few hundred requests (HTTP 429, or clips coming back with no caption tracks). A "429" warning alone is harmless; `collect_captions.py` checks a known clip (PROBE) before pausing. yt-dlp now needs `yt-dlp-ejs` for its JavaScript challenge.
- Classroom filter results on the first big run: 37 clips dropped for titles (murder, drugs, sexual crimes…), 25 mostly music (Sesame Street songs), 7 with many bleeped words. Watch for false positives (a title with "Stablecoins" once matched "stab").
- The free translation services (MyMemory, translate.googleapis.com gtx) refuse cloud IPs but work from a normal home connection.

## Constraints and decisions
- claude.ai Artifacts cannot embed YouTube iframes, so the site is hosted on GitHub Pages instead.
- Opening `index.html` from a local file may stop YouTube from playing; always test through a web server (`python3 -m http.server`).
- No API keys anywhere. Everything external is keyless: YouTube IFrame API, dictionaryapi.dev, Wiktionary REST, MyMemory, gtx.
- Only official channels; clips play through YouTube's player and are never downloaded. For teaching, not for profit.
- Thai transliteration of English words was deliberately left out (it reinforces Thai-accented pronunciation); the tips box explains sounds instead.

## Ideas not done yet
- Finish the channels above and add more movie, sitcom and talk-show sources; balance accents (IRL, SCO, NZ, CAN have few clips).
- Grow `THAI_EN` from words students search for that miss.
- A teacher view of class progress would need a backend; current stats are per browser only.

## Next project: communicative curriculum A1 → C1 (agreed with the owner, not started)
Goal: turn the search tool into a course where every topic starts from what the learner can **say** in real life, then shows the grammar and words it needs, proved by native-speaker clips. Start at A1 and finish each level before the next.

### Topic page (one per topic)
1. Can-do statement in Thai, e.g. "แนะนำตัวเองได้"
2. Thai explanation card: when to use it, the pattern (e.g. `Subject + am/is/are + ...`), and what Thai speakers get wrong
3. Real clips, slow and clear first (manual captions, short complete lines, low words-per-minute)
4. Practice for that topic: speak along with scoring, quiz, dictation, minimal pairs where relevant
5. Progress per topic (localStorage)
The search box stays and also says which topic a word belongs to.

### Sections
1. Communication functions per level (the spine of the course)
2. Grammar, ordered A1 → C1: verb to be, do/does/did, have/has, parts of speech, sentence types (statement, negative, yes/no question, Wh-/How question, imperative, exclamation), modals, 12 tenses, active/passive, conditionals, reported speech, relative clauses, comparatives, gerund/infinitive, articles, prepositions
3. Topic vocabulary with a 👁 "see it" tag: body actions (kneel down, squat, roll over, lie down, breathe in), movement and direction (go in, come out, go through, in front of, behind), daily routines, kitchen, body, feelings
4. Existing sets: connectors, phrasal verbs, expressions, connected speech

### A1 topics to build first (communication → grammar → words)
| # | Can do (Thai) | Grammar | Words / clips |
|---|---|---|---|
| 1 | ทักทาย ลา ขอบคุณ ขอโทษ | set phrases | hello, bye, thanks, sorry, excuse me |
| 2 | แนะนำตัว บอกชื่อ อายุ ประเทศ อาชีพ | verb to be (am/is/are), my/your | I'm, my name is, I'm from |
| 3 | ถาม-ตอบข้อมูลส่วนตัว | Wh- questions with be (what, where, how old) | What's your name? Where are you from? |
| 4 | พูดถึงครอบครัวและคนรอบตัว | have/has got, his/her, plurals | mother, brother, friend |
| 5 | บอกสิ่งที่ชอบ/ไม่ชอบ | present simple + don't/doesn't | like, love, hate, don't like |
| 6 | เล่ากิจวัตรประจำวัน | present simple, adverbs of frequency, time | get up, have breakfast, always, usually |
| 7 | บอกว่าทำอะไรได้/ไม่ได้ | can / can't, yes/no questions | can you swim? |
| 8 | บอกตำแหน่งสิ่งของและสถานที่ | there is/are, prepositions of place | in, on, under, next to, behind, in front of 👁 |
| 9 | ถามทาง บอกทาง | imperatives, directions | turn left, go straight, go through 👁 |
| 10 | สั่งอาหาร ซื้อของ ถามราคา | I'd like, can I have, how much | menu, price, numbers |
| 11 | บอกเวลา วัน เดือน นัดหมาย | numbers, time, prepositions of time | at 7, on Monday, in May |
| 12 | บรรยายคน สิ่งของ ความรู้สึก | adjectives, be + adjective | tall, happy, tired |
| 13 | ทำตามคำสั่งท่าทาง (TPR) | imperatives | stand up, sit down, kneel down, breathe in 👁 |
| 14 | พูดถึงสิ่งที่กำลังทำอยู่ | present continuous | I'm cooking, she's running 👁 |
| 15 | เล่าเรื่องเมื่อวาน (แนะนำ past) | past of be (was/were), common past verbs | yesterday, went, had |

### How to get the clips
- Tag every caption line at build time with spaCy (free, offline): sentence type, tense, passive, modal, question word, imperative. Topic pages then fill themselves. It is accurate but not perfect; say so on the page.
- "See it" 👁 clips must come from instructional channels where speech and action happen together (yoga, fitness, cooking, dance, first aid, DIY, kids' action songs from official channels). Check each channel allows embedding and has English captions (the `web_embedded` client only returns embeddable videos).
- For A1–A2 prefer slow, clear speech: instructional videos, kids' programmes, learner-friendly native content. News and talk shows stay for B2–C1.
- Word lists: use NGSL and NGSL-Spoken (open licence) as the base. Oxford 3000 and English Vocabulary Profile are copyrighted; use them only as a reference, do not copy them into the site. Order topics to match the Thai basic education curriculum (หลักสูตรแกนกลางฯ) where possible.
- Collect for missing words instead of collecting at random: for each target word with fewer than 5 good clips, search for videos likely to contain it.
- `data.js` is split into parts (done). If the corpus grows past ~40 MB, consider loading parts only when a search needs them.
- Collecting: YouTube rate-limits a container after a few hundred requests. `collect_captions.py` checks a known clip (PROBE) before pausing, so channels without captions (e.g. VOA Learning English, whose videos have no caption tracks) are skipped instead of stalling. yt-dlp needs `yt-dlp-ejs` (pip) and `--js-runtimes node` is optional.

### Phases (one new session each)
1. Course page + spaCy tagging + A1 topics 1–15 with clips and practice
2. 👁 "See it" sources and action/direction vocabulary
3. A2 topics, then B1, B2, C1 functions and grammar
4. Fill words with fewer than 5 clips; split the data files

## Design
- Colours follow the main site dreamenglishlearning.com: mint `--brand #00c2a8` / `--accent #0c8c80`, coral `--coral #ff7a59` for primary buttons and the play button, cream `--bg #fbf7ee`, level colours `--lv1..lv5` (A1 green, A2 blue, B1 purple, B2 pink, C1 gold). Headings use Mitr / Fredoka. The gratitude card to Ajahn Sujin keeps its own gold tones.
- `img/owl-192.png` is the Dreamy Owl app icon from the main site (the owner's own brand), used as logo and favicon.
- Clip area works like YouGlish: icon bar under the video, one whole sentence in a large card (`sentence()` joins caption pieces up to sentence ends), context lines on demand. Phones get a bottom tab bar.
