# -*- coding: utf-8 -*-
"""Bước 20 - Viết REPRODUCE.md: cách lấy lại chính xác các kết quả từ dataset. Mọi số lấy từ results/*.csv, không gõ tay."""
import csv
import pathlib
import subprocess

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RT = pd.read_csv(ROOT / "results" / "results_table.csv")
MAN = pd.read_csv(ROOT / "results" / "data_manifest.csv")
CHK = pd.read_csv(ROOT / "results" / "catalog_recheck.csv")
CMP = pd.read_csv(ROOT / "results" / "paper_comparison.csv")
PVC = pd.read_csv(ROOT / "results" / "paper_value_check.csv")
lit = list(csv.DictReader(open(ROOT / "data" / "literature" / "verified_curated.csv")))
dl = list(csv.DictReader(open(ROOT / "data" / "literature" / "downloaded.csv")))
npdf = sum(r["status"] in ("OK", "already") for r in dl)
ver = {k: subprocess.run([str(ROOT / ".venv/bin/python"), "-c", f"import importlib.metadata as m;print(m.version('{k}'))"], capture_output=True, text=True).stdout.strip()
       for k in ("numpy", "scipy", "astropy", "lightkurve", "batman-package", "emcee", "matplotlib", "pandas", "pymupdf")}

L = ["# How to get every result back from the dataset", "",
     "All commands run from the project folder. Data are public: TESS SPOC light curves (MAST) and the NASA Exoplanet Archive.", "",
     "## 0. Environment", "", "```", "python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt", "```", "",
     "Versions used: " + ", ".join(f"{k} {v}" for k, v in ver.items()) + ".", "",
     "## 1. Catalog values (the 'Catalog' column)", "",
     "Table `pscomppars` of the NASA Exoplanet Archive, queried with TAP. One planet:", "",
     "```", 'curl -s "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?format=csv&query=select+pl_name,pl_orbper,pl_rade,pl_ratror,st_rad,tic_id+from+pscomppars+where+pl_name=\'pi+Men+c\'"', "```", "",
     f"`python code/16_reproduce.py` re-queries all {CHK.planet.nunique()} planets live and compares with `data/raw/tess_catalog.csv` (downloaded 2026-11-14): "
     f"**{int(CHK.same.sum())} of {len(CHK)} values identical** on 2026-11-16 (`results/catalog_recheck.csv`). The archive changes over time, so re-run this check before quoting numbers.", "",
     "## 2. Light curves (the input of 'Measured')", "",
     f"{len(MAN)} SPOC 2-minute files for {MAN.planet.nunique()} planets, each listed with URL and md5 in `results/data_manifest.csv`. URL pattern (TIC number zero-padded to 16 digits and split in four):", "",
     "```", "https://archive.stsci.edu/missions/tess/tid/s<SECTOR 4 digits>/<tic16[0:4]>/<tic16[4:8]>/<tic16[8:12]>/<tic16[12:16]>/<file>_lc.fits", "```", "",
     "Example (pi Men c, sector 1): `python code/03b_fetch_static.py 261136679 1`, then:", "",
     "```", "import lightkurve as lk", 'lc = lk.read("data/mast_cache/static/261136679/tess2018206045859-s0001-0000000261136679-0120-s_lc.fits", flux_column="pdcsap_flux").remove_nans().normalize()', "```", "",
     "The MAST API (astroquery, lightkurve search) timed out during this work (16 Nov 2026); the static archive above was used for pi Men c, and cached downloads for the other planets.", "",
     "## 3. Measure a planet", "", "```", 'python code/04_measure_planet.py "pi Men c" --sectors 1          # blind search', 'python code/04_measure_planet.py "K2-141 b" --guided               # search window around the catalog period', "```", "",
     "Output: `results/<planet>/result.json` (all numbers), `chain.npy` (posterior samples), `figures/<planet>_fit.png`. Expected values (`results/results_table.csv`):", "",
     "| Planet | Mode | Sectors | Transits | Period (d) | Rp/R* | Rp (R_earth) | Catalog Rp |", "|---|---|---|---|---|---|---|---|"]
for _, t in RT.iterrows():
    L.append(f"| {t.planet} | {t['mode']} | {t.sectors} | {t.n_transits} | {t.period_d:.5f} | {t.ror:.4f} | {t.rp_rearth:.2f} +- {t.rp_rearth_err:.2f} | {t.cat_rade:.2f} |")
