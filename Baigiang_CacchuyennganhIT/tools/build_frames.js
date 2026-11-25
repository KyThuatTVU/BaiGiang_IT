const fs = require('fs');
const path = require('path');
const ROOT = 'D:/Edit/Baigiang_CacchuyennganhIT';
const ICON = n => fs.readFileSync(path.join(ROOT, 'assets/icons', n + '.svg'), 'utf8')
  .replace(/<\?xml[^>]*\?>/, '')
  .replace(/width="24"/, 'width="100%"').replace(/height="24"/, 'height="100%"');

const FONTS = `
@font-face{font-family:'Plus Jakarta Sans';src:url('file:///${ROOT}/assets/fonts/PlusJakartaSans-var.ttf') format('truetype');font-weight:100 900;}
@font-face{font-family:'Be Vietnam Pro';src:url('file:///${ROOT}/assets/fonts/BeVietnamPro-Regular.ttf') format('truetype');font-weight:400;}
@font-face{font-family:'Be Vietnam Pro';src:url('file:///${ROOT}/assets/fonts/BeVietnamPro-Medium.ttf') format('truetype');font-weight:500;}
@font-face{font-family:'Be Vietnam Pro';src:url('file:///${ROOT}/assets/fonts/BeVietnamPro-SemiBold.ttf') format('truetype');font-weight:600;}
@font-face{font-family:'Be Vietnam Pro';src:url('file:///${ROOT}/assets/fonts/BeVietnamPro-Bold.ttf') format('truetype');font-weight:700;}
@font-face{font-family:'JetBrains Mono';src:url('file:///${ROOT}/assets/fonts/JetBrainsMono-var.ttf') format('truetype');font-weight:100 800;}
`;
const BASE = `
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1920px;height:1080px;overflow:hidden;}
body{background:#F8FAFC;font-family:'Be Vietnam Pro',sans-serif;color:#0F172A;position:relative;}
.safe{position:absolute;inset:54px 96px;}
.tag{font-size:28px;font-weight:600;letter-spacing:2px;}
h1{font-family:'Plus Jakarta Sans';font-weight:800;font-size:56px;line-height:1.2;}
.card{background:#FFFFFF;border-radius:16px;box-shadow:0 2px 8px rgba(15,23,42,0.08);}
.note{font-size:28px;color:#475569;}
`;
const icon = (n, size, color) => `<div style="width:${size}px;height:${size}px;color:${color}">${ICON(n)}</div>`;

const frameIcon = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}${BASE}</style></head><body>
<div class="safe">
  <div class="tag" style="color:#0F766E">06 · ĐỒ HỌA MÁY TÍNH &amp; PHÁT TRIỂN TRÒ CHƠI</div>
  <h1 style="margin-top:12px">Sản phẩm của lĩnh vực</h1>
  <div style="display:flex;gap:32px;margin-top:64px">
    ${[['gamepad-2','Trò chơi điện tử','Game 2D / 3D'],
       ['box','Mô hình 3D','Nhân vật, vật thể'],
       ['clapperboard','Hoạt hình','Phim, chuyển động'],
       ['cog','Mô phỏng kỹ thuật','Huấn luyện, thử nghiệm'],
       ['glasses','Thực tế ảo','VR / AR']]
      .map(([ic, t, s]) => `<div class="card" style="flex:1;height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px">
        ${icon(ic, 96, '#0D9488')}
        <div style="font-size:32px;font-weight:600;text-align:center">${t}</div>
        <div class="note" style="text-align:center">${s}</div></div>`).join('')}
  </div>
  <div class="note" style="position:absolute;bottom:0;left:0">Icon: Lucide (ISC) · nét 2 px trên lưới 24 · một bộ duy nhất toàn video · màu đồ họa #0D9488, chữ #0F172A</div>
