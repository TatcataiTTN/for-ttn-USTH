// Node test: browser calculators (site/_shared/calc.js) versus Python (site/data/verified.json). Run: node tests/test_calc.js
const fs = require('fs'), path = require('path');
const SITE = fs.existsSync(path.join(__dirname, '..', 'site')) ? path.join(__dirname, '..', 'site') : path.join(__dirname, '..');
const OO = require(path.join(SITE, '_shared', 'calc.js'));
const V = JSON.parse(fs.readFileSync(path.join(SITE, 'data', 'verified.json'), 'utf8'));
let n = 0, bad = 0;
function eq(name, a, b, tol) { n++; const rel = Math.abs(a - b) / Math.max(Math.abs(a), Math.abs(b), 1e-300); if (!(rel <= tol)) { bad++; console.log('FAIL', name, a, b, rel); } }
// pure water
const W = V.pure_water_bw;
for (const [form, key] of [['morel', 'morel'], ['buiteveld', 'buiteveld']])
  for (const lam of [400, 450, 500, 550, 600, 700]) for (const S of [0, 35, 37]) {
    const p = W[`${key}_${lam}_S${S}`];
    eq(`bw ${form} ${lam} S${S}`, OO.bw(lam, S, form), p.b_w, 1e-9); eq(`bw numeric ${form} ${lam} S${S}`, OO.bwNumeric(lam, S, form), p.b_w, 1e-5); eq(`beta90 ${form} ${lam} S${S}`, OO.beta90(lam, S, form), p.beta90, 1e-9);
  }
eq('beta90 546 morel', OO.beta90(546, 0, 'morel'), V.beta90_546_morel_S0, 1e-9); eq('beta90 546 buiteveld', OO.beta90(546, 0, 'buiteveld'), V.beta90_546_buiteveld_S0, 1e-9);
// Beer-Lambert
for (const k of Object.keys(V.beer_lambert_T)) { const m = k.match(/c([\d.]+)_L([\d.]+)/); eq('beer ' + k, OO.beer(+m[1], +m[2]), V.beer_lambert_T[k], 1e-6); }
for (const T of Object.keys(V.c_from_T_25cm)) eq('cFromT ' + T, OO.cFromT(+T, 0.25), V.c_from_T_25cm[T], 1e-9);
// exponentials
eq('cdom 443/412', OO.expAbs(1, 0.014, 412, 443), V.cdom_ratio_443_from_412_S014, 1e-9); eq('nap 443/412', OO.expAbs(1, 0.011, 412, 443), V.nap_ratio_443_from_412_S011, 1e-9);
eq('cdom 350/440', OO.expAbs(1, 0.014, 440, 350), V.cdom_ratio_350_over_440_S014, 1e-9); eq('nap 350/440', OO.expAbs(1, 0.011, 440, 350), V.nap_ratio_350_over_440_S011, 1e-9);
// power law, sum N sigma, Chl, POC/SPM, mixing
for (const k of Object.keys(V.bp_440_over_550)) eq('bp ratio n=' + k, OO.bpLaw(1, +k, 440), V.bp_440_over_550[k], 1e-9);
eq('sumNs', OO.sumNs(5, 1e7, 2), V.sum_N_sigma_c_example, 1e-9);
for (const k of Object.keys(V.bp550_from_chl)) eq('bpChl ' + k, OO.bpChl(+k), V.bp550_from_chl[k], 1e-9);
for (const k of Object.keys(V.poc_spm_from_ap_ratio)) eq('pocSpm ' + k, OO.pocSpm(+k), V.poc_spm_from_ap_ratio[k], 1e-9);
for (const k of Object.keys(V.cdom_mixing_example)) eq('mix ' + k, OO.mix(+k, 10, 0.1), V.cdom_mixing_example[k], 1e-9);
// package effect
for (const k of Object.keys(V.package_Qstar)) eq('pkg ' + k, OO.pkg(+k), V.package_Qstar[k], 1e-9);
// euphotic / Secchi
for (const k of Object.keys(V.euphotic_1pct)) { eq('z1% ' + k, OO.euphotic(+k), V.euphotic_1pct[k].z1pct, 1e-9); eq('z10% ' + k, OO.euphotic(+k, 0.1), V.euphotic_1pct[k].z10pct, 1e-9); }
for (const k of Object.keys(V.secchi_examples)) { const m = k.match(/Kd([\d.]+)_c([\d.]+)/); eq('secchi ' + k, OO.secchi(+m[1], +m[2], 8), V.secchi_examples[k], 1e-9); }
eq('junge', OO.junge(4).n, -1, 1e-12);
console.log(`test_calc.js: ${n - bad}/${n} comparisons OK`); process.exit(bad ? 1 : 0);
