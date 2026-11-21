# -*- coding: utf-8 -*-
"""Bước 29 - Bản tiếng Việt của các deck HTML: không viết lại deck mà dịch từng đơn vị chữ hiển thị (li, p, td, th, h3, figcaption, tiêu đề, chữ SVG) và ghi chú người nói (data-notes).
Quy trình: (1) `extract`: đọc deck tiếng Anh, tạo danh sách đơn vị (khóa = sha1 của HTML trong phần tử) trong i18n/<deck>_en.tsv và danh sách còn thiếu bản dịch i18n/<deck>_todo.tsv;
(2) dịch: điền i18n/<deck>_vi.tsv (khóa<TAB>tiếng Việt); (3) `apply`: ghi slides/<deck>-VI/index.html (+ sao chép ảnh).
Quy tắc cố định cho các câu lặp theo mẫu (RULES). Tên riêng, số, đơn vị, tiêu đề bài báo giữ nguyên. Hình matplotlib (ảnh PNG) vẫn là tiếng Anh.
Dùng: python3 code/29_translate_deck.py extract|apply|merge <deck> [batch.tsv]"""
import hashlib
import pathlib
import re
import shutil
import sys

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
I18N = ROOT / "i18n"; I18N.mkdir(exist_ok=True)
DECKS = {"study": "Space-Observation-Project-Group-2-Study", "group2": "Space-Observation-Project-Group-2"}
BLOCK = ["div", "p", "ul", "ol", "li", "table", "tr", "td", "th", "h2", "h3", "figure", "figcaption", "svg", "section"]
TAGS = ["li", "p", "td", "th", "h3", "figcaption", "div", "text", "span", "b"]
COMMON = {"planet", "planets", "period", "radius", "ratio", "depth", "question", "answer", "source", "quantity", "value", "where", "page", "year", "mission", "start", "hardware", "result",
          "statement", "class", "axis", "column", "cadence", "product", "available", "sectors", "camera", "transits", "facility", "discovery", "measured", "catalog", "published", "ours", "paper",
          "mode", "verdict", "difference", "pull", "group", "title", "star", "distance", "image", "pixels", "used", "yes", "no", "step", "tool", "what", "why", "how", "term", "meaning",
          "notes", "transit", "duration", "sector", "classes", "address", "case", "setting", "outcome", "check", "comment", "figure", "data", "file", "files", "files", "run", "sectors"}
H = lambda s: hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]


def name_like(txt):
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-\.']*", txt)
    if not words: return True
    for w in words:
        if w.lower() in COMMON: return False
        if re.fullmatch(r"[A-Z][a-zA-Z]*", w) and len(w) > 3 and not w.isupper() and w.lower() not in {"kepler", "spitzer", "cheops", "plato", "corot", "mearth", "espresso", "superwasp", "hatnet", "pulsar", "doppler", "ground"}:
            pass
        if w.islower() and len(w) >= 3 and w not in {"and", "the", "of"} and not re.search(r"\d", w): return False
        if len(w) >= 3 and w.lower() == w: return False
    return True


def units(soup, skip_lit=True, force=frozenset(), raw=False):
    out = []
    for s in soup.select(".mdeck-slide"):
        h = s.find("h2"); title = h.get_text(" ", strip=True) if h else ""
        lit = skip_lit and (title.startswith("A  Appendix. Literature") or re.match(r"\d+ +Literature\. ", title))
        for el in s.find_all(TAGS + ["h2"]):
            if el.name == "h2":
                continue
            if el.name == "span" and ("pg" in (el.get("class") or []) or el.parent.name != "h2"): continue
            if el.name == "b" and el.find_parent(["li", "td", "p", "th", "h3", "figcaption", "text", "div", "span"]) is not None: continue
            if el.name == "span" and el.parent.name == "h2": pass
            elif el.find(BLOCK): continue
            if el.name == "td" and lit: continue
            if el.name == "div" and ("src" in (el.get("class") or []) or "pg" in (el.get("class") or [])): pass
            if el.name == "text" or el.find_parent("svg") is not None: continue      # chữ SVG được vẽ lại bằng tiếng Việt, không dịch từng đoạn
            inner = el.decode_contents().strip()
            txt = el.get_text(" ", strip=True)
            if not re.search(r"[A-Za-z]{3,}", txt): continue
            if not raw and name_like(txt) and H(inner) not in force: continue
            out.append((el, inner))
    return out


def load_vi(deck):
    f = I18N / f"{deck}_vi.tsv"; d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                k, v = line.split("\t", 1); d[k] = v
    return d


