# Ocean Optics — self-study and exam practice (USTH)

Static site (no backend). Sources: the lecture *Marine Optics* (H. Loisel, LOG; 120 slides) and the Ocean Optics Web Book (CC BY 2.0, https://oceanopticsbook.info/). Unofficial student material.

* `index.html`, `lessons/`, `slides/`, `calculators.html`, `exam.html`, `reference.html`, `lecture-slides.html`, `resources.html` — the site.
* `data/verified.json` — every number shown on the site, recomputed by two independent methods (`build/verify_numbers.py`); `notebooks/verify_numbers.ipynb` re-checks key values with independent code.
* `build/` — generators (`build_all.py` builds everything; `check_deck.py` checks every slide in Chrome); `tests/` — `test_calc.js` (browser calculators vs Python) and `browser_test.py` (whole site, Selenium).
* `notes/figures_notes.md`, `notes/formulas_from_slides.md` — what is actually on each lecture slide (read from page images); `textbook/` — licence notes, map lecture → textbook pages, extracted text (no images copied).

Limits: no sample exam from the lecturer was available; levels A/B/C and "coverage" refer to papers written for this site. The light-field module is textbook-only. See `resources.html`.
