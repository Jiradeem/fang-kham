# ฟังคำจริง (fang-kham)

A YouGlish-style listening site for Thai learners of English: search a word or phrase (in English or Thai) and hear it in real YouTube clips from official channels, with accents, levels and practice tools.

- Live site: https://jiradeem.github.io/fang-kham/ (GitHub Pages, branch `main`, folder `/`)
- Owner: an English teacher in Thailand who uses it for self-study and with students from A1 to C1. Talk to the owner in Thai, plainly; they are not a programmer.
- Pushing to `main` updates the live site within 1–2 minutes. No build step on GitHub; `data.js` is committed.

## Start here (handoff for the next session)
Last updated 2026-10-27.

### Status
- 2026-10-27: a GoatCounter visitor counter is now on every page (`fangkham.goatcounter.com`, one async script
  tag at the end of index.html). It sets no cookie and keeps no personal data, so the site needs no consent
  banner. Nothing was counted before this, so the owner's first real visitor numbers start from this date;
  the free plan keeps 6 months of history. Removing the one script tag turns it off.
- 2026-10-27: the home job is confirmed working — three "Add clips collected on the home computer" commits that day, the last collecting round saving 687 clips with no HTTP 429 and no "blocked by YouTube". Next steps item 1 is therefore done. Added the same day: usage groups above the player (see "Features").
- 2026-10-24 follow-up: the home run published 16 new clips at 17:58 Thai time (1,237 total). A direct diagnostic reproduced HTTP 429 on a caption download. The collector now pauses the whole run on caption HTTP 429, refreshes the same clip's metadata, and retries at most three times (20/40/80 minutes with the nightly settings, or longer if Retry-After requires it). It stops when the remaining collection time is insufficient, preserving already saved clips for the normal merge/publish step. This handles rate limiting; it does not guarantee a nightly clip count. Regression tests: `python -B -I test_rate_limit.py` (7 cases); merge/recount checked with two fixture clips without changing existing parts; browser checks passed at widths 1366 and 390, light and dark.
- General corpus: 4,590 clips (833,979 lines) in 45 parts, format 2 (on-demand parts, see below), cap 30,000. 128 official channels in `tools/channels.tsv`.
- Dhamma: 2,554 clips listed, 119 with searchable captions.
- **Clips are collected every night on the owner's Windows 11 computer** (user `Lenovo`, clone at `C:\Users\Lenovo\fang-kham`), not on GitHub: YouTube blocked GitHub's runner on the first try (run 39971839183). Installed 2026-10-24; first run started 10:57 Thai time.

### What is running
- Since 2026-10-25 the job runs all day: `home_run.py` collects in 3-hour rounds and publishes after each, until 22:30; it adds a logon start to the task (best effort, `add_logon_start`) and a lock file stops overlapping runs. Task Scheduler job "fang-kham clips", daily 23:00 (WakeToRun, StartWhenAvailable) → `tools/windows/run.bat` → relaunches itself with `conhost.exe --headless` (no window; the owner asked for this) → `tools/home_run.py`:
  sync to origin/main → `update_corpus.py --save-dir home-clips --limit 1500 --minutes 420 --per-channel 40 --depth 500 --wait-when-blocked 20` → sync again → `--merge-dir home-clips` (`build_data.append`) → `node tools/count_lessons.js` → commit "Add clips collected on the home computer" → push. Clips stay in `home-clips/` until a push succeeds.
  Because each run resets the clone to origin/main first, **anything pushed to `main` reaches the owner's computer by the next night** (scripts included). Do not break `tools/home_run.py`, `tools/update_corpus.py`, `tools/build_data.py` or `tools/windows/run.bat`: the owner cannot fix them. Test any change to them (see "Testing the nightly job" below).
- Channel order: everyday speech first (films, series, real conversations, cartoons), then teaching, TV, documentaries, then interviews, TED, news (`build_data.TIER`). Search results follow the same order (`clipRank()` in index.html), politics last.
- GitHub Actions `update-corpus.yml` (Wed) and `update-dhamma.yml` (Tue) still exist but YouTube blocks GitHub, so they add nothing; they stop safely. Dhamma clips therefore are not updating; see "Next steps".

