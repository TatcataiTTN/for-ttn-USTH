"""Pipeline đo bán kính + chu kỳ quỹ đạo hành tinh từ ánh sáng TESS.

Quy trình bám theo tutorial "Quick fits for TESS light curves" (exoplanet-case-studies):
  1. lightkurve: tải SPOC PDCSAP, stitch, bỏ NaN, bỏ outlier 7-sigma
  2. BLS: ước lượng chu kỳ, t0, độ sâu, thời lượng (astropy BoxLeastSquares)
  3. Chỉ giữ dữ liệu gần transit (mask) rồi fit mô hình transit
  4. Fit: batman (Mandel & Agol, limb darkening bậc 2 tham số Kipping q1,q2) + emcee
     (thay PyMC3/exoplanet của tutorial bằng stack hiện đại, cùng mô hình vật lý)
  5. MỞ RỘNG so với tutorial: Rp = (Rp/R*) x R*  -> bán kính vật lý (R_earth), đối chiếu catalog

Mọi file trung gian nằm trong thư mục dự án (data/mast_cache, results/).
"""
from __future__ import annotations

import json
import pathlib
import warnings
from dataclasses import dataclass, asdict

import numpy as np

warnings.filterwarnings("ignore")
import batman
import emcee
import lightkurve as lk
from astropy.timeseries import BoxLeastSquares
from scipy.optimize import minimize

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "mast_cache"
R_SUN_IN_R_EARTH = 109.076
R_SUN_IN_R_JUP = 9.731


