// Counts how many corpus lines each course lesson finds and writes counts.js.
// Run from the repository root after changing data.js or curriculum.js:  node tools/count_lessons.js [--full]
// Only parts added since the last count are read (counts.js remembers how many were counted), unless the
// curriculum changed or --full is given; then every part is read again.
const fs = require('fs'), path = require('path');
global.window = {};
const root = path.join(__dirname, '..');
require('../data.js'); require('../curriculum.js');
const C = window.CORPUS, esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const norm = s => s.toLowerCase().replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim();
const makeRe = q => new RegExp("(^|[^a-z0-9'’])(" + norm(q).split('|').map(x => esc(x.trim()).replace(/'/g, "['’]").replace(/ /g, "[\\s,.\\-–—]+")).join('|') + ")(?=$|[^a-z0-9'’])", 'i');

const lessons = [];
for (const [key, c] of Object.entries(window.COURSES))
  c.volumes.forEach((v, vi) => v.sections.forEach(s => s.lessons.forEach(l => lessons.push([key + '-' + vi + '-' + l[0], l[3]]))));
const curKey = require('crypto').createHash('md5').update(JSON.stringify(lessons)).digest('hex');

const countsFile = path.join(root, 'counts.js');
if (fs.existsSync(countsFile)) require(countsFile);
const parts = C.parts || [];
const fmt2 = C.fmt === 2;
let from = 0, out = {};
if (fmt2 && !process.argv.includes('--full') && window.LESSON_KEY === curKey && window.LESSON_COUNTS) {
  from = window.LESSON_PARTS || 0; out = window.LESSON_COUNTS;
}
lessons.forEach(([id]) => { if (out[id] === undefined) out[id] = 0; });

// Lines of the parts to count.
const lines = [];
if (fmt2) {
  for (let i = from; i < parts.length; i++) {
    require(path.join(root, parts[i][0]));
    for (const r of window.CORPUS_PARTS[i + 1].s) lines.push(r[3]);
    delete window.CORPUS_PARTS[i + 1];
  }
} else {
  (C.s || []).forEach(r => lines.push(r[3]));
  parts.forEach((p, i) => { require(path.join(root, p[0])); window.CORPUS_PARTS[i].forEach(r => lines.push(r[3])); });
}
for (const [id, phrases] of lessons) {
  const re = makeRe(phrases); let n = 0;
  for (const t of lines) if (re.test(t)) n++;
  out[id] += n;
}
fs.writeFileSync(countsFile, 'window.LESSON_COUNTS=' + JSON.stringify(out) + ';\nwindow.LESSON_PARTS=' + (fmt2 ? parts.length : 0) +
  ';\nwindow.LESSON_KEY=' + JSON.stringify(curKey) + ';\n');
const z = Object.entries(out).filter(([, n]) => n < 3);
console.log(lessons.length, 'lessons; counted parts', from + 1, 'to', parts.length, ';', z.length, 'with fewer than 3 lines:', z.map(([k, n]) => k + '=' + n).join(' '));