# ------------------------------------------------------------------ quy tắc cho câu lặp theo mẫu (trả về None nếu không khớp)
NUM = r"([\d.,]+)"
RULES = [
    (r"Raw PDCSAP and momentum dumps; detrended with red ticks at transits; folded dip with binned data and model\.", "PDCSAP thô và các lần xả mômen; đường đã làm phẳng với vạch đỏ tại transit; dip gập pha với dữ liệu gộp bin và mô hình."),
    (r"Image obtained", "Hình ảnh thu được"),
    (r"A  Appendix\. Literature, groups (\w) to (\w) \((\d+)/(\d+)\)", r"A  Phụ lục. Tài liệu, nhóm \1 đến \2 (\3/\4)"),
    (r"(.+): blind search, sectors (\[[\d, ]+\])\. Same three-panel layout as Figure 2 of the paper\.", r"\1: tìm mù, sector \2. Cùng bố cục ba khung như Hình 2 của bài báo."),
    (r"(.+): guided search, sectors (\[[\d, ]+\])\. Same three-panel layout as Figure 2 of the paper\.", r"\1: tìm có hướng dẫn, sector \2. Cùng bố cục ba khung như Hình 2 của bài báo."),
    (r"(\d+)  Light curves\. (\d+) (.+): raw, detrended and folded", r"\1  Đường cong ánh sáng. \2 \3: thô, đã làm phẳng và gập pha"),
    (r"%s transits folded, duration %s h, %s momentum dumps" % (NUM, NUM, NUM), r"\1 transit được gập pha, thời lượng \2 h, \3 lần xả mômen"),
    (r"depth at mid-transit %s ppm observed, %s ppm model; scatter %s ppm per 2 min" % (NUM, NUM, NUM), r"độ sâu giữa transit \1 ppm quan sát, \2 ppm theo mô hình; độ phân tán \3 ppm mỗi 2 phút"),
    (r"detrending cut the rms from %s to %s ppm: stellar variability" % (NUM, NUM), r"làm phẳng giảm rms từ \1 xuống \2 ppm: do biến thiên của sao"),
    (r"detrending changed the rms by under 20 %: the raw curve is already flat", "làm phẳng chỉ đổi rms dưới 20 %: đường cong thô đã phẳng"),
]


def rule(inner):
    for pat, rep in RULES:
        m = re.fullmatch(pat, inner)
        if m: return m.expand(rep)
    return None


def cmd_extract(deck):
    soup = BeautifulSoup((ROOT / "slides" / DECKS[deck] / "index.html").read_text(encoding="utf-8"), "html.parser")
    vi = load_vi(deck); seen = {}; todo = []
    for el, inner in units(soup, force=frozenset(vi)):
        k = H(inner)
        if k in seen: continue
        seen[k] = inner
        if k not in vi and rule(inner) is None: todo.append((k, inner))
    for s in soup.select(".mdeck-slide"):
        n = s.get("data-notes", "").strip()
        if n:
            k = H(n)
            if k not in seen:
                seen[k] = n
                if k not in vi and rule(n) is None: todo.append((k, n))
    (I18N / f"{deck}_en.tsv").write_text("\n".join(f"{k}\t{v.replace(chr(10), ' ')}" for k, v in seen.items()), encoding="utf-8")
    (I18N / f"{deck}_todo.tsv").write_text("\n".join(f"t{i:03d}\t{k}\t{v.replace(chr(10), ' ')}" for i, (k, v) in enumerate(todo, 1)), encoding="utf-8")
    print(deck, "đơn vị:", len(seen), "| còn phải dịch:", len(todo), "| từ:", sum(len(re.sub(r'<[^>]+>', ' ', v).split()) for _, v in todo))


def cmd_merge(deck, batch):
    todo = {l.split("\t")[0]: l.split("\t")[1] for l in (I18N / f"{deck}_todo.tsv").read_text(encoding="utf-8").splitlines()}
    vi = load_vi(deck); n = 0
    for line in pathlib.Path(batch).read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            tid, v = line.split("\t", 1)
            if tid in todo: vi[todo[tid]] = v.strip(); n += 1
    (I18N / f"{deck}_vi.tsv").write_text("\n".join(f"{k}\t{v}" for k, v in vi.items()), encoding="utf-8")
    print("đã gộp", n, "bản dịch; tổng", len(vi))


def cmd_put(deck, f):
    soup = BeautifulSoup((ROOT / "slides" / DECKS[deck] / "index.html").read_text(encoding="utf-8"), "html.parser")
    allu = {}
    for el, inner in units(soup, raw=True):
        allu.setdefault(inner, el.get_text(" ", strip=True))
    vi = load_vi(deck); n = 0
    for line in pathlib.Path(f).read_text(encoding="utf-8").splitlines():
        if "\t" not in line: continue
        sub, v = line.split("\t", 1)
        ex = [i for i, t in allu.items() if t == sub or i == sub]
        hit = ex or [i for i in allu if sub in i]
        if len(hit) != 1:
            print("  KHÔNG KHỚP DUY NHẤT:", len(hit), sub[:60]); continue
        vi[H(hit[0])] = v.strip(); n += 1
    (I18N / f"{deck}_vi.tsv").write_text("\n".join(f"{k}\t{v}" for k, v in vi.items()), encoding="utf-8")
    print("đã đặt", n, "bản dịch; tổng", len(vi))


