# How to get every result back from the dataset

All commands run from the project folder. Data are public: TESS SPOC light curves (MAST) and the NASA Exoplanet Archive.

## 0. Environment

```
python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Versions used: numpy 2.5.4, scipy 1.18.1, astropy 8.0.2, lightkurve 2.6.0, batman-package 2.5.3, emcee 3.1.6, matplotlib 3.11.2, pandas 2.3.3, pymupdf 2.1.

## 1. Catalog values (the 'Catalog' column)

Table `pscomppars` of the NASA Exoplanet Archive, queried with TAP. One planet:

```
curl -s "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?format=csv&query=select+pl_name,pl_orbper,pl_rade,pl_ratror,st_rad,tic_id+from+pscomppars+where+pl_name='pi+Men+c'"
```

`python code/16_reproduce.py` re-queries all 13 planets live and compares with `data/raw/tess_catalog.csv` (downloaded 2026-11-14): **52 of 52 values identical** on 2026-11-16 (`results/catalog_recheck.csv`). The archive changes over time, so re-run this check before quoting numbers.

## 2. Light curves (the input of 'Measured')

21 SPOC 2-minute files for 11 planets, each listed with URL and md5 in `results/data_manifest.csv`. URL pattern (TIC number zero-padded to 16 digits and split in four):

```
https://archive.stsci.edu/missions/tess/tid/s<SECTOR 4 digits>/<tic16[0:4]>/<tic16[4:8]>/<tic16[8:12]>/<tic16[12:16]>/<file>_lc.fits
```

Example (pi Men c, sector 1): `python code/03b_fetch_static.py 261136679 1`, then:

```
import lightkurve as lk
lc = lk.read("data/mast_cache/static/261136679/tess2018206045859-s0001-0000000261136679-0120-s_lc.fits", flux_column="pdcsap_flux").remove_nans().normalize()
```

The MAST API (astroquery, lightkurve search) timed out during this work (16 Nov 2026); the static archive above was used for pi Men c, and cached downloads for the other planets.

## 3. Measure a planet

```
python code/04_measure_planet.py "pi Men c" --sectors 1          # blind search
python code/04_measure_planet.py "K2-141 b" --guided               # search window around the catalog period
```

Output: `results/<planet>/result.json` (all numbers), `chain.npy` (posterior samples), `figures/<planet>_fit.png`. Expected values (`results/results_table.csv`):

| Planet | Mode | Sectors | Transits | Period (d) | Rp/R* | Rp (R_earth) | Catalog Rp |
|---|---|---|---|---|---|---|---|
| HD 118203 b | blind | 15 16 | 7 | 6.13498 | 0.0553 | 12.30 +- 0.35 | 12.78 |
| HD 189733 b | blind | 41 | 12 | 2.21858 | 0.1541 | 12.61 +- 0.18 | 12.67 |
| HD 209458 b | blind | 56 | 8 | 3.52473 | 0.1212 | 15.74 +- 0.27 | 15.58 |
| WASP-18 b | blind | 103 104 105 106 | 97 | 0.94145 | 0.0986 | 14.18 +- 0.66 | 13.90 |
| WASP-62 b | blind | 1 2 3 4 | 22 | 4.41195 | 0.1104 | 14.82 +- 0.97 | 14.80 |
| LTT 9779 b | guided | 2 | 34 | 0.79205 | 0.0440 | 4.55 +- 0.59 | 4.72 |
| TOI-270 c | blind | 3 4 5 | 11 | 5.66023 | 0.0575 | 2.38 +- 0.07 | 2.33 |
| LTT 1445 A b | guided | 4 | 4 | 5.35904 | 0.0470 | 1.39 +- 0.12 | 1.34 |
| GJ 1132 b | blind | 9 10 | 26 | 1.62891 | 0.0474 | 1.14 +- 0.05 | 1.19 |
| K2-141 b | guided | 42 | 57 | 0.28041 | 0.0188 | 1.40 +- 0.10 | 1.51 |
| pi Men c | blind | 1 | 5 | 6.26778 | 0.0159 | 2.03 +- 0.07 | 2.02 |
| AU Mic b | guided | 1 | 3 | 8.22095 | 0.2452 | 23.05 +- 10.88 | 4.79 |
| DS Tuc A b | guided | 102 103 104 | 8 | 8.12443 | 0.0605 | 6.36 +- 12.70 | 5.70 |

### Repeatability

Float32 against float64 is not an issue: the SPOC flux is stored as float32 (rounding 1e-7), the noise is 1e-4; a refit with float32 flux moved Rp/R* by 0.2 %, which is MCMC noise.
Until 16 Nov 2026 the emcee random generator was not seeded (`seed` only set the walker start); two runs of pi Men c gave Rp = 2.0302 and 2.0319 R_earth. `transit_pipeline.fit_transit` now fixes it; two fits of the same data give identical chains. The ten results published earlier were produced before the fix and reproduce to about 0.1 %.

## 4. Authors' numbers against ours

`python code/18_compare_with_papers.py` compares 12 published values (read from the PDFs in `literature/pdf/`, text in `literature/text/`) with our results: `results/paper_comparison.csv`. Every published number string was found verbatim in the PDF text: **35 of 35** (`results/paper_value_check.csv`).

`python -I code/19_annotate_pdfs.py` writes annotated copies to `literature/checking/` (yellow: planet names; green: published value consistent within 2 sigma; red: deviation; click a mark for the comment).

| Planet | Source | Ratio published | Ratio ours | Difference | Pull | Verdict |
|---|---|---|---|---|---|---|
| HD 118203 b | Pepper+2020 | 0.0554 | 0.0553 | -0.2 % | -0.1 | agree |
| HD 189733 b | Bouchy+2005 | 0.1720 | 0.1541 | -10.4 % | -5.8 | differ |
| HD 189733 b | Knutson+2007 | 0.1545 | 0.1541 | -0.2 % | -0.6 | agree |
| HD 209458 b | Charbonneau+2000 | 0.1186 | 0.1212 | +2.2 % | +1.4 | agree |
| WASP-18 b | Shporer+2019 | 0.0972 | 0.0986 | +1.5 % | +5.1 | differ |
| WASP-62 b | Hellier+2012 | 0.1109 | 0.1104 | -0.4 % | -0.5 | agree |
| LTT 9779 b | Jenkins+2020 | 0.0455 | 0.0440 | -3.4 % | -0.3 | agree |
| TOI-270 c | Gunther+2019 | 0.0583 | 0.0575 | -1.3 % | -0.6 | agree |
| LTT 1445 A b | Winters+2021 | 0.0451 | 0.0470 | +4.2 % | +0.7 | agree |
| GJ 1132 b | Berta-Thompson+2015 | 0.0512 | 0.0474 | -7.5 % | -1.4 | agree |
| K2-141 b | Malavolta+2018 | 0.0204 | 0.0188 | -7.5 % | -1.1 | agree |
| pi Men c | Huang+2018 | 0.0170 | 0.0159 | -6.6 % | -1.0 | agree |

## 5. Figures and literature

- `python code/12_paper_figures.py`: rebuilds the figures of Huang et al. 2018 and adds odd-even, phase 0.5, red-noise plots (`figures/paper/`, numbers in `figure_stats.json`).
- `python code/13_verify_literature.py`, `13b_curate_literature.py`, `13c_more_literature.py`: 150 papers verified on arXiv or Crossref; `python code/14_download_literature.py`: 144 open-access PDFs in `literature/pdf/`; `python code/15_literature_review.py`: `notes/literature_review_TESS.md`.
- Not downloaded (paywalled, not fetched around the paywall): Gelman 1992, Mayor 1995, Hellier 2009, Borucki 1984, Wolszczan 1992, Konacki 2003.
- `python code/17_build_study_deck.py`: the study deck `slides/Space-Observation-Project-Group-2-Study/index.html`.
- `python code/21_catalog_methods.py`: which paper each NASA default value comes from (`data/raw/catalog_methods.csv`, `data/literature/catalog_refs.csv`; NASA TAP and Crossref).
- `python code/22_deviation_vs_catalog.py`: difference from the catalog in units of the error, with and without the red-noise factor (`results/deviation_vs_catalog.csv`, `catalog_sources.csv`, `figures/paper/deviation_vs_catalog.png`).
- `python code/23_team_notes.py`: the team notes in `team/` (answers to the group chat, planet split, submission folder; not published, it quotes teammates).
- `python code/24_tess_facts.py`: TESS numbers measured on the 21 SPOC files (headers), coverage of our ten planets against the 471, figures (`results/tess_*.csv`, `sample_coverage.csv`).
- `python code/25_history_literature.py`, `25b_history_by_id.py`, then `14_download_literature.py`: group K (history of the search, 22 papers) verified on arXiv/Crossref and downloaded.
- `python code/26_tess_sources.py`: every TESS fact with its quoted phrase and PDF page, searched verbatim in the PDF or the saved web page (`data/literature/tess_fact_sources.csv`).
- `python code/27_discoveries_by_year.py`: confirmed planets per year, method and facility from the NASA archive (TAP).
- `python code/28_orbit_figure.py`: TESS orbit figure and the Kepler, delta-v and latitude computations (`results/tess_orbit_numbers.json`).
