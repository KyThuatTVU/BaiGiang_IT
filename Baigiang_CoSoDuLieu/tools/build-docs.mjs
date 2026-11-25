// Sinh tài liệu storyboard và lời thoại từ script + timeline (nếu đã dựng).
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';

const script = JSON.parse(readFileSync('build/script.json', 'utf8'));
const tl = existsSync('build/timeline.json') ? JSON.parse(readFileSync('build/timeline.json', 'utf8')) : null;
const tmap = new Map((tl?.scenes || []).map((s) => [s.id, s]));
mkdirSync('docs', { recursive: true });

const VIS = {
  intro: ['Nền tối navy, lưới kỹ thuật, trụ dữ liệu 3D phát sáng; tiêu đề lớn hai dòng màu trắng/cyan.', 'Tiêu đề trượt và mở bằng clip-path; hạt sáng và vòng quét; nhịp boot.', 'boot, whoosh'],
  objectives: ['Bảy thẻ lộ trình học tập xếp thành lưới, đánh số phần 1–7.', 'Thẻ hiện dần theo nhóm nội dung; thẻ đang nói được viền cyan.', 'whoosh, sparkle'],
  divider: ['Số phần lớn dạng outline, tên phần, nhãn tiếng Anh; vạch sáng ngang.', 'Số phần đếm/scale nhẹ, vạch sáng quét, nền chuyển sắc.', 'riser'],
  dbconcept: ['Thẻ định nghĩa "cơ sở dữ liệu", ba ví dụ dạng chip, sơ đồ dữ liệu có cấu trúc.', 'Từ khóa nhấn màu; các chip hiện lần lượt; đường nối giữa các khối.', 'chime'],
  datainfo: ['Hai cột DỮ LIỆU (số thô) → THÔNG TIN (doanh thu theo tháng), mũi tên xử lý.', 'Con số thô bay vào bộ xử lý, biểu đồ cột mọc lên.', 'chime'],
  whydb: ['Bốn vấn đề của file truyền thống đối chiếu bốn giải pháp của CSDL.', 'Từng cặp vấn đề–giải pháp sáng lên; dấu gạch đỏ → dấu kiểm xanh.', 'whoosh, sparkle'],
  shop: ['Bối cảnh cửa hàng điện thoại: 1.200 sản phẩm, 380 khách, 5.000+ hóa đơn/năm; so sánh Excel rời rạc và CSDL tập trung.', 'Bộ đếm tăng dần; các file Excel tản mát bị gom về một khối dữ liệu.', 'whoosh, success'],
  dbms: ['Bốn thẻ DBMS: MySQL, SQL Server, PostgreSQL, Oracle; lõi chung SQL ở giữa.', 'Thẻ lật/hiện lần lượt; dòng "SQL" chạy qua cả bốn.', 'whoosh'],
  tableanatomy: ['Bảng SinhVien 4 cột; chú thích field/record/bảng; một dòng được tô sáng.', 'Đường dẫn chú thích vẽ ra; dòng SV002 sáng lên như một bản ghi.', 'chime'],
  primarykey: ['Bảng SinhVien, cột MaSV tô vàng; hộp thoại thử INSERT trùng SV002 bị từ chối.', 'Cột PK sáng dần; toast lỗi rung nhẹ; so sánh hai sinh viên cùng tên.', 'chime, error'],
  foreignkey: ['Hai bảng LOP và SINHVIEN; đường nối MaLop; thử INSERT lớp DA99 bị từ chối.', 'Đường nối vẽ từ trái sang; cột FK phát sáng; toast lỗi xuất hiện.', 'whoosh, error'],
  'rel-1-1': ['Hai thẻ SINHVIEN và HOSO, đường 1—1, nhãn UNIQUE trên MaSV của HOSO.', 'Thẻ trượt vào; đường nối vẽ; cột FK+UNIQUE nhấn sáng; ghi chú hiện dưới.', 'whoosh'],
  'rel-1-n': ['Thẻ LOP bên trái, bảng SINHVIEN bên phải, đường 1—N trỏ vào bảng.', 'Đường nối và mũi tên vẽ; cột MaLop của cả 4 dòng sáng lên; ví dụ thực tế hiện dần.', 'whoosh, chime'],
  'rel-n-n': ['Hai thẻ SINHVIEN và MONHOC, bảng trung gian DANGKY ở giữa với khóa chính ghép.', 'Hai nhánh 1—N vẽ xuống bảng giữa; MaSV+MaMH chuyển vàng; kết luận "2 quan hệ 1—N".', 'whoosh, chime, success'],
  'erd-concepts': ['Ký pháp ERD: hình chữ nhật thực thể, elip thuộc tính, hình thoi quan hệ; ánh xạ sang bảng.', 'Ba ký pháp hiện lần lượt; phép biến đổi entity→table, attribute→column.', 'chime'],
  'erd-analysis': ['Yêu cầu bài toán → gạch chân danh từ → 5 thực thể; sơ đồ quan hệ sơ bộ.', 'Các danh từ được đánh dấu và bay vào thẻ thực thể; đường quan hệ nối dần.', 'whoosh, chime'],
  'erd-build': ['ERD hoàn chỉnh 5 bảng của cửa hàng điện thoại; PK vàng, FK xanh; nhãn 1—N.', 'Từng bảng và đường quan hệ hiện theo lời giảng; ghi chú DonGia trong ChiTietHoaDon.', 'whoosh, chime, sparkle'],
  'sql-groups': ['Năm cột nhóm lệnh DDL, DML, DQL, DCL, TCL kèm lệnh đại diện.', 'Cột hiện lần lượt; lệnh đang nói được đóng khung; bản đồ tổng thể hoàn chỉnh.', 'chime, sparkle'],
  'sql-create': ['Trình soạn SQL tối màu; gõ CREATE TABLE SinhVien; thẻ kết quả "tạo bảng thành công".', 'Con trỏ gõ từng ký tự, token đổi màu; toast xanh sau khi chạy.', 'whoosh, type, success'],
  'sql-insert': ['Gõ INSERT INTO SinhVien; bảng kết quả SELECT * hiện bản ghi mới.', 'Gõ lệnh, dòng mới trượt vào result set; nhấn chữ N trước chuỗi Unicode.', 'type, chime, success'],
  'shop-schema': ['Bốn bảng dữ liệu mẫu: SANPHAM, KHACHHANG, HOADON, CHITIET HOADON; quy trình 4 bước đọc đề → SQL → kết quả.', 'Bảng hiện dần; badge số dòng; dải 4 bước sáng lên.', 'whoosh'],
  q1: ['Đề bài, phân tích, SQL SELECT * FROM SanPham, bảng kết quả 5 dòng.', 'Các bước phân tích hiện; gõ SQL; kết quả và toast thành công.', 'whoosh, type, success'],
  q2: ['SQL WHERE DonGia > 10000000; kết quả 3 sản phẩm cao cấp.', 'Gõ lệnh; các dòng không thỏa bị làm mờ; 3 dòng đạt được nhấn.', 'whoosh, type, success'],
  q3: ['SQL DISTINCT + INNER JOIN KhachHang/HoaDon; kết quả 3 khách đã mua.', 'Sơ đồ nối bảng; bảng kết quả lọc trùng; khách chưa mua bị loại.', 'whoosh, type, success'],
  q4: ['SQL SUM(SoLuong*DonGia); bảng tính doanh thu từng hóa đơn và tổng 215 triệu.', 'Từng hóa đơn cộng dồn; tổng tiền đếm lên; nhấn hàm SUM.', 'whoosh, type, success'],
  q5: ['SQL GROUP BY MaSP với SUM(SoLuong); biểu đồ thanh số lượng theo sản phẩm.', 'Các thanh mọc lần lượt; SP01 dẫn đầu 4 chiếc.', 'whoosh, type, success'],
  q6: ['SQL nối 4 bảng INNER JOIN; sơ đồ join; bảng kê 8 dòng với thành tiền.', 'Sơ đồ nối bảng sáng dần; gõ câu lệnh dài; bảng kết quả 8 dòng.', 'whoosh, type, success'],
  summary: ['Sáu thẻ tổng kết: khái niệm, bảng/PK/FK, quan hệ, ERD, SQL, quy trình thực tế.', 'Thẻ hiện lần lượt theo lời thoại; dấu kiểm hoàn thành.', 'sparkle, success'],
  quiz: ['Năm câu hỏi trắc nghiệm A–D, tiến độ 5 câu, thẻ điểm cuối 5/5.', 'Câu hỏi hiện; đáp án đúng sáng xanh; chuyển câu; vòng điểm kết thúc.', 'whoosh, success, sparkle'],
  outro: ['Lời kết, ba bước thực hành, lời cảm ơn; nền tối dần.', 'Nội dung hiện rồi fade out; logo và tiêu đề giữ lại.', 'chime, sparkle']
};
const FALLBACK = ['Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính.', 'Các khối nội dung hiện dần theo lời thoại.', 'whoosh'];

