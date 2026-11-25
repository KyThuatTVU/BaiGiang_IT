// Dựng timeline tổng từ audio theo cảnh: thời lượng cảnh, cue, phụ đề, sự kiện âm thanh.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const script = JSON.parse(readFileSync('build/script.json', 'utf8'));
const scenes = script.scenes;

const LEAD = { divider: 0.9, coldopen: 1.1, outro: 1.2, default: 0.8 };
const TAIL = { divider: 1.3, outro: 3.0, default: 1.0 };
const FPS = 25;

function voice(id) {
  const p = `build/voice/scenes/${id}.json`;
  if (!existsSync(p)) throw new Error('missing voice ' + id);
  const v = JSON.parse(readFileSync(p, 'utf8'));
  if (!v.cues || v.cues.length === 0) throw new Error('missing cue spans ' + id);
  return v;
}

function splitChunks(text, max = 75) {
  const sentences = text.match(/[^.!?;:]+[.!?;:]?/g) || [text];
  const out = [];
  for (let s of sentences) {
    s = s.trim();
    if (!s) continue;
    while (s.length > max) {
      let cut = -1;
      const slice = s.slice(0, max + 1);
      for (const ch of [',', ';', ':', '—', '–', '-', ' ']) {
        const i = slice.lastIndexOf(ch);
        if (i > max * 0.3) { cut = i; break; }
      }
      if (cut < 0) cut = max;
      out.push(s.slice(0, cut + 1).trim());
      s = s.slice(cut + 1).trim();
    }
    if (s) out.push(s);
  }
  const merged = [];
  for (const ch of out) {
    const prev = merged[merged.length - 1];
    if (prev && ch.length < 18 && prev.length + 1 + ch.length <= 64) merged[merged.length - 1] = prev + ' ' + ch;
    else merged.push(ch);
  }
  return merged;
}

const weight = (s) => s.replace(/\s/g, '').length + 12;

let t = 0;
const tlScenes = [];
const captions = [];
const sfx = [];
const typingScenes = new Set(['sql-create', 'sql-insert', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']);

for (const sc of scenes) {
  const lead = LEAD[sc.type] ?? LEAD.default;
  const tail = TAIL[sc.type] ?? TAIL.default;
  const start = t;
  const v = voice(sc.id);
  const spans = v.cues;
  const cues = sc.cues.map((c, i) => {
    const sp = spans[i] || spans[spans.length - 1];
    const s = start + lead + sp.start;
    const e = start + lead + Math.max(sp.end, sp.start + 0.35);
    return { ...c, start: +s.toFixed(3), end: +e.toFixed(3), dur: +(e - s).toFixed(3) };
  });
  const audioEnd = start + lead + v.dur;
  const dur = +(audioEnd + tail - start).toFixed(3);
  tlScenes.push({ id: sc.id, type: sc.type, part: sc.part, title: sc.title, start: +start.toFixed(3), dur, lead, audio: v.dur, cues });

  for (const c of cues) {
    if (c.sfx) sfx.push({ t: +(c.start + 0.03).toFixed(3), type: c.sfx, gain: 1 });
    const chunks = splitChunks(c.say);
    const wsum = chunks.reduce((a, s) => a + weight(s), 0);
    let w = 0;
    const span = c.end - c.start;
    for (const ch of chunks) {
      const s0 = c.start + (span * w) / wsum;
      const d = (span * weight(ch)) / wsum;
      captions.push({ start: +s0.toFixed(3), end: +(s0 + d).toFixed(3), text: ch });
      w += weight(ch);
    }
  }

  if (typingScenes.has(sc.id)) {
    const typeCue = cues.find((c) => c.sfx === 'type');
    if (typeCue) {
      const t0 = typeCue.start + 0.1;
      const t1 = typeCue.end - 0.05;
      let i = 0;
      for (let x = t0; x < t1; x += 0.085) {
        if (i % 4 !== 3) sfx.push({ t: +x.toFixed(3), type: 'key', gain: 0.5 + (i % 3) * 0.08 });
        i++;
      }
    }
  }

  t = start + dur;
}

const duration = +t.toFixed(3);
const timeline = { fps: FPS, width: 1920, height: 1080, duration, scenes: tlScenes, captions, sfx };

writeFileSync('build/timeline.json', JSON.stringify(timeline, null, 1));
writeFileSync('src/timeline.js', 'window.__TIMELINE = ' + JSON.stringify(timeline) + ';\n');
console.log('duration', (duration / 60).toFixed(2), 'min |', tlScenes.length, 'scenes |',
  captions.length, 'captions |', sfx.length, 'sfx');
