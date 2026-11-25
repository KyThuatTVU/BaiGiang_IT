// Dựng timeline tuyệt đối từ độ dài giọng đọc thật (nếu có) hoặc ước lượng.
// Xuất build/timeline.json và src/timeline.js cho engine cảnh.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const ESC = 3.8;          // từ / giây ở tốc độ +22%
const PAD_HEAD = 0.12;
const GAP = 0.30;
const TAIL = 0.38;
const SCENE_GAP = 0.34;
const MIN = {
  intro: 24, goals: 14, div1: 2.5, backend: 34, flow: 22, div2: 3,
  langfw: 36, div3: 2.8, js: 33, python: 34, php: 26, java: 25,
  csharp: 23, go: 22, ruby: 22, compare: 30, choose: 23, login: 36,
  recap: 17, quiz: 35, outro: 12
};

const script = JSON.parse(readFileSync('build/script.json', 'utf8'));

const estimate = (text) => {
  const tokens = text.trim().split(/\s+/).filter(Boolean).length;
  const pauses = (text.match(/[,.;:!?…]/g) || []).length;
  return Math.max(1.6, tokens / ESC + 0.42 + pauses * 0.11);
};

const voiceOf = (id) => {
  const p = `build/voice/scenes/${id}.json`;
  return existsSync(p) ? JSON.parse(readFileSync(p, 'utf8')) : null;
};

const chunkText = (text, max = 78) => {
  const parts = text.match(/[^,.;:!?…]+[,.;:!?…]?/g) || [text];
  const out = [];
  for (const part of parts) {
    const s = part.trim();
    if (!s) continue;
    if (s.length <= max) { out.push(s); continue; }
    const words = s.split(/\s+/);
    let line = '';
    for (const w of words) {
      if ((line + ' ' + w).trim().length > max && line) { out.push(line.trim()); line = w; }
      else line = (line + ' ' + w).trim();
    }
    if (line) out.push(line.trim());
  }
  return out;
};

let cursor = 0.0;
const scenes = [];
const captions = [];
const sfx = [];

for (const sc of script.scenes) {
  const v = voiceOf(sc.id);
  let spans;
  let total;
  if (v) {
    spans = v.cues;
    total = v.dur;
  } else {
    spans = [];
    let t = PAD_HEAD;
    for (const c of sc.cues) {
      const d = estimate(c.say);
      spans.push({ id: c.id, start: +t.toFixed(3), end: +(t + d).toFixed(3) });
      t += d + GAP + (c.hold || 0);
    }
    total = t - GAP + TAIL;
  }
  total = Math.max(total, MIN[sc.id] || 6);
  const start = +cursor.toFixed(3);
  const dur = +total.toFixed(3);
  const cues = sc.cues.map((c, i) => ({
    id: c.id,
    say: c.say,
    start: +(start + spans[i].start).toFixed(3),
    end: +(start + spans[i].end).toFixed(3),
    dur: +(spans[i].end - spans[i].start).toFixed(3),
    hold: c.hold || 0,
    sfx: c.sfx || null
  }));

  // caption theo cụm dấu câu, chia thời gian theo số ký tự
  cues.forEach((c, ci) => {
    const pieces = chunkText(c.say);
    const chars = pieces.map((p) => p.length);
    const sum = chars.reduce((a, b) => a + b, 0) || 1;
    const span = Math.max(0.4, c.end - c.start);
    let t = c.start;
    const items = pieces.map((p, i) => {
      const d = (chars[i] / sum) * span;
      const it = { text: p, start: t, end: t + d };
      t += d;
      return it;
    });
    // gộp cụm quá ngắn để phụ đề không nhấp nháy
    for (let i = 0; i < items.length - 1;) {
      const short = items[i].end - items[i].start < 0.9;
      if (short && items[i].text.length + items[i + 1].text.length + 1 <= 92) {
        items[i].text += ' ' + items[i + 1].text;
        items[i].end = items[i + 1].end;
        items.splice(i + 1, 1);
      } else i++;
    }
    const last = items[items.length - 1];
    const nextStart = ci + 1 < cues.length ? cues[ci + 1].start : last.end + 2;
    last.end = Math.max(last.end, Math.min(last.start + 1.0, nextStart - 0.06));
    for (const it of items) {
      captions.push({
        start: +it.start.toFixed(3),
        end: +(Math.max(it.start + 0.3, it.end - 0.04)).toFixed(3),
        text: it.text
      });
    }
  });

  for (const c of cues) {
    if (c.sfx) sfx.push({ t: +Math.max(0, c.start - 0.12).toFixed(3), type: c.sfx, gain: 0.9 });
    if (c.hold) {
      for (let k = 0; k < Math.floor(c.hold); k++) {
        sfx.push({ t: +(c.end + 0.55 + k).toFixed(3), type: 'tick', gain: 0.5 });
      }
    }
  }

  scenes.push({ id: sc.id, type: sc.type, part: sc.part, title: sc.title, start, dur, lead: spans[0].start, cues });
  cursor = start + dur + SCENE_GAP;
}

captions.sort((a, b) => a.start - b.start);
sfx.sort((a, b) => a.t - b.t);
const duration = +(scenes[scenes.length - 1].start + scenes[scenes.length - 1].dur + 0.6).toFixed(3);
const timeline = { fps: 25, width: 1920, height: 1080, duration, scenes, captions, sfx };

mkdirSync('build', { recursive: true });
writeFileSync('build/timeline.json', JSON.stringify(timeline, null, 1));
writeFileSync('src/timeline.js', 'window.__TIMELINE=' + JSON.stringify(timeline) + ';\n');

const speech = captions.reduce((a, c) => a + (c.end - c.start), 0);
console.log(`timeline ${duration.toFixed(1)}s (${(duration / 60).toFixed(2)} min) | ${scenes.length} scenes | ${captions.length} captions | ${sfx.length} sfx | speech ${speech.toFixed(0)}s`);
for (const s of scenes) {
  console.log(`  ${s.id.padEnd(9)} ${s.start.toFixed(1).padStart(6)}s  ${s.dur.toFixed(1).padStart(5)}s  ${s.cues.length} cues`);
}
