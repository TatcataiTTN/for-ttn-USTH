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
