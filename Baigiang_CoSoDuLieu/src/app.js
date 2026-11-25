/* ============================================================
   CƠ SỞ DỮ LIỆU — ĐỘNG CƠ DỰNG CẢNH (deterministic timeline)
   renderFrame(t) đặt toàn bộ trạng thái hình ảnh theo thời gian t.
   ============================================================ */
(() => {
  const TL = window.__TIMELINE;
  const root = document.getElementById('scenes');
  const captionEl = document.getElementById('caption');
  const fill = document.getElementById('progressFill');
  const plabel = document.getElementById('progressLabel');
  const tcode = document.getElementById('timecode');
  const partChip = document.getElementById('partChip');
  const flash = document.getElementById('transitionFlash');

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, p) => a + (b - a) * p;
  const ease = (p) => 1 - Math.pow(1 - clamp(p), 3);
  const smooth = (p) => { p = clamp(p); return p * p * (3 - 2 * p); };
  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (s) => `${pad(Math.floor(s / 60))}:${pad(Math.floor(s % 60))}`;
  const money = (n) => n.toLocaleString('vi-VN');

  const PARTS = [
    { n: 1, title: 'Giới thiệu cơ sở dữ liệu', en: 'FUNDAMENTALS' },
    { n: 2, title: 'Các thành phần của cơ sở dữ liệu', en: 'ANATOMY' },
    { n: 3, title: 'Các loại mối quan hệ', en: 'RELATIONSHIPS' },
    { n: 4, title: 'Thiết kế CSDL và sơ đồ ERD', en: 'DATA MODELING' },
    { n: 5, title: 'Ngôn ngữ SQL cơ bản', en: 'SQL BASICS' },
    { n: 6, title: 'Bài toán truy vấn thực tế', en: 'REAL QUERIES' },
    { n: 7, title: 'Tổng kết và ôn tập', en: 'REVIEW' }
  ];

  /* ---------- ICONS ---------- */
  const P = {
    db: '<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v14c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/>',
    table: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18M9 9v11M15 9v11"/>',
    key: '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 4l4 4M14 6l3 3"/>',
    link: '<path d="M10 13a5 5 0 0 0 7 0l2-2a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-2 2a5 5 0 0 0 7 7l1-1"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    users: '<circle cx="9" cy="8" r="3.5"/><path d="M2 21c0-3.8 3.1-6.5 7-6.5s7 2.7 7 6.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.5.7 4 2.7 4 5.5"/>',
    cart: '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.4 12h11L21 7H6"/>',
    receipt: '<path d="M6 2h12v20l-3-2-3 2-3-2-3 2V2z"/><path d="M9 7h6M9 11h6M9 15h4"/>',
    chart: '<path d="M3 21h18"/><path d="M6 17V9M11 17V4M16 17v-6M21 17v-9"/>',
    server: '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01"/>',
    shield: '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    refresh: '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>',
    layers: '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 12l10 5 10-5"/><path d="M2 17l10 5 10-5"/>',
    code: '<path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    check: '<path d="M20 6L9 17l-5-5"/>',
    alert: '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    sparkle: '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4L12 3z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    box: '<path d="M21 8l-9-5-9 5v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    lock: '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    zap: '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    flow: '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 6h10M6 8l5 8M18 8l-5 8"/>',
    filter: '<path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>',
    sum: '<path d="M18 4H7l6 8-6 8h11"/><path d="M15 4v16"/>'
  };
  const icon = (name, cls = 'icon') => `<svg class="${cls}" viewBox="0 0 24 24"><g stroke="currentColor" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${P[name] || ''}</g></svg>`;

  /* ---------- DOM helpers ---------- */
  function h(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  const show = (el, p, y = 18, x = 0) => {
    p = clamp(p);
    el.style.opacity = p;
    el.style.transform = `translate(${(1 - p) * x}px, ${(1 - p) * y}px)`;
  };
  function head(def) {
    return `<div class="scene-head"><div class="eyebrow">${def.part ? 'PHẦN ' + pad(def.part) + ' · ' + (PARTS[def.part - 1]?.en || '') : 'BÀI GIẢNG'}</div><h1 class="scene-title">${def.title}</h1></div>`;
  }

  /* ---------- DATA ---------- */
  const SV = [
    ['SV001', 'Nguyễn Văn An', 'DA22TTC', 'an@gmail.com'],
    ['SV002', 'Trần Thị Bình', 'DA22TTC', 'binh@gmail.com'],
    ['SV003', 'Lê Văn Nam', 'DA22TTC', 'nam@gmail.com']
  ];
  const SP = [
    ['SP01', 'iPhone 15 Pro Max', 'Apple', 32000000, 12],
    ['SP02', 'Galaxy S24 Ultra', 'Samsung', 30000000, 8],
    ['SP03', 'Xiaomi 14', 'Xiaomi', 14000000, 21],
    ['SP04', 'OPPO Reno 11', 'OPPO', 9500000, 17],
    ['SP05', 'Galaxy A55', 'Samsung', 8000000, 34]
  ];
  const KH = [
    ['KH01', 'Nguyễn Văn An', '0901 234 567', 'Quận 1, TP.HCM'],
    ['KH02', 'Trần Thị Bình', '0912 345 678', 'Thủ Đức, TP.HCM'],
    ['KH03', 'Lê Văn Nam', '0987 654 321', 'Quận 7, TP.HCM'],
    ['KH04', 'Phạm Thu Hà', '0909 888 777', 'Bình Thạnh, TP.HCM']
  ];
  const HD = [
    ['HD001', '05/03/2024', 'KH01', 'NV01'],
    ['HD002', '12/03/2024', 'KH02', 'NV01'],
    ['HD003', '02/04/2024', 'KH01', 'NV02'],
    ['HD004', '18/04/2024', 'KH03', 'NV02'],
    ['HD005', '25/04/2024', 'KH03', 'NV01']
  ];
  const CT = [
    ['HD001', 'SP01', 1, 32000000],
    ['HD001', 'SP05', 2, 8000000],
    ['HD002', 'SP02', 1, 30000000],
    ['HD002', 'SP04', 2, 9500000],
    ['HD003', 'SP01', 2, 32000000],
    ['HD004', 'SP03', 1, 14000000],
    ['HD004', 'SP05', 1, 8000000],
    ['HD005', 'SP01', 1, 32000000]
  ];

  /* ---------- TABLE BUILDER ---------- */
  function dataTable(headers, rows, opts = {}) {
    const wrap = h('div', 'table-wrap');
    const t = h('table', 'dt');
    const thead = h('thead');
    const trh = h('tr');
    headers.forEach((hd) => {
      const th = h('th', hd.cls || '', hd.label + (hd.tag ? `<span class="keytag ${hd.tag}">${hd.tag.toUpperCase()}</span>` : ''));
      trh.appendChild(th);
    });
    thead.appendChild(trh);
    const tbody = h('tbody');
    const rowEls = rows.map((r) => {
      const tr = h('tr');
      if (r.cls) tr.className = r.cls;
      (r.cells || r).forEach((c, i) => {
        const td = h('td', headers[i]?.cellCls || '', String(c));
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
      return tr;
    });
    t.append(thead, tbody);
    wrap.appendChild(t);
    return { el: wrap, rows: rowEls, table: t };
  }

  /* ---------- SQL CODE BUILDER ---------- */
  const KW = new Set(('CREATE ALTER DROP TABLE INSERT INTO VALUES UPDATE DELETE SELECT FROM WHERE AND OR NOT NULL PRIMARY KEY FOREIGN REFERENCES UNIQUE INNER JOIN LEFT RIGHT ON GROUP BY ORDER HAVING AS DISTINCT SUM COUNT AVG MIN MAX VARCHAR NVARCHAR INT DATE DECIMAL GRANT REVOKE COMMIT ROLLBACK USE SET').split(' '));
  const FN = new Set(['SUM', 'COUNT', 'AVG', 'MIN', 'MAX', 'GETDATE']);
  function tokenize(line) {
    const out = [];
    const re = /(--.*$)|(N?'(?:[^']|'')*')|(\b\d+(?:[.,]\d+)*\b)|([A-Za-z_À-ỹ][\wÀ-ỹ]*)|([(),;.*=<>+\-/]+)|(\s+)/g;
    let m;
    while ((m = re.exec(line))) {
      let cls = 'ident';
      if (m[1]) cls = 'cmt';
      else if (m[2]) cls = 'str';
      else if (m[3]) cls = 'num2';
      else if (m[4]) {
        const u = m[4].toUpperCase();
        cls = KW.has(u) ? 'kw' : FN.has(u) ? 'fn' : 'ident';
      } else cls = 'punct';
      out.push({ cls, text: m[0] });
    }
    return out;
  }
  function codeBlock(lines, opts = {}) {
    const box = h('div', 'editor');
    const bar = h('div', 'editor-bar', '<span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="editor-file">query.sql <b>— ' + (opts.context || 'CSDL_CuaHang') + '</b></span>');
    const area = h('div', 'code-area');
    area.style.fontSize = (opts.size || 25) + 'px';
    const chars = [];
    const lineEls = [];
    lines.forEach((ln, li) => {
      const ld = h('div', 'code-line');
      ld.dataset.n = li + 1;
      const tokens = tokenize(ln);
      tokens.forEach((tk) => {
        const sp = h('span', tk.cls);
        for (const ch of tk.text) {
          const cs = h('span', 'ch');
          cs.textContent = ch;
          sp.appendChild(cs);
          chars.push({ el: cs, line: li });
        }
        ld.appendChild(sp);
      });
      area.appendChild(ld);
      lineEls.push(ld);
    });
    const caret = h('span', 'caret');
    box.append(bar, area);
    let n = -1;
    let curLine = -1;
    function setTyped(v) {
      v = Math.max(0, Math.min(chars.length, Math.round(v)));
      if (v === n) return;
      if (n < 0 || v < n || v - n > 90) {
        for (let i = 0; i < chars.length; i++) chars[i].el.classList.toggle('on', i < v);
      } else {
        for (let i = n; i < v; i++) chars[i].el.classList.add('on');
      }
      const line = v < chars.length ? chars[v].line : lines.length - 1;
      if (line !== curLine) {
        lineEls.forEach((el, i) => el.classList.toggle('typing-line', i === line));
        curLine = line;
      }
      if (v < chars.length) chars[v].el.parentNode.insertBefore(caret, chars[v].el);
      else lineEls[lines.length - 1].appendChild(caret);
      n = v;
    }
    setTyped(0);
    return {
      el: box, area, caret, lines: lineEls, total: chars.length,
      setTyped, get typed() { return n; },
      blink(t) { caret.style.opacity = Math.floor(t * 2.6) % 2 ? 0.15 : 1; },
      highlight(li) { lineEls.forEach((el, i) => el.classList.toggle('hl-line', i === li)); }
    };
  }
  const sqlTextLen = (lines) => lines.map((l) => l.length).reduce((a, b) => a + b, 0);

  /* ---------- BUILDERS ---------- */
  const B = {};
  const built = [];

  /* ===== COLD OPEN ===== */
  B.coldopen = (el) => {
    el.innerHTML = '';
    const boot = h('div', 'boot');
    const bootLines = [
      '> khởi động học phần <b>DATABASE_FUNDAMENTALS</b>',
      '> kết nối kho dữ liệu <b>shop_db</b> ................ <span class="ok">OK</span>',
      '> nạp lược đồ: SANPHAM · KHACHHANG · HOADON ... <span class="ok">OK</span>',
      '> kiểm tra toàn vẹn khóa ngoại ................. <span class="ok">OK</span>',
      '> sẵn sàng. <b>render lecture...</b>'
    ];
    const boots = bootLines.map((t) => { const d = h('div', null, t); d.style.opacity = 0; boot.appendChild(d); return d; });

    const orbit = h('div', 'hero-orbit');
    orbit.innerHTML = `
      <svg viewBox="0 0 620 620" width="620" height="620" style="position:absolute;inset:0;overflow:visible">
        <defs>
          <linearGradient id="og" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#22d3ee" stop-opacity=".85"/><stop offset="1" stop-color="#3b82f6" stop-opacity=".1"/>
          </linearGradient>
          <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <g id="ringA" style="transform-origin:310px 310px">
          <ellipse cx="310" cy="310" rx="268" ry="120" fill="none" stroke="url(#og)" stroke-width="1.4" stroke-dasharray="3 10" opacity=".65"/>
        </g>
        <g id="ringB" style="transform-origin:310px 310px">
          <ellipse cx="310" cy="310" rx="198" ry="238" fill="none" stroke="url(#og)" stroke-width="1.1" stroke-dasharray="2 14" opacity=".5"/>
        </g>
        <g id="ringC" style="transform-origin:310px 310px">
          <ellipse cx="310" cy="310" rx="300" ry="300" fill="none" stroke="rgba(34,211,238,.16)" stroke-width="1"/>
          <ellipse cx="310" cy="310" rx="238" ry="238" fill="none" stroke="rgba(34,211,238,.1)" stroke-width="1"/>
        </g>
        <g opacity=".55">${Array.from({ length: 48 }).map((_, i) => { const a = (i / 48) * Math.PI * 2; const r = 300; const x = 310 + Math.cos(a) * r, y = 310 + Math.sin(a) * r; return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${i % 6 === 0 ? 2.4 : 1.1}" fill="#22d3ee" opacity="${i % 6 === 0 ? .9 : .35}"/>`; }).join('')}</g>
        <g id="sweep" filter="url(#glow)" opacity=".8">
          <path d="M310 310 L310 10 A300 300 0 0 1 470 42 Z" fill="rgba(34,211,238,.07)"/>
          <line x1="310" y1="310" x2="310" y2="10" stroke="rgba(103,232,249,.55)" stroke-width="1.2"/>
        </g>
        <circle cx="310" cy="310" r="190" fill="none" stroke="rgba(34,211,238,.18)" stroke-width="1" stroke-dasharray="1 6"/>
      </svg>`;

    const core = h('div', 'hero-core');
    core.innerHTML = `
      <div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 50% 45%, rgba(34,211,238,.28), transparent 68%);filter:blur(10px)"></div>
      <div class="cyl" style="left:50%;top:44%;transform:translate(-50%,-50%);width:150px;height:190px">
        <div class="cyl-top" style="width:150px;height:46px"></div>
        <div class="cyl-body" style="width:150px;height:146px;top:22px"></div>
        <div class="cyl-bot" style="width:150px;height:46px"></div>
        <div style="position:absolute;left:0;right:0;top:24px;bottom:24px;background:repeating-linear-gradient(180deg,transparent 0 15px,rgba(34,211,238,.18) 15px 16px)"></div>
      </div>
      <div class="hero-center" style="top:8px;bottom:auto;height:120px">
        <div class="big">DB</div>
        <div class="small">SQL · 2024</div>
      </div>`;
    orbit.appendChild(core);
    const packets = [];
    for (let i = 0; i < 10; i++) {
      const p = h('div', 'dbc-packet');
      p.style.width = p.style.height = (7 + (i % 3) * 3) + 'px';
      orbit.appendChild(p);
      packets.push(p);
    }

    const titleWrap = h('div', 'hero-title-wrap');
    titleWrap.innerHTML = `<div class="hero-kicker">BÀI GIẢNG · HỌC PHẦN CƠ SỞ DỮ LIỆU</div>
      <div class="hero-line" id="hl1"></div>
      <div class="hero-line grad" id="hl2"></div>
      <div class="hero-sub">Từ mô hình dữ liệu đến truy vấn SQL — hiểu để làm được.</div>`;

    const chips = h('div', 'hero-chips');
    [['01', 'Hiểu CSDL', 'db'], ['02', 'Thiết kế ERD', 'flow'], ['03', 'Viết SQL', 'code']].forEach(([i, t, ic]) => {
      chips.appendChild(h('div', 'hero-chip', `<span class="idx">${i}</span>${icon(ic)}<span>${t}</span>`));
    });
    el.append(boot, orbit, titleWrap, chips);

    const mk = (id, text) => {
      const el2 = document.getElementById(id);
      [...text].forEach((ch) => {
        const s = h('span', 'ch2', ch === ' ' ? '&nbsp;' : ch);
        el2.appendChild(s);
        s.style.transform = 'translateY(115%)';
      });
      return el2;
    };
    const l1 = mk('hl1', 'CƠ SỞ DỮ LIỆU');
    const l2 = mk('hl2', 'VÀ ỨNG DỤNG THỰC TẾ');
    const sub = titleWrap.querySelector('.hero-sub');
    const chipEls = [...chips.children];

    return {
      update(U) {
        const t = U.t;
        boots.forEach((d, i) => {
          const p = ease(clamp((U.p(0, 0.1 + i * 0.28, 0.3))));
          d.style.opacity = p * (i === boots.length - 1 ? (Math.floor(t * 3) % 2 ? 0.55 : 1) : 0.9);
          d.style.transform = `translateX(${(1 - p) * -14}px)`;
        });
        const rev1 = U.p(1, 0.15, 1.25);
        [...l1.children].forEach((s, i) => {
          const p = ease(clamp((rev1 * 12 - i) / 2.2));
          s.style.transform = `translateY(${(1 - p) * 115}%)`;
          s.style.opacity = clamp(p * 1.4);
        });
        const rev2 = U.p(1, 0.5, 1.25);
        l2.style.clipPath = `inset(${(1 - rev2) * 100}% 0 0 0)`;
        l2.style.transform = `translateY(${(1 - rev2) * 22}px)`;
        l2.style.opacity = rev2;
        [...l2.children].forEach((s) => { s.style.transform = 'none'; s.style.opacity = 1; });
        const ps = U.p(2, 0.05, 0.7);
        sub.style.opacity = ps * 0.95;
        sub.style.transform = `translateY(${(1 - ps) * 14}px)`;
        chipEls.forEach((c, i) => {
          const p = U.p(2, 0.35 + i * 0.22, 0.55);
          c.style.opacity = p;
          c.style.transform = `translateY(${(1 - p) * 16}px)`;
        });
        const rot = t * 4;
        const ra = docRing('ringA'), rb = docRing('ringB'), rc = docRing('ringC'), sw = docRing('sweep');
        if (ra) ra.style.transform = `rotate(${rot}deg)`;
        if (rb) rb.style.transform = `rotate(${-rot * 0.7}deg)`;
        if (rc) rc.style.transform = `rotate(${rot * 0.12}deg)`;
        if (sw) sw.style.transform = `rotate(${t * 42}deg)`;
        packets.forEach((p, i) => {
          const a = t * (0.55 + (i % 3) * 0.1) + i * 0.63;
          const rx = 300, ry = 300;
          const x = 310 + Math.cos(a) * rx;
          const y = 310 + Math.sin(a) * ry * 0.62;
          p.style.transform = `translate(${x - 5}px, ${y - 5}px) scale(${0.7 + Math.sin(a) * 0.3})`;
          p.style.opacity = 0.25 + 0.6 * Math.max(0, Math.sin(a * 1.3));
        });
      }
    };
    function docRing(id) { return el.querySelector('#' + id); }
  };

  /* ===== OBJECTIVES ===== */
  B.objectives = (el, def) => {
    el.innerHTML = head(def);
    const grid = h('div', 'obj-grid');
    const items = [
      ['Khái niệm CSDL', 'Dữ liệu, thông tin, DBMS và lý do dùng cơ sở dữ liệu.', 'db', '01'],
      ['Thành phần bảng', 'Table, row, column, khóa chính, khóa ngoại.', 'table', '02'],
      ['Ba loại quan hệ', '1-1, 1-N, N-N và bảng trung gian.', 'link', '03'],
      ['Thiết kế ERD', 'Từ yêu cầu thực tế đến mô hình dữ liệu.', 'flow', '04'],
      ['Ngôn ngữ SQL', 'DDL, DML, DQL, DCL, TCL và cú pháp cơ bản.', 'code', '05'],
      ['Truy vấn thực tế', 'Sáu bài toán trên dữ liệu cửa hàng điện thoại.', 'search', '06']
    ];
    const cards = items.map(([t, d, ic, n]) => {
      const c = h('div', 'card obj-card');
      c.innerHTML = `<div class="top"><span class="n">${n}</span>${icon(ic, 'icon ico')}</div><h3>${t}</h3><p>${d}</p>`;
      c.style.opacity = 0;
      grid.appendChild(c);
      return c;
    });
    const foot = h('div', 'obj-foot', `<span>7 phần</span><span class="sep"></span><span>6 bài truy vấn SQL</span><span class="sep"></span><span>Sơ đồ ERD đầy đủ</span><span class="sep"></span><span>5 câu ôn tập</span>`);
    el.append(grid, foot);
    return {
      update(U) {
        const groups = [[2, 0], [2, 2], [3, 4]];
        cards.forEach((c, i) => {
          const gi = i < 2 ? 0 : i < 4 ? 1 : 2;
          const cue = groups[gi][0], base = groups[gi][1];
          const p = U.p(cue, 0.1 + (i - base) * 0.22, 0.5);
          c.style.opacity = p;
          c.style.transform = `translateY(${(1 - p) * 22}px)`;
        });
        const pf = U.p(3, 0.25, 0.6);
        foot.style.opacity = pf;
        foot.style.transform = `translateY(${(1 - pf) * 12}px)`;
      }
    };
  };

  /* ===== DIVIDER ===== */
  B.divider = (el, def) => {
    const part = PARTS[def.part - 1];
    el.innerHTML = `
      <div class="div-wrap">
        <div class="div-num">${pad(part.n)}<span class="fill">${pad(part.n)}</span></div>
        <div class="div-body">
          <div class="div-eyebrow">PHẦN ${pad(part.n)} / 07</div>
          <div class="div-title">${def.title}</div>
          <div class="div-en">${part.en}</div>
          <div class="div-line"></div>
        </div>
        <div class="div-ticks">${PARTS.map((p) => `<span class="div-tick ${p.n === def.part ? 'on' : ''}">${pad(p.n)}</span>`).join('')}</div>
        <div class="div-watermark">DATABASE FUNDAMENTALS</div>
      </div>`;
    const num = el.querySelector('.div-num');
    const fillEl = el.querySelector('.fill');
    const line = el.querySelector('.div-line');
    const title = el.querySelector('.div-title');
    const nchar = def.title.length;
    title.style.fontSize = nchar > 34 ? '50px' : nchar > 27 ? '60px' : nchar > 22 ? '69px' : '78px';
    const eye = el.querySelector('.div-eyebrow');
    const en = el.querySelector('.div-en');
    return {
      update(U) {
        const p = U.p(0, 0.02, 0.9);
        const pf = U.p(0, 0.35, 1.0);
        num.style.opacity = p;
        num.style.transform = `translateX(${(1 - p) * -30}px)`;
        fillEl.style.clipPath = `inset(${100 - pf * 100}% 0 0 0)`;
        line.style.width = (U.p(0, 0.5, 0.9) * 520) + 'px';
        title.style.opacity = U.p(0, 0.15, 0.7);
        title.style.transform = `translateY(${(1 - U.p(0, 0.15, 0.7)) * 24}px)`;
        eye.style.opacity = U.p(0, 0.05, 0.5);
        en.style.opacity = U.p(0, 0.45, 0.6) * 0.8;
      }
    };
  };

  /* ===== DB CONCEPT ===== */
  B.dbconcept = (el, def) => {
    el.innerHTML = head(def);
    const left = h('div', 'dbc-left');
    const defText = `Cơ sở dữ liệu là một tập hợp <b>dữ liệu có cấu trúc</b>, được lưu trữ trên máy tính và quản lý để nhiều người có thể <b>truy cập, tìm kiếm và cập nhật</b> một cách hiệu quả.`;
    const p1 = h('div', 'dbc-def', defText.replace(/<b>/g, '<b class="w">').replace(/<\/b>/g, '</b>'));
    const quote = h('div', 'dbc-quote', 'Không phải một mớ dữ liệu hỗn độn — mà có cấu trúc, và các phần tử <span class="hl">có quan hệ</span> với nhau.');
    left.append(p1, quote);

    const exWrap = h('div', 'dbc-examples');
    const exs = [
      ['Danh sách sinh viên', 'table'],
      ['Hóa đơn bán hàng', 'receipt'],
      ['Lịch sử giao dịch', 'clock']
    ].map(([t, ic]) => {
      const d = h('div', 'dbc-ex', `${icon(ic)}<span>${t}</span>`);
      d.style.opacity = 0;
      exWrap.appendChild(d);
      return d;
    });

    const vis = h('div', 'dbc-visual');
    vis.innerHTML = `
      <svg viewBox="0 0 560 520" style="position:absolute;inset:0">
        <g id="rim1" style="transform-origin:280px 280px">
          <ellipse cx="280" cy="280" rx="230" ry="108" fill="none" stroke="rgba(34,211,238,.25)" stroke-width="1.2" stroke-dasharray="4 12"/>
        </g>
        <g id="rim2" style="transform-origin:280px 280px">
          <ellipse cx="280" cy="280" rx="170" ry="225" fill="none" stroke="rgba(59,130,246,.22)" stroke-width="1.2" stroke-dasharray="3 10"/>
        </g>
        <circle cx="280" cy="280" r="150" fill="radial-gradient"/>
        <circle cx="280" cy="280" r="148" fill="rgba(8,47,73,.18)" stroke="rgba(34,211,238,.12)"/>
      </svg>
      <div class="dbc-core">
        <div class="cyl">
          <div class="cyl-top"></div><div class="cyl-body"></div><div class="cyl-bot"></div>
        </div>
        <div class="dbc-label">SHOP_DB</div>
      </div>`;
    const packets = [];
    for (let i = 0; i < 8; i++) {
      const p = h('div', 'dbc-packet');
      p.style.width = p.style.height = (6 + (i % 3) * 3) + 'px';
      vis.appendChild(p);
      packets.push(p);
    }
    el.append(left, exWrap, vis);

    const words = [...p1.querySelectorAll('b.w')];
    const defEl = p1;
    const q = quote;
    return {
      update(U) {
        const pd = U.p(1, 0.05, 0.5);
        defEl.style.opacity = pd * 0.98;
        defEl.style.transform = `translateY(${(1 - pd) * 16}px)`;
        const pq = U.p(3, 0.1, 0.6);
        q.style.opacity = pq;
        q.style.transform = `translateY(${(1 - pq) * 12}px)`;
        exs.forEach((d, i) => {
          const p = U.p(2, 0.1 + i * 0.22, 0.5);
          d.style.opacity = p;
          d.style.transform = `translateY(${(1 - p) * 16}px)`;
        });
        const pv = U.p(1, 0, 1.1);
        vis.style.opacity = pv;
        vis.style.transform = `translateY(${(1 - pv) * 20}px) scale(${0.96 + pv * 0.04})`;
        const r1 = vis.querySelector('#rim1'), r2 = vis.querySelector('#rim2');
        if (r1) r1.style.transform = `rotate(${U.t * 18}deg)`;
        if (r2) r2.style.transform = `rotate(${-U.t * 12}deg)`;
        packets.forEach((p, i) => {
          const a = U.t * (0.5 + (i % 4) * 0.08) + i * 0.78;
          const rx = 210, ry = 150;
          const x = 280 + Math.cos(a) * rx;
          const y = 280 + Math.sin(a) * ry;
          p.style.transform = `translate(${x - 5}px, ${y - 5}px) scale(${0.65 + 0.35 * Math.sin(a)})`;
          p.style.opacity = 0.2 + 0.6 * Math.max(0, Math.sin(a));
        });
      }
    };
  };

  /* ===== DATA / INFO ===== */
  B.datainfo = (el, def) => {
    el.innerHTML = head(def);
    const cols = h('div', 'di-cols');
    const left = h('div', 'card di-col');
    left.innerHTML = `<div class="head"><div><h3>DỮ LIỆU</h3><div class="sub">Raw data — sự kiện thô</div></div><span class="badge" style="font-size:12px;padding:7px 12px">INPUT</span></div><div class="di-raw"></div>`;
    const raw = left.querySelector('.di-raw');
    const tokens = ['32.000.000', '05/03/2024', 'HD001', 'SP01', 'x2', 'KH01', 'NV01', '8.000.000', '12/03/2024', 'HD002'];
    const tokEls = tokens.map((t) => { const d = h('span', 'di-token', t); raw.appendChild(d); return d; });

    const mid = h('div', 'di-arrow');
    const op1 = h('div', 'di-op', 'SUM(SoLuong × DonGia)');
    const pipe = h('div', 'di-pipe', '<div class="flow"></div>');
    const op2 = h('div', 'di-op', 'GROUP BY tháng');
    mid.append(op1, pipe, op2);

    const right = h('div', 'card di-col');
    right.innerHTML = `<div class="head"><div><h3>THÔNG TIN</h3><div class="sub">Information — sau xử lý, có ngữ cảnh</div></div><span class="badge" style="font-size:12px;padding:7px 12px;border-color:rgba(52,211,153,.4);color:#6ee7b7;background:rgba(6,78,59,.3)">OUTPUT</span></div>
      <div class="di-info"><div class="lb">DOANH THU THÁNG 3 / 2024</div><div class="val">97.000.000 <span style="font-size:22px;color:#6ee7b7">đ</span></div><div class="note">↑ 18% so với tháng trước</div></div>
      <div class="di-insight">${icon('chart')}<span>Quyết định: nhập thêm iPhone và Galaxy S24 Ultra</span></div>`;
    cols.append(left, mid, right);
    const bottom = h('div', 'di-bottom', '<span>Dữ liệu là <b>nguyên liệu</b></span><span>→</span><span>Thông tin là <b>sản phẩm</b></span>');
    el.append(cols, bottom);

    const flow = pipe.querySelector('.flow');
    const info = right.querySelector('.di-info');
    const insight = right.querySelector('.di-insight');
    return {
      update(U) {
        tokEls.forEach((d, i) => {
          const p = U.p(0, 0.06 + i * 0.1, 0.4);
          d.style.opacity = p;
          d.style.transform = `translateY(${(1 - p) * 10}px)`;
        });
        const pa = U.p(1, 0.1, 0.5);
        op1.style.opacity = pa;
        op2.style.opacity = pa;
        flow.style.width = (U.p(1, 0.3, 0.75) * 100) + '%';
        const pi = U.p(1, 0.55, 0.6);
        info.style.opacity = pi;
        info.style.transform = `translateY(${(1 - pi) * 14}px)`;
        const pin = U.p(2, 0.1, 0.55);
        insight.style.opacity = pin;
        insight.style.transform = `translateX(${(1 - pin) * -10}px)`;
        const pb = U.p(2, 0.25, 0.6);
        bottom.style.opacity = pb;
        bottom.style.transform = `translateY(${(1 - pb) * 10}px)`;
      }
    };
  };

  /* ===== WHY DB ===== */
  B.whydb = (el, def) => {
    el.innerHTML = head(def);
    const grid = h('div', 'why-grid');
    const leftCol = h('div', 'why-col');
    leftCol.innerHTML = '<div class="why-col-head before">' + icon('alert') + 'Lưu file / sổ sách</div>';
    const rightCol = h('div', 'why-col');
    rightCol.innerHTML = '<div class="why-col-head after">' + icon('check') + 'Cơ sở dữ liệu</div>';
    const bads = [
      ['Dư thừa dữ liệu', 'Cùng một khách hàng bị nhập lại ở nhiều file.', 'layers'],
      ['Không nhất quán', 'File A giá cũ, file B giá mới — tin cái nào?', 'alert'],
      ['Tìm kiếm chậm', 'Dò thủ công hàng nghìn dòng mất hàng giờ.', 'search'],
      ['Không chia sẻ an toàn', 'Ai cũng mở được, ai cũng sửa được.', 'lock']
    ];
    const goods = [
      ['Giảm dư thừa', 'Chuẩn hóa: mỗi thông tin lưu một nơi.', 'layers'],
      ['Nhất quán', 'Ràng buộc & giao dịch ACID.', 'shield'],
      ['Truy vấn nhanh', 'Chỉ mục (index) và tối ưu truy vấn.', 'zap'],
      ['Phân quyền', 'Kiểm soát ai được đọc, ghi, sửa.', 'lock']
    ];
    const badEls = bads.map(([t, d, ic]) => {
      const x = h('div', 'why-item bad', `<div class="ico-box">${icon(ic)}</div><div><h4>${t}</h4><p>${d}</p></div>`);
      x.style.opacity = 0;
      leftCol.appendChild(x);
      return x;
    });
    const goodEls = goods.map(([t, d, ic]) => {
      const x = h('div', 'why-item good', `<div class="ico-box">${icon(ic)}</div><div><h4>${t}</h4><p>${d}</p></div>`);
      x.style.opacity = 0;
      rightCol.appendChild(x);
      return x;
    });
    const midCol = h('div', 'why-mid', '<div class="arrowdown"></div><div class="lbl">DBMS</div><div class="arrowdown"></div>');
    grid.append(leftCol, midCol, rightCol);
    const conc = h('div', 'why-concurrent', `<div class="users">${['A', 'B', 'C', 'D'].map((u) => `<div class="u">${u}</div>`).join('')}</div><p><b>Nhiều người dùng đồng thời</b> — khóa & giao dịch đảm bảo không ghi đè lên nhau.</p><div class="lib">CONCURRENCY</div>`);
    conc.style.opacity = 0;
    el.append(grid, conc);
    return {
      update(U) {
        badEls.forEach((x, i) => {
          const p = U.p(1, 0.05 + i * 0.18, 0.45);
          x.style.opacity = p;
          x.style.transform = `translateY(${(1 - p) * 16}px)`;
        });
        const pm = U.p(2, 0.0, 0.5);
        midCol.style.opacity = pm;
        goodEls.forEach((x, i) => {
          const p = U.p(2, 0.05 + i * 0.18, 0.45);
          x.style.opacity = p;
          x.style.transform = `translateY(${(1 - p) * 16}px)`;
        });
        const pc = U.p(3, 0.1, 0.55);
        conc.style.opacity = pc;
        conc.style.transform = `translateY(${(1 - pc) * 14}px)`;
      }
    };
  };

  /* ===== SHOP BEFORE / AFTER ===== */
  B.shop = (el, def) => {
    el.innerHTML = head(def);
    const split = h('div', 'shop-split');
    const before = h('div', 'shop-side before');
    before.innerHTML = `<div class="side-head">${icon('folder')} TRƯỚC KHI CÓ CSDL</div><div class="verdict">PHÂN MẢNH</div>`;
    const sheetsData = [
      ['Excel_KH.xlsx', 40, 70], ['Gia_2023.xlsx', 280, 110], ['HD_thang3.xlsx', 110, 230],
      ['Kho_copy(2).xlsx', 330, 270], ['Khach_trung.xlsx', 180, 380]
    ];
    const sheets = sheetsData.map(([name, x, y], i) => {
      const s = h('div', 'sheet', '<div class="bar m"></div><div class="bar"></div><div class="bar s"></div><div class="bar"></div><div class="tag">' + name + '</div>');
      s.style.left = x + 'px'; s.style.top = y + 'px';
      s.style.transform = `rotate(${(i % 2 ? -1 : 1) * (2 + i)}deg)`;
      s.style.opacity = 0;
      before.appendChild(s);
      return s;
    });
    const dupWarn = h('div', 'error-toast', icon('alert') + 'KH01 xuất hiện 3 lần · giá lệch');
    dupWarn.style.left = '150px'; dupWarn.style.top = '330px'; dupWarn.style.fontSize = '16px';
    dupWarn.style.opacity = 0;
    before.appendChild(dupWarn);

    const after = h('div', 'shop-side after');
    after.innerHTML = `<div class="side-head">${icon('db')} SAU KHI CÓ CSDL</div><div class="verdict">MỘT NGUỒN</div>`;
    const statsData = [
      ['SẢN PHẨM', '1.240', 'SKU'],
      ['KHÁCH HÀNG', '380', 'hồ sơ'],
      ['HÓA ĐƠN / NĂM', '5.680', 'giao dịch']
    ];
    const stats = statsData.map(([lb, v, u], i) => {
      const s = h('div', 'shop-stat', `<div class="lb">${lb}</div><div class="v">${v}<small>${u}</small></div>`);
      s.style.left = (26 + i * 262) + 'px'; s.style.top = '78px'; s.style.width = '240px';
      s.style.opacity = 0;
      after.appendChild(s);
      return s;
    });
    const dash = h('div', 'shop-dash');
    const small = dataTable(
      [{ label: 'MaHD' }, { label: 'Ngày' }, { label: 'Khách' }, { label: 'Tồn kho SP01' }],
      [['HD001', '05/03', 'Nguyễn Văn An', '120 → 119']]
    );
    small.table.style.fontSize = '17px';
    dash.appendChild(small.el);
    dash.style.opacity = 0;
    after.appendChild(dash);
    const live = h('div', null, `<div style="position:absolute;right:26px;bottom:26px;display:flex;align-items:center;gap:10px;font-family:'JBMono';font-size:12px;color:#6ee7b7;letter-spacing:.14em"><span style="width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 10px #34d399"></span>ĐÃ ĐỒNG BỘ</div>`);
    after.appendChild(live);

    const arrow = h('div', 'shop-arrow', icon('arrow'));
    split.append(before, arrow, after);
    const bottom = h('div', 'shop-bottom', '<span class="k">KẾT LUẬN</span><span>Một nguồn dữ liệu duy nhất — mọi nghiệp vụ cập nhật tức thời, nhất quán.</span>');
    el.append(split, arrow, bottom);

    return {
      update(U) {
        sheets.forEach((s, i) => {
          const p = U.p(1, 0.15 + i * 0.14, 0.5);
          s.style.opacity = p * 0.95;
          s.style.marginLeft = (1 - p) * -14 + 'px';
        });
        const pw = U.p(1, 0.55, 0.5);
        dupWarn.style.opacity = pw;
        dupWarn.style.transform = `translateY(${(1 - pw) * 10}px)`;
        const pa = U.p(2, 0.02, 0.6);
        arrow.style.opacity = pa;
        arrow.style.transform = `translate(-50%, -50%) rotate(${pa * 360}deg)`;
        stats.forEach((s, i) => {
          const p = U.p(2, 0.2 + i * 0.18, 0.5);
          s.style.opacity = p;
          s.style.transform = `translateY(${(1 - p) * 14}px)`;
        });
        const pd = U.p(2, 0.65, 0.5);
        dash.style.opacity = pd;
        dash.style.transform = `translateY(${(1 - pd) * 12}px)`;
        const cell = small.rows[0]?.cells[3];
        if (cell) cell.textContent = U.p(2, 0.9, 0.4) > 0.5 ? '119 ✓' : '120';
        const pb = U.p(3, 0.05, 0.55);
        bottom.style.opacity = pb;
        bottom.style.transform = `translateY(${(1 - pb) * 10}px)`;
      }
    };
  };

  /* ===== DBMS ===== */
  B.dbms = (el, def) => {
    el.innerHTML = head(def);
    const top = h('div', 'dbms-top');
    const appNode = h('div', 'card dbms-node', `<div style="display:flex;justify-content:center;margin-bottom:8px;color:#7dd3fc">${icon('server', 'icon')}</div><h4>Ứng dụng</h4><p>Web · Mobile · POS</p>`);
    const link1 = h('div', 'dbms-link');
    const core = h('div', 'dbms-core', `<div class="n">DBMS</div><div class="s">QUẢN TRỊ DỮ LIỆU</div>`);
    const link2 = h('div', 'dbms-link');
    const dbNode = h('div', 'card dbms-node', `<div style="display:flex;justify-content:center;margin-bottom:8px;color:#7dd3fc">${icon('db', 'icon')}</div><h4>Dữ liệu</h4><p>Bảng · Quan hệ · Chỉ mục</p>`);
    top.append(appNode, link1, core, link2, dbNode);

    const vendors = h('div', 'dbms-vendors');
    const vData = [
      ['MySQL', 'Mã nguồn mở, phổ biến cho web.', 'MY', '#0ea5e9'],
      ['SQL Server', 'Microsoft, mạnh về T-SQL.', 'MS', '#38bdf8'],
      ['PostgreSQL', 'Chuẩn mở, mở rộng mạnh.', 'PG', '#818cf8'],
      ['Oracle', 'Hệ thống lớn, tài chính.', 'OR', '#f87171']
    ];
    const vEls = vData.map(([n, d, l, c]) => {
      const v = h('div', 'card vendor', `<div class="logo" style="background:${c}1f;border:1px solid ${c}55;color:${c}">${l}</div><div><h4>${n}</h4><p>${d}</p></div>`);
      v.style.opacity = 0;
      vendors.appendChild(v);
      return v;
    });
    const services = h('div', 'dbms-services', [
      ['Bảo mật & phân quyền', 'shield'], ['Sao lưu & phục hồi', 'refresh'],
      ['Giao dịch đồng thời', 'users'], ['Tối ưu truy vấn', 'zap']
    ].map(([t, ic]) => `<div class="svc">${icon(ic)}<span>${t}</span></div>`).join(''));
    el.append(top, vendors, services);

    return {
      update(U) {
        const p1 = U.p(0, 0.1, 0.6);
        appNode.style.opacity = p1; appNode.style.transform = `translateX(${(1 - p1) * -16}px)`;
        dbNode.style.opacity = p1; dbNode.style.transform = `translateX(${(1 - p1) * 16}px)`;
        link1.style.opacity = U.p(0, 0.35, 0.4); link2.style.opacity = U.p(0, 0.35, 0.4);
        const pc = U.p(0, 0.25, 0.6);
        core.style.opacity = pc;
        core.style.transform = `scale(${0.9 + pc * 0.1})`;
        core.style.transformOrigin = 'center';
        const pulse = 0.5 + 0.5 * Math.sin(U.t * 2);
        core.style.boxShadow = `0 0 70px rgba(34,211,238,${0.12 + pulse * 0.12}), inset 0 0 60px rgba(34,211,238,.08)`;
        const pv = U.p(1, 0.05, 0.55);
        vEls.forEach((v, i) => {
          const p = U.p(1, 0.05 + i * 0.2, 0.5);
          v.style.opacity = p;
          v.style.transform = `translateY(${(1 - p) * 18}px)`;
        });
        const ps = U.p(3, 0.05, 0.55);
        services.style.opacity = ps;
        services.style.transform = `translateY(${(1 - ps) * 12}px)`;
      }
    };
  };

  /* ===== TABLE ANATOMY ===== */
  B.tableanatomy = (el, def) => {
    el.innerHTML = head(def);
    const layout = h('div', 'ta-layout');
    const tCard = h('div', 'card ta-table');
    tCard.innerHTML = '<div class="card-title" style="margin-bottom:14px"><span class="num">T</span> BẢNG SINHVIEN</div>';
    const dt = dataTable(
      [{ label: 'MaSV', cls: 'pk-col' }, { label: 'HoTen' }, { label: 'Lop' }, { label: 'Email' }],
      SV.map((r) => ({ cells: r, cls: '' }))
    );
    tCard.appendChild(dt.el);
    const count = h('div', 'ta-count', '<span><b>4</b> cột / trường</span><span><b>3</b> dòng / bản ghi</span><span class="mono" style="margin-left:auto;color:#5f7f99">table: SinhVien</span>');
    tCard.appendChild(count);

    const notes = h('div', 'ta-notes');
    const noteData = [
      ['Bảng', 'Table', 'Tập hợp dữ liệu cùng chủ đề — ở đây là toàn bộ sinh viên.', 'table'],
      ['Cột', 'Column / Field', 'Mỗi cột mô tả một thuộc tính: mã, tên, lớp, email.', 'layers'],
      ['Dòng', 'Row / Record', 'Mỗi dòng là một sinh viên cụ thể với đầy đủ giá trị.', 'user']
    ];
    const noteEls = noteData.map(([vi, en, d, ic]) => {
      const n = h('div', 'card ta-note', `<h4>${icon(ic)}${vi}<span class="en">${en}</span></h4><p>${d}</p>`);
      n.style.opacity = 0;
      notes.appendChild(n);
      return n;
    });
    layout.append(tCard, notes);
    el.appendChild(layout);

    const ths = [...dt.table.querySelectorAll('th')];
    const trs = dt.rows;
    return {
      update(U) {
        const pt = U.p(0, 0.05, 0.6);
        tCard.style.opacity = pt;
        tCard.style.transform = `translateY(${(1 - pt) * 16}px)`;
        // cột
        ths.forEach((th, i) => {
          const p = U.p(1, 0.08 + i * 0.22, 0.45);
          th.style.background = `rgba(34,211,238,${0.08 + p * 0.18})`;
          th.style.color = p > 0.3 ? '#c9f2ff' : '';
          [...dt.rows].forEach((tr) => {
            const td = tr.cells[i];
            if (td) {
              td.style.boxShadow = `inset 0 2px 0 rgba(34,211,238,${p * 0.75}), inset 0 -2px 0 rgba(34,211,238,${p * 0.45})`;
              td.style.background = `rgba(34,211,238,${p * 0.07})`;
            }
          });
        });
        // dòng
        trs.forEach((tr, i) => {
          const p = U.p(2, 0.05 + i * 0.3, 0.45);
          tr.style.background = `rgba(34,211,238,${p * 0.14})`;
          tr.style.boxShadow = p > 0.03 ? `inset 2px 0 0 rgba(34,211,238,${p})` : 'none';
        });
        noteEls.forEach((n, i) => {
          const p = U.p(i + 1, 0.15, 0.5);
          n.style.opacity = p;
          n.style.transform = `translateX(${(1 - p) * 18}px)`;
        });
        const pc = U.p(3, 0.05, 0.5);
        count.style.opacity = 0.4 + pc * 0.6;
      }
    };
  };

  /* ===== PRIMARY KEY ===== */
  B.primarykey = (el, def) => {
    el.innerHTML = head(def);
    const layout = h('div', 'ta-layout');
    const left = h('div', 'card ta-table');
    left.innerHTML = '<div class="card-title" style="margin-bottom:14px"><span class="num" style="background:#fbbf24;color:#2b1c00">PK</span> KHÓA CHÍNH = MaSV</div>';
    const dt = dataTable(
      [{ label: 'MaSV', cls: 'pk-col', tag: 'pk' }, { label: 'HoTen' }, { label: 'Lop' }, { label: 'Email' }],
      SV.map((r) => ({ cells: r }))
    );
    left.appendChild(dt.el);
    const badge = h('div', 'pk-badge', icon('key') + '<span>Mỗi sinh viên có <b style="color:#fff">một mã duy nhất</b></span>');
    badge.style.position = 'relative'; badge.style.left = '0'; badge.style.transform = 'none';
    badge.style.marginTop = '22px'; badge.style.justifyContent = 'center';
    left.appendChild(badge);

    const right = h('div', 'ta-notes');
    const rules = [
      ['DUY NHẤT', 'Không có hai dòng cùng khóa chính.'],
      ['KHÔNG TRỐNG', 'Không được để NULL — mỗi bản ghi phải định danh được.'],
      ['KHÔNG ĐỔI', 'Giá trị khóa ổn định suốt vòng đời bản ghi.']
    ];
    const ruleEls = rules.map(([t, d]) => {
      const r = h('div', 'pk-rule', `<span style="font-family:'JBMono';font-size:12px;color:#fbbf24;letter-spacing:.1em">${t}</span><span style="color:#cbd5e1;font-size:16px">${d}</span>`);
      r.style.position = 'relative';
      r.style.opacity = 0;
      right.appendChild(r);
      return r;
    });
    const tryCard = h('div', 'card', `<div class="card-title" style="color:#fca5a5"><span class="num" style="background:#f87171;color:#2b0000">!</span> THỬ NHẬP TRÙNG</div>
      <div style="font-family:'JBMono';font-size:16px;line-height:1.7;color:#fecaca;margin-top:10px">INSERT INTO SinhVien<br>VALUES (<span style="color:#fca5a5">'SV002'</span>, N'Nguyễn Văn An', ...);</div>`);
    tryCard.style.padding = '18px 20px';
    tryCard.style.opacity = 0;
    const toast = h('div', 'error-toast', icon('alert') + 'Vi phạm khóa chính: trùng MaSV');
    toast.style.position = 'relative';
    toast.style.marginTop = '10px';
    toast.style.opacity = 0;
    tryCard.append(toast);
    right.appendChild(tryCard);
    layout.append(left, right);
    el.appendChild(layout);

    return {
      update(U) {
        const pl = U.p(0, 0.05, 0.6);
        left.style.opacity = pl;
        left.style.transform = `translateY(${(1 - pl) * 16}px)`;
        const pk = U.p(0, 0.1, 0.6);
        [...dt.table.querySelectorAll('th')][0].style.background = `rgba(251,191,36,${0.1 + pk * 0.18})`;
        dt.rows.forEach((tr) => {
          const td = tr.cells[0];
          td.style.color = '#fbbf24';
          td.style.fontWeight = '600';
          td.style.background = `rgba(251,191,36,${0.06 + pk * 0.1})`;
          td.style.boxShadow = `inset 3px 0 0 rgba(251,191,36,${pk * 0.9})`;
        });
        badge.style.opacity = U.p(3, 0.1, 0.5);
        ruleEls.forEach((r, i) => {
          const p = U.p(1, 0.1 + i * 0.22, 0.45);
          r.style.opacity = p;
          r.style.transform = `translateY(${(1 - p) * 10}px)`;
        });
        const pt = U.p(2, 0.1, 0.5);
        tryCard.style.opacity = pt;
        tryCard.style.transform = `translateY(${(1 - pt) * 12}px)`;
        const pe = U.p(2, 0.45, 0.35);
        toast.style.opacity = pe;
        toast.style.transform = `translateX(${Math.sin(U.t * 38) * (1 - pe) * 6}px)`;
      }
    };
  };

  /* ===== FOREIGN KEY ===== */
  B.foreignkey = (el, def) => {
    el.innerHTML = head(def);
    const stage = h('div', 'fk-wrap');
    stage.innerHTML = `<svg class="fk-svg" viewBox="0 0 1712 620" width="1712" height="620"></svg>`;
    const svg = stage.querySelector('svg');
    const lop = h('div', 'card fk-table fk-lop');
    lop.innerHTML = '<div class="card-title" style="padding:18px 20px 0"><span class="num">1</span> BẢNG LOP</div>';
    const d1 = dataTable([{ label: 'MaLop', tag: 'pk' }, { label: 'TenLop' }, { label: 'Khoa' }],
      [['DA22TTC', 'CNTT CLC 2022', 'CNTT'], ['DA22TTD', 'CNTT 2022', 'CNTT']]);
    d1.el.style.border = 'none'; d1.el.style.borderRadius = '0';
    lop.appendChild(d1.el);
    lop.style.width = '470px'; lop.style.left = '110px'; lop.style.top = '50px';

    const sv = h('div', 'card fk-table fk-sv');
    sv.innerHTML = '<div class="card-title" style="padding:18px 20px 0"><span class="num">2</span> BẢNG SINHVIEN</div>';
    const d2 = dataTable([{ label: 'MaSV', tag: 'pk' }, { label: 'HoTen' }, { label: 'MaLop', tag: 'fk' }, { label: 'Email' }],
      SV.map((r) => ({ cells: r })));
    d2.el.style.border = 'none'; d2.el.style.borderRadius = '0';
    sv.appendChild(d2.el);
    sv.style.width = '580px'; sv.style.right = '60px'; sv.style.top = '50px';

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M 590 132 H 700 V 220 H 1072');
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', '#38bdf8');
    path.setAttribute('stroke-width', '2.4');
    path.setAttribute('pathLength', '100');
    path.setAttribute('stroke-dasharray', '100');
    path.setAttribute('stroke-dashoffset', '100');
    path.style.filter = 'drop-shadow(0 0 6px rgba(56,189,248,.7))';
    svg.appendChild(path);
    const foot = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    foot.setAttribute('d', 'M 1072 220 l -14 -9 M 1072 220 l -14 9 M 1072 220 l -14 0');
    foot.setAttribute('stroke', '#38bdf8'); foot.setAttribute('stroke-width', '2.2'); foot.setAttribute('fill', 'none');
    foot.setAttribute('pathLength', '100'); foot.setAttribute('stroke-dasharray', '100'); foot.setAttribute('stroke-dashoffset', '100');
    svg.appendChild(foot);

    const lab1 = h('div', 'fk-tag', '1');
    lab1.style.left = '606px'; lab1.style.top = '104px';
    const labN = h('div', 'fk-tag', 'N');
    labN.style.left = '1014px'; labN.style.top = '192px';
    labN.style.color = '#38bdf8'; labN.style.background = 'rgba(8,47,73,.8)'; labN.style.borderColor = 'rgba(56,189,248,.45)';
    const fkNote = h('div', 'fk-note', `<div class="pin" style="background:#38bdf8"></div><span><b style="color:#a5f3fc">MaLop</b> trong SINHVIEN tham chiếu <b style="color:#fbbf24">MaLop</b> trong LOP.</span>`);
    const badCard = h('div', 'insert-try', `INSERT INTO SinhVien<br>VALUES ('SV004', N'Phạm Thu Hà', <span style="color:#f87171">'DA99'</span>, 'ha@gmail.com');`);
    badCard.style.position = 'absolute'; badCard.style.left = '560px'; badCard.style.top = '330px'; badCard.style.width = '620px';
    const toast = h('div', 'error-toast', icon('alert') + 'Không tồn tại lớp DA99 — từ chối');
    toast.style.position = 'relative'; toast.style.marginTop = '10px'; toast.style.opacity = 0; toast.style.fontSize = '17px';
    const noteOk = h('div', 'card', `<div style="display:flex;gap:12px;align-items:center;font-size:17px;color:#a7f3d0">${icon('shield')}<span>Ràng buộc <b>toàn vẹn tham chiếu</b>: khóa ngoại phải trỏ tới một khóa chính tồn tại.</span></div>`);
    noteOk.style.position = 'absolute'; noteOk.style.left = '560px'; noteOk.style.top = '470px'; noteOk.style.width = '620px'; noteOk.style.padding = '16px 20px';
    noteOk.style.opacity = 0;

    stage.append(lop, sv, lab1, labN, badCard, toast, noteOk);
    el.append(stage, fkNote);
    return {
      update(U) {
        const p1 = U.p(0, 0.05, 0.55);
        lop.style.opacity = p1;
        lop.style.transform = `translateY(${(1 - p1) * 14}px)`;
        sv.style.opacity = U.p(0, 0.25, 0.55);
        sv.style.transform = `translateY(${(1 - U.p(0, 0.25, 0.55)) * 14}px)`;
        const pl = U.p(1, 0.05, 0.7);
        path.setAttribute('stroke-dashoffset', 100 * (1 - pl));
        foot.setAttribute('stroke-dashoffset', 100 * (1 - U.p(1, 0.4, 0.4)));
        lab1.style.opacity = U.p(1, 0.15, 0.4);
        labN.style.opacity = U.p(1, 0.35, 0.4);
        const fk = U.p(1, 0.1, 0.5);
        d2.rows.forEach((tr) => {
          const td = tr.cells[2];
          td.style.color = '#38bdf8';
          td.style.background = `rgba(56,189,248,${0.05 + fk * 0.1})`;
          td.style.boxShadow = `inset 0 0 0 1px rgba(56,189,248,${fk * 0.4})`;
        });
        const th0 = [...d1.table.querySelectorAll('th')][0];
        th0.style.background = `rgba(251,191,36,${0.1 + fk * 0.15})`;
        th0.style.color = '#fbbf24';
        const pb = U.p(2, 0.15, 0.5);
        badCard.style.opacity = pb;
        badCard.style.transform = `translateY(${(1 - pb) * 12}px)`;
        const pe = U.p(2, 0.5, 0.35);
        toast.style.opacity = pe;
        toast.style.transform = `translateX(${Math.sin(U.t * 40) * (1 - pe) * 6}px)`;
        const pn = U.p(3, 0.1, 0.55);
        noteOk.style.opacity = pn;
        noteOk.style.transform = `translateY(${(1 - pn) * 12}px)`;
        fkNote.style.opacity = U.p(3, 0.05, 0.5);
      }
    };
  };

  /* ===== 1-1 ===== */
  B.rel11 = (el, def) => {
    el.innerHTML = head(def);
    const stage = h('div', 'rel-stage');
    stage.innerHTML = `<svg class="sum-lines" viewBox="0 0 1712 600" width="1712" height="600" style="position:absolute;inset:0">
      <path d="M 640 250 H 1072" stroke="#22d3ee" stroke-width="2" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" id="l11" opacity=".8"/>
      <circle cx="640" cy="250" r="4" fill="#22d3ee"/><circle cx="1072" cy="250" r="4" fill="#22d3ee"/>
    </svg>`;
    const a = h('div', 'card rel-card');
    a.style.cssText = 'left:170px;top:150px;width:470px';
    a.innerHTML = `<h4>${icon('user')} SINHVIEN</h4><div class="cols"><div><span class="k">MaSV</span> · PK</div><div>HoTen</div><div>Lop</div><div>Email</div></div>`;
    const b = h('div', 'card rel-card');
    b.style.cssText = 'right:170px;top:150px;width:470px';
    b.innerHTML = `<h4>${icon('file')} HOSO</h4><div class="cols"><div><span class="f">MaSV</span> · FK · UNIQUE</div><div>NgaySinh</div><div>DiaChi</div><div>AnhCaNhan</div></div>`;
    const l1 = h('div', 'rel-label', '1');
    l1.style.left = '652px'; l1.style.top = '200px';
    const r1 = h('div', 'rel-label', '1');
    r1.style.left = '1016px'; r1.style.top = '200px';
    const note = h('div', 'rel-note', `<div class="pin"></div><span>Mỗi sinh viên có đúng <b class="hl">một hồ sơ</b>; mỗi hồ sơ thuộc về đúng <b class="hl">một sinh viên</b>. Khóa ngoại đặt ở HOSO kèm ràng buộc UNIQUE.</span>`);
    const use = h('div', 'card', `<div style="display:flex;gap:14px;align-items:center"><div style="color:#a78bfa">${icon('lock')}</div><div><div style="font-size:17px;font-weight:600;color:#e9d5ff">Thông tin ít dùng hoặc nhạy cảm</div><div style="font-size:14px;color:#8fb0cc;margin-top:2px">Tách sang bảng riêng: dễ phân quyền, gọn bảng chính.</div></div></div>`);
    use.style.cssText = 'position:absolute;left:170px;right:170px;bottom:120px;padding:16px 20px;opacity:0';
    stage.append(a, b, l1, r1, note, use);
    el.appendChild(stage);
    const path = stage.querySelector('#l11');
    const L = path.getTotalLength();
    path.setAttribute('stroke-dasharray', L);
    path.setAttribute('stroke-dashoffset', L);
    return {
      update(U) {
        const p = U.p(0, 0.1, 0.6);
        a.style.opacity = p; a.style.transform = `translateY(${(1 - p) * 16}px)`;
        b.style.opacity = U.p(0, 0.3, 0.6); b.style.transform = `translateY(${(1 - U.p(0, 0.3, 0.6)) * 16}px)`;
        const pl = U.p(0, 0.55, 0.5);
        path.setAttribute('stroke-dashoffset', L * (1 - pl));
        l1.style.opacity = pl; r1.style.opacity = pl;
        const pu = U.p(1, 0.05, 0.5);
        const fkRow = b.querySelector('.cols .f');
        if (fkRow) {
          fkRow.style.background = `rgba(56,189,248,${0.08 + pu * 0.14})`;
          fkRow.style.padding = '2px 6px';
          fkRow.style.borderRadius = '4px';
        }
        use.style.opacity = U.p(2, 0.1, 0.55);
        use.style.transform = `translateY(${(1 - U.p(2, 0.1, 0.55)) * 12}px)`;
        note.style.opacity = U.p(2, 0.0, 0.5);
      }
    };
  };

  /* ===== 1-N ===== */
  B.rel1n = (el, def) => {
    el.innerHTML = head(def);
    const stage = h('div', 'rel-stage');
    stage.innerHTML = `<svg viewBox="0 0 1712 600" width="1712" height="600" style="position:absolute;inset:0">
      <path d="M 600 250 H 962" stroke="#22d3ee" stroke-width="2" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" id="l1n"/>
      <path d="M 962 250 l -20 -12 M 962 250 l -20 12 M 962 250 l -20 0" stroke="#22d3ee" stroke-width="2" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" id="foot1n"/>
    </svg>`;
    const a = h('div', 'card rel-card');
    a.style.cssText = 'left:170px;top:120px;width:420px';
    a.innerHTML = `<h4>${icon('layers')} LOP</h4><div class="cols"><div><span class="k">MaLop</span> · PK</div><div>TenLop</div><div>Khoa</div></div>`;
    const b = h('div', 'card rel-card');
    b.style.cssText = 'right:150px;top:60px;width:600px';
    b.innerHTML = `<h4>${icon('users')} SINHVIEN</h4>
      <div class="table-wrap" style="margin-top:10px"><table class="dt" style="font-size:16px">
      <thead><tr><th>MaSV</th><th>HoTen</th><th style="color:#38bdf8">MaLop</th></tr></thead>
      <tbody>${[['SV001', 'Nguyễn Văn An'], ['SV002', 'Trần Thị Bình'], ['SV003', 'Lê Văn Nam'], ['SV004', 'Phạm Thu Hà']].map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td><td style="color:#38bdf8">DA22TTC</td></tr>`).join('')}</tbody>
      </table></div>`;
    const l1 = h('div', 'rel-label', '1');
    l1.style.left = '600px'; l1.style.top = '200px';
    const lN = h('div', 'rel-label', 'N');
    lN.style.left = '912px'; lN.style.top = '200px';
    const note = h('div', 'rel-note', `<div class="pin"></div><span>Khóa ngoại nằm ở phía <b class="hl">nhiều</b> — cột <b class="mono" style="color:#38bdf8">MaLop</b> trong bảng SINHVIEN.</span>`);
    const ex = h('div', null, ['Khách hàng → Hóa đơn', 'Danh mục → Sản phẩm', 'Nhân viên → Hợp đồng'].map((t) => `<span class="chip" style="font-size:15px">${t}</span>`).join(''));
    ex.style.cssText = 'position:absolute;left:170px;bottom:120px;display:flex;gap:10px;opacity:0';
    stage.append(a, b, l1, lN, note, ex);
    el.appendChild(stage);
    const p1 = stage.querySelector('#l1n'), pf = stage.querySelector('#foot1n');
    const L1 = p1.getTotalLength(), LF = pf.getTotalLength();
    p1.setAttribute('stroke-dasharray', L1); p1.setAttribute('stroke-dashoffset', L1);
    pf.setAttribute('stroke-dasharray', LF); pf.setAttribute('stroke-dashoffset', LF);
    return {
      update(U) {
        const pa = U.p(0, 0.1, 0.55);
        a.style.opacity = pa; a.style.transform = `translateY(${(1 - pa) * 16}px)`;
        b.style.opacity = U.p(0, 0.3, 0.55); b.style.transform = `translateY(${(1 - U.p(0, 0.3, 0.55)) * 16}px)`;
        const pl = U.p(0, 0.55, 0.5);
        p1.setAttribute('stroke-dashoffset', L1 * (1 - pl));
        pf.setAttribute('stroke-dashoffset', LF * (1 - U.p(0, 0.8, 0.3)));
        l1.style.opacity = pl; lN.style.opacity = pl;
        const pd = U.p(1, 0.05, 0.5);
        b.querySelectorAll('tbody tr td:nth-child(3)').forEach((td) => {
          td.style.background = `rgba(56,189,248,${0.06 + pd * 0.14})`;
          td.style.boxShadow = `inset 0 0 0 1px rgba(56,189,248,${pd * 0.4})`;
          td.style.color = '#7dd3fc';
        });
        const pe = U.p(2, 0.05, 0.55);
        ex.style.opacity = pe;
        ex.style.transform = `translateY(${(1 - pe) * 10}px)`;
        note.style.opacity = U.p(2, 0.0, 0.5);
      }
    };
  };

  /* ===== N-N ===== */
  B.relnn = (el, def) => {
    el.innerHTML = head(def);
    const stage = h('div', 'rel-stage nn-stage');
    stage.style.height = '470px';
    const svg = h('div', 'nn-split');
    svg.innerHTML = `<svg viewBox="0 0 1712 470" width="1712" height="470" style="position:absolute;inset:0">
      <path d="M 400 104 V 140 H 496 V 186" stroke="#22d3ee" stroke-width="2" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" id="nn1"/>
      <path d="M 1312 104 V 140 H 1216 V 186" stroke="#22d3ee" stroke-width="2" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" id="nn2"/>
    </svg>`;
    const sv = h('div', 'card rel-card');
    sv.style.cssText = 'left:120px;top:0;width:560px';
    sv.innerHTML = `<h4>${icon('user')} SINHVIEN</h4><div class="cols"><span class="k">MaSV</span> · PK · HoTen</div>`;
    const mh = h('div', 'card rel-card');
    mh.style.cssText = 'right:120px;top:0;width:560px';
    mh.innerHTML = `<h4>${icon('box')} MONHOC</h4><div class="cols"><span class="k">MaMH</span> · PK · TenMH · SoTinChi</div>`;
    const jk = h('div', 'nn-junction card');
    jk.style.top = '186px';
    jk.style.width = '720px';
    jk.innerHTML = `<div class="jt"><div class="card-title" style="font-size:13px"><span class="num">J</span> BẢNG TRUNG GIAN: DANGKY</div><div style="font-family:'JBMono';font-size:10px;color:#67e8f9">JUNCTION</div></div>
      <div class="table-wrap"><table class="dt dense" style="font-size:16px">
      <thead><tr><th><span style="color:#fbbf24">MaSV</span> · PK</th><th><span style="color:#fbbf24">MaMH</span> · PK</th><th>HocKy</th><th>Diem</th></tr></thead>
      <tbody>${[['SV001', 'CSDL', 'HK1', '8.5'], ['SV001', 'MMT', 'HK1', '7.8'], ['SV002', 'CSDL', 'HK1', '9.0'], ['SV003', 'CSDL', 'HK1', '7.2']].map((r) => `<tr><td style="color:#fbbf24">${r[0]}</td><td style="color:#fbbf24">${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join('')}</tbody>
      </table></div>`;
    const nnBadge = h('div', 'rel-label', 'N');
    nnBadge.style.left = '486px'; nnBadge.style.top = '152px';
    const nnBadge2 = h('div', 'rel-label', 'N');
    nnBadge2.style.left = '1182px'; nnBadge2.style.top = '152px';
    const note = h('div', 'nn-note', `<div class="pin"></div><span>Không thể đặt khóa ngoại trực tiếp: mỗi ô chỉ chứa <b class="hl">một giá trị</b>. Bảng DANGKY tách N-N thành <b class="hl">hai quan hệ 1-N</b>.</span>`);
    const result = h('div', 'nn-result', '<span class="pill">SINHVIEN <b>1 : N</b> DANGKY</span><span class="plus">+</span><span class="pill">MONHOC <b>1 : N</b> DANGKY</span>');
    stage.append(svg, sv, mh, jk, nnBadge, nnBadge2);
    el.append(stage, note, result);
    const paths = ['nn1', 'nn2'].map((id) => { const p = stage.querySelector('#' + id); const L = p.getTotalLength(); p.setAttribute('stroke-dasharray', L); p.setAttribute('stroke-dashoffset', L); return p; });
    return {
      update(U) {
        const ps = U.p(0, 0.05, 0.55);
        sv.style.opacity = ps; sv.style.transform = `translateY(${(1 - ps) * 14}px)`;
        mh.style.opacity = ps; mh.style.transform = `translateY(${(1 - ps) * 14}px)`;
        nnBadge.style.opacity = U.p(0, 0.5, 0.5); nnBadge2.style.opacity = U.p(0, 0.5, 0.5);
        const pj = U.p(1, 0.1, 0.6);
        jk.style.opacity = pj;
        jk.style.transform = `translateX(-50%) translateY(${(1 - pj) * 18}px)`;
        const d1 = U.p(1, 0.3, 0.5);
        paths.forEach((p) => p.setAttribute('stroke-dashoffset', p.getTotalLength() * (1 - d1)));
        const pcomp = U.p(2, 0.05, 0.5);
        jk.querySelectorAll('tbody td:nth-child(1), tbody td:nth-child(2)').forEach((td) => {
          td.style.background = `rgba(251,191,36,${0.05 + pcomp * 0.12})`;
          td.style.fontWeight = '600';
        });
        jk.querySelectorAll('thead th:nth-child(1), thead th:nth-child(2)').forEach((th) => {
          th.style.background = `rgba(251,191,36,${0.07 + pcomp * 0.13})`;
        });
        const p4 = U.p(3, 0.05, 0.5);
        note.style.opacity = p4;
        note.style.transform = `translateY(${(1 - p4) * 10}px)`;
        const p5 = U.p(3, 0.3, 0.5);
        result.style.opacity = p5;
        result.style.transform = `translateY(${(1 - p5) * 10}px)`;
      }
    };
  };

  /* ===== ERD CONCEPTS ===== */
  B.erdconcepts = (el, def) => {
    el.innerHTML = head(def);
    const left = h('div', 'erd-concepts-left');
    left.innerHTML = `
      <svg viewBox="0 0 780 540" width="780" height="540" style="position:absolute;inset:0">
        <g id="ec-entity">
          <rect x="250" y="210" width="220" height="90" rx="4" fill="rgba(14,116,144,.22)" stroke="#22d3ee" stroke-width="1.8"/>
          <text x="360" y="252" text-anchor="middle" fill="#eafaff" font-family="BeVietnam" font-weight="700" font-size="21">KHACHHANG</text>
          <text x="360" y="278" text-anchor="middle" fill="#67e8f9" font-family="JBMono" font-size="11" letter-spacing="2">THỰC THỂ</text>
        </g>
        <g id="ec-attrs" opacity="0">
          <ellipse cx="140" cy="96" rx="96" ry="34" fill="rgba(30,64,175,.16)" stroke="#60a5fa" stroke-width="1.4"/>
          <text x="140" y="101" text-anchor="middle" fill="#bfdbfe" font-family="JBMono" font-size="13">HoTen</text>
          <ellipse cx="360" cy="86" rx="86" ry="32" fill="rgba(30,64,175,.16)" stroke="#60a5fa" stroke-width="1.4"/>
          <text x="360" y="91" text-anchor="middle" fill="#bfdbfe" font-family="JBMono" font-size="13">SDT</text>
          <ellipse cx="596" cy="96" rx="96" ry="34" fill="rgba(30,64,175,.16)" stroke="#60a5fa" stroke-width="1.4"/>
          <text x="596" y="101" text-anchor="middle" fill="#bfdbfe" font-family="JBMono" font-size="13">DiaChi</text>
          <line x1="200" y1="122" x2="262" y2="210" stroke="#3b82f6" stroke-width="1.2"/>
          <line x1="360" y1="118" x2="360" y2="210" stroke="#3b82f6" stroke-width="1.2"/>
          <line x1="530" y1="124" x2="458" y2="210" stroke="#3b82f6" stroke-width="1.2"/>
        </g>
        <g id="ec-rel" opacity="0">
          <path d="M 470 255 H 590" stroke="#22d3ee" stroke-width="1.6" stroke-dasharray="4 5"/>
          <polygon points="640,255 690,220 740,255 690,290" fill="rgba(139,92,246,.2)" stroke="#a78bfa" stroke-width="1.6"/>
          <text x="690" y="259" text-anchor="middle" fill="#ddd6fe" font-family="BeVietnam" font-weight="600" font-size="15">MUA</text>
          <text x="690" y="320" text-anchor="middle" fill="#a78bfa" font-family="JBMono" font-size="11" letter-spacing="1">MỐI QUAN HỆ</text>
        </g>
        <g id="ec-note" opacity="0">
          <text x="140" y="458" fill="#8fb0cc" font-family="BeVietnam" font-size="16">Hình chữ nhật · hình elip · hình thoi</text>
        </g>
      </svg>`;
    const stack = h('div', 'erd-map');
    const maps = [
      ['Thực thể', 'Entity', 'Bảng (Table)', 'db'],
      ['Thuộc tính', 'Attribute', 'Cột (Column)', 'layers'],
      ['Mối quan hệ', 'Relationship', 'Khóa ngoại (FK)', 'link']
    ];
    const mapEls = maps.map(([l, en, r, ic]) => {
      const row = h('div', 'erd-map-row', `<div style="color:#67e8f9">${icon(ic)}</div><div class="l">${l}<span style="font-family:'JBMono';font-size:11px;color:#5f7f99;margin-left:8px">${en}</span></div><span class="arrow">→</span><div class="r">${r}</div>`);
      row.style.opacity = 0;
      stack.appendChild(row);
      return row;
    });
    const note = h('div', 'erd-note', '<b style="color:#a5f3fc">Ký pháp Chen:</b> thực thể = hình chữ nhật, thuộc tính = hình elip, quan hệ = hình thoi. Sơ đồ thực tế thường dùng dạng bảng gọn hơn — ý nghĩa không đổi.');
    stack.appendChild(note);
    left.appendChild(stack);
    // di chuyển stack sang cột phải
    left.removeChild(stack);
    el.append(left, stack);
    stack.style.position = 'absolute';
    stack.style.right = '104px';
    stack.style.top = '210px';
    stack.style.width = '820px';

    const ent = left.querySelector('#ec-entity'), attrs = left.querySelector('#ec-attrs'), rel = left.querySelector('#ec-rel'), nt = left.querySelector('#ec-note');
    const bbox = (g) => { const b = g.getBBox(); return b; };
    return {
      update(U) {
        const p0 = U.p(0, 0.05, 0.6);
        ent.style.opacity = p0;
        ent.style.transform = `translate(${(1 - p0) * -20}px, 0)`;
        ent.style.transformOrigin = '360px 255px';
        const p1 = U.p(1, 0.05, 0.6);
        attrs.style.opacity = p1;
        const p2 = U.p(1, 0.45, 0.55);
        rel.style.opacity = p2;
        nt.style.opacity = U.p(1, 0.7, 0.5);
        mapEls.forEach((r, i) => {
          const p = U.p(2, 0.1 + i * 0.25, 0.45);
          r.style.opacity = p;
          r.style.transform = `translateX(${(1 - p) * 16}px)`;
        });
        note.style.opacity = U.p(3, 0.05, 0.55);
        note.style.transform = `translateY(${(1 - U.p(3, 0.05, 0.55)) * 10}px)`;
      }
    };
  };

  /* ===== ERD ANALYSIS ===== */
  B.erdanalysis = (el, def) => {
    el.innerHTML = head(def);
    const wrap = h('div', 'erd-analysis');
    const req = h('div', 'card erd-req');
    req.innerHTML = `<div class="card-title"><span class="num">?</span> YÊU CẦU BÀI TOÁN</div>
      <div class="brief">Xây dựng cơ sở dữ liệu quản lý bán hàng cho <span class="noun">cửa hàng điện thoại</span>: quản lý <span class="noun">khách hàng</span>, <span class="noun">sản phẩm</span>, <span class="noun">nhân viên</span>, <span class="noun">hóa đơn</span> và <span class="noun">chi tiết từng hóa đơn</span>.</div>
      <div style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap">
        <span class="chip" style="font-size:14px">Ai mua?</span><span class="chip" style="font-size:14px">Mua gì?</span><span class="chip" style="font-size:14px">Ai bán?</span><span class="chip" style="font-size:14px">Bao nhiêu?</span><span class="chip" style="font-size:14px">Giá nào?</span>
      </div>`;
    const steps = h('div', 'erd-steps');
    const stepData = [
      ['Xác định thực thể', 'Danh từ trong yêu cầu → KHACHHANG, SANPHAM, NHANVIEN, HOADON, CHITIETHOADON.'],
      ['Xác định thuộc tính & khóa', 'Mỗi thực thể có mã định danh và các thuộc tính cần quản lý.'],
      ['Xác định quan hệ & số lượng', 'Khách → hóa đơn (1-N), hóa đơn → chi tiết (1-N), sản phẩm → chi tiết (1-N).']
    ];
    const stepEls = stepData.map(([t, d], i) => {
      const s = h('div', 'erd-step', `<div class="n">${i + 1}</div><div><h4>${t}</h4><p>${d}</p></div>`);
      s.style.opacity = 0;
      steps.appendChild(s);
      return s;
    });
    wrap.append(req, steps);
    const ents = h('div', 'erd-entities');
    const entData = [['KHACHHANG', 'Khách hàng'], ['SANPHAM', 'Sản phẩm'], ['NHANVIEN', 'Nhân viên'], ['HOADON', 'Hóa đơn'], ['CHITIETHOADON', 'Chi tiết hóa đơn']];
    const entEls = entData.map(([t, v], i) => {
      const e = h('div', 'card ent-chip', `<div class="tb">${t}</div><div class="vn">${v}</div>`);
      e.style.opacity = 0;
      ents.appendChild(e);
      return e;
    });
    el.append(wrap, ents);
    const nouns = [...req.querySelectorAll('.noun')];
    return {
      update(U) {
        const p0 = U.p(0, 0.05, 0.55);
        req.style.opacity = p0;
        req.style.transform = `translateY(${(1 - p0) * 14}px)`;
        nouns.forEach((n, i) => { n.style.color = U.p(2, 0.15 + i * 0.06, 0.4) > 0.1 ? '#67e8f9' : ''; });
        stepEls.forEach((s, i) => {
          const cue = i < 2 ? 1 : 4;
          const p = U.p(cue, 0.08 + i * 0.2, 0.5);
          s.style.opacity = p;
          s.style.transform = `translateY(${(1 - p) * 12}px)`;
        });
        entEls.forEach((e, i) => {
          const p = U.p(2, 0.1 + i * 0.16, 0.45);
          e.style.opacity = p;
          e.style.transform = `translateY(${(1 - p) * 14}px)`;
          e.style.borderColor = i === 4 ? 'rgba(251,191,36,.45)' : '';
        });
        const pf = U.p(4, 0.1, 0.5);
        ents.style.opacity = pf * 0.25 + 0.75;
      }
    };
  };

  /* ===== ERD BUILD ===== */
  B.erdbuild = (el, def) => {
    el.innerHTML = head(def);
    const stage = h('div', 'erd-stage');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'erd-svg');
    svg.setAttribute('viewBox', '0 0 1712 620');
    svg.setAttribute('width', '1712'); svg.setAttribute('height', '620');
    stage.appendChild(svg);

    const boxes = {};
    const mkBox = (id, name, vn, rows, attrs, x, y, w) => {
      const b = h('div', 'erd-box');
      b.style.left = x + 'px'; b.style.top = y + 'px'; b.style.width = w + 'px';
      b.innerHTML = `<div class="hd"><span>${name}</span><span class="vn">${vn}</span></div><div class="rows">${rows.map((r) => `<div class="erd-row"><span>${r[2] ? `<span class="key ${r[2]}">${r[2].toUpperCase()}</span> ` : ''}${r[0]}</span><span class="type">${r[1]}</span></div>`).join('')}</div>${attrs ? `<div class="attrs">${attrs}</div>` : ''}`;
      stage.appendChild(b);
      boxes[id] = b;
      return b;
    };

    mkBox('KH', 'KHACHHANG', 'khách hàng', [['MaKH', 'CHAR(5)', 'pk'], ['HoTen', 'NVARCHAR', ''], ['SDT', 'VARCHAR', ''], ['DiaChi', 'NVARCHAR', '']], '', 10, 0, 300);
    mkBox('NV', 'NHANVIEN', 'nhân viên', [['MaNV', 'CHAR(5)', 'pk'], ['HoTen', 'NVARCHAR', ''], ['ChucVu', 'NVARCHAR', '']], '', 1402, 0, 300);
    mkBox('HD', 'HOADON', 'hóa đơn', [['MaHD', 'CHAR(6)', 'pk'], ['NgayLap', 'DATE', ''], ['MaKH', 'CHAR(5)', 'fk'], ['MaNV', 'CHAR(5)', 'fk']], 'TongTien là thuộc tính dẫn xuất — tính từ chi tiết', 610, 178, 330);
    mkBox('SP', 'SANPHAM', 'sản phẩm', [['MaSP', 'CHAR(5)', 'pk'], ['TenSP', 'NVARCHAR', ''], ['Hang', 'NVARCHAR', ''], ['DonGia', 'DECIMAL', ''], ['SoLuongTon', 'INT', '']], '', 1402, 296, 300);
    mkBox('CT', 'CHITIETHOADON', 'chi tiết hóa đơn', [['MaHD', 'CHAR(6)', 'pk'], ['MaSP', 'CHAR(5)', 'pk'], ['SoLuong', 'INT', ''], ['DonGia', 'DECIMAL', '']], 'Khóa chính ghép: (MaHD, MaSP) · MaHD, MaSP đồng thời là FK', 585, 424, 380);

    const linkDefs = [
      { d: 'M 160 152 V 205 H 560 V 240 H 610', one: [178, 168], many: [585, 228] },
      { d: 'M 1552 126 V 205 H 990 V 240 H 940', one: [1532, 168], many: [963, 228] },
      { d: 'M 775 348 V 424', one: [795, 370], many: [795, 408] },
      { d: 'M 1402 390 H 1200 V 470 H 965', one: [1385, 404], many: [988, 456] }
    ];
    const links = linkDefs.map((ld) => {
      const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      p.setAttribute('d', ld.d);
      p.setAttribute('fill', 'none');
      p.setAttribute('stroke', '#38bdf8');
      p.setAttribute('stroke-width', '2');
      p.setAttribute('pathLength', '100');
      p.setAttribute('stroke-dasharray', '100');
      p.setAttribute('stroke-dashoffset', '100');
      p.style.filter = 'drop-shadow(0 0 5px rgba(56,189,248,.55))';
      svg.appendChild(p);
      const l1 = h('div', 'erd-card-label', '1');
      l1.style.left = ld.one[0] + 'px'; l1.style.top = ld.one[1] + 'px';
      const lN = h('div', 'erd-card-label', 'N');
      lN.style.left = ld.many[0] + 'px'; lN.style.top = ld.many[1] + 'px';
      lN.style.color = '#38bdf8';
      stage.append(l1, lN);
      return { p, l1, lN };
    });

    const legend = h('div', 'erd-legend', `<div class="lg"><span class="dotk" style="background:#fbbf24"></span>Khóa chính (PK)</div><div class="lg"><span class="dotk" style="background:#38bdf8"></span>Khóa ngoại (FK)</div><div class="lg"><span class="dotk" style="background:#22d3ee"></span>Quan hệ 1 — N</div>`);
    legend.style.top = '8px'; legend.style.left = '650px'; legend.style.bottom = 'auto';
    const foot = h('div', 'erd-footnote', `<b style="color:#fcd34d">Vì sao lưu DonGia trong CHITIETHOADON?</b> Để giữ đúng giá tại thời điểm bán — sản phẩm đổi giá sau này không làm sai hóa đơn cũ.`);
    foot.style.right = '8px'; foot.style.bottom = '0px'; foot.style.width = '470px';
    stage.append(legend, foot);
    el.appendChild(stage);

    const dn = boxes.CT;
    return {
      update(U) {
        const order = ['KH', 'NV', 'HD', 'SP', 'CT'];
        order.forEach((id, i) => {
          const p = U.p(0, 0.05 + i * 0.14, 0.5);
          const b = boxes[id];
          b.style.opacity = p;
          b.style.transform = `translateY(${(1 - p) * 14}px)`;
        });
        links.forEach((l, i) => {
          const cue = i < 2 ? 1 : 2;
          const p = U.p(cue, 0.05 + (i % 2) * 0.3, 0.65);
          l.p.setAttribute('stroke-dashoffset', 100 * (1 - p));
          l.l1.style.opacity = p;
          l.lN.style.opacity = p;
        });
        const pd = U.p(3, 0.05, 0.5);
        const dg = dn.querySelectorAll('.erd-row')[3];
        if (dg) {
          dg.style.background = `rgba(251,191,36,${0.08 + pd * 0.12})`;
          dg.style.borderRadius = '4px';
        }
        foot.style.opacity = U.p(3, 0.1, 0.55);
        foot.style.transform = `translateY(${(1 - U.p(3, 0.1, 0.55)) * 12}px)`;
        legend.style.opacity = U.p(0, 0.3, 0.5);
      }
    };
  };

  /* ===== SQL GROUPS ===== */
  B.sqlgroups = (el, def) => {
    el.innerHTML = head(def);
    const wrap = h('div', 'sqlg');
    const data = [
      ['DDL', 'Định nghĩa cấu trúc dữ liệu', ['CREATE', 'ALTER', 'DROP'], 'ddl', '01'],
      ['DML', 'Thao tác trên dữ liệu', ['INSERT', 'UPDATE', 'DELETE'], 'dml', '02'],
      ['DQL', 'Truy vấn dữ liệu', ['SELECT'], 'dql', '03'],
      ['DCL', 'Điều khiển truy cập', ['GRANT', 'REVOKE'], 'dcl', '04'],
      ['TCL', 'Điều khiển giao dịch', ['COMMIT', 'ROLLBACK'], 'tcl', '05']
    ];
    const rows = data.map(([n, d, cmds, cls, num]) => {
      const r = h('div', 'sqlg-row ' + cls, `<div class="gname">${n}</div><div class="gdesc">${d}</div><div class="cmds">${cmds.map((c) => `<span class="sqlg-cmd">${c}</span>`).join('')}</div><div class="cn">${num}</div>`);
      r.style.opacity = 0;
      wrap.appendChild(r);
      return r;
    });
    const foot = h('div', 'sqlg-foot', `${icon('code')}<span><b style="color:#a5f3fc">SELECT</b> là lệnh dùng nhiều nhất — nhưng DDL và DML mới là phần tạo nên dữ liệu.</span>`);
    el.append(wrap, foot);
    return {
      update(U) {
        rows.forEach((r, i) => {
          const cue = i < 3 ? i + 1 : 4;
          const p = U.p(cue, 0.05, 0.5);
          r.style.opacity = p;
          r.style.transform = `translateX(${(1 - p) * -20}px)`;
        });
        const p = U.p(5, 0.05, 0.5);
        foot.style.opacity = p;
        foot.style.transform = `translateY(${(1 - p) * 10}px)`;
      }
    };
  };

  /* ===== SQL CREATE ===== */
  B.sqlcreate = (el, def) => {
    el.innerHTML = head(def);
    const layout = h('div', 'sql-create-layout');
    const code = codeBlock([
      'CREATE TABLE SinhVien (',
      '    MaSV   VARCHAR(10) PRIMARY KEY,',
      '    HoTen  NVARCHAR(100),',
      '    Lop    VARCHAR(20),',
      '    Email  VARCHAR(100)',
      ');'
    ], { context: 'CSDL_SinhVien', size: 27 });
    layout.appendChild(code.el);
    const side = h('div', 'side');
    const hints = [
      ['Tạo bảng', 'CREATE TABLE + tên bảng, các cột nằm trong ngoặc đơn.', 'table'],
      ['PRIMARY KEY', 'Ghi ngay sau kiểu dữ liệu của MaSV — định danh duy nhất.', 'key'],
      ['NVARCHAR', 'Kiểu Unicode, lưu đúng tiếng Việt có dấu.', 'code']
    ];
    const hintEls = hints.map(([t, d, ic], i) => {
      const x = h('div', 'card create-hint', `<h4>${icon(ic)}${t}</h4><p>${d}</p>`);
      x.style.opacity = 0;
      side.appendChild(x);
      return x;
    });
    const struct = h('div', 'card struct-table');
    const st = dataTable([{ label: 'Cột' }, { label: 'Kiểu' }, { label: 'Ràng buộc' }], [
      ['MaSV', 'VARCHAR(10)', 'PK'],
      ['HoTen', 'NVARCHAR(100)', ''],
      ['Lop', 'VARCHAR(20)', ''],
      ['Email', 'VARCHAR(100)', '']
    ]);
    st.table.style.fontSize = '15px';
    struct.appendChild(st.el);
    struct.style.opacity = 0;
    side.appendChild(struct);
    const ok = h('div', 'success-toast', icon('check') + 'Query OK — đã tạo bảng SinhVien');
    ok.style.position = 'relative';
    ok.style.opacity = 0;
    side.appendChild(ok);
    layout.appendChild(side);
    el.appendChild(layout);

    const t0 = def.cues[0].start - def.start;
    const t1 = def.cues[2].start - def.start + def.cues[2].dur * 0.95;
    return {
      update(U) {
        const prog = clamp((U.t - t0 - 0.55) / (t1 - t0 - 0.6));
        code.setTyped(prog * code.total);
        code.blink(U.t);
        hintEls.forEach((x, i) => {
          const cue = i === 0 ? 0 : i === 1 ? 1 : 2;
          const p = U.p(cue, 0.15, 0.5);
          x.style.opacity = p;
          x.style.transform = `translateY(${(1 - p) * 12}px)`;
        });
        const pl = U.p(1, 0.05, 0.4);
        code.lines.forEach((ln, i) => ln.classList.toggle('hl-line', i === 1 && pl > 0.1));
        const pc = U.p(2, 0.05, 0.4);
        if (pc > 0.1) code.lines.forEach((ln, i) => ln.classList.toggle('hl-line', i >= 3 && i <= 4));
        const p3 = U.p(3, 0.1, 0.55);
        struct.style.opacity = p3;
        struct.style.transform = `translateY(${(1 - p3) * 12}px)`;
        const p4 = U.p(3, 0.4, 0.4);
        ok.style.opacity = p4;
        ok.style.transform = `translateY(${(1 - p4) * 8}px)`;
      }
    };
  };

  /* ===== SQL INSERT ===== */
  B.sqlinsert = (el, def) => {
    el.innerHTML = head(def);
    const layout = h('div', 'insert-layout');
    const code = codeBlock([
      "INSERT INTO SinhVien",
      "VALUES ('SV001', N'Nguyen Van An', 'DA22TTC', 'an@gmail.com');",
      '',
      'SELECT * FROM SinhVien;'
    ], { context: 'CSDL_SinhVien', size: 24 });
    layout.appendChild(code.el);
    const res = h('div', 'insert-result');
    const rhead = h('div', 'result-head', '<span class="rt">KẾT QUẢ TRUY VẤN</span><span>1 dòng</span>');
    const rs = h('div', 'result-set');
    const t = dataTable([{ label: 'MaSV', tag: 'pk' }, { label: 'HoTen' }, { label: 'Lop' }, { label: 'Email' }], [SV[0]]);
    t.table.style.fontSize = '18px';
    rs.appendChild(t.el);
    const note = h('div', 'result-note', '<b style="color:#a5f3fc">Result set</b> — bảng tạm trả về. Câu lệnh SELECT <b>không</b> thay đổi dữ liệu gốc.');
    const ok = h('div', 'success-toast', icon('check') + '1 row affected — đã thêm bản ghi');
    ok.style.position = 'relative';
    ok.style.opacity = 0;
    res.append(rhead, rs, note, ok);
    layout.appendChild(res);
    el.appendChild(layout);

    const splitAt = "VALUES ('SV001', N'Nguyen Van An', 'DA22TTC', 'an@gmail.com');".length + 1;
    const split = code.lines[0].textContent.length + 1 + splitAt;
    const t0 = def.cues[0].start - def.start;
    const t1 = def.cues[0].start - def.start + def.cues[0].dur;
    const t2 = def.cues[2].start - def.start;
    const t3 = def.cues[2].start - def.start + def.cues[2].dur;
    return {
      update(U) {
        let chars;
        if (U.t < t1) chars = clamp((U.t - t0 - 0.3) / (t1 - t0 - 0.4)) * split;
        else if (U.t < t2) chars = split;
        else chars = split + clamp((U.t - t2 - 0.2) / (t3 - t2 - 0.3)) * (code.total - split);
        code.setTyped(chars);
        code.blink(U.t);
        const pn = U.p(1, 0.05, 0.4);
        if (pn > 0.1) code.lines.forEach((ln, i) => ln.classList.toggle('hl-line', i === 1));
        const p2 = U.p(2, 0.08, 0.4);
        if (p2 > 0.1) code.lines.forEach((ln, i) => ln.classList.toggle('hl-line', i === 3));
        const pr = U.p(2, 0.3, 0.5);
        rs.style.opacity = pr;
        rs.style.transform = `translateY(${(1 - pr) * 12}px)`;
        t.rows.forEach((tr) => { tr.style.background = `rgba(34,211,238,${0.04 + pr * 0.08})`; });
        note.style.opacity = U.p(3, 0.05, 0.5);
        const p4 = U.p(3, 0.3, 0.4);
        ok.style.opacity = p4;
        ok.style.transform = `translateY(${(1 - p4) * 8}px)`;
      }
    };
  };

  /* ===== SHOP SCHEMA ===== */
  B.shopschema = (el, def) => {
    el.innerHTML = head(def);
    const layout = h('div', 'ss-layout');
    const main = h('div', 'card ss-main');
    main.innerHTML = `<div class="card-title" style="margin-bottom:12px"><span class="num">S</span> SANPHAM <span style="margin-left:auto;font-family:'JBMono';font-size:11px;color:#5f7f99;letter-spacing:.06em">5 dòng</span></div>`;
    const t1 = dataTable([{ label: 'MaSP', tag: 'pk' }, { label: 'TenSP' }, { label: 'Hang' }, { label: 'DonGia (đ)' }, { label: 'Ton' }],
      SP.map(([a, b, c, d, e]) => [a, b, c, money(d), e]));
    t1.table.style.fontSize = '17px';
    main.appendChild(t1.el);
    const ctCard = h('div', 'ss-ct');
    ctCard.innerHTML = `<div class="mh"><span class="t">CHITIETHOADON</span><span class="c">8 dòng · PK ghép (MaHD, MaSP)</span></div>`;
    const t4 = dataTable([{ label: 'MaHD', tag: 'pk' }, { label: 'MaSP', tag: 'pk' }, { label: 'SoLuong' }, { label: 'DonGia (đ)' }],
      [['HD001', 'SP01', 1, money(32000000)], ['HD001', 'SP05', 2, money(8000000)], ['HD002', 'SP02', 1, money(30000000)]]);
    t4.table.classList.add('dense');
    t4.table.style.fontSize = '15px';
    ctCard.appendChild(t4.el);
    main.appendChild(ctCard);
    const side = h('div', 'ss-side');
    const khCard = h('div', 'card ss-mini');
    khCard.innerHTML = `<div class="mh"><span class="t">KHACHHANG</span><span class="c">4 khách</span></div>`;
    const t2 = dataTable([{ label: 'MaKH', tag: 'pk' }, { label: 'HoTen' }, { label: 'SDT' }], KH.map(([a, b, c]) => [a, b, c]));
    khCard.appendChild(t2.el);
    const hdCard = h('div', 'card ss-mini');
    hdCard.innerHTML = `<div class="mh"><span class="t">HOADON</span><span class="c">5 hóa đơn</span></div>`;
    const t3 = dataTable([{ label: 'MaHD', tag: 'pk' }, { label: 'NgayLap' }, { label: 'MaKH', tag: 'fk' }, { label: 'MaNV', tag: 'fk' }], HD.map(([a, b, c, d]) => [a, b, c, d]));
    hdCard.appendChild(t3.el);
    side.append(khCard, hdCard);
    layout.append(main, side);
    const steps = h('div', 'ss-steps', ['Đọc đề bài', 'Phân tích yêu cầu', 'Viết câu lệnh SQL', 'Đọc kết quả'].map((t, i) => `<div class="ss-step"><span class="n">0${i + 1}</span><span>${t}</span></div>`).join(''));
    el.append(layout, steps);
    return {
      update(U) {
        const p0 = U.p(0, 0.05, 0.55);
        main.style.opacity = p0;
        main.style.transform = `translateY(${(1 - p0) * 14}px)`;
        [khCard, hdCard].forEach((c, i) => {
          const p = U.p(1, 0.1 + i * 0.25, 0.5);
          c.style.opacity = p;
          c.style.transform = `translateY(${(1 - p) * 12}px)`;
          c.querySelectorAll('tbody tr').forEach((tr, k) => {
            tr.style.opacity = clamp(p * 1.6 - k * 0.06);
          });
        });
        t1.rows.forEach((tr, i) => {
          tr.style.opacity = clamp(U.p(1, i * 0.06, 0.4) * 1.4);
        });
        const pct = U.p(2, 0.0, 0.45);
        ctCard.style.opacity = pct;
        ctCard.style.transform = `translateY(${(1 - pct) * 10}px)`;
        const p2 = U.p(2, 0.05, 0.55);
        steps.style.opacity = p2;
        steps.style.transform = `translateY(${(1 - p2) * 10}px)`;
      }
    };
  };

  /* ===== QUERY SCENES ===== */
  function queryScene(el, def, cfg) {
    el.innerHTML = head(def);
    const wrap = h('div', 'q-layout');
    const left = h('div', 'q-left');
    const bBrief = h('div', 'card q-block');
    bBrief.innerHTML = `<h4>${icon('search')} Đề bài</h4><div class="brief">${cfg.brief}</div>`;
    const bAna = h('div', 'card q-block');
    bAna.innerHTML = `<h4>${icon('flow')} Phân tích</h4><div class="q-bullets">${cfg.analysis.map((t, i) => `<div class="q-bullet"><span class="b">0${i + 1}</span><span>${t}</span></div>`).join('')}</div>`;
    const extra = h('div', 'q-extra');
    if (cfg.extra) extra.innerHTML = cfg.extra.html;
    left.append(bBrief, bAna, extra);

    const right = h('div', 'q-right');
    const code = codeBlock(cfg.code, { context: cfg.context || 'CSDL_CuaHang', size: cfg.codeSize || 24 });
    code.el.classList.add('q-code');
    const resCard = h('div', 'card q-result');
    resCard.innerHTML = `<div class="rhead"><span class="rt">KẾT QUẢ TRUY VẤN</span><span class="rc">${cfg.count || ''}</span></div>`;
    const body = h('div', 'result-scroll');
    let rowEls = [];
    if (cfg.resultTable) {
      const rt = dataTable(cfg.resultTable.headers, cfg.resultTable.rows);
      rt.table.style.fontSize = (cfg.resultSize || 17) + 'px';
      body.appendChild(rt.el);
      rowEls = rt.rows;
    } else if (cfg.resultHTML) {
      body.innerHTML = cfg.resultHTML;
    }
    const note = h('div', 'q-note', `<span class="mini">✓</span><span>${cfg.note}</span>`);
    if (cfg.compact) resCard.classList.add('compact');
    resCard.append(body);
    if (cfg.note && !cfg.hideNote) resCard.append(note);
    const summary = h('div', 'result-summary', cfg.summary || '');
    const ok = h('div', 'success-toast', icon('check') + (cfg.toast || 'Truy vấn thành công'));
    ok.style.position = 'relative'; ok.style.opacity = 0;
    if (!cfg.hideSummary) resCard.append(summary);
    if (!cfg.hideToast) resCard.append(ok);
    right.append(code.el, resCard);
    wrap.append(left, right);
    el.appendChild(wrap);

    const bullets = [...bAna.querySelectorAll('.q-bullet')];
    const extraEls = [...extra.querySelectorAll('[data-rev]')];
    const t0 = def.cues[2].start - def.start + 0.25;
    const t1 = def.cues[2].start - def.start + def.cues[2].dur * 0.95;
    const counter = cfg.counter;
    return {
      update(U) {
        const p0 = U.p(0, 0.05, 0.55);
        bBrief.style.opacity = p0;
        bBrief.style.transform = `translateY(${(1 - p0) * 14}px)`;
        const pa = U.p(1, 0.02, 0.5);
        bAna.style.opacity = pa;
        bAna.style.transform = `translateY(${(1 - pa) * 12}px)`;
        bullets.forEach((b, i) => {
          const p = U.p(1, 0.1 + i * 0.22, 0.45);
          b.style.opacity = p;
          b.style.transform = `translateX(${(1 - p) * -8}px)`;
        });
        extraEls.forEach((b, i) => {
          const p = U.p(1, 0.3 + i * 0.15, 0.45);
          b.style.opacity = p;
          b.style.transform = `translateY(${(1 - p) * 10}px)`;
        });
        const prog = clamp((U.t - t0) / (t1 - t0));
        code.setTyped(prog * code.total);
        code.blink(U.t);
        const pr = U.p(3, 0.02, 0.5);
        resCard.style.opacity = 0.35 + pr * 0.65;
        resCard.style.transform = `translateY(${(1 - pr) * 10}px)`;
        rowEls.forEach((tr, i) => {
          const p = U.p(3, 0.08 + i * 0.1, 0.4);
          tr.style.opacity = p;
          tr.style.transform = `translateY(${(1 - p) * 10}px)`;
          if (cfg.rowTone) cfg.rowTone(tr, i, U);
        });
        note.style.opacity = U.p(3, 0.4, 0.5);
        const ps = U.p(3, 0.3, 0.5);
        summary.style.opacity = ps;
        summary.style.transform = `translateY(${(1 - ps) * 8}px)`;
        const pok = U.p(3, 0.5, 0.4);
        ok.style.opacity = pok;
        ok.style.transform = `translateY(${(1 - pok) * 8}px)`;
        if (counter) counter(U, el, pr);
      }
    };
  }

  B.queryAll = (el, def) => queryScene(el, def, {
    brief: 'Hiển thị toàn bộ danh sách sản phẩm để nhân viên kiểm kê kho.',
    analysis: ['Cần tất cả các cột của bảng SanPham.', 'Không có điều kiện lọc — lấy mọi dòng.', 'Dùng dấu * để chọn toàn bộ cột.'],
    code: ['SELECT *', 'FROM SanPham;'],
    resultTable: {
      headers: [{ label: 'MaSP', tag: 'pk' }, { label: 'TenSP' }, { label: 'Hang' }, { label: 'DonGia (đ)' }, { label: 'Ton' }],
      rows: SP.map(([a, b, c, d, e]) => [a, b, c, money(d), e])
    },
    count: '5 dòng',
    note: 'SELECT * trả về mọi cột; không có WHERE nên toàn bộ 5 dòng được lấy.',
    toast: 'Đã lấy 5 sản phẩm',
    summary: `<span class="lb">SẢN PHẨM</span><span class="big">5</span><span style="color:#6ee7b7">dòng dữ liệu</span>`
  });

  B.queryPrice = (el, def) => queryScene(el, def, {
    brief: 'Lọc các sản phẩm có giá trên 10 triệu đồng để đưa vào nhóm cao cấp.',
    analysis: ['Lọc theo cột DonGia.', 'Mệnh đề WHERE, toán tử >.', 'Đơn giá tính bằng đồng: 10.000.000.'],
    code: ['SELECT *', 'FROM SanPham', 'WHERE DonGia > 10000000;'],
    extra: { html: `<div class="q2-rule" data-rev>${icon('filter')} DonGia &gt; 10.000.000 đ</div>` },
    resultTable: {
      headers: [{ label: 'MaSP', tag: 'pk' }, { label: 'TenSP' }, { label: 'Hang' }, { label: 'DonGia (đ)' }],
      rows: SP.map(([a, b, c, d]) => [a, b, c, money(d)])
    },
    count: '5 dòng → lọc còn 3',
    note: 'WHERE kiểm tra từng dòng; chỉ giữ các dòng có DonGia lớn hơn 10 triệu.',
    toast: '3 sản phẩm thỏa điều kiện',
    summary: `<span class="lb">KẾT QUẢ LỌC</span><span class="big">3</span><span style="color:#6ee7b7">/ 5 sản phẩm</span>`,
    rowTone(tr, i, U) {
      const p = U.p(3, 0.02, 0.4);
      const keep = i < 3;
      tr.classList.toggle('rowdim', !keep && p > 0.3);
      tr.classList.toggle('rowon', keep && p > 0.3);
    }
  });

  B.queryCustomers = (el, def) => queryScene(el, def, {
    brief: 'Liệt kê khách hàng đã từng mua hàng, mỗi người xuất hiện một lần.',
    analysis: ['Tên khách ở bảng KhachHang.', 'Việc mua hàng nằm ở bảng HoaDon.', 'Nối qua MaKH; DISTINCT để loại trùng.'],
    code: [
      'SELECT DISTINCT KH.MaKH, KH.HoTen',
      'FROM KhachHang KH',
      'INNER JOIN HoaDon HD',
      '    ON KH.MaKH = HD.MaKH;'
    ],
    extra: { html: `<div class="q3-join" data-rev><span class="t">KhachHang</span><span class="j">INNER JOIN</span><span class="t">HoaDon</span><span style="color:#94a3b8">ON MaKH</span></div>` },
    resultTable: {
      headers: [{ label: 'MaKH', tag: 'pk' }, { label: 'HoTen' }],
      rows: [['KH01', 'Nguyễn Văn An'], ['KH02', 'Trần Thị Bình'], ['KH03', 'Lê Văn Nam']]
    },
    count: '3 khách',
    note: 'INNER JOIN chỉ giữ các cặp khớp ở cả hai bảng — KH04 chưa mua hàng nên không xuất hiện.',
    toast: 'Tìm thấy 3 khách đã mua hàng',
    summary: `<span class="lb">KHÁCH ĐÃ MUA</span><span class="big">3</span><span style="color:#6ee7b7">/ 4 khách hàng</span>`
  });

  B.queryRevenue = (el, def) => queryScene(el, def, {
    brief: 'Tính tổng doanh thu của cửa hàng từ toàn bộ chi tiết hóa đơn.',
    analysis: ['Thành tiền 1 dòng = SoLuong × DonGia.', 'Tổng doanh thu = SUM tất cả các dòng.', 'Không cần GROUP BY — gộp toàn bộ.'],
    code: ['SELECT SUM(SoLuong * DonGia)', '       AS TongDoanhThu', 'FROM ChiTietHoaDon;'],
    extra: {
      html: `<div class="q4-calc" data-rev>${[['HD001', '48.000.000'], ['HD002', '49.000.000'], ['HD003', '64.000.000'], ['HD004', '22.000.000'], ['HD005', '32.000.000']].map(([a, b]) => `<div class="q4-row"><span>${a}</span><b>${b} đ</b></div>`).join('')}<div class="q4-total"><span>TỔNG</span><span>215.000.000 đ</span></div></div>`
    },
    resultHTML: `<div style="padding:26px 8px;text-align:center"><div style="font-size:12px;letter-spacing:.2em;color:#6ee7b7;font-weight:700">TONGDOANHTHU</div><div id="revNum" style="font-size:58px;font-weight:800;letter-spacing:-.03em;color:#ecfeff;margin-top:6px">0</div><div style="font-size:15px;color:#7f9db8;margin-top:4px">đồng</div></div>`,
    count: '1 dòng',
    note: 'SUM gộp nhiều dòng thành một giá trị duy nhất — đúng 215.000.000 đồng.',
    toast: 'Tổng doanh thu: 215.000.000 đ',
    summary: `<span class="lb">DOANH THU</span><span class="big">215 triệu</span><span style="color:#6ee7b7">đồng</span>`,
    counter(U, el, pr) {
      const n = el.querySelector('#revNum');
      if (!n) return;
      const v = Math.round(215000000 * clamp(pr * 1.15));
      n.textContent = money(v);
    }
  });

  B.queryQty = (el, def) => queryScene(el, def, {
    brief: 'Thống kê số lượng đã bán của từng sản phẩm để biết mặt hàng nào bán chạy.',
    analysis: ['Nhóm các dòng theo MaSP.', 'Cộng SoLuong trong mỗi nhóm.', 'GROUP BY + SUM.'],
    code: ['SELECT MaSP, SUM(SoLuong) AS TongSoLuong', 'FROM ChiTietHoaDon', 'GROUP BY MaSP;'],
    extra: {
      html: `<div class="q5-bars" data-rev>${[['SP01', 4], ['SP02', 1], ['SP03', 1], ['SP04', 2], ['SP05', 3]].map(([s, v]) => `<div class="q5-bar"><span class="lbl2">${s}</span><div class="track"><div class="fill2" data-w="${v / 4 * 100}"></div></div><span class="v2">${v}</span></div>`).join('')}</div>`
    },
    resultTable: {
      headers: [{ label: 'MaSP', tag: 'pk' }, { label: 'TongSoLuong' }],
      rows: [['SP01', 4], ['SP02', 1], ['SP03', 1], ['SP04', 2], ['SP05', 3]]
    },
    count: '5 nhóm',
    note: 'GROUP BY gom các dòng cùng MaSP; SUM cộng số lượng trong từng nhóm.',
    toast: 'Đã thống kê 5 sản phẩm',
    summary: `<span class="lb">BÁN CHẠY NHẤT</span><span class="big">SP01</span><span style="color:#6ee7b7">4 chiếc</span>`,
    counter(U, el) {
      const p = U.p(1, 0.5, 0.9);
      el.querySelectorAll('.q5-bar .fill2').forEach((f, i) => {
        const target = parseFloat(f.dataset.w);
        f.style.width = (target * clamp(p * 1.2 - i * 0.04)) + '%';
      });
    }
  });

  B.queryJoin = (el, def) => queryScene(el, def, {
    brief: 'In bảng kê chi tiết: khách hàng, nhân viên, sản phẩm, số lượng và thành tiền.',
    analysis: ['Thông tin nằm ở 4 bảng.', 'Nối HoaDon → KhachHang, NhanVien.', 'Nối tiếp ChiTietHoaDon → SanPham.', 'Thành tiền = SoLuong × DonGia.'],
    code: [
      'SELECT HD.MaHD, KH.HoTen AS KhachHang,',
      '       NV.HoTen AS NhanVien, SP.TenSP,',
      '       CT.SoLuong, CT.SoLuong * CT.DonGia AS ThanhTien',
      'FROM HoaDon HD',
      'INNER JOIN KhachHang KH ON HD.MaKH = KH.MaKH',
      'INNER JOIN NhanVien NV ON HD.MaNV = NV.MaNV',
      'INNER JOIN ChiTietHoaDon CT ON HD.MaHD = CT.MaHD',
      'INNER JOIN SanPham SP ON CT.MaSP = SP.MaSP;'
    ],
    codeSize: 16,
    extra: {
      html: `<div class="q6-map" data-rev><span class="q6-t">HoaDon</span><span class="q6-a">⋈</span><span class="q6-t">KhachHang</span><span class="q6-a">⋈</span><span class="q6-t">NhanVien</span><span class="q6-a">⋈</span><span class="q6-t">ChiTiet</span><span class="q6-a">⋈</span><span class="q6-t">SanPham</span></div>`
    },
    resultTable: {
      headers: [{ label: 'MaHD' }, { label: 'Khách hàng' }, { label: 'Nhân viên' }, { label: 'Sản phẩm' }, { label: 'SL' }, { label: 'Thành tiền' }],
      rows: [
        ['HD001', 'Nguyễn Văn An', 'Nguyễn Minh Tuấn', 'iPhone 15 Pro Max', 1, '32.000.000'],
        ['HD001', 'Nguyễn Văn An', 'Nguyễn Minh Tuấn', 'Galaxy A55', 2, '16.000.000'],
        ['HD002', 'Trần Thị Bình', 'Nguyễn Minh Tuấn', 'Galaxy S24 Ultra', 1, '30.000.000'],
        ['HD002', 'Trần Thị Bình', 'Nguyễn Minh Tuấn', 'OPPO Reno 11', 2, '19.000.000'],
        ['HD003', 'Nguyễn Văn An', 'Trần Hoài An', 'iPhone 15 Pro Max', 2, '64.000.000'],
        ['HD004', 'Lê Văn Nam', 'Trần Hoài An', 'Xiaomi 14', 1, '14.000.000'],
        ['HD004', 'Lê Văn Nam', 'Trần Hoài An', 'Galaxy A55', 1, '8.000.000'],
        ['HD005', 'Lê Văn Nam', 'Nguyễn Minh Tuấn', 'iPhone 15 Pro Max', 1, '32.000.000']
      ]
    },
    resultSize: 13.5,
    compact: true,
    hideNote: true,
    hideSummary: true,
    hideToast: true,
    count: '8 dòng',
    note: 'Bốn lần INNER JOIN ghép dữ liệu đã tách nhỏ — đúng như một hóa đơn in cho khách.',
    toast: 'Đã ghép 4 bảng — 8 dòng',
    summary: `<span class="lb">BẢNG KÊ</span><span class="big">8</span><span style="color:#6ee7b7">dòng chi tiết</span>`
  });

  /* ===== SUMMARY ===== */
  B.summary = (el, def) => {
    el.innerHTML = head(def);
    const map = h('div', 'sum-map');
    map.innerHTML = `<svg class="sum-lines" viewBox="0 0 1712 620" width="1712" height="620" style="position:absolute;inset:0">
      ${[[300, 160], [1412, 160], [300, 430], [1412, 430], [856, 520]].map(([x, y]) => `<line x1="856" y1="310" x2="${x}" y2="${y}" stroke="rgba(34,211,238,.28)" stroke-width="1.3" stroke-dasharray="5 6"/>`).join('')}
    </svg>`;
    const center = h('div', 'sum-center', '<div class="t1">DATABASE</div><div class="t2">CSDL</div><div style="font-size:12px;color:#5f8fb2;margin-top:2px">bài giảng</div>');
    const nodes = [
      { x: 30, y: 30, t: 'Khái niệm', d: 'Dữ liệu có cấu trúc · DBMS · dữ liệu và thông tin', ic: 'db' },
      { x: 1342, y: 30, t: 'Thành phần', d: 'Bảng · dòng · cột · khóa chính · khóa ngoại', ic: 'table' },
      { x: 30, y: 330, t: 'Quan hệ', d: '1-1 · 1-N · N-N · bảng trung gian', ic: 'link' },
      { x: 1342, y: 330, t: 'Thiết kế ERD', d: 'Thực thể → bảng · thuộc tính → cột', ic: 'flow' },
      { x: 686, y: 470, t: 'SQL', d: 'DDL · DML · DQL · DCL · TCL + truy vấn', ic: 'code' }
    ];
    const nodeEls = nodes.map((n) => {
      const d = h('div', 'card sum-node', `<h4><span class="dot2"></span>${n.t}</h4><p>${n.d}</p>`);
      d.style.left = n.x + 'px'; d.style.top = n.y + 'px';
      map.append(d);
      return d;
    });
    map.appendChild(center);
    const wf = h('div', 'sum-workflow', ['Hiểu yêu cầu', 'Thiết kế ERD', 'Tạo bảng', 'Nhập dữ liệu', 'Truy vấn'].map((t, i) => `<div class="sum-wf">${t}</div>${i < 4 ? '<span class="sum-wf-ar">→</span>' : ''}`).join(''));
    el.append(map, wf);
    return {
      update(U) {
        const pc = U.p(0, 0.1, 0.6);
        center.style.opacity = pc;
        center.style.transform = `translate(-50%, -50%) scale(${0.88 + pc * 0.12})`;
        nodeEls.forEach((n, i) => {
          const p = U.p(Math.min(i + 1, 5), 0.1, 0.5);
          n.style.opacity = p;
          n.style.transform = `scale(${0.94 + p * 0.06})`;
        });
        const pw = U.p(5, 0.05, 0.55);
        wf.style.opacity = pw;
        wf.style.transform = `translateY(${(1 - pw) * 10}px)`;
      }
    };
  };

  /* ===== QUIZ ===== */
  const quizData = [
    { q: 'Thành phần nào xác định duy nhất mỗi bản ghi trong bảng?', options: ['Khóa ngoại', 'Khóa chính', 'Chỉ mục', 'Khóa ghép'], answer: 1, explain: 'Khóa chính không trùng và không để trống.' },
    { q: 'Quan hệ giữa Lop và SinhVien là loại nào?', options: ['Một-một', 'Một-nhiều', 'Nhiều-nhiều', 'Không xác định'], answer: 1, explain: 'Một lớp có nhiều sinh viên, mỗi sinh viên thuộc một lớp.' },
    { q: 'Lệnh nào thuộc nhóm DDL?', options: ['INSERT', 'SELECT', 'CREATE TABLE', 'COMMIT'], answer: 2, explain: 'CREATE TABLE định nghĩa cấu trúc bảng.' },
    { q: 'Lọc sản phẩm có giá trên 10 triệu dùng mệnh đề nào?', options: ['GROUP BY', 'ORDER BY', 'WHERE', 'HAVING'], answer: 2, explain: 'WHERE lọc từng dòng trước khi nhóm.' },
    { q: 'Quan hệ nhiều-nhiều được xử lý bằng cách nào?', options: ['Thêm khóa ngoại vào một bảng', 'Tạo bảng trung gian chứa hai khóa ngoại', 'Gộp hai bảng làm một', 'Dùng khóa chính ghép trong bảng gốc'], answer: 1, explain: 'Bảng trung gian chứa hai khóa ngoại, tạo thành khóa chính ghép.' }
  ];

  B.quiz = (el, def) => {
    el.innerHTML = head(def);
    const wrap = h('div', 'quiz-wrap');
    const side = h('div', 'quiz-side');
    const dots = quizData.map((_, i) => {
      const d = h('div', 'quiz-dot', `<span class="qdn">${i + 1}</span><span>CÂU ${i + 1}</span>`);
      side.appendChild(d);
      return d;
    });
    const cards = quizData.map((q, qi) => {
      const c = h('div', 'quiz-card card');
      c.style.position = 'absolute';
      c.style.left = '250px'; c.style.right = '0'; c.style.top = '0'; c.style.bottom = '0';
      c.style.opacity = 0;
      c.innerHTML = `<div class="quiz-qnum">CÂU HỎI ${qi + 1} / 05</div>
        <div class="quiz-q">${q.q}</div>
        <div class="quiz-opts">${q.options.map((o, i) => `<div class="quiz-opt" data-i="${i}"><span class="ol">${'ABCD'[i]}</span><span>${o}</span></div>`).join('')}</div>
        <div class="quiz-explain"><span class="ok2">✓</span><span>${q.explain}</span></div>
        <div class="quiz-timer"><span>SUY NGHĨ</span><svg class="quiz-ring" viewBox="0 0 44 44"><circle cx="22" cy="22" r="18" fill="none" stroke="rgba(148,163,184,.18)" stroke-width="3"/><circle class="ringfg" cx="22" cy="22" r="18" fill="none" stroke="#22d3ee" stroke-width="3" stroke-linecap="round" stroke-dasharray="113" stroke-dashoffset="113" transform="rotate(-90 22 22)"/></svg></div>`;
      wrap.appendChild(c);
      return c;
    });
    wrap.appendChild(side);
    const score = h('div', 'quiz-score', `<span>TIẾN ĐỘ</span><b id="qScore">0 / 5</b><span>đáp án</span>`);
    const final = h('div', 'card quiz-final', `<div class="qf-score"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="none" stroke="rgba(34,211,238,.16)" stroke-width="5"/><circle cx="60" cy="60" r="52" fill="none" stroke="#22d3ee" stroke-width="5" stroke-linecap="round" stroke-dasharray="327" stroke-dashoffset="0" transform="rotate(-90 60 60)"/></svg><div class="qfs-in"><b>5<span>/5</span></b><small>CÂU ĐÚNG</small></div></div>
      <div class="qf-body">
        <div class="quiz-qnum">HOÀN THÀNH · PHẦN 7</div>
        <div class="qf-title">Bạn đã đi hết 5 câu hỏi</div>
        <div class="qf-sub">Từ 4 câu đúng trở lên — bạn đã nắm chắc phần nền tảng.</div>
        <div class="qf-chips"><span class="chip">Khóa chính</span><span class="chip">Quan hệ 1–N</span><span class="chip">DDL</span><span class="chip">WHERE</span><span class="chip">Bảng trung gian</span></div>
        <div class="qf-note">Ôn lại: khóa chính · quan hệ · DDL/DML · WHERE · bảng trung gian</div>
      </div>`);
    final.style.position = 'absolute'; final.style.left = '250px'; final.style.right = '0'; final.style.top = '0'; final.style.bottom = '0';
    final.style.opacity = 0;
    wrap.appendChild(final);
    el.append(wrap, score);

    const timerEls = cards.map((c) => c.querySelector('.ringfg'));
    const qStart = (i) => def.cues[1 + i * 2].start - def.start;
    const getQ = (U) => {
      if (U.t >= def.cues[11].start - def.start) return 5;
      let q = 0;
      for (let i = 0; i < 5; i++) if (U.t >= qStart(i)) q = i;
      return q;
    };
    return {
      update(U) {
        const qi = getQ(U);
        cards.forEach((c, i) => { c.style.display = i === qi ? 'flex' : 'none'; });
        final.style.display = qi === 5 ? 'block' : 'none';
        final.style.opacity = qi === 5 ? U.p(11, 0.05, 0.6) : 0;
        score.style.opacity = 0.6;
        const pQuiz = U.p(0, 0.1, 0.6);
        wrap.style.opacity = pQuiz;
        if (qi < 5) {
          const c = cards[qi];
          const qCue = 1 + qi * 2, aCue = 2 + qi * 2;
          const show = U.p(qCue, 0.02, 0.5);
          c.style.opacity = show;
          c.style.transform = `translateY(${(1 - show) * 16}px)`;
          const isAnswer = U.on(aCue);
          const opts = [...c.querySelectorAll('.quiz-opt')];
          opts.forEach((o, oi) => {
            o.classList.toggle('correct', isAnswer && oi === quizData[qi].answer);
            o.classList.toggle('wrong', isAnswer && oi !== quizData[qi].answer);
          });
          const ex = c.querySelector('.quiz-explain');
          ex.style.opacity = isAnswer ? U.p(aCue, 0.1, 0.5) : 0;
          const ring = timerEls[qi];
          if (!isAnswer) {
            const qd = def.cues[qCue].dur;
            const p = clamp((U.t - (def.cues[qCue].start - def.start)) / qd);
            ring.setAttribute('stroke-dashoffset', 113 * (1 - p));
          } else ring.setAttribute('stroke-dashoffset', 0);
          dots.forEach((d, i) => {
            d.classList.toggle('active', i === qi && !isAnswer);
            d.classList.toggle('done', i < qi || (i === qi && isAnswer));
          });
          const sc = document.getElementById('qScore');
          if (sc) sc.textContent = `${qi + (isAnswer ? 1 : 0)} / 5`;
        } else {
          dots.forEach((d) => { d.classList.add('done'); d.classList.remove('active'); });
          const sc = document.getElementById('qScore');
          if (sc) sc.textContent = '5 / 5';
        }
        const ps = U.p(11, 0.05, 0.5);
        score.style.opacity = ps * 0.8;
        score.style.transform = `translateY(${(1 - ps) * 8}px)`;
      }
    };
  };

  /* ===== OUTRO ===== */
  B.outro = (el, def) => {
    el.innerHTML = `<div class="outro-wrap">
      <div class="outro-mark" style="color:#22d3ee">${icon('db', 'icon')}</div>
      <div class="outro-title">Hiểu dữ liệu,<br>hiểu hệ thống.</div>
      <div class="outro-sub">Cơ sở dữ liệu là nền móng của mọi phần mềm — và bạn đã có nền tảng để bắt đầu.</div>
      <div class="outro-chips">${[['Cài MySQL hoặc PostgreSQL', 'server'], ['Tạo bảng SinhVien', 'table'], ['Viết truy vấn đầu tiên', 'code']].map(([t, ic]) => `<div class="outro-chip">${icon(ic)}<span>${t}</span></div>`).join('')}</div>
      <div class="outro-thanks"><span class="ln"></span><span>CẢM ƠN CÁC BẠN ĐÃ THEO DÕI</span><span class="ln"></span></div>
    </div>`;
    const mark = el.querySelector('.outro-mark');
    const title = el.querySelector('.outro-title');
    const sub = el.querySelector('.outro-sub');
    const chips = [...el.querySelectorAll('.outro-chip')];
    const thanks = el.querySelector('.outro-thanks');
    const wrap = el.querySelector('.outro-wrap');
    return {
      update(U) {
        const pm = U.p(0, 0.05, 0.6);
        mark.style.opacity = pm;
        mark.style.transform = `scale(${0.85 + pm * 0.15})`;
        const pt = U.p(0, 0.15, 0.75);
        title.style.opacity = pt;
        title.style.transform = `translateY(${(1 - pt) * 22}px)`;
        const ps = U.p(0, 0.4, 0.7);
        sub.style.opacity = ps * 0.95;
        chips.forEach((c, i) => {
          const p = U.p(1, 0.05 + i * 0.22, 0.5);
          c.style.opacity = p;
          c.style.transform = `translateY(${(1 - p) * 12}px)`;
        });
        const pth = U.p(2, 0.1, 0.6);
        thanks.style.opacity = pth;
        if (U.t > def.dur - 0.8) {
          const f = clamp((def.dur - U.t) / 0.8);
          wrap.style.opacity = f;
          wrap.style.transform = `scale(${0.99 + f * 0.01})`;
        } else {
          wrap.style.opacity = 1;
          wrap.style.transform = 'none';
        }
      }
    };
  };

  /* ============================================================
     ENGINE
     ============================================================ */
  TL.scenes.forEach((def) => {
    const el = h('div', 'scene sc-' + def.type);
    root.appendChild(el);
    const builder = B[def.type];
    if (!builder) { el.innerHTML = head(def); console.warn('missing builder', def.type); }
    const api = builder ? builder(el, def) : null;
    const cues = def.cues.map((c) => ({ ...c, ls: c.start - def.start, le: c.end - def.start }));
    built.push({ def, el, api, cues });
  });

  // particles
  const particles = [];
  const pRoot = document.getElementById('particles');
  let seed = 42;
  const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
  for (let i = 0; i < 36; i++) {
    const d = h('div', 'particle');
    const x = rnd() * 1920, y = rnd() * 1080, s = 0.6 + rnd() * 1.8, sp = 0.15 + rnd() * 0.5;
    d.style.opacity = 0.15 + rnd() * 0.35;
    pRoot.appendChild(d);
    particles.push({ el: d, x, y, s, sp, ph: rnd() * 6.28 });
  }

  let cur = -1;
  let prev = -1;
  let capIdx = -1;
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
      if (sc.part) partChip.textContent = 'PHẦN ' + pad(sc.part) + ' · ' + PARTS[sc.part - 1].en;
      else partChip.textContent = 'BÀI GIẢNG';
      flash.style.opacity = 0;
    }
    const def = TL.scenes[idx];
    const local = t - def.start;
    const b = built[idx];
    const fin = smooth(local / 0.5);
    const fout = smooth((def.dur - local) / 0.45);
    b.el.style.opacity = Math.min(fin, fout, 1);
    b.el.style.transform = `translateY(${(1 - fin) * 10}px)`;
    b.el.style.zIndex = 20;
    if (prev >= 0 && prev !== idx) {
      const pb = built[prev];
      const po = 1 - clamp((t - (TL.scenes[prev].start + TL.scenes[prev].dur)) / 0.4);
      pb.el.style.opacity = po;
      pb.el.style.zIndex = 10;
      if (po <= 0) { pb.el.classList.remove('on'); prev = -1; }
    }
    if (b.api && b.api.update) {
      const U = {
        t: local,
        on: (i) => local >= b.cues[i].ls,
        p: (i, delay = 0, dur = 0.5) => ease(clamp((local - b.cues[i].ls - delay) / dur)),
        raw: (i, delay = 0) => clamp((local - b.cues[i].ls - delay) / 0.5),
        cueT: (i) => local - b.cues[i].ls,
        cueEnd: (i) => b.cues[i].le
      };
      b.api.update(U);
    }

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
    } else captionEl.style.opacity = 0;

    // chrome
    fill.style.width = (100 * t / TL.duration).toFixed(2) + '%';
    plabel.textContent = fmt(t);
    tcode.textContent = fmt(t) + ' / ' + fmt(TL.duration);

    // particles
    particles.forEach((p) => {
      const y = (p.y - t * 12 * p.sp + 2000) % 1200 - 60;
      const x = p.x + Math.sin(t * 0.35 + p.ph) * 26;
      p.el.style.transform = `translate(${x}px, ${y}px) scale(${p.s})`;
    });
  }

  window.renderFrame = renderFrame;
  window.__ready = true;
  window.__sceneAt = (id) => built.findIndex((b) => b.def.id === id);
  window.__built = built;
})();
