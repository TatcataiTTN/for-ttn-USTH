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
    initBig12(); initPractice(); initExam(); initCalcs(); initGallery(); initWritten(); progressBadges();
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

  /* ---------- written practice: remember which model answers were opened ---------- */
  function initWritten() {
    var done = LS.get('so:written', {});
    document.querySelectorAll('details.w').forEach(function (d) {
      var id = d.getAttribute('data-id'); var cb = d.querySelector('input[type=checkbox]'); if (!cb) return; cb.checked = !!done[id];
      cb.addEventListener('change', function () { done[id] = cb.checked; LS.set('so:written', done); count(); }); });
    function count() { var el = document.getElementById('w-count'); if (el) el.textContent = Object.keys(done).filter(function (k) { return done[k]; }).length + ' / ' + document.querySelectorAll('details.w').length; }
    count();
  }
})();
