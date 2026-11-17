/* Renders every .kx element with KaTeX (display math from data-tex; .kx.inl = inline). Content is our own, so trust:true (needed for \htmlClass). */
(function () {
  function run() {
    if (typeof katex === 'undefined') return false;
    [].forEach.call(document.querySelectorAll('.kx'), function (el) {
      if (el.dataset.done) return;
      try { katex.render(el.getAttribute('data-tex'), el, { displayMode: !el.classList.contains('inl'), throwOnError: false, trust: true, strict: false }); el.dataset.done = '1'; } catch (e) {}
    });
    document.dispatchEvent(new Event('kx-ready'));
    return true;
  }
  function go() { if (!run()) window.addEventListener('load', function () { run(); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
/* auto-fit for static big formulas in narrow columns (.kx.fit) */
(function () {
  function extent(h) { var l = 1e9, r = -1e9; [].forEach.call(h.querySelectorAll('*'), function (e) { if (e.children.length || !e.textContent.replace(/[​ \s]/g, '')) return; var q = e.getBoundingClientRect(); if (!q.width) return; l = Math.min(l, q.left); r = Math.max(r, q.right); }); return r > l ? r - l : 0; }
  function fitAll() {
    [].forEach.call(document.querySelectorAll('.kx.fit'), function (k) {
      var sl = k.closest('.mdeck-slide'); if (!k.offsetWidth || (sl && !sl.classList.contains('active'))) return;
      k.style.fontSize = ''; var h = k.querySelector('.katex-html'); if (!h) return;
      var fs0 = parseFloat(getComputedStyle(k).fontSize), w = k.parentElement.clientWidth - 12, sc = k.getBoundingClientRect().width / (k.offsetWidth || 1), sw = extent(h) / (sc || 1);
      if (sw > w) k.style.fontSize = Math.max(18, fs0 * w / sw * 0.97) + 'px';
    });
  }
  document.addEventListener('kx-ready', function () { fitAll(); setTimeout(fitAll, 120);
    if (typeof MutationObserver !== 'undefined') { var mo = new MutationObserver(function (ms) { ms.forEach(function (m) { if (m.target.classList.contains('active')) setTimeout(fitAll, 30); }); });
      [].forEach.call(document.querySelectorAll('.mdeck-slide'), function (s) { mo.observe(s, { attributes: true, attributeFilter: ['class'] }); }); } });
  window.addEventListener('resize', fitAll);
})();
