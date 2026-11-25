/* Shared behaviour: language, theme, lightbox, KaTeX, progress, quiz, exam, calculators. Everything runs in the browser; progress is stored in localStorage (this browser only). */
(function () {
  'use strict';
  var LS = { get: function (k, d) { var v = null; try { v = localStorage.getItem(k); } catch (e) { return d; } if (v === null) return d; try { return JSON.parse(v); } catch (e) { return v; } }, set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  var root = document.documentElement;
  function lang() { return root.getAttribute('data-lang') || 'en'; }
  function setLang(l) { root.setAttribute('data-lang', l); root.lang = l; LS.set('so:lang', l); document.querySelectorAll('[data-rerender]').forEach(function (n) { if (n._render) n._render(); }); renderMath(); }
  var stored = LS.get('so:lang', null);
  root.setAttribute('data-lang', stored || ((navigator.language || '').toLowerCase().indexOf('vi') === 0 ? 'vi' : 'en'));
  var th = LS.get('so:theme', null); if (th) root.setAttribute('data-theme', th);
  function renderMath() { if (window.renderMathInElement) { try { renderMathInElement(document.body, { delimiters: [{ left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }], throwOnError: false }); } catch (e) {} } }
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-act=lang]').forEach(function (b) { b.addEventListener('click', function () { setLang(lang() === 'en' ? 'vi' : 'en'); }); });
    document.querySelectorAll('[data-act=theme]').forEach(function (b) { b.addEventListener('click', function () { var d = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', d); LS.set('so:theme', d); }); });
    var lb = document.getElementById('lb');
    if (lb) { lb.addEventListener('click', function () { lb.classList.remove('on'); }); document.addEventListener('keydown', function (e) { if (e.key === 'Escape') lb.classList.remove('on'); }); }
    document.body.addEventListener('click', function (e) { var a = e.target.closest('[data-zoom]'); if (a && lb) { e.preventDefault(); lb.querySelector('img').src = a.getAttribute('data-zoom'); lb.querySelector('p').textContent = a.getAttribute('data-cap') || ''; lb.classList.add('on'); } });
    renderMath(); setTimeout(renderMath, 300);
    initEq(); initTrainer(); initExplore(); initBig12(); initPractice(); initExam(); initCalcs(); initGallery(); initWritten(); initSelfcheck(); initViewer(); progressBadges();
  });
  window.addEventListener('load', renderMath);

  /* ---------- progress ---------- */
  var PROG = LS.get('so:prog', {});           // id -> 1 right, 0 wrong (last attempt)
  function saveProg() { LS.set('so:prog', PROG); }
  function progressBadges() {
    var el = document.getElementById('prog-summary'); if (!el || !window.BANK) return;
    var n = BANK.length, r = 0, w = 0; BANK.forEach(function (q) { if (PROG[q.id] === 1) r++; else if (PROG[q.id] === 0) w++; });
    el.innerHTML = '<span lang="en">Answered ' + (r + w) + ' of ' + n + ' · right ' + r + ' · to review ' + w + '</span><span lang="vi">Đã làm ' + (r + w) + '/' + n + ' · đúng ' + r + ' · cần ôn ' + w + '</span>';
  }
  function T(o) { return o && typeof o === 'object' ? (o[lang()] || o.en) : o; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  var LECN = { L1: 'L1', L2: 'L2', L3: 'L3' };

  /* ---------- question rendering ---------- */
  function renderQ(q, idx, opts) {
    opts = opts || {};
    var d = document.createElement('div'); d.className = 'q'; d.id = 'q-' + q.id;
    var meta = '<div class="meta"><span class="tag">' + q.lec + '</span><span class="tag red">' + (q.origin === 'goc' ? (lang() === 'vi' ? 'Câu gốc của cô' : "Lecturer's question") : (lang() === 'vi' ? 'Bổ sung' : 'Added')) + '</span>' + (opts.num ? '#' + opts.num + ' · ' : '') + 'slide ' + esc(q.page) + '</div>';
    d.innerHTML = meta + '<div class="stem">' + esc(T(q.q)) + '</div>' + q.o.map(function (o, i) { return '<button class="opt" data-i="' + i + '">' + String.fromCharCode(65 + i) + '. ' + esc(T(o)) + '</button>'; }).join('') + '<div class="exp">' + esc(T(q.e)) + '</div>';
    d._q = q;
    var ans = opts.state && opts.state[q.id];
    function mark(pick) {
      d.classList.add('done');
      d.querySelectorAll('.opt').forEach(function (b) { var i = +b.dataset.i; b.disabled = true; if (i === q.c) b.classList.add('right'); else if (i === pick) b.classList.add('wrong'); });
    }
    d.querySelectorAll('.opt').forEach(function (b) {
      b.addEventListener('click', function () {
        if (d.classList.contains('done')) return;
        var pick = +b.dataset.i; mark(pick);
        if (opts.state) opts.state[q.id] = pick;
        if (opts.onAnswer) opts.onAnswer(q, pick === q.c, pick);
      });
    });
    if (ans !== undefined && ans !== null) mark(ans);
    return d;
  }

  /* ---------- Big 12 quiz (index) ---------- */
  function initBig12() {
    var box = document.getElementById('big12-quiz'); if (!box || !window.BANK) return;
    var qs = BANK.filter(function (q) { return q.big12; }).sort(function (a, b) { return a.big12 - b.big12; });
    var state = {}, out = document.getElementById('big12-result');
    function render() {
      box.innerHTML = ''; qs.forEach(function (q, i) { box.appendChild(renderQ(q, i, { num: q.big12, state: state, onAnswer: onAns })); }); sc();
    }
    function sc() {
      var done = Object.keys(state).length, right = qs.filter(function (q) { return state[q.id] === q.c; }).length;
      var cls = right >= 10 ? 'ok' : 'no';
      out.innerHTML = done < qs.length ? '<span class="score">' + done + '/' + qs.length + '</span>' : '<div class="banner ' + cls + '"><span lang="en">Big 12 score: ' + right + '/12. ' + (right >= 10 ? 'Well done: you can move on to the lectures.' : 'Review the items above, then retry.') + '</span><span lang="vi">Điểm Big 12: ' + right + '/12. ' + (right >= 10 ? 'Tốt: bạn có thể sang các bài.' : 'Xem lại các mục ở trên rồi làm lại.') + '</span></div>';
      LS.set('so:big12', { done: done, right: right });
    }
    function onAns(q, ok) { PROG[q.id] = ok ? 1 : 0; saveProg(); sc(); }
    box._render = function () { var s = state; render(); }; box.setAttribute('data-rerender', '1');
    document.getElementById('big12-reset').addEventListener('click', function () { state = {}; render(); });
    render();
  }

  /* ---------- practice bank ---------- */
  function initPractice() {
    var box = document.getElementById('bank'); if (!box || !window.BANK) return;
    var f = { lec: 'all', tag: 'all', org: 'all', st: 'all' }, state = {};
    var tags = {}; BANK.forEach(function (q) { tags[q.tag] = 1; });
    var tsel = document.getElementById('f-tag'); Object.keys(tags).sort().forEach(function (t) { var o = document.createElement('option'); o.value = t; o.textContent = t; tsel.appendChild(o); });
    ['lec', 'tag', 'org', 'st'].forEach(function (k) { document.getElementById('f-' + k).addEventListener('change', function (e) { f[k] = e.target.value; render(); }); });
    function pass(q) {
      if (f.lec !== 'all' && q.lec !== f.lec) return false; if (f.tag !== 'all' && q.tag !== f.tag) return false; if (f.org !== 'all' && q.origin !== f.org) return false;
      if (f.st === 'new' && PROG[q.id] !== undefined) return false; if (f.st === 'wrong' && PROG[q.id] !== 0) return false; if (f.st === 'right' && PROG[q.id] !== 1) return false; return true;
    }
    function render() {
      var list = BANK.filter(pass); box.innerHTML = '';
      document.getElementById('bank-count').textContent = list.length + ' / ' + BANK.length;
      list.forEach(function (q, i) { box.appendChild(renderQ(q, i, { num: i + 1, state: state, onAnswer: function (qq, ok) { PROG[qq.id] = ok ? 1 : 0; saveProg(); progressBadges(); } })); });
      progressBadges();
    }
    box._render = render; box.setAttribute('data-rerender', '1');
    document.getElementById('bank-reset').addEventListener('click', function () { if (confirm(lang() === 'vi' ? 'Xóa tiến độ?' : 'Reset progress?')) { PROG = {}; saveProg(); state = {}; render(); } });
    render();
  }

  /* ---------- mock exam ---------- */
  function initExam() {
    var box = document.getElementById('exam-box'); if (!box || !window.BANK) return;
    var cfg = document.getElementById('exam-cfg'), run = document.getElementById('exam-run'), res = document.getElementById('exam-res'), clock = document.getElementById('exam-clock');
    var timer = null, qs = [], answers = {}, left = 0, submitted = false;
    function pick(n, lec) {
      var pool = BANK.filter(function (q) { return lec === 'all' || q.lec === lec; });
      var a = pool.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
      return a.slice(0, Math.min(n, a.length));
    }
    function fmt(s) { var m = Math.floor(s / 60), x = s % 60; return (m < 10 ? '0' : '') + m + ':' + (x < 10 ? '0' : '') + x; }
    function draw() {
      run.innerHTML = ''; qs.forEach(function (q, i) {
        var d = document.createElement('div'); d.className = 'q'; d.id = 'e-' + q.id;
        d.innerHTML = '<div class="meta"><span class="tag">' + q.lec + '</span>#' + (i + 1) + '</div><div class="stem">' + esc(T(q.q)) + '</div>' + q.o.map(function (o, k) { return '<button class="opt" data-k="' + k + '"' + (submitted ? ' disabled' : '') + '>' + String.fromCharCode(65 + k) + '. ' + esc(T(o)) + '</button>'; }).join('') + '<div class="exp">' + esc(T(q.e)) + '</div>';
        d.querySelectorAll('.opt').forEach(function (b) {
          var k = +b.dataset.k; if (answers[q.id] === k) b.style.outline = '3px solid var(--blue)';
          b.addEventListener('click', function () { if (submitted) return; answers[q.id] = k; d.querySelectorAll('.opt').forEach(function (x) { x.style.outline = ''; }); b.style.outline = '3px solid var(--blue)'; });
          if (submitted) { if (k === q.c) b.classList.add('right'); else if (answers[q.id] === k) b.classList.add('wrong'); }
        });
        if (submitted) d.classList.add('done'); run.appendChild(d);
      });
    }
    function finish() {
      submitted = true; clearInterval(timer); var right = 0; qs.forEach(function (q) { var ok = answers[q.id] === q.c; if (ok) right++; PROG[q.id] = ok ? 1 : 0; }); saveProg();
      var pct = Math.round(100 * right / qs.length);
      res.innerHTML = '<div class="banner ' + (pct >= 70 ? 'ok' : 'no') + '"><span lang="en">Score ' + right + '/' + qs.length + ' (' + pct + ' %). Wrong answers are marked below with the explanation.</span><span lang="vi">Điểm ' + right + '/' + qs.length + ' (' + pct + ' %). Câu sai được đánh dấu bên dưới kèm giải thích.</span></div>';
      draw(); window.scrollTo(0, 0);
    }
    box._render = function () { if (qs.length) draw(); }; box.setAttribute('data-rerender', '1');
    document.getElementById('exam-start').addEventListener('click', function () {
      var n = +document.getElementById('ex-n').value, lec = document.getElementById('ex-lec').value, min = +document.getElementById('ex-min').value;
      qs = pick(n, lec); answers = {}; submitted = false; res.innerHTML = ''; left = min * 60; draw(); document.getElementById('exam-submit').style.display = '';
      clearInterval(timer); clock.textContent = fmt(left); timer = setInterval(function () { left--; clock.textContent = fmt(left); if (left <= 0) finish(); }, 1000);
    });
    document.getElementById('exam-submit').addEventListener('click', function () { if (!submitted && qs.length) finish(); });
  }

  /* ---------- calculators ---------- */
  function initCalcs() {
    if (!window.CALC) return; var C = CALC, K = C.K;
    function num(id) { return parseFloat(document.getElementById(id).value); }
    function fmt(x, d) { if (!isFinite(x)) return 'n/a'; var a = Math.abs(x); return (a !== 0 && (a < 1e-3 || a >= 1e6)) ? x.toExponential(d || 3) : x.toPrecision((d || 3) + 1).replace(/\.?0+$/, function (m) { return m.indexOf('.') >= 0 ? '' : m; }); }
    function bind(id, fn) { var box = document.getElementById(id); if (!box) return; var out = box.querySelector('.out'); function run() { try { out.textContent = fn(); } catch (e) { out.textContent = String(e); } } box.querySelectorAll('input,select').forEach(function (i) { i.addEventListener('input', run); i.addEventListener('change', run); }); run(); }
    bind('c-em', function () {
      var v = num('em-v'), u = document.getElementById('em-u').value; var f = { m: 1, cm: 1e-2, mm: 1e-3, um: 1e-6, nm: 1e-9, A: 1e-10 }[u]; var lam = v * f;
      return 'band: ' + C.band(lam) + '\nlambda = ' + fmt(lam) + ' m\nnu = c/lambda = ' + fmt(C.freq(lam)) + ' Hz\nE = h nu = ' + fmt(C.energyEV(lam)) + ' eV\nWien T (peak at this lambda) = ' + fmt(C.wienT(lam)) + ' K';
    });
    bind('c-tff', function () {
      var n = num('tf-n'), mu = num('tf-mu'), r = C.rho(n, mu);
      return 'rho = n mu m_H = ' + fmt(r) + ' g/cm3\nt_ff (slide) = 1/sqrt(G rho) = ' + fmt(C.tffSlide(r) / K.Myr) + ' Myr\nt_ff (full) = sqrt(3 pi/(32 G rho)) = ' + fmt(C.tffFull(r) / K.Myr) + ' Myr';
    });
    bind('c-jeans', function () {
      var n = num('j-n'), mu = num('j-mu'), T_ = num('j-T'), conv = document.getElementById('j-conv').value, sph = document.getElementById('j-sph').value;
      var L = C.LJ(T_, mu, n, conv), M = C.MJ(T_, mu, n, conv, sph);
      return 'c_s = ' + fmt(C.cs(T_, mu) / 1e5) + ' km/s\nL_J = ' + fmt(L / K.pc) + ' pc = ' + fmt(L / K.AU) + ' AU\nM_J = ' + fmt(M / K.Msun) + ' Msun  (sphere radius ' + (sph === 'half' ? 'L_J/2' : 'L_J') + ')\nconvention: ' + (conv === 'rig' ? 'L_J = c_s sqrt(pi/(G rho))' : 'L_J = c_s/sqrt(G rho) (slide-style)');
    });
    bind('c-spin', function () { var r = num('s-r'), w = num('s-w'); return 'omega2 = omega1 (r1/r2)^2 = ' + fmt(w * r * r) + '\nfactor (r1/r2)^2 = ' + fmt(r * r); });
    bind('c-age', function () {
      var th = num('a-th'), dp = num('a-dp'), t = num('a-t');
      return 'age from D/P: t = T_half log2(1 + D/P) = ' + fmt(C.ageFromDP(dp, th)) + ' Gyr\nparent left at t = ' + t + ' Gyr: ' + fmt(C.parentFrac(t, th)) + ' (' + fmt(100 * C.parentFrac(t, th)) + ' %)\nhalf-lives in t: ' + fmt(t / th);
    });
  }

  /* ---------- slide gallery ---------- */
  function initGallery() {
    var g = document.getElementById('gal'); if (!g || !window.SLIDES) return; var cur = 'all';
    function render() {
      g.innerHTML = ''; SLIDES.filter(function (s) { return cur === 'all' || s.l === cur; }).forEach(function (s) {
        var f = document.createElement('figure'); var cap = (lang() === 'vi' ? s.vi : s.en) || '';
        f.innerHTML = '<img loading="lazy" src="assets/slides/' + s.id + '_t.jpg" alt="' + esc(s.id) + '" data-zoom="assets/slides/' + s.id + '.jpg" data-cap="Lecture slide ' + s.l + ' p' + s.p + ' · ' + esc(cap) + '"><figcaption><b>' + s.l + ' p' + s.p + '</b> · ' + esc(cap) + '</figcaption>'; g.appendChild(f);
      });
    }
    g._render = render; g.setAttribute('data-rerender', '1');
    document.querySelectorAll('[data-gal]').forEach(function (b) { b.addEventListener('click', function () { cur = b.getAttribute('data-gal'); render(); }); }); render();
  }



  /* ---------- trainer: 126 similar problems, type your number, tolerance 3 % ---------- */
  function parseNum(t) {
    t = String(t).trim().replace(/\s+/g, '').replace(/,/g, '.').replace(/[x×*]10\^?([-+−]?\d+)/i, 'e$1').replace(/−/g, '-').replace(/[⁻]/g, '-');
    t = t.replace(/10\^([-+]?\d+)$/i, '1e$1'); var v = parseFloat(t); return isFinite(v) ? v : NaN;
  }
  function fmtN(x) { var a = Math.abs(x); if (a !== 0 && (a < 1e-2 || a >= 1e5)) { var e = x.toExponential(2).split('e'); return e[0] + '×10^' + parseInt(e[1], 10); } return String(+x.toPrecision(3)); }
  function initTrainer() {
    var box = document.getElementById('train'); if (!box || !window.PROBLEMS) return;
    var PS = LS.get('so:prob', {}), cur = null, hist = [], f = { lec: 'all', type: 'all', st: 'all' };
    var tsel = box.querySelector('#t-type'), lsel = box.querySelector('#t-lec'), ssel = box.querySelector('#t-st'), view = box.querySelector('#t-view'), stat = box.querySelector('#t-stat');
    (window.PTYPES || []).forEach(function (t) { var o = document.createElement('option'); o.value = t.id; o.setAttribute('data-lec', t.lec); o.innerHTML = t.lec + ' · ' + t.en + ' / ' + t.vi; tsel.appendChild(o); });
    if (/^#train-(L[123])$/.test(location.hash)) { f.lec = RegExp.$1; lsel.value = f.lec; }
    function pool() { return PROBLEMS.filter(function (p) { return (f.lec === 'all' || p.l === f.lec) && (f.type === 'all' || p.t === f.type) && (f.st === 'all' || (f.st === 'new' ? PS[p.id] === undefined : f.st === 'wrong' ? PS[p.id] === 0 : PS[p.id] === 1)); }); }
    function stats() { var r = 0, w = 0; PROBLEMS.forEach(function (p) { if (PS[p.id] === 1) r++; else if (PS[p.id] === 0) w++; }); stat.innerHTML = '<span lang="en">Solved ' + r + ' · to review ' + w + ' · of ' + PROBLEMS.length + '</span><span lang="vi">Đúng ' + r + ' · cần ôn ' + w + ' · trên ' + PROBLEMS.length + '</span>'; }
    function show(p) {
      cur = p; if (!p) { view.innerHTML = '<p>' + (lang() === 'vi' ? 'Không có bài nào trong bộ lọc này.' : 'No problem matches this filter.') + '</p>'; return; }
      var fl = p.f.map(function (x, i) { return '<label class="tf"><span>' + T(x.l) + ' (' + esc(x.u) + ')</span> <input type="text" inputmode="decimal" data-i="' + i + '" placeholder="?"> <span class="tfm" data-m="' + i + '"></span></label>'; }).join('');
      view.innerHTML = '<div class="tq"><span class="tag">' + p.l + '</span><span class="tag">' + p.id + '</span>' + (p.lv > 1 ? '<span class="tag red">' + (lang() === 'vi' ? 'khó hơn' : 'harder') + '</span>' : '') + '<p class="qverb">' + esc(T(p.q)) + '</p>' + fl +
        '<p><button type="button" class="btn t-check">' + (lang() === 'vi' ? 'Kiểm tra' : 'Check') + '</button> <button type="button" class="btn alt t-show">' + (lang() === 'vi' ? 'Hiện đáp án ngắn' : 'Show the short answer') + '</button> <button type="button" class="btn alt t-next">' + (lang() === 'vi' ? 'Bài khác ▶' : 'Another ▶') + '</button> <a class="pill" href="formulas.html#eq-' + p.e + '">' + (lang() === 'vi' ? 'công thức cần dùng →' : 'formula to use →') + '</a></p><div class="t-res"></div></div>';
      view.querySelector('.t-check').addEventListener('click', check); view.querySelector('.t-show').addEventListener('click', reveal); view.querySelector('.t-next').addEventListener('click', next);
      view.querySelectorAll('input').forEach(function (i) { i.addEventListener('keydown', function (e) { if (e.key === 'Enter') check(); }); });
    }
    function check() {
      if (!cur) return; var ok = 0, any = 0;
      cur.f.forEach(function (x, i) {
        var inp = view.querySelector('input[data-i="' + i + '"]'), m = view.querySelector('[data-m="' + i + '"]'), v = parseNum(inp.value); if (isNaN(v)) { m.textContent = ''; return; } any++;
        var good = x.a.some(function (a) { return Math.abs(v - a) <= 0.03 * Math.abs(a); }); if (good) ok++;
        m.textContent = good ? '✓' : '✗'; m.className = 'tfm ' + (good ? 'okm' : 'badm');
      });
      if (!any) return; var all = ok === cur.f.length; PS[cur.id] = all ? 1 : 0; LS.set('so:prob', PS); stats();
      view.querySelector('.t-res').innerHTML = '<div class="banner ' + (all ? 'ok' : 'no') + '">' + (all ? (lang() === 'vi' ? 'Đúng (sai số ≤ 3 %).' : 'Correct (within 3 %).') : (lang() === 'vi' ? 'Chưa đúng ở ' + (cur.f.length - ok) + ' ô. Kiểm lại đơn vị và quy ước, rồi bấm "Hiện đáp án ngắn".' : 'Not yet right in ' + (cur.f.length - ok) + ' field(s). Check units and convention, then "Show the short answer".')) + '</div>';
    }
    function reveal() {
      if (!cur) return;
      var rows = cur.f.map(function (x) { return '<li><b>' + T(x.l) + ':</b> ' + x.a.map(fmtN).join(' ' + (lang() === 'vi' ? 'hoặc' : 'or') + ' ') + ' ' + esc(x.u) + '</li>'; }).join('');
      view.querySelector('.t-res').innerHTML = '<div class="shortans"><b>' + (lang() === 'vi' ? 'Đáp án ngắn' : 'Short answer') + '</b><ul>' + rows + '</ul></div><details open><summary>' + (lang() === 'vi' ? 'Các bước' : 'Steps') + '</summary><ol>' + cur.s.map(function (x) { return '<li>' + esc(T(x)) + '</li>'; }).join('') + '</ol></details>';
    }
    function next() { var p = pool(); if (!p.length) { show(null); return; } var c; do { c = p[Math.floor(Math.random() * p.length)]; } while (p.length > 1 && cur && c.id === cur.id); show(c); }
    lsel.addEventListener('change', function () { f.lec = lsel.value; next(); }); tsel.addEventListener('change', function () { f.type = tsel.value; next(); }); ssel.addEventListener('change', function () { f.st = ssel.value; next(); });
    box.querySelector('#t-reset').addEventListener('click', function () { if (confirm(lang() === 'vi' ? 'Xóa tiến độ bài tập?' : 'Reset problem progress?')) { PS = {}; LS.set('so:prob', PS); stats(); next(); } });
    box._render = function () { show(cur); stats(); }; box.setAttribute('data-rerender', '1'); stats(); next();
  }

  /* ---------- explore: sliders and plots ---------- */
  function initExplore() {
    var box = document.getElementById('explore'); if (!box || !window.CALC) return; var C = CALC, K = C.K;
    function cv(id) { var c = document.getElementById(id), r = window.devicePixelRatio || 1, w = c.clientWidth || 600, h = +c.getAttribute('data-h') || 300; c.width = w * r; c.height = h * r; var x = c.getContext('2d'); x.setTransform(r, 0, 0, r, 0, 0); return { x: x, w: w, h: h }; }
    var css = getComputedStyle(document.documentElement); function col(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim() || '#888'; }
    function axes(c, xl, yl, x0, x1, y0, y1, logx, logy, xt, yt) {
      var x = c.x, W = c.w, H = c.h, L = 58, B = 40, Tp = 12, Rt = 12; x.fillStyle = col('--card'); x.fillRect(0, 0, W, H); x.strokeStyle = col('--line'); x.fillStyle = col('--mute'); x.font = '12px system-ui'; x.lineWidth = 1;
      var fx = function (v) { var a = logx ? Math.log10(v) : v, lo = logx ? Math.log10(x0) : x0, hi = logx ? Math.log10(x1) : x1; return L + (a - lo) / (hi - lo) * (W - L - Rt); };
      var fy = function (v) { var a = logy ? Math.log10(v) : v, lo = logy ? Math.log10(y0) : y0, hi = logy ? Math.log10(y1) : y1; return H - B - (a - lo) / (hi - lo) * (H - B - Tp); };
      (xt || []).forEach(function (t) { var px = fx(t); x.beginPath(); x.moveTo(px, Tp); x.lineTo(px, H - B); x.stroke(); x.textAlign = 'center'; x.fillText(logx ? '10^' + Math.round(Math.log10(t)) : String(t), px, H - B + 14); });
      (yt || []).forEach(function (t) { var py = fy(t); x.beginPath(); x.moveTo(L, py); x.lineTo(W - Rt, py); x.stroke(); x.textAlign = 'right'; x.fillText(logy ? '10^' + Math.round(Math.log10(t)) : String(t), L - 5, py + 4); });
      x.textAlign = 'center'; x.fillText(xl, (L + W - Rt) / 2, H - 6); x.save(); x.translate(13, (H - B + Tp) / 2); x.rotate(-Math.PI / 2); x.fillText(yl, 0, 0); x.restore();
      return { fx: fx, fy: fy };
    }
    function line(c, A, f, x0, x1, logx, color, lw) { var x = c.x, N = 160, st = true; x.strokeStyle = color; x.lineWidth = lw || 2.2; x.beginPath(); for (var i = 0; i <= N; i++) { var t = i / N, v = logx ? Math.pow(10, Math.log10(x0) + t * (Math.log10(x1) - Math.log10(x0))) : x0 + t * (x1 - x0); var y = f(v); if (!isFinite(y) || y <= 0 && A.logy) continue; var px = A.fx(v), py = A.fy(y); if (st) { x.moveTo(px, py); st = false; } else x.lineTo(px, py); } x.stroke(); }
    function dot(c, px, py, color) { c.x.fillStyle = color; c.x.beginPath(); c.x.arc(px, py, 6, 0, 7); c.x.fill(); c.x.strokeStyle = '#fff'; c.x.lineWidth = 2; c.x.stroke(); }
    function val(id) { return parseFloat(document.getElementById(id).value); }
    function lab(id, t) { document.getElementById(id).textContent = t; }
    // 1 free fall vs density
    function p1() {
      var lgn = val('e1-n'), mu = val('e1-mu'), n = Math.pow(10, lgn), c = cv('cv1'), A = axes(c, 'n (cm^-3)', 't_ff (Myr)', 1e1, 1e8, 0.01, 100, true, true, [1e2, 1e3, 1e4, 1e5, 1e6, 1e7], [0.01, 0.1, 1, 10, 100]);
      c.x.fillStyle = 'rgba(255,196,0,.25)'; c.x.fillRect(A.fx(1e3), 12, A.fx(1e4) - A.fx(1e3), c.h - 52); c.x.fillStyle = col('--mute'); c.x.fillText('exercise', (A.fx(1e3) + A.fx(1e4)) / 2, 26);
      line(c, { fx: A.fx, fy: A.fy, logy: true }, function (nn) { return C.tffSlide(C.rho(nn, mu)) / K.Myr; }, 1e1, 1e8, true, col('--blue')); line(c, { fx: A.fx, fy: A.fy, logy: true }, function (nn) { return C.tffFull(C.rho(nn, mu)) / K.Myr; }, 1e1, 1e8, true, col('--red'));
      var ts = C.tffSlide(C.rho(n, mu)) / K.Myr, tf = C.tffFull(C.rho(n, mu)) / K.Myr; dot(c, A.fx(n), A.fy(ts), col('--blue')); dot(c, A.fx(n), A.fy(tf), col('--red'));
      lab('e1-out', 'n = ' + fmtN(n) + ' cm⁻³ → t_ff slide = ' + fmtN(ts) + ' Myr (blue), exact = ' + fmtN(tf) + ' Myr (red)');
    }
    // 2 Jeans
    function p2() {
      var lgn = val('e2-n'), T = val('e2-T'), n = Math.pow(10, lgn), mu = 2.33, c = cv('cv2'), A = axes(c, 'n (cm^-3)', 'M_J (Msun, r = L_J/2)', 1e1, 1e8, 1e-3, 1e5, true, true, [1e2, 1e3, 1e4, 1e5, 1e6, 1e7], [1e-3, 1e-1, 1e1, 1e3, 1e5]);
      c.x.fillStyle = 'rgba(255,196,0,.25)'; c.x.fillRect(A.fx(1e3), 12, A.fx(1e4) - A.fx(1e3), c.h - 52);
      [[10, '#0e9aa7'], [30, '#3b6fd8'], [100, '#8e5bd0']].forEach(function (q) { line(c, { fx: A.fx, fy: A.fy, logy: true }, function (nn) { return C.MJ(q[0], mu, nn, 'rig', 'half') / K.Msun; }, 1e1, 1e8, true, q[1], 1.5); c.x.fillStyle = q[1]; c.x.fillText(q[0] + ' K', A.fx(2e7), A.fy(C.MJ(q[0], mu, 2e7, 'rig', 'half') / K.Msun) - 5); });
      var M = C.MJ(T, mu, n, 'rig', 'half') / K.Msun; dot(c, A.fx(n), A.fy(M), col('--red')); var L = C.LJ(T, mu, n, 'rig');
      lab('e2-out', 'n = ' + fmtN(n) + ' cm⁻³, T = ' + T + ' K → c_s = ' + fmtN(C.cs(T, mu) / 1e5) + ' km/s, L_J = ' + fmtN(L / K.pc) + ' pc (' + fmtN(L / K.AU) + ' AU), M_J = ' + fmtN(M) + ' Msun (r = L_J/2) or ' + fmtN(8 * M) + ' Msun (r = L_J)');
    }
    // 3 decay
    function p3() {
      var Th = val('e3-T'), dp = Math.pow(10, val('e3-dp')), c = cv('cv3'), tmax = 6 * Th, A = axes(c, 't (Gyr)', 'fraction', 0, tmax, 0, 1, false, false, [0, 1, 2, 3, 4, 5, 6].map(function (k) { return +(k * Th).toPrecision(3); }), [0, .25, .5, .75, 1]);
      line(c, { fx: A.fx, fy: A.fy }, function (t) { return C.parentFrac(t, Th); }, 0, tmax, false, col('--red')); line(c, { fx: A.fx, fy: A.fy }, function (t) { return 1 - C.parentFrac(t, Th); }, 0, tmax, false, col('--blue'));
      var t = C.ageFromDP(dp, Th); c.x.strokeStyle = col('--ok'); c.x.setLineDash([5, 4]); c.x.beginPath(); c.x.moveTo(A.fx(Math.min(t, tmax)), 12); c.x.lineTo(A.fx(Math.min(t, tmax)), c.h - 40); c.x.stroke(); c.x.setLineDash([]);
      c.x.fillStyle = col('--red'); c.x.fillText('parent', A.fx(tmax * 0.86), A.fy(C.parentFrac(tmax * .86, Th)) - 6); c.x.fillStyle = col('--blue'); c.x.fillText('daughter', A.fx(tmax * 0.86), A.fy(1 - C.parentFrac(tmax * .86, Th)) - 6);
      lab('e3-out', 'T½ = ' + Th + ' Gyr, D/P = ' + fmtN(dp) + ' → age t = T½ log₂(1 + D/P) = ' + fmtN(t) + ' Gyr (' + fmtN(t / Th) + ' half-lives); parent left = ' + fmtN(100 * C.parentFrac(t, Th)) + ' %');
    }
    // 4 Planck / Wien
    function p4() {
      var lgT = val('e4-T'), T = Math.pow(10, lgT), c = cv('cv4'), A = axes(c, 'wavelength (m)', 'B_λ / peak', 1e-12, 1e3, 1e-4, 1.2, true, true, [1e-12, 1e-9, 1e-6, 1e-3, 1], [1e-4, 1e-2, 1]);
      var bands = [['gamma', 1e-12, 1e-11, '#b3261e'], ['X', 1e-11, 1e-8, '#d9822b'], ['UV', 1e-8, 3.8e-7, '#8e5bd0'], ['vis', 3.8e-7, 7.5e-7, '#1f9d5c'], ['IR', 7.5e-7, 1e-3, '#c0392b'], ['µwave', 1e-3, 0.1, '#3b6fd8'], ['radio', 0.1, 1e3, '#0e9aa7']];
      bands.forEach(function (b) { c.x.fillStyle = b[3] + '33'; var a = A.fx(b[1]), z = A.fx(b[2]); c.x.fillRect(a, 12, z - a, c.h - 52); c.x.fillStyle = b[3]; c.x.save(); c.x.translate((a + z) / 2, 24); c.x.font = '11px system-ui'; c.x.textAlign = 'center'; c.x.fillText(b[0], 0, 0); c.x.restore(); });
      var h = K.h, cc = K.c / 100, kb = K.kB * 1e-7;                                    // SI
      var B = function (lam) { var x = h * cc / (lam * kb * T); return x > 700 ? 0 : 1 / (Math.pow(lam, 5) * (Math.exp(x) - 1)); }, lm = 2.897771955e-3 / T, pk = B(lm);
      line(c, { fx: A.fx, fy: A.fy, logy: true }, function (lam) { return Math.max(B(lam) / pk, 1e-9); }, 1e-12, 1e3, true, col('--fg'), 2.4); dot(c, A.fx(lm), A.fy(1), col('--red'));
      lab('e4-out', 'T = ' + fmtN(T) + ' K → peak λ = 2898 µm·K / T = ' + fmtN(lm) + ' m (' + C.band(lm) + '); ν = ' + fmtN(C.freq(lm)) + ' Hz; photon E = ' + fmtN(C.energyEV(lm)) + ' eV');
    }
    // 5 equilibrium temperature
    function p5() {
      var d = Math.pow(10, val('e5-d')), c = cv('cv5'), A = axes(c, 'd (AU)', 'T_eq (K)', 0.3, 100, 20, 500, true, true, [1, 10, 100], [20, 50, 100, 200, 500]);
      line(c, { fx: A.fx, fy: A.fy, logy: true }, function (dd) { return C.teq(dd); }, 0.3, 100, true, col('--blue'));
      c.x.strokeStyle = col('--red'); c.x.setLineDash([5, 4]); c.x.beginPath(); c.x.moveTo(A.fx(0.3), A.fy(150)); c.x.lineTo(A.fx(100), A.fy(150)); c.x.stroke(); c.x.setLineDash([]); c.x.fillStyle = col('--red'); c.x.fillText('150 K (water ice, our illustration)', A.fx(1.2), A.fy(150) - 5);
      dot(c, A.fx(d), A.fy(C.teq(d)), col('--red')); lab('e5-out', 'd = ' + fmtN(d) + ' AU → T_eq = ' + fmtN(C.teq(d)) + ' K (no albedo, no greenhouse; a trend only)');
    }
    var fns = [p1, p2, p3, p4, p5]; function all() { fns.forEach(function (f) { try { f(); } catch (e) { console.error(e); } }); }
    box.querySelectorAll('input[type=range]').forEach(function (r) { r.addEventListener('input', all); });
    box._render = all; box.setAttribute('data-rerender', '1'); all(); window.addEventListener('resize', all); document.querySelectorAll('[data-act=theme]').forEach(function (b) { b.addEventListener('click', function () { setTimeout(all, 50); }); });
  }

  /* ---------- annotated equations: coloured symbols, 'next symbol' stepper, table of meanings ---------- */
  function initEq() {
    document.querySelectorAll('.kx').forEach(function (el) {
      if (!window.katex) return;
      try { katex.render(el.getAttribute('data-tex'), el, { displayMode: !el.classList.contains('inl'), trust: true, throwOnError: false }); } catch (e) {}
    });
    document.querySelectorAll('.eqbig').forEach(function (box) {
      var rows = [].slice.call(box.querySelectorAll('tr.lr')), keys = rows.map(function (r) { return r.getAttribute('data-k'); }), cur = -1, info = box.querySelector('.eqinfo');
      function apply() {
        box.querySelectorAll('.ks').forEach(function (x) { x.classList.remove('on', 'dim'); });
        rows.forEach(function (r) { r.classList.remove('sel'); });
        if (cur < 0) { info.hidden = true; return; }
        var k = keys[cur];
        box.querySelectorAll('.ks').forEach(function (x) { x.classList.add(x.classList.contains('ks-' + k) ? 'on' : 'dim'); });
        var r = rows[cur]; r.classList.add('sel'); var c = r.children;
        info.innerHTML = '<div class="eqinfo-h">' + c[0].innerHTML + ' <b>' + c[1].innerHTML + '</b></div><p>' + c[2].innerHTML + '</p>' + (c[3].textContent.trim() ? '<p class="imp"><b>' + (lang() === 'vi' ? 'Hệ quả: ' : 'It implies: ') + '</b>' + c[3].innerHTML + '</p>' : '') + (c[4].textContent.trim() ? '<p class="vals"><b>' + (lang() === 'vi' ? 'Số gán: ' : 'Numbers: ') + '</b>' + c[4].innerHTML + '</p>' : '');
        info.hidden = false; if (window.renderMathInElement) renderMath();
      }
      box.querySelector('.eqnext').addEventListener('click', function () { cur = (cur + 1) % keys.length; apply(); });
      box.querySelector('.eqprev').addEventListener('click', function () { cur = cur <= 0 ? keys.length - 1 : cur - 1; apply(); });
      box.querySelector('.eqclear').addEventListener('click', function () { cur = -1; apply(); });
      rows.forEach(function (r, i) { r.addEventListener('click', function () { cur = i; apply(); }); });
      box.addEventListener('click', function (e) { var sp = e.target.closest('.ks'); if (sp) { var m = /ks-(\w+)/.exec(sp.className); var i = m ? keys.indexOf(m[1]) : -1; if (i >= 0) { cur = i; apply(); } } });
      box._render = apply; box.setAttribute('data-rerender', '1');
    });
  }

  /* ---------- self-check: 10 random questions of one lecture ---------- */
  function initSelfcheck() {
    document.querySelectorAll('.selfcheck').forEach(function (box) {
      if (!window.BANK) return; var lec = box.getAttribute('data-lec'), list = box.querySelector('.sc-list'), state = {};
      function draw() {
        var pool = BANK.filter(function (q) { return q.lec === lec; }), a = pool.slice();
        for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
        list._sel = a.slice(0, 10); render();
      }
      function render() { list.innerHTML = ''; (list._sel || []).forEach(function (q, i) { list.appendChild(renderQ(q, i, { num: i + 1, state: state, onAnswer: function (qq, ok) { PROG[qq.id] = ok ? 1 : 0; saveProg(); } })); }); }
      box.querySelector('.sc-new').addEventListener('click', function () { state = {}; draw(); });
      list._render = render; list.setAttribute('data-rerender', '1'); draw();
    });
  }

  /* ---------- lecture-slide viewer (arrow keys) ---------- */
  function initViewer() {
    document.querySelectorAll('.sviewer').forEach(function (box) {
      if (!window.SLIDES) return; var ids = JSON.parse(box.getAttribute('data-ids')), by = {}; SLIDES.forEach(function (s) { by[s.id] = s; }); var i = 0;
      var img = box.querySelector('img'), cap = box.querySelector('.sv-cap'), sel = box.querySelector('select');
      ids.forEach(function (id, k) { var o = document.createElement('option'); o.value = k; o.textContent = id.replace('-', ' p').replace(/p0/, 'p'); sel.appendChild(o); });
      function show() { var s = by[ids[i]]; if (!s) return; img.src = 'assets/slides/' + s.id + '.jpg'; img.setAttribute('data-zoom', 'assets/slides/' + s.id + '.jpg'); img.setAttribute('data-cap', 'Lecture slide ' + s.l + ' p' + s.p + ' · ' + (lang() === 'vi' ? s.vi : s.en)); cap.textContent = s.l + ' p' + s.p + ' · ' + (lang() === 'vi' ? s.vi : s.en); sel.value = i; }
      box.querySelector('.sv-prev').addEventListener('click', function () { i = (i + ids.length - 1) % ids.length; show(); });
      box.querySelector('.sv-next').addEventListener('click', function () { i = (i + 1) % ids.length; show(); });
      sel.addEventListener('change', function () { i = +sel.value; show(); });
      box.tabIndex = 0; box.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { i = (i + 1) % ids.length; show(); e.preventDefault(); } else if (e.key === 'ArrowLeft') { i = (i + ids.length - 1) % ids.length; show(); e.preventDefault(); } });
      box._render = show; box.setAttribute('data-rerender', '1'); show();
    });
  }

  /* ---------- written practice: remember which model answers were opened ---------- */
  function initWritten() {
    var done = LS.get('so:written', {});
    document.querySelectorAll('details.w').forEach(function (d) {
      var id = d.getAttribute('data-id'); var cb = d.querySelector('input[type=checkbox]'); if (!cb) return; cb.checked = !!done[id];
      cb.addEventListener('change', function () { done[id] = cb.checked; LS.set('so:written', done); count(); }); });
    function count() { ['w-count', 'ex-count'].forEach(function (id) { var el = document.getElementById(id); if (!el) return; var ds = [].slice.call(document.querySelectorAll('details.w[data-id]')); el.textContent = ds.filter(function (d) { return done[d.getAttribute('data-id')]; }).length + ' / ' + ds.length; }); }
    count();
  }
})();
