# Licence notes — Ocean Optics Web Book

- Source: https://oceanopticsbook.info/ (home page footer read 2026-11-17): "Ocean Optics Web Book — All contents — Creative Commons logo — 2020 Creative Commons Attribution license", link https://creativecommons.org/licenses/by/2.0/ (CC BY 2.0).
- No separate "About/Copyright" page exists (https://oceanopticsbook.info/about returned HTTP 404). `robots.txt` disallows only application/system paths, not /view/.
- CC BY 2.0 allows copying and adaptation with attribution. Individual figures on a page can carry their own credit (e.g. "Data from Segelstein (1981)", "Photo from ICBM Uni. Oldenburg").
- **Decision:** to stay safe with third-party figures, we do NOT copy any textbook image onto the site. We (a) link to the page, (b) cite chapter title + URL, (c) redraw curves from our own Python computations. Short formula statements are restated in our words/notation with attribution "Textbook: <chapter>, oceanopticsbook.info (CC BY 2.0)".
- Crawl: <= 1 request per 1.1 s, User-Agent "study-notes-bot", 34 pages + 11 section index pages, raw HTML in `raw/`, extracted text in `text/`.
- Authorship: the book is edited by Curtis Mobley with contributions from many authors; each page's author is not always shown in the HTML we saved, so we cite "Ocean Optics Web Book" + page title + URL and do not attribute individual sentences to a named person.