</div></body></html>`;

const arrow = (color) => `<svg width="120" height="48" viewBox="0 0 120 48"><line x1="0" y1="24" x2="96" y2="24" stroke="${color}" stroke-width="4"/><polygon points="96,12 120,24 96,36" fill="${color}"/><circle cx="34" cy="24" r="7" fill="${color}"/><circle cx="66" cy="24" r="7" fill="${color}" opacity="0.55"/></svg>`;

const frameDiagram = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}${BASE}</style></head><body>
<div class="safe">
  <div class="tag" style="color:#6D28D9">02 · KHOA HỌC DỮ LIỆU &amp; TRÍ TUỆ NHÂN TẠO</div>
  <h1 style="margin-top:12px">Hệ thống gợi ý sản phẩm</h1>
  <div style="display:flex;align-items:center;gap:28px;margin-top:80px">
    <div class="card" style="width:400px;height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px">
      ${icon('history', 80, '#7C3AED')}<div style="font-size:32px;font-weight:600">Lịch sử xem / mua</div></div>
    ${arrow('#7C3AED')}
    <div class="card" style="width:400px;height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px">
      ${icon('cpu', 80, '#7C3AED')}<div style="font-size:32px;font-weight:600">Mô hình gợi ý</div></div>
    ${arrow('#7C3AED')}
    <div style="display:flex;flex-direction:column;align-items:center;gap:16px">
      <div class="card" style="width:300px;height:420px;border:4px solid #0F172A;border-radius:28px;padding:24px;display:flex;flex-direction:column;gap:16px">
        <div style="height:20px;width:80px;background:#E2E8F0;border-radius:8px;margin:0 auto"></div>
        ${[1,2].map(() => `<div style="flex:1;background:#F5F3FF;border-radius:12px;padding:14px;display:flex;gap:14px;align-items:center">
          <div style="width:64px;height:64px;background:#7C3AED;border-radius:10px;opacity:0.85"></div>
          <div style="flex:1"><div style="height:14px;background:#CBD5E1;border-radius:6px;margin-bottom:10px"></div><div style="height:14px;width:70%;background:#E2E8F0;border-radius:6px"></div></div></div>`).join('')}
        <div style="height:44px;background:#7C3AED;border-radius:10px"></div>
      </div>
      <div style="font-size:32px;font-weight:600">Sản phẩm đề xuất</div>
    </div>
  </div>
  <div class="note" style="position:absolute;bottom:0;left:0">Sơ đồ tự dựng SVG/HTML · dữ liệu một chiều: lịch sử → mô hình → gợi ý · chấm tím = luồng dữ liệu</div>
</div></body></html>`;

const majors = [['1','Công nghệ phần mềm','#2563EB','#FFFFFF'],['2','Khoa học dữ liệu & AI','#7C3AED','#FFFFFF'],['3','An toàn thông tin','#DC2626','#FFFFFF'],['4','Hệ thống thông tin','#D97706','#0F172A'],['5','Mạng & Đám mây','#0369A1','#FFFFFF'],['6','Đồ họa & Game','#0D9488','#0F172A']];
const frameType = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}${BASE}</style></head><body>
<div class="safe">
  <div style="display:flex;gap:64px">
    <div style="width:760px">
      <div class="tag" style="color:#1D4ED8">MỞ ĐẦU · S03</div>
      <h1 style="font-size:48px;margin-top:12px">Mục tiêu bài học</h1>
      <div style="margin-top:40px;display:flex;flex-direction:column;gap:28px">
        ${['Phân biệt được sáu nhóm chuyên ngành CNTT','Kể được vị trí nghề nghiệp tiêu biểu mỗi nhóm','Tự đối chiếu sở thích với từng hướng đi']
          .map(t => `<div style="display:flex;gap:20px;align-items:center">${icon('circle-check', 44, '#15803D')}<div style="font-size:32px;font-weight:500">${t}</div></div>`).join('')}
      </div>
      <div class="card" style="margin-top:48px;padding:28px 32px;display:flex;flex-direction:column;gap:14px">
        <div style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:56px;line-height:1.1">Plus Jakarta Sans 56</div>
        <div style="font-size:32px;font-weight:500">Be Vietnam Pro 32 — nội dung, phụ đề</div>
        <div style="font-family:'JetBrains Mono';font-size:28px">JetBrains Mono 28 — code</div>
      </div>
    </div>
    <div style="flex:1">
      <div class="tag" style="color:#475569">BẢN ĐỒ 6 CHUYÊN NGÀNH</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:36px;margin-top:36px">
        ${majors.map(([n, t, bg, fg]) => `<div style="display:flex;flex-direction:column;align-items:center;gap:16px">
          <div style="width:130px;height:130px;border-radius:50%;background:${bg};color:${fg};display:flex;align-items:center;justify-content:center;font-family:'Plus Jakarta Sans';font-weight:800;font-size:52px">${n}</div>
          <div style="font-size:30px;font-weight:600;text-align:center;line-height:1.3">${t}</div></div>`).join('')}
      </div>
      <div class="note" style="margin-top:36px">Màu nút = màu chuyên ngành; chữ trên nút đã kiểm tra tương phản (04_ArtDirection)</div>
    </div>
  </div>