# --------------------------------------------------------------------------- tải + làm sạch
def load_lightcurve(tic: int, max_sectors: int = 4):
    """Tải SPOC 2-min PDCSAP, tối đa `max_sectors` sector (giữ thời gian chạy hợp lý)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    # file đã tải sẵn từ kho tĩnh archive.stsci.edu (03b_fetch_static.py) dùng được khi API MAST không phản hồi
    sdir = CACHE / "static" / str(tic)
    sfiles = sorted(sdir.glob("*_lc.fits")) if sdir.exists() else []
    if sfiles:
        lcs = [lk.read(str(f), flux_column="pdcsap_flux").remove_nans().normalize() for f in sfiles[:max_sectors]]
        return lcs, [int(lc.sector) for lc in lcs], len(sfiles)
    res = lk.search_lightcurve(f"TIC {tic}", mission="TESS", author="SPOC", exptime=120)
    if len(res) == 0:
        raise RuntimeError(f"Không có SPOC 2-min cho TIC {tic}")
    n_all = len(res)
    # chọn khối sector LIÊN TIẾP dài nhất (tối đa max_sectors): baseline ngắn -> BLS nhanh, không lệch chu kỳ
    secs = np.array([int(str(m).split()[-1]) for m in res.table["mission"]])
    order = np.argsort(secs)
    res, secs = res[order], secs[order]
    best_start, best_len, i = 0, 0, 0
    while i < len(secs):
        j = i
        while j + 1 < len(secs) and secs[j + 1] - secs[j] == 1 and j + 1 - i < max_sectors:
            j += 1
        if j - i + 1 > best_len:
            best_start, best_len = i, j - i + 1
        i = j + 1
    res = res[best_start:best_start + best_len]
    coll = res.download_all(flux_column="pdcsap_flux", download_dir=str(CACHE))
    sectors = [int(lc.sector) for lc in coll]
    out = []
    for lc in coll:
        lc = lc.remove_nans().normalize()
        out.append(lc)
    return out, sectors, n_all


def flatten(lcs, window_days: float, mask=None):
    """Làm phẳng từng sector bằng bộ lọc Savitzky-Golay, `mask` True = transit (không làm phẳng)."""
    flat = []
    for lc in lcs:
        dt = np.nanmedian(np.diff(lc.time.value))
        win = int(window_days / dt) // 2 * 2 + 1
        m = None if mask is None else mask(lc.time.value)
        flat.append(lc.flatten(window_length=max(win, 101), polyorder=2, break_tolerance=50,
                               mask=m, sigma=100))
    return lk.LightCurveCollection(flat).stitch()


# --------------------------------------------------------------------------- BLS
@dataclass
class BLSResult:
    period: float
    t0: float
    duration: float
    depth_ppm: float
    snr: float


def run_bls(t, f, fe, pmin=0.26, pmax=15.0, max_duty=0.2, durations=None) -> tuple[BLSResult, np.ndarray, np.ndarray]:
    # gộp 10 phút để BLS nhanh với dữ liệu nhiều sector
    bins = np.floor((t - t.min()) / (10 / 1440))
    ub, inv = np.unique(bins, return_inverse=True)
    tb = np.bincount(inv, t) / np.bincount(inv)
    fb = np.bincount(inv, f) / np.bincount(inv)
    eb = np.sqrt(np.bincount(inv, fe ** 2)) / np.bincount(inv)
    if durations is None:
        durations = np.array([0.02, 0.04, 0.06, 0.09, 0.13, 0.18, 0.25])
    bls = BoxLeastSquares(tb, fb, dy=eb)
    pg = bls.autopower(durations, minimum_period=pmin,
                       maximum_period=pmax, frequency_factor=2.0, objective="snr")
    # loại nghiệm phi vật lý: transit kéo dài > max_duty chu kỳ (thường là nhiễu/biến thiên sao ở chu kỳ rất ngắn)
    power = np.where(np.asarray(pg.duration) / np.asarray(pg.period) <= max_duty, pg.power, -np.inf)
    i = int(np.argmax(power))
    return (BLSResult(float(pg.period[i]), float(pg.transit_time[i]), float(pg.duration[i]),
                      float(pg.depth[i] * 1e6), float(pg.depth_snr[i])),
            np.asarray(pg.period), np.where(np.isfinite(power), power, 0.0))


def in_transit_mask(period, t0, width):
    def f(t):
        ph = (t - t0 + 0.5 * period) % period - 0.5 * period
        return np.abs(ph) < width
    return f


# --------------------------------------------------------------------------- fit transit
def _model(theta, t, params, tmod):
    t0, per, ror, b, loga, q1, q2 = theta
    a = np.exp(loga)
    inc = np.degrees(np.arccos(b / a))
    params.t0, params.per, params.rp, params.a, params.inc = t0, per, ror, a, inc
    sq = np.sqrt(q1)
    params.u = [2 * sq * q2, sq * (1 - 2 * q2)]
    return tmod.light_curve(params)


def _lnprob(theta, t, f, fe, params, tmod, per0, t00, pw=None):
    t0, per, ror, b, loga, q1, q2 = theta
    if not (0 < ror < 0.6 and 0 <= b < 1 + ror and 1.2 < np.exp(loga) < 200
            and 0 < q1 < 1 and 0 < q2 < 1 and abs(per - per0) < (0.05 * per0 if pw is None else pw)
            and abs(t0 - t00) < 0.2):
        return -np.inf
    # a/R* >= (1+ror) / ... : b < a
    if b >= np.exp(loga):
        return -np.inf
    m = _model(theta, t, params, tmod)
    # lực nhiễu thêm (jitter) giữ cố định = 0, fe đã hiệu chuẩn bằng MAD ở ngoài
    return -0.5 * np.sum(((f - m) / fe) ** 2)


@dataclass
class FitResult:
    period: float; period_err: float
    t0: float; t0_err: float
    ror: float; ror_err: float
    b: float; b_err: float
    a_rs: float; a_rs_err: float
    depth_ppm_model: float
    chi2_red: float
    n_transits: int
    n_points: int
    ror_err_stat: float = 0.0


def fit_transit(t, f, fe, bls: BLSResult, nwalk=32, nburn=1500, nstep=2500, seed=1):
    rng = np.random.default_rng(seed)
    # chỉ giữ dữ liệu gần transit (±2.5 lần duration), như bước "mask" của tutorial
    ph = (t - bls.t0 + 0.5 * bls.period) % bls.period - 0.5 * bls.period
    keep = np.abs(ph) < max(2.5 * bls.duration, 0.15)
    t, f, fe = t[keep], f[keep], fe[keep]
    # hiệu chuẩn sai số bằng MAD ngoài transit
    oot = np.abs(ph[keep]) > 1.2 * bls.duration
    sig = 1.4826 * np.median(np.abs(f[oot] - np.median(f[oot])))
    fe = np.full_like(f, sig)

    params = batman.TransitParams()
    params.t0, params.per, params.rp, params.a, params.inc = bls.t0, bls.period, 0.05, 10, 89
    params.ecc, params.w, params.limb_dark, params.u = 0.0, 90.0, "quadratic", [0.4, 0.2]
    tmod = batman.TransitModel(params, t)

    ror0 = float(np.sqrt(max(bls.depth_ppm, 50) * 1e-6))
    # a/R* ban đầu từ thời lượng: T ~ P/(pi a) -> a ~ P/(pi T)
    a0 = np.clip(bls.period / (np.pi * bls.duration), 2.0, 150.0)
    x0 = np.array([bls.t0, bls.period, ror0, 0.3, np.log(a0), 0.36, 0.3])
    # prior chu kỳ: nửa độ rộng = 1 thời lượng transit / số epoch (ít transit -> chu kỳ không được trôi quá 1 duration qua baseline)
    nep = max((t.max() - t.min()) / bls.period, 1.0)
    pw = min(0.05 * bls.period, max(bls.duration / nep, 1e-4))
    nll = lambda th: -_lnprob(th, t, f, fe, params, tmod, bls.period, bls.t0, pw) if np.isfinite(
        _lnprob(th, t, f, fe, params, tmod, bls.period, bls.t0, pw)) else 1e25
    best = x0
    for b0 in (0.1, 0.4, 0.7):
        for scale in (0.8, 1.0, 1.25):
            s = x0.copy(); s[3] = b0; s[4] = np.log(a0 * scale)
            r = minimize(nll, s, method="Nelder-Mead",
                         options=dict(maxiter=4000, xatol=1e-7, fatol=1e-4))
            if r.fun < nll(best):
                best = r.x
    sc = np.array([2e-4, min(2e-6, 0.1 * pw), 0.02 * best[2], 0.05, 0.03, 0.05, 0.05])
    p0 = best + sc * rng.standard_normal((nwalk, 7))
    p0[:, 3] = np.abs(p0[:, 3]); p0[:, 5] = np.clip(p0[:, 5], 0.02, 0.98); p0[:, 6] = np.clip(p0[:, 6], 0.02, 0.98)
    sampler = emcee.EnsembleSampler(nwalk, 7, _lnprob, args=(t, f, fe, params, tmod, bls.period, bls.t0, pw))
    sampler.random_state = np.random.RandomState(seed).get_state()   # bước đề xuất của emcee cũng cố định: chạy lại ra đúng cùng số
    sampler.run_mcmc(p0, nburn + nstep, progress=False)
    ch = sampler.get_chain(discard=nburn, flat=True)
    q = lambda i: (np.median(ch[:, i]), 0.5 * (np.percentile(ch[:, i], 84) - np.percentile(ch[:, i], 16)))
    (t0, t0e), (per, pere), (ror, rore), (b, be) = q(0), q(1), q(2), q(3)
    a_samp = np.exp(ch[:, 4]); a, ae = np.median(a_samp), 0.5 * (np.percentile(a_samp, 84) - np.percentile(a_samp, 16))
    med = np.median(ch, axis=0)
    mdl = _model(med, t, params, tmod)
    chi2 = float(np.sum(((f - mdl) / fe) ** 2) / (len(f) - 7))
    ntr = int(len(np.unique(np.round((t - t0) / per))))
    fit = FitResult(per, pere, t0, t0e, ror, rore, b, be, a, ae,
                    float((1 - mdl.min()) * 1e6), chi2, ntr, int(len(f)))
    return fit, ch, (t, f, fe, mdl, med)


# --------------------------------------------------------------------------- bán kính vật lý
def physical_radius(fit: FitResult, rstar, rstar_err):
    """Rp = ror x R*  (R* tính bằng R_sun, TIC/NASA) -> R_earth và R_jup, truyền sai số."""
    rp = fit.ror * rstar * R_SUN_IN_R_EARTH
    err = rp * np.hypot(fit.ror_err / fit.ror, (rstar_err or 0.0) / rstar)
    return rp, err, rp / (R_SUN_IN_R_EARTH / R_SUN_IN_R_JUP), err / (R_SUN_IN_R_EARTH / R_SUN_IN_R_JUP)
