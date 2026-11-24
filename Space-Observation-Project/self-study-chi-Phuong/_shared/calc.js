/* Pure functions for the calculators (CGS unless stated). The same numbers are computed in Python by build/verify_numbers.py;
   tests/test_calc.js checks that the two agree. Constants: CODATA 2018. m_H is taken as 1 u (1.66053907e-24 g). */
(function (root) {
  var K = {
    G: 6.6743e-8, kB: 1.380649e-16, mH: 1.66053906660e-24, c: 2.99792458e10, h: 6.62607015e-27, eV: 1.602176634e-12,
    pc: 3.0856775814913673e18, AU: 1.495978707e13, ly: 9.4607304725808e17, Msun: 1.98847e33, yr: 365.25 * 86400, Myr: 365.25 * 86400 * 1e6,
    wien: 0.2897771955 /* cm K */
  };
  function rho(n, mu) { return n * mu * K.mH; }
  function tffSlide(r) { return 1 / Math.sqrt(K.G * r); }
  function tffFull(r) { return Math.sqrt(3 * Math.PI / (32 * K.G * r)); }
  function cs(T, mu) { return Math.sqrt(K.kB * T / (mu * K.mH)); }
  function LJ(T, mu, n, conv) {            // conv: 'rig' = c_s sqrt(pi/(G rho)) ; 'slide' = c_s / sqrt(G rho)
    var r = rho(n, mu), c = cs(T, mu);
    return conv === 'slide' ? c / Math.sqrt(K.G * r) : c * Math.sqrt(Math.PI / (K.G * r));
  }
  function MJ(T, mu, n, conv, sphere) {    // sphere: 'half' = radius L_J/2 ; 'full' = radius L_J (wording of the slide)
    var L = LJ(T, mu, n, conv), R = sphere === 'half' ? L / 2 : L;
    return 4 / 3 * Math.PI * R * R * R * rho(n, mu);
  }
  function freq(lam_m) { return K.c / (lam_m * 100); }                 // Hz
  function energyEV(lam_m) { return K.h * freq(lam_m) / K.eV; }
  function wienT(lam_m) { return K.wien / (lam_m * 100); }              // K
  function band(lam_m) {
    if (lam_m >= 1e-1) return 'radio'; if (lam_m >= 1e-3) return 'microwave'; if (lam_m >= 7.5e-7) return 'infrared';
    if (lam_m >= 3.8e-7) return 'visible'; if (lam_m >= 1e-8) return 'ultraviolet'; if (lam_m >= 1e-11) return 'X-ray'; return 'gamma';
  }
  function parentFrac(t, th) { return Math.pow(2, -t / th); }
  function ageFromDP(DP, th) { return th * Math.log2(1 + DP); }
  function spin(w1, r1, r2) { return w1 * (r1 / r2) * (r1 / r2); }
  var api = { K: K, rho: rho, tffSlide: tffSlide, tffFull: tffFull, cs: cs, LJ: LJ, MJ: MJ, freq: freq, energyEV: energyEV, wienT: wienT, band: band, parentFrac: parentFrac, ageFromDP: ageFromDP, spin: spin };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.CALC = api;
})(typeof window !== 'undefined' ? window : globalThis);
