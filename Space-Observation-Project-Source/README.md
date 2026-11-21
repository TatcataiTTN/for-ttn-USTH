# USTH Space Observation Project: measuring exoplanet radii and periods with TESS

Ten exoplanets measured from TESS SPOC light curves (BLS period search, batman + emcee transit fit), compared with the NASA Exoplanet Archive and with the discovery papers.
Folder map and what to share: `LAYOUT.md`. How to get every number back: `REPRODUCE.md`.

## Open these first

| What | Where |
|---|---|
| Presentation deck, 31 slides (25-minute talk) | `slides/deck/index.html` |
| Deck published on GitHub Pages, 37 slides (local source) | `slides/Space-Observation-Project-Group-2/index.html` |
| Study deck, 87 slides (history of the search, TESS numbers with sources, ten planets, authors' numbers, literature); live at https://tatcataittn.github.io/for-ttn-USTH/Space-Observation-Project-Group-2-Study/ | `slides/Space-Observation-Project-Group-2-Study/index.html` |
| Browser demo (works offline via file://) | `slides/demo/index.html` |
| Speaker script, Vietnamese | `notes/script_vi.md` |
| Tutorial notebook | `notebooks/01_measure_one_planet.ipynb` |
| Literature review, 150 papers by sub-method (group K: history of the search) | `notes/literature_review_TESS.md` |
| Answers to the group chat (is a 0.3 to 10 % difference reasonable, which paper each catalog value comes from, what the instructor may ask) | `team/tra_loi_hoi_thoai_lan_2.md` |
| Proposal to split the ten planets between four people, with commands and expected numbers | `team/chia_hanh_tinh.md` |
| Where teammates put their work | `team/nop_bai/` |
| PDFs with planets highlighted and deviations commented | `literature/checking/` (index: `INDEX.csv`) |

## Run order (inside `source .venv/bin/activate`)

| Step | Script | Output |
|---|---|---|
| 1 | `code/01_crawl_catalog.py` | `data/raw/*.csv` from the NASA Exoplanet Archive (TAP) |
| 2 | `code/02_group_candidates.py` | `data/candidates_grouped.csv` (471 planets, group labels) |
| 3 | `code/03_check_mast.py` | `data/shortlist_mast.csv` (SPOC availability) |
| 3b | `code/03b_fetch_static.py <TIC> <sector>` | SPOC files from archive.stsci.edu when the MAST API times out |
| 4 | `code/04_measure_planet.py "<name>" [--guided]` (batch: `code/run_all.sh`) | `results/<slug>/result.json`, `figures/<slug>_fit.png` |
| 5-7 | `code/05_overview_figures.py`, `06_slide_figures.py`, `07_export_demo_data.py` | slide figures, `slides/demo/data/*.js` |
| 8 | `code/08_make_notebook.py` | notebook |
| 9-10 | `code/10_physics_figure.py`, `code/09_build_deck.py` | `slides/deck/index.html` |
| 11 | `code/11_build_group2_deck.py` | `slides/Space-Observation-Project-Group-2/` |
| 12 | `code/12_paper_figures.py` | `figures/paper/*.png`, `figure_stats.json` (Fig 2, 4, 1, 5 types, odd-even, phase 0.5, red noise) |
| 13-15 | `code/13_verify_literature.py`, `13b`, `13c`, `14_download_literature.py`, `15_literature_review.py` | `data/literature/*.csv`, `literature/pdf/`, `notes/literature_review_TESS.md` |
| 16, 20 | `code/16_reproduce.py`, `code/20_write_reproduce.py` | `results/results_table.csv`, `catalog_recheck.csv`, `data_manifest.csv`, `REPRODUCE.md` |
| 17 | `code/17_build_study_deck.py` | `slides/Space-Observation-Project-Group-2-Study/index.html` |
| 18 | `code/18_compare_with_papers.py` | `results/paper_comparison.csv`, `paper_value_check.csv` |
| 19 | `python -I code/19_annotate_pdfs.py` | `literature/checking/` (annotated PDF copies; originals in `literature/pdf/` untouched) |
| 21 | `code/21_catalog_methods.py` | `data/raw/catalog_methods.csv`, `data/literature/catalog_refs.csv` (paper behind each catalog value) |
| 22 | `code/22_deviation_vs_catalog.py` | `results/deviation_vs_catalog.csv`, `catalog_sources.csv`, `figures/paper/deviation_vs_catalog.png` |
| 23 | `code/23_team_notes.py` | `team/*.md`, `team/nop_bai/` (not published) |
| 24 | `code/24_tess_facts.py` | `results/tess_files.csv`, `tess_planets.csv`, `sample_coverage.csv`, TESS figures |
| 25 | `code/25_history_literature.py`, `25b_history_by_id.py` (then `14_download_literature.py`) | group K in `data/literature/verified_curated.csv`, PDFs in `literature/pdf/K_Search_history/` |
| 26 | `code/26_tess_sources.py` | `data/literature/tess_fact_sources.csv` (quote, PDF page and source of each TESS fact) |
| 27 | `code/27_discoveries_by_year.py` | `data/raw/discoveries_by_*.csv`, `figures/paper/exo_discoveries.png` |
| 28 | `code/28_orbit_figure.py` | `figures/paper/tess_orbit.png`, `results/tess_orbit_numbers.json` |

Selection: `data/selected.txt` (10 planets, numbering order), `data/stress_tests.txt` (AU Mic b, DS Tuc A b: reported as failures).
`mode` in each `result.json`: `blind` (BLS over 0.26-15 d) or `guided` (BLS within +-3 % of the catalog period).
Check a deck (system python with selenium): `python3 slides/deck/check_deck.py shots "file://$PWD/slides/Space-Observation-Project-Group-2-Study/index.html"`.
`archive/` holds the first blind-failure JSONs, temporary screenshots, one unrelated PDF and the previous `ULTIMATE_PROMPT.md`; nothing there is read by the code.

## Public copy
`https://github.com/TatcataiTTN/for-ttn-USTH`: the folders `Space-Observation-Project-Group-2/` (31-slide talk, 37 slides), `Space-Observation-Project-Group-2-Study/` (study deck) and `Space-Observation-Project-Source/` (code, results, figures, notes, small data, deck sources).
Not published, on purpose: the paper PDFs (`literature/pdf`, `literature/checking`, `literature/text`; rebuild with `code/14_download_literature.py`), the SPOC cache (`data/mast_cache`, 150 MB; `results/data_manifest.csv` lists every file), saved third-party web pages (`data/raw/tess_docs`; `code/26_tess_sources.py` needs them to re-verify the quotes), course material and the group chats (`inputs/`), the teammates' notes (`team/`) and the virtual environment.

## Vietnamese versions
`slides/Space-Observation-Project-Group-2-Study-VI/` and `slides/Space-Observation-Project-Group-2-VI/`: the same decks with the slide text and speaker notes in Vietnamese (`code/29_translate_deck.py`, translations in `i18n/`). The PNG figures keep their English labels. `code/30_check_overlap.py` checks that nothing is cut off at the bottom of a slide.
Live: https://tatcataittn.github.io/for-ttn-USTH/Space-Observation-Project-Group-2-Study-VI/ and https://tatcataittn.github.io/for-ttn-USTH/Space-Observation-Project-Group-2-VI/

## Raw TESS data (added 21 Nov 2026)
`code/32_raw_data.py`: structure of a SPOC light-curve file and of a target-pixel file, the raw columns plotted, and the check that SAP_FLUX equals the sum of the 45 aperture pixels (`results/raw_data_facts.json`, `figures/paper/raw_*.png`). `code/31_make_pdf.py`: PDF of the four decks in `pdf/`. Study deck: 97 slides, section 10 Data covers file anatomy, columns, plots, pixels, access routes, all data products, the spectral band and the techniques.
