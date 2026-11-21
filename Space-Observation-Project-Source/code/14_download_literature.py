"""Bước 14 - Tải PDF các bài đã kiểm chứng (data/literature/verified.csv, cột status == OK) vào literature/pdf/<nhóm>/.

Nguồn hợp pháp, công khai: arXiv (https://arxiv.org/pdf/<id>) và liên kết open-access do OpenAlex báo (không dùng
email người dùng, không vượt paywall). Mỗi file tải về được kiểm tra: đầu file là %PDF, và 2 trang đầu (pdftotext)
chứa họ tác giả đầu hoặc vài từ của tiêu đề; sai thì xoá và ghi MISMATCH. Kết quả: data/literature/downloaded.csv.
File tải về là dữ liệu không tin cậy: chỉ đọc bằng pdftotext, không chạy gì từ trong đó.
"""
import csv
import json
import pathlib
import re
import subprocess
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIT = ROOT / "data" / "literature"
PDF = ROOT / "literature" / "pdf"
HEAD = {"User-Agent": "course-literature-check/1.0"}


def get(url, timeout=60, binary=True):
    req = urllib.request.Request(url, headers=HEAD)
    data = urllib.request.urlopen(req, timeout=timeout).read()
    return data if binary else data.decode("utf8", "replace")


def openalex_pdf(doi):
    j = json.loads(get("https://api.openalex.org/works/doi:" + doi, binary=False))
    urls = []
    for loc in [j.get("best_oa_location")] + (j.get("locations") or []):
        if loc and loc.get("pdf_url"):
            urls.append(loc["pdf_url"])
    return list(dict.fromkeys(urls))


def text_ok(path, first_author, title):
    try:
        t = subprocess.run(["pdftotext", "-l", "2", str(path), "-"], capture_output=True, text=True, timeout=60).stdout.lower()
    except Exception:
        return False
    last = re.sub(r"[^a-z]", "", first_author.split()[-1].lower().replace("ü", "u").replace("ö", "o"))
    t2 = re.sub(r"[^a-z ]", "", t.replace("ü", "u").replace("ö", "o").replace("á", "a").replace("é", "e"))
    words = [w for w in re.sub(r"[^a-z ]", " ", title.lower()).split() if len(w) > 4][:6]
    hit = sum(w in t2 for w in words)
    return last in t2.replace(" ", "") or hit >= max(2, len(words) // 2)


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:60]


rows = list(csv.DictReader(open(LIT / "verified_curated.csv")))
out = []
for r in rows:
    if r["status"] != "OK":
        continue
    d = PDF / slug(r["group"])
    d.mkdir(parents=True, exist_ok=True)
    fn = d / f"{slug(r['first_author'])}_{r['year']}_{slug(r['title'])[:40]}.pdf"
    res = dict(group=r["group"], first_author=r["first_author"], year=r["year"], title=r["title"], ref=r["ref"], file="", status="")
    if fn.exists() and fn.stat().st_size > 20000:
        res.update(file=str(fn.relative_to(ROOT)), status="already")
        out.append(res)
        continue
    cands = []
    if r["ref"].startswith("arXiv:"):
        cands.append("https://arxiv.org/pdf/" + r["ref"].split(":")[1])
    else:
        try:
            cands += openalex_pdf(r["ref"].split(":", 1)[1])
        except Exception as e:
            res["status"] = "openalex-error"
    status = res["status"] or "no open-access PDF found"
    for u in cands:
        try:
            b = get(u)
            if not b.startswith(b"%PDF") or len(b) < 20000:
                status = "not a PDF"
                continue
            fn.write_bytes(b)
            if text_ok(fn, r["first_author"], r["title"]):
                res.update(file=str(fn.relative_to(ROOT)), status="OK")
                status = "OK"
                break
            fn.unlink()
            status = "MISMATCH content"
        except Exception as e:
            status = "download-error " + str(e)[:40]
    res["status"] = status
    out.append(res)
    print(status, "|", r["first_author"], r["year"], "|", r["title"][:60], flush=True)
    time.sleep(1.5)

with open(LIT / "downloaded.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["group", "first_author", "year", "title", "ref", "file", "status"])
    w.writeheader()
    w.writerows(out)
print("tải được", sum(o["status"] in ("OK", "already") for o in out), "/", len(out))
