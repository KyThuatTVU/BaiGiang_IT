/* ============================================================
   AN TECH ACADEMY — NGÔN NGỮ & FRAMEWORK BACKEND
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
  const smooth = (p) => { p = clamp(p); return p * p * (3 - 2 * p); };
  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (s) => `${pad(Math.floor(s / 60))}:${pad(Math.floor(s % 60))}`;

  const PARTS = {
    1: 'BACKEND',
    2: 'LANGUAGE VS FRAMEWORK',
    3: 'BẢY HỆ SINH THÁI',
    4: 'SO SÁNH & LỰA CHỌN',
    5: 'BACKEND IN ACTION',
    6: 'TỔNG KẾT'
  };

  /* ---------- icons ---------- */
  const P = {
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    browser: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    gate: '<path d="M4 21V8l8-5 8 5v13"/><path d="M8 21v-8h8v8M12 10v3"/>',
    server: '<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01M12 7h5M12 17h5"/>',
    db: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7"/>',
    shield: '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 10-4.6-1.6-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/>',
    gear: '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
    check: '<path d="M20 6L9 17l-5-5"/>',
    alert: '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    key: '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 3h4v4M14 6l2 2"/>',
    lock: '<rect x="4" y="10" width="16" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
    cart: '<circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M3 4h2l2.4 11h11.2L21 7H6"/>',
    card: '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20M6 15h4"/>',
    code: '<path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/>',
    layers: '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 12l10 5 10-5M2 17l10 5 10-5"/>',
    spark: '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4L12 3z"/>',
    box: '<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>',
    cloud: '<path d="M17 18a5 5 0 0 0 .9-9.9A7 7 0 0 0 4.3 10 4 4 0 0 0 6 18z"/>',
    bolt: '<path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/>',
    book: '<path d="M4 4h7a3 3 0 0 1 3 3v13a3 3 0 0 0-3-3H4zM20 4h-4a3 3 0 0 0-3 3v13a3 3 0 0 1 3-3h4z"/>',
    terminal: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M7 9l4 3-4 3M13 15h4"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    phone: '<rect x="7" y="2" width="10" height="20" rx="3"/><path d="M11 18h2"/>',
    chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    wave: '<path d="M2 12c2-6 4-6 6 0s4 6 6 0 4-6 6 0"/>',
    coffee: '<path d="M4 8h12v7a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 9h2a3 3 0 0 1 0 6h-2M7 3v2M11 3v2"/>',
    gem: '<path d="M6 3h12l4 6-10 12L2 9z"/><path d="M2 9h20M8 3l4 6 4-6M8 9l4 12 4-12"/>',
    hat: '<path d="M3 18h18M5 18c1-4 3-9 7-9s6 5 7 9M9 9h6"/>',
    play: '<path d="M8 5l12 7-12 7z"/>',
    restart: '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5"/>'
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
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const KW = new Set('import from export default const let var function return if else new await async class extends public private protected static void try catch throw interface type use require package func def end do for while'.split(' '));
  function tokenize(line) {
    let out = '', i = 0;
    const re = /(\/\/.*$|#.*$)|('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`[^`]*`)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/g;
    let m;
    while ((m = re.exec(line))) {
      out += esc(line.slice(i, m.index));
      if (m[1]) out += `<span class="tok-com">${esc(m[1])}</span>`;
      else if (m[2]) out += `<span class="tok-str">${esc(m[2])}</span>`;
      else if (m[3]) out += `<span class="tok-num">${m[3]}</span>`;
      else if (m[4]) {
        const w = m[4];
        if (KW.has(w)) out += `<span class="tok-kw">${esc(w)}</span>`;
        else if (/^[ \t]*\(/.test(line.slice(m.index + w.length))) out += `<span class="tok-fn">${esc(w)}</span>`;
        else if (w[0] === w[0].toUpperCase() && /[a-z]/.test(w)) out += `<span class="tok-var">${esc(w)}</span>`;
        else out += esc(w);
      }
      i = m.index + m[0].length;
    }
    out += esc(line.slice(i));
    return out;
  }
  function codePanel(lines, o = {}) {
    const el = h('div', 'code-panel' + (o.compact ? ' compact' : ''));
    const ph = o.h || (o.compact ? 34 + 24 + lines.length * 21 : 38 + 30 + lines.length * 26.4);
    el.style.cssText = `left:${o.x}px;top:${o.y}px;width:${o.w}px;height:${Math.round(ph)}px`;
    el.innerHTML = `<div class="code-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="code-name">${o.name || 'server.js'}</span><span class="code-badge">${o.badge || 'NODE.JS'}</span></div>
      <div class="code-body">${lines.map((l, i) => `<div class="code-line" data-l="${i}"><span class="ln">${i + 1}</span><span>${tokenize(l)}</span></div>`).join('')}</div>`;
    return el;
  }
  const setHot = (panel, idx, selectors) => {
    panel.querySelectorAll('.code-line').forEach((l) => {
      const i = +l.dataset.l;
      l.classList.toggle('hot', idx.includes(i));
      l.classList.toggle('dim', idx.length > 0 && !idx.includes(i) && selectors === 'dim');
    });
  };

  const LOGOS = {
    javascript: ['javascript', '#EAB308'], typescript: ['typescript', '#3178C6'],
    node: ['nodedotjs', '#5FA04E'], express: ['express', '#475569'], nestjs: ['nestjs', '#E0234E'],
    fastify: ['fastify', '#0F172A'], python: ['python', '#3776AB'], django: ['django', '#0C4B33'],
    flask: ['flask', '#334155'], fastapi: ['fastapi', '#059669'], php: ['php', '#777BB4'],
    laravel: ['laravel', '#FF2D20'], symfony: ['symfony', '#1F2937'], codeigniter: ['codeigniter', '#EF4223'],
    java: ['java', '#E76F00'], springboot: ['springboot', '#6DB33F'], quarkus: ['quarkus', '#4695EB'],
    micronaut: ['micronaut', '#0F172A'], dotnet: ['dotnet', '#512BD4'], csharp: ['csharp', '#512BD4'],
    go: ['go', '#00ADD8'], gin: ['gin', '#008ECF'], echo: ['echo', '#0F172A'], fiber: ['fiber', '#00ACD7'],
    ruby: ['ruby', '#CC342D'], rails: ['rubyonrails', '#CC0000'], sinatra: ['sinatra', '#0F172A'],
    mysql: ['mysql', '#4479A1'], postgres: ['postgresql', '#4169E1'], mongodb: ['mongodb', '#47A248'],
    redis: ['redis', '#DC382D']
  };
  const logo = (key, size = 36, color) => {
    const [file, c] = LOGOS[key];
    return `<span class="logo-mark" style="width:${size}px;height:${size}px;--logo:url('../assets/logos/${file}.svg');color:${color || c}"></span>`;
  };
  const logoWrap = (key, size = 54, opts = {}) => {
    const [, c] = LOGOS[key];
    return `<span class="logo-wrap ${opts.sm ? 'sm' : ''}" style="width:${size}px;height:${size}px;background:${opts.bg || c + '12'};border-color:${opts.border || c + '2E'}">${logo(key, Math.round(size * 0.54), c)}</span>`;
  };

  /* ---------- TEACHER ---------- */
  let uid = 0;
  function teacher(opts = {}) {
    const id = 't' + (++uid);
    const el = h('div', 'teacher ' + (opts.cls || ''));
    if (opts.style) el.style.cssText += opts.style;
    el.innerHTML = `
      <svg viewBox="0 0 300 400" aria-hidden="true">
        <defs><linearGradient id="shirt-${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3B82F6"/><stop offset="1" stop-color="#1D4ED8"/></linearGradient></defs>
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

  /* ---------- PIECES ---------- */
  function browser(body, url = 'nova.vn') {
    return `<div class="browser" style="height:100%"><div class="browser-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="url">${url}</span></div><div class="browser-body">${body}</div></div>`;
  }
  function shopMini(compact = false) {
    return `<div class="shop">
      <div class="shop-nav"><div class="shop-logo"><span class="mark"></span>NOVA SHOP</div><div class="shop-links"><span>Trang chủ</span><span>Sản phẩm</span><span>Sale</span></div><div class="shop-cart">Giỏ hàng · 2</div></div>
      <div class="shop-body">
        <div class="shop-hero"><div class="shop-hero-copy"><div class="shop-h">Tai nghe Aurora X</div><div class="shop-p">Chống ồn chủ động · pin 40 giờ</div><div class="shop-cta-row"><span class="btn btn-amber">Mua ngay</span><span class="btn btn-secondary">Chi tiết</span></div></div><div class="shop-art" style="${compact ? 'width:105px;height:82px' : ''}"><div class="phone" style="${compact ? 'width:36px;height:62px;top:9px' : ''}"></div></div></div>
        <div class="shop-grid">
          ${['Aurora Buds|1.290.000', 'Nova Watch|3.490.000', 'Flux Pad|2.150.000'].map((x) => { const [n, p] = x.split('|'); return `<div class="shop-card"><div class="thumb"></div><div class="name">${n}</div><div class="price">${p} đ</div></div>`; }).join('')}
        </div>
      </div>
    </div>`;
  }
  function loginModal() {
    return `<div class="login-modal"><div class="login-box">
      <div class="login-title">Đăng nhập</div><div class="login-sub">Chào mừng trở lại NOVA SHOP</div>
      <div class="field focus"><span class="ph">Email</span><span class="typed" data-email></span><span class="cur" style="width:1px;height:15px;background:#2563EB;display:inline-block"></span></div>
      <div class="field"><span class="ph">Mật khẩu</span><span data-pass style="letter-spacing:.12em;color:#334155"></span></div>
      <div class="field"><span data-dot style="width:8px;height:8px;border-radius:50%;background:#10B981;display:inline-block"></span><span class="ph">Ghi nhớ đăng nhập</span></div>
      <div class="login-btn" data-login>Đăng nhập</div>
      <div class="login-note">Mật khẩu được gửi qua HTTPS và băm ở server</div>
      <svg class="cursor" data-cursor viewBox="0 0 24 32" style="left:190px;top:238px"><path d="M2 2l18 14-8 2-4 8z" fill="#fff" stroke="#0F172A" stroke-width="2"/></svg>
      <div class="pulse-ring" data-ring style="width:70px;height:70px;left:140px;top:222px"></div>
    </div></div>`;
  }
  function rack() {
    return `<div class="rack"><div class="rack-unit"><span class="led"></span><span class="led b"></span><span class="led a"></span><span class="slot"></span></div>
      <div class="rack-unit"><span class="led b"></span><span class="led"></span><span class="led"></span><span class="slot"></span></div>
      <div class="rack-unit"><span class="led"></span><span class="led a"></span><span class="led b"></span><span class="slot"></span></div>
      <div class="rack-label">APPLICATION SERVER</div></div>`;
  }
  function dbCyl(label = 'DATABASE') {
    return `<div class="db"><div class="cyl"></div><div class="top"></div><div class="bot"></div><div class="band" style="top:58px"></div><div class="band" style="top:98px"></div><div class="db-label">${label}</div></div>`;
  }

  /* ============================================================
     SCENES
     ============================================================ */
  const B = {};

  /* ---------- 01 INTRO ---------- */
  B.intro = (cam, def) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1080px">
        <div class="eyebrow">AN TECH ACADEMY · BÀI GIẢNG</div>
        <h1 class="scene-title" style="font-size:66px;line-height:1.02">Backend<br><span class="accent" style="font-size:42px;letter-spacing:.01em" data-sub>ngôn ngữ &amp; framework</span></h1>
        <p class="scene-sub" style="max-width:760px" data-lead>Từ một cú click đăng nhập đến database — hiểu bản chất trước khi chọn công cụ.</p>
      </div>
      <div style="position:absolute;left:96px;top:424px;width:690px;height:396px" data-browser>${browser(shopMini() + loginModal(), 'nova.vn/dang-nhap')}</div>
      <div style="position:absolute;left:1046px;top:300px">${rack()}</div>
      <div style="position:absolute;left:1300px;top:430px">${dbCyl()}</div>
      <svg style="position:absolute;inset:0;width:1920px;height:1080px;z-index:3;overflow:visible" viewBox="0 0 1920 1080">
        <path data-beam1 d="M786 600 C 880 560, 950 430, 1046 410" fill="none" stroke="rgba(37,99,235,.35)" stroke-width="3" stroke-dasharray="8 10"/>
        <path data-beam2 d="M1236 410 C 1270 430, 1280 470, 1300 500" fill="none" stroke="rgba(6,182,212,.4)" stroke-width="3" stroke-dasharray="8 10"/>
      </svg>
      <div class="packet" data-packet style="left:780px;top:592px;opacity:0"><span class="trail"></span><span class="core"></span></div>
      <div style="position:absolute;left:96px;top:840px;display:flex;gap:12px;align-items:center" data-badges>
        ${['javascript', 'python', 'php', 'java', 'csharp', 'go', 'ruby'].map((k, i) => `<div style="display:flex;align-items:center;gap:7px;padding:6px 11px 6px 8px;border-radius:11px;background:#fff;border:1px solid #E1ECF8;box-shadow:0 8px 18px rgba(37,99,235,.06)" data-badge="${i}">${logoWrap(k, 30, { sm: true })}<span style="font-family:Quicksand;font-weight:700;font-size:13px;color:#334155">${['JS', 'Python', 'PHP', 'Java', 'C#', 'Go', 'Ruby'][i]}</span></div>`).join('')}
      </div>
      <div class="teacher-slot"></div>`;
    const tr = teacher({ pose: 'wave', width: 238, style: 'left:1576px;top:470px;' });
    cam.querySelector('.teacher-slot').replaceWith(tr.el);
    const email = cam.querySelector('[data-email]');
    const pass = cam.querySelector('[data-pass]');
    const cursor = cam.querySelector('[data-cursor]');
    const ring = cam.querySelector('[data-ring]');
    const fieldPass = pass.closest('.field');
    const login = cam.querySelector('[data-login]');
    const packet = cam.querySelector('[data-packet]');
    const badges = [...cam.querySelectorAll('[data-badge]')];
    const sub = cam.querySelector('[data-sub]');
    const lead = cam.querySelector('[data-lead]');
    const beam1 = cam.querySelector('[data-beam1]');
    const beam2 = cam.querySelector('[data-beam2]');
    const emailText = 'an@example.com';
    return {
      update(U) {
        const te = clamp((U.t - 0.6) / 1.7);
        email.textContent = emailText.slice(0, Math.round(emailText.length * te));
        email.classList.toggle('typed', te > 0 && te < 1);
        const tp = clamp((U.t - 2.5) / 1.3);
        pass.textContent = '•'.repeat(Math.round(9 * tp));
        fieldPass.classList.toggle('focus', U.t > 2.4 && U.t < 4.3);
        const clickT = U.t - 4.4;
        cursor.style.left = (190 + Math.sin(clamp(U.t / 4.4) * 1.2) * 18) + 'px';
        cursor.style.top = (238 + clamp(U.t / 4.4) * 40) + 'px';
        cursor.style.opacity = U.t < 5.2 ? 1 : 0;
        ring.style.opacity = clickT > 0 && clickT < 0.9 ? (1 - clickT / 0.9) * 0.9 : 0;
        ring.style.transform = `scale(${0.4 + clamp(clickT / 0.9) * 1.6})`;
        login.style.transform = clickT > 0 && clickT < 0.25 ? 'scale(.97)' : 'scale(1)';
        const trv = clamp((U.t - 5.4) / 5.0);
        const bx = lerp(786, 1046, smooth(clamp(trv * 1.6)));
        const by = lerp(600, 410, smooth(clamp(trv * 1.6))) - Math.sin(clamp(trv * 1.6) * Math.PI) * 80;
        const late = clamp((trv - 0.62) / 0.38);
        const px = trv < 0.62 ? bx : lerp(1046, 1375, smooth(late));
        const py = trv < 0.62 ? by : lerp(410, 505, smooth(late));
        packet.style.left = px + 'px';
        packet.style.top = py + 'px';
        packet.style.opacity = U.t > 5.4 && U.t < 10.6 ? 1 : 0;
        const dash = -U.t * 60;
        beam1.setAttribute('stroke-dashoffset', dash);
        beam2.setAttribute('stroke-dashoffset', dash);
        fade(sub, U.p(1, 0.05, 0.7), 14);
        fade(lead, U.p(1, 0.35, 0.7), 12);
        badges.forEach((b, i) => fade(b, U.p(2, 0.15 + i * 0.13, 0.55), 18, 0, 0.94));
        tr.update(U.t, U.t > 16 ? 'point' : 'wave');
        return `scale(${1 + U.p(0, 0, 20) * 0.012}) translateX(${U.p(0, 0, 20) * -6}px)`;
      }
    };
  };

  /* ---------- 02 GOALS ---------- */
  B.goals = (cam) => {
    const items = [
      { n: '01', t: 'Backend là gì?', d: 'Xử lý nghiệp vụ, xác thực, dữ liệu phía máy chủ.', c: '#2563EB' },
      { n: '02', t: 'Ngôn ngữ vs Framework', d: 'Phân biệt ngôn ngữ, runtime, framework, thư viện.', c: '#8B5CF6' },
      { n: '03', t: 'Bảy hệ sinh thái', d: 'JS/TS, Python, PHP, Java, C#, Go, Ruby.', c: '#06B6D4' },
      { n: '04', t: 'So sánh & chọn', d: 'Chọn theo bài toán, đội ngũ và khả năng bảo trì.', c: '#F59E0B' }
    ];
    cam.innerHTML = `
      <div class="scene-head"><div class="eyebrow">LỘ TRÌNH BÀI GIẢNG</div><h1 class="scene-title">Bốn chặng trên <span class="accent">lộ trình</span></h1><p class="scene-sub">Đi từ khái niệm gốc đến quyết định chọn công nghệ cho dự án thật.</p></div>
      <svg style="position:absolute;inset:0;width:1920px;height:1080px;z-index:1" viewBox="0 0 1920 1080"><path d="M130 470 C 380 360, 560 590, 760 470 S 1180 350, 1360 470 S 1600 560, 1760 470" fill="none" stroke="#BFDBFE" stroke-width="4" stroke-dasharray="12 12"/></svg>
      ${items.map((x, i) => `<div class="card" data-card="${i}" style="left:${110 + i * 430}px;top:${330 + (i % 2) * 56}px;width:380px;height:250px;padding:26px 26px;z-index:2">
        <div style="display:flex;align-items:center;justify-content:space-between"><div class="num" style="font-size:42px;color:${x.c}">${x.n}</div><div style="width:54px;height:54px;border-radius:16px;background:${x.c}16;color:${x.c};display:flex;align-items:center;justify-content:center">${icon(['server', 'layers', 'globe', 'chart'][i], 28)}</div></div>
        <h3 style="font-family:Quicksand;font-size:23px;color:#0F172A;margin-top:10px">${x.t}</h3>
        <p style="font-size:14px;line-height:1.5;color:#64748B;margin-top:8px">${x.d}</p>
      </div>`).join('')}
      <div class="card" data-quiz style="left:1290px;top:736px;padding:14px 20px;display:flex;align-items:center;gap:12px;border-radius:16px">
        <span style="width:40px;height:40px;border-radius:12px;background:#FFF6E5;color:#F59E0B;display:flex;align-items:center;justify-content:center">${icon('bolt', 24)}</span>
        <div><div style="font-family:Quicksand;font-weight:700;font-size:17px;color:#0F172A">3 câu hỏi nhanh</div><div style="font-size:11px;color:#64748B">ở cuối bài — sẵn sàng chưa?</div></div>
      </div>
      <div class="teacher-slot"></div>`;
    const tr = teacher({ pose: 'point', width: 168, style: 'left:92px;top:690px;' });
    cam.querySelector('.teacher-slot').replaceWith(tr.el);
    const cards = [...cam.querySelectorAll('[data-card]')];
    const quiz = cam.querySelector('[data-quiz]');
    return {
      update(U) {
        cards.forEach((c, i) => fade(c, U.p(0, 0.15 + i * 0.28, 0.6), 30, 0, 0.95));
        fade(quiz, U.p(1, 0.05, 0.55), 20, 0, 0.94);
        tr.update(U.t, 'point');
        return `scale(${1 + U.p(0, 0, 16) * 0.008})`;
      }
    };
  };

  /* ---------- DIVIDERS ---------- */
  const divider = (cam, o) => {
    cam.innerHTML = `<div class="divider ${o.tone}"><div class="grid-lines"></div><div class="dnum">${o.num}</div>
      <div class="dcopy"><div class="deyebrow">${o.eyebrow}</div><h1>${o.title}</h1><p>${o.sub}</p>
      <div class="dchips">${o.chips.map((c, i) => `<span class="dchip" data-chip="${i}">${c}</span>`).join('')}</div></div></div>`;
    const chips = [...cam.querySelectorAll('[data-chip]')];
    const h1 = cam.querySelector('h1');
    const p = cam.querySelector('p');
    return {
      update(U) {
        fade(h1, U.p(0, 0.05, 0.55), 26);
        fade(p, U.p(0, 0.2, 0.55), 16);
        chips.forEach((c, i) => fade(c, U.p(0, 0.28 + i * 0.08, 0.45), 14));
        return `scale(${1 + U.p(0, 0, 3) * 0.03})`;
      }
    };
  };
  B.div1 = (cam) => divider(cam, { tone: 'blue', num: '01', eyebrow: 'PHẦN MỘT', title: 'Backend là gì?', sub: 'Phần não nằm sau mọi giao diện: nhận yêu cầu, quyết định, kiểm tra và ghi nhớ.', chips: ['Yêu cầu', 'Nghiệp vụ', 'Xác thực', 'Truy vấn', 'Phản hồi'] });
  B.div2 = (cam) => divider(cam, { tone: 'purple', num: '02', eyebrow: 'PHẦN HAI', title: 'Ngôn ngữ vs Framework', sub: 'Hai khái niệm bị nhầm nhiều nhất — và runtime, thư viện cũng nằm ngay cạnh.', chips: ['Ngôn ngữ', 'Runtime', 'Framework', 'Thư viện'] });
  B.div3 = (cam) => divider(cam, { tone: 'teal', num: '03', eyebrow: 'PHẦN BA', title: 'Bảy hệ sinh thái Backend', sub: 'Mỗi ngôn ngữ một thế mạnh, mỗi framework một cách giải quyết bài toán.', chips: ['JavaScript', 'Python', 'PHP', 'Java', 'C#', 'Go', 'Ruby'] });
  B.divider = (cam, def) => (B[def.id] || B.div1)(cam);

  /* ---------- 04 BACKEND ---------- */
  B.backend = (cam) => {
    const nodes = [
      { x: 96, t: 'Người dùng', s: 'Yêu cầu thao tác', ic: 'user' },
      { x: 430, t: 'Frontend', s: 'Giao diện web / app', ic: 'browser' },
      { x: 764, t: 'API', s: 'Cửa ngõ giao tiếp', ic: 'gate' },
      { x: 1098, t: 'Backend', s: 'Xử lý nghiệp vụ', ic: 'server' },
      { x: 1432, t: 'Database', s: 'Lưu trữ dữ liệu', ic: 'db' }
    ];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1200px"><div class="eyebrow">PHẦN 01 · BACKEND</div><h1 class="scene-title">Backend <span class="accent">làm việc gì?</span></h1><p class="scene-sub">Mọi cú click đều biến thành request — và backend là nơi quyết định điều gì xảy ra tiếp theo.</p></div>
      <div class="card" style="left:1370px;top:106px;width:454px;height:286px;padding:12px" data-shop>${shopMini(true)}</div>
      <div class="hotspot" data-hs="0" style="left:1458px;top:196px"></div>
      <div class="hotspot" data-hs="1" style="left:1610px;top:192px"></div>
      <div class="hotspot" data-hs="2" style="left:1760px;top:192px"></div>
      <div class="hotspot" data-hs="3" style="left:1520px;top:316px"></div>
      <div class="hotspot" data-hs="4" style="left:1690px;top:300px"></div>
      ${nodes.map((n, i) => `<div class="node" data-node="${i}" style="left:${n.x}px;top:400px"><div class="ni">${icon(n.ic, 28)}</div><b>${n.t}</b><span>${n.s}</span></div>`).join('')}
      ${[0, 1, 2, 3].map((i) => `<div class="conn" style="left:${nodes[i].x + 196}px;top:474px;width:${nodes[i + 1].x - nodes[i].x - 196}px"></div>`).join('')}
      <div data-labels>${[2, 3, 4].map((i) => `<span class="chip ${i === 3 ? 'purple-chip' : i === 4 ? 'green-chip' : ''}" data-label="${i}" style="position:absolute;left:${nodes[i].x + 4}px;top:562px;width:188px;justify-content:center;font-size:12.5px;padding:6px 8px">${i === 2 ? 'cửa ngõ' : i === 3 ? 'bộ não' : 'trí nhớ dài hạn'}</span>`).join('')}</div>
      <div style="position:absolute;left:96px;top:600px;width:1728px;display:flex;justify-content:center;gap:14px" data-chips>${[['shield', 'Xác thực người dùng'], ['gear', 'Xử lý nghiệp vụ'], ['db', 'Truy vấn dữ liệu']].map(([ic, t]) => `<span class="chip">${icon(ic, 18)} ${t}</span>`).join('')}</div>
      <div class="card" data-split style="left:300px;top:680px;width:610px;height:132px;padding:20px 22px;display:flex;gap:16px;align-items:center;opacity:0"><span style="width:52px;height:52px;border-radius:15px;background:#EAF3FF;color:#2563EB;display:flex;align-items:center;justify-content:center;flex:none">${icon('browser', 28)}</span><div><b style="font-family:Quicksand;font-size:19px;color:#0F172A">Frontend — bạn thấy</b><p style="font-size:13px;color:#64748B;margin-top:3px">Bố cục, màu sắc, nút bấm, hiệu ứng.</p></div></div>
      <div class="card" data-split style="left:940px;top:680px;width:680px;height:132px;padding:20px 22px;display:flex;gap:16px;align-items:center;opacity:0"><span style="width:52px;height:52px;border-radius:15px;background:#F3EFFF;color:#8B5CF6;display:flex;align-items:center;justify-content:center;flex:none">${icon('server', 28)}</span><div><b style="font-family:Quicksand;font-size:19px;color:#0F172A">Backend — phải quyết định</b><p style="font-size:13px;color:#64748B;margin-top:3px">Kiểm tra, tính toán, ghi nhớ và bảo vệ dữ liệu.</p></div></div>
      <div class="stamp" data-stamp style="left:1108px;top:326px">SẬP!</div>
      <div class="packet blue" data-packet style="left:190px;top:468px;opacity:0"><span class="trail"></span><span class="core"></span></div>`;
    const nodeEls = [...cam.querySelectorAll('[data-node]')];
    const hotspots = [...cam.querySelectorAll('[data-hs]')];
    const labels = [...cam.querySelectorAll('[data-label]')];
    const chips = cam.querySelector('[data-chips]');
    const splits = [...cam.querySelectorAll('[data-split]')];
    const packet = cam.querySelector('[data-packet]');
    const stamp = cam.querySelector('[data-stamp]');
    return {
      update(U) {
        fade(cam.querySelector('[data-shop]'), U.p(0, 0.1, 0.5), 16);
        hotspots.forEach((d, i) => {
          const on = U.on(0) && Math.sin((U.t - i * 0.9) * 2.2) > 0.2;
          d.style.transform = `scale(${on ? 1.1 : 0.8})`;
          d.style.opacity = U.t > 1 + i * 0.9 ? (on ? 1 : 0.45) : 0;
        });
        nodeEls.forEach((n, i) => {
          fade(n, U.p(i < 3 ? 0 : 1, 0.05 + i * 0.12, 0.5), 22, 0, 0.95);
          n.classList.toggle('hot', U.on(1) && Math.floor(U.cueT(1) * 1.4) % 5 === i);
        });
        labels.forEach((l, i) => fade(l, U.p(2, 0.1 + i * 0.25, 0.5), 10));
        fade(chips, U.p(1, 0.05, 0.5), 10);
        splits.forEach((s, i) => fade(s, U.p(3, 0.15 + i * 0.3, 0.6), 18, 0, 0.96));
        const t1 = U.cueT(1);
        if (t1 > 0 && t1 < 9.5) {
          const q = smooth(clamp(t1 / 4.5));
          const bx = t1 < 5 ? lerp(190, 1526, q) : lerp(1526, 190, smooth(clamp((t1 - 5) / 4.5)));
          const by = 468 - Math.sin((t1 % 4.5) / 4.5 * Math.PI) * 100;
          packet.style.left = bx + 'px';
          packet.style.top = by + 'px';
          packet.style.opacity = 1;
        } else packet.style.opacity = 0;
        const fail = U.cueT(4);
        const bad = fail > 0 && fail < 3.4;
        nodeEls[3].classList.toggle('bad', bad);
        nodeEls[3].classList.toggle('good', fail > 3.8);
        stamp.style.opacity = bad ? 1 : 0;
        stamp.style.transform = `rotate(-6deg) scale(${bad ? 1 : 1.3})`;
        nodeEls[3].style.transform = bad ? `translate(${Math.sin(fail * 60) * 4}px,0)` : '';
        return `scale(${1.01 + U.p(0, 0, 40) * 0.012})`;
      }
    };
  };

  /* ---------- 05 FLOW ---------- */
  B.flow = (cam) => {
    const st = [
      { x: 180, t: 'Nhập liệu', s: 'email + mật khẩu', ic: 'user' },
      { x: 460, t: 'HTTP POST', s: '/login', ic: 'arrow' },
      { x: 740, t: 'API', s: 'nhận request', ic: 'gate' },
      { x: 1020, t: 'Xác thực', s: 'so sánh hash', ic: 'shield' },
      { x: 1300, t: 'Database', s: 'tìm tài khoản', ic: 'db' },
      { x: 1580, t: 'Response', s: '200 + token', ic: 'check' }
    ];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1320px"><div class="eyebrow">PHẦN 01 · LUỒNG REQUEST</div><h1 class="scene-title">Một yêu cầu <span class="accent">đi qua hệ thống</span></h1><p class="scene-sub">Không có phép màu: chỉ là một chuỗi bước kiểm tra diễn ra trong vài trăm mili giây.</p></div>
      <svg style="position:absolute;inset:0;width:1920px;height:1080px;z-index:1" viewBox="0 0 1920 1080"><path d="M180 380H1580" stroke="#DBEAFE" stroke-width="4" stroke-dasharray="10 10"/></svg>
      ${st.map((s, i) => `<div style="position:absolute;left:${s.x - 68}px;top:312px;width:136px;text-align:center" data-st="${i}">
        <div class="node" style="position:relative;left:0;top:0;width:104px;height:104px;margin:0 auto;border-radius:50%;gap:0" data-circle>${icon(s.ic, 30)}</div>
        <b style="display:block;font-family:Quicksand;font-size:16px;color:#0F172A;margin-top:9px">${s.t}</b><span style="font-size:11px;color:#64748B">${s.s}</span>
      </div>`).join('')}
      <div class="packet blue" data-packet style="left:72px;top:356px;opacity:0"><span class="trail"></span><span class="core"></span></div>
      <div class="code-panel" data-req style="left:96px;top:540px;width:800px;height:226px">
        <div class="code-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="code-name">request.http</span><span class="code-badge">CLIENT → SERVER</span></div>
        <div class="code-body" style="font-size:15px">
          <div class="code-line"><span class="ln">1</span><span><span class="tok-kw">POST</span> /login <span class="tok-op">HTTP/1.1</span></span></div>
          <div class="code-line"><span class="ln">2</span><span>Content-Type: application/json</span></div>
          <div class="code-line"><span class="ln">3</span><span>{</span></div>
          <div class="code-line"><span class="ln">4</span><span>  "email": "an@example.com",</span></div>
          <div class="code-line"><span class="ln">5</span><span>  "password": "••••••••"</span></div>
          <div class="code-line"><span class="ln">6</span><span>}</span></div>
        </div>
      </div>
      <div class="card" data-res style="left:1024px;top:540px;width:800px;height:226px;padding:18px 22px">
        <div style="display:flex;align-items:center;gap:10px"><span class="chip green-chip">${icon('check', 16)} 200 OK</span><span class="mini-note">~180 ms · mật khẩu không lưu dạng thô</span></div>
        <div style="margin-top:12px;display:grid;grid-template-columns:1fr auto;gap:10px">
          <div style="font-family:JetBrains;font-size:14px;line-height:1.7;color:#334155">access_token: eyJhbGciOi...<br><span style="color:#94A3B8">expires_in: 900 giây</span></div>
          <div style="width:58px;height:58px;border-radius:50%;background:#ECFDF5;border:2px solid #6EE7B7;color:#10B981;display:flex;align-items:center;justify-content:center">${icon('shield', 28)}</div>
        </div>
      </div>
      <div class="card" data-timer style="left:1556px;top:216px;padding:10px 16px;display:flex;align-items:center;gap:8px"><span style="color:#2563EB">${icon('clock', 20)}</span><b style="font-family:Jakarta;font-size:18px;color:#0F172A" data-clock>0.00s</b></div>`;
    const circles = [...cam.querySelectorAll('[data-circle]')];
    const packet = cam.querySelector('[data-packet]');
    const req = cam.querySelector('[data-req]');
    const res = cam.querySelector('[data-res]');
    const clock = cam.querySelector('[data-clock]');
    const timer = cam.querySelector('[data-timer]');
    const pos = st.map((s) => s.x);
    return {
      update(U) {
        const t = U.t - U.cueStart(0);
        const total = U.cueStart(2) - U.cueStart(0);
        const p = smooth(clamp(t / total));
        const idx = Math.min(5, Math.floor(p * 6));
        circles.forEach((c, i) => {
          c.classList.toggle('hot', i === idx && t > 0 && t < total);
          c.style.borderColor = i <= idx ? '#60A5FA' : '';
        });
        const seg = p * 5;
        const a = Math.min(4, Math.floor(seg));
        const f = seg - a;
        packet.style.left = lerp(pos[a], pos[a + 1], f) - 9 + 'px';
        packet.style.top = '356px';
        packet.style.opacity = U.on(0) && U.t < U.cueStart(2) + 1 ? 1 : 0;
        fade(req, U.p(0, 0.1, 0.6), 16);
        fade(res, U.p(2, 0.05, 0.6), 16);
        fade(timer, U.p(0, 0.2, 0.5), 10);
        const ms = U.on(2) ? 0.18 : Math.min(0.18, t / total * 0.18);
        clock.textContent = ms.toFixed(2) + 's';
        timer.style.borderColor = U.on(2) ? '#6EE7B7' : '';
        return `scale(${1 + U.p(0, 0, 26) * 0.008})`;
      }
    };
  };

  /* ---------- 07 LANGFW ---------- */
  B.langfw = (cam) => {
    const bins = [
      { t: 'NGÔN NGỮ', c: '#2563EB', bg: '#EAF3FF' },
      { t: 'RUNTIME', c: '#06B6D4', bg: '#E8FAFD' },
      { t: 'FRAMEWORK', c: '#8B5CF6', bg: '#F3EFFF' },
      { t: 'THƯ VIỆN', c: '#F59E0B', bg: '#FFF6E5' }
    ];
    const cards = [
      { n: 'JavaScript', k: 'javascript', bin: 0, c: '#EAB308' },
      { n: 'Node.js', k: 'node', bin: 1, c: '#5FA04E' },
      { n: 'Express', k: 'express', bin: 2, c: '#475569' },
      { n: 'bcrypt', k: 'lock', bin: 3, c: '#F59E0B' }
    ];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 02 · PHÂN BIỆT</div><h1 class="scene-title">Ba lớp <span class="accent">dễ nhầm</span></h1><p class="scene-sub">Ngôn ngữ là dụng cụ. Framework là giàn giáo. Runtime là môi trường chạy. Thư viện là mảnh ghép.</p></div>
      <div class="card" data-tool style="left:96px;top:250px;width:520px;height:468px;padding:24px 26px">
        <div class="card-kicker">NGÔN NGỮ = DỤNG CỤ</div>
        <div style="display:flex;flex-wrap:wrap;gap:9px;margin-top:18px">${['JavaScript', 'Python', 'PHP', 'Java', 'C#', 'Go', 'Ruby'].map((x) => `<span class="chip">${x}</span>`).join('')}</div>
        <p style="font-size:14px;line-height:1.55;color:#64748B;margin-top:18px">Công cụ viết mã và xây logic. Bạn dùng nó để tạo ra sản phẩm — nhưng tự tổ chức mọi thứ.</p>
        <div style="margin-top:22px;padding:16px;border-radius:14px;background:#F8FBFF;border:1px dashed #CFE1F4;font-size:13px;color:#475569;line-height:1.55">Giống như <b>vật liệu và dụng cụ</b> trên công trường: gạch, gỗ, máy khoan.</div>
      </div>
      <div class="card" data-scaffold style="left:1300px;top:250px;width:524px;height:468px;padding:24px 26px">
        <div class="card-kicker" style="color:#8B5CF6">FRAMEWORK = GIÀN GIÁO</div>
        <svg viewBox="0 0 440 260" style="width:100%;height:260px;margin-top:10px" data-scafsvg>
          <rect x="30" y="200" width="380" height="16" rx="4" fill="#DDD6FE"/>
          <g stroke="#8B5CF6" stroke-width="7" stroke-linecap="round" fill="none" data-beams>
            <path d="M70 200V60M370 200V60M70 60h300"/>
            <path d="M70 120h300M170 60v140M270 60v140"/>
            <path d="M70 60l300 140M370 60L70 200" stroke="#C4B5FD" stroke-width="4"/>
          </g>
          <rect x="160" y="96" width="120" height="64" rx="8" fill="#FFFFFF" stroke="#8B5CF6" stroke-width="3"/>
          <text x="220" y="134" text-anchor="middle" font-family="Quicksand" font-weight="700" font-size="20" fill="#5B21B6">Ứng dụng</text>
        </svg>
        <p style="font-size:14px;line-height:1.55;color:#64748B">Cung cấp cấu trúc, quy ước, thư viện — giúp dựng nhanh hơn và có tổ chức hơn.</p>
      </div>
      ${bins.map((b, i) => `<div style="position:absolute;left:${650 + i * 155}px;top:300px;width:140px;height:300px;border:2px dashed ${b.c}55;border-radius:16px;background:${b.bg}" data-bin="${i}">
        <div style="position:absolute;left:0;right:0;top:12px;text-align:center;font-family:Jakarta;font-size:10.5px;font-weight:700;letter-spacing:.1em;color:${b.c}">${b.t}</div>
        <div style="position:absolute;left:8px;right:8px;bottom:10px;top:44px;border-radius:10px;background:rgba(255,255,255,.55);border:1px solid ${b.c}22"></div>
      </div>`).join('')}
      ${cards.map((c, i) => `<div class="card" data-fly="${i}" style="left:${680 + i * 148}px;top:660px;width:132px;height:56px;padding:0 10px;display:flex;align-items:center;gap:8px;border-radius:13px;z-index:6">
        ${c.k === 'lock' ? `<span style="width:28px;height:28px;border-radius:8px;background:#FFF6E5;color:#F59E0B;display:flex;align-items:center;justify-content:center">${icon('lock', 17)}</span>` : logo(c.k, 24)}
        <b style="font-family:Quicksand;font-size:14px;color:#0F172A">${c.n}</b>
      </div>`).join('')}
      <div style="position:absolute;left:96px;top:752px;width:1728px;display:flex;justify-content:center;gap:12px" data-rules>
        ${[['Express', 'JavaScript'], ['Laravel', 'PHP'], ['Spring Boot', 'Java']].map(([a, b], i) => `<span class="chip purple-chip" data-rule="${i}" style="font-family:JetBrains;font-size:13.5px">${a} ∈ ${b}</span>`).join('')}
      </div>`;
    const tool = cam.querySelector('[data-tool]');
    const scaf = cam.querySelector('[data-scaffold]');
    const beams = [...cam.querySelectorAll('[data-beams] path')];
    const binsEl = [...cam.querySelectorAll('[data-bin]')];
    const cardsEl = [...cam.querySelectorAll('[data-fly]')];
    const rules = [...cam.querySelectorAll('[data-rule]')];
    const flyTo = cards.map((c) => ({ x: 650 + c.bin * 155 + 5, y: 520 }));
    return {
      update(U) {
        fade(tool, U.p(0, 0.1, 0.6), 20);
        fade(scaf, U.p(1, 0.05, 0.6), 20);
        beams.forEach((b, i) => { b.style.opacity = 0.2 + 0.8 * U.p(1, i * 0.12, 0.45); });
        binsEl.forEach((b, i) => fade(b, U.p(2, 0.05 + i * 0.1, 0.5), 18, 0, 0.95));
        rules.forEach((r, i) => fade(r, U.p(2, 0.3 + i * 0.18, 0.5), 12));
        cardsEl.forEach((c, i) => {
          const p = U.p(3, 0.15 + i * 0.5, 0.8);
          const sx = 680 + i * 148;
          const sy = 660;
          c.style.left = lerp(sx, flyTo[i].x, p) + 'px';
          c.style.top = lerp(sy, flyTo[i].y, p) + 'px';
          c.style.opacity = U.t > 0.2 ? 1 : 0;
          c.style.transform = `scale(${1 + (1 - p) * 0.04})`;
        });
        return `scale(${1 + U.p(0, 0, 40) * 0.006})`;
      }
    };
  };

  /* ---------- ECOSYSTEM SCENES ---------- */
  B.js = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 01</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('javascript', 58)} JavaScript <span style="color:#94A3B8;font-size:30px">&amp;</span> ${logoWrap('typescript', 58)} TypeScript</h1><p class="scene-sub">Một ngôn ngữ dùng được cả hai phía — trình duyệt và server.</p></div>
      <div class="card" style="left:96px;top:262px;width:470px;height:238px;padding:22px 24px" data-lang>
        <div class="card-kicker">NGÔN NGỮ</div>
        <div style="display:flex;gap:10px;margin-top:14px"><span class="chip">JavaScript</span><span class="chip">TypeScript</span></div>
        <p style="font-size:13.5px;line-height:1.55;color:#64748B;margin-top:14px">TypeScript là superset của JavaScript: thêm kiểu tĩnh, biên dịch về JS. Không phải framework.</p>
        <div style="margin-top:14px;font-size:13px;color:#475569">Chạy trên trình duyệt <b>và</b> trên server nhờ Node.js.</div>
      </div>
      <div class="card" style="left:96px;top:524px;width:470px;height:188px;padding:22px 24px" data-strength>
        <div class="card-kicker">ĐIỂM MẠNH</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px"><span class="chip green-chip">Chung ngôn ngữ frontend</span><span class="chip green-chip">Cộng đồng cực lớn</span><span class="chip green-chip">Thư viện đủ mọi thứ</span></div>
        <p style="font-size:12.5px;color:#64748B;margin-top:12px">Hợp: thương mại điện tử, quản lý, API mobile, ứng dụng thời gian thực.</p>
      </div>
      <div style="position:absolute;left:640px;top:286px;width:300px;height:300px;border-radius:50%;border:3px dashed #5FA04E66;background:radial-gradient(circle at 50% 40%,#F0FDF4,#E8F7EE)" data-ring>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px">${logoWrap('node', 92)}<b style="font-family:Quicksand;font-size:26px;color:#14532D">Node.js</b><span class="chip green-chip" style="font-size:11px;padding:4px 10px">RUNTIME</span></div>
        <div style="position:absolute;left:12px;top:14px;font-size:11px;color:#166534;font-family:Jakarta">V8 + libuv</div>
      </div>
      <div class="card" style="left:640px;top:250px;width:76px;height:56px;padding:0;display:flex;align-items:center;justify-content:center" data-browsericon>${icon('browser', 30)}</div>
      <div style="position:absolute;left:716px;top:278px;width:54px;height:3px;background:linear-gradient(90deg,#93C5FD,#5FA04E);z-index:2" data-arrow></div>
      ${[
        { n: 'Express', k: 'express', d: 'Tối giản, linh hoạt, phổ biến để dựng REST API.', tag: 'Phổ biến nhất' },
        { n: 'NestJS', k: 'nestjs', d: 'Cấu trúc rõ ràng, TypeScript mạnh, DI, module hóa.', tag: 'Kiến trúc chặt' },
        { n: 'Fastify', k: 'fastify', d: 'Tối ưu hiệu năng và độ trễ ở mức thiết kế.', tag: 'Tối ưu throughput' }
      ].map((x, i) => `<div class="eco-card" data-fw="${i}" style="left:1040px;top:${250 + i * 140}px;width:784px;height:132px">
        <div class="ec-top">${logoWrap(x.k, 48)}<div><b>${x.n}</b><div class="ec-sub">${x.tag}</div></div></div>
        <p style="margin-top:6px">${x.d}</p>
      </div>`).join('')}
      <div data-code></div>
      <div style="position:absolute;left:1130px;top:700px;width:694px;display:flex;flex-wrap:wrap;gap:8px" data-use>
        <span class="chip amber-chip">Thương mại điện tử</span><span class="chip amber-chip">Hệ thống quản lý</span><span class="chip amber-chip">API mobile</span><span class="chip amber-chip">Realtime</span>
      </div>
      <div class="stamp blue-stamp" data-stamp style="left:640px;top:812px">NODE.JS ≠ FRAMEWORK</div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "const express = require('express');",
      "const app = express();",
      "",
      "app.get('/api/products', async (req, res) => {",
      "  res.json({ items: await db.products.all() });",
      "});",
      "app.listen(3000);"
    ], { x: 590, y: 588, w: 440, compact: true, name: 'server.js', badge: 'NODE.JS' }));
    const ring = cam.querySelector('[data-ring]');
    const fws = [...cam.querySelectorAll('[data-fw]')];
    const browserIcon = cam.querySelector('[data-browsericon]');
    const use = cam.querySelector('[data-use]');
    const stamp = cam.querySelector('[data-stamp]');
    const strength = cam.querySelector('[data-strength]');
    return {
      update(U) {
        fade(browserIcon, U.p(0, 0.2, 0.5), 10, -14);
        fade(ring, U.p(0, 0.45, 0.6), 18, 0, 0.94);
        fws.forEach((f, i) => fade(f, U.p(1, 0.1 + i * 0.28, 0.5), 20, 0, 0.97));
        fade(strength, U.p(2, 0.05, 0.55), 16);
        fade(use, U.p(2, 0.15, 0.55), 12);
        stamp.style.opacity = U.p(3, 0.1, 0.45);
        stamp.style.transform = `rotate(-6deg) scale(${0.9 + U.p(3, 0.1, 0.45) * 0.1})`;
        ring.style.transform = `rotate(${Math.sin(U.t * 0.5) * 2}deg)`;
        return `scale(${1 + U.p(0, 0, 30) * 0.008})`;
      }
    };
  };

  B.python = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 02</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('python', 58)} Python</h1><p class="scene-sub">Dễ đọc, dễ học — và là ngôn ngữ mạnh nhất cho AI, dữ liệu ở phía backend.</p></div>
      <div class="card" data-left style="left:96px;top:240px;width:470px;height:490px;padding:24px 26px">
        <div class="card-kicker">VÌ SAO PHỔ BIẾN</div>
        <div style="margin-top:16px;display:flex;flex-direction:column;gap:12px">
          ${[['book', 'Cú pháp dễ đọc, dễ bảo trì'], ['bolt', 'Hệ sinh thái AI, khoa học dữ liệu'], ['layers', 'Thư viện phong phú cho backend'], ['globe', 'Cộng đồng lớn, tài liệu dày']].map(([ic, t]) => `<div style="display:flex;align-items:center;gap:12px;font-size:14px;color:#334155"><span style="width:38px;height:38px;border-radius:11px;background:#EAF3FF;color:#2563EB;display:flex;align-items:center;justify-content:center">${icon(ic, 21)}</span>${t}</div>`).join('')}
        </div>
        <p style="font-size:13.5px;line-height:1.55;color:#64748B;margin-top:18px">Hợp: hệ thống quản lý, REST API, dịch vụ xử lý dữ liệu, ứng dụng AI cần backend tích hợp.</p>
        <div style="margin-top:16px;display:flex;flex-wrap:wrap;gap:8px"><span class="chip amber-chip">AI backend</span><span class="chip amber-chip">Data service</span><span class="chip amber-chip">REST API</span></div>
        <div style="position:absolute;left:26px;right:26px;bottom:20px;padding:11px 14px;border-radius:12px;background:#F8FAFC;border:1px solid #E2E8F0;font-size:12px;line-height:1.5;color:#475569"><b>Python là ngôn ngữ.</b> Django, Flask, FastAPI là framework chạy trên Python.</div>
      </div>
      ${[
        { n: 'Django', k: 'django', d: 'Đầy đủ: ORM, trang quản trị, xác thực, bảo mật.', tag: 'Full-stack · batteries included' },
        { n: 'Flask', k: 'flask', d: 'Nhẹ, linh hoạt, bạn tự lắp từng mảnh.', tag: 'Micro-framework' },
        { n: 'FastAPI', k: 'fastapi', d: 'Type hints, tự sinh tài liệu API, hỗ trợ async.', tag: 'API hiện đại' }
      ].map((x, i) => `<div class="eco-card" data-fw="${i}" style="left:600px;top:${240 + i * 140}px;width:556px;height:130px">
        <div class="ec-top">${logoWrap(x.k, 48)}<div><b>${x.n}</b><div class="ec-sub">${x.tag}</div></div></div>
        <p>${x.d}</p>
      </div>`).join('')}
      <div data-code></div>
      <div class="card" data-swagger style="left:1200px;top:500px;width:624px;height:250px;padding:0;overflow:hidden">
        <div style="height:44px;background:#0F172A;color:#fff;display:flex;align-items:center;padding:0 16px;gap:9px"><span style="width:9px;height:9px;border-radius:50%;background:#22C55E"></span><b style="font-family:Jakarta;font-size:12px;letter-spacing:.06em">/docs · Swagger UI</b><span style="margin-left:auto;font-size:10px;color:#7DD3FC">tự sinh từ type hints</span></div>
        <div style="padding:14px 18px">
          <div style="display:flex;align-items:center;gap:8px"><span class="chip green-chip" style="font-family:JetBrains;font-size:11px;padding:4px 8px">GET</span><span style="font-family:JetBrains;font-size:13px;color:#0F172A">/items/{item_id}</span><span style="margin-left:auto;font-size:10px;color:#64748B">Try it out</span></div>
          <div style="margin-top:10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px;font-family:JetBrains;font-size:11px;line-height:1.6;color:#475569">{<br>&nbsp;&nbsp;"id": 1,<br>&nbsp;&nbsp;"name": "Aurora X"<br>}</div>
        </div>
      </div>
      <div class="card" data-need style="left:1200px;top:240px;width:624px;height:244px;padding:20px 22px">
        <div class="card-kicker">CHỌN THEO NHU CẦU</div>
        <div style="display:flex;flex-direction:column;gap:10px;margin-top:14px;font-size:13.5px;color:#334155">
          <div><b style="color:#0C4B33">Django</b> — cần nhanh, đầy đủ, ít quyết định.</div>
          <div><b style="color:#334155">Flask</b> — muốn kiểm soát tối đa từng thành phần.</div>
          <div><b style="color:#059669">FastAPI</b> — ưu tiên API hiện đại, async, tài liệu tự động.</div>
        </div>
        <p style="font-size:12px;color:#94A3B8;margin-top:14px">Cả ba đều là framework, chạy trên Python.</p>
      </div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "from fastapi import FastAPI",
      "",
      "app = FastAPI()",
      "",
      "@app.get('/items/{item_id}')",
      "async def read_item(item_id: int):",
      "    return {'id': item_id}"
    ], { x: 600, y: 664, w: 556, compact: true, name: 'main.py', badge: 'FASTAPI' }));
    const left = cam.querySelector('[data-left]');
    const fws = [...cam.querySelectorAll('[data-fw]')];
    const swagger = cam.querySelector('[data-swagger]');
    const need = cam.querySelector('[data-need]');
    return {
      update(U) {
        fade(left, U.p(0, 0.1, 0.55), 18);
        fws.forEach((f, i) => fade(f, U.p(1, 0.1 + i * 0.3, 0.5), 20, 0, 0.97));
        fade(swagger, U.p(1, 0.7, 0.5), 16);
        fade(need, U.p(2, 0.05, 0.55), 14);
        return `scale(${1 + U.p(0, 0, 36) * 0.008})`;
      }
    };
  };

  B.php = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 03</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('php', 58)} PHP</h1><p class="scene-sub">Vẫn là lực lượng đáng gờm ở website doanh nghiệp, hệ thống nội dung và admin.</p></div>
      <div class="card" data-laravel style="left:96px;top:262px;width:640px;height:470px;padding:24px 26px">
        <div style="display:flex;align-items:center;gap:14px">${logoWrap('laravel', 64)}<div><b style="font-family:Quicksand;font-size:28px;color:#0F172A">Laravel</b><div style="font-size:12px;color:#64748B">Full-stack framework phổ biến nhất của PHP</div></div></div>
        <p style="font-size:14px;line-height:1.55;color:#64748B;margin-top:16px">Gần như có sẵn mọi thứ bạn cần cho một ứng dụng web nghiêm túc.</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:16px">
          ${['Eloquent ORM', 'Routing', 'Middleware', 'Xác thực', 'Queue', 'Blade'].map((x) => `<span class="chip red-chip" style="justify-content:center">${x}</span>`).join('')}
        </div>
        <div style="margin-top:16px;padding:12px 14px;border-radius:12px;background:#FEF2F2;border:1px solid #FEE2E2;font-size:12.5px;color:#7F1D1D">Phù hợp: website doanh nghiệp, quản trị, thương mại điện tử, CMS.</div>
        <div style="position:absolute;left:26px;right:26px;bottom:26px">
          <div class="card-kicker" style="font-size:10px">HỆ SINH THÁI</div>
          <div style="display:flex;gap:8px;margin-top:10px">${['Artisan', 'Forge', 'Vapor', 'Nova', 'Livewire'].map((x) => `<span class="chip" style="font-size:11px;padding:6px 9px">${x}</span>`).join('')}</div>
          <p style="font-size:12px;color:#94A3B8;margin-top:10px;line-height:1.5">Artisan CLI, migration và seeder giúp dựng CRUD nhanh.</p>
        </div>
      </div>
      <div class="card" data-symfony style="left:770px;top:262px;width:470px;height:238px;padding:22px 24px">
        <div style="display:flex;align-items:center;gap:12px">${logoWrap('symfony', 46)}<div><b style="font-family:Quicksand;font-size:21px;color:#0F172A">Symfony</b><div style="font-size:11px;color:#64748B">Framework + bộ component tái sử dụng</div></div></div>
        <div style="display:flex;gap:8px;margin-top:16px">${['HttpFoundation', 'Routing', 'Twig'].map((x) => `<span class="chip" style="font-size:11px;padding:6px 9px">${x}</span>`).join('')}</div>
        <p style="font-size:12.5px;line-height:1.5;color:#64748B;margin-top:12px">Rất hợp hệ thống lớn, cần cấu trúc và tái sử dụng.</p>
        <p style="position:absolute;left:24px;right:24px;bottom:18px;font-size:12px;color:#94A3B8">Component dùng bởi Drupal, PrestaShop, API Platform.</p>
      </div>
      <div class="card" data-ci style="left:770px;top:524px;width:470px;height:208px;padding:22px 24px">
        <div style="display:flex;align-items:center;gap:12px">${logoWrap('codeigniter', 46)}<div><b style="font-family:Quicksand;font-size:21px;color:#0F172A">CodeIgniter</b><div style="font-size:11px;color:#64748B">Nhẹ, đơn giản, dễ tiếp cận</div></div></div>
        <p style="font-size:12.5px;line-height:1.5;color:#64748B;margin-top:12px">Ít cấu hình, phù hợp dự án nhỏ và người mới.</p>
        <p style="position:absolute;left:24px;right:24px;bottom:18px;font-size:12px;color:#94A3B8">CodeIgniter 4: hướng đối tượng, chạy tốt trên hosting phổ thông.</p>
      </div>
      <div data-code></div>
      <div style="position:absolute;left:1270px;top:526px;width:554px;display:flex;flex-wrap:wrap;gap:8px" data-use>
        <span class="chip red-chip" style="font-size:11.5px;padding:6px 10px">Website doanh nghiệp</span><span class="chip red-chip" style="font-size:11.5px;padding:6px 10px">Quản trị</span><span class="chip red-chip" style="font-size:11.5px;padding:6px 10px">Thương mại điện tử</span><span class="chip red-chip" style="font-size:11.5px;padding:6px 10px">CMS</span>
      </div>
      <div class="card" data-cost style="left:1270px;top:700px;width:554px;height:86px;padding:14px 18px;display:flex;align-items:center;gap:12px"><span style="color:#10B981">${icon('check', 24)}</span><div style="font-size:12.5px;color:#475569">Chi phí triển khai thấp · hosting phổ biến · nhiều lập trình viên</div></div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "use Illuminate\\Support\\Facades\\Route;",
      "",
      "Route::get('/shop', [ShopController::class, 'index']);",
      "Route::post('/cart', [CartController::class, 'add']);",
      "",
      "// Eloquent: thao tác DB bằng đối tượng",
      "$products = Product::where('active', true)->get();"
    ], { x: 1270, y: 262, w: 554, name: 'routes/web.php', badge: 'LARAVEL' }));
    const laravel = cam.querySelector('[data-laravel]');
    const symfony = cam.querySelector('[data-symfony]');
    const ci = cam.querySelector('[data-ci]');
    const use = cam.querySelector('[data-use]');
    const cost = cam.querySelector('[data-cost]');
    return {
      update(U) {
        fade(laravel, U.p(0, 0.05, 0.55), 18);
        fade(symfony, U.p(1, 0.08, 0.5), 20);
        fade(ci, U.p(1, 0.4, 0.5), 20);
        fade(use, U.p(2, 0.05, 0.5), 12);
        fade(cost, U.p(2, 0.3, 0.5), 12);
        return `scale(${1 + U.p(0, 0, 28) * 0.007})`;
      }
    };
  };

  B.java = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 04</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('java', 58)} Java</h1><p class="scene-sub">Trụ cột hệ thống doanh nghiệp — nơi ổn định quan trọng hơn tốc độ viết code.</p></div>
      <div style="position:absolute;left:96px;top:262px;width:600px" data-stack>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">${logoWrap('springboot', 54)}<div><b style="font-family:Quicksand;font-size:24px;color:#0F172A">Spring Boot</b><div style="font-size:11.5px;color:#64748B">Framework phổ biến nhất của Java</div></div></div>
        <div class="stack" style="position:relative;width:100%">
          ${[['gear', 'Auto-configuration', 'Tự cấu hình theo dependency'], ['server', 'Embedded server', 'Máy chủ nhúng, chạy một lệnh'], ['globe', 'Hệ sinh thái Spring', 'Bảo mật, dữ liệu, messaging, cloud']].map(([ic, t, d]) => `<div class="layer"><span class="li" style="background:#FFF1E8;color:#E76F00">${icon(ic, 22)}</span><div><b>${t}</b><span>${d}</span></div></div>`).join('')}
        </div>
      </div>
      <div class="eco-card" data-quarkus style="left:740px;top:262px;width:420px;height:166px">
        <div class="ec-top">${logoWrap('quarkus', 46)}<div><b>Quarkus</b><div class="ec-sub">Cloud-native · container-first</div></div></div>
        <p>Tối ưu cho container, hỗ trợ biên dịch native.</p>
      </div>
      <div class="eco-card" data-micronaut style="left:1180px;top:262px;width:644px;height:166px">
        <div class="ec-top">${logoWrap('micronaut', 46)}<div><b>Micronaut</b><div class="ec-sub">Microservices hiện đại</div></div></div>
        <p>Thiết kế cho khởi động nhanh và ít bộ nhớ.</p>
      </div>
      <div class="card" data-bars style="left:740px;top:448px;width:1084px;height:184px;padding:20px 24px">
        <div style="display:flex;justify-content:space-between;align-items:center"><div class="card-kicker">ĐỊNH HƯỚNG KHỞI ĐỘNG</div><span class="mini-note">MINH HỌA — KHÔNG PHẢI BENCHMARK</span></div>
        <div class="bar-row" style="margin-top:16px"><div class="bl"><span>Spring Boot</span><span>khởi động đầy đủ</span></div><div class="bar"><i data-bar="0" style="background:linear-gradient(90deg,#E76F00,#F59E0B)"></i></div></div>
        <div class="bar-row"><div class="bl"><span>Quarkus / Micronaut</span><span>tối ưu cho microservices</span></div><div class="bar"><i data-bar="1"></i></div></div>
      </div>
      <div data-code></div>
      <div style="position:absolute;left:1040px;top:670px;width:784px;display:flex;flex-wrap:wrap;gap:8px" data-use>
        <span class="chip amber-chip">Ngân hàng</span><span class="chip amber-chip">Hệ thống giao dịch</span><span class="chip amber-chip">Doanh nghiệp</span><span class="chip amber-chip">Microservices</span>
      </div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "@RestController",
      "@RequestMapping(\"/api/orders\")",
      "public class OrderController {",
      "  @GetMapping(\"/{id}\")",
      "  public Order get(@PathVariable Long id) {",
      "    return service.find(id);",
      "  }",
      "}"
    ], { x: 96, y: 656, w: 900, compact: true, name: 'OrderController.java', badge: 'SPRING BOOT' }));
    const stack = cam.querySelector('[data-stack]');
    const quarkus = cam.querySelector('[data-quarkus]');
    const micronaut = cam.querySelector('[data-micronaut]');
    const bars = cam.querySelector('[data-bars]');
    const barEls = [...cam.querySelectorAll('[data-bar]')];
    const use = cam.querySelector('[data-use]');
    return {
      update(U) {
        fade(stack, U.p(0, 0.05, 0.55), 18);
        fade(quarkus, U.p(1, 0.05, 0.5), 18);
        fade(micronaut, U.p(1, 0.3, 0.5), 18);
        fade(bars, U.p(1, 0.5, 0.5), 14);
        barEls.forEach((b, i) => { b.style.width = (U.p(1, 0.7 + i * 0.25, 0.7) * (i ? 42 : 100)) + '%'; });
        fade(use, U.p(2, 0.05, 0.55), 12);
        return `scale(${1 + U.p(0, 0, 26) * 0.007})`;
      }
    };
  };

  B.csharp = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 05</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('csharp', 58)} C# <span style="color:#94A3B8;font-size:30px">&amp;</span> ${logoWrap('dotnet', 58)} .NET</h1><p class="scene-sub">Mạnh trong thế giới Microsoft — và .NET hiện đại đã chạy đa nền tảng.</p></div>
      <div class="card" data-asp style="left:96px;top:262px;width:520px;height:238px;padding:22px 24px">
        <div style="display:flex;align-items:center;gap:12px">${logoWrap('dotnet', 50)}<div><b style="font-family:Quicksand;font-size:23px;color:#0F172A">ASP.NET Core</b><div style="font-size:11.5px;color:#64748B">Framework web đa nền tảng</div></div></div>
        <p style="font-size:13px;line-height:1.55;color:#64748B;margin-top:14px">Xây web API và ứng dụng web hiệu năng cao trên .NET.</p>
        <div style="display:flex;gap:8px;margin-top:14px"><span class="chip purple-chip">Web API</span><span class="chip purple-chip">MVC</span><span class="chip purple-chip">SignalR</span></div>
      </div>
      <div class="card" data-ef style="left:1320px;top:262px;width:504px;height:238px;padding:22px 24px">
        <div class="card-kicker" style="color:#512BD4">ORM</div>
        <b style="display:block;font-family:Quicksand;font-size:22px;color:#0F172A;margin-top:8px">Entity Framework Core</b>
        <p style="font-size:13px;line-height:1.55;color:#64748B;margin-top:10px">Làm việc với database bằng đối tượng thay vì SQL thủ công.</p>
        <div style="margin-top:14px;background:#F5F0FF;border:1px solid #E4D9FF;border-radius:10px;padding:10px;font-family:JetBrains;font-size:11px;color:#4C1D95">var users = await db.Users.ToListAsync();</div>
      </div>
      <div style="position:absolute;left:990px;top:250px;width:310px;height:310px;border-radius:50%;background:radial-gradient(circle at 50% 42%,#F5F0FF,#EDE4FF);border:3px dashed #C4B5FD" data-ring>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px">${logoWrap('dotnet', 88)}<b style="font-family:Quicksand;font-size:25px;color:#3B0764">.NET</b><span style="font-size:11px;color:#6D28D9">nền tảng / runtime</span><div style="display:flex;gap:6px;margin-top:4px"><span class="chip purple-chip" style="font-size:10px;padding:3px 7px">CLR</span><span class="chip purple-chip" style="font-size:10px;padding:3px 7px">Cross-platform</span></div></div>
      </div>
      <div data-code></div>
      <div style="position:absolute;left:1040px;top:568px;width:784px;display:flex;flex-wrap:wrap;gap:8px" data-use>
        <span class="chip purple-chip">Quản lý doanh nghiệp</span><span class="chip purple-chip">Nhân sự</span><span class="chip purple-chip">Web API</span><span class="chip purple-chip">Hệ thống nội bộ</span>
      </div>
      <div class="card" data-note style="left:1040px;top:662px;width:784px;height:124px;padding:18px 22px;display:flex;align-items:center;gap:14px"><span style="width:46px;height:46px;border-radius:13px;background:#F5F0FF;color:#512BD4;display:flex;align-items:center;justify-content:center;flex:none">${icon('globe', 25)}</span><div style="font-size:13px;line-height:1.55;color:#475569">Minimal APIs cho phép dựng HTTP API gọn nhẹ chỉ với vài dòng — vẫn nằm trong ASP.NET Core, không phải framework riêng.</div></div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "var builder = WebApplication.CreateBuilder(args);",
      "var app = builder.Build();",
      "",
      "app.MapGet(\"/hello\", () => \"Xin chào từ .NET\");",
      "app.MapGet(\"/users/{id}\", async (int id, AppDb db) =>",
      "    await db.Users.FindAsync(id));",
      "",
      "app.Run();"
    ], { x: 96, y: 560, w: 840, name: 'Program.cs', badge: 'MINIMAL API' }));
    const asp = cam.querySelector('[data-asp]');
    const ef = cam.querySelector('[data-ef]');
    const ring = cam.querySelector('[data-ring]');
    const use = cam.querySelector('[data-use]');
    const note = cam.querySelector('[data-note]');
    return {
      update(U) {
        fade(asp, U.p(0, 0.05, 0.55), 18);
        fade(ring, U.p(0, 0.3, 0.55), 18, 0, 0.95);
        fade(ef, U.p(1, 0.05, 0.55), 18);
        fade(use, U.p(2, 0.05, 0.5), 12);
        fade(note, U.p(2, 0.25, 0.5), 12);
        return `scale(${1 + U.p(0, 0, 30) * 0.007})`;
      }
    };
  };

  B.go = (cam) => {
    const dots = Array.from({ length: 200 }, (_, i) => `<span data-g="${i}"></span>`).join('');
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 06</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('go', 58)} Go <span style="font-family:BeVietnam;font-size:22px;color:#94A3B8;font-weight:500">(Golang)</span></h1><p class="scene-sub">Đơn giản, đồng thời và sinh ra cho các dịch vụ chịu tải lớn.</p></div>
      <div class="card" data-gor style="left:96px;top:262px;width:620px;height:378px;padding:22px 24px">
        <div style="display:flex;justify-content:space-between;align-items:center"><div class="card-kicker">GOROUTINE</div><span class="mini-note">HÀNG NGHÌN TÁC VỤ NHẸ</span></div>
        <div class="gor" style="margin-top:18px" data-grid>${dots}</div>
      </div>
      ${[
        { n: 'Gin', k: 'gin', d: 'Nhẹ, phổ biến, định tuyến nhanh gọn.', tag: 'Phổ biến' },
        { n: 'Echo', k: 'echo', d: 'Đầy đủ tính năng, middleware phong phú.', tag: 'Đầy đủ' },
        { n: 'Fiber', k: 'fiber', d: 'Cú pháp gần Express, chạy trên fasthttp.', tag: 'Quen thuộc' }
      ].map((x, i) => `<div class="eco-card" data-fw="${i}" style="left:760px;top:${262 + i * 144}px;width:500px;height:130px">
        <div class="ec-top">${logoWrap(x.k, 46)}<div><b>${x.n}</b><div class="ec-sub">${x.tag}</div></div></div>
        <p>${x.d}</p>
      </div>`).join('')}
      <div class="card" data-std style="left:760px;top:752px;width:500px;height:82px;padding:14px 18px;display:flex;align-items:center;gap:11px"><span style="color:#00ADD8">${icon('box', 23)}</span><div style="font-size:12.5px;color:#475569">Cũng có thể dùng thư viện chuẩn <b style="font-family:JetBrains">net/http</b>.</div></div>
      <div data-code></div>
      <div style="position:absolute;left:760px;top:700px;width:500px;display:flex;flex-wrap:wrap;gap:8px" data-use>
        <span class="chip green-chip">Microservices</span><span class="chip green-chip">Tải cao</span><span class="chip green-chip">Độ trễ thấp</span>
      </div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "r := gin.Default()",
      "",
      "r.GET(\"/ping\", func(c *gin.Context) {",
      "  c.JSON(200, gin.H{\"message\": \"pong\"})",
      "})",
      "",
      "r.Run(\":8080\")"
    ], { x: 96, y: 672, w: 620, compact: true, name: 'main.go', badge: 'GIN' }));
    const grid = cam.querySelector('[data-grid]');
    const spans = [...grid.querySelectorAll('span')];
    const fws = [...cam.querySelectorAll('[data-fw]')];
    const use = cam.querySelector('[data-use]');
    const std = cam.querySelector('[data-std]');
    return {
      update(U) {
        spans.forEach((s, i) => {
          const phase = (U.t * 0.9 + i * 0.37) % 4;
          s.classList.toggle('on', phase < 1.6 || (i % 7 === Math.floor(U.t * 3) % 7));
        });
        fws.forEach((f, i) => fade(f, U.p(1, 0.1 + i * 0.28, 0.5), 18, 0, 0.97));
        fade(use, U.p(2, 0.05, 0.5), 12);
        fade(std, U.p(2, 0.28, 0.5), 12);
        return `scale(${1 + U.p(0, 0, 30) * 0.007})`;
      }
    };
  };

  B.ruby = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 03 · HỆ SINH THÁI 07</div><h1 class="scene-title" style="display:flex;align-items:center;gap:16px">${logoWrap('ruby', 58)} Ruby</h1><p class="scene-sub">Triết lý lập trình vui vẻ — và tốc độ phát triển sản phẩm rất đáng nể.</p></div>
      <div class="card" data-rails style="left:96px;top:262px;width:760px;height:470px;padding:24px 26px">
        <div style="display:flex;align-items:center;gap:14px">${logoWrap('rails', 64)}<div><b style="font-family:Quicksand;font-size:28px;color:#0F172A">Rails</b><div style="font-size:12px;color:#64748B">Convention over Configuration</div></div></div>
        <div style="margin-top:14px;display:inline-flex;gap:8px;align-items:center;background:#FEF2F2;border:1px solid #FEE2E2;border-radius:10px;padding:7px 12px;font-family:Jakarta;font-size:11px;font-weight:700;letter-spacing:.08em;color:#B91C1C">QUY ƯỚC HƠN CẤU HÌNH</div>
        <div style="margin-top:16px;background:#0B1526;border-radius:12px;padding:16px 18px;font-family:JetBrains;font-size:13.5px;line-height:1.8;color:#D6E3F5" data-term>
          <div><span style="color:#86EFAC">$</span> rails new shop</div>
          <div style="color:#5B7292">create  app/controllers</div>
          <div style="color:#5B7292">create  app/models</div>
          <div style="color:#5B7292">create  config/routes.rb</div>
          <div><span style="color:#86EFAC">$</span> rails generate scaffold Product name price</div>
          <div style="color:#5B7292">route  resources :products</div>
        </div>
        <p style="font-size:13px;line-height:1.55;color:#64748B;margin-top:14px">Rails lo phần khung; bạn tập trung vào nghiệp vụ. Hợp web app, nền tảng dịch vụ, startup cần ra mắt nhanh.</p>
      </div>
      <div class="eco-card" data-sinatra style="left:900px;top:262px;width:420px;height:196px">
        <div class="ec-top">${logoWrap('sinatra', 46)}<div><b>Sinatra</b><div class="ec-sub">Micro-framework / DSL</div></div></div>
        <p>Route tối giản cho API nhỏ hoặc dịch vụ nội bộ.</p>
      </div>
      <div class="card" data-trade style="left:900px;top:482px;width:420px;height:250px;padding:20px 22px">
        <div class="card-kicker">ĐÁNH ĐỔI</div>
        <div style="display:flex;flex-direction:column;gap:13px;margin-top:14px;font-size:13.5px;color:#334155">
          <div><b style="color:#047857">Tốc độ phát triển</b><br><span style="color:#64748B">Rất nhanh, ít cấu hình.</span></div>
          <div><b style="color:#B91C1C">Hiệu năng thuần</b><br><span style="color:#64748B">Không phải điểm mạnh nhất.</span></div>
        </div>
      </div>
      <div data-code></div>
      <div style="position:absolute;left:900px;top:752px;width:924px;display:flex;flex-wrap:wrap;gap:8px" data-use>
        <span class="chip red-chip">Web application</span><span class="chip red-chip">Nền tảng dịch vụ</span><span class="chip red-chip">Startup</span><span class="chip red-chip">MVP nhanh</span>
      </div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "require 'sinatra'",
      "",
      "get '/ping' do",
      "  content_type :json",
      "  { message: 'pong' }.to_json",
      "end",
      "",
      "get '/shop' do",
      "  erb :shop",
      "end"
    ], { x: 1360, y: 262, w: 464, name: 'app.rb', badge: 'SINATRA' }));
    const rails = cam.querySelector('[data-rails]');
    const sinatra = cam.querySelector('[data-sinatra]');
    const trade = cam.querySelector('[data-trade]');
    const term = cam.querySelector('[data-term]');
    const use = cam.querySelector('[data-use]');
    return {
      update(U) {
        fade(rails, U.p(0, 0.05, 0.55), 18);
        const lines = [...term.children];
        lines.forEach((l, i) => fade(l, U.p(0, 0.25 + i * 0.16, 0.32), 6));
        fade(sinatra, U.p(1, 0.05, 0.5), 18);
        fade(trade, U.p(2, 0.05, 0.55), 18);
        fade(use, U.p(2, 0.2, 0.5), 12);
        return `scale(${1 + U.p(0, 0, 28) * 0.007})`;
      }
    };
  };

  /* ---------- 16 COMPARE ---------- */
  B.compare = (cam) => {
    const rows = [
      ['javascript', 'JavaScript / TS', 'JavaScript, TypeScript', 'Node.js · Express · NestJS · Fastify', 'Web, API, realtime, mobile'],
      ['python', 'Python', 'Python', 'Django · Flask · FastAPI', 'API, AI, dữ liệu, quản lý'],
      ['php', 'PHP', 'PHP', 'Laravel · Symfony · CodeIgniter', 'Web doanh nghiệp, CMS, admin'],
      ['java', 'Java', 'Java', 'Spring Boot · Quarkus · Micronaut', 'Ngân hàng, giao dịch, microservices'],
      ['csharp', 'C#', 'C#', 'ASP.NET Core · EF Core', 'Doanh nghiệp, nhân sự, nội bộ'],
      ['go', 'Go', 'Go', 'Gin · Echo · Fiber · net/http', 'Hiệu năng, đồng thời, tải cao'],
      ['ruby', 'Ruby', 'Ruby', 'Rails · Sinatra', 'Web app, dịch vụ, startup']
    ];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 04 · SO SÁNH</div><h1 class="scene-title">Bảy hệ sinh thái <span class="accent">cạnh nhau</span></h1><p class="scene-sub">Không chấm điểm tuyệt đối — chỉ đối chiếu ngôn ngữ, framework và bài toán điển hình.</p></div>
      <div class="cmp" data-table>
        <div class="cmp-row head"><span>Hệ sinh thái</span><span>Ngôn ngữ</span><span>Framework tiêu biểu</span><span>Thế mạnh · bài toán</span></div>
        ${rows.map((r, i) => `<div class="cmp-row" data-row="${i}"><span class="eco">${logoWrap(r[0], 34, { sm: true })}${r[1]}</span><span class="lg">${r[2]}</span><span class="fw">${r[3]}</span><span class="use">${r[4]}</span></div>`).join('')}
      </div>
      <div class="cmp-cover" data-cover style="left:96px;top:238px;width:1400px;height:496px;border-radius:20px">
        <div style="text-align:center"><div style="font-family:Quicksand;font-size:54px;font-weight:700;color:#0F172A;line-height:1.1">KHÔNG CÓ<br><span style="color:#2563EB">FRAMEWORK TỐT NHẤT</span></div><div style="margin-top:14px;font-size:18px;color:#64748B">Mỗi công cụ sinh ra cho một bài toán.</div></div>
      </div>
      <div class="card" data-crit style="left:1530px;top:238px;width:294px;height:496px;padding:20px 20px;opacity:0">
        <div class="card-kicker" style="font-size:11px">SÁU TIÊU CHÍ</div>
        <div style="display:flex;flex-direction:column;gap:10px;margin-top:14px">
          ${[['chart', 'Quy mô dự án'], ['layers', 'Yêu cầu nghiệp vụ'], ['bolt', 'Hiệu năng'], ['user', 'Đội ngũ hiện có'], ['box', 'Hệ sinh thái'], ['gear', 'Khả năng bảo trì']].map(([ic, t]) => `<div style="display:flex;align-items:center;gap:9px;padding:9px 10px;border-radius:10px;background:#F6FAFF;border:1px solid #E4EFFA;font-size:12.5px;color:#334155">${icon(ic, 17)} ${t}</div>`).join('')}
        </div>
      </div>
      <div class="quote-card" data-quote style="left:96px;top:752px;width:1400px;height:96px;display:flex;align-items:center;gap:18px;opacity:0">
        <div class="qm">“</div><p style="flex:1">Chọn công nghệ đội bạn giỏi — nhanh hơn chọn công nghệ đang hot nhưng không ai biết dùng.</p>
      </div>`;
    const rowEls = [...cam.querySelectorAll('[data-row]')];
    const table = cam.querySelector('[data-table]');
    const cover = cam.querySelector('[data-cover]');
    const crit = cam.querySelector('[data-crit]');
    const quote = cam.querySelector('[data-quote]');
    return {
      update(U) {
        fade(table, U.p(0, 0.05, 0.5), 16);
        rowEls.forEach((r, i) => fade(r, U.p(0, 0.2 + i * 0.35, 0.5), 14, 0, 0.98));
        const c = U.p(1, 0.15, 0.45);
        cover.style.opacity = c * (1 - U.p(2, 0.05, 0.35));
        cover.style.transform = `scale(${1 + (1 - c) * 0.04})`;
        fade(crit, U.p(2, 0.1, 0.55), 20, 18);
        fade(quote, U.p(3, 0.1, 0.55), 16, 0, 0.98);
        table.style.filter = U.on(2) ? 'saturate(.55)' : 'none';
        return `scale(${1 + U.p(0, 0, 34) * 0.006})`;
      }
    };
  };

  /* ---------- 17 CHOOSE ---------- */
  B.choose = (cam) => {
    const crit = ['Quy mô dự án', 'Hiệu năng', 'Đội ngũ', 'Hệ sinh thái', 'Chi phí bảo trì'];
    const scen = [
      { n: '01', t: 'REST API nhỏ, ra mắt nhanh', s: 'Ít nghi thức, triển khai gọn', techs: [['express', 'Express'], ['fastapi', 'FastAPI']] },
      { n: '02', t: 'Quản lý nhiều nghiệp vụ', s: 'Cần cấu trúc, auth, admin, ORM', techs: [['laravel', 'Laravel'], ['django', 'Django'], ['nestjs', 'NestJS'], ['dotnet', 'ASP.NET Core']] },
      { n: '03', t: 'Doanh nghiệp lớn', s: 'Ổn định, bảo mật, tích hợp sâu', techs: [['springboot', 'Spring Boot'], ['dotnet', 'ASP.NET Core']] }
    ];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 04 · LỰA CHỌN</div><h1 class="scene-title">Chọn theo <span class="accent">bài toán</span>, không theo trend</h1><p class="scene-sub">Năm câu hỏi trước khi chốt công nghệ — và ba kịch bản thường gặp.</p></div>
      <div class="card" data-crit style="left:96px;top:262px;width:380px;height:470px;padding:22px 24px">
        <div class="card-kicker">NĂM CÂU HỎI</div>
        <div style="display:flex;flex-direction:column;gap:11px;margin-top:16px">
          ${crit.map((c, i) => `<div style="display:flex;align-items:center;gap:11px;padding:11px 13px;border-radius:12px;background:#F6FAFF;border:1px solid #E4EFFA" data-c="${i}"><span class="num" style="font-size:12px;color:#2563EB">0${i + 1}</span><span style="font-size:14px;color:#334155">${c}</span></div>`).join('')}
        </div>
      </div>
      ${scen.map((s, i) => `<div class="card" data-scen="${i}" style="left:520px;top:${262 + i * 166}px;width:1304px;height:146px;padding:20px 24px;display:flex;align-items:center;gap:22px">
        <div style="width:360px;flex:none"><div style="display:flex;align-items:center;gap:10px"><span class="num" style="font-size:13px;color:#2563EB">${s.n}</span><b style="font-family:Quicksand;font-size:21px;color:#0F172A">${s.t}</b></div><div style="font-size:12.5px;color:#64748B;margin-top:5px">${s.s}</div></div>
        <div style="color:#93C5FD">${icon('arrow', 26)}</div>
        <div style="display:flex;gap:9px;flex-wrap:wrap;flex:1">${s.techs.map(([k, n]) => `<span class="chip" style="font-size:13.5px">${logoWrap(k, 22, { sm: true })} ${n}</span>`).join('')}</div>
      </div>`).join('')}`;
    const critEls = [...cam.querySelectorAll('[data-c]')];
    const scens = [...cam.querySelectorAll('[data-scen]')];
    return {
      update(U) {
        critEls.forEach((c, i) => fade(c, U.p(0, 0.08 + i * 0.16, 0.45), 12, 10));
        scens.forEach((s, i) => fade(s, U.p(i + 1, 0.1, 0.55), 22, 0, 0.97));
        return `scale(${1 + U.p(0, 0, 30) * 0.007})`;
      }
    };
  };

  /* ---------- 18 LOGIN ---------- */
  B.login = (cam) => {
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 05 · BACKEND IN ACTION</div><h1 class="scene-title">Backend <span class="accent">hoạt động thật</span></h1><p class="scene-sub">Form đăng nhập bên trái, API Express bên phải — nhìn từng bước đồng bộ.</p></div>
      <div class="card" data-form style="left:96px;top:250px;width:560px;height:470px;padding:24px 26px">
        <div style="display:flex;align-items:center;justify-content:space-between"><div class="card-kicker">ĐĂNG NHẬP</div><span class="chip green-chip" data-status style="font-size:10px;padding:4px 9px">READY</span></div>
        <div style="margin-top:20px"><div style="font-size:12px;color:#64748B;margin-bottom:6px">Email</div><div class="field" style="height:46px;font-size:14px">an@example.com</div>
        <div style="font-size:12px;color:#64748B;margin:14px 0 6px">Mật khẩu</div><div class="field" style="height:46px;font-size:18px;letter-spacing:.18em">••••••••</div></div>
        <div class="login-btn" style="margin-top:22px;height:48px;font-size:16px" data-btn>Đăng nhập</div>
        <div style="margin-top:16px;display:flex;gap:8px;align-items:center;font-size:11px;color:#94A3B8">${icon('lock', 15)} Mật khẩu không bao giờ lưu dạng văn bản thuần.</div>
        <div style="margin-top:20px;padding:12px 14px;border-radius:10px;background:#F8FBFF;border:1px solid #E1ECF8;font-family:JetBrains;font-size:11px;color:#64748B" data-db>${icon('db', 15)} DB: SELECT * FROM users WHERE email = ?</div>
      </div>
      <div data-code></div>
      <div class="toast err" data-err style="left:150px;top:744px">${icon('alert', 18)} 401 · Sai email hoặc mật khẩu</div>
      <div class="toast ok" data-ok style="left:150px;top:744px">${icon('check', 18)} 200 · Đăng nhập thành công</div>
      <div class="packet blue" data-packet style="left:620px;top:430px;opacity:0"><span class="trail"></span><span class="core"></span></div>
      <div class="steps" data-steps style="left:250px;top:790px">
        ${['Nhận request', 'Kiểm tra dữ liệu', 'Tìm user', 'So hash', 'Ký JWT', 'Trả response', 'Lưu token', 'Chuyển trang'].map((s, i) => `<div class="step" data-step="${i}" style="width:160px"><div class="sd">${i + 1}</div><span>${s}</span></div>`).join('')}
      </div>`;
    cam.querySelector('[data-code]').replaceWith(codePanel([
      "import express from 'express';",
      "import bcrypt from 'bcrypt';",
      "import jwt from 'jsonwebtoken';",
      "",
      "const app = express();",
      "app.use(express.json());",
      "",
      "app.post('/login', async (req, res) => {",
      "  const { email, password } = req.body;",
      "  if (!email || !password) return res.status(400).end();",
      "",
      "  const user = await db.users.findByEmail(email);",
      "  if (!user) return res.status(401).json({ error: 'Sai email hoặc mật khẩu' });",
      "",
      "  const ok = await bcrypt.compare(password, user.password_hash);",
      "  if (!ok) return res.status(401).json({ error: 'Sai email hoặc mật khẩu' });",
      "",
      "  const token = jwt.sign({ sub: user.id }, process.env.JWT_SECRET, { expiresIn: '15m' });",
      "  res.json({ token, user: { id: user.id, name: user.name } });",
      "});"
    ], { x: 700, y: 238, w: 1124, compact: true, name: 'server.js', badge: 'EXPRESS · BCRYPT · JWT' }));
    const code = cam.querySelector('.code-panel');
    const status = cam.querySelector('[data-status]');
    const btn = cam.querySelector('[data-btn]');
    const db = cam.querySelector('[data-db]');
    const err = cam.querySelector('[data-err]');
    const ok = cam.querySelector('[data-ok]');
    const packet = cam.querySelector('[data-packet]');
    const steps = [...cam.querySelectorAll('[data-step]')];
    const lineEls = [...code.querySelectorAll('.code-line')];
    const highlight = (idx) => {
      lineEls.forEach((l) => {
        const i = +l.dataset.l;
        l.classList.toggle('hot', idx.includes(i));
        l.classList.toggle('dim', idx.length > 0 && !idx.includes(i));
      });
    };
    return {
      update(U) {
        fade(cam.querySelector('[data-form]'), U.p(0, 0.05, 0.55), 18);
        fade(code, U.p(0, 0.2, 0.55), 18, 12);
        btn.style.transform = U.on(1) && U.cueT(1) < 0.3 ? 'scale(.97)' : 'scale(1)';
        let hi = [];
        if (U.on(1) && U.t < U.cueStart(2)) hi = [10, 11, 12, 13, 14, 15];
        if (U.on(2) && U.t < U.cueStart(3)) hi = [12, 13, 15, 16];
        if (U.on(3)) hi = [18, 19];
        highlight(hi);
        const dbOn = U.on(1) && U.t < U.cueStart(3);
        db.style.background = dbOn ? '#EAF6FF' : '#F8FBFF';
        db.style.borderColor = dbOn ? '#93C5FD' : '#E1ECF8';
        fade(db, U.p(1, 0.1, 0.4), 6);
        const e = U.on(2) && U.t < U.cueStart(3);
        const o = U.on(3) && U.t < U.cueStart(3) + 3.6;
        err.style.opacity = e ? 1 : 0;
        err.style.transform = `translateY(${e ? 0 : 10}px)`;
        ok.style.opacity = o ? 1 : 0;
        ok.style.transform = `translateY(${o ? 0 : 10}px)`;
        status.textContent = U.on(3) ? '200 OK' : U.on(2) ? '401' : 'READY';
        status.className = 'chip ' + (U.on(3) ? 'green-chip' : U.on(2) ? 'red-chip' : 'green-chip');
        status.style.fontSize = '10px'; status.style.padding = '4px 9px';
        const pt = U.cueT(1);
        packet.style.opacity = pt > 0 && pt < 2.2 ? 1 : (U.on(3) && U.cueT(3) < 2.2 ? 1 : 0);
        packet.style.left = (620 + Math.abs(Math.sin(U.t * 2.2)) * 70) + 'px';
        const activeStep = U.on(3) ? 7 : U.on(2) ? 3 : U.on(1) ? Math.min(5, 1 + Math.floor((U.t - U.cueStart(1)) / 2.2)) : 0;
        steps.forEach((s, i) => {
          s.classList.toggle('on', i === activeStep);
          s.classList.toggle('done', i < activeStep);
        });
        return `scale(${1 + U.p(0, 0, 30) * 0.006})`;
      }
    };
  };

  /* ---------- 19 RECAP ---------- */
  B.recap = (cam) => {
    const items = [
      { n: '01', t: 'Backend', d: 'Xử lý nghiệp vụ, xác thực và dữ liệu phía máy chủ.', ic: 'server', c: '#2563EB' },
      { n: '02', t: 'Ngôn ngữ', d: 'Công cụ viết mã và xây logic.', ic: 'code', c: '#06B6D4' },
      { n: '03', t: 'Framework', d: 'Bộ khung, quy ước và thư viện hỗ trợ.', ic: 'layers', c: '#8B5CF6' },
      { n: '04', t: 'Nhiều lựa chọn', d: 'Mỗi ngôn ngữ có nhiều framework, thế mạnh riêng.', ic: 'box', c: '#F59E0B' },
      { n: '05', t: 'Chọn theo bài toán', d: 'Quy mô, đội ngũ, hiệu năng, bảo trì — không theo trend.', ic: 'chart', c: '#10B981' }
    ];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1250px"><div class="eyebrow">PHẦN 06 · TỔNG KẾT</div><h1 class="scene-title">Năm điều <span class="accent">mang về</span></h1><p class="scene-sub">Nếu chỉ nhớ một câu: hiểu công cụ trước, chọn công nghệ sau.</p></div>
      ${items.map((x, i) => `<div class="card" data-tile="${i}" style="left:${96 + i * 350}px;top:${282 + (i % 2) * 34}px;width:320px;height:240px;padding:22px 22px">
        <div style="display:flex;align-items:center;justify-content:space-between"><span class="num" style="font-size:34px;color:${x.c}">${x.n}</span><span style="width:48px;height:48px;border-radius:14px;background:${x.c}16;color:${x.c};display:flex;align-items:center;justify-content:center">${icon(x.ic, 25)}</span></div>
        <h3 style="font-family:Quicksand;font-size:20px;color:#0F172A;margin-top:10px">${x.t}</h3><p style="font-size:12.5px;line-height:1.5;color:#64748B;margin-top:6px">${x.d}</p>
      </div>`).join('')}
      <div class="card" data-banner style="left:300px;top:612px;width:1320px;height:86px;display:flex;align-items:center;gap:16px;padding:0 26px;opacity:0;background:linear-gradient(100deg,#EFF6FF,#F5F3FF)">
        <span style="width:50px;height:50px;border-radius:50%;background:#10B981;color:#fff;display:flex;align-items:center;justify-content:center;flex:none">${icon('check', 28)}</span>
        <div><div style="font-family:Quicksand;font-weight:700;font-size:24px;color:#0F172A">Hiểu công cụ — chọn đúng công nghệ</div><div style="font-size:13px;color:#64748B">Đừng học framework trước khi hiểu ngôn ngữ. Đừng chọn công nghệ trước khi hiểu dự án.</div></div>
      </div>
      <div class="teacher-slot"></div>`;
    const tr = teacher({ pose: 'wave', width: 200, style: 'left:1628px;top:650px;' });
    cam.querySelector('.teacher-slot').replaceWith(tr.el);
    const tiles = [...cam.querySelectorAll('[data-tile]')];
    const banner = cam.querySelector('[data-banner]');
    return {
      update(U) {
        tiles.forEach((t, i) => fade(t, U.p(0, 0.1 + i * 0.25, 0.5), 24, 0, 0.96));
        fade(banner, U.p(1, 0.05, 0.6), 18, 0, 0.98);
        tr.update(U.t, 'wave');
        return `scale(${1 + U.p(0, 0, 20) * 0.006})`;
      }
    };
  };

  /* ---------- 20 QUIZ ---------- */
  B.quiz = (cam) => {
    const QS = [
      { q: 'Node.js là ngôn ngữ lập trình hay môi trường thực thi?', opts: ['Ngôn ngữ lập trình', 'Môi trường thực thi'], a: 1, ex: 'Node.js chạy JavaScript; ngôn ngữ là JavaScript còn Node.js là runtime.' },
      { q: 'Framework nào thường được dùng trong hệ sinh thái Java?', opts: ['Laravel', 'Spring Boot'], a: 1, ex: 'Spring Boot là framework Java. Quarkus và Micronaut cho nhu cầu cloud native.' },
      { q: 'Framework nào phù hợp để xây API bằng Python?', opts: ['FastAPI', 'Ruby on Rails'], a: 0, ex: 'FastAPI tối ưu cho API hiện đại; Flask và Django cũng dùng được.' }
    ];
    const labels = ['A', 'B'];
    cam.innerHTML = `
      <div class="scene-head" style="max-width:1100px"><div class="eyebrow">PHẦN 06 · ÔN TẬP</div><h1 class="scene-title">Kiểm tra nhanh</h1><p class="scene-sub">Ba câu, mỗi câu ba giây. Chọn đáp án trong đầu trước khi đáp án hiện ra.</p></div>
      <div class="card quiz-panel" style="left:150px;top:262px;width:1320px;height:580px">
        ${QS.map((q, i) => `<div class="quiz-group" data-q="${i}" style="position:absolute;inset:26px 34px">
          <div class="quiz-top"><div class="quiz-kicker">CÂU HỎI ${i + 1} / 3</div><div class="quiz-counter" style="font-size:11px;letter-spacing:.14em;color:#94A3B8">CHỌN MỘT ĐÁP ÁN</div></div>
          <div class="quiz-progress">${[0, 1, 2].map((k) => `<span class="${k <= i ? 'on' : ''}"></span>`).join('')}</div>
          <div class="quiz-q">${q.q}</div>
          <div class="quiz-ring" data-ring="${i}"><svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="41" fill="none" stroke="#E2EFFB" stroke-width="7"/><circle class="ring-fill" cx="48" cy="48" r="41" fill="none" stroke="#2563EB" stroke-width="7" stroke-linecap="round" stroke-dasharray="257.6" stroke-dashoffset="0"/></svg><div class="num3">3</div></div>
          <div class="quiz-options">${q.opts.map((o, k) => `<div class="q-option" data-o="${k}"><span class="k">${labels[k]}</span><span>${o}</span></div>`).join('')}</div>
          <div class="quiz-explain" data-ex>${q.ex}</div>
        </div>`).join('')}
        <div class="quiz-foot"><span>Đáp án hiện sau 3 giây đếm ngược</span><b>AN TECH ACADEMY · REVIEW</b></div>
      </div>
      <div class="teacher-slot"></div>`;
    const tr = teacher({ pose: 'explain', width: 218, style: 'left:1520px;top:600px;' });
    cam.querySelector('.teacher-slot').replaceWith(tr.el);
    const groups = [...cam.querySelectorAll('[data-q]')];
    const meta = [{ q: 0, a: 1 }, { q: 2, a: 3 }, { q: 4, a: 5 }];
    return {
      update(U) {
        let active = 0;
        if (U.t >= U.cueStart(2)) active = 1;
        if (U.t >= U.cueStart(4)) active = 2;
        groups.forEach((g, i) => {
          const on = i === active;
          g.style.opacity = on ? 1 : 0;
          g.style.transform = `translateY(${on ? 0 : 16}px)`;
        });
        const m = meta[active];
        const g = groups[active];
        const q = QS[active];
        const qEnd = U.cueEnd(m.q);
        const aStart = U.cueStart(m.a);
        const hold = Math.max(0.01, Math.min(3, qEnd - (aStart - 0.3)));
        const t0 = qEnd - hold;
        const p = clamp((U.t - t0) / hold);
        const answered = U.t >= qEnd - 0.02;
        const ring = g.querySelector('.ring-fill');
        const ringBox = g.querySelector('.quiz-ring');
        const num = g.querySelector('.num3');
        ring.style.strokeDashoffset = 257.6 * p;
        ringBox.style.opacity = U.t >= t0 && !answered ? 1 : 0;
        num.style.opacity = U.t >= t0 && !answered ? 1 : 0;
        num.textContent = String(Math.max(1, Math.ceil(3 * (1 - p))));
        g.querySelectorAll('.q-option').forEach((o, k) => {
          o.classList.toggle('correct', answered && k === q.a);
          o.classList.toggle('dim', answered && k !== q.a);
        });
        const ex = g.querySelector('[data-ex]');
        ex.style.opacity = answered ? 1 : 0;
        ex.style.transform = `translateY(${answered ? 0 : 8}px)`;
        tr.update(U.t, answered ? 'wave' : 'explain');
        return `scale(${1 + U.p(0, 0, 40) * 0.006})`;
      }
    };
  };

  /* ---------- 21 OUTRO ---------- */
  B.outro = (cam, def) => {
    cam.innerHTML = `
      <div class="outro-k">AN TECH ACADEMY · BACKEND SERIES</div>
      <div class="outro-quote">
        <h2 class="outro-h" data-h>Backend chính là bộ não<br>phía sau mỗi ứng dụng web.</h2>
        <svg class="scribble" style="margin:6px auto 0;width:340px" viewBox="0 0 300 16"><path data-scrib d="M4 10C64 3 150 3 208 7c30 2 58 4 88 1"/></svg>
        <p class="outro-p">Hiểu ngôn ngữ và framework sẽ giúp bạn chọn đúng công nghệ, xây những hệ thống mạnh mẽ và chuyên nghiệp hơn.</p>
        <div class="outro-chips"><span class="chip">${icon('server', 18)} Hiểu backend</span><span class="chip purple-chip">${icon('layers', 18)} Phân biệt công cụ</span><span class="chip amber-chip">${icon('chart', 18)} Chọn theo bài toán</span></div>
      </div>
      <div class="outro-teacher"></div>
      <div class="outro-sign">HẸN GẶP BẠN Ở BÀI TIẾP THEO</div>
      <div style="position:absolute;right:150px;top:300px;display:flex;flex-direction:column;align-items:center;gap:10px;opacity:.92">
        <svg width="86" height="86" viewBox="0 0 48 48"><rect x="4" y="4" width="40" height="40" rx="13" fill="#1D4ED8"/><path d="M14 32l7-16 4 9 3-6 6 13" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="34" cy="14" r="4" fill="#F59E0B"/></svg>
        <div style="font-family:Quicksand;font-weight:700;font-size:18px;letter-spacing:.14em;color:#1D4ED8">AN TECH ACADEMY</div>
      </div>`;
    const tr = teacher({ pose: 'wave', width: 300, style: 'left:120px;top:430px;' });
    cam.querySelector('.outro-teacher').replaceWith(tr.el);
    const hh = cam.querySelector('[data-h]');
    const p = cam.querySelector('.outro-p');
    const chips = [...cam.querySelectorAll('.chip')];
    const scrib = cam.querySelector('[data-scrib]');
    const k = cam.querySelector('.outro-k');
    const sign = cam.querySelector('.outro-sign');
    return {
      update(U) {
        const pp = U.p(0, 0.05, 0.7);
        k.style.opacity = pp;
        fade(hh, U.p(0, 0.1, 0.7), 26, 0, 0.97);
        scrib.style.strokeDashoffset = 100 * (1 - U.p(0, 0.5, 0.7));
        fade(p, U.p(0, 0.8, 0.7), 16);
        chips.forEach((c, i) => fade(c, U.p(0, 1.0 + i * 0.2, 0.5), 12));
        fade(sign, U.p(0, 1.3, 0.6), 8);
        tr.update(U.t, 'wave');
        const end = U.p(0, def.dur - 2.4, 1.4);
        cam.style.background = `rgba(255,255,255,${end * 0.92})`;
        return `scale(${1 + U.p(0, 0, def.dur) * 0.02})`;
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
      cam.innerHTML = `<h1 style="position:absolute;left:96px;top:300px">${def.title}</h1>`;
      console.warn('missing builder', def.type);
    }
    const api = builder ? builder(cam, def) : null;
    const cues = def.cues.map((c) => ({ ...c, ls: c.start - def.start, le: c.end - def.start }));
    built.push({ def, el, cam, api, cues });
  });

  /* ---------- global decor ---------- */
  const floatRoot = document.getElementById('floating');
  const chips = [];
  const palette = ['#2563EB', '#06B6D4', '#F59E0B', '#8B5CF6', '#BFDBFE', '#FDE68A'];
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
      prev = cur;
      cur = idx;
      built.forEach((b, i) => {
        if (i === cur) b.el.classList.add('on');
        if (i !== cur && i !== prev) { b.el.classList.remove('on'); b.el.style.opacity = 0; }
      });
      const sc = TL.scenes[idx];
      if (sc.part) partChip.textContent = 'PHẦN ' + pad(sc.part) + ' · ' + PARTS[sc.part];
      else if (sc.id === 'quiz') partChip.textContent = 'ÔN TẬP · REVIEW';
      else if (sc.id === 'outro') partChip.textContent = 'KẾT THÚC · WRAP-UP';
      else partChip.textContent = 'BÀI GIẢNG · BACKEND';
      document.body.classList.toggle('dark-chrome', sc.type === 'divider' || ['div1', 'div2', 'div3'].includes(sc.type));
      sweep.style.background = sc.part === 2 || sc.part === 3
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