### Fix of 2026-10-25 (why the first home nights gave 16 and then 0 clips)
Some caption tracks always answer HTTP 429 while others download fine. Any 429 used to pause the whole night (20+40+80 min) and then stop. Now `captions_with_backoff` first checks the PROBE clip: if it still works, only that clip is skipped (`ClipCaptionDenied`); the night pauses only when the probe fails too. Captions are downloaded by yt-dlp itself (`download_track`, same cookie jar as the lookup) instead of a bare urllib request, with 12 s between clips. `home_run.py` publishes `tools/home-log.txt` (last 400 collector lines) every night, even with no clips: **read it first**. Tests: `python -B -I test_rate_limit.py` (9 cases, written partly by another AI the owner runs on the home computer).

### Check first in a new session
1. `git log --oneline -15` — are there commits "Add clips collected on the home computer" (one per night since 2026-10-24)? If yes, the home job works.
2. `python3 -c "import json,re;m=json.loads(re.sub(r'^window\.CORPUS=','',open('data.js',encoding='utf-8').read()).rstrip().rstrip(';'));print(m['clips'],len(m['parts']))"` — clip count should grow by ~1,000 a night.
3. If there are no nightly commits: ask the owner to open `C:\Users\Lenovo\fang-kham\collect.log` in Notepad and send a photo of the end. Likely causes, in order: `conhost --headless` did not start (no `==== start` line for that night; fall back to a visible window or a .vbs launcher), the computer was off, YouTube blocking (`blocked by YouTube`), GitHub sign-in expired (push errors; rerun `setup.bat`).
4. Open the live site, search a word, check the footer "คลังตอนนี้: … คลิป" and that clips play.

### Next steps (recommended order; ask the owner before starting)
1. ~~**Verify the first nights**~~ — done 2026-10-27, the settings were left as they are. Watch for blocking again later; if YouTube blocks often, lower `--limit`/raise the sleep in `update_corpus.py`.
2. **Dhamma updates from the home computer**: make `home_run.py` also run `tools/update_dhamma.py` (it needs the same save/merge split as the general corpus so it never conflicts), since GitHub cannot reach YouTube.
3. **New learning features the owner liked** (from a survey of PlayPhrase, Language Reactor, LyricsTraining, Voscreen, EnglishCentral, ELSA): (1) "play all clips in a row" for a word, (2) gap-fill dictation with levels 10/25/50/100% and letter-count dots, write or choose mode, (4) Thai translation blurred until hovered/tapped. Later: (3) timed meaning game, (5) Anki/Quizlet export, (6) per-clip lesson with a total score, (7) points.
4. **Watch phone data**: a common phrase may load many 1 MB parts (`ENOUGH = 80`, `BATCH = 3` in index.html). If the corpus passes ~15,000 clips and searches feel slow on phones, split the index by two letters and lower `ENOUGH`.
5. **Communicative curriculum A1 → C1** (agreed earlier, not started; see the section at the end).
6. Small items waiting for the owner: link "ฟังคำจริง" from the main site's menu "คลังสื่อ" (main site is on Netlify, code not here); permission e-mail to the Baan Dhamma foundation (offered, not written); a nicer address such as listen.dreamenglishlearning.com (the owner made a Cloudflare account on 2026-10-24 but it is **not used**; the Cloudflare server plan was replaced by on-demand parts).

