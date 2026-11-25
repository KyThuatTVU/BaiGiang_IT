// Sinh docs/loi-thoai.md từ timeline thật (ước lượng hoặc đã có giọng đọc).
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const tl = JSON.parse(readFileSync('build/timeline.json', 'utf8'));
const realVoice = tl.scenes.every((s) => existsSync(`build/voice/scenes/${s.id}.json`));
const fmt = (s) => {
  const m = Math.floor(s / 60);
  const sec = s - m * 60;
  return `${m}:${sec.toFixed(1).padStart(4, '0')}`;
};
const fmtShort = (s) => {
  const m = Math.floor(s / 60);
  const sec = Math.round(s - m * 60);
  return `${m}:${String(sec).padStart(2, '0')}`;
};

const PART = {
  null: 'Mở đầu',
  1: 'Phần 1 — Backend là gì',
  2: 'Phần 2 — Ngôn ngữ vs Framework',
  3: 'Phần 3 — Bảy hệ sinh thái',
  4: 'Phần 4 — So sánh và lựa chọn',
  5: 'Phần 5 — Backend hoạt động thật',
  6: 'Phần 6 — Tổng kết và quiz'
};

let md = `# Lời thoại — Khám phá ngôn ngữ lập trình và framework Backend

Giọng đọc: **vi-VN-NamMinhNeural** (Edge TTS), tốc độ **+22%** (\u2248 1.22x), loudnorm I=-19 dBTP, 48 kHz.
Tổng thời lượng: **${fmt(tl.duration)}** (${tl.duration.toFixed(0)} giây) · ${tl.scenes.length} cảnh · ${tl.captions.length} phụ đề.

> ${realVoice
  ? 'Mốc thời gian khớp trực tiếp với file WAV giọng đọc thật của từng cue (độ lệch dưới 1 khung hình).'
  : 'Mốc thời gian dưới đây là ước lượng từ số từ trước khi tổng hợp giọng đọc; sau khi có WAV thật, file này được sinh lại và mốc sẽ khớp chính xác đến từng cue.'}

`;

for (const sc of tl.scenes) {
  md += `\n## ${sc.title}\n\n`;
  md += `**Cảnh \`${sc.id}\`** · ${fmt(sc.start)} → ${fmt(sc.start + sc.dur)} (${sc.dur.toFixed(1)}s) · ${PART[String(sc.part)] || ''}\n\n`;
  md += `| Thời điểm | Cue | Lời thoại | SFX |\n|---|---|---|---|\n`;
  for (const c of sc.cues) {
    const say = c.say.replace(/\|/g, '\\|');
    const sfx = [c.sfx, c.hold ? `hold ${c.hold}s` : ''].filter(Boolean).join(' + ') || '—';
    md += `| ${fmt(c.start)} | \`${c.id}\` | ${say} | ${sfx} |\n`;
  }
}

md += `\n---\n\nTổng: **${fmt(tl.duration)}**. Kịch bản không dùng mật khẩu thật; ví dụ đăng nhập chỉ mô tả bcrypt + JWT ở mức khái niệm.\n`;

mkdirSync('docs', { recursive: true });
writeFileSync('docs/loi-thoai.md', md, 'utf8');
console.log(`loi-thoai.md: ${tl.scenes.length} scenes, ${fmt(tl.duration)}`);