</div></body></html>`;

const frameMood = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}${BASE}
.bad{background:radial-gradient(circle at 30% 20%, #f0abfc, #7c3aed 45%, #06b6d4 80%);border-radius:60px;box-shadow:0 18px 40px rgba(124,58,237,0.55),0 6px 16px rgba(6,182,212,0.5),inset 0 -14px 30px rgba(0,0,0,0.35),inset 0 14px 24px rgba(255,255,255,0.65);}
</style></head><body>
<div class="safe">
  <h1 style="font-size:48px">Mood board đối chiếu chuẩn 5.6</h1>
  <div style="display:flex;gap:48px;margin-top:48px">
    <div class="card" style="flex:1;padding:40px;border:3px solid #15803D">
      <div class="tag" style="color:#15803D">ĐÚNG — CHUẨN 2.2</div>
      <div style="display:flex;gap:28px;align-items:center;margin-top:36px">
        <div class="card" style="width:220px;height:160px;display:flex;align-items:center;justify-content:center">${icon('monitor', 72, '#2563EB')}</div>
        <div style="display:flex;flex-direction:column;gap:14px">
          <div style="display:flex;gap:12px"><span style="width:44px;height:44px;border-radius:10px;background:#2563EB"></span><span style="width:44px;height:44px;border-radius:10px;background:#0F172A"></span><span style="width:44px;height:44px;border-radius:10px;background:#E2E8F0"></span></div>
          <div style="font-size:30px;font-weight:600">Phẳng 2D, vector sắc nét</div>
        </div>
      </div>
      <div style="margin-top:32px;font-size:28px;line-height:1.5;color:#334155">1 lớp bóng nhẹ ≤ 12% · tối đa 3 màu ngữ nghĩa<br>bo góc nhất quán · line icon một bộ · không glow</div>
    </div>
    <div class="card" style="flex:1;padding:40px;border:3px solid #B91C1C;background:#FFF1F2">
      <div class="tag" style="color:#B91C1C">SAI — KHÔNG DÙNG</div>
      <div style="display:flex;gap:28px;align-items:center;margin-top:36px">
        <div class="bad" style="width:220px;height:160px;display:flex;align-items:center;justify-content:center">
          <div style="width:96px;height:96px;border-radius:50%;background:radial-gradient(circle at 35% 30%, #fef9c3, #facc15 60%, #ca8a04);box-shadow:inset 0 -8px 14px rgba(0,0,0,0.3),0 0 24px 8px rgba(250,204,21,0.8);display:flex;align-items:center;justify-content:center;gap:14px">
            <span style="width:12px;height:16px;border-radius:50%;background:#0F172A"></span><span style="width:12px;height:16px;border-radius:50%;background:#0F172A"></span>
          </div>
        </div>
        <div style="font-size:30px;font-weight:600;color:#B91C1C">Bóng nhựa, gradient cầu vồng,<br>glow tràn lan, chibi</div>
      </div>
      <div style="margin-top:32px;font-size:28px;line-height:1.5;color:#7f1d1d">Nhiều lớp bóng + highlight giả · neon nhiều màu<br>khối phồng bo quá mức · nhân vật trẻ con hóa</div>
    </div>
  </div>
  <div class="note" style="position:absolute;bottom:0;left:0">Ví dụ SAI dựng cố ý để đối chiếu khi duyệt mẫu; không xuất hiện trong video chính thức</div>
</div></body></html>`;

const out = path.join(ROOT, 'mau/frames');
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'frame_icon.html'), frameIcon);
fs.writeFileSync(path.join(out, 'frame_diagram.html'), frameDiagram);
fs.writeFileSync(path.join(out, 'frame_type.html'), frameType);
fs.writeFileSync(path.join(out, 'frame_moodboard.html'), frameMood);
console.log('frames written:', fs.readdirSync(out).join(', '));