### About the owner (follow these)
- English teacher (not a researcher, not a nursing teacher for this project). Their own site is https://dreamenglishlearning.com (on Netlify; its code is not in this repo). Contact on the site: LINE @154yrgoe and dreamenglishlearningthai@gmail.com (already in the About box).
- Keep the name "ฟังคำจริง". The owner asked twice about renaming and cancelled both times: do not rename.
- When the owner is discussing or asking "should we…?", explain and recommend, then wait for "ทำ / ปรับ / ก / ข …" before changing anything. Answer in Thai, short, with a recommendation. The owner works from Windows screenshots; give click-by-click steps.
- Before every push: test with Playwright through `python3 -m http.server` (desktop 1366, phone 390, light and dark), then tell the owner what changed in plain Thai.
- Claude credits are limited on the owner's plan: suggest a new session for big work, keep answers short.
- Gratitude to Ajahn Sujin: the gold card on the Dhamma page, the gold card in the About box, and a gold line under the player while a Dhamma clip plays (owner's choice "ข"). Name spelling: ท่านอาจารย์สุจินต์ บริหารวนเขตต์.
- Do not use proxies or IP rotation to get around YouTube limits. The YouTube Data API cannot download other channels' captions.

### Testing the nightly job
Clone the repo into a temp folder, put two caption files in `home-clips/`, run `python3 -X utf8 -I tools/update_corpus.py --merge-dir home-clips` and `node tools/count_lessons.js`; a new `data-pNNNN.js` must appear and no existing part may change. For the whole flow, clone a bare copy as "origin" and run `tools/home_run.py git node` with a small `--limit`/`--minutes` (the previous session did this; it published to the stand-in origin correctly).

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app: markup, CSS tokens (light and dark), and one inline script. No framework. |
| `data.js`, `data-pNNNN.js`, `data-i-X.js` | The general corpus: manifest, append-only parts, word index (format below), generated by `tools/build_data.py`. Do not edit by hand. |
| `thai.js` | `THAI_EN` (Thai word or phrase → English options, ~218 entries), `THAI_WORD_TIPS` and `thaiTips()` (pronunciation warnings for Thai speakers). Edit by hand. |
| `curriculum.js` | Two tables of contents: `book` = the owner's speaking course "คิดเป็นไทย พูดเป็นอังกฤษ" (volumes 1–3, 115 lessons) and `grammar` = the owner's A1–A2 grammar syllabus (140 lessons). Each lesson is `[number, Thai title, structure, 'phrase|phrase']`; opening a lesson searches every phrase at once. Edit by hand, then run `node tools/count_lessons.js`. |
| `counts.js` | Lines found per lesson (`course-volumeIndex-lessonNumber`), generated by `tools/count_lessons.js`. |
| `dhamma.js` | `[videoId, title, durationSec, category]` for 2,554 English Dhamma clips of Ajahn Sujin: all of @IntlDhammaDiscussions (streams + videos), "Studying Dhamma with Ajahn Sujin" (UC0gJW7nCHv_4Sv1CF0UTwWQ) and the English/Hindi playlists of the Thai foundation channel; the Alan Weller channel was left out because its videos do not say they are Ajahn Sujin's. From the official channel @IntlDhammaDiscussions (Baan Dhamma / มูลนิธิศึกษาและเผยแพร่พระพุทธศาสนา, dhammahome.com/en). Shown in the "ฟังธรรมะ" tab with a plain YouTube embed; not part of the word corpus. |
| `dhamma-shards.js`, `dhamma-corpus-<key>.js` | The Dhamma corpus, split so the browser fetches only what the learner selects (`#shardBar`): `short` = "Studying Dhamma with Ajahn Sujin" excerpts (manual English captions), then long discussions by year in chunks of 60 talks. Rows have the same shape as `CORPUS`; selected shards are merged into `window.DHAMMA_CORPUS` and the search view switches `C` to it (`useCorpus`). Built by `tools/build_dhamma.py <caption dir> .` from captions fetched by `tools/collect_dhamma_captions.py tools/dhamma-queue.json` (2,554 clips in priority order; it skips files that already exist, so it can be resumed in any session). |
| `dhamma-glossary-core.js` | `DHAMMA_CORE`: ~70 key terms `[term, Thai, gloss, 'variants']`. Variants include the misspellings YouTube auto captions really produce (citta → jitta, rupa → ruper, kusala → kusula); check new ones by counting tokens in the captions. |
| `dhamma-glossary.js` | `DHAMMA_GLOSSARY`: 461 `[term, definition]` pairs parsed from dhammahome.com's Glossary of Pali Terms (article-en topics 124–148). |
| `tools/collect_captions.py` | Collects caption files from the channels listed in a TSV into `<TSV folder>/videos/<id>.json` (pauses when YouTube rate-limits). |
| `tools/build_data.py` | Turns a folder of caption files into `data.js` + `data-*.js`; also holds the topic and grammar word sets with Thai notes. |
| `tools/update_corpus.py` | Finds new suitable clips and appends them (`--save-dir` collects only, `--merge-dir` merges a folder; used by the nightly home job). Holds the classroom filters `UNSUITABLE` and `suitable()`. |
| `tools/home_run.py`, `tools/windows/setup.bat`, `tools/windows/run.bat` | The nightly job on the owner's computer and its one-time installer. |
| `tools/channels.tsv` | `handle<TAB>category<TAB>accent` for every channel used (128). |
| `tools/corpus-skip.json` | Clip ids never to add again (unsuitable, no captions, or removed on request). |
| `img/owl-192.png` | Dreamy Owl logo from the owner's main site. |

### `data.js` format (format 2, since 2026-10-24)
- `data.js` = `window.CORPUS = {fmt: 2, parts: [[file, clips, lines], …], clips, lines, accs, sets, quiz, top, cuts, removed}` (about 80 KB).
- `data-pNNNN.js` = one part of about 20,000 lines (~1 MB): `{v: [clip rows], s: [[clipIndexInPart, start, dur, text], …]}`. **Parts are append-only**: `build_data.append()` writes new clips into new parts and never rewrites published ones, so nightly commits stay small. Removed clips are listed in `removed` and skipped by the page.
- `data-i-X.js` = word index by first letter: `{token: [part numbers]}` or `0` when the token is in more than half of the parts.
- The page loads part 1 at once (hand-made captions and the learning/kids channels sort first). A search looks up its words in the index, loads the parts that hold them three at a time, best parts first, until it has about 80 clips, then shows "ค้นเพิ่มในคลัง (อีก N ชุด)". Loaded parts join `MAIN`, so the open clip never restarts. Stats show the totals from `data.js`.
- **Result order (owner's request, 2026-10-24):** everyday speech first. `clipRank()` in index.html and `TIER`/`everyday()` in build_data.py: tier 0 = movie, series, conversation, kids; tier 1 = learning, tv, documentary; tier 2 = interview, ted, news; titles about politics (`POLITICS` regex) last. Within a tier slower speech first, then hand-made captions. Each `parts` entry has a 4th number, the share of everyday clips (%), and searches load those parts first; part 1 (always loaded) is all everyday clips. The collector (`update_corpus.py`) also visits tier-0 channels first.
- `sets` keeps every item with its count (low counts too, so appends can add to them); the page shows items heard at least 3 times (2 for sets with a Thai note). `top` (2,500 commonest words) and `cuts` fix the level of new clips without re-levelling old ones. A full rebuild (`python3 -I tools/build_data.py <caption dir> data.js`) recomputes everything and renumbers the parts; avoid it unless needed, it rewrites every part.
- `counts.js` also stores `LESSON_PARTS` and `LESSON_KEY`; `count_lessons.js` only reads parts added since, unless the curriculum changed or `--full` is given.
- `v[i] = [videoId, title, channel, category, accent, captionKind('m' manual | 'a' auto), durationSec, wordsPerMinute, level]`
- `s[j] = [videoIndex, startSec, durSec, text]`, sorted by video then time.
- `sets[name] = {d: Thai description, w: [[phrase, lineCount, Thai note], ...]}`
- `quiz` = mid-frequency lowercase words used for the fill-in-the-blank quiz.
- Categories: movie, series, tv, interview, documentary, ted, news, conversation, learning (BBC Learning English…), kids (Sesame Street, Peppa Pig, Bluey…). Accents: US, UK, AUS, CAN, IRL, SCO, NZ (assigned by the channel's country, not per speaker).
- Level (A2–C1) is an estimate from speaking speed and the share of less common words, split by percentile. Native media has almost no A1 material; the site says so.

## Features in `index.html`
Search (English regex with word boundaries; Thai via `THAI_EN`, then free machine translation as fallback), filters (accent, category, speed, level), usage groups (`#useChips`, above the player: a common word returns hundreds of lines that teach different things, so `useKey()` reads the word that follows each hit and splits them into ปฏิเสธ, เป็นคำถาม and collocations such as "will be", "will you"; groups need 3 hits and the bar hides itself for a lesson, under 12 hits, or when the named groups cover less than a fifth of them), YouTube IFrame player that jumps to the line, subtitle strip with prev/next lines, approximate word-by-word highlight, Thai translation of the current line, controls and keyboard shortcuts (N P R B K L H T S), dictionary panel (dictionaryapi.dev, Wiktionary fallback) with "จุดที่คนไทยมักพลาด" tips, practice tabs (speak along with scoring via Web Speech API, continuous shadowing, dictation, write your own sentence, fill-in-the-blank quiz, minimal-pairs game), word sets, nearby words, notebook with spaced review (1·3·7·14·30 days), daily goal with streak. Learning system: a "แนะนำในคลิปนี้" guide per clip (sentences worth learning, connectors, Dhamma terms, useful words, each with a ☆ save), a notebook with filters, spaced review (1·3·7·14·30 days) whose word cards change form with the box (choose the Thai meaning → fill the gap from the clip → produce the English from Thai), lesson progress ticks and bars in both courses, a Dhamma word of the day, "lessons from the latest discussions", and backup/restore of all `fk.*` localStorage keys as a JSON file to move between devices (notes are merged). Notebook, stats and review live in `localStorage` per browser; there is no server or login.

## Automatic general-clip updates
Done on the owner's computer every night (see "Start here"). The GitHub workflow `update-corpus.yml` runs the same script weekly but YouTube blocks GitHub. Classroom filters: 1–20 min, embeddable, not age-restricted, no violent/adult/drug words in the title (`UNSUITABLE`, whole words only; "Stablecoins" and the name "Rapelang" once matched older patterns), at most 2 bleeped lines, mostly speech, English captions (hand-made preferred). Rejected clips go to `tools/corpus-skip.json`; adding a clip id there by hand also removes it from the corpus on the next run (it is listed in `removed`). When the corpus passes `--max`, auto-captioned clips from the biggest groups are removed, fastest speech first.
Teachers can hide an unsuitable clip with "🚫 ซ่อนคลิปนี้" under the player (per browser, `fk.hidden`); "คัดลอกรายการเพื่อส่งผู้ดูแล" in the filter box copies the ids to send to the owner, who adds them to `tools/corpus-skip.json`.

## Automatic Dhamma updates
`.github/workflows/update-dhamma.yml` runs `tools/update_dhamma.py` once a week on Tuesday 03:17 UTC (the owner asked for weekly checks), after the discussions are held on Saturday (International, India), Sunday (Chinese–English, Vietnamese–English) and Monday (English); it can also be started by hand from the Actions tab. Each run lists the newest clips of the two verified Ajahn Sujin channels, adds them to `dhamma.js`, fetches captions for up to 400 clips within 5 hours (short clips and English talks first), rebuilds the shards from the published shard files and commits.

Only clips where English is really spoken are kept: hand-made English captions, or YouTube speech recognition in English (`en-orig`). A plain `en` caption track alone is a machine translation; many "สตรีมแบบสดของ dhamma home" streams are Thai (`th-orig`). Rejected ids go to `tools/dhamma-skip.json` and disappear from `dhamma.js`. Streams whose title says nothing are listed as "ไลฟ์ (ยังไม่ตรวจภาษา)" until checked. The Alan Weller channel is not included (its videos do not say they are Ajahn Sujin's).

No raw caption files are stored; the shards are the source. If YouTube blocks GitHub's runners the log says "blocked by YouTube" and the run stops; then run the same script from a Claude Code session (`--caps-dir` merges captions collected elsewhere).

## Rebuilding or extending the corpus
The published files are the source; no raw caption files are kept. To add clips from a Claude Code session (Network access: Full) instead of the home computer:

```bash
python3 -m venv .venv && .venv/bin/pip install yt-dlp yt-dlp-ejs
.venv/bin/python -X utf8 -I tools/update_corpus.py --save-dir work --limit 400 --minutes 100   # run in the background (2-hour limit per command)
git fetch origin main && git reset --hard FETCH_HEAD     # the home job pushes to main too
.venv/bin/python -X utf8 -I tools/update_corpus.py --merge-dir work && node tools/count_lessons.js
```
For clips collected another way (e.g. `tools/collect_captions.py` for one channel), apply `UNSUITABLE` and `suitable()` yourself, write the kept records into a folder and use `--merge-dir`.

What we learned while collecting:
- From cloud IPs, YouTube answers normal requests with "Sign in to confirm you're not a bot". `yt-dlp` with `--extractor-args youtube:player_client=web_embedded --ignore-no-formats-error` still works, and it only returns videos whose owners allow embedding, which is exactly what the site needs. `youtube-transcript-api` was blocked.
- Caption files are fetched as `json3`; manual English captions are preferred, auto captions are the fallback.
- Channels that gave nothing (embedding disabled or no captions): @1NewsNZ, @7NEWS, @BBCThree, @VOALearningEnglish (no caption tracks at all), @TEDxTalks, @TheLateShow, @nbcsnl, @GQ. Few clips: @FallonTonight, @VanityFair, @jubilee, @PeppaPigOfficial (7), @LastWeekTonight (5).
- Of the 54 channels added on 2026-10-23, only the first 24 in the list were collected before time ran out; the weekly job will reach the rest.
- YouTube rate-limits one machine after a few hundred requests (HTTP 429, or clips coming back with no caption tracks). A "429" warning alone is harmless; `collect_captions.py` checks a known clip (PROBE) before pausing. yt-dlp now needs `yt-dlp-ejs` for its JavaScript challenge.
- Classroom filter results on the first big run: 37 clips dropped for titles (murder, drugs, sexual crimes…), 25 mostly music (Sesame Street songs), 7 with many bleeped words. Watch for false positives (a title with "Stablecoins" once matched "stab").
- The free translation services (MyMemory, translate.googleapis.com gtx) refuse cloud IPs but work from a normal home connection.

## Money and copyright (decided 2026-10-27; do not undo without the owner saying so)
- **Removed on the owner's instruction (2026-10-27):** the notebook's CSV download and the "อัดเสียงตัวเอง"
  recorder in the speaking tab. Neither was a copyright problem — the CSV held only the learner's own saved
  notes (300 at most, each with a link back to YouTube) and the recorder captured the learner's own voice into
  memory and never stored or sent it — but the owner did not want either, so do not add them back. The
  backup/restore pair (`bBackup` / `fRestore`) was kept: the owner asked for it so learners can move devices.
The owner asked whether students could be charged, YouGlish-style, and whether metering clips (20 free, then pay)
would be allowed. Both were researched and declined:
- **Never charge to watch a clip, and never meter them.** YouTube's API Services Developer Policies III.F:
  "API Clients must not charge users to watch content in an embedded YouTube player", and developers may not
  charge for what YouTube gives away free. The site uses the IFrame Player API, so this binds it. A free
  allowance followed by a paywall is still charging to watch.
- **Staying free also protects the stored captions.** `data-pNNNN.js` holds ~834,000 caption lines, which are
  the channel owners' copyright. The site relies on the teaching/study exception of the Thai Copyright Act
  (ม.32), which needs the use to be non-commercial. Charging would remove that footing on both sides at once.
- **Do not add a way to read a whole transcript.** The snippet-sized display is what keeps the position
  defensible: the strip shows the matched sentence plus one line either side, and `renderGuide()` picks at most
  6 sentences per clip. Keep those caps.
- Income comes from the owner's own CEFR course instead. `#joinCard` in index.html invites learners to it after
  20, 100 and 400 searches; it is dismissible and blocks nothing. Edit that markup to change the wording or link.
- The About box carries the source credits, states that no video is downloaded, and promises removal within
  48 hours on request (`tools/corpus-skip.json` is how a clip is taken out). Keep all three.

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
