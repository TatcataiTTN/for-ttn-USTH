# Space Observation, L1 to L3: self-study site (USTH)

Live: https://tatcataittn.github.io/for-ttn-USTH/Space-Observation-Project/self-study-chi-Phuong/

Bilingual (EN | VI switch) study notes made from the three lecture slide decks of the course (L1 Multiwavelength Astronomy, 23 pages; L2 The Life Cycle of Stars, 17 pages; L3 Formation of the Solar System, 40 pages). Browser only, no backend; progress is kept in localStorage.

- Start here: the Big 12 (3 key points, 3 formulas, 3 concepts, 3 principles) with a 12-question self-test and a 3-hour plan.
- Lessons L1, L2, L3: plain words, slide-by-slide notes with page numbers, thumbnails, memory hooks, quick Q and A.
- Formulas and tools: formula sheet, six calculators (wavelength, free-fall time, Jeans length and mass, spin-up, radioactive age), reference tables.
- Practice: 91 questions with explanations citing the slide page (4 derived from the lecturer's three exercises, the rest added); mock exam with timer; 12 written problems with full solutions; 73 slide pages with captions.

Numbers: `build/verify_numbers.py` computes every quantity by two independent methods (closed form and an independent numerical method) and writes `data/verified.json`; `tests/test_calc.js` checks that the JavaScript calculators agree (`node tests/test_calc.js`, 125 comparisons).

Limits: only the three slide decks were used, there is no sample exam and no syllabus, so the exam format is unknown. The slides do not write the Jeans formulas; they are rebuilt from physics and labelled. Differences between slides are listed on the "Sources and limits" page. The slide images belong to the lecturer and to the sources credited inside them.
