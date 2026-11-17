/* Interactive annotated equations: click a symbol -> it pops up with a frame, a callout box with an arrow appears (like the lecturer's slides),
   other symbols fade; callout shows name, unit, meaning, implication and the numbers assigned (with sources). "Plug in numbers" shows a worked example. */
(function () {
  var SVGNS = 'http://www.w3.org/2000/svg';
  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function init(box) {
    if (box.dataset.ready) return; box.dataset.ready = '1';
    var D = JSON.parse(box.querySelector('script.eqdata').textContent), order = D._order, cur = -1;
    var slideMode = !!box.closest('.mdeck-slide');
    var stage = box.querySelector('.eqstage'), svg = stage.querySelector('svg.eqarrows'), info = box.querySelector('.eqinfo'), plug = box.querySelector('.eqplug');
    var callout = null; setTimeout(fit, 30);
    function spans(k) { return [].slice.call(stage.querySelectorAll('.ks-' + k)).filter(function (s) { return !s.parentElement.closest('.ks-' + k); }); }
    function scaleOf() { var r = stage.getBoundingClientRect(); return stage.offsetWidth ? r.width / stage.offsetWidth : 1; }
    function rectOf(list) {
      var sr = stage.getBoundingClientRect(), sc = scaleOf(), x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      list.forEach(function (s) { var r = s.getBoundingClientRect(); x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); });
      return { x: (x0 - sr.left) / sc, y: (y0 - sr.top) / sc, w: (x1 - x0) / sc, h: (y1 - y0) / sc };
    }
    function clear() {
      [].forEach.call(stage.querySelectorAll('.ks'), function (s) { s.classList.remove('on', 'dim'); });
      [].forEach.call(stage.querySelectorAll('.ksframe'), function (f) { f.remove(); });
      if (callout) { callout.remove(); callout = null; }
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      stage.style.paddingTop = ''; stage.style.paddingBottom = '';
      [].forEach.call(box.querySelectorAll('tr.lr'), function (r) { r.classList.remove('sel'); });
      info.hidden = true; var idle = stage.querySelector('.eqidle'); if (idle) idle.hidden = false;
    }
    function textExtent(h) {   // real horizontal extent of the visible glyphs (ignores stretchy-svg strips and block widths)
      var l = 1e9, r = -1e9;
      [].forEach.call(h.querySelectorAll('*'), function (e) {
        if (e.children.length || !e.textContent.replace(/[\u200b\u00a0\s]/g, '')) return;
        var q = e.getBoundingClientRect(); if (!q.width) return; l = Math.min(l, q.left); r = Math.max(r, q.right);
      });
      return r > l ? (r - l) / scaleOf() : 0;
    }
    function fit() {
      var sl = stage.closest('.mdeck-slide'); if (!stage.offsetWidth || (sl && !sl.classList.contains('active'))) return;
      [].forEach.call(stage.querySelectorAll('.kx'), function (k) {
        k.style.fontSize = k.getAttribute('data-fs') ? k.getAttribute('data-fs') + 'px' : ''; var h = k.querySelector('.katex-html'); if (!h) return;
        var fs0 = parseFloat(getComputedStyle(k).fontSize), w = stage.clientWidth - 24, sw = textExtent(h);
        if (sw > w) k.style.fontSize = Math.max(16, fs0 * w / sw * 0.97) + 'px';
      });
    }
    function contentBox() {
      var sr = stage.getBoundingClientRect(), sc = scaleOf(), t = 1e9, bt = -1e9;
      [].forEach.call(stage.querySelectorAll('.kx'), function (k) { var r = k.getBoundingClientRect(); t = Math.min(t, r.top); bt = Math.max(bt, r.bottom); });
      return { top: (t - sr.top) / sc, bottom: (bt - sr.top) / sc };
    }
    function glyphRects() {
      var sr = stage.getBoundingClientRect(), sc = scaleOf(), out = [];
      [].forEach.call(stage.querySelectorAll('.katex-html *'), function (e) {
        if (e.children.length || !e.textContent.replace(/[\u200b\u00a0\s]/g, '')) return;
        var q = e.getBoundingClientRect(); if (q.width) out.push({ x: (q.left - sr.left) / sc, y: (q.top - sr.top) / sc, w: q.width / sc, h: q.height / sc });
      });
      return out;
    }
    function ov(a, b, m) { var w = Math.min(a.x + a.w, b.x + b.w + m) - Math.max(a.x, b.x - m), h = Math.min(a.y + a.h, b.y + b.h + m) - Math.max(a.y, b.y - m); return w > 0 && h > 0 ? w * h : 0; }
    function placeOnSlide(key, S, list) {
      var W = stage.offsetWidth, H = stage.offsetHeight, pad = 6, cw = W - 16;
      callout.style.width = cw + 'px'; callout.classList.add('bottom');
      var ch = callout.offsetHeight, cb = { bottom: Math.max.apply(null, glyphRects().map(function (g) { return g.y + g.h; }).concat([0])) };
      for (var it = 0; it < 6 && H - ch - 6 < cb.bottom + 12; it++) { stage.style.paddingBottom = (parseFloat(getComputedStyle(stage).paddingBottom) + (cb.bottom + 12 - (H - ch - 6))) + 'px'; H = stage.offsetHeight; }
      var cy = H - ch - 6, cx = 8;
      callout.style.left = cx + 'px'; callout.style.top = cy + 'px';
      var rects = list.map(function (s) { return rectOf([s]); });
      rects.forEach(function (R) { var fr = el('div', 'ksframe'); fr.style.cssText = 'left:' + (R.x - pad) + 'px;top:' + (R.y - pad) + 'px;width:' + (R.w + 2 * pad) + 'px;height:' + (R.h + 2 * pad) + 'px;border-color:' + S.color; stage.appendChild(fr); });
      svg.setAttribute('width', W); svg.setAttribute('height', H);
      var id = 'ah' + box.dataset.eq + key, defs = document.createElementNS(SVGNS, 'defs'), mk = document.createElementNS(SVGNS, 'marker');
      mk.setAttribute('id', id); mk.setAttribute('viewBox', '0 0 10 10'); mk.setAttribute('refX', '9'); mk.setAttribute('refY', '5'); mk.setAttribute('markerWidth', '7'); mk.setAttribute('markerHeight', '7'); mk.setAttribute('orient', 'auto');
      var p = document.createElementNS(SVGNS, 'path'); p.setAttribute('d', 'M0,0 L10,5 L0,10 z'); p.setAttribute('fill', S.color); mk.appendChild(p); defs.appendChild(mk); svg.appendChild(defs);
      rects.forEach(function (R, n) {
        var ex = R.x + R.w / 2, ey = R.y + R.h + pad + 3, sx = Math.max(cx + 40, Math.min(ex, cx + cw - 40)), sy = cy, my = (sy + ey) / 2;
        var path = document.createElementNS(SVGNS, 'path'); path.setAttribute('d', 'M' + sx + ',' + sy + ' C' + sx + ',' + my + ' ' + ex + ',' + my + ' ' + ex + ',' + ey);
        path.setAttribute('fill', 'none'); path.setAttribute('stroke', S.color); path.setAttribute('stroke-width', n ? 2.2 : 3.6); if (n) path.setAttribute('stroke-dasharray', '6 5');
        path.setAttribute('marker-end', 'url(#' + id + ')'); svg.appendChild(path);
      });
    }
    function select(i) {
      clear(); fit(); cur = i; var idl = stage.querySelector('.eqidle'); if (idl) idl.hidden = true; var k = order[i], S = D[k], list = spans(k); if (!list.length) return; var key = k;
      [].forEach.call(stage.querySelectorAll('.ks'), function (s) { s.classList.add('dim'); });
      list.forEach(function (s) { s.classList.remove('dim'); s.classList.add('on'); [].forEach.call(s.querySelectorAll('.ks'), function (q) { q.classList.remove('dim'); }); });
      var row = box.querySelector('tr.lr[data-k="' + k + '"]'); if (row) row.classList.add('sel');
      var vals = (S.values || []).map(function (v) { return '<li>' + esc(v[0]) + ': <b>' + esc(v[1]) + '</b> <small>(' + esc(v[2]) + ')</small></li>'; }).join('');
      callout = el('div', 'eqcall', '<div class="ch" style="background:' + S.color + '">' + esc(S.name) + (S.unit ? ' <span>[' + esc(S.unit) + ']</span>' : '') + '</div><div class="cb"><div class="cm"><p>' + esc(S.meaning) + '</p>' +
        (S.implication ? '<p class="imp">→ ' + esc(S.implication) + '</p>' : '') + '</div>' + (vals ? '<div class="cv"><b>Numbers assigned</b><ul>' + vals + '</ul></div>' : '') + '</div>');
      callout.style.borderColor = S.color; stage.appendChild(callout);
      var cw = Math.min(slideMode ? 600 : 460, stage.offsetWidth - 16); callout.style.width = cw + 'px';
      if (slideMode) return placeOnSlide(key, S, list);
      var ch = callout.offsetHeight, gap = slideMode ? 60 : 50, base = slideMode ? 18 : 24, pad = 6;
      var R0 = rectOf([list[0]]), cb0 = contentBox(), firstLine = R0.y + R0.h / 2 < cb0.top + (cb0.bottom - cb0.top) * (box.dataset.single ? 2 : 0.4);
      stage.style.paddingTop = (firstLine ? base + ch + gap : base) + 'px'; stage.style.paddingBottom = (firstLine ? base : base + ch + gap) + 'px';
      var cb = contentBox(); R0 = rectOf([list[0]]);
      // one frame per occurrence
      var rects = list.map(function (s) { return rectOf([s]); });
      rects.forEach(function (R) { var fr = el('div', 'ksframe'); fr.style.cssText = 'left:' + (R.x - pad) + 'px;top:' + (R.y - pad) + 'px;width:' + (R.w + 2 * pad) + 'px;height:' + (R.h + 2 * pad) + 'px;border-color:' + S.color; stage.appendChild(fr); });
      var cx = Math.max(8, Math.min(R0.x + R0.w / 2 - cw / 2, stage.offsetWidth - cw - 8)), cy = firstLine ? cb.top - gap - ch : cb.bottom + gap;
      callout.style.left = cx + 'px'; callout.style.top = cy + 'px';
      svg.setAttribute('width', stage.offsetWidth); svg.setAttribute('height', stage.scrollHeight || stage.offsetHeight);
      var id = 'ah' + box.dataset.eq + i, defs = document.createElementNS(SVGNS, 'defs'), mk = document.createElementNS(SVGNS, 'marker');
      mk.setAttribute('id', id); mk.setAttribute('viewBox', '0 0 10 10'); mk.setAttribute('refX', '9'); mk.setAttribute('refY', '5'); mk.setAttribute('markerWidth', '7'); mk.setAttribute('markerHeight', '7'); mk.setAttribute('orient', 'auto');
      var p = document.createElementNS(SVGNS, 'path'); p.setAttribute('d', 'M0,0 L10,5 L0,10 z'); p.setAttribute('fill', S.color); mk.appendChild(p); defs.appendChild(mk); svg.appendChild(defs);
      rects.forEach(function (R, n) {   // an arrow from the callout to every occurrence (solid to the first, thinner to the others)
        var sx = Math.max(cx + 22, Math.min(R.x + R.w / 2, cx + cw - 22)), sy = firstLine ? cy + ch : cy, ex = R.x + R.w / 2, ey = firstLine ? R.y - pad - 2 : R.y + R.h + pad + 2;
        var path = document.createElementNS(SVGNS, 'path'), my = (sy + ey) / 2;
        path.setAttribute('d', 'M' + sx + ',' + sy + ' C' + sx + ',' + my + ' ' + ex + ',' + my + ' ' + ex + ',' + ey);
        path.setAttribute('fill', 'none'); path.setAttribute('stroke', S.color); path.setAttribute('stroke-width', n ? 1.8 : (slideMode ? 3 : 2.6)); if (n) path.setAttribute('stroke-dasharray', '5 4');
        path.setAttribute('marker-end', 'url(#' + id + ')'); svg.appendChild(path);
      });
      if (!slideMode) callout.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    function showAll() { clear(); cur = -1; plug.hidden = true; }
    // clicks on symbols and rows
    order.forEach(function (k, i) {
      spans(k).forEach(function (s) { s.addEventListener('click', function (ev) { ev.stopPropagation(); select(i); }); });
      var row = box.querySelector('tr.lr[data-k="' + k + '"]'); if (row) row.addEventListener('click', function () { select(i); });
    });
    stage.addEventListener('click', function (ev) { if (ev.target === stage) showAll(); });
    var pv = box.querySelector('.eqprev'), nx = box.querySelector('.eqnext'), cl = box.querySelector('.eqclear'), pb = box.querySelector('.eqplugbtn');
    if (nx) nx.onclick = function () { select((cur + 1) % order.length); };
    if (pv) pv.onclick = function () { select((cur - 1 + order.length) % order.length); };
    if (cl) cl.onclick = showAll;
    if (pb) pb.onclick = function () {
      if (!plug.hidden) { plug.hidden = true; return; }
      plug.innerHTML = '<b>Plug in numbers</b>' + D._example.map(function (t, i) { return '<div class="kx" data-tex="' + t.replace(/&/g, '&amp;').replace(/"/g, '&quot;') + '"></div>'; }).join('');
      plug.hidden = false; document.dispatchEvent(new Event('kx-run'));
      [].forEach.call(plug.querySelectorAll('.kx'), function (e) { try { katex.render(e.getAttribute('data-tex'), e, { displayMode: true, throwOnError: false, trust: true, strict: false }); } catch (x) {} });
    };
    box._fit = fit;
    window.addEventListener('resize', function () { if (cur >= 0) select(cur); else fit(); });
  }
  var mo = typeof MutationObserver !== 'undefined' && new MutationObserver(function (ms) { ms.forEach(function (m) { var s = m.target; if (s.classList && s.classList.contains('active')) [].forEach.call(s.querySelectorAll('.eqbig'), function (b) { if (b._fit) setTimeout(b._fit, 20); }); }); });
  function watch() { if (mo) [].forEach.call(document.querySelectorAll('.mdeck-slide'), function (s) { mo.observe(s, { attributes: true, attributeFilter: ['class'] }); }); }
  function all() { watch(); [].forEach.call(document.querySelectorAll('.eqbig'), init); }
  document.addEventListener('kx-ready', all);
  if (document.readyState !== 'loading') setTimeout(all, 50);
})();
