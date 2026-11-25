// Export SRT captions from the built timeline.
import { readFileSync, writeFileSync } from 'node:fs';

const tl = JSON.parse(readFileSync('build/timeline.json', 'utf8'));
const pad = (n, w = 2) => String(n).padStart(w, '0');
const ts = (s) => {
  s = Math.max(0, s);
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = Math.floor(s % 60);
  const ms = Math.round((s - Math.floor(s)) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(sec)},${pad(ms, 3)}`;
};
const out = tl.captions.map((c, i) =>
  `${i + 1}\n${ts(c.start)} --> ${ts(c.end)}\n${c.text}\n`).join('\n');
writeFileSync('build/captions.srt', out, 'utf8');
console.log('captions.srt', tl.captions.length, 'lines');