const sfxOf = (sc) => [...new Set(sc.cues.map((c) => c.sfx).filter(Boolean))].join(', ') || '—';
const fmt = (s) => {
  if (s == null) return '—';
  const m = Math.floor(s / 60), sec = Math.floor(s % 60);
  return `${m}:${String(sec).padStart(2, '0')}`;
};

// ---------- storyboard ----------
let rows = [];
script.scenes.forEach((sc, i) => {
  const v = VIS[sc.id] || FALLBACK;
  const t = tmap.get(sc.id);
  rows.push(`| ${i + 1} | \`${sc.id}\` | ${sc.part ? 'P' + sc.part : 'Mở đầu'} | **${sc.title}** | ${v[0]} | ${v[1]} | ${sfxOf(sc)} | ${t ? fmt(t.dur) : '—'} | ${t ? fmt(t.start) : '—'} |`);
});
let story = `# Storyboard — Cơ sở dữ liệu và ứng dụng trong thực tế

Video 16:9, 1920×1080, 25 fps. Toàn bộ hình ảnh được dựng bằng HTML/CSS/SVG (không dùng ảnh tĩnh ghép slide);
mỗi cảnh là một "sân khấu" động, render theo từng khung hình từ \`window.renderFrame(t)\`.

- Tổng số cảnh: **${script.scenes.length}**
- Tổng số cue thuyết minh: **${script.scenes.reduce((a, s) => a + s.cues.length, 0)}**
- Thời lượng: **${tl ? fmt(tl.duration) + ' (' + (tl.duration / 60).toFixed(1) + ' phút)' : 'đang cập nhật sau khi dựng timeline'}**
- Ảnh still QA: \`build/previews/<scene-id>.png\` (36 ảnh, chụp ở cuối mỗi cảnh)

## Bảng storyboard

| # | Scene ID | Phần | Tiêu đề | Hình ảnh chính | Chuyển động / nhấn | SFX | Thời lượng | Bắt đầu |
|---|---|---|---|---|---|---|---|---|
${rows.join('\n')}

## Danh sách hình ảnh & tài nguyên

| Nhóm | Tệp / nguồn | Dùng cho |
|---|---|---|
| Ảnh still QA | \`build/previews/*.png\` (36 tệp) | Kiểm tra bố cục từng cảnh |
| Font tiêu đề | \`assets/fonts/be-vietnam-pro-*.woff2\` | Toàn bộ chữ Latin + tiếng Việt |
| Font code | \`assets/fonts/jetbrains-mono-*.woff2\` | SQL, mã bảng, nhãn kỹ thuật |
| Nền & hiệu ứng | CSS gradient + lưới + hạt (không tệp) | Nền công nghệ navy/cyan |
| Sơ đồ ERD, mũi tên, biểu đồ | SVG nội tuyến trong \`src/app.js\` | Phần 3, 4, 6 |
| Dữ liệu mẫu | \`src/app.js\` (SV, SP, KH, HD, CT) + \`build/script.json\` | Bảng, ERD, truy vấn |
| Giọng đọc | \`build/voice/scenes/*.wav\` | Thuyết minh từng cảnh |
| Nhạc nền & SFX | Sinh bằng numpy trong \`tools/build-audio.py\` | Ambient pad, pulse, pluck, whoosh/chime/type… |
| Phụ đề | \`build/captions.srt\` | Bản dịch thoại kèm video |

## Nguyên tắc hình ảnh

- Nền navy \`#050d1a\` → \`#0a1c30\`, lưới mảnh, hạt sáng, glow cyan \`#22d3ee\`.
- Màu ngữ nghĩa: vàng \`#fbbf24\` = khóa chính; xanh \`#38bdf8\` = khóa ngoại; đỏ \`#f87171\` = lỗi;
  xanh lá \`#6ee7b7\` = thành công.
- Mỗi cảnh có nhịp: tiêu đề → nội dung chính → nhấn trọng tâm → kết luận, khớp với cue thuyết minh.
`;
writeFileSync('docs/storyboard.md', story, 'utf8');

