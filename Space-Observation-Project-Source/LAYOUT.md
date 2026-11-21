# Project layout

Re-organised on 21 Nov 2026. Only folders were moved (`mv`, nothing deleted); `code/`, `data/`, `results/`, `figures/`, `literature/`, `notebooks/`, `notes/`, `logs/` stayed where they were, so their paths did not change.

```
USTH - Space Observation Project/
├── README.md  REPRODUCE.md  LAYOUT.md  requirements.txt
├── inputs/              what the course and the group gave us (read-only)
│   ├── assignment/        "Yêu cầu đề .jpg" (exam slip), "Hội thoại.md" and "Hội thoại lần 2.md" (group chats)
│   ├── papers/            1809.05967v2.pdf (Huang et al. 2018, the template paper)
│   └── lectures/          L1, L2, L3 lecture PDFs
├── code/                numbered pipeline scripts 01-20, transit_pipeline.py, lit_content.py, run_all.sh
├── data/                catalogue (raw/), selection lists, SPOC cache (mast_cache/), flattened light curves (lightcurves/*.npz), literature CSVs
├── results/             one folder per planet (result.json, chain.npy) + results_table.csv, paper_comparison.csv, ...
├── figures/             per-planet fits and folds; paper/ = figures that rebuild the template paper and the extra checks
├── literature/          pdf/ (121 downloaded), text/ (pdftotext), checking/ (annotated copies, yellow = planet, green/red = value)
├── notebooks/           01_measure_one_planet.ipynb
├── notes/               script_vi.md, literature_review_TESS.md, course/ (notes of the Exoplanets course, other lecturer)
├── logs/                one log per run
├── slides/
│   ├── deck/              source and shared CSS/JS/helpers of the 31-slide deck (+ check_deck.py)
│   ├── assets/            logos and slide images (decks refer to ../assets/images/)
│   ├── demo/              browser demo
│   ├── Space-Observation-Project-Group-2/        37 slides, the version published on GitHub Pages
│   └── Space-Observation-Project-Group-2-Study/  87 slides, study deck (published)
├── team/                for the group: answers to the chat (tra_loi_hoi_thoai_lan_2.md), planet split (chia_hanh_tinh.md), nop_bai/ (submission folder + result template)
├── archive/             not read by any script: scratch_shots/, results_blind_failed/, unrelated/, ULTIMATE_PROMPT.before_layout.md
├── OCR_output/          lecture pages and OCR for the L1-L3 site task (see ULTIMATE_PROMPT.md)
├── publish_clone/       git clone of github.com/TatcataiTTN/for-ttn-USTH (deploy only)
├── ULTIMATE_PROMPT.md   prompt for the L1-L3 lecture site (paths updated to this layout)
└── .venv/               Python environment (`pip install -r requirements.txt`)
```

## Old path to new path

| Before | Now |
|---|---|
| `deck/` | `slides/deck/` |
| `assets/` | `slides/assets/` |
| `demo/` | `slides/demo/` |
| `Space-Observation-Project-Group-2/` | `slides/Space-Observation-Project-Group-2/` |
| `Space-Observation-Project-Group-2-Study/` | `slides/Space-Observation-Project-Group-2-Study/` |
| `Yêu cầu đề .jpg`, `Hội thoại.md`, `Hội thoại lần 2.md` | `inputs/assignment/` |
| `1809.05967v2.pdf` | `inputs/papers/` |
| `L1-MultiwavelengthAstro.pdf`, `L2-StarFormation.pdf`, `L3-PlanetFormation.pdf` | `inputs/lectures/` |
| `scratch_shots/`, `results_blind_failed/` | `archive/` |
| `Gia hạn Bảo hiểm y tế năm học 2026-2027!.pdf` (not part of the project) | `archive/unrelated/` |

Scripts changed to follow the move: `07`, `09`, `10`, `11`, `17`, `19`, `20` (paths only). Added later the same day: `21` to `28`, the folder `team/` and `slides/deck/exo_timeline_svg.py`; `17` and `20` also gained the matching slides and lines (study deck: 87 slides; section 3 history, 4 TESS, 5 sample). Published copy: see the README, section Public copy.

Check after the move: scripts 07, 09, 10, 11, 15, 17, 18 and 20 were re-run (11 before its one-sentence note on `archive/results_blind_failed/` was edited; the local copy of the published deck keeps the sentence that is live); 19 of 20 outputs are byte-identical to before (decks, demo data, figures, CSVs, review), and the 20th, `REPRODUCE.md`, differs only in the study-deck path line. `19_annotate_pdfs.py` was not re-run (it rewrites 105 MB): only its output path was tested and it matches the existing file. All relative image and script links in the four HTML pages resolve.

## What to hand to teammates

| Part | Size | Note |
|---|---|---|
| `README.md`, `REPRODUCE.md`, `LAYOUT.md`, `requirements.txt` | < 20 KB | start here |
| `code/`, `notebooks/`, `notes/`, `results/`, `figures/`, `logs/` | about 10 MB | everything needed to read and rerun the analysis |
| `slides/` | about 8.5 MB | four HTML pages with their images |
| `data/raw/`, `data/*.csv`, `data/*.txt`, `data/literature/` | about 4 MB | catalogue and selection |
| `data/lightcurves/` | 7.1 MB | flattened light curves written by `04_measure_planet.py`; read by `06`, `07`, `12` (the demo data come from them) |
| `inputs/` | 8.6 MB | course material, optional |
| `data/mast_cache/` | 150 MB | SPOC files; `results/data_manifest.csv` lists URL and md5 for each |
| `literature/pdf/` | 389 MB | `code/14_download_literature.py` fetches them again (list: `data/literature/downloaded.csv`) |
| `literature/checking/` | 105 MB | `code/19_annotate_pdfs.py` rebuilds them from `literature/pdf/` |
| `.venv/`, `publish_clone/`, `OCR_output/` | 971 MB, 215 MB, 43 MB | local tooling; do not share |

The three large literature and data folders are too big for a normal GitHub push; share them through a drive link if the group wants the PDFs.