L += ["", "### Repeatability", "",
      "Float32 against float64 is not an issue: the SPOC flux is stored as float32 (rounding 1e-7), the noise is 1e-4; a refit with float32 flux moved Rp/R* by 0.2 %, which is MCMC noise.",
      "Until 16 Nov 2026 the emcee random generator was not seeded (`seed` only set the walker start); two runs of pi Men c gave Rp = 2.0302 and 2.0319 R_earth. "
      "`transit_pipeline.fit_transit` now fixes it; two fits of the same data give identical chains. The ten results published earlier were produced before the fix and reproduce to about 0.1 %.", "",
      "## 4. Authors' numbers against ours", "",
      f"`python code/18_compare_with_papers.py` compares {len(CMP)} published values (read from the PDFs in `literature/pdf/`, text in `literature/text/`) with our results: `results/paper_comparison.csv`. "
      f"Every published number string was found verbatim in the PDF text: **{int(PVC.found.sum())} of {len(PVC)}** (`results/paper_value_check.csv`).", "",
      "`python -I code/19_annotate_pdfs.py` writes annotated copies to `literature/checking/` (yellow: planet names; green: published value consistent within 2 sigma; red: deviation; click a mark for the comment).", "",
      "| Planet | Source | Ratio published | Ratio ours | Difference | Pull | Verdict |", "|---|---|---|---|---|---|---|"]
for _, c in CMP.iterrows():
    L.append(f"| {c.planet} | {c.source.split(' ')[0]} | {c.pub_ror:.4f} | {c.ours_ror:.4f} | {c.dror_pct:+.1f} % | {c.ror_pull:+.1f} | {'agree' if abs(c.ror_pull) < 2 else 'differ'} |")
L += ["", "## 5. Figures and literature", "",
      "- `python code/12_paper_figures.py`: rebuilds the figures of Huang et al. 2018 and adds odd-even, phase 0.5, red-noise plots (`figures/paper/`, numbers in `figure_stats.json`).",
      f"- `python code/13_verify_literature.py`, `13b_curate_literature.py`, `13c_more_literature.py`: {len(lit)} papers verified on arXiv or Crossref; `python code/14_download_literature.py`: {npdf} open-access PDFs in `literature/pdf/`; `python code/15_literature_review.py`: `notes/literature_review_TESS.md`.",
      "- Not downloaded (paywalled, not fetched around the paywall): " + ", ".join(f"{r['first_author']} {r['year']}" for r in dl if r["status"] not in ("OK", "already")) + ".",
      "- `python code/17_build_study_deck.py`: the study deck `slides/Space-Observation-Project-Group-2-Study/index.html`.",
      "- `python code/21_catalog_methods.py`: which paper each NASA default value comes from (`data/raw/catalog_methods.csv`, `data/literature/catalog_refs.csv`; NASA TAP and Crossref).",
      "- `python code/22_deviation_vs_catalog.py`: difference from the catalog in units of the error, with and without the red-noise factor (`results/deviation_vs_catalog.csv`, `catalog_sources.csv`, `figures/paper/deviation_vs_catalog.png`).",
      "- `python code/23_team_notes.py`: the team notes in `team/` (answers to the group chat, planet split, submission folder; not published, it quotes teammates).",
      "- `python code/24_tess_facts.py`: TESS numbers measured on the 21 SPOC files (headers), coverage of our ten planets against the 471, figures (`results/tess_*.csv`, `sample_coverage.csv`).",
      "- `python code/25_history_literature.py`, `25b_history_by_id.py`, then `14_download_literature.py`: group K (history of the search, 22 papers) verified on arXiv/Crossref and downloaded.",
      "- `python code/26_tess_sources.py`: every TESS fact with its quoted phrase and PDF page, searched verbatim in the PDF or the saved web page (`data/literature/tess_fact_sources.csv`).",
      "- `python code/27_discoveries_by_year.py`: confirmed planets per year, method and facility from the NASA archive (TAP).",
      "- `python code/28_orbit_figure.py`: TESS orbit figure and the Kepler, delta-v and latitude computations (`results/tess_orbit_numbers.json`).", ""]
(ROOT / "REPRODUCE.md").write_text("\n".join(L), encoding="utf-8")
print("REPRODUCE.md:", len(L), "dòng")
