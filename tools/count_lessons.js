// Counts how many corpus lines each course lesson finds and writes counts.js.
// Run from the repository root after changing data.js or curriculum.js:  node tools/count_lessons.js
global.window = {};
require('../data.js'); require('../curriculum.js');
const C = window.CORPUS, esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const norm = s => s.toLowerCase().replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim();
const makeRe = q => new RegExp("(^|[^a-z0-9'’])(" + norm(q).split('|').map(x => esc(x.trim()).replace(/'/g, "['’]").replace(/ /g, "[\\s,.\\-–—]+")).join('|') + ")(?=$|[^a-z0-9'’])", 'i');
const out = {};
for (const [key, c] of Object.entries(window.COURSES))
  c.volumes.forEach((v, vi) => v.sections.forEach(s => s.lessons.forEach(l => {
    const re = makeRe(l[3]); let n = 0;
    for (const x of C.s) if (re.test(x[3])) n++;
    out[key + '-' + vi + '-' + l[0]] = n;
  })));
require('fs').writeFileSync(require('path').join(__dirname, '..', 'counts.js'), 'window.LESSON_COUNTS=' + JSON.stringify(out) + ';\n');
const z = Object.entries(out).filter(([, n]) => n < 3);
console.log(Object.keys(out).length, 'lessons;', z.length, 'with fewer than 3 lines:', z.map(([k, n]) => k + '=' + n).join(' '));
