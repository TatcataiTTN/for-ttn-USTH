/* Ocean Optics calculators — run 100% in the browser.
   The pure-function part (OO) also runs in Node so it can be tested against Python (data/verified.json). */
(function (root) {
  var OO = {};
  OO.beer = function (c, L) { return Math.exp(-c * L); };
  OO.cFromT = function (T, L) { return -Math.log(T) / L; };
  var FORMS = { morel: { A: 1.38, e: -4.32, d: 0.09 }, buiteveld: { A: 1.29, e: -4.14, d: 0.051 } };
  OO.beta90 = function (lam, S, form) { var f = FORMS[form]; return f.A * Math.pow(lam / 500, f.e) * (1 + 0.3 * S / 37) * 1e-4; };
  OO.beta = function (theta, lam, S, form) { var f = FORMS[form], k = (1 - f.d) / (1 + f.d); return OO.beta90(lam, S, form) * (1 + Math.pow(Math.cos(theta), 2) * k); };
  OO.bw = function (lam, S, form) { var f = FORMS[form], k = (1 - f.d) / (1 + f.d); return 2 * Math.PI * OO.beta90(lam, S, form) * (2 + 2 * k / 3); };
  OO.bwNumeric = function (lam, S, form) { var n = 2000, s = 0, h = Math.PI / n; for (var i = 0; i < n; i++) { var th = (i + 0.5) * h; s += 2 * Math.PI * OO.beta(th, lam, S, form) * Math.sin(th) * h; } return s; };
  OO.expAbs = function (a0, S, lam0, lam) { return a0 * Math.exp(-S * (lam - lam0)); };
  OO.pkg = function (rho) { if (rho < 1e-6) return 1; return 1.5 * (1 + 2 * Math.exp(-rho) / rho + 2 * (Math.exp(-rho) - 1) / (rho * rho)) / rho; };
  OO.bpLaw = function (b550, n, lam) { return b550 * Math.pow(lam / 550, n); };
  OO.sumNs = function (rUm, N, Q) { var r = rUm * 1e-6; return N * Q * Math.PI * r * r; };
  OO.bpChl = function (chl) { return 0.30 * Math.pow(chl, 0.7); };
  OO.euphotic = function (Kd, frac) { return -Math.log(frac == null ? 0.01 : frac) / Kd; };
  OO.secchi = function (Kd, c, G) { return (G == null ? 8 : G) / (Kd + c); };
  OO.pocSpm = function (R) { return 0.0133 * Math.exp(1.27 * R); };
  OO.mix = function (S, af, as, Ss) { Ss = Ss == null ? 36 : Ss; return af * (1 - S / Ss) + as * (S / Ss); };
  OO.junge = function (xi) { return { gamma: xi - 3, n: -(xi - 3) }; };
  root.OO = OO;
  if (typeof document === 'undefined') { if (typeof module !== 'undefined') module.exports = OO; return; }
  function $(i) { return document.getElementById(i); }
  function val(i) { return parseFloat($(i).value); }
  function fmt(x, d) { if (!isFinite(x)) return '—'; var a = Math.abs(x); if (a !== 0 && (a < 1e-3 || a >= 1e5)) return x.toExponential(d == null ? 3 : d); return x.toFixed(d == null ? 3 : d).replace(/\.?0+$/, function (m) { return m.indexOf('.') === 0 && m.length > 1 ? '' : m; }); }
  function bind(ids, fn) { ids.forEach(function (i) { var e = $(i); if (e) { e.addEventListener('input', fn); e.addEventListener('change', fn); } }); fn(); }
  function plot(cv, series, o) {
    if (!cv) return; var ctx = cv.getContext('2d'), W = cv.width, H = cv.height, m = { l: 64, r: 16, t: 14, b: 44 }; ctx.clearRect(0, 0, W, H);
    var xs = [], ys = []; series.forEach(function (s) { s.x.forEach(function (v) { xs.push(v); }); s.y.forEach(function (v) { if (isFinite(v) && (!o.logy || v > 0)) ys.push(v); }); });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = o.ymin != null ? o.ymin : Math.min.apply(null, ys), y1 = o.ymax != null ? o.ymax : Math.max.apply(null, ys);
    if (o.logy) { y0 = Math.log10(y0); y1 = Math.log10(y1); } if (y1 === y0) y1 = y0 + 1;
    var X = function (v) { return m.l + (v - x0) / (x1 - x0 || 1) * (W - m.l - m.r); }, Y = function (v) { if (o.logy) v = Math.log10(v); return H - m.b - (v - y0) / (y1 - y0) * (H - m.t - m.b); };
    ctx.strokeStyle = '#999'; ctx.fillStyle = '#555'; ctx.font = '15px sans-serif'; ctx.strokeRect(m.l, m.t, W - m.l - m.r, H - m.t - m.b);
    for (var i = 0; i <= 4; i++) { var xv = x0 + (x1 - x0) * i / 4, yv = y0 + (y1 - y0) * i / 4; ctx.fillText(fmt(xv, 3), X(xv) - 16, H - m.b + 20); ctx.fillText(o.logy ? '1e' + Math.round(yv) : fmt(yv, 3), 4, Y(o.logy ? Math.pow(10, yv) : yv) + 5); }
    ctx.fillText(o.xl || '', W / 2 - 80, H - 8);
    series.forEach(function (s) { ctx.strokeStyle = s.c; ctx.fillStyle = s.c; if (s.dots) { s.x.forEach(function (v, k) { ctx.beginPath(); ctx.arc(X(v), Y(s.y[k]), 5, 0, 7); ctx.fill(); }); return; }
      ctx.lineWidth = 2.5; ctx.beginPath(); s.x.forEach(function (v, k) { if (k === 0) ctx.moveTo(X(v), Y(s.y[k])); else ctx.lineTo(X(v), Y(s.y[k])); }); ctx.stroke(); });
  }
  document.addEventListener('DOMContentLoaded', function () {
    if (!$('beer')) return;
    bind(['be_c', 'be_L', 'be_T'], function () { var c = val('be_c'), L = val('be_L'), T = OO.beer(c, L), c2 = OO.cFromT(val('be_T'), L);
      $('be_out').innerHTML = 'T = e<sup>−cL</sup> = <b>' + fmt(T, 4) + '</b> (' + fmt(T * 100, 2) + ' % of the beam remains). Reverse: T = ' + val('be_T') + ' over L = ' + L + ' m ⇒ c = −ln T/L = <b>' + fmt(c2, 4) + ' m⁻¹</b>';
      var xs = [], ys = []; for (var i = 0; i <= 60; i++) { var l = i * Math.max(L, 0.1) * 4 / 60; xs.push(l); ys.push(OO.beer(c, l)); }
      plot($('be_cv'), [{ x: xs, y: ys, c: '#273896' }, { x: [L], y: [T], c: '#ED1C24', dots: true }], { xl: 'path length (m)', ymin: 0, ymax: 1 }); });
    bind(['vw_l', 'vw_s', 'vw_f'], function () { var lam = val('vw_l'), S = val('vw_s'), f = $('vw_f').value;
      $('vw_out').innerHTML = 'β<sub>w</sub>(90°) = <b>' + fmt(OO.beta90(lam, S, f), 4) + ' m⁻¹ sr⁻¹</b>; b<sub>w</sub> = 2π∫β sinθ dθ = <b>' + fmt(OO.bw(lam, S, f), 4) + ' m⁻¹</b> (numerical integration: ' + fmt(OO.bwNumeric(lam, S, f), 4) + '); b<sub>bw</sub> = b<sub>w</sub>/2 = ' + fmt(OO.bw(lam, S, f) / 2, 4) + ' m⁻¹. Angular term read as cos²θ.';
      var xs = [], ys = []; for (var d = 0; d <= 180; d += 3) { xs.push(d); ys.push(OO.beta(d * Math.PI / 180, lam, S, f)); }
      plot($('vw_cv'), [{ x: xs, y: ys, c: '#273896' }], { xl: 'scattering angle (deg)', logy: true, ymin: 5e-5, ymax: 6e-3 }); });
    bind(['ea_a', 'ea_l0', 'ea_s', 'ea_l'], function () { var a = OO.expAbs(val('ea_a'), val('ea_s'), val('ea_l0'), val('ea_l'));
      $('ea_out').innerHTML = 'a(λ) = a(λ₀)·exp[−S(λ−λ₀)] = <b>' + fmt(a, 4) + ' m⁻¹</b>; ratio to a(λ₀) = ' + fmt(a / val('ea_a'), 4) + '; e-folding distance 1/S = <b>' + fmt(1 / val('ea_s'), 1) + ' nm</b>';
      var xs = [], ys = []; for (var l = 350; l <= 700; l += 10) { xs.push(l); ys.push(OO.expAbs(val('ea_a'), val('ea_s'), val('ea_l0'), l)); }
      plot($('ea_cv'), [{ x: xs, y: ys, c: '#273896' }, { x: [val('ea_l')], y: [a], c: '#ED1C24', dots: true }], { xl: 'wavelength (nm)', logy: true }); });
    bind(['pk_r'], function () { $('pk_out').innerHTML = 'Q*<sub>a</sub>(ρ = ' + val('pk_r') + ') = <b>' + fmt(OO.pkg(val('pk_r')), 4) + '</b> (1 = no package effect; → 0 = maximal)'; });
    bind(['bl_b', 'bl_n', 'bl_l'], function () { var n = val('bl_n');
      $('bl_out').innerHTML = 'b<sub>p</sub>(λ) = b<sub>p</sub>(550)·(λ/550)<sup>n</sup> = <b>' + fmt(OO.bpLaw(val('bl_b'), n, val('bl_l')), 4) + ' m⁻¹</b>. Junge link ξ = γ + 3: n = ' + n + ' ⇒ ξ ≈ <b>' + fmt(3 - n, 2) + '</b>';
      var xs = [], ys = []; for (var l = 400; l <= 700; l += 10) { xs.push(l); ys.push(OO.bpLaw(val('bl_b'), n, l)); }
      plot($('bl_cv'), [{ x: xs, y: ys, c: '#273896' }, { x: [val('bl_l')], y: [OO.bpLaw(val('bl_b'), n, val('bl_l'))], c: '#ED1C24', dots: true }], { xl: 'wavelength (nm)', ymin: 0 }); });
    bind(['sn_r', 'sn_n', 'sn_q'], function () { var c = OO.sumNs(val('sn_r'), val('sn_n'), val('sn_q')); $('sn_out').innerHTML = 'σ = Q·πr² = <b>' + fmt(val('sn_q') * Math.PI * Math.pow(val('sn_r') * 1e-6, 2), 3) + ' m²</b>; c = (N/V)·σ = <b>' + fmt(c, 4) + ' m⁻¹</b>'; });
    bind(['bc_chl'], function () { var b = OO.bpChl(val('bc_chl')); $('bc_out').innerHTML = 'b<sub>p</sub>(550) = 0.30·Chl<sup>0.7</sup> = <b>' + fmt(b, 4) + ' m⁻¹</b> (spread ≈ ×2–3: ' + fmt(b / 2.5, 3) + '–' + fmt(b * 2.5, 3) + '). A tenfold change in Chl changes b<sub>p</sub> by ' + fmt(Math.pow(10, 0.7), 3) + '×.'; });
    bind(['eu_k', 'eu_c', 'eu_g'], function () { var K = val('eu_k'); $('eu_out').innerHTML = '1 % light depth = 4.605/K<sub>d</sub> = <b>' + fmt(OO.euphotic(K), 3) + ' m</b>; penetration depth 1/K<sub>d</sub> = <b>' + fmt(1 / K, 3) + ' m</b>; Secchi z<sub>SD</sub> = Γ/(K<sub>d</sub>+c) = <b>' + fmt(OO.secchi(K, val('eu_c'), val('eu_g')), 3) + ' m</b>'; });
    bind(['pm_r'], function () { $('pm_out').innerHTML = 'POC/SPM = 0.0133·exp(1.27 R) = <b>' + fmt(OO.pocSpm(val('pm_r')), 4) + '</b> (Wozniak et al. 2010 regression, r² = 0.81)'; });
    bind(['mx_s', 'mx_f', 'mx_o'], function () { $('mx_out').innerHTML = 'Conservative mixing a(S) = a<sub>f</sub>(1 − S/36) + a<sub>o</sub>·S/36 = <b>' + fmt(OO.mix(val('mx_s'), val('mx_f'), val('mx_o')), 4) + ' m⁻¹</b>'; });
  });
})(typeof window !== 'undefined' ? window : globalThis);
