/* Atmospheric Remote Sensing calculators — run 100% in the browser.
   The pure-function part (ARS) also runs in Node so it can be tested against Python (data/verified.json). */
(function (root) {
  var H = 6.62607015e-34, C = 2.99792458e8, KB = 1.380649e-23, DEG = Math.PI / 180;
  var ARS = {};
  ARS.lifetime = function (k, oh) { var t = 1 / (k * oh); return { tau_s: t, tau_days: t / 86400 }; };
  ARS.parallel = function (taus) { var s = 0; taus.forEach(function (t) { s += 1 / t; }); return 1 / s; };
  ARS.plume = function (U, Lkm) { var t = Lkm * 1000 / U; return { tau_s: t, tau_h: t / 3600 }; };
  ARS.decay = function (tOverTau) { return Math.exp(-tOverTau); };
  ARS.beer = function (tauV, szaDeg) { var ts = tauV / Math.cos(szaDeg * DEG); return { tau_slant: ts, T: Math.exp(-ts) }; };
  ARS.planck = function (lamUm, T) { var l = lamUm * 1e-6; return 2 * H * C * C / Math.pow(l, 5) / (Math.exp(H * C / (l * KB * T)) - 1); }; // W m-2 sr-1 m-1
  ARS.planckInv = function (lamUm, B) { var l = lamUm * 1e-6; return H * C / (l * KB) / Math.log(1 + 2 * H * C * C / (Math.pow(l, 5) * B)); };
  ARS.wien = function (T) { return 2898 / T; };
  ARS.stefan = function (T) { return 5.670374419e-8 * Math.pow(T, 4); };
  ARS.amf = function (szaDeg, vzaDeg) { return 1 / Math.cos(szaDeg * DEG) + 1 / Math.cos(vzaDeg * DEG); };
  ARS.doas = function (sza, vza, scd, scdStrat) { var a = ARS.amf(sza, vza); var v = (scd - scdStrat) / a; return { amf: a, vcd: v, du: v / 2.687e16 }; };
  ARS.angstrom = function (t1, l1, t2, l2) { return Math.log(t1 / t2) / Math.log(l2 / l1); };
  ARS.aodAt = function (t1, l1, alpha, l) { return t1 * Math.pow(l / l1, -alpha); };
  ARS.size = function (rUm, lamUm) {
    var x = 2 * Math.PI * rUm / lamUm, reg;
    if (x < 0.1) reg = 'Rayleigh'; else if (x <= 50) reg = 'Mie'; else if (x <= 100) reg = 'upper Mie (approaching geometric optics)'; else reg = 'Geometric optics';
    return { x: x, regime: reg };
  };
  ARS.tir = function (Ts, zKm, tau, lapse, lamUm) {
    lamUm = lamUm || 10; lapse = lapse == null ? 6.5 : lapse;
    var Tl = Ts - lapse * zKm;
    var I = ARS.planck(lamUm, Ts) * Math.exp(-tau) + ARS.planck(lamUm, Tl) * (1 - Math.exp(-tau));
    var bt = ARS.planckInv(lamUm, I);
    return { Tl: Tl, BT: bt, dBT: Ts - bt };
  };
  function matInv(M) {
    var n = M.length, A = M.map(function (r, i) { return r.slice().concat(Array.apply(null, Array(n)).map(function (_, j) { return i === j ? 1 : 0; })); });
    for (var c = 0; c < n; c++) {
      var p = c; for (var r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      var t = A[c]; A[c] = A[p]; A[p] = t;
      var d = A[c][c]; for (var j = 0; j < 2 * n; j++) A[c][j] /= d;
      for (var r2 = 0; r2 < n; r2++) if (r2 !== c) { var f = A[r2][c]; if (f) for (var j2 = 0; j2 < 2 * n; j2++) A[r2][j2] -= f * A[c][j2]; }
    }
    return A.map(function (r) { return r.slice(n); });
  }
  function mul(A, B) { var n = A.length, m = B[0].length, k = B.length, R = []; for (var i = 0; i < n; i++) { R[i] = []; for (var j = 0; j < m; j++) { var s = 0; for (var l = 0; l < k; l++) s += A[i][l] * B[l][j]; R[i][j] = s; } } return R; }
  function tr(A) { return A[0].map(function (_, j) { return A.map(function (r) { return r[j]; }); }); }
  ARS.ak = function (N, w, se, sa, Lc) {
    var K = [], Sa = [], i, j;
    for (i = 0; i < N; i++) { K[i] = []; Sa[i] = []; for (j = 0; j < N; j++) { K[i][j] = Math.exp(-0.5 * Math.pow((j - i) / w, 2)); Sa[i][j] = sa * sa * Math.exp(-Math.abs(i - j) / Lc); } }
    var Kt = tr(K), KtK = mul(Kt, K).map(function (r) { return r.map(function (v) { return v / (se * se); }); });
    var Sai = matInv(Sa), M = KtK.map(function (r, a) { return r.map(function (v, b) { return v + Sai[a][b]; }); });
    var G = mul(matInv(M), Kt.map(function (r) { return r.map(function (v) { return v / (se * se); }); }));
    var A = mul(G, K), d = 0; for (i = 0; i < N; i++) d += A[i][i];
    return { A: A, dofs: d };
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = ARS;
  root.ARS = ARS;
  if (typeof document === 'undefined') return;

  /* ---------------- user interface ---------------- */
  function fmt(x, d) { if (!isFinite(x)) return '—'; d = d == null ? 3 : d;
    if (x !== 0 && (Math.abs(x) >= 1e5 || Math.abs(x) < 1e-3)) { var p = x.toExponential(d).split('e'); return p[0] + '×10<sup>' + String(parseInt(p[1], 10)).replace('-', '−') + '</sup>'; }
    return x.toFixed(d); }
  function $(id) { return document.getElementById(id); }
  function val(id) { return parseFloat($(id).value); }
  function bind(ids, fn) { ids.forEach(function (i) { var e = $(i); if (e) { e.addEventListener('input', fn); e.addEventListener('change', fn); } }); fn(); }
  function plot(cv, series, o) {
    var ctx = cv.getContext('2d'), W = cv.width, Hh = cv.height, m = { l: 62, r: 14, t: 16, b: 40 };
    ctx.clearRect(0, 0, W, Hh); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, Hh);
    var xs = [], ys = []; series.forEach(function (s) { s.x.forEach(function (v, i) { xs.push(v); ys.push(s.y[i]); }); });
    var x0 = o.xmin != null ? o.xmin : Math.min.apply(null, xs), x1 = o.xmax != null ? o.xmax : Math.max.apply(null, xs);
    var y0 = o.ymin != null ? o.ymin : Math.min.apply(null, ys), y1 = o.ymax != null ? o.ymax : Math.max.apply(null, ys);
    var fx = function (v) { var a = o.logx ? Math.log(v) : v, b0 = o.logx ? Math.log(x0) : x0, b1 = o.logx ? Math.log(x1) : x1; return m.l + (a - b0) / (b1 - b0) * (W - m.l - m.r); };
    var fy = function (v) { var a = o.logy ? Math.log(v) : v, b0 = o.logy ? Math.log(y0) : y0, b1 = o.logy ? Math.log(y1) : y1; return Hh - m.b - (a - b0) / (b1 - b0) * (Hh - m.t - m.b); };
    ctx.strokeStyle = '#d5dae6'; ctx.fillStyle = '#566074'; ctx.font = '13px sans-serif'; ctx.lineWidth = 1;
    for (var k = 0; k <= 4; k++) {
      var gx = x0 + (x1 - x0) * k / 4, gy = y0 + (y1 - y0) * k / 4;
      if (o.logx) gx = Math.exp(Math.log(x0) + (Math.log(x1) - Math.log(x0)) * k / 4);
      if (o.logy) gy = Math.exp(Math.log(y0) + (Math.log(y1) - Math.log(y0)) * k / 4);
      ctx.beginPath(); ctx.moveTo(fx(gx), m.t); ctx.lineTo(fx(gx), Hh - m.b); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(m.l, fy(gy)); ctx.lineTo(W - m.r, fy(gy)); ctx.stroke();
      ctx.textAlign = 'center'; ctx.fillText(+gx.toPrecision(3), fx(gx), Hh - m.b + 16);
      ctx.textAlign = 'right'; ctx.fillText(+gy.toPrecision(3), m.l - 6, fy(gy) + 4);
    }
    ctx.textAlign = 'center'; ctx.fillText(o.xl || '', (W + m.l) / 2, Hh - 6);
    ctx.save(); ctx.translate(14, (Hh - m.b + m.t) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText(o.yl || '', 0, 0); ctx.restore();
    series.forEach(function (s) {
      ctx.strokeStyle = s.c; ctx.lineWidth = 2.2; ctx.beginPath();
      s.x.forEach(function (v, i) { var X = fx(v), Y = fy(s.y[i]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }); ctx.stroke();
      if (s.dots) s.x.forEach(function (v, i) { ctx.fillStyle = s.c; ctx.beginPath(); ctx.arc(fx(v), fy(s.y[i]), 4, 0, 6.3); ctx.fill(); });
    });
    var lx = m.l + 10; series.forEach(function (s) { if (!s.n) return; ctx.fillStyle = s.c; ctx.textAlign = 'left'; ctx.fillRect(lx, m.t + 4, 16, 4); ctx.fillText(s.n, lx + 22, m.t + 10); lx += 28 + ctx.measureText(s.n).width + 10; });
  }
  document.addEventListener('DOMContentLoaded', function () {
    if (!$('lifetime')) return;
    bind(['lt_k', 'lt_oh', 'lt_t1', 'lt_t2', 'lt_t3'], function () {
      var r = ARS.lifetime(val('lt_k'), val('lt_oh')), p = ARS.parallel([val('lt_t1'), val('lt_t2'), val('lt_t3')]);
      $('lt_out').innerHTML = 'τ<sub>chem</sub> = 1/(k·[OH]) = <b>' + fmt(r.tau_s, 3) + ' s</b> = <b>' + fmt(r.tau_days, 2) + ' days</b> (half-life t<sub>½</sub> = τ ln 2 = ' + fmt(r.tau_days * Math.LN2, 2) + ' days)<br>Three parallel sinks: 1/τ = Σ 1/τ<sub>i</sub> ⇒ τ = <b>' + fmt(p, 3) + '</b> days (shorter than the fastest single sink)';
    });
    bind(['pl_U', 'pl_L'], function () { var r = ARS.plume(val('pl_U'), val('pl_L')); $('pl_out').innerHTML = 'τ = L/U = <b>' + fmt(r.tau_s, 0) + ' s</b> = <b>' + fmt(r.tau_h, 2) + ' h</b>. Range for NO₂ in the study guide: 2–6 h — ' + (r.tau_h >= 2 && r.tau_h <= 6 ? 'inside the range.' : 'outside the range.');
      var xs = [], ys = [], L = val('pl_L'); for (var i = 0; i <= 60; i++) { var x = i * L * 3 / 60; xs.push(x); ys.push(Math.exp(-x / L)); }
      plot($('pl_cv'), [{ x: xs, y: ys, c: '#273896', n: 'C(x)/C₀' }], { xl: 'distance downwind (km)', yl: 'C/C₀', ymin: 0, ymax: 1 }); });
    bind(['be_tau', 'be_sza'], function () { var r = ARS.beer(val('be_tau'), val('be_sza'));
      $('be_out').innerHTML = 'τ<sub>slant</sub> = τ/cos θ = <b>' + fmt(r.tau_slant, 3) + '</b> ⇒ T = e<sup>−τ</sup> = <b>' + fmt(r.T, 4) + '</b> (' + fmt(r.T * 100, 1) + '% of the direct beam is transmitted)';
      var xs = [], ys = []; for (var i = 0; i <= 80; i++) { var s = i * 85 / 80; xs.push(s); ys.push(Math.exp(-val('be_tau') / Math.cos(s * DEG))); }
      plot($('be_cv'), [{ x: xs, y: ys, c: '#ED1C24', n: 'T vs zenith angle' }, { x: [val('be_sza')], y: [r.T], c: '#273896', dots: true }], { xl: 'solar zenith angle (deg)', yl: 'transmittance T', ymin: 0, ymax: 1 }); });
    bind(['pk_T', 'pk_lam'], function () { var T = val('pk_T'), lam = val('pk_lam');
      $('pk_out').innerHTML = 'Wien: λ<sub>max</sub> = 2898/T = <b>' + fmt(ARS.wien(T), 3) + ' µm</b> · Stefan–Boltzmann: M = σT⁴ = <b>' + fmt(ARS.stefan(T), 1) + ' W m⁻²</b> · B(' + fmt(lam, 2) + ' µm) = <b>' + fmt(ARS.planck(lam, T) * 1e-6, 4) + ' W m⁻² sr⁻¹ µm⁻¹</b>';
      var xs = [], ys = [], lm = ARS.wien(T); for (var i = 0; i <= 120; i++) { var l = lm * 0.25 * Math.pow(60, i / 120); xs.push(l); ys.push(ARS.planck(l, T) * 1e-6); }
      plot($('pk_cv'), [{ x: xs, y: ys, c: '#ED1C24', n: 'B(λ,T)' }, { x: [lm], y: [ARS.planck(lm, T) * 1e-6], c: '#273896', dots: true }], { xl: 'wavelength (µm), log scale', yl: 'B (W m⁻² sr⁻¹ µm⁻¹)', logx: true, ymin: 0 }); });
    bind(['do_sza', 'do_vza', 'do_scd', 'do_str'], function () { var r = ARS.doas(val('do_sza'), val('do_vza'), val('do_scd') * 1e15, val('do_str') * 1e15);
      $('do_out').innerHTML = 'AMF ≈ 1/cos θ₀ + 1/cos θ = <b>' + fmt(r.amf, 4) + '</b> ⇒ VCD = (SCD − SCD<sub>strat</sub>)/AMF = <b>' + fmt(r.vcd, 3) + ' molecule cm⁻²</b> = <b>' + fmt(r.du, 4) + ' DU</b> (1 DU = 2.687×10¹⁶ molecule cm⁻²)'; });
    bind(['an_t1', 'an_l1', 'an_t2', 'an_l2', 'an_lq'], function () { var a = ARS.angstrom(val('an_t1'), val('an_l1'), val('an_t2'), val('an_l2'));
      var cls = a < 0.5 ? 'coarse particles (dust, sea salt)' : (a >= 1.5 ? 'fine particles (smoke, urban, sulfate)' : 'mixed / intermediate');
      $('an_out').innerHTML = 'α = ln(τ₁/τ₂)/ln(λ₂/λ₁) = <b>' + fmt(a, 3) + '</b> ⇒ ' + cls + '. AOD(' + val('an_lq') + ' nm) = <b>' + fmt(ARS.aodAt(val('an_t1'), val('an_l1'), a, val('an_lq')), 3) + '</b>';
      var xs = [], ys = []; for (var l = 350; l <= 1100; l += 25) { xs.push(l); ys.push(ARS.aodAt(val('an_t1'), val('an_l1'), a, l)); }
      plot($('an_cv'), [{ x: xs, y: ys, c: '#273896', n: 'AOD(λ)' }, { x: [val('an_l1'), val('an_l2')], y: [val('an_t1'), val('an_t2')], c: '#ED1C24', dots: true }], { xl: 'wavelength (nm)', yl: 'AOD', ymin: 0 }); });
    bind(['sz_r', 'sz_lam'], function () { var r = ARS.size(val('sz_r'), val('sz_lam'));
      $('sz_out').innerHTML = 'x = 2πr/λ = <b>' + fmt(r.x, 4) + '</b> ⇒ regime: <b>' + r.regime + '</b>. In the Rayleigh regime: doubling r ⇒ σ ×64; halving λ ⇒ σ ×16.'; });
    bind(['ti_Ts', 'ti_tau', 'ti_lap'], function () { var Ts = val('ti_Ts'), tau = val('ti_tau'), lap = val('ti_lap');
      var xs = [], ys = []; for (var z = 0; z <= 12; z += 0.5) { xs.push(z); ys.push(ARS.tir(Ts, z, tau, lap, 10).dBT); }
      var a = ARS.tir(Ts, 1, tau, lap, 10), b = ARS.tir(Ts, 5, tau, lap, 10);
      $('ti_out').innerHTML = 'Layer at 1 km: T<sub>layer</sub> = ' + fmt(a.Tl, 1) + ' K, BT = ' + fmt(a.BT, 2) + ' K ⇒ ΔBT = <b>' + fmt(a.dBT, 2) + ' K</b><br>Layer at 5 km: T<sub>layer</sub> = ' + fmt(b.Tl, 1) + ' K, BT = ' + fmt(b.BT, 2) + ' K ⇒ ΔBT = <b>' + fmt(b.dBT, 2) + ' K</b> (higher layer is colder ⇒ larger depression)';
      plot($('ti_cv'), [{ x: xs, y: ys, c: '#ED1C24', n: 'ΔBT vs layer height' }, { x: [1, 5], y: [a.dBT, b.dBT], c: '#273896', dots: true }], { xl: 'dust layer height (km)', yl: 'ΔBT = T_s − BT (K)', ymin: 0 }); });
    bind(['ak_w', 'ak_se', 'ak_sa', 'ak_L'], function () { var N = 12, r = ARS.ak(N, val('ak_w'), val('ak_se'), val('ak_sa'), val('ak_L')), cols = ['#273896', '#ED1C24', '#15AFF0', '#1b7f4c', '#a05a00', '#7a3fa0'];
      var series = [], xs = []; for (var j = 0; j < N; j++) xs.push(j + 1);
      [1, 3, 5, 7, 9, 11].forEach(function (i, q) { series.push({ x: xs, y: r.A[i].map(function (v) { return v; }), c: cols[q], n: 'level ' + (i + 1) }); });
      var dg = r.A.map(function (row, i) { return row[i]; });
      $('ak_out').innerHTML = 'DOFS = tr(A) = <b>' + fmt(r.dofs, 3) + '</b> (maximum 12). Diagonal of A: ' + dg.map(function (v) { return fmt(v, 2); }).join(' · ') + '<br>Try: w = 0.3 and σ<sub>ε</sub> = 0.01 ⇒ A ≈ I, DOFS ≈ 12; w = 3, σ<sub>ε</sub> = 0.1 ⇒ DOFS ≈ 4.3.';
      plot($('ak_cv'), series, { xl: 'vertical level j', yl: 'row of A (sensitivity)', ymin: -0.3, ymax: 1.05 }); });
  });
})(typeof window !== 'undefined' ? window : globalThis);
