/* ============================================================
   AN TECH ACADEMY — HỆ THỐNG GỢI Ý SẢN PHẨM
   Engine cảnh tất định: renderFrame(t) đặt toàn bộ trạng thái theo t.
   Không CSS animation / requestAnimationFrame -> frame nào cũng tái lập.
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
  const smooth = (p) => { p = clamp(p); return p * p * (3 - 2 * p); };
  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (s) => `${pad(Math.floor(s / 60))}:${pad(Math.floor(s % 60))}`;

  const PARTS = {
    1: 'CÁ NHÂN HÓA', 2: 'LỌC PHỔ BIẾN', 3: 'LỌC CỘNG TÁC',
    4: 'LỌC NỘI DUNG', 5: 'HYBRID', 6: 'TỔNG KẾT'
  };

  /* ---------- icons ---------- */
  const P = {
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
    click: '<path d="M9 9l5 12 1.8-5.2L21 14z"/><path d="M7.2 2.2l.8 2.8M2.2 7.2l2.8.8M4.9 4.9l2 2"/>',
    star: '<path d="M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z"/>',
    cart: '<circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M3 4h2l2.4 11h11.2L21 7H6"/>',
    gear: '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
    profile: '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2.4"/><path d="M5.5 17c.7-2 2-3 3.5-3s2.8 1 3.5 3M15 9h4M15 13h4"/>',
    list: '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    spark: '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4L12 3z"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    check: '<path d="M20 6L9 17l-5-5"/>',
    alert: '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    phone: '<rect x="7" y="2" width="10" height="20" rx="3"/><path d="M11 18h2"/>',
    chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    layers: '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 12l10 5 10-5M2 17l10 5 10-5"/>',
    db: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7"/>',
    bolt: '<path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/>',
    play: '<path d="M8 5l12 7-12 7z"/>'
  };
  const icon = (name, size = 24, stroke = 1.8) =>
    `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${stroke}" stroke-linecap="round" stroke-linejoin="round">${P[name] || ''}</svg>`;

  /* ---------- DOM helpers ---------- */
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

  /* ---------- TEACHER (chibi giảng viên) ---------- */
  let uid = 0;
  function teacher(opts = {}) {
    const id = 't' + (++uid);
    const el = h('div', 'teacher ' + (opts.cls || ''));
    if (opts.style) el.style.cssText += opts.style;
    el.innerHTML = `
      <svg viewBox="0 0 300 400" aria-hidden="true">
        <defs><linearGradient id="shirt-${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6366F1"/><stop offset="1" stop-color="#4338CA"/></linearGradient></defs>
        <ellipse cx="150" cy="384" rx="88" ry="13" fill="rgba(67,56,202,.13)"/>
        <g class="t-body">
          <rect x="119" y="296" width="24" height="64" rx="12" fill="#312E81"/>
          <rect x="157" y="296" width="24" height="64" rx="12" fill="#312E81"/>
          <ellipse cx="131" cy="366" rx="19" ry="9" fill="#0F172A"/>
          <ellipse cx="169" cy="366" rx="19" ry="9" fill="#0F172A"/>
          <path d="M92 238c0-35 26-64 58-64s58 29 58 64v42c0 27-22 46-58 46s-58-19-58-46z" fill="url(#shirt-${id})"/>
          <path d="M131 180l19 24 19-24" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M98 234c-17 10-26 29-23 49" fill="none" stroke="#4F46E5" stroke-width="24" stroke-linecap="round"/>
          <circle cx="74" cy="292" r="15" fill="#FFD8B8"/>
          <g class="t-arm">
            <path d="M202 234c15 11 23 28 20 46" fill="none" stroke="#4F46E5" stroke-width="24" stroke-linecap="round"/>
            <circle cx="224" cy="290" r="15" fill="#FFD8B8"/>
            <line x1="227" y1="292" x2="288" y2="212" stroke="#F59E0B" stroke-width="7" stroke-linecap="round"/>
            <circle cx="289" cy="210" r="8" fill="#F59E0B"/>
          </g>
          <circle cx="150" cy="132" r="76" fill="#FFD8B8"/>
          <circle cx="80" cy="140" r="13" fill="#FFC9A3"/><circle cx="220" cy="140" r="13" fill="#FFC9A3"/>
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
          <circle cx="103" cy="157" r="9" fill="#FDA4AF" opacity=".45"/><circle cx="197" cy="157" r="9" fill="#FDA4AF" opacity=".45"/>
        </g>
      </svg>`;
    if (opts.width) el.style.width = opts.width + 'px';
    const bubble = h('div', 'bubble', opts.bubble || '');
    bubble.style.display = opts.bubble ? 'block' : 'none';
    bubble.style.left = (opts.bubbleX ?? 200) + 'px';
    bubble.style.top = (opts.bubbleY ?? 6) + 'px';
    el.appendChild(bubble);
    const body = el.querySelector('.t-body');
    const arm = el.querySelector('.t-arm');
    const eyes = [...el.querySelectorAll('.t-eye')];
    const mouth = el.querySelector('.t-mouth');
    return {
      el, bubble,
      update(t, pose = 'point', showBubble = 0) {
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
  }

  /* ---------- SHOP MOCKUP ---------- */
  function phoneCard(name, spec, price, badge) {
    return `<div class="p-card" data-pcard>
      ${badge ? `<span class="p-badge">${badge}</span>` : ''}
      <div class="p-thumb"><div class="p-phone"></div></div>
      <div class="p-name">${name}</div><div class="p-spec">${spec}</div><div class="p-price">${price}</div>
    </div>`;
  }
  function recCard(name, why, score) {
    return `<div class="rec-card" data-rec><div class="r-thumb"></div><div><div class="r-name">${name}</div><div class="r-why">${why}</div></div><div class="r-score">${score}</div></div>`;
  }
  function shopBrowser(body, url = 'novashop.vn') {
    return `<div class="browser" style="height:100%"><div class="browser-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="url">${url}</span></div><div class="browser-body">${body}</div></div>`;
  }

  /* ---------- DATA (nhất quán với catalog.mjs) ---------- */
  const ITEMS = [
    { id: 'I1', name: 'Galaxy S24', brand: 'Samsung', ram: 12, rom: 256, pin: 5000, cam: 200 },
    { id: 'I2', name: 'Galaxy A55', brand: 'Samsung', ram: 8, rom: 256, pin: 5000, cam: 50 },
    { id: 'I3', name: 'iPhone 15', brand: 'Apple', ram: 6, rom: 128, pin: 3349, cam: 48 },
    { id: 'I4', name: 'iPhone 15 Pro', brand: 'Apple', ram: 8, rom: 256, pin: 3274, cam: 48 },
    { id: 'I5', name: 'Xiaomi 14', brand: 'Xiaomi', ram: 12, rom: 256, pin: 4610, cam: 50 }
  ];
  const USERS = [
    { id: 'A', taste: 'Samsung · cấu hình cao', color: '#2563EB' },
    { id: 'B', taste: 'iPhone · camera', color: '#7C3AED' },
    { id: 'C', taste: 'Người mới', color: '#64748B' },
    { id: 'D', taste: 'Cùng gu với A', color: '#06B6D4' }
  ];
  const MATRIX = [
    [5, 4, null, null, null],
    [3, null, 5, null, null],
    [null, null, null, null, null],
    [5, 4, 2, null, 5]
  ];

  /* ============================================================
     SCENE BUILDERS
     ============================================================ */
  const B = {};

  /* ---------- INTRO ---------- */
  B.intro = (cam, def) => {
    cam.innerHTML = `
      <div class="hero-eyebrow" data-eb>AN TECH ACADEMY · CÔNG NGHỆ GỢI Ý</div>
      <h1 class="hero-title" data-title><span data-l1>HỆ THỐNG</span><br><span class="l2" data-l2>GỢI Ý SẢN PHẨM</span></h1>
      <p class="hero-sub" data-sub>Cá nhân hóa người dùng và các thuật toán đứng sau những đề xuất "đọc được suy nghĩ".</p>
      <div class="hero-tags" data-tags>
        <span class="chip">Personalization</span>
        <span class="chip cyan-chip">Recommender System</span>
        <span class="chip violet-chip">KNN · SVD</span>
        <span class="chip amber-chip">Hybrid</span>
      </div>
      <div data-teacher></div>
      <div data-shop style="position:absolute;left:1010px;top:150px;width:814px;height:664px">
        ${shopBrowser(`
          <div class="shop">
            <div class="shop-nav"><div class="shop-logo"><span class="mark"></span>NOVA SHOP</div><div class="shop-links"><span>Điện thoại</span><span>Laptop</span><span>Phụ kiện</span></div><div class="shop-cart">Giỏ hàng · 2</div></div>
            <div class="shop-body">
              <div class="shop-row-label">${icon('phone', 15)} Đang xem · Samsung cấu hình cao</div>
              <div class="shop-grid">
                ${phoneCard('Galaxy S24', 'RAM 12GB · pin 5000mAh', '22.990.000 đ', 'HOT')}
                ${phoneCard('Galaxy A55', 'RAM 8GB · pin 5000mAh', '9.990.000 đ')}
                ${phoneCard('Xiaomi 14', 'RAM 12GB · ROM 256GB', '16.990.000 đ')}
              </div>
              <div class="shop-row-label" data-reclabel style="margin-top:4px">${icon('spark', 15)} Gợi ý cho bạn</div>
              <div class="rec-strip" data-recs>
                ${recCard('Galaxy S24', 'Cùng gu cấu hình cao', '98%')}
                ${recCard('Xiaomi 14', 'RAM 12GB · pin trâu', '95%')}
              </div>
            </div>
          </div>`)}
      </div>
      <div data-cursor style="position:absolute;width:26px;height:26px;z-index:8;color:#0F172A;opacity:0">
        <svg viewBox="0 0 24 24" width="26" height="26" fill="#fff" stroke="#0F172A" stroke-width="1.6"><path d="M5 3l14 8-6 1.5L11 19z"/></svg>
      </div>`;
    const eb = cam.querySelector('[data-eb]');
    const l1 = cam.querySelector('[data-l1]');
    const l2 = cam.querySelector('[data-l2]');
    const sub = cam.querySelector('[data-sub]');
    const tags = [...cam.querySelectorAll('[data-tags] .chip')];
    const shop = cam.querySelector('[data-shop]');
    const pcards = [...cam.querySelectorAll('[data-pcard]')];
    const reclabel = cam.querySelector('[data-reclabel]');
    const recs = [...cam.querySelectorAll('[data-rec]')];
    const cursor = cam.querySelector('[data-cursor]');
    const tr = teacher({ width: 250, style: 'left:120px;top:600px;' });
    cam.querySelector('[data-teacher]').replaceWith(tr.el);

    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.018})`,
      update(U) {
        fade(eb, U.p(0, 0, 0.5), 12);
        fade(l1, U.p(0, 0.15, 0.6), 26);
        fade(l2, U.p(0, 0.35, 0.6), 26);
        fade(sub, U.p(0, 0.7, 0.6), 16);
        tags.forEach((c, i) => fade(c, U.p(2, 0.1 + i * 0.18, 0.45), 12));
        fade(shop, U.p(0, 0.4, 0.7), 24, 30, 0.98);
        pcards.forEach((c, i) => fade(c, U.p(0, 0.7 + i * 0.16, 0.5), 14));
        // hook: cursor lướt các máy Samsung (cue1), gợi ý hiện ra
        const hookP = U.raw(1, 0, 2.6);
        const cx = lerp(1120, 1620, smooth(clamp(hookP * 1.4)));
        const cy = 320 + Math.sin(hookP * Math.PI * 2) * 16;
        cursor.style.opacity = U.on(1) ? clamp(U.p(1, 0, 0.3) - U.p(2, 0.4, 0.5)) : 0;
        cursor.style.transform = `translate(${cx}px, ${cy}px)`;
        pcards.forEach((c, i) => {
          const near = clamp(1 - Math.abs(cx - (1120 + i * 175)) / 120);
          c.classList.toggle('hot', U.on(1) && near > 0.4);
        });
        fade(reclabel, U.p(1, 1.5, 0.5), 10);
        recs.forEach((c, i) => fade(c, U.p(1, 1.7 + i * 0.3, 0.5), 16, 20));
        tr.update(U.t, U.on(2) ? 'point' : 'wave', U.p(0, 0.5, 0.5) * (1 - U.p(2, 0.6, 0.5)));
      }
    };
  };

  /* ---------- PERSONALIZATION (luồng dữ liệu) ---------- */
  B.personalization = (cam, def) => {
    const NX = [0, 430, 860, 1290];
    const node = (i, ico, color, title, sub, body) => `
      <div class="flow-node" data-node="${i}" style="left:${NX[i]}px;top:30px;width:300px">
        <div class="fn-head"><div class="fn-ico" style="background:${color}">${icon(ico, 26)}</div>
          <div><div class="fn-title">${title}</div><div class="fn-sub">${sub}</div></div></div>
        <div class="fn-body">${body}</div>
      </div>`;
    const behav = (ico, label) => `<div class="behav" data-behav><span class="b-ico">${icon(ico, 16)}</span>${label}</div>`;
    cam.innerHTML = `
      <div class="scene-head" data-head>
        <div class="eyebrow">PHẦN 1 · CÁ NHÂN HÓA NGƯỜI DÙNG</div>
        <h2 class="scene-title">Từ hành vi đến <span class="accent">hồ sơ sở thích</span></h2>
      </div>
      <div class="flow-stage">
        ${node(0, 'eye', '#4F46E5', 'Hành vi', 'DỮ LIỆU ĐẦU VÀO',
          behav('eye', 'Xem sản phẩm') + behav('search', 'Tìm kiếm') + behav('click', 'Nhấn chọn') + behav('star', 'Đánh giá') + behav('cart', 'Mua hàng'))}
        ${node(1, 'profile', '#7C3AED', 'Hồ sơ sở thích', 'USER PROFILE',
          `<div class="tag-row" data-tags>
            <span class="mini-tag" data-tag>Samsung</span>
            <span class="mini-tag" data-tag>Cấu hình cao</span>
            <span class="mini-tag" data-tag>Pin 5000mAh</span>
            <span class="mini-tag" data-tag>RAM 12GB</span>
          </div>
          <div style="font-size:13px;color:var(--muted);line-height:1.4;margin-top:4px" data-pnote>Ghi nhận gu riêng của từng người dùng.</div>`)}
        ${node(2, 'gear', '#06B6D4', 'Hệ thống gợi ý', 'RECOMMENDER SYSTEM',
          `<div style="font-size:14px;color:var(--ink);line-height:1.5" data-engine>Học sở thích từ hồ sơ, đối chiếu catalog sản phẩm.</div>
          <div class="chip cyan-chip" data-algo style="margin-top:6px">${icon('layers', 16)} KNN · SVD · TF-IDF</div>`)}
        ${node(3, 'list', '#14B8A6', 'Danh sách gợi ý', 'KẾT QUẢ ĐẦU RA',
          `<div class="flow-out" data-out>
            ${recCard('Galaxy S24', 'Đúng gu Samsung', '98%')}
            ${recCard('Xiaomi 14', 'Cấu hình cao', '95%')}
          </div>`)}
        <div class="flow-link" data-link="0" style="left:300px;top:120px;width:130px"></div>
        <div class="flow-link" data-link="1" style="left:730px;top:120px;width:130px"></div>
        <div class="flow-link" data-link="2" style="left:1160px;top:120px;width:130px"></div>
        <div class="packet" data-pk="0" style="left:300px;top:114px"></div>
        <div class="packet" data-pk="1" style="left:730px;top:114px"></div>
        <div class="packet" data-pk="2" style="left:1160px;top:114px"></div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const nodes = [...cam.querySelectorAll('[data-node]')];
    const links = [...cam.querySelectorAll('[data-link]')];
    const pks = [...cam.querySelectorAll('[data-pk]')];
    const behavs = [...cam.querySelectorAll('[data-behav]')];
    const tags = [...cam.querySelectorAll('[data-tag]')];
    const pnote = cam.querySelector('[data-pnote]');
    const engine = cam.querySelector('[data-engine]');
    const algo = cam.querySelector('[data-algo]');
    const outs = [...cam.querySelectorAll('[data-out] [data-rec]')];

    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.012})`,
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        // node 0 + behaviors (cue0)
        fade(nodes[0], U.p(0, 0.2, 0.55), 20);
        behavs.forEach((b, i) => fade(b, U.p(0, 0.5 + i * 0.12, 0.4), 10));
        // link0 + node1 profile (cue1)
        const l0 = U.p(1, 0, 0.5);
        links[0].style.transform = `scaleX(${l0})`;
        links[0].style.opacity = l0;
        fade(nodes[1], U.p(1, 0.25, 0.55), 20);
        tags.forEach((t, i) => fade(t, U.p(1, 0.6 + i * 0.16, 0.4), 10));
        fade(pnote, U.p(1, 1.2, 0.5), 8);
        // link1 + node2 engine (cue1->cue2)
        const l1 = U.p(1, 1.3, 0.6);
        links[1].style.transform = `scaleX(${l1})`;
        links[1].style.opacity = l1;
        fade(nodes[2], U.p(2, 0, 0.55), 20);
        fade(engine, U.p(2, 0.3, 0.5), 10);
        fade(algo, U.p(2, 0.6, 0.5), 10);
        // link2 + node3 output (cue2)
        const l2 = U.p(2, 0.7, 0.6);
        links[2].style.transform = `scaleX(${l2})`;
        links[2].style.opacity = l2;
        fade(nodes[3], U.p(2, 0.9, 0.55), 20);
        outs.forEach((o, i) => fade(o, U.p(2, 1.2 + i * 0.25, 0.45), 14, 16));
        // packets chạy dọc link khi đã nối
        const run = (pk, link, start, span) => {
          const on = U.t > start;
          const baseX = [300, 730, 1160][link];
          const prog = ((U.t - start) % span) / span;
          pk.style.opacity = on && link === 0 ? 0.95 : (on ? 0.95 : 0);
          pk.style.transform = `translateX(${prog * 118}px)`;
          pk.style.left = baseX + 'px';
        };
        run(pks[0], 0, U.cueStart(1), 1.1);
        run(pks[1], 1, U.cueStart(2), 1.1);
        run(pks[2], 2, U.cueStart(2) + 0.7, 1.1);
      }
    };
  };

  /* ---------- MATRIX (User–Item) ---------- */
  B.matrix = (cam, def) => {
    const colW = 158, rowW = 176, gap = 8, headH = 64, cellH = 78;
    let cellsHtml = '';
    // corner + column heads
    cellsHtml += `<div class="m-corner"></div>`;
    ITEMS.forEach((it) => {
      cellsHtml += `<div class="m-colhead" data-colhead><span class="mc-id">${it.id}</span><span class="mc-name">${it.name}</span></div>`;
    });
    // rows
    USERS.forEach((u, ri) => {
      cellsHtml += `<div class="m-rowhead" data-rowhead="${ri}"><span class="mr-av" style="background:${u.color}">${u.id}</span><span><span class="mr-name">Người dùng ${u.id}</span><br><span class="mr-taste">${u.taste}</span></span></div>`;
      MATRIX[ri].forEach((v, ci) => {
        const empty = v == null;
        cellsHtml += `<div class="m-cell ${empty ? 'empty' : 'filled'}" data-cell="${ri}-${ci}" data-empty="${empty ? 1 : 0}">${empty ? '?' : v}${empty ? '' : '<span class="m-star">★</span>'}</div>`;
      });
    });
    cam.innerHTML = `
      <div class="scene-head" data-head>
        <div class="eyebrow">PHẦN 1 · DỮ LIỆU NỀN TẢNG</div>
        <h2 class="scene-title">Ma trận <span class="accent">Người dùng – Sản phẩm</span></h2>
      </div>
      <div class="matrix-wrap" data-mwrap style="left:96px;top:290px">
        <div class="matrix-grid" style="grid-template-columns:${rowW}px repeat(5, ${colW}px);grid-template-rows:${headH}px repeat(4, ${cellH}px);gap:${gap}px">
          ${cellsHtml}
        </div>
      </div>
      <div class="card card-pad" data-legend style="left:1180px;top:290px;width:644px">
        <div class="card-kicker">${icon('grid', 18)} CÁCH ĐỌC MA TRẬN</div>
        <div style="display:flex;flex-direction:column;gap:12px;margin-top:16px;font-size:17px;line-height:1.4">
          <div data-lg><b class="indigo">Hàng</b> = người dùng (A, B, C, D)</div>
          <div data-lg><b class="violet">Cột</b> = sản phẩm (I1 … I5)</div>
          <div data-lg><b class="teal">Ô</b> = điểm đánh giá 1–5</div>
        </div>
        <div class="matrix-note" data-note style="position:relative;margin-top:20px;left:0;top:0">
          <span class="mn-x">≠</span> Ô trống KHÔNG phải điểm 0
        </div>
        <div class="sparsity" data-sp style="position:relative;margin-top:22px;left:0;top:0">
          <div class="sp-bar"><div class="sp-fill" data-spfill style="width:0%"></div></div>
          <div class="sp-label" data-splabel>0% ô trống</div>
        </div>
        <div class="chip cyan-chip" data-predchip style="margin-top:20px">${icon('spark', 16)} Dự đoán ô trống → chọn điểm cao</div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const mwrap = cam.querySelector('[data-mwrap]');
    const colheads = [...cam.querySelectorAll('[data-colhead]')];
    const rowheads = [...cam.querySelectorAll('[data-rowhead]')];
    const cells = [...cam.querySelectorAll('[data-cell]')];
    const legend = cam.querySelector('[data-legend]');
    const lgs = [...cam.querySelectorAll('[data-lg]')];
    const note = cam.querySelector('[data-note]');
    const sp = cam.querySelector('[data-sp]');
    const spfill = cam.querySelector('[data-spfill]');
    const splabel = cam.querySelector('[data-splabel]');
    const predchip = cam.querySelector('[data-predchip]');
    const cellRC = (r, c) => cam.querySelector(`[data-cell="${r}-${c}"]`);

    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.01})`,
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(mwrap, U.p(0, 0.1, 0.5), 18);
        colheads.forEach((c, i) => fade(c, U.p(0, 0.3 + i * 0.1, 0.4), 10));
        rowheads.forEach((r, i) => fade(r, U.p(0, 0.5 + i * 0.12, 0.4), 10));
        // ô filled hiện lần lượt theo cue0
        cells.forEach((cell) => {
          const [r, c] = cell.dataset.cell.split('-').map(Number);
          const isEmpty = cell.dataset.empty === '1';
          const delay = 0.7 + (r * 5 + c) * 0.045;
          if (!isEmpty) fade(cell, U.p(0, delay, 0.35), 8, 0, 0.9);
          else { cell.style.opacity = clamp(U.p(0, delay, 0.35)); cell.style.transform = 'none'; }
        });
        fade(legend, U.p(0, 0.4, 0.6), 20, 24);
        lgs.forEach((l, i) => fade(l, U.p(0, 0.7 + i * 0.18, 0.4), 10));
        // cue1: nhấn ô trống ≠ 0, hàng C, sparsity
        const eP = U.p(1, 0, 0.6);
        cells.forEach((cell) => {
          if (cell.dataset.empty === '1') {
            const pulse = 0.5 + 0.5 * Math.sin(U.t * 3);
            cell.style.borderColor = U.on(1) ? `rgba(239,68,68,${0.35 + 0.3 * pulse * eP})` : '#CBD5E1';
            cell.style.color = U.on(1) ? `rgba(239,68,68,${0.5 + 0.4 * eP})` : '#CBD5E1';
          }
        });
        const cRow = cellRC(2, 0);
        rowheads[2].style.boxShadow = U.on(1) ? `0 0 0 3px rgba(100,116,139,${0.25 * eP})` : 'none';
        fade(note, U.p(1, 0.3, 0.5), 12);
        fade(sp, U.p(1, 0.7, 0.5), 10);
        const spP = U.p(1, 0.8, 1.0);
        spfill.style.width = (60 * spP) + '%';
        splabel.textContent = Math.round(60 * spP) + '% ô trống';
        // cue2: dự đoán ô A×I5 (r0,c4)
        const target = cellRC(0, 4);
        const pr = U.p(2, 0.3, 0.7);
        if (U.on(2)) {
          target.classList.add('predict');
          target.classList.remove('empty');
          target.style.opacity = 1;
          target.innerHTML = pr > 0.5 ? '5.0<span class="m-star" style="color:#06B6D4">✦</span>' : '?';
          target.style.borderColor = '#67E8F9';
          target.style.color = '#0E7490';
          target.style.boxShadow = `0 0 0 ${3 + 3 * Math.sin(U.t * 4) * pr}px rgba(6,182,212,${0.2 * pr})`;
        }
        fade(predchip, U.p(2, 0.8, 0.5), 12);
      }
    };
  };

  /* ---------- DIVIDER ---------- */
  B.divider = (cam, def) => {
    cam.innerHTML = `
      <div class="divider-bg"></div>
      <div class="divider-num" data-num>${pad(def.part)}</div>
      <div class="divider-k" data-k>PHẦN ${def.part}</div>
      <div class="divider-title" data-title>${def.title}</div>
      <div class="divider-rule" data-rule></div>`;
    const num = cam.querySelector('[data-num]');
    const k = cam.querySelector('[data-k]');
    const title = cam.querySelector('[data-title]');
    const rule = cam.querySelector('[data-rule]');
    return {
      cam: (t) => `scale(${1.04 - ease(t / def.dur) * 0.04})`,
      update(U) {
        fade(num, U.p(0, 0, 0.6), 30);
        fade(k, U.p(0, 0.15, 0.5), 16);
        fade(title, U.p(0, 0.3, 0.6), 24);
        rule.style.transform = `scaleX(${U.p(0, 0.5, 0.6)})`;
        rule.style.opacity = U.p(0, 0.5, 0.4);
      }
    };
  };

  /* ---------- GOALS (khung cơ bản, hoàn thiện sau duyệt) ---------- */
  B.goals = (cam, def) => {
    const G = [
      ['01', 'Cá nhân hóa', 'Hành vi → hồ sơ sở thích'],
      ['02', 'Lọc phổ biến', 'Xếp hạng theo số đông'],
      ['03', 'Lọc cộng tác', 'KNN & SVD'],
      ['04', 'Lọc nội dung', 'TF-IDF & Cosine'],
      ['05', 'Hybrid', 'Weighted · Switching · Cascade']
    ];
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">LỘ TRÌNH BÀI HỌC</div>
        <h2 class="scene-title">Năm chặng <span class="accent">khám phá</span></h2></div>
      <div style="position:absolute;left:96px;top:320px;display:flex;gap:22px" data-row>
        ${G.map((g, i) => `<div class="goal-card" data-g="${i}" style="position:relative;width:316px"><div class="g-num">${g[0]}</div><div class="g-title">${g[1]}</div><div class="g-sub">${g[2]}</div></div>`).join('')}
      </div>`;
    const head = cam.querySelector('[data-head]');
    const gs = [...cam.querySelectorAll('[data-g]')];
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        gs.forEach((g, i) => fade(g, U.p(0, 0.3 + i * 0.22, 0.5), 20));
      }
    };
  };

  /* ---------- OUTRO (khung cơ bản, hoàn thiện sau duyệt) ---------- */
  B.outro = (cam, def) => {
    cam.innerHTML = `
      <div class="outro-k" data-k>AN TECH ACADEMY · RECOMMENDER SYSTEMS</div>
      <div class="outro-quote">
        <h2 class="outro-h" data-h>Từ dữ liệu đến thuật toán,<br>từ thuật toán đến gợi ý thông minh.</h2>
        <p class="outro-p" data-p>Hiểu bản chất từng thuật toán, bạn sẽ xây được hệ thống gợi ý cho chính dự án của mình.</p>
        <div class="outro-chips" data-chips><span class="chip">Cá nhân hóa</span><span class="chip cyan-chip">Thuật toán</span><span class="chip amber-chip">Hybrid</span></div>
      </div>
      <div class="outro-sign" data-sign>HẸN GẶP BẠN Ở BÀI TIẾP THEO</div>`;
    const k = cam.querySelector('[data-k]');
    const hh = cam.querySelector('[data-h]');
    const p = cam.querySelector('[data-p]');
    const chips = [...cam.querySelectorAll('[data-chips] .chip')];
    const sign = cam.querySelector('[data-sign]');
    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.02})`,
      update(U) {
        fade(k, U.p(0, 0, 0.5), 12);
        fade(hh, U.p(0, 0.15, 0.7), 26);
        fade(p, U.p(0, 0.8, 0.6), 16);
        chips.forEach((c, i) => fade(c, U.p(0, 1.1 + i * 0.2, 0.5), 12));
        fade(sign, U.p(0, 1.5, 0.6), 8);
      }
    };
  };

  /* ---------- DATA bổ sung cho các cảnh thuật toán (khớp catalog.mjs) ---------- */
  const POP = [
    { id: 'I1', name: 'Galaxy S24', buys: 1000, views: 12000, rating: 4.8 },
    { id: 'I3', name: 'iPhone 15', buys: 750, views: 9500, rating: 4.7 },
    { id: 'I5', name: 'Xiaomi 14', buys: 500, views: 6000, rating: 4.6 }
  ];
  const CAS = [
    { id: 'I1', name: 'Galaxy S24', svd: 4.9, cb: 0.95, final: 0.95, owned: true },
    { id: 'I5', name: 'Xiaomi 14', svd: 4.6, cb: 0.86, final: 0.88 },
    { id: 'I2', name: 'Galaxy A55', svd: 4.0, cb: 0.72, final: 0.74 },
    { id: 'I4', name: 'iPhone 15 Pro', svd: 3.1, cb: 0.55, final: 0.52 },
    { id: 'I3', name: 'iPhone 15', svd: 2.4, cb: 0.40, final: 0.38 }
  ];
  const TERMS = [
    { w: '12gb', tf: .9, idf: .9 }, { w: '200mp', tf: .7, idf: .95 }, { w: '5000', tf: .8, idf: .8 },
    { w: 'ram', tf: .9, idf: .2 }, { w: 'pin', tf: .8, idf: .25 }, { w: 'camera', tf: .7, idf: .3 }
  ];
  const miniGrid = (rows, cols, cell, gap, cls, valFn) => {
    let s = `<div class="fb-grid" style="grid-template-columns:repeat(${cols},${cell}px);grid-template-rows:repeat(${rows},${cell}px);gap:${gap}px">`;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) s += `<div class="fb-cell ${cls}" data-fb="${r}-${c}" style="width:${cell}px;height:${cell}px">${valFn ? valFn(r, c) : ''}</div>`;
    return s + '</div>';
  };

  /* ---------- POPULARITY (leaderboard) ---------- */
  B.popularity = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 2 · LỌC ĐỘ PHỔ BIẾN</div>
        <h2 class="scene-title">Xếp hạng theo <span class="accent">mức độ phổ biến</span></h2></div>
      <div style="position:absolute;left:96px;top:300px;width:1150px;display:flex;flex-direction:column;gap:18px" data-board>
        ${POP.map((p, i) => `<div class="lb-row" data-row="${i}">
          ${i === 0 ? `<span class="lb-crown" data-crown>${icon('star', 26)}</span>` : ''}
          <span class="lb-rank">#${i + 1}</span><span class="lb-name">${p.name}</span>
          <div class="lb-bar"><div class="lb-fill" data-fill style="width:0%"></div></div>
          <span class="lb-val" data-val>0</span>
          <span class="lb-meta">${p.views.toLocaleString('vi-VN')} xem · ★${p.rating}</span>
        </div>`).join('')}
      </div>
      <div class="card card-pad" data-crit style="left:1290px;top:300px;width:534px">
        <div class="card-kicker">${icon('chart', 18)} TÍN HIỆU XẾP HẠNG</div>
        <div style="display:flex;flex-direction:column;gap:12px;margin-top:16px;font-size:17px">
          <div data-c>${icon('cart', 18)} Lượt mua</div><div data-c>${icon('eye', 18)} Lượt xem</div>
          <div data-c>${icon('star', 18)} Điểm đánh giá</div><div data-c>${icon('click', 18)} Tần suất tương tác</div>
        </div>
        <div class="chip green-chip" data-pick style="margin-top:20px">${icon('check', 16)} Galaxy S24 dẫn đầu → gợi ý</div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const rows = [...cam.querySelectorAll('[data-row]')];
    const fills = [...cam.querySelectorAll('[data-fill]')];
    const vals = [...cam.querySelectorAll('[data-val]')];
    const crit = cam.querySelector('[data-crit]');
    const cs = [...cam.querySelectorAll('[data-c]')];
    const pick = cam.querySelector('[data-pick]');
    const crown = cam.querySelector('[data-crown]');
    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.012})`,
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(crit, U.p(0, 0.2, 0.6), 20, 24);
        cs.forEach((c, i) => fade(c, U.p(0, 0.4 + i * 0.15, 0.4), 10));
        rows.forEach((r, i) => fade(r, U.p(0, 0.3 + i * 0.12, 0.5), 16));
        const g = U.p(1, 0.2, 1.4);
        fills.forEach((f, i) => { f.style.width = (POP[i].buys / 1000 * 100 * g) + '%'; });
        vals.forEach((v, i) => { v.textContent = Math.round(POP[i].buys * g).toLocaleString('vi-VN'); });
        const hot = U.p(2, 0.3, 0.6);
        rows[0].classList.toggle('hot', hot > 0.4);
        if (crown) { crown.style.opacity = hot; crown.style.transform = `translateY(${(1 - hot) * -8}px)`; }
        fade(pick, U.p(2, 0.6, 0.5), 12);
      }
    };
  };

  /* ---------- POPLIMIT (ưu / nhược) ---------- */
  B.poplimit = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 2 · ƯU ĐIỂM & HẠN CHẾ</div>
        <h2 class="scene-title">Nhanh, nhưng <span class="warm">đại trà</span></h2></div>
      <div class="card card-pad" data-pro style="left:96px;top:290px;width:840px">
        <div class="card-kicker" style="color:var(--green)">${icon('check', 18)} ƯU ĐIỂM</div>
        <p style="margin-top:14px;font-size:19px;line-height:1.5">Luôn có kết quả, kể cả <b>người mới như C</b> chưa có lịch sử. Không cần dữ liệu cá nhân.</p>
      </div>
      <div class="card card-pad" data-con style="left:984px;top:290px;width:840px">
        <div class="card-kicker" style="color:var(--red)">${icon('alert', 18)} HẠN CHẾ</div>
        <p style="margin-top:14px;font-size:19px;line-height:1.5">Ai cũng nhận <b>một danh sách giống nhau</b> — theo số đông, không theo từng người.</p>
      </div>
      <div style="position:absolute;left:96px;top:520px;display:flex;gap:24px" data-cols>
        ${USERS.slice(0, 3).map((u, i) => `<div class="pers-col" data-col="${i}" style="width:250px">
          <div class="pc-av" style="background:${u.color}">${u.id}</div>
          <div class="pc-taste">${u.taste}</div>
          ${recCard('Galaxy S24', 'Bán chạy nhất', '#1')}
        </div>`).join('')}
      </div>
      <div class="matrix-note" data-note style="left:900px;top:560px"><span class="mn-x">≠</span> Số đông không phải cá nhân hóa → cần lọc cộng tác</div>`;
    const head = cam.querySelector('[data-head]');
    const pro = cam.querySelector('[data-pro]');
    const con = cam.querySelector('[data-con]');
    const cols = [...cam.querySelectorAll('[data-col]')];
    const note = cam.querySelector('[data-note]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(pro, U.p(0, 0.2, 0.6), 20);
        fade(con, U.p(0, 0.4, 0.6), 20);
        cols.forEach((c, i) => fade(c, U.p(0, 0.6 + i * 0.15, 0.5), 16));
        const w = U.p(1, 0.3, 0.6);
        cols[1].classList.toggle('warn', w > 0.4);
        fade(note, U.p(1, 0.7, 0.6), 14);
      }
    };
  };

  /* ---------- CFINTRO (đồ thị người–sản phẩm) ---------- */
  B.cfintro = (cam, def) => {
    const ux = [140, 320, 500, 680], iy = 470, uy = 330;
    const ix = [110, 250, 390, 530, 670];
    const edges = [[0, 0], [0, 1], [1, 0], [1, 2], [3, 0], [3, 1], [3, 2], [3, 4]];
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 3 · LỌC CỘNG TÁC</div>
        <h2 class="scene-title">Học từ những người <span class="accent">giống bạn</span></h2></div>
      <svg data-graph style="position:absolute;left:96px;top:250px" width="800" height="330" viewBox="0 0 800 330">
        ${edges.map((e, i) => `<line data-e="${i}" x1="${ux[e[0]]}" y1="${uy - 250 + 40}" x2="${ix[e[1]]}" y2="${iy - 250}" stroke="#C7D2FE" stroke-width="2.5"/>`).join('')}
        <line data-ad x1="${ux[0]}" y1="${uy - 250}" x2="${ux[3]}" y2="${uy - 250}" stroke="#06B6D4" stroke-width="4" stroke-dasharray="7 6"/>
        ${USERS.map((u, i) => `<g data-u="${i}"><circle cx="${ux[i]}" cy="${uy - 250}" r="30" fill="${u.color}"/><text x="${ux[i]}" y="${uy - 250 + 7}" text-anchor="middle" font-family="Quicksand" font-weight="700" font-size="22" fill="#fff">${u.id}</text></g>`).join('')}
        ${ITEMS.map((it, i) => `<g data-i="${i}"><rect x="${ix[i] - 26}" y="${iy - 250 - 26}" width="52" height="52" rx="12" fill="#EEF2FF" stroke="#C7D2FE"/><text x="${ix[i]}" y="${iy - 250 + 6}" text-anchor="middle" font-family="Jakarta" font-weight="700" font-size="16" fill="#4F46E5">${it.id}</text></g>`).join('')}
      </svg>
      <div style="position:absolute;left:960px;top:300px;width:864px;display:flex;flex-direction:column;gap:18px">
        <div class="card card-pad" data-ub style="position:relative;left:0;top:0"><div class="card-kicker">${icon('user', 18)} USER-BASED</div><p style="margin-top:10px;font-size:18px">Tìm <b>người</b> có gu giống bạn, mượn đánh giá của họ.</p></div>
        <div class="card card-pad" data-ib style="position:relative;left:0;top:0"><div class="card-kicker" style="color:var(--violet)">${icon('grid', 18)} ITEM-BASED</div><p style="margin-top:10px;font-size:18px">Tìm <b>sản phẩm</b> giống món bạn đã thích.</p></div>
        <div class="chip cyan-chip" data-knn style="align-self:flex-start">${icon('spark', 16)} Cần thước đo tương đồng → KNN</div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const es = [...cam.querySelectorAll('[data-e]')];
    const ad = cam.querySelector('[data-ad]');
    const us = [...cam.querySelectorAll('[data-u]')];
    const ub = cam.querySelector('[data-ub]');
    const ib = cam.querySelector('[data-ib]');
    const knn = cam.querySelector('[data-knn]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        es.forEach((e, i) => { e.style.opacity = U.p(0, 0.3 + i * 0.08, 0.4); });
        us.forEach((u, i) => { u.style.opacity = U.p(0, 0.2 + i * 0.1, 0.4); });
        const sim = U.p(1, 0.2, 0.6);
        ad.style.opacity = sim;
        us[0].style.filter = us[3].style.filter = sim > 0.4 ? 'drop-shadow(0 0 10px rgba(6,182,212,.7))' : 'none';
        fade(ub, U.p(1, 0.4, 0.5), 16);
        fade(ib, U.p(1, 0.7, 0.5), 16);
        fade(knn, U.p(2, 0.3, 0.5), 12);
      }
    };
  };

  /* ---------- KNN ---------- */
  B.knn = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 3 · KNN — K LÁNG GIỀNG GẦN NHẤT</div>
        <h2 class="scene-title">Đo tương đồng, <span class="accent">suy ô thiếu</span></h2></div>
      <div class="card card-pad" data-sim style="left:96px;top:300px;width:820px">
        <div class="card-kicker">${icon('user', 18)} ĐỘ TƯƠNG ĐỒNG (COSINE) · Ô CÙNG ĐÁNH GIÁ</div>
        <div style="display:flex;flex-direction:column;gap:14px;margin-top:18px">
          <div class="vec-row"><span class="vec-av" style="background:#2563EB">A</span><span class="vec-cell">5</span><span class="vec-cell">4</span><span class="vec-cell na">?</span><span class="vec-cell na">?</span><span class="vec-cell na">?</span></div>
          <div class="vec-row"><span class="vec-av" style="background:#06B6D4">D</span><span class="vec-cell">5</span><span class="vec-cell">4</span><span class="vec-cell">2</span><span class="vec-cell na">?</span><span class="vec-cell">5</span></div>
        </div>
        <div style="display:flex;align-items:center;gap:16px;margin-top:20px">
          <span class="cos-badge" data-cos>1.00</span>
          <span style="font-size:16px;color:var(--muted)">vector A, D trùng nhau trên I1, I2 → rất giống · K = 1</span>
        </div>
      </div>
      <div class="card card-pad" data-pred style="left:960px;top:300px;width:864px">
        <div class="card-kicker" style="color:var(--teal)">${icon('spark', 18)} DỰ ĐOÁN Ô THIẾU A × I5</div>
        <div style="display:flex;align-items:center;gap:18px;margin-top:20px">
          <span class="vec-av" style="background:#06B6D4">D</span><span class="vec-cell">5</span>
          <span data-arrow style="color:var(--teal)">${icon('arrow', 30)}</span>
          <span class="vec-av" style="background:#2563EB">A</span><span class="vec-cell" data-acell style="border-color:#67E8F9;background:#ECFEFF;color:#0E7490">?</span>
        </div>
        <div class="formula" data-f style="margin-top:20px">r̂(A,I5) = Σ sim·r / Σ sim = 5.0</div>
        <div class="chip amber-chip" data-dist style="margin-top:16px">${icon('alert', 16)} Đo tương đồng ≠ dự đoán điểm</div>
        <div class="chip violet-chip" data-item style="margin-top:12px">${icon('grid', 16)} Item-Based: đổi trục sang sản phẩm</div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const sim = cam.querySelector('[data-sim]');
    const cos = cam.querySelector('[data-cos]');
    const pred = cam.querySelector('[data-pred]');
    const acell = cam.querySelector('[data-acell]');
    const arrow = cam.querySelector('[data-arrow]');
    const f = cam.querySelector('[data-f]');
    const dist = cam.querySelector('[data-dist]');
    const item = cam.querySelector('[data-item]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(sim, U.p(0, 0.2, 0.6), 20);
        cos.style.opacity = U.p(1, 0.3, 0.6);
        fade(pred, U.p(2, 0.1, 0.6), 20);
        const pr = U.p(2, 0.6, 0.7);
        acell.textContent = pr > 0.5 ? '5.0' : '?';
        arrow.style.opacity = pr;
        fade(f, U.p(3, 0.2, 0.5), 12);
        fade(dist, U.p(3, 0.6, 0.5), 12);
        fade(item, U.p(4, 0.3, 0.5), 12);
      }
    };
  };

  /* ---------- SVD ---------- */
  B.svd = (cam, def) => {
    const A = MATRIX;
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 3 · SVD — PHÂN RÃ MA TRẬN</div>
        <h2 class="scene-title">Nén thành <span class="accent">yếu tố tiềm ẩn</span></h2></div>
      <div class="formula" data-formula style="position:absolute;left:96px;top:250px">A = U · Σ · Vᵀ</div>
      <div style="position:absolute;left:96px;top:340px;display:flex;align-items:center;gap:16px" data-decomp>
        <div class="fb"><div data-mA>${miniGrid(4, 5, 40, 4, '', (r, c) => A[r][c] == null ? '' : A[r][c])}</div><div class="fb-sub">Ma trận gốc A</div></div>
        <span class="svd-op">=</span>
        <div class="fb" data-u><div>${miniGrid(4, 3, 34, 4, '')}</div><div class="fb-label">U</div><div class="fb-sub">đặc trưng người dùng</div></div>
        <span class="svd-op">·</span>
        <div class="fb" data-s><div>${miniGrid(3, 3, 34, 4, 'sig', (r, c) => r === c ? 'σ' : '')}</div><div class="fb-label">Σ</div><div class="fb-sub">trọng số yếu tố</div></div>
        <span class="svd-op">·</span>
        <div class="fb" data-v><div>${miniGrid(3, 5, 34, 4, 'v')}</div><div class="fb-label">Vᵀ</div><div class="fb-sub">đặc trưng sản phẩm</div></div>
        <span class="svd-op">→</span>
        <div class="fb" data-rec><div data-mR>${miniGrid(4, 5, 40, 4, '', (r, c) => A[r][c] == null ? '' : A[r][c])}</div><div class="fb-sub">Tái tạo A ≈ UΣVᵀ</div></div>
      </div>
      <div class="card card-pad" data-latent style="left:1300px;top:300px;width:524px">
        <div class="card-kicker">${icon('layers', 18)} LATENT FACTORS</div>
        <div style="display:flex;flex-direction:column;gap:12px;margin-top:16px;font-size:16px">
          <div data-l>Hệ điều hành (Samsung / Apple)</div><div data-l>Mức cấu hình (RAM / ROM)</div><div data-l>Camera / pin</div>
        </div>
      </div>
      <div class="matrix-note" data-note style="left:96px;top:760px"><span class="mn-x">!</span> SVD nguyên bản cần ma trận đầy đủ</div>
      <div class="chip cyan-chip" data-mf style="position:absolute;left:760px;top:772px">${icon('gear', 16)} Thực tế: Matrix Factorization (FunkSVD) — chỉ học ô đã biết, không lấp 0</div>`;
    const head = cam.querySelector('[data-head]');
    const formula = cam.querySelector('[data-formula]');
    const decomp = cam.querySelector('[data-decomp]');
    const latent = cam.querySelector('[data-latent]');
    const ls = [...cam.querySelectorAll('[data-l]')];
    const note = cam.querySelector('[data-note]');
    const mf = cam.querySelector('[data-mf]');
    const recCells = [...cam.querySelectorAll('[data-mR] .fb-cell')];
    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.01})`,
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(latent, U.p(0, 0.2, 0.6), 20);
        ls.forEach((l, i) => fade(l, U.p(0, 0.4 + i * 0.15, 0.4), 10));
        fade(formula, U.p(1, 0.1, 0.5), 12);
        fade(decomp, U.p(1, 0.3, 0.8), 20);
        const rp = U.p(2, 0.3, 1.0);
        recCells.forEach((cell) => {
          const [r, c] = cell.dataset.fb.split('-').map(Number);
          if (A[r][c] == null) {
            cell.style.background = `rgba(6,182,212,${0.25 * rp})`;
            cell.style.borderColor = `rgba(103,232,249,${rp})`;
            cell.textContent = rp > 0.5 ? '·' : '';
            cell.style.color = '#0E7490';
          }
        });
        fade(note, U.p(3, 0.3, 0.5), 12);
        fade(mf, U.p(4, 0.3, 0.5), 12);
      }
    };
  };

  /* ---------- CFLIMITS ---------- */
  B.cflimits = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 3 · HAI BÀI TOÁN KHÓ</div>
        <h2 class="scene-title">Dữ liệu thưa & <span class="warm">khởi đầu lạnh</span></h2></div>
      <div class="card card-pad" data-sp style="left:96px;top:290px;width:840px">
        <div class="card-kicker" style="color:var(--red)">${icon('grid', 18)} DỮ LIỆU THƯA</div>
        <p style="margin-top:12px;font-size:18px;line-height:1.5">Quá ít ô được đánh giá → khó tìm láng giềng tin cậy.</p>
        <div style="margin-top:14px">${miniGrid(3, 6, 34, 5, '', (r, c) => (r * 6 + c) % 5 === 0 ? '★' : '')}</div>
      </div>
      <div class="card card-pad" data-cold style="left:984px;top:290px;width:840px">
        <div class="card-kicker" style="color:var(--red)">${icon('user', 18)} KHỞI ĐẦU LẠNH</div>
        <p style="margin-top:12px;font-size:18px;line-height:1.5">Người mới như <b>C</b> chưa có gì → lọc cộng tác bó tay.</p>
        <div class="pers-col" style="margin-top:14px;width:220px"><div class="pc-av" style="background:#64748B">C</div><div class="pc-taste">chưa tương tác</div></div>
      </div>
      <div class="card card-pad" data-cmp style="left:96px;top:640px;width:1728px">
        <div class="card-kicker">${icon('chart', 18)} SO SÁNH KNN vs SVD</div>
        <div style="display:flex;gap:40px;margin-top:14px;font-size:17px">
          <div style="flex:1"><b class="indigo">KNN</b> — dễ giải thích, nhưng nặng khi dữ liệu lớn.</div>
          <div style="flex:1"><b class="violet">SVD</b> — dự đoán tốt trên dữ liệu thưa, nhưng khó diễn giải.</div>
        </div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const sp = cam.querySelector('[data-sp]');
    const cold = cam.querySelector('[data-cold]');
    const cmp = cam.querySelector('[data-cmp]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(sp, U.p(0, 0.2, 0.6), 20);
        fade(cold, U.p(1, 0.2, 0.6), 20);
        fade(cmp, U.p(2, 0.2, 0.6), 20);
      }
    };
  };

  /* ---------- TFIDF ---------- */
  B.tfidf = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 4 · TF-IDF</div>
        <h2 class="scene-title">Biến mô tả thành <span class="accent">vector đặc trưng</span></h2></div>
      <div class="card card-pad" data-desc style="left:96px;top:290px;width:600px">
        <div class="card-kicker">${icon('phone', 18)} MÔ TẢ SẢN PHẨM</div>
        <p style="margin-top:14px;font-size:17px;line-height:1.7;font-family:'JetBrains'">"Galaxy S24 <b data-t>ram</b> <b data-t>12gb</b>, <b data-t>pin</b> <b data-t>5000</b>, <b data-t>camera</b> <b data-t>200mp</b>…"</p>
        <div class="chip cyan-chip" data-vec style="margin-top:18px">${icon('arrow', 16)} Mỗi sản phẩm → một vector</div>
      </div>
      <div class="card card-pad" data-terms style="left:744px;top:290px;width:1080px">
        <div class="card-kicker">${icon('chart', 18)} TF (trong mô tả) × IDF (nghịch đảo độ phổ biến)</div>
        <div style="display:flex;flex-direction:column;gap:12px;margin-top:18px">
          ${TERMS.map((t, i) => `<div class="term-row" data-t="${i}">
            <span class="term-word">${t.w}</span>
            <div class="term-bar"><div class="term-fill tf" data-tf style="width:0%"></div></div>
            <div class="term-bar"><div class="term-fill idf" data-idf style="width:0%"></div></div>
            <span class="term-score" data-sc>0</span>
          </div>`).join('')}
        </div>
        <div style="display:flex;gap:24px;margin-top:14px;font-size:13px;color:var(--muted)"><span><b class="indigo">■</b> TF</span><span><b class="cyan">■</b> IDF</span><span>điểm = TF×IDF</span></div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const desc = cam.querySelector('[data-desc]');
    const toks = [...cam.querySelectorAll('[data-t]')];
    const vec = cam.querySelector('[data-vec]');
    const terms = cam.querySelector('[data-terms]');
    const rows = [...cam.querySelectorAll('.term-row')];
    const tfs = [...cam.querySelectorAll('[data-tf]')];
    const idfs = [...cam.querySelectorAll('[data-idf]')];
    const scs = [...cam.querySelectorAll('[data-sc]')];
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(desc, U.p(0, 0.2, 0.6), 20);
        toks.forEach((t, i) => { t.style.color = U.p(0, 0.5 + i * 0.1, 0.3) > 0.5 ? 'var(--indigo)' : 'inherit'; });
        fade(terms, U.p(1, 0.1, 0.6), 20);
        const g = U.p(1, 0.4, 1.2);
        TERMS.forEach((t, i) => {
          tfs[i].style.width = (t.tf * 100 * g) + '%';
          idfs[i].style.width = (t.idf * 100 * g) + '%';
          scs[i].textContent = (t.tf * t.idf * g).toFixed(2);
        });
        const hi = U.p(2, 0.3, 0.7);
        rows.forEach((r, i) => r.classList.toggle('hi', hi > 0.4 && TERMS[i].idf > 0.5));
        fade(vec, U.p(2, 0.6, 0.5), 12);
      }
    };
  };

  /* ---------- COSINE ---------- */
  B.cosine = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 4 · COSINE SIMILARITY</div>
        <h2 class="scene-title">Đo <span class="accent">góc giữa hai vector</span></h2></div>
      <div class="card card-pad" data-plot style="left:96px;top:290px;width:820px;height:470px">
        <div class="card-kicker">${icon('chart', 18)} VECTOR SỞ THÍCH vs VECTOR SẢN PHẨM</div>
        <svg width="760" height="380" viewBox="0 0 760 380" style="margin-top:8px">
          <line x1="60" y1="330" x2="720" y2="330" stroke="#E2E8F0" stroke-width="2"/>
          <line x1="60" y1="330" x2="60" y2="30" stroke="#E2E8F0" stroke-width="2"/>
          <path data-arc fill="none" stroke="#F59E0B" stroke-width="3"/>
          <line data-vu x1="60" y1="330" x2="60" y2="330" stroke="#4F46E5" stroke-width="5" stroke-linecap="round"/>
          <line data-vp x1="60" y1="330" x2="60" y2="330" stroke="#06B6D4" stroke-width="5" stroke-linecap="round"/>
          <text data-lu font-family="Quicksand" font-weight="700" font-size="18" fill="#4F46E5">A</text>
          <text data-lp font-family="Quicksand" font-weight="700" font-size="18" fill="#0E7490">Xiaomi 14</text>
          <text data-cos font-family="Quicksand" font-weight="700" font-size="26" fill="#0F172A">cos θ = 0.98</text>
        </svg>
      </div>
      <div style="position:absolute;left:960px;top:290px;width:864px;display:flex;flex-direction:column;gap:16px">
        <div class="card card-pad" data-attr style="position:relative;left:0;top:0">
          <div class="card-kicker" style="color:var(--teal)">${icon('check', 18)} THUỘC TÍNH A MUỐN</div>
          <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap"><span class="chip">RAM 12GB</span><span class="chip">ROM 256GB</span><span class="chip">pin 5000mAh</span></div>
          <p style="margin-top:12px;font-size:17px;color:var(--muted)">Khớp nhất → <b class="teal">Xiaomi 14</b>. Góc nhỏ = giống.</p>
        </div>
        <div class="chip violet-chip" data-feat style="align-self:flex-start">${icon('gear', 16)} Số / danh mục → Feature-Based Similarity</div>
        <div class="matrix-note" data-over style="position:relative;left:0;top:0"><span class="mn-x">!</span> Over-specialization: cứ na ná món đã xem</div>
      </div>`;
    const head = cam.querySelector('[data-head]');
    const plot = cam.querySelector('[data-plot]');
    const vu = cam.querySelector('[data-vu]');
    const vp = cam.querySelector('[data-vp]');
    const lu = cam.querySelector('[data-lu]');
    const lp = cam.querySelector('[data-lp]');
    const arc = cam.querySelector('[data-arc]');
    const cosT = cam.querySelector('[data-cos]');
    const attr = cam.querySelector('[data-attr]');
    const feat = cam.querySelector('[data-feat]');
    const over = cam.querySelector('[data-over]');
    const polar = (ang, r) => [60 + r * Math.cos(ang), 330 - r * Math.sin(ang)];
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(plot, U.p(0, 0.2, 0.6), 20);
        const au = 0.42;
        const ap = lerp(1.15, 0.5, U.p(1, 0.3, 1.2));
        const [ux, uy] = polar(au, 300); const [px, py] = polar(ap, 280);
        vu.setAttribute('x2', ux); vu.setAttribute('y2', uy);
        vp.setAttribute('x2', px); vp.setAttribute('y2', py);
        lu.setAttribute('x', ux + 8); lu.setAttribute('y', uy - 8);
        lp.setAttribute('x', px + 8); lp.setAttribute('y', py - 8);
        const [a1x, a1y] = polar(au, 90); const [a2x, a2y] = polar(ap, 90);
        arc.setAttribute('d', `M ${a1x} ${a1y} A 90 90 0 0 0 ${a2x} ${a2y}`);
        const cv = Math.cos(ap - au);
        cosT.textContent = 'cos θ = ' + cv.toFixed(2);
        cosT.setAttribute('x', 480); cosT.setAttribute('y', 60);
        fade(attr, U.p(1, 0.2, 0.6), 16);
        fade(feat, U.p(2, 0.3, 0.5), 12);
        fade(over, U.p(3, 0.3, 0.6), 14);
      }
    };
  };

  /* ---------- WEIGHTED ---------- */
  B.weighted = (cam, def) => {
    const tags = ['S_CF · cộng tác', 'S_CB · nội dung', 'S_POP · phổ biến'];
    const vals = [0.9, 0.8, 0.5];
    const ws = [0.5, 0.3, 0.2];
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 5 · WEIGHTED HYBRID</div>
        <h2 class="scene-title">Trộn điểm <span class="accent">theo trọng số</span></h2></div>
      <div class="formula" data-f style="position:absolute;left:96px;top:250px">Score = 0.5·S_CF + 0.3·S_CB + 0.2·S_POP</div>
      <div style="position:absolute;left:96px;top:340px;display:flex;gap:24px" data-srcs>
        ${tags.map((t, i) => `<div class="src-card" data-s="${i}" style="width:280px">
          <span class="sc-tag">${t}</span><span class="sc-val" data-v>${vals[i].toFixed(1)}</span>
          <span class="sc-w" data-w>× ${ws[i].toFixed(1)}</span>
          <span style="font-size:12px;color:var(--muted)">đã chuẩn hóa [0,1]</span>
        </div>`).join('')}
      </div>
      <div style="position:absolute;left:1010px;top:340px;display:flex;align-items:center;gap:24px">
        <span data-arrow style="color:var(--indigo)">${icon('arrow', 40)}</span>
        <div class="card card-pad" data-mix style="position:relative;left:0;top:0;width:300px;align-items:center;display:flex;flex-direction:column;gap:8px">
          <div class="card-kicker">${icon('gear', 18)} BỘ TRỘN</div>
          <span class="result-big" data-res>0.79</span>
          <span style="font-size:13px;color:var(--muted)">điểm xếp hạng cuối</span>
        </div>
      </div>
      <div class="matrix-note" data-norm style="left:96px;top:640px"><span class="mn-x">!</span> Bắt buộc chuẩn hóa về cùng thang đo trước khi trộn</div>
      <div class="chip cyan-chip" data-calc style="position:absolute;left:96px;top:730px">${icon('check', 16)} 0.5×0.9 + 0.3×0.8 + 0.2×0.5 = 0.45+0.24+0.10 = 0.79</div>`;
    const head = cam.querySelector('[data-head]');
    const f = cam.querySelector('[data-f]');
    const srcs = [...cam.querySelectorAll('[data-s]')];
    const arrow = cam.querySelector('[data-arrow]');
    const mix = cam.querySelector('[data-mix]');
    const res = cam.querySelector('[data-res]');
    const norm = cam.querySelector('[data-norm]');
    const calc = cam.querySelector('[data-calc]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(f, U.p(1, 0.1, 0.5), 12);
        srcs.forEach((s, i) => fade(s, U.p(1, 0.3 + i * 0.2, 0.5), 16));
        const mp = U.p(2, 0.3, 0.8);
        arrow.style.opacity = mp;
        fade(mix, U.p(2, 0.4, 0.6), 16);
        res.textContent = (0.79 * mp).toFixed(2);
        fade(calc, U.p(2, 0.8, 0.5), 12);
        fade(norm, U.p(3, 0.3, 0.6), 14);
      }
    };
  };

  /* ---------- SWITCHING ---------- */
  B.switching = (cam, def) => {
    const br = [
      ['Người mới (C) · chưa dữ liệu', 'Popularity', 'var(--amber)'],
      ['Có lịch sử xem', 'Content-Based', 'var(--cyan)'],
      ['Đủ tương tác', 'SVD / KNN', 'var(--indigo)']
    ];
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 5 · SWITCHING HYBRID</div>
        <h2 class="scene-title">Đổi phương pháp <span class="accent">theo lượng dữ liệu</span></h2></div>
      <div class="chip dark-chip" data-in style="position:absolute;left:96px;top:280px">${icon('db', 16)} Lượng dữ liệu người dùng → chọn nhánh</div>
      <div style="position:absolute;left:96px;top:360px;display:flex;gap:28px" data-brs>
        ${br.map((b, i) => `<div class="sw-branch" data-b="${i}" style="width:540px">
          <span class="sw-cond">${b[0]}</span>
          <span class="sw-meth" style="color:${b[2]}">${b[1]}</span>
          <div class="lb-bar"><div class="lb-fill" data-on style="width:0%;background:${b[2]}"></div></div>
        </div>`).join('')}
      </div>
      <div class="matrix-note" data-note style="left:96px;top:600px"><span class="mn-x">✓</span> Không trộn — chuyển nhánh; luôn có phương án phù hợp mỗi giai đoạn</div>`;
    const head = cam.querySelector('[data-head]');
    const inp = cam.querySelector('[data-in]');
    const brs = [...cam.querySelectorAll('[data-b]')];
    const ons = [...cam.querySelectorAll('[data-on]')];
    const note = cam.querySelector('[data-note]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        fade(inp, U.p(0, 0.3, 0.5), 12);
        brs.forEach((b, i) => fade(b, U.p(0, 0.4 + i * 0.15, 0.5), 16));
        const t = U.raw(1, 0.2, 3.0);
        brs.forEach((b, i) => {
          const on = clamp(t * 3 - i);
          b.classList.toggle('on', on > 0.5);
          ons[i].style.width = (on * 100) + '%';
        });
        fade(note, U.p(2, 0.3, 0.6), 14);
      }
    };
  };

  /* ---------- CASCADE ---------- */
  B.cascade = (cam, def) => {
    const sorted = [...CAS].sort((a, b) => b.final - a.final);
    const panel = (title, rows, key) => `<div class="stage-panel" data-st style="width:400px">
      <span class="st-title">${title}</span>
      ${rows.map((r) => `<div class="stage-row ${key === 'final' && r.id === 'I5' ? 'top' : ''} ${r.owned && key === 'final' ? 'owned' : ''}"><span class="sr-name">${r.name}</span><span class="sr-val">${key ? r[key].toFixed(2) : ''}</span></div>`).join('')}
    </div>`;
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 5 · CASCADE HYBRID</div>
        <h2 class="scene-title">Lọc <span class="accent">theo tầng</span></h2></div>
      <div style="position:absolute;left:96px;top:300px;display:flex;gap:20px;align-items:stretch" data-stages>
        ${panel('1 · ỨNG VIÊN', CAS, null)}
        ${panel('2 · SVD DỰ ĐOÁN', CAS, 'svd')}
        ${panel('3 · NỘI DUNG', CAS, 'cb')}
        ${panel('4 · XẾP HẠNG TOP 5', sorted, 'final')}
      </div>
      <div style="position:absolute;left:96px;top:640px;display:flex;gap:16px" data-cmp>
        <span class="chip">Weighted · trộn điểm</span><span class="chip cyan-chip">Switching · chọn một</span><span class="chip violet-chip">Cascade · nối tiếp</span>
      </div>
      <div class="matrix-note" data-note style="left:96px;top:720px"><span class="mn-x">✓</span> Hệ thống thực tế kết hợp cả ba: chuyển theo dữ liệu → lọc tầng → trộn điểm</div>`;
    const head = cam.querySelector('[data-head]');
    const sts = [...cam.querySelectorAll('[data-st]')];
    const cmp = [...cam.querySelectorAll('[data-cmp] .chip')];
    const note = cam.querySelector('[data-note]');
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        sts.forEach((s, i) => fade(s, U.p(1, 0.2 + i * 0.5, 0.5), 16));
        cmp.forEach((c, i) => fade(c, U.p(2, 0.2 + i * 0.2, 0.4), 12));
        fade(note, U.p(3, 0.3, 0.6), 14);
      }
    };
  };

  /* ---------- RECAP ---------- */
  B.recap = (cam, def) => {
    const R = [
      ['Cá nhân hóa', 'Hành vi → hồ sơ sở thích'],
      ['Phổ biến', 'Nhanh nhưng đại trà'],
      ['Cộng tác', 'Học từ người giống bạn'],
      ['Nội dung', 'Học từ chính sản phẩm'],
      ['Hybrid', 'Kết hợp: chính xác + linh hoạt']
    ];
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">PHẦN 6 · TỔNG KẾT</div>
        <h2 class="scene-title">Năm điều <span class="accent">mang về</span></h2></div>
      <div style="position:absolute;left:96px;top:320px;display:flex;gap:22px" data-row>
        ${R.map((r, i) => `<div class="goal-card" data-g="${i}" style="position:relative;width:316px"><div class="g-num">${pad(i + 1)}</div><div class="g-title">${r[0]}</div><div class="g-sub">${r[1]}</div></div>`).join('')}
      </div>
      <div class="chip amber-chip" data-close style="position:absolute;left:96px;top:640px">${icon('spark', 16)} Hiểu bản chất thuật toán → chọn đúng cách kết hợp</div>`;
    const head = cam.querySelector('[data-head]');
    const gs = [...cam.querySelectorAll('[data-g]')];
    const close = cam.querySelector('[data-close]');
    return {
      cam: (t) => `scale(${1 + ease(t / def.dur) * 0.012})`,
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        gs.forEach((g, i) => fade(g, U.p(0, 0.3 + i * 0.25, 0.5), 20));
        fade(close, U.p(1, 0.3, 0.6), 12);
      }
    };
  };

  /* ---------- QUIZ ---------- */
  B.quiz = (cam, def) => {
    const QS = [
      { q: 'Ô trống trong ma trận nghĩa là gì?', o: ['Điểm 0', 'Chưa tương tác', 'Sản phẩm lỗi'], a: 1, ex: 'Chưa tương tác, không phải điểm 0. Lấp 0 sẽ làm sai dự đoán.' },
      { q: 'Người mới chưa có lịch sử, ưu tiên phương pháp nào?', o: ['SVD', 'KNN', 'Lọc phổ biến'], a: 2, ex: 'Lọc phổ biến — cách Switching Hybrid xử lý khởi đầu lạnh.' },
      { q: 'Chiến lược nào trộn điểm theo trọng số?', o: ['Switching', 'Weighted', 'Cascade'], a: 1, ex: 'Weighted Hybrid. Nhớ chuẩn hóa điểm trước khi trộn.' }
    ];
    cam.innerHTML = `
      <div class="scene-head" data-head><div class="eyebrow">ÔN TẬP · KIỂM TRA NHANH</div>
        <h2 class="scene-title">Ba câu hỏi <span class="accent">củng cố</span></h2></div>
      ${QS.map((q, k) => `<div class="quiz-card" data-q="${k}" style="display:none">
        <div class="quiz-q">${q.q}</div>
        <svg class="quiz-ring" viewBox="0 0 86 86"><circle cx="43" cy="43" r="38" fill="none" stroke="#E2E8F0" stroke-width="7"/><circle class="ring-fill" cx="43" cy="43" r="38" fill="none" stroke="#4F46E5" stroke-width="7" stroke-linecap="round" stroke-dasharray="238.8" stroke-dashoffset="0" transform="rotate(-90 43 43)"/><text class="num3" x="43" y="52" text-anchor="middle">3</text></svg>
        <div class="quiz-opts">${q.o.map((o, i) => `<div class="q-option" data-o="${i}"><span class="qo-key">${'ABC'[i]}</span>${o}</div>`).join('')}</div>
        <div class="q-explain" data-ex>${icon('check', 18)} ${q.ex}</div>
      </div>`).join('')}`;
    const head = cam.querySelector('[data-head]');
    const cards = [...cam.querySelectorAll('[data-q]')];
    return {
      update(U) {
        fade(head, U.p(0, 0, 0.5), 16);
        const k = U.on(4) ? 2 : U.on(2) ? 1 : 0;
        cards.forEach((c, i) => { c.style.display = i === k ? 'block' : 'none'; });
        const g = cards[k];
        const q = QS[k];
        const qEnd = U.cueEnd(2 * k);
        const aStart = U.cueStart(2 * k + 1);
        const hold = Math.max(0.01, aStart - qEnd);
        const p = clamp((U.t - qEnd) / hold);
        const answered = U.on(2 * k + 1);
        const ring = g.querySelector('.ring-fill');
        const ringBox = g.querySelector('.quiz-ring');
        const num = g.querySelector('.num3');
        ring.style.strokeDashoffset = 238.8 * p;
        const showRing = U.t >= qEnd && !answered;
        ringBox.style.opacity = showRing ? 1 : 0;
        num.style.opacity = showRing ? 1 : 0;
        num.textContent = String(Math.max(1, Math.ceil(3 * (1 - p))));
        g.querySelectorAll('.q-option').forEach((o, i) => {
          o.classList.toggle('correct', answered && i === q.a);
          o.classList.toggle('dim', answered && i !== q.a);
        });
        const ex = g.querySelector('[data-ex]');
        ex.style.opacity = answered ? 1 : 0;
        ex.style.transform = `translateY(${answered ? 0 : 8}px)`;
      }
    };
  };

  /* ============================================================
     BUILD
     ============================================================ */
  const built = [];
  TL.scenes.forEach((def) => {
    const el = h('div', 'scene sc-' + def.type);
    el.style.opacity = 0;
    const cam = h('div', 'cam');
    el.appendChild(cam);
    root.appendChild(el);
    const builder = B[def.type];
    if (!builder) {
      cam.innerHTML = `<div class="scene-head"><div class="eyebrow">PHẦN ${def.part || ''}</div><h2 class="scene-title">${def.title}</h2></div>`;
      console.warn('missing builder', def.type);
    }
    const api = builder ? builder(cam, def) : null;
    const cues = def.cues.map((c) => ({ ...c, ls: c.start - def.start, le: c.end - def.start }));
    built.push({ def, el, cam, api, cues });
  });

  /* ---------- global decor ---------- */
  const floatRoot = document.getElementById('floating');
  const chips = [];
  const palette = ['#4F46E5', '#06B6D4', '#F59E0B', '#7C3AED', '#C7D2FE', '#A5F3FC'];
  let seed = 11;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  for (let i = 0; i < 22; i++) {
    const d = h('div', 'float-chip');
    const w = 12 + rnd() * 28;
    d.style.width = w + 'px';
    d.style.height = (9 + rnd() * 24) + 'px';
    d.style.background = palette[i % palette.length];
    d.style.opacity = 0.14 + rnd() * 0.18;
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
      prev = cur; cur = idx;
      built.forEach((b, i) => {
        if (i === cur) b.el.classList.add('on');
        if (i !== cur && i !== prev) { b.el.classList.remove('on'); b.el.style.opacity = 0; }
      });
      const sc = TL.scenes[idx];
      if (sc.part) partChip.textContent = 'PHẦN ' + pad(sc.part) + ' · ' + PARTS[sc.part];
      else if (sc.id === 'quiz') partChip.textContent = 'ÔN TẬP · REVIEW';
      else if (sc.id === 'outro') partChip.textContent = 'KẾT THÚC · WRAP-UP';
      else partChip.textContent = 'BÀI GIẢNG · GỢI Ý SẢN PHẨM';
      document.body.classList.toggle('dark-chrome', sc.type === 'divider');
      sweep.style.background = sc.part === 3 || sc.part === 5
        ? 'linear-gradient(100deg, rgba(124,58,237,0) 0%, rgba(124,58,237,.20) 34%, rgba(79,70,229,.32) 50%, rgba(124,58,237,.20) 66%, rgba(124,58,237,0) 100%)'
        : 'linear-gradient(100deg, rgba(79,70,229,0) 0%, rgba(79,70,229,.16) 34%, rgba(6,182,212,.32) 50%, rgba(79,70,229,.16) 66%, rgba(79,70,229,0) 100%)';
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

    const sp = smooth(local / 0.7);
    sweep.style.transform = `translateX(${(-100 + sp * 200).toFixed(2)}%)`;
    sweep.style.opacity = sp > 0.02 && sp < 0.98 ? (0.5 * Math.sin(Math.PI * sp)).toFixed(3) : 0;

    blobA.style.transform = `translate(${Math.sin(t * 0.16) * 50}px,${Math.cos(t * 0.13) * 34}px)`;
    blobB.style.transform = `translate(${Math.cos(t * 0.12 + 2) * 60}px,${Math.sin(t * 0.15) * 40}px)`;
    blobC.style.transform = `translate(${Math.sin(t * 0.1 + 4) * 70}px,${Math.cos(t * 0.11) * 30}px)`;
    chips.forEach((c) => {
      const x = c.x + Math.sin(t * 0.12 * c.s + c.ph) * 40;
      const y = c.y + Math.cos(t * 0.1 * c.s + c.ph) * 30;
      c.el.style.transform = `translate(${x}px,${y}px) rotate(${c.rot + t * 4 * c.s}deg)`;
    });

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

    fill.style.width = (100 * t / TL.duration).toFixed(2) + '%';
    plabel.textContent = fmt(t);
    tcode.textContent = fmt(t) + ' / ' + fmt(TL.duration);
  }

  window.renderFrame = renderFrame;
  window.__ready = true;
  window.__sceneAt = (id) => built.findIndex((b) => b.def.id === id);
  window.__built = built;
})();