/* ============================================================
   UI LAB — THIẾT KẾ MÀU SẮC & HỆ THỐNG NÚT BẤM
   Engine cảnh tất định: renderFrame(t) đặt toàn bộ trạng thái theo t.
   ============================================================ */
(() => {
  const TL = window.__TIMELINE;
  const root = document.getElementById('scenes');
  const captionEl = document.getElementById('caption');
  const captionWrap = document.querySelector('.caption-wrap');
  const fill = document.getElementById('progressFill');
  const plabel = document.getElementById('progressLabel');
  const tcode = document.getElementById('timecode');
  const partChip = document.getElementById('partChip');
  const sweep = document.getElementById('sweep');
  const blobA = document.getElementById('blobA');
  const blobB = document.getElementById('blobB');
  const blobC = document.getElementById('blobC');

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, p) => a + (b - a) * p;
  const ease = (p) => 1 - Math.pow(1 - clamp(p), 3);
  const easeIn = (p) => Math.pow(clamp(p), 3);
  const smooth = (p) => { p = clamp(p); return p * p * (3 - 2 * p); };
  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (s) => `${pad(Math.floor(s / 60))}:${pad(Math.floor(s % 60))}`;

  const PARTS = {
    1: { title: 'Màu sắc', en: 'COLOR SYSTEM' },
    2: { title: 'Hệ thống nút bấm', en: 'BUTTON SYSTEM' }
  };

  /* ---------- icons ---------- */
  const P = {
    palette: '<path d="M12 3a9 9 0 1 0 0 18h1.4a2.2 2.2 0 0 0 1.7-3.6 2.2 2.2 0 0 1 1.7-3.6H19A3.8 3.8 0 0 0 22 10c0-4-4.2-7-10-7z"/><circle cx="7.5" cy="10" r="1"/><circle cx="11" cy="7" r="1"/><circle cx="15.5" cy="8" r="1"/>',
    wheel: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6M5.6 5.6l4.2 4.2M14.2 14.2l4.2 4.2M18.4 5.6l-4.2 4.2M9.8 14.2l-4.2 4.2"/>',
    button: '<rect x="3" y="8" width="18" height="8" rx="4"/><path d="M8 12h8"/>',
    check: '<path d="M20 6L9 17l-5-5"/>',
    alert: '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    type: '<path d="M4 6h16M9 6v13M15 6v7"/>',
    layers: '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 12l10 5 10-5"/><path d="M2 17l10 5 10-5"/>',
    sparkle: '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4L12 3z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/>',
    mouse: '<rect x="7" y="2" width="10" height="20" rx="5"/><path d="M12 6v5"/>',
    scale: '<path d="M4 20V8M4 8l4-4 4 4M20 4v12M20 16l-4 4-4-4M8 8h4M12 16h4"/>',
    radius: '<path d="M4 20V8a4 4 0 0 1 4-4h12"/><path d="M4 14h6v6"/>',
    stack: '<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/>'
  };
  const icon = (name, size = 24, stroke = 1.8) =>
    `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${stroke}" stroke-linecap="round" stroke-linejoin="round">${P[name] || ''}</svg>`;

  /* ---------- DOM ---------- */
  function h(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  const fade = (el, p, dy = 18, dx = 0, sc = 1) => {
    p = clamp(p);
    el.style.opacity = p;
    el.style.transform = `translate(${(1 - p) * dx}px, ${(1 - p) * dy}px) scale(${1 + (1 - p) * (sc - 1)})`;
  };
  const set = (el, key, val) => { el.style[key] = val; };
  let uid = 0;
  const nextId = () => 'u' + (++uid);

  /* ---------- TEACHER ---------- */
  function teacher(opts = {}) {
    const id = nextId();
    const el = h('div', 'teacher ' + (opts.cls || ''));
    if (opts.style) el.style.cssText += opts.style;
    el.innerHTML = `
      <svg viewBox="0 0 300 400" aria-hidden="true">
        <defs>
          <linearGradient id="shirt-${id}" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#3B82F6"/><stop offset="1" stop-color="#2563EB"/>
          </linearGradient>
        </defs>
        <ellipse cx="150" cy="384" rx="88" ry="13" fill="rgba(37,99,235,.13)"/>
        <g class="t-body">
          <rect x="119" y="296" width="24" height="64" rx="12" fill="#1E3A8A"/>
          <rect x="157" y="296" width="24" height="64" rx="12" fill="#1E3A8A"/>
          <ellipse cx="131" cy="366" rx="19" ry="9" fill="#0F172A"/>
          <ellipse cx="169" cy="366" rx="19" ry="9" fill="#0F172A"/>
          <path d="M92 238c0-35 26-64 58-64s58 29 58 64v42c0 27-22 46-58 46s-58-19-58-46z" fill="url(#shirt-${id})"/>
          <path d="M131 180l19 24 19-24" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M98 234c-17 10-26 29-23 49" fill="none" stroke="#2563EB" stroke-width="24" stroke-linecap="round"/>
          <circle cx="74" cy="292" r="15" fill="#FFD8B8"/>
          <g class="t-arm">
            <path d="M202 234c15 11 23 28 20 46" fill="none" stroke="#2563EB" stroke-width="24" stroke-linecap="round"/>
            <circle cx="224" cy="290" r="15" fill="#FFD8B8"/>
            <line x1="227" y1="292" x2="288" y2="212" stroke="#F59E0B" stroke-width="7" stroke-linecap="round"/>
            <circle cx="289" cy="210" r="8" fill="#F59E0B"/>
          </g>
          <circle cx="150" cy="132" r="76" fill="#FFD8B8"/>
          <circle cx="80" cy="140" r="13" fill="#FFC9A3"/>
          <circle cx="220" cy="140" r="13" fill="#FFC9A3"/>
          <path d="M74 122c1-42 35-70 76-70s75 28 76 70c-15-13-29-19-46-19-12 0-20 6-30 6s-18-6-30-6c-17 0-31 6-46 19z" fill="#1F2937"/>
          <path d="M96 96c14-14 32-21 54-21" fill="none" stroke="#374151" stroke-width="6" stroke-linecap="round" opacity=".55"/>
          <rect x="101" y="116" width="41" height="35" rx="11" fill="#FFFFFF" fill-opacity=".32" stroke="#1F2937" stroke-width="4"/>
          <rect x="158" y="116" width="41" height="35" rx="11" fill="#FFFFFF" fill-opacity=".32" stroke="#1F2937" stroke-width="4"/>
          <path d="M142 129h16" stroke="#1F2937" stroke-width="4" stroke-linecap="round"/>
          <g class="t-eye"><circle cx="121" cy="134" r="6" fill="#1F2937"/></g>
          <g class="t-eye"><circle cx="179" cy="134" r="6" fill="#1F2937"/></g>
          <path d="M112 110c5-4 12-4 17-1M171 109c5-3 12-3 17 1" fill="none" stroke="#1F2937" stroke-width="4" stroke-linecap="round" opacity=".7"/>
          <path d="M150 142v10" stroke="#E8A87C" stroke-width="4" stroke-linecap="round"/>
          <path class="t-mouth" d="M132 170c6 10 30 10 36 0" fill="none" stroke="#B45309" stroke-width="4" stroke-linecap="round"/>
          <circle cx="103" cy="157" r="9" fill="#FDA4AF" opacity=".45"/>
          <circle cx="197" cy="157" r="9" fill="#FDA4AF" opacity=".45"/>
        </g>
      </svg>`;
    if (opts.width) el.style.width = opts.width + 'px';
    const bubble = h('div', 'bubble', opts.bubble || '');
    bubble.style.display = opts.bubble ? 'block' : 'none';
    bubble.style.left = (opts.bubbleX ?? 210) + 'px';
    bubble.style.top = (opts.bubbleY ?? 10) + 'px';
    el.appendChild(bubble);
    const body = el.querySelector('.t-body');
    const arm = el.querySelector('.t-arm');
    const eyes = [...el.querySelectorAll('.t-eye')];
    const mouth = el.querySelector('.t-mouth');
    const api = {
      el, bubble,
      update(t, pose = 'point', showBubble = 1) {
        const bob = Math.sin(t * 2.2) * 2.2;
        body.style.transform = `translateY(${bob}px)`;
        const poses = { point: -26, explain: -6, wave: -104, down: 8 };
        arm.style.transform = `rotate(${poses[pose] ?? -26}deg)`;
        const ph = t % 3.8;
        const blink = ph > 3.62 && ph < 3.74 ? 0.12 : 1;
        eyes.forEach((e) => { e.style.transform = `scaleY(${blink})`; });
        mouth.setAttribute('d', pose === 'wave' ? 'M128 168c8 14 36 14 44 0' : 'M132 170c6 10 30 10 36 0');
        bubble.style.opacity = showBubble;
        bubble.style.transform = `translateY(${(1 - showBubble) * 8}px)`;
      }
    };
    return api;
  }

  /* ---------- BROWSER / UI ---------- */
  function browser(body, opts = {}) {
    return `<div class="browser ${opts.cls || ''}">
      <div class="browser-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="url">${opts.url || 'shopxanh.vn'}</span></div>
      <div class="browser-body" style="${opts.bodyStyle || ''}">${body}</div>
    </div>`;
  }

  function shopUI(opts = {}) {
    return `<div class="shop ${opts.theme ? 'theme-' + opts.theme : ''}">
      <div class="shop-nav">
        <div class="shop-logo"><span class="mark"></span><span class="shop-name">SHOP XANH</span></div>
        <div class="shop-links"><span>Trang chủ</span><span>Sản phẩm</span><span>Khuyến mãi</span></div>
        <div class="shop-cart">Giỏ hàng · 2</div>
      </div>
      <div class="shop-body">
        <div class="shop-hero">
          <div class="shop-hero-copy">
            <div class="shop-h">Tai nghe Aurora X</div>
            <div class="shop-p">Chống ồn chủ động, pin 40 giờ, kết nối đa thiết bị.</div>
            <div class="shop-cta-row"><span class="btn btn-amber">Mua ngay</span><span class="btn btn-secondary">Chi tiết</span></div>
          </div>
          <div class="shop-art"><div class="phone"></div><div class="spark"></div></div>
        </div>
        <div class="shop-grid">
          ${[['Aurora Buds', '1.290.000'], ['Nova Watch', '3.490.000'], ['Flux Pad', '2.150.000']].map(([n, p]) => `
            <div class="shop-card"><div class="thumb"></div><div class="name">${n}</div><div class="price">${p} đ</div></div>`).join('')}
        </div>
      </div>
    </div>`;
  }

  function chaosUI() {
    return `<div class="chaos">
      <div class="chaos-nav">
        <div class="chaos-logo">SHOP XANH</div>
        <div class="chaos-links">${['Trang chủ', 'Sản phẩm', 'Sale', 'Liên hệ'].map((x) => `<span>${x}</span>`).join('')}</div>
      </div>
      <div class="chaos-banner">SALE SỐC GIẢM 90% - MUA NGAY!!!</div>
      <div class="chaos-hero">
        <div class="chaos-copy">
          <div class="chaos-h">TAI NGHE AURORA X</div>
          <div class="chaos-p">Sản phẩm mới nhất với nhiều ưu đãi hấp dẫn, chất lượng tuyệt vời, giá rẻ bất ngờ.</div>
          <div class="chaos-btns">
            <span class="chaos-btn" style="background:#DC2626">MUA NGAY</span>
            <span class="chaos-btn" style="background:#16A34A;border-radius:20px">CHI TIẾT</span>
            <span class="chaos-btn" style="background:#9333EA;padding:12px 6px">SALE</span>
            <span class="chaos-btn" style="background:#EA580C;border-radius:0">THÊM VÀO GIỎ</span>
          </div>
        </div>
        <div class="chaos-img"></div>
      </div>
      <div class="chaos-strip">
        <div class="chaos-tile" style="background:#F43F5E"></div>
        <div class="chaos-tile" style="background:#22C55E"></div>
        <div class="chaos-tile" style="background:#3B82F6"></div>
        <div class="chaos-tile" style="background:#EAB308"></div>
      </div>
    </div>`;
  }

  function badShopUI(compact = false) {
    return `<div class="bad-shop" style="height:100%;background:#FFF7ED;font-family:BeVietnam">
      <div style="height:44px;display:flex;align-items:center;gap:10px;padding:0 14px;background:#FDE047;color:#7E22CE">
        <b style="font-family:Quicksand;font-size:16px;color:#C026D3">SHOP XANH</b>
        <span style="font-size:9px;color:#166534">Trang chủ</span><span style="font-size:9px;color:#166534">Sản phẩm</span>
        <span style="margin-left:auto;font-size:9px;background:#A7F3D0;padding:3px 6px">Giỏ hàng</span>
      </div>
      <div style="padding:12px 16px">
        <div style="font-family:Quicksand;font-weight:700;font-size:${compact ? 20 : 25}px;color:#BE185D;line-height:1.05">TAI NGHE AURORA X</div>
        <div style="font-size:${compact ? 9 : 10}px;color:#C7D2FE;margin-top:4px">Sản phẩm mới nhất với nhiều ưu đãi hấp dẫn, chất lượng tuyệt vời.</div>
        <div style="display:flex;gap:6px;margin-top:10px;flex-wrap:wrap">
          <span class="mistake-btn" style="background:#DC2626;height:${compact ? 22 : 26}px;border-radius:2px">MUA NGAY</span>
          <span class="mistake-btn" style="background:#16A34A;height:${compact ? 30 : 36}px;border-radius:20px">CHI TIẾT</span>
          <span class="mistake-btn" style="background:#9333EA;height:${compact ? 20 : 24}px;border-radius:0">SALE</span>
          <span class="mistake-btn" style="background:#EA580C;height:${compact ? 34 : 40}px;border-radius:7px">THÊM VÀO GIỎ</span>
          <span class="mistake-btn" style="background:#0284C7;height:${compact ? 26 : 30}px;border-radius:12px">MUA</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:12px">
          ${[1, 2, 3].map((i) => `<div style="height:${compact ? 52 : 66}px;border-radius:3px;background:${['#FDE047', '#F9A8D4', '#A7F3D0'][i - 1]};border:2px solid #7E22CE"></div>`).join('')}
        </div>
        <div style="font-size:${compact ? 9 : 10}px;color:#CBD5E1;margin-top:8px">Giá chỉ từ 1.290.000đ — miễn phí vận chuyển toàn quốc.</div>
      </div>
    </div>`;
  }

  function shopMiniUI() {
    return `<div class="shop" style="transform:scale(.86);transform-origin:50% 40%">
      <div class="shop-nav" style="height:38px;padding:0 14px"><div class="shop-logo" style="font-size:14px"><span class="mark" style="width:15px;height:15px"></span>SHOP XANH</div><div class="shop-cart" style="font-size:9px;padding:4px 8px">Giỏ hàng · 2</div></div>
      <div class="shop-body" style="padding:10px 14px;gap:8px">
        <div class="shop-hero" style="padding:10px 12px;gap:10px"><div class="shop-hero-copy"><div class="shop-h" style="font-size:16px">Tai nghe Aurora X</div><div class="shop-p" style="font-size:8px">Chống ồn chủ động, pin 40 giờ.</div><div class="shop-cta-row" style="margin-top:6px"><span class="btn btn-amber" style="height:24px;font-size:9px;padding:0 9px">Mua ngay</span></div></div><div class="shop-art" style="width:78px;height:64px"><div class="phone" style="width:28px;height:50px;top:8px"></div></div></div>
        <div class="shop-grid"><div class="shop-card"><div class="thumb" style="height:30px"></div><div class="name" style="font-size:8px">Aurora Buds</div><div class="price" style="font-size:8px">1.290.000 đ</div></div><div class="shop-card"><div class="thumb" style="height:30px"></div><div class="name" style="font-size:8px">Nova Watch</div><div class="price" style="font-size:8px">3.490.000 đ</div></div><div class="shop-card"><div class="thumb" style="height:30px"></div><div class="name" style="font-size:8px">Flux Pad</div><div class="price" style="font-size:8px">2.150.000 đ</div></div></div>
      </div>
    </div>`;
  }

  function words(el, text, cls = 'ch') {
    el.innerHTML = '';
    const spans = [];
    [...text].forEach((ch) => {
      const s = h('span', cls, ch === ' ' ? '&nbsp;' : ch);
      s.style.display = 'inline-block';
      s.style.transform = 'translateY(110%)';
      s.style.opacity = 0;
      el.appendChild(s);
      spans.push(s);
    });
    return spans;
  }

  /* ============================================================
     SCENES
     ============================================================ */
  const B = {};
  const built = [];

  /* ---------- 1. INTRO ---------- */
  B.intro = (cam) => {
    cam.innerHTML = `
      <div class="intro-hero-title">
        <div class="intro-kicker">BÀI GIẢNG UI/UX · 5 PHÚT</div>
        <h1 class="intro-h1"><span class="grad">Màu sắc</span> &amp; <span class="grad2">hệ thống nút bấm</span></h1>
        <div class="intro-sub">Vì sao cùng một website, có bản trông chuyên nghiệp — có bản khiến người dùng rời đi?</div>
      </div>
      <div class="intro-bad">${browser(chaosUI(), { url: 'shopxanh.vn/sale-hot' })}</div>
      <div class="intro-good">${browser(shopUI(), { url: 'shopxanh.vn' })}</div>
      <div class="vs">VS</div>
      <div class="badge-status badge-bad">${icon('alert', 16)} Rối mắt trong 3 giây</div>
      <div class="badge-status badge-good">${icon('check', 16)} Rõ ràng trong 3 giây</div>
      <div class="pillar pillar-1"><div class="picon" style="background:#2563EB">${icon('palette', 22)}</div><div><b>Bảng màu có nguyên tắc</b><span>60 · 30 · 10</span></div></div>
      <div class="pillar pillar-2"><div class="picon" style="background:#F59E0B">${icon('button', 22)}</div><div><b>Hệ thống nút bấm</b><span>nhất quán &amp; đủ trạng thái</span></div></div>`;
    const tr = teacher({ pose: 'point', bubble: 'Vì sao?', bubbleX: 168, bubbleY: -34, width: 214, style: 'left:42px;top:598px;' });
    cam.appendChild(tr.el);
    const bad = cam.querySelector('.intro-bad');
    const good = cam.querySelector('.intro-good');
    const badges = [...cam.querySelectorAll('.badge-status')];
    const pillars = [...cam.querySelectorAll('.pillar')];
    const title = cam.querySelector('.intro-h1');
    const sub = cam.querySelector('.intro-sub');
    const tSpan = words(title, 'Màu sắc & hệ thống nút bấm');
    const vs = cam.querySelector('.vs');

    return {
      update(U) {
        const t = U.t;
        const glitch = t < 3.2 ? Math.sin(t * 47) * 2.2 : 0;
        bad.style.transform = `rotate(-2.2deg) translate(${glitch}px,${Math.cos(t * 31) * 1.6}px)`;
        bad.style.opacity = 1 - 0.25 * U.p(1, 0, 0.6);
        const reveal = U.p(1, 0.25, 1.2);
        good.style.clipPath = `inset(0 0 0 ${(1 - reveal) * 100}%)`;
        good.style.transform = `translateX(${(1 - reveal) * 120}px) rotate(1.2deg)`;
        good.style.opacity = reveal;
        vs.style.opacity = U.p(1, 0.25, 0.5);
        vs.style.transform = `scale(${0.6 + 0.4 * U.p(1, 0.25, 0.5)}) rotate(${-8 + 8 * U.p(1, 0.25, 0.5)}deg)`;
        badges.forEach((b, i) => { fade(b, U.p(1, 0.2 + i * 0.2, 0.5), 10); });
        pillars.forEach((p, i) => { fade(p, U.p(2, 0.1 + i * 0.18, 0.55), 20); });
        const pt = U.p(2, 0.05, 0.7);
        sub.style.opacity = pt;
        sub.style.transform = `translateY(${(1 - pt) * 14}px)`;
        tSpan.forEach((s, i) => {
          const p = ease(clamp((U.p(0, 0.25, 1.0) * 26 - i) / 2.4));
          s.style.transform = `translateY(${(1 - p) * 110}%)`;
          s.style.opacity = p;
        });
        const tl = U.p(0, 0, 0.9);
        cam.querySelector('.intro-kicker').style.opacity = tl;
        tSpan.forEach((s) => { s.style.filter = 'none'; });
        tSpan.forEach((s, i) => {
          s.style.color = i < 7 ? 'var(--blue)' : i > 9 ? 'var(--amber)' : 'inherit';
        });
        const bubble = U.p(0, 0.25, 0.4) * (1 - U.p(0, 3.4, 0.7));
        tr.update(t, 'point', bubble);
        tr.bubble.textContent = 'Vì sao?';
      }
    };
  };

  /* ---------- 2. GOALS ---------- */
  B.goals = (cam) => {
    const cards = [
      { n: '01', t: 'Phối màu 60–30–10', d: 'Nền 60, màu phụ 30, màu nhấn 10. Tỷ lệ định hướng cho cảm nhận thị giác.', art: `<div style="position:absolute;left:24px;top:26px;width:116px;height:116px;border-radius:50%;background:conic-gradient(#BFDBFE 0 60%,#2563EB 60% 90%,#F59E0B 90% 100%)"></div><div style="position:absolute;left:40px;top:42px;width:84px;height:84px;border-radius:50%;background:#fff"></div><div style="position:absolute;left:162px;top:30px;font-family:Jakarta;font-weight:800;font-size:24px;color:#2563EB">60<span style="font-size:13px">%</span></div><div style="position:absolute;left:162px;top:64px;font-family:Jakarta;font-weight:800;font-size:19px;color:#1E40AF">30<span style="font-size:11px">%</span></div><div style="position:absolute;left:162px;top:94px;font-family:Jakarta;font-weight:800;font-size:15px;color:#B45309">10<span style="font-size:10px">%</span></div>` },
      { n: '02', t: 'Chọn màu theo mục đích', d: 'Giáo dục, thương mại điện tử hay công nghệ — mỗi ngành một bảng màu riêng.', art: `<div style="position:absolute;left:28px;top:30px;display:flex;gap:8px">${['#2563EB', '#06B6D4', '#8B5CF6', '#F59E0B', '#10B981'].map((c, i) => `<span style="width:34px;height:76px;border-radius:8px;background:${c};opacity:${0.45 + i * 0.11}"></span>`).join('')}</div><div style="position:absolute;left:28px;top:118px;display:flex;gap:6px">${['MONO', 'ANALOG', 'COMP'].map((x) => `<span style="font-family:Jakarta;font-size:8px;font-weight:800;letter-spacing:.08em;color:#64748B;border:1px solid #DCE9F7;border-radius:6px;padding:3px 6px">${x}</span>`).join('')}</div>` },
      { n: '03', t: 'Chuẩn hóa nút bấm', d: 'Cùng chiều cao, bo góc, font — và đủ 6 trạng thái tương tác.', art: `<div style="position:absolute;left:28px;top:26px;display:flex;gap:7px;align-items:center"><span class="btn btn-primary" style="height:38px;font-size:10px;padding:0 12px">Thêm vào giỏ</span><span class="btn btn-outline" style="height:38px;font-size:10px;padding:0 12px">So sánh</span></div><div style="position:absolute;left:28px;top:76px;display:flex;gap:6px">${['Default', 'Hover', 'Active', 'Focus', 'Disabled', 'Loading'].map((x) => `<span style="font-family:Jakarta;font-size:7px;font-weight:800;color:#64748B;background:#fff;border:1px solid #DCE9F7;border-radius:5px;padding:3px 5px">${x}</span>`).join('')}</div>` }
    ];
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">LỘ TRÌNH BÀI HỌC</div><h1 class="scene-title">Ba bước để giao diện <span class="accent">có hệ thống</span></h1></div>
      ${cards.map((c, i) => `<div class="card goal-card" style="left:${96 + i * 476}px;top:250px">
        <div class="card-kicker"><span class="idx">${c.n}</span> BƯỚC ${i + 1}</div>
        <h3>${c.t}</h3><p>${c.d}</p><div class="goal-art">${c.art}</div>
      </div>`).join('')}
      <div class="goal-shop-tag" data-shop-tag style="opacity:0">${icon('check', 16)} Shop Xanh · sau 3 bước</div>
      <div class="card goal-shop" style="overflow:hidden">${browser(shopMiniUI(), { url: 'shopxanh.vn', bodyStyle: 'height:100%' })}</div>`;
    const tr = teacher({ pose: 'explain', width: 212, style: 'left:1620px;top:104px;' });
    cam.appendChild(tr.el);
    const cardsEl = [...cam.querySelectorAll('.goal-card')];
    const shop = cam.querySelector('.goal-shop');
    const shopTag = cam.querySelector('[data-shop-tag]');
    return {
      update(U) {
        cardsEl.forEach((c, i) => fade(c, U.p(0, 0.1 + i * 0.5, 0.6), 34, 0, 0.97));
        const sp = U.p(1, 0.1, 0.7);
        fade(shop, sp, 26, 20, 0.96);
        fade(shopTag, sp, 14, 20);
        tr.update(U.t, 'explain');
      }
    };
  };

  /* ---------- 3. DIVIDER ---------- */
  B.divider = (cam, def) => {
    const isPurple = def.part === 2;
    cam.innerHTML = `
      <div class="divider-plane ${isPurple ? 'purple' : 'blue'}">
        <div class="divider-num">${pad(def.part || 1)}</div>
        <div class="divider-center">
          <div class="divider-kicker">PHẦN ${pad(def.part || 1)} · ${isPurple ? 'BUTTON SYSTEM' : 'COLOR SYSTEM'}</div>
          <div class="divider-title">${def.title}</div>
          <div class="divider-sub">${isPurple ? 'Từ thông số đến trạng thái — một hệ thống duy nhất.' : 'Từ bánh xe màu đến bảng màu có nguyên tắc.'}</div>
        </div>
        <div class="divider-chips">${(isPurple ? ['48px', '8px', '16px · 600', 'Hover', 'Active', 'Focus', 'Loading'] : ['60%', '30%', '10%', 'Monochromatic', 'Analogous', 'Complementary']).map((x) => `<span class="divider-chip">${x}</span>`).join('')}</div>
      </div>`;
    const title = cam.querySelector('.divider-title');
    const kicker = cam.querySelector('.divider-kicker');
    const sub = cam.querySelector('.divider-sub');
    const num = cam.querySelector('.divider-num');
    const chips = [...cam.querySelectorAll('.divider-chip')];
    return {
      update(U) {
        const p = U.p(0, 0.05, 0.6);
        title.style.opacity = p;
        title.style.transform = `translateY(${(1 - p) * 26}px)`;
        kicker.style.opacity = p;
        sub.style.opacity = p * 0.92;
        sub.style.transform = `translateY(${(1 - p) * 16}px)`;
        num.style.opacity = p * 0.95;
        num.style.transform = `scale(${0.92 + p * 0.08})`;
        chips.forEach((c, i) => { fade(c, U.p(0, 0.15 + i * 0.08, 0.4), 12); });
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === def.id).dur;
        const p = clamp(local / d);
        return `scale(${1 + p * 0.11}) translateY(${-p * 14}px)`;
      }
    };
  };

  /* ---------- 4. WHY ---------- */
  B.why = (cam) => {
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 01 · MÀU SẮC</div><h1 class="scene-title">Màu sắc làm <span class="accent">ba việc</span> cùng lúc</h1></div>
      <div class="why-tabs">
        <div class="why-tab" data-k="0"><span class="n">1</span> Tạo phân cấp thông tin</div>
        <div class="why-tab" data-k="1"><span class="n">2</span> Nhận diện thương hiệu</div>
        <div class="why-tab" data-k="2"><span class="n">3</span> Hướng sự chú ý</div>
      </div>
      <div class="why-stage">${browser(shopUI(), { url: 'shopxanh.vn', cls: 'why-browser', bodyStyle: 'height:100%' })}
        <div class="why-layer" data-l="0">
          <div class="why-dim"></div>
          <div class="why-note" style="left:46px;top:64px;border-left:4px solid #2563EB">H1 · Tiêu đề · 32px</div>
          <div class="why-note" style="left:46px;top:150px;border-left:4px solid #64748B">Body · Nội dung · 16px</div>
          <div class="why-note" style="left:46px;top:206px;border-left:4px solid #F59E0B">CTA · Hành động</div>
          <div style="position:absolute;left:230px;top:78px;width:170px;height:2px;background:#2563EB"></div>
          <div style="position:absolute;left:230px;top:164px;width:130px;height:2px;background:#64748B"></div>
          <div style="position:absolute;left:230px;top:220px;width:90px;height:2px;background:#F59E0B"></div>
        </div>
        <div class="why-layer" data-l="1">
          <div class="why-dim" style="opacity:.55"></div>
          <div class="why-brand-name">THƯƠNG HIỆU</div>
          <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#fff;border-radius:16px;padding:18px 22px;box-shadow:0 18px 44px rgba(15,23,42,.18);display:flex;gap:18px;align-items:center">
            <div id="brandDots" style="display:flex;gap:8px"></div><div style="width:1px;height:44px;background:#E2EFFB"></div>
            <div><div id="brandName" style="font-family:Quicksand;font-weight:700;font-size:22px;color:#1E293B">TechBlue</div><div id="brandFont" style="font-size:12px;color:#64748B">Quicksand · 700</div></div>
          </div>
        </div>
        <div class="why-layer" data-l="2">
          <div class="why-spot" id="spot"></div>
          <div class="why-note" style="left:24%;top:54%">${icon('eye', 16)} Mắt đi theo màu nhấn</div>
        </div>
      </div>`;
    const tabs = [...cam.querySelectorAll('.why-tab')];
    const layers = [...cam.querySelectorAll('.why-layer')];
    const shop = cam.querySelector('.shop');
    const brandDots = cam.querySelector('#brandDots');
    const brandName = cam.querySelector('#brandName');
    const brandFont = cam.querySelector('#brandFont');
    const spot = cam.querySelector('#spot');
    const brands = [
      { name: 'TechBlue', font: 'Quicksand · 700', colors: ['#2563EB', '#06B6D4', '#F59E0B'], cls: 'theme-tech' },
      { name: 'Organic', font: 'Be Vietnam Pro · 600', colors: ['#15803D', '#84CC16', '#F59E0B'], cls: 'theme-organic' },
      { name: 'Luxury', font: 'Jakarta · 700', colors: ['#0F172A', '#B45309', '#E2E8F0'], cls: 'theme-luxury' }
    ];
    let lastBrand = -1;

    return {
      update(U) {
        const k = U.t < U.cueStart(1) ? 0 : U.t < U.cueStart(2) ? 1 : 2;
        tabs.forEach((tab, i) => tab.classList.toggle('on', i === k));
        layers.forEach((l, i) => { l.style.opacity = i === k ? 1 : 0; });
        const lp = U.p(k, 0.05, 0.5);
        layers[k].style.transform = `translateY(${(1 - lp) * 12}px)`;
        if (k === 1) {
          const p = U.p(1, 0.1, 1.4);
          const bi = Math.min(2, Math.floor(p * 3));
          if (bi !== lastBrand) {
            lastBrand = bi;
            const b = brands[bi];
            shop.classList.remove('theme-tech', 'theme-organic', 'theme-luxury');
            shop.classList.add(b.cls);
            brandName.textContent = b.name;
            brandFont.textContent = b.font;
            brandDots.innerHTML = b.colors.map((c) => `<span style="width:28px;height:28px;border-radius:8px;background:${c};box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)"></span>`).join('');
          }
        }
        if (k === 2) {
          const p = U.p(2, 0.2, 1.1);
          const x = lerp(62, 12, smooth(p));
          spot.style.background = `radial-gradient(270px 205px at ${x}% 38%, rgba(15,23,42,0) 0%, rgba(15,23,42,0) 34%, rgba(15,23,42,.58) 84%)`;
        }
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'why').dur;
        const p = clamp(local / d);
        return `scale(${1.01 + p * 0.02})`;
      }
    };
  };

  /* ---------- 5. RULE 60-30-10 ---------- */
  B.rule = (cam) => {
    const C = 2 * Math.PI * 150;
    const arcs = [
      { len: C * 0.6, color: '#BFDBFE', rot: -90, w: 34 },
      { len: C * 0.3, color: '#2563EB', rot: -90 + 216, w: 34 },
      { len: C * 0.1, color: '#F59E0B', rot: -90 + 324, w: 34 }
    ];
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 01 · MÀU SẮC</div><h1 class="scene-title">Quy tắc <span class="accent">60–30–10</span></h1><svg class="scribble" viewBox="0 0 300 16"><path d="M4 10C64 3 150 3 208 7c30 2 58 4 88 1"/></svg></div>
      <div class="board">
        <div class="board-tape"></div>
        <div class="board-title">Công thức màu cho <span>Shop Xanh</span></div>
        <div class="rule-donut">
          <svg viewBox="0 0 420 420" width="420" height="420">
            <circle cx="210" cy="210" r="150" fill="none" stroke="#F1F5F9" stroke-width="34"/>
            ${arcs.map((a, i) => `<circle class="arc" data-a="${i}" cx="210" cy="210" r="150" fill="none" stroke="${a.color}" stroke-width="${a.w}" stroke-linecap="butt" stroke-dasharray="${a.len} ${C - a.len}" stroke-dashoffset="${a.len}" transform="rotate(${a.rot} 210 210)"/>`).join('')}
            <circle cx="210" cy="210" r="112" fill="#FFFDF8"/>
            <text x="210" y="198" text-anchor="middle" font-family="Jakarta" font-weight="800" font-size="44" fill="#1E293B">60·30·10</text>
            <text x="210" y="228" text-anchor="middle" font-family="BeVietnam" font-weight="600" font-size="14" fill="#64748B">tỷ lệ định hướng</text>
          </svg>
        </div>
        <div class="rule-legend">
          <div class="rule-leg" data-l="1"><span class="swatch" style="background:#EAF6FF;width:30px;height:30px;box-shadow:inset 0 0 0 2px #BFDBFE"></span><b style="color:#1D4ED8">60%</b><span>Nền &amp; vùng chính</span></div>
          <div class="rule-leg" data-l="2"><span class="swatch" style="background:#2563EB;width:30px;height:30px"></span><b style="color:#2563EB">30%</b><span>Màu phụ, phân khu</span></div>
          <div class="rule-leg" data-l="3"><span class="swatch" style="background:#F59E0B;width:30px;height:30px"></span><b style="color:#B45309">10%</b><span>Nhấn, CTA</span></div>
        </div>
        <div class="rule-note">${icon('sparkle', 18)} <b>Lưu ý:</b> tỷ lệ cảm nhận — không phải đo từng pixel.</div>
      </div>
      <div class="rule-browser">
        <div class="rm-frame">
          <div class="rm-nav">
            <span class="rm-logo"></span>
            <span class="rm-links"><i></i><i></i><i></i></span>
            <span class="rm-cart"></span>
          </div>
          <div class="rm-hero">
            <div class="rm-copy">
              <div class="rm-h"></div>
              <div class="rm-p"></div>
              <div class="rm-p short"></div>
              <div class="rm-cta-row"><span class="rm-cta">Mua ngay</span><span class="rm-tag10" data-l10><b data-n="10">0</b>% NHẤN</span></div>
            </div>
            <div class="rm-art"><div class="rm-phone"></div><div class="rm-spark"></div></div>
          </div>
          <div class="rm-grid"><i></i><i></i><i></i></div>
          <div class="rm-zone" data-z="60"></div>
          <div class="rm-zone" data-z="30"></div>
          <div class="rm-zone" data-z="10"></div>
        </div>
        <div class="zone-label l60" data-pl="60" style="left:22px;top:-46px;color:#1D4ED8"><b data-n="60">0</b>% <small>NỀN</small></div>
        <div class="zone-label l30" data-pl="30" style="right:22px;top:-46px;color:#1D4ED8"><b data-n="30">0</b>% <small>PHỤ</small></div>
      </div>`;
    const tr = teacher({ pose: 'point', width: 186, style: 'left:54px;top:656px;z-index:10;' });
    cam.appendChild(tr.el);
    const arcEls = [...cam.querySelectorAll('.arc')];
    const legs = [...cam.querySelectorAll('.rule-leg')];
    const zones = [...cam.querySelectorAll('.rm-zone')];
    const labels = [...cam.querySelectorAll('.zone-label')];
    const numEls = [...cam.querySelectorAll('[data-n]')];
    const tag10 = cam.querySelector('[data-l10]');
    const note = cam.querySelector('.rule-note');
    const scrib = cam.querySelector('.scribble path');

    const counter = (el, from, to, p) => { el.textContent = Math.round(lerp(from, to, clamp(p))); };

    return {
      update(U) {
        const p1 = U.p(0, 0.25, 1.1);
        arcEls.forEach((a, i) => {
          const seq = [U.p(0, 0.25, 0.6), U.p(1, 0.15, 0.55), U.p(2, 0.15, 0.5)][i];
          a.style.strokeDashoffset = a.getAttribute('stroke-dasharray').split(' ')[0] * (1 - seq);
          a.style.opacity = i === 0 ? 1 : (seq > 0.01 ? 1 : 0);
        });
        legs.forEach((l, i) => fade(l, U.p(i, 0.1, 0.5), 12, 10));
        zones.forEach((z) => { z.style.opacity = 0; });
        labels.forEach((l) => { l.style.opacity = 0; });
        tag10.style.opacity = 0;
        const p60 = U.p(1, 0.15, 0.7);
        zones.find((z) => z.dataset.z === '60').style.opacity = p60 * 0.95;
        labels.find((l) => l.dataset.pl === '60').style.opacity = p60;
        counter(numEls.find((n) => n.dataset.n === '60'), 0, 60, p60);
        const p30 = U.p(2, 0.15, 0.7);
        zones.find((z) => z.dataset.z === '30').style.opacity = p30;
        labels.find((l) => l.dataset.pl === '30').style.opacity = p30;
        counter(numEls.find((n) => n.dataset.n === '30'), 0, 30, p30);
        const p10 = U.p(3, 0.15, 0.7);
        zones.find((z) => z.dataset.z === '10').style.opacity = p10;
        tag10.style.opacity = p10;
        tag10.style.transform = `translateX(${(1 - p10) * -8}px)`;
        counter(numEls.find((n) => n.dataset.n === '10'), 0, 10, p10);
        const pn = U.p(4, 0.05, 0.6);
        fade(note, pn, 8);
        scrib.style.strokeDashoffset = 100 * (1 - U.p(0, 0.2, 0.9));
        legPulse(legs, U);
        tr.update(U.t, 'point');
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'rule').dur;
        const p = clamp(local / d);
        return `scale(${1 + p * 0.025}) translateX(${-p * 10}px)`;
      }
    };
    function legPulse(legs, U) {
      legs.forEach((l, i) => {
        const active = U.t >= U.cueStart(i + 1) && (i === 2 || U.t < U.cueStart(i + 2));
        l.style.borderColor = active ? '#93C5FD' : '#ECE5D8';
        l.style.background = active ? '#F0F9FF' : '#fff';
        l.style.transform = `translateX(${active ? -4 : 0}px)`;
      });
    }
  };

  /* ---------- 6. WHEEL ---------- */
  B.wheel = (cam) => {
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 01 · MÀU SẮC</div><h1 class="scene-title">Xây bảng màu từ <span class="accent">bánh xe màu</span></h1></div>
      <div class="wheel-wrap">
        <div class="wheel"></div>
        <div class="wheel-hole"><b>COLOR</b><span>WHEEL</span></div>
        <div class="wheel-needle" id="needle"></div>
        <svg class="wheel-svg" viewBox="0 0 600 600">
          <g id="mono" opacity="0">${[0, 1, 2].map((i) => `<circle cx="300" cy="300" r="${238 - i * 9}" fill="none" stroke="${['#BFDBFE', '#3B82F6', '#1E3A8A'][i]}" stroke-width="7" stroke-dasharray="70 1495" stroke-dashoffset="${-60}"/>`).join('')}</g>
          <g id="analog" opacity="0"><path d="M300 62 A238 238 0 0 1 506 181" fill="none" stroke="#06B6D4" stroke-width="10" stroke-linecap="round" stroke-dasharray="300" stroke-dashoffset="300"/></g>
          <g id="comp" opacity="0"><line x1="146" y1="454" x2="454" y2="146" stroke="#F59E0B" stroke-width="8" stroke-linecap="round"/><circle cx="180" cy="420" r="16" fill="#F59E0B"/><circle cx="420" cy="180" r="16" fill="#3B82F6"/></g>
        </svg>
      </div>
      <div class="card scheme-card" data-s="0" style="top:248px"><div class="scheme-swatches">${['#1E3A8A', '#3B82F6', '#BFDBFE'].map((c) => `<span style="background:${c}"></span>`).join('')}</div><div><h4>Monochromatic · Đơn sắc</h4><p>Các sắc độ của cùng một màu — an toàn, đồng bộ.</p></div></div>
      <div class="card scheme-card" data-s="1" style="top:396px"><div class="scheme-swatches">${['#06B6D4', '#3B82F6', '#8B5CF6'].map((c) => `<span style="background:${c}"></span>`).join('')}</div><div><h4>Analogous · Tương đồng</h4><p>Ba màu nằm cạnh nhau — hài hòa, có chiều sâu.</p></div></div>
      <div class="card scheme-card" data-s="2" style="top:544px"><div class="scheme-swatches">${['#F59E0B', '#2563EB', '#1D4ED8'].map((c) => `<span style="background:${c}"></span>`).join('')}</div><div><h4>Complementary · Bổ sung</h4><p>Hai màu đối diện — tương phản mạnh, cần tiết chế.</p></div></div>
      <div class="industry-row">
        ${[
          { n: 'Giáo dục', nav: '#2563EB', btn: '#10B981', dots: ['#2563EB', '#FFFFFF', '#10B981'] },
          { n: 'TMĐT', nav: '#334155', btn: '#F59E0B', dots: ['#F8FAFC', '#F59E0B', '#334155'] },
          { n: 'Công nghệ', nav: '#1E3A8A', btn: '#06B6D4', dots: ['#2563EB', '#06B6D4', '#8B5CF6'] }
        ].map((x, i) => `<div class="card industry" data-i="${i}"><div class="mini-nav" style="background:${x.nav}">${x.n}</div><div class="mini-body"><div class="mini-h">${x.n === 'Giáo dục' ? 'Học liệu số' : x.n === 'TMĐT' ? 'Deal hôm nay' : 'Giải pháp cloud'}</div><div class="mini-line" style="width:78%"></div><div class="mini-line" style="width:58%"></div><span class="mini-btn" style="background:${x.btn}">Khám phá</span><div class="mini-dots">${x.dots.map((c) => `<span style="background:${c};box-shadow:inset 0 0 0 1px #E2E8F0"></span>`).join('')}</div></div></div>`).join('')}
      </div>`;
    const needle = cam.querySelector('#needle');
    const cards = [...cam.querySelectorAll('.scheme-card')];
    const inds = [...cam.querySelectorAll('.industry')];
    const mono = cam.querySelector('#mono');
    const analog = cam.querySelector('#analog');
    const comp = cam.querySelector('#comp');
    const analogPath = analog.querySelector('path');
    return {
      update(U) {
        needle.style.transform = `rotate(${U.t * 4 + 120}deg)`;
        cards.forEach((c, i) => fade(c, U.p(i, 0.05, 0.55), 14, 18));
        mono.style.opacity = U.p(0, 0.1, 0.5);
        analog.style.opacity = U.p(0, 0.45, 0.5);
        if (analogPath) analogPath.style.strokeDashoffset = 300 * (1 - U.p(0, 0.45, 0.5));
        comp.style.opacity = U.p(1, 0.1, 0.5);
        inds.forEach((x, i) => fade(x, U.p(2, 0.15 + i * 0.16, 0.5), 20, 0, 0.96));
        cards.forEach((c, i) => {
          c.style.borderColor = U.t >= U.cueStart(i) ? 'rgba(37,99,235,.42)' : '#D8E7F6';
          c.style.boxShadow = U.t >= U.cueStart(i) ? '0 18px 40px rgba(37,99,235,.16)' : 'var(--shadow)';
        });
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'wheel').dur;
        const p = clamp(local / d);
        return `scale(${1.01 + p * 0.02}) rotate(${p * 0.3}deg)`;
      }
    };
  };

  /* ---------- 7. ANATOMY ---------- */
  B.anatomy = (cam) => {
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 02 · NÚT BẤM</div><h1 class="scene-title">Giải phẫu một <span class="accent">nút bấm</span></h1><svg class="scribble" viewBox="0 0 300 16"><path d="M4 10C64 3 150 3 208 7c30 2 58 4 88 1"/></svg></div>
      <div class="anatomy-stage">
        <div class="grid-paper"></div>
        <div class="btn-layer" data-layer style="opacity:0"></div>
        <div class="giant-btn" data-btn><span class="btn btn-primary">Thêm vào giỏ</span></div>
        <div class="dim-v" data-dim style="opacity:0"></div>
        <div class="dim-h" data-dimh style="opacity:0"></div>
        <div class="spec" data-spec="0" style="left:110px;top:262px">${icon('scale', 16)} Cao <b>40–48px</b></div>
        <div class="spec" data-spec="1" style="right:40px;top:150px">${icon('mouse', 16)} Vùng chạm <b>44px+</b></div>
        <div class="spec" data-spec="2" style="left:210px;top:404px">${icon('radius', 16)} Bo góc <b>8px</b></div>
        <div class="spec" data-spec="3" style="left:470px;top:120px">${icon('type', 16)} <b>Be Vietnam Pro</b> · 16px · 600</div>
        <div class="spec" data-spec="4" style="left:430px;top:474px">${icon('stack', 16)} Padding ngang <b>24px</b></div>
        <div class="spec" data-spec="5" style="right:52px;top:430px">${icon('layers', 16)} Bội số <b>8 · 12 · 16</b></div>
        <div class="radius-row" data-radii style="opacity:0">
          <div class="radius-sample" style="border-radius:6px"><span>6px</span></div>
          <div class="radius-sample" style="border-radius:8px;background:#DBEAFE"><span>8px</span></div>
          <div class="radius-sample bad" style="border-radius:12px"><span>12px</span></div>
        </div>
      </div>`;
    const tr = teacher({ pose: 'point', width: 196, style: 'left:70px;top:664px;z-index:9;' });
    cam.appendChild(tr.el);
    const btn = cam.querySelector('[data-btn]');
    const layer = cam.querySelector('[data-layer]');
    const dims = [...cam.querySelectorAll('[data-dim],[data-dimh]')];
    const specs = [...cam.querySelectorAll('[data-spec]')];
    const radii = cam.querySelector('[data-radii]');
    const pressed = cam.querySelector('.giant-btn .btn');
    const scrib = cam.querySelector('.scribble path');
    return {
      update(U) {
        const p0 = U.p(0, 0.1, 0.6);
        btn.style.opacity = p0;
        btn.style.transform = `translateX(-50%) translateY(${(1 - p0) * 22}px) scale(${0.94 + p0 * 0.06})`;
        layer.style.opacity = p0 * 0.8;
        layer.style.transform = `translateX(-50%) translateY(${18 + p0 * 10}px) scale(${0.96 + p0 * 0.04})`;
        dims.forEach((d, i) => { d.style.opacity = U.p(1 + (i > 0 ? 0 : 0), 0.05, 0.5); });
        specs.forEach((s, i) => {
          const cue = i === 0 ? 1 : i === 1 ? 1 : i === 2 || i === 3 ? 2 : 3;
          fade(s, U.p(cue, 0.1 + (i % 2) * 0.12, 0.5), 10, i % 2 ? 10 : -10);
        });
        const pr = U.p(2, 0.3, 0.6);
        radii.style.opacity = pr;
        radii.style.transform = `translateY(${(1 - pr) * 12}px)`;
        const lock = U.p(2, 0.7, 0.5);
        pressed.style.boxShadow = `0 20px 40px rgba(37,99,235,${0.24 + lock * 0.1})`;
        pressed.style.transform = `translateY(${lock * 2}px)`;
        scrib.style.strokeDashoffset = 100 * (1 - U.p(0, 0.2, 0.9));
        tr.update(U.t, 'point');
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'anatomy').dur;
        const p = clamp(local / d);
        return `scale(${1.02 + p * 0.015}) translateX(${p * 8}px)`;
      }
    };
  };

  /* ---------- 8. TYPES ---------- */
  B.types = (cam) => {
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 02 · NÚT BẤM</div><h1 class="scene-title">Bốn loại nút, <span class="accent">bốn vai trò</span></h1></div>
      <div class="type-roles">
        <div class="type-role" data-r="0"><span class="dot" style="background:#2563EB"></span><div><b>Primary</b><span>Hành động chính</span></div></div>
        <div class="type-role" data-r="1"><span class="dot" style="background:#06B6D4"></span><div><b>Secondary</b><span>Hành động phụ</span></div></div>
        <div class="type-role" data-r="2"><span class="dot" style="background:#94A3B8"></span><div><b>Outline</b><span>Lựa chọn nhẹ</span></div></div>
        <div class="type-role" data-r="3"><span class="dot" style="background:#EF4444"></span><div><b>Danger</b><span>Thao tác nguy hiểm</span></div></div>
      </div>
      <div class="types-page">${browser(`
      <div class="shop" style="min-height:100%">
        <div class="shop-nav"><div class="shop-logo"><span class="mark"></span>SHOP XANH</div><div class="shop-links"><span>Sản phẩm</span><span>Tai nghe</span></div><div class="shop-cart">Giỏ hàng · 2</div></div>
        <div class="product-hero">
          <div class="product-art"><div class="ph"></div></div>
          <div class="product-info">
            <h3>Tai nghe Aurora X</h3>
            <div class="price">1.290.000 đ</div>
            <p>Chống ồn chủ động · Pin 40 giờ · Kết nối đa thiết bị · Bảo hành 24 tháng.</p>
            <div class="product-actions">
              <span class="btn btn-primary" data-b="0">Thêm vào giỏ</span>
              <span class="btn btn-secondary" data-b="1">Mua sau</span>
              <span class="btn btn-outline" data-b="2">So sánh</span>
            </div>
          </div>
        </div>
        <div class="cart-row"><div class="thumb"></div><div><div class="nm">Aurora Buds</div><div class="pr">1.290.000 đ</div></div><span class="btn btn-danger btn-sm" data-b="3">Xóa</span></div>
        <div class="cart-row"><div class="thumb" style="background:#E0F2FE"></div><div><div class="nm">Nova Watch</div><div class="pr">3.490.000 đ</div></div><span class="btn btn-danger btn-sm">Xóa</span></div>
        <div class="cart-row"><div class="thumb" style="background:#EDE9FE"></div><div><div class="nm">Flux Pad</div><div class="pr">2.150.000 đ</div></div><span class="btn btn-danger btn-sm">Xóa</span></div>
      </div>`, { url: 'shopxanh.vn/aurora-x' })}</div>`;
    const roles = [...cam.querySelectorAll('.type-role')];
    const btns = [...cam.querySelectorAll('[data-b]')];
    const cursor = h('div', 'cursor', `<svg viewBox="0 0 34 42" width="34" height="42"><path d="M4 2l24 18-11 2-5 12z" fill="#1E293B" stroke="#fff" stroke-width="2"/></svg>`);
    cam.appendChild(cursor);
    return {
      update(U) {
        const t = U.t;
        const t0 = U.cueStart(0);
        roles.forEach((r, i) => {
          const on = t > t0 + 8.4 || (t >= t0 + i * 2.1 && (i === 3 || t < t0 + (i + 1) * 2.1));
          r.classList.toggle('on', on);
          r.style.borderColor = on ? 'rgba(37,99,235,.42)' : '#DCE9F7';
        });
        const seq = clamp((t - U.cueStart(0)) / 8.4);
        const idx = Math.min(3, Math.floor(seq * 4));
        const pts = [{ x: 980, y: 484 }, { x: 1136, y: 484 }, { x: 1272, y: 484 }, { x: 1738, y: 646 }];
        const p = pts[idx];
        cursor.style.left = p.x + 'px';
        cursor.style.top = p.y + 'px';
        cursor.style.opacity = t < t0 + 8.6 ? 0.95 : 0;
        btns.forEach((b, i) => {
          const k = idx === i;
          b.style.transform = k ? 'translateY(2px) scale(.98)' : 'none';
          b.style.filter = idx > i && idx !== 3 ? 'none' : (k ? 'brightness(.92)' : 'none');
        });
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'types').dur;
        const p = clamp(local / d);
        return `scale(${1.01 + p * 0.02}) translateX(${p * -6}px)`;
      }
    };
  };

  /* ---------- 9. STATES ---------- */
  B.states = (cam) => {
    const states = ['DEFAULT', 'HOVER', 'ACTIVE', 'FOCUS', 'DISABLED', 'LOADING'];
    const samples = [
      '<span class="state-sample" style="background:#2563EB;color:#fff">Mua</span>',
      '<span class="state-sample" style="background:#1D4ED8;color:#fff;box-shadow:0 6px 12px rgba(37,99,235,.3)">Mua</span>',
      '<span class="state-sample" style="background:#1E40AF;color:#fff;transform:translateY(1px)">Mua</span>',
      '<span class="state-sample" style="background:#2563EB;color:#fff;box-shadow:0 0 0 3px #fff,0 0 0 5px #06B6D4">Mua</span>',
      '<span class="state-sample" style="background:#E2E8F0;color:#64748B">Mua</span>',
      '<span class="state-sample" style="background:#2563EB;color:rgba(255,255,255,.6)">◌</span>'
    ];
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 02 · NÚT BẤM</div><h1 class="scene-title">Sáu trạng thái <span class="accent">tạo cảm giác chuyên nghiệp</span></h1></div>
      <div class="states-lab">
        <div class="card lab-card" style="background:#fff">
          <div style="position:absolute;left:30px;top:22px;font-family:Jakarta;font-size:11px;font-weight:800;letter-spacing:.14em;color:#94A3B8">BUTTON LAB · LIVE DEMO</div>
          <div class="lab-btn-wrap"><span class="btn btn-primary" id="demoBtn" style="width:320px;height:72px;font-size:22px;border-radius:10px"><span id="demoLabel">Thêm vào giỏ</span><span id="spin" class="spinner" style="display:none"></span></span></div>
          <div class="state-note" id="stateNote"><b>DEFAULT</b><span>Trạng thái bình thường khi chưa tương tác.</span></div>
          <div class="state-specs" id="stateSpecs"><span>Cao 48px</span><span>Bo góc 8px</span><span>Chữ 16px · 600</span></div>
          <div id="rippleRoot" class="ripple-clip"></div>
          <div class="state-grid">${states.map((s, i) => `<div class="state-card" data-st="${i}"><b>${s}</b>${samples[i]}</div>`).join('')}</div>
          <div class="keycap" id="tabKey" style="right:118px;top:150px;opacity:0">Tab ⇥</div>
        </div>
      </div>`;
    const tr = teacher({ pose: 'explain', width: 208, style: 'left:1640px;top:606px;' });
    cam.appendChild(tr.el);
    const demo = cam.querySelector('#demoBtn');
    const label = cam.querySelector('#demoLabel');
    const spin = cam.querySelector('#spin');
    const specs = cam.querySelector('#stateSpecs');
    const cards = [...cam.querySelectorAll('.state-card')];
    const cursor = h('div', 'cursor', `<svg viewBox="0 0 34 42" width="34" height="42"><path d="M4 2l24 18-11 2-5 12z" fill="#1E293B" stroke="#fff" stroke-width="2"/></svg>`);
    cam.appendChild(cursor);
    const tab = cam.querySelector('#tabKey');
    const rippleRoot = cam.querySelector('#rippleRoot');
    const noteB = cam.querySelector('#stateNote b');
    const noteS = cam.querySelector('#stateNote span');
    const notes = {
      DEFAULT: 'Trạng thái bình thường khi chưa tương tác.',
      HOVER: 'Rê chuột: đậm hơn và nâng lên 2px.',
      ACTIVE: 'Nhấn xuống: tối hơn, lún 1–2px.',
      FOCUS: 'Bàn phím: viền rõ để biết đang ở đâu.',
      DISABLED: 'Không thao tác được: giảm tương phản, vẫn đọc được.',
      LOADING: 'Đang xử lý: giữ kích thước, thay chữ bằng vòng xoay.'
    };
    const setNote = (k) => { noteB.textContent = k; noteS.textContent = notes[k]; };
    const base = { left: 1040, top: 330 };
    const target = { left: 880, top: 408 };
    let active = -1;

    return {
      update(U) {
        const t = U.t;
        const p0 = U.p(0, 0.1, 0.7);
        const p1 = U.p(1, 0.05, 0.6);
        const p2 = U.p(2, 0.05, 0.6);
        const p3 = U.p(3, 0.05, 0.5);
        let left = base.left, top = base.top;
        if (t < U.cueStart(1)) {
          const hov = U.p(0, 1.9, 0.7);
          left = lerp(base.left, target.left, ease(hov));
          top = lerp(base.top, target.top, ease(hov));
          demo.style.transform = `translateY(${-2 * hov}px)`;
          demo.style.background = hov > 0.5 ? '#1D4ED8' : '#2563EB';
          demo.style.boxShadow = `0 ${8 + hov * 4}px ${18 + hov * 10}px rgba(29,78,216,${0.3 + hov * 0.1})`;
          const k0 = hov > 0.5 ? 1 : 0;
          setActive(cards, k0);
          setNote(states[k0]);
        } else if (t < U.cueStart(2)) {
          left = target.left; top = target.top;
          const click = U.p(1, 0.25, 0.35);
          demo.style.transform = `translateY(${3 * (click > 0 && click < 1 ? 1 : 0)}px)`;
          demo.style.background = '#1E40AF';
          addRipple(click);
          const tabIn = U.p(1, 1.3, 0.5);
          tab.style.opacity = tabIn;
          tab.style.transform = `translateY(${(1 - tabIn) * 10}px)`;
          const focus = U.p(1, 1.9, 0.5);
          demo.style.boxShadow = focus > 0.05 ? `0 0 0 3px #fff, 0 0 0 6px rgba(6,182,212,${focus}), 0 12px 26px rgba(6,182,212,.28)` : 'none';
          const k1 = focus > 0.5 ? 3 : (click > 0.2 ? 2 : 1);
          setActive(cards, k1);
          setNote(states[k1]);
          if (focus > 0.5) { tab.style.opacity = 0; }
        } else if (t < U.cueStart(3)) {
          left = target.left; top = target.top;
          const dis = U.p(2, 0.2, 0.5);
          const load = U.p(2, 2.8, 0.5);
          demo.style.background = dis > 0.5 ? '#E2E8F0' : '#1E40AF';
          demo.style.color = dis > 0.5 ? '#64748B' : '#fff';
          demo.style.boxShadow = 'none';
          label.textContent = load > 0.5 ? 'Đang xử lý' : 'Thêm vào giỏ';
          label.style.opacity = load > 0.5 ? 0.55 : 1;
          spin.style.display = load > 0.5 ? 'block' : 'none';
          spin.style.transform = `rotate(${t * 300}deg)`;
          label.style.display = load > 0.5 ? 'none' : 'inline';
          cursor.style.left = (target.left + 4) + 'px';
          const k2 = load > 0.5 ? 5 : (dis > 0.5 ? 4 : 2);
          setActive(cards, k2);
          setNote(states[k2]);
        } else {
          left = target.left; top = target.top;
          cursor.style.opacity = 0.9;
          cards.forEach((c, i) => {
            c.classList.add('on');
            c.style.transform = `translateY(${Math.sin(t * 3 + i * 0.9) * 3}px)`;
          });
          noteB.textContent = 'MỘT HỆ THỐNG';
          noteS.textContent = 'Sáu trạng thái, cùng thông số, cùng nhịp điệu.';
          demo.style.background = '#2563EB'; demo.style.color = '#fff'; demo.style.transform = 'none';
          demo.style.boxShadow = '0 10px 24px rgba(37,99,235,.26)';
          label.style.display = 'inline'; label.textContent = 'Thêm vào giỏ'; spin.style.display = 'none'; tab.style.opacity = 0;
        }
        cursor.style.left = left + 'px';
        cursor.style.top = top + 'px';
        const specP = U.p(3, 0.25, 0.6);
        specs.style.opacity = specP;
        specs.style.transform = `translateX(-50%) translateY(${(1 - specP) * 10}px)`;
        tr.update(t, t > U.cueStart(3) ? 'wave' : 'explain');
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'states').dur;
        const p = clamp(local / d);
        return `scale(${1 + p * 0.03})`;
      }
    };

    function setActive(cards, i) {
      if (i === active) return;
      active = i;
      cards.forEach((c, k) => c.classList.toggle('on', k === i));
    }
    function addRipple(p) {
      if (p <= 0.02 || p >= 1) { rippleRoot.innerHTML = ''; return; }
      if (!rippleRoot.dataset.on) {
        rippleRoot.dataset.on = '1';
        const r = h('div', 'ripple');
        r.style.cssText = 'position:absolute;left:50%;top:50%;border-radius:50%;background:rgba(255,255,255,.45);transform:translate(-50%,-50%);pointer-events:none;';
        rippleRoot.appendChild(r);
      }
      const r = rippleRoot.firstChild;
      if (!r) return;
      const s = 180 * p;
      r.style.width = s + 'px'; r.style.height = s + 'px'; r.style.opacity = 0.5 * (1 - p);
    }
  };

  /* ---------- 10. MISTAKES ---------- */
  B.mistakes = (cam) => {
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 02 · NÚT BẤM</div><h1 class="scene-title">Ba lỗi thường gặp &amp; <span class="green">cách sửa</span></h1></div>
      <div class="compare bad">
        <div class="compare-head">${icon('alert', 20)} SAI · thiếu hệ thống</div>
        <div class="compare-body">
          <div class="bad-frame">${badShopUI(true)}</div>
          <div class="mistake-list">
            <div class="mistake-item" data-i="0"><span class="mn">1</span><div><b>Quá nhiều màu nhấn</b><span>Bốn CTA bốn màu — mắt không biết nhìn đâu.</span></div></div>
            <div class="mistake-item" data-i="1"><span class="mn">2</span><div><b>Mỗi nút một kích thước</b><span>Chiều cao, bo góc, độ đậm khác nhau.</span></div></div>
            <div class="mistake-item" data-i="2"><span class="mn">3</span><div><b>Chữ và nền thiếu tương phản</b><span>Nội dung gần như biến mất trên nền sáng.</span></div></div>
          </div>
        </div>
      </div>
      <div class="fix-arrow" data-arrow style="opacity:0"></div>
      <div class="compare good">
        <div class="compare-head">${icon('check', 20)} ĐÚNG · một hệ thống</div>
        <div class="compare-body" style="padding:0">${browser(shopUI(), { url: 'shopxanh.vn', bodyStyle: 'height:100%' })}</div>
        <div class="fix-checks" style="position:absolute;left:22px;right:22px;bottom:16px;background:#fff;border:1px solid #D1FAE5;border-radius:12px;padding:12px 16px">
          <div class="fix-check"><span class="tick">✓</span> Một màu nhấn duy nhất cho CTA</div>
          <div class="fix-check"><span class="tick">✓</span> Cùng chiều cao 48px · bo góc 8px</div>
          <div class="fix-check"><span class="tick">✓</span> Tương phản chữ/nền đạt WCAG AA</div>
        </div>
      </div>`;
    const issues = [...cam.querySelectorAll('.mistake-item')];
    const arrow = cam.querySelector('[data-arrow]');
    const good = cam.querySelector('.compare.good');
    const bad = cam.querySelector('.compare.bad');
    return {
      update(U) {
        const p = U.p(0, 0.2, 2.4);
        issues.forEach((el, i) => {
          const k = clamp((p * 3 - i) / 0.55);
          el.style.opacity = k;
          el.style.transform = `translateY(${(1 - k) * 12}px)`;
        });
        const pf = U.p(1, 0.15, 0.8);
        arrow.style.opacity = pf;
        arrow.style.transform = `scaleX(${pf})`;
        arrow.style.transformOrigin = '0 50%';
        good.style.boxShadow = pf > 0.2 ? `0 26px 60px rgba(16,185,129,${0.14 + pf * 0.1})` : 'var(--shadow)';
        bad.style.opacity = 1 - pf * 0.15;
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'mistakes').dur;
        const p = clamp(local / d);
        const pan = Math.sin(p * Math.PI * 1.6) * 18;
        return `scale(1.015) translateX(${pan}px)`;
      }
    };
  };

  /* ---------- 11. MAKEOVER ---------- */
  B.makeover = (cam) => {
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">PHẦN 02 · THỰC HÀNH</div><h1 class="scene-title">Cùng nội dung, <span class="accent">khác hệ thống</span></h1></div>
      <div class="browser makeover-browser">
        <div class="browser-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="url">shopxanh.vn</span></div>
        <div class="browser-body" style="position:absolute;inset:34px 0 0">
          <div class="mk-layer" id="beforeLayer">${badShopUI()}</div>
          <div class="mk-layer" id="afterLayer" style="clip-path:inset(0 0 0 92%)">${shopUI()}</div>
          <div class="mk-slider" id="mkSlider" style="left:92%"><div class="mk-handle">↔</div></div>
        </div>
      </div>
      <div class="mk-tag before">TRƯỚC</div><div class="mk-tag after">SAU</div>
      <div class="mk-stats">
        <div class="mk-stat"><b>60%</b><span>nền trắng &amp; xanh nhạt</span></div>
        <div class="mk-stat"><b>30%</b><span>xanh dương phân khu</span></div>
        <div class="mk-stat"><b>10%</b><span>cam cho CTA duy nhất</span></div>
      </div>`;
    const after = cam.querySelector('#afterLayer');
    const slider = cam.querySelector('#mkSlider');
    const stats = [...cam.querySelectorAll('.mk-stat')];
    const before = cam.querySelector('#beforeLayer');
    const tagBefore = cam.querySelector('.mk-tag.before');
    return {
      update(U) {
        const p = U.p(0, 0.1, 4.2);
        const x = lerp(92, 0, smooth(p));
        after.style.clipPath = `inset(0 0 0 ${x}%)`;
        slider.style.left = x + '%';
        slider.style.opacity = 1 - U.p(0, 0.9, 0.2);
        tagBefore.style.opacity = 1 - U.p(0, 0.78, 0.25);
        before.style.opacity = 1;
        stats.forEach((s, i) => fade(s, U.p(0, 0.4 + i * 0.6, 0.5), 12, 14));
        const done = U.p(1, 0.1, 0.8);
        const cta = cam.querySelectorAll('.mk-layer#afterLayer .btn-amber');
        cta.forEach((b) => { b.style.boxShadow = `0 8px 22px rgba(245,158,11,${0.28 + done * 0.2})`; });
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'makeover').dur;
        const p = clamp(local / d);
        return `scale(${1.01 + p * 0.018})`;
      }
    };
  };

  /* ---------- 12. RECAP ---------- */
  B.recap = (cam) => {
    const items = [
      { n: '01', t: 'Phối màu có nguyên tắc', d: 'Bắt đầu từ 60–30–10, rồi mới chọn sắc độ.', icon: 'palette', c: '#2563EB' },
      { n: '02', t: 'Màu để phân cấp', d: 'Nền, phụ, nhấn — mỗi màu một nhiệm vụ.', icon: 'layers', c: '#06B6D4' },
      { n: '03', t: 'Nút bấm là hệ thống', d: 'Cùng thông số, cùng trạng thái, cùng ngôn ngữ.', icon: 'button', c: '#F59E0B' }
    ];
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">TỔNG KẾT</div><h1 class="scene-title">Ba điều mang về</h1><svg class="scribble" viewBox="0 0 300 16"><path d="M4 10C64 3 150 3 208 7c30 2 58 4 88 1"/></svg></div>
      ${items.map((x, i) => `<div class="card recap-card" data-c="${i}" style="left:${96 + i * 476}px;top:${300 - i * 26}px">
        <div style="display:flex;align-items:center;justify-content:space-between"><div class="n" style="color:${x.c}">${x.n}</div><div style="width:54px;height:54px;border-radius:15px;background:${x.c}1A;color:${x.c};display:flex;align-items:center;justify-content:center">${icon(x.icon, 28)}</div></div>
        <h3>${x.t}</h3><p>${x.d}</p>
        <div style="position:absolute;left:28px;right:28px;bottom:24px;height:5px;border-radius:3px;background:#EAF2FC"><div data-bar style="height:100%;width:0;border-radius:3px;background:${x.c}"></div></div>
      </div>`).join('')}
      <div class="recap-banner" data-banner style="opacity:0">${icon('check', 30)} Giao diện chuyên nghiệp = nhất quán trong từng chi tiết</div>`;
    const tr = teacher({ pose: 'wave', width: 196, style: 'left:1632px;top:636px;' });
    cam.appendChild(tr.el);
    const cards = [...cam.querySelectorAll('.recap-card')];
    const banner = cam.querySelector('[data-banner]');
    const bars = [...cam.querySelectorAll('[data-bar]')];
    const scrib = cam.querySelector('.scribble path');
    return {
      update(U) {
        cards.forEach((c, i) => fade(c, U.p(0, 0.1 + i * 0.55, 0.6), 26, 0, 0.96));
        bars.forEach((b, i) => { b.style.width = (U.p(0, 0.2 + i * 0.55, 0.6) * 100) + '%'; });
        fade(banner, U.p(1, 0.15, 0.7), 20, 0, 0.97);
        scrib.style.strokeDashoffset = 100 * (1 - U.p(0, 0.1, 0.8));
        tr.update(U.t, 'wave');
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'recap').dur;
        const p = clamp(local / d);
        return `scale(${1 + p * 0.03}) translateY(${-p * 8}px)`;
      }
    };
  };

  /* ---------- 13. QUIZ ---------- */
  B.quiz = (cam) => {
    const QS = [
      { q: 'Quy tắc phối màu trong bài dùng tỷ lệ nào?', opts: ['50–40–10', '60–30–10', '70–20–10', '80–15–5'], a: 1, ex: 'Nền 60% · màu phụ 30% · màu nhấn 10%.' },
      { q: 'Màu nhấn 10% dùng để làm gì?', opts: ['Trang trí nền', 'Hướng mắt vào hành động chính', 'Thay thế màu phụ', 'Làm mờ nội dung'], a: 1, ex: 'Màu nhấn dành cho CTA và thông tin quan trọng.' },
      { q: 'Trạng thái nào xuất hiện khi rê chuột lên nút?', opts: ['Active', 'Focus', 'Hover', 'Disabled'], a: 2, ex: 'Hover khi rê chuột · Active khi nhấn · Focus khi dùng bàn phím.' }
    ];
    const labels = ['A', 'B', 'C', 'D'];
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">ÔN TẬP · 3 CÂU</div><h1 class="scene-title">Kiểm tra nhanh</h1></div>
      <div class="card quiz-panel">
        ${QS.map((q, i) => `<div class="quiz-group" data-q="${i}" style="position:absolute;inset:34px 40px">
          <div class="quiz-top"><div class="quiz-kicker">CÂU HỎI ${i + 1} / 3</div><div class="quiz-counter">CHỌN MỘT ĐÁP ÁN</div></div>
          <div class="quiz-progress">${[0, 1, 2].map((k) => `<span class="${k <= i ? 'on' : ''}"></span>`).join('')}</div>
          <div class="quiz-q">${q.q}</div>
          <div style="position:absolute;right:0;top:0" class="quiz-ring" data-ring="${i}"><svg viewBox="0 0 86 86"><circle cx="43" cy="43" r="36" fill="none" stroke="#E2EFFB" stroke-width="7"/><circle class="ring-fill" cx="43" cy="43" r="36" fill="none" stroke="#2563EB" stroke-width="7" stroke-linecap="round" stroke-dasharray="226.2" stroke-dashoffset="0"/></svg><div class="num3">3</div></div>
          <div class="quiz-options">${q.opts.map((o, k) => `<div class="q-option" data-o="${k}"><span class="k">${labels[k]}</span><span>${o}</span></div>`).join('')}</div>
          <div class="quiz-explain" data-ex>${q.ex}</div>
        </div>`).join('')}
        <div class="quiz-foot"><span>Chọn đáp án · đáp án đúng hiện sau 3 giây</span><b>UI LAB · REVIEW</b></div>
      </div>`;
    const tr = teacher({ pose: 'explain', width: 236, style: 'left:1608px;top:580px;' });
    cam.appendChild(tr.el);
    const groups = [...cam.querySelectorAll('.quiz-group')];
    const groupsMeta = [
      { q: 0, a: 1 }, { q: 2, a: 3 }, { q: 4, a: 5 }
    ];

    return {
      update(U) {
        let active = 0;
        if (U.t >= U.cueStart(2)) active = 1;
        if (U.t >= U.cueStart(4)) active = 2;
        groups.forEach((g, i) => {
          const on = i === active;
          g.style.opacity = on ? 1 : 0;
          g.style.pointerEvents = 'none';
          g.style.transform = `translateY(${on ? 0 : 20}px)`;
        });
        const meta = groupsMeta[active];
        const g = groups[active];
        const qEnd = U.cueEnd(meta.q);
        const aStart = U.cueStart(meta.a);
        const during = U.t >= qEnd && U.t < aStart;
        const answered = U.t >= aStart;
        const p = clamp((U.t - qEnd) / Math.max(0.01, aStart - qEnd));
        const ring = g.querySelector('.ring-fill');
        const ringBox = g.querySelector('.quiz-ring');
        const num = g.querySelector('.num3');
        const q = QS[active];
        ring.style.strokeDashoffset = 226.2 * p;
        ringBox.style.opacity = during ? 1 : 0;
        num.style.opacity = during ? 1 : 0;
        num.textContent = String(Math.max(1, Math.ceil(3 * (1 - p))));
        g.querySelectorAll('.q-option').forEach((o, k) => {
          o.classList.toggle('correct', answered && k === q.a);
          o.classList.toggle('dim', answered && k !== q.a);
        });
        const ex = g.querySelector('[data-ex]');
        ex.style.opacity = answered ? 1 : 0;
        ex.style.transform = `translateY(${answered ? 0 : 8}px)`;
        tr.update(U.t, answered ? 'wave' : 'explain', 1);
      },
      cam(local) {
        const d = TL.scenes.find((s) => s.id === 'quiz').dur;
        const p = clamp(local / d);
        return `scale(${1 + p * 0.015})`;
      }
    };
  };

  /* ---------- 14. OUTRO ---------- */
  B.outro = (cam) => {
    cam.innerHTML = `
      <div class="outro-k">UI LAB · BÀI GIẢNG 05 PHÚT</div>
      <div class="outro-quote">
        <h2 class="outro-h">Nhất quán trong từng chi tiết.</h2>
        <svg class="scribble outro-scribble" viewBox="0 0 300 16"><path d="M4 10C64 3 150 3 208 7c30 2 58 4 88 1"/></svg>
        <p class="outro-p">Một giao diện đẹp không chỉ nằm ở màu sắc bắt mắt, mà ở sự nhất quán trong từng chi tiết. Hãy bắt đầu từ bảng màu và hệ thống nút bấm.</p>
        <div class="outro-chips"><span class="chip">${icon('palette', 18)} Bảng màu 60–30–10</span><span class="chip amber-chip">${icon('button', 18)} Hệ thống nút bấm</span></div>
      </div>
      <div class="outro-teacher"></div>
      <div class="outro-sign">SHOP XANH · CASE STUDY · 2026</div>`;
    const tr = teacher({ pose: 'wave', width: 330, style: 'left:186px;top:486px;' });
    cam.querySelector('.outro-teacher').replaceWith(tr.el);
    const h = cam.querySelector('.outro-h');
    const pEl = cam.querySelector('.outro-p');
    const chips = [...cam.querySelectorAll('.chip')];
    const k = cam.querySelector('.outro-k');
    const sign = cam.querySelector('.outro-sign');
    const scrib = cam.querySelector('.outro-scribble path');
    const hs = words(h, 'Nhất quán trong từng chi tiết.');
    return {
      update(U) {
        const p = U.p(0, 0.05, 0.8);
        k.style.opacity = p;
        hs.forEach((s, i) => {
          const q = ease(clamp((p * (hs.length + 4) - i) / 2.6));
          s.style.transform = `translateY(${(1 - q) * 110}%)`;
          s.style.opacity = q;
        });
        scrib.style.strokeDashoffset = 100 * (1 - U.p(0, 0.55, 0.7));
        fade(pEl, U.p(0, 0.85, 0.7), 16);
        chips.forEach((c, i) => fade(c, U.p(0, 1.1 + i * 0.25, 0.5), 12));
        fade(sign, U.p(0, 1.4, 0.6), 8);
        tr.update(U.t, 'wave');
        const end = U.p(0, 5.5, 1.2);
        cam.style.filter = `opacity(${1 - end * 0.0})`;
        cam.style.background = `rgba(255,255,255,${end * 0.55})`;
        cam.style.borderRadius = '0';
      }
    };
  };

  /* ============================================================
     BUILD
     ============================================================ */
  TL.scenes.forEach((def) => {
    const el = h('div', 'scene sc-' + def.type);
    el.style.opacity = 0;
    const cam = h('div', 'cam');
    el.appendChild(cam);
    root.appendChild(el);
    const builder = B[def.type];
    if (!builder) { cam.innerHTML = `<h1>${def.title}</h1>`; console.warn('missing builder', def.type); }
    const api = builder ? builder(cam, def) : null;
    const cues = def.cues.map((c) => ({ ...c, ls: c.start - def.start, le: c.end - def.start }));
    built.push({ def, el, cam, api, cues });
  });

  /* ---------- global decor ---------- */
  const floatRoot = document.getElementById('floating');
  const chips = [];
  const palette = ['#2563EB', '#06B6D4', '#F59E0B', '#8B5CF6', '#BFDBFE', '#FDE68A'];
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  for (let i = 0; i < 24; i++) {
    const d = h('div', 'float-chip');
    const w = 14 + rnd() * 30;
    d.style.width = w + 'px';
    d.style.height = (10 + rnd() * 26) + 'px';
    d.style.background = palette[i % palette.length];
    d.style.opacity = 0.16 + rnd() * 0.2;
    floatRoot.appendChild(d);
    chips.push({ el: d, x: rnd() * 1920, y: rnd() * 1080, s: 0.4 + rnd(), ph: rnd() * 6.28, rot: rnd() * 360 });
  }

  let cur = -1, prev = -1, capIdx = -1;
  const binary = (arr, t, key) => {
    let lo = 0, hi = arr.length - 1, ans = -1;
    while (lo <= hi) { const m = (lo + hi) >> 1; if (arr[m][key] <= t) { ans = m; lo = m + 1; } else hi = m - 1; }
    return ans;
  };

  function renderFrame(t) {
    t = clamp(t, 0, TL.duration);
    const idx = Math.max(0, binary(TL.scenes, t, 'start'));
    if (idx !== cur) {
      prev = cur;
      cur = idx;
      built.forEach((b, i) => {
        if (i === cur) b.el.classList.add('on');
        if (i !== cur && i !== prev) { b.el.classList.remove('on'); b.el.style.opacity = 0; }
      });
      const sc = TL.scenes[idx];
      if (sc.part) partChip.textContent = 'PHẦN ' + pad(sc.part) + ' · ' + PARTS[sc.part].en;
      else if (sc.id === 'quiz') partChip.textContent = 'ÔN TẬP · REVIEW';
      else if (sc.id === 'outro') partChip.textContent = 'KẾT THÚC · WRAP-UP';
      else partChip.textContent = 'BÀI GIẢNG';
      document.body.classList.toggle('dark-chrome', sc.type === 'divider');
      sweep.style.background = sc.part === 2
        ? 'linear-gradient(100deg, rgba(139,92,246,0) 0%, rgba(139,92,246,.20) 34%, rgba(37,99,235,.32) 50%, rgba(139,92,246,.20) 66%, rgba(139,92,246,0) 100%)'
        : 'linear-gradient(100deg, rgba(37,99,235,0) 0%, rgba(37,99,235,.16) 34%, rgba(6,182,212,.32) 50%, rgba(37,99,235,.16) 66%, rgba(37,99,235,0) 100%)';
    }
    const def = TL.scenes[idx];
    const local = t - def.start;
    const b = built[idx];
    const fin = smooth(local / 0.55);
    const fout = smooth((def.dur - local) / 0.5);
    b.el.style.opacity = Math.min(fin, fout, 1);
    b.el.style.zIndex = 20;
    if (b.api && b.api.cam) b.cam.style.transform = b.api.cam(local);
    if (prev >= 0 && prev !== idx) {
      const pb = built[prev];
      const po = 1 - clamp((t - (TL.scenes[prev].start + TL.scenes[prev].dur)) / 0.42);
      pb.el.style.opacity = po;
      pb.el.style.zIndex = 10;
      if (po <= 0) { pb.el.classList.remove('on'); prev = -1; }
    }
    if (b.api && b.api.update) {
      const U = {
        t: local,
        on: (i) => local >= b.cues[i].ls,
        p: (i, delay = 0, dur = 0.5) => ease(clamp((local - b.cues[i].ls - delay) / dur)),
        raw: (i, delay = 0, dur = 0.5) => clamp((local - b.cues[i].ls - delay) / dur),
        cueStart: (i) => b.cues[i].ls,
        cueEnd: (i) => b.cues[i].le,
        cueT: (i) => local - b.cues[i].ls
      };
      b.api.update(U);
    }

    // sweep on scene entry
    const sp = smooth(local / 0.7);
    sweep.style.transform = `translateX(${(-100 + sp * 200).toFixed(2)}%)`;
    sweep.style.opacity = sp > 0.02 && sp < 0.98 ? (0.55 * Math.sin(Math.PI * sp)).toFixed(3) : 0;

    // background breathing
    blobA.style.transform = `translate(${Math.sin(t * 0.16) * 50}px,${Math.cos(t * 0.13) * 34}px)`;
    blobB.style.transform = `translate(${Math.cos(t * 0.12 + 2) * 60}px,${Math.sin(t * 0.15) * 40}px)`;
    blobC.style.transform = `translate(${Math.sin(t * 0.1 + 4) * 70}px,${Math.cos(t * 0.11) * 30}px)`;
    chips.forEach((c) => {
      const x = c.x + Math.sin(t * 0.12 * c.s + c.ph) * 40;
      const y = c.y + Math.cos(t * 0.1 * c.s + c.ph) * 30;
      c.el.style.transform = `translate(${x}px,${y}px) rotate(${c.rot + t * 4 * c.s}deg)`;
    });

    // captions
    const ci = binary(TL.captions, t, 'start');
    if (ci !== capIdx) {
      capIdx = ci;
      if (ci >= 0) captionEl.textContent = TL.captions[ci].text;
    }
    if (ci >= 0) {
      const c = TL.captions[ci];
      const a = smooth((t - c.start) / 0.16) * smooth((c.end - t) / 0.16 + 0.35);
      captionEl.style.opacity = clamp(a, 0, 1);
      captionWrap.classList.toggle('on', a > 0.04);
    } else {
      captionEl.style.opacity = 0;
      captionWrap.classList.remove('on');
    }

    // chrome
    fill.style.width = (100 * t / TL.duration).toFixed(2) + '%';
    plabel.textContent = fmt(t);
    tcode.textContent = fmt(t) + ' / ' + fmt(TL.duration);
  }

  window.renderFrame = renderFrame;
  window.__ready = true;
  window.__sceneAt = (id) => built.findIndex((b) => b.def.id === id);
  window.__built = built;
})();