def cmd_apply(deck):
    src = ROOT / "slides" / DECKS[deck]; dst = ROOT / "slides" / (DECKS[deck] + "-VI")
    soup = BeautifulSoup((src / "index.html").read_text(encoding="utf-8"), "html.parser")
    vi = load_vi(deck); miss = 0; done = 0
    for el, inner in units(soup, force=frozenset(vi)):
        t = rule(inner) or vi.get(H(inner))
        if t: t = re.sub(r"(?<=\d),(?=\d)", ".", t)
        if t is None: miss += 1; continue
        el.clear(); el.append(BeautifulSoup(t, "html.parser")); done += 1
    for s in soup.select(".mdeck-slide"):
        n = s.get("data-notes", "").strip()
        if n:
            t = rule(n) or vi.get(H(n))
            if t: s["data-notes"] = re.sub(r"(?<=\d),(?=\d)", ".", t)
            else: miss += 1
    # SVG vẽ lại bằng tiếng Việt (độ rộng nhãn tính theo chữ Việt)
    sys.path.insert(0, str(ROOT / "slides" / "deck"))
    try:
        import exo_timeline_svg as T
        for svg in soup.find_all("svg"):
            lab = svg.get("aria-label", "")
            if lab.startswith("Timeline of exoplanet"): svg.replace_with(BeautifulSoup(T.exo_timeline_svg(lang="vi"), "html.parser"))
            elif lab.startswith("Where our ten planets"): svg.replace_with(BeautifulSoup(T.exo_planets_svg(700, 400, lang="vi"), "html.parser"))
    except TypeError:
        print("exo_timeline_svg chưa có tham số lang")
    if soup.head:     # tiếng Việt dài hơn: nén khoảng đệm nhưng giữ chữ >= 20 px
        soup.head.append(BeautifulSoup("<style>.mdeck-slide .take{font-size:26px;padding:9px 16px;margin:6px 0}.mdeck-slide .note{font-size:21px;line-height:1.28;margin:4px 0}"
                                       ".mdeck-slide .card p{font-size:24px!important}.mdeck-slide .card h3{font-size:27px!important}.mdeck-slide figcaption{font-size:20px;margin-top:2px}"
                                       ".mdeck-slide table.tbl.sm td,.mdeck-slide table.tbl.sm th{padding:4px 9px}.mdeck-slide table.tbl.md td,.mdeck-slide table.tbl.md th{padding:7px 10px}"
                                       ".mdeck-slide table.tbl.xs td,.mdeck-slide table.tbl.xs th{padding:3px 8px}.mdeck-slide li{line-height:1.25}</style>", "html.parser"))
    for tb in soup.find_all("table"):
        rows = tb.find_all("tr")
        if rows and len(rows[0].find_all(["th", "td"])) >= 8:
            for tr_ in rows:
                c = tr_.find(["th", "td"])
                if c is not None: c["style"] = (c.get("style", "") + ";white-space:nowrap").strip(";")
            for th in rows[0].find_all("th"): th["style"] = (th.get("style", "") + ";font-size:21px").strip(";")
    html = soup.find("html")
    if html: html["lang"] = "vi"
    if soup.title: soup.title.string = {"study": "Mười ngoại hành tinh đo bằng TESS, bộ slide học (tiếng Việt)", "group2": "Đo bán kính và chu kỳ ngoại hành tinh bằng TESS (tiếng Việt)"}[deck]
    out = str(soup)
    for a, b in (("viewbox=", "viewBox="), ("markerwidth=", "markerWidth="), ("markerheight=", "markerHeight="), ("refx=", "refX="), ("refy=", "refY=")):
        out = out.replace(a, b)
    for a, b in (("Full screen", "Toàn màn hình"), ("⛶ Fullscreen", "⛶ Toàn màn hình"), (">Prev<", ">Trước<"), (">Next<", ">Sau<")):
        out = out.replace(a, b)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("index.html"))
    (dst / "index.html").write_text(out, encoding="utf-8")
    print(deck, "đã dịch", done, "đơn vị; chưa dịch", miss, "->", dst.relative_to(ROOT))


if __name__ == "__main__":
    cmd, deck = sys.argv[1], sys.argv[2]
    {"extract": lambda: cmd_extract(deck), "apply": lambda: cmd_apply(deck), "merge": lambda: cmd_merge(deck, sys.argv[3]), "put": lambda: cmd_put(deck, sys.argv[3])}[cmd]()
