// Xuất kịch bản nguồn (ESM) ra build/script.json cho TTS và timeline.
// --sample : chỉ xuất 3 cảnh mở đầu (intro, personalization, matrix) để dựng mẫu 30–45s.
import { mkdirSync, writeFileSync } from 'node:fs';
import { scenes } from '../src/data/script.mjs';

const sample = process.argv.includes('--sample');
const SAMPLE_IDS = ['intro', 'personalization', 'matrix'];
const picked = sample ? scenes.filter((s) => SAMPLE_IDS.includes(s.id)) : scenes;

mkdirSync('build', { recursive: true });
const out = {
  title: 'Cá nhân hóa người dùng và các thuật toán trong hệ thống gợi ý sản phẩm',
  sample, scenes: picked
};
writeFileSync('build/script.json', JSON.stringify(out, null, 1));
const cues = picked.reduce((n, s) => n + s.cues.length, 0);
console.log(`script.json${sample ? ' [SAMPLE]' : ''}: ${picked.length} scenes, ${cues} cues`);