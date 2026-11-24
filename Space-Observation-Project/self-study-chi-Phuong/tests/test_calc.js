// Checks that the browser calculators (site/_shared/calc.js) agree with the Python-verified numbers (data/verified.json).
const fs = require('fs'), path = require('path');
const C = require(path.join(__dirname, '..', '_shared', 'calc.js'));
const V = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'verified.json'), 'utf8'));
let fails = [], n = 0;
function eq(name, a, b, tol) { n++; tol = tol || 2e-3; const rel = Math.abs(a - b) / Math.max(Math.abs(a), Math.abs(b), 1e-300); if (!(rel <= tol)) fails.push(`${name}: js ${a} py ${b} rel ${rel}`); }
for (const r of V.jeans_table) {
  const rho = C.rho(r.n, r.mu);
  eq(`rho n=${r.n} mu=${r.mu}`, rho, r.rho);
  eq('tff slide', C.tffSlide(rho) / C.K.Myr, r.tff_slide_Myr);
  eq('tff full', C.tffFull(rho) / C.K.Myr, r.tff_full_Myr);
  for (const T of [30, 50, 100]) {
    const k = r['T' + T]; if (!k) continue;
    eq(`cs T=${T}`, C.cs(T, r.mu) / 1e5, k.cs_kms);
    eq(`LJ rig T=${T}`, C.LJ(T, r.mu, r.n, 'rig') / C.K.pc, k.LJ_rig_pc);
    eq(`LJ slide T=${T}`, C.LJ(T, r.mu, r.n, 'slide') / C.K.pc, k.LJ_slide_pc);
    eq(`MJ rig half T=${T}`, C.MJ(T, r.mu, r.n, 'rig', 'half') / C.K.Msun, k.MJ_rig_halfsphere_Msun);
    eq(`MJ rig full T=${T}`, C.MJ(T, r.mu, r.n, 'rig', 'full') / C.K.Msun, k.MJ_rig_sphereR_Msun);
    eq(`MJ slide full T=${T}`, C.MJ(T, r.mu, r.n, 'slide', 'full') / C.K.Msun, k.MJ_slide_sphereR_Msun);
  }
}
for (const b of V.em) {
  eq('freq ' + b.band, C.freq(b.lam_m), b.nu_Hz); eq('E ' + b.band, C.energyEV(b.lam_m), b.E_eV); eq('Wien ' + b.band, C.wienT(b.lam_m), b.T_wien_K);
  n++; if (C.band(b.lam_m) !== b.band) fails.push('band ' + b.band + ' -> ' + C.band(b.lam_m));
}
for (const d of V.decay) eq('parent ' + d.n_half_lives, C.parentFrac(d.t_Gyr, 1.25), d.parent, 1e-9);
for (const a of V.ages) eq('age D/P=' + a.DP, C.ageFromDP(a.DP, 1.25), a.t_Gyr, 1e-9);
eq('spin', C.spin(1, 10, 1), V.spinup.omega_ratio, 1e-12);
console.log(fails.length ? 'FAILS:\n' + fails.join('\n') : 'FAILS: none', `(${n} comparisons)`);
process.exit(fails.length ? 1 : 0);