// ---------- narration ----------
let nar = `# Lời thoại bài giảng (bản đầy đủ)

Giọng đọc: \`vi-VN-NamMinhNeural\` (Edge TTS, nam, giọng Bắc chuẩn; xem README về giới hạn giọng miền Nam).
Thời lượng: ${tl ? fmt(tl.duration) : 'đang cập nhật'}. Thời gian dưới đây là mốc tuyệt đối trong video.

`;
let curPart = null;
script.scenes.forEach((sc) => {
  if (sc.part !== curPart) {
    curPart = sc.part;
    nar += curPart ? `\n## Phần ${curPart}\n\n` : `\n## Mở đầu\n\n`;
  }
  const t = tmap.get(sc.id);
  nar += `### ${sc.title}\n\n`;
  if (t) nar += `*Cảnh ${fmt(t.start)} – ${fmt(t.start + t.dur)} (${t.dur.toFixed(1)} giây)*\n\n`;
  sc.cues.forEach((c) => {
    const cue = t?.cues.find((x) => x.id === c.id);
    const tm = cue ? `\`${fmt(cue.start)}\` ` : '';
    nar += `- ${tm}${c.say}${c.sfx ? ` *[${c.sfx}]*` : ''}\n`;
  });
  nar += '\n';
});
writeFileSync('docs/loi-thoai.md', nar, 'utf8');
console.log('docs/storyboard.md, docs/loi-thoai.md');
