// Xuất phụ đề SRT từ caption trong timeline.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const tl = JSON.parse(readFileSync('build/timeline.json', 'utf8'));
const ts = (s) => {
  const ms = Math.round(s * 1000);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const sec = Math.floor((ms % 60000) / 1000);
  const milli = ms % 1000;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')},${String(milli).padStart(3, '0')}`;
};

const body = tl.captions.map((c, i) =>
  `${i + 1}\n${ts(c.start)} --> ${ts(c.end)}\n${c.text}\n`).join('\n');

mkdirSync('build', { recursive: true });
writeFileSync('build/subtitles.srt', body, 'utf8');
console.log(`subtitles.srt: ${tl.captions.length} cues, ${ts(tl.duration)}`);
