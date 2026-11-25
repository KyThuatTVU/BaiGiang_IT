// Xuất kịch bản nguồn (ESM) ra build/script.json cho TTS và timeline.
import { mkdirSync, writeFileSync } from 'node:fs';
import { scenes } from '../src/data/script.mjs';

mkdirSync('build', { recursive: true });
const out = { title: 'Thiết kế màu sắc và chuẩn hóa hệ thống nút bấm', scenes };
writeFileSync('build/script.json', JSON.stringify(out, null, 1));
const cues = scenes.reduce((n, s) => n + s.cues.length, 0);
console.log(`script.json: ${scenes.length} scenes, ${cues} cues`);
