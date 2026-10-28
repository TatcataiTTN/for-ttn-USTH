// Lớp 1: kiểm thử các hàm thuần của calc.js (chạy trong Node) đối chiếu với data/verified.json do Python tính độc lập.
const fs = require('fs'); const R = fs.existsSync(__dirname + '/../site') ? '../site' : '..';
const ARS = require(R + '/_shared/calc.js'); const V = require(R + '/data/verified.json');
let fail = 0, n = 0;
function near(name, a, b, rel) { n++; const ok = Math.abs(a - b) <= (rel || 1e-6) * Math.max(1, Math.abs(b)); if (!ok) { fail++; console.log('FAIL', name, a, b); } }
near('co days', ARS.lifetime(2e-13, 1e6).tau_days, V.co_oh.tau_days);
near('parallel', ARS.parallel([2, 3, 6]), V.par_example.total);
near('plume h', ARS.plume(5, 50).tau_h, V.plume.tau_h);
near('beer slant', ARS.beer(0.5, 60).tau_slant, V.beer.tau_slant); near('beer T', ARS.beer(0.5, 60).T, V.beer.T);
near('wien sun', ARS.wien(5778), V.wien.sun.lam_max_um); near('wien earth', ARS.wien(288), V.wien.earth.lam_max_um);
near('stefan', ARS.stefan(288), V.stefan.M_earth, 1e-6);
near('planck 10um', ARS.planck(10, 288), V.planck_10um_288, 1e-9);
near('planck inverse', ARS.planckInv(10, ARS.planck(10, 288)), 288, 1e-9);
const d = ARS.doas(60, 30, 8e15, 3e15); near('amf', d.amf, V.amf.amf); near('vcd', d.vcd, V.amf.vcd, 1e-9);
const al = ARS.angstrom(0.60, 440, 0.15, 870); near('alpha', al, V.angstrom.alpha); near('aod550', ARS.aodAt(0.6, 440, al, 550), V.angstrom.tau550);
near('x N2', ARS.size(2e-4, 0.55).x, V.size.N2); near('x sulfate', ARS.size(0.2, 0.55).x, V.size.sulfate); near('x dust', ARS.size(5, 0.55).x, V.size.dust);
if (ARS.size(2e-4, .55).regime !== 'Rayleigh' || ARS.size(0.2, .55).regime !== 'Mie') { fail++; console.log('FAIL regime'); }
const t1 = ARS.tir(300, 1, 0.5, 6.5, 10), t5 = ARS.tir(300, 5, 0.5, 6.5, 10);
near('dBT 1km', t1.dBT, V.tir.z1.dBT, 1e-6); near('dBT 5km', t5.dBT, V.tir.z5.dBT, 1e-6); near('BT 5km', t5.BT, V.tir.z5.BT, 1e-6);
for (const [k, p] of Object.entries({ ideal: [0.3, 0.01], realistic: [3, 0.1], noisy: [3, 1.0] })) {
  const r = ARS.ak(12, p[0], p[1], 1.0, 3.0); near('dofs ' + k, r.dofs, V.oe[k].dofs, 1e-5);
  for (let i = 0; i < 12; i++) for (let j = 0; j < 12; j++) near('A[' + i + '][' + j + '] ' + k, r.A[i][j], V.oe[k].A[i][j], 1e-5);
}
console.log(n + ' phép so sánh, ' + fail + ' lỗi'); process.exit(fail ? 1 : 0);
