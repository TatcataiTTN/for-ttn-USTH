# -*- coding: utf-8 -*-
"""Bước 31 - Xuất mỗi deck HTML thành PDF (mỗi slide một trang 1280x720 px, chữ vẫn chọn được) bằng Chrome in ra PDF.
Dùng: python3 code/31_make_pdf.py  -> pdf/<tên deck>.pdf cho 4 deck (EN, VI của bộ học và bộ thuyết trình)."""
import base64, os, pathlib, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "pdf"; OUT.mkdir(exist_ok=True)
DECKS = {"Space-Observation-Project-Group-2": "Group2-talk-EN", "Space-Observation-Project-Group-2-VI": "Group2-talk-VI",
         "Space-Observation-Project-Group-2-Study": "Group2-study-EN", "Space-Observation-Project-Group-2-Study-VI": "Group2-study-VI"}
CSS = """@page{size:1280px 720px;margin:0}
html,body{margin:0!important;padding:0!important;background:#fff!important}
.mdeck,.mdeck-canvas-wrap,.mdeck-viewport{width:1280px!important;height:auto!important;transform:none!important;position:static!important;margin:0!important;display:block!important;overflow:visible!important}
.mdeck-slide{display:flex!important;position:relative!important;inset:auto!important;width:1280px!important;height:720px!important;min-height:720px!important;max-height:720px!important;overflow:hidden!important;break-after:page;page-break-after:always;box-sizing:border-box}
.mdeck-bar,.mdeck-notes{display:none!important}"""
o = Options(); o.add_argument("--headless=new"); o.add_argument("--window-size=1400,900"); o.add_argument("--hide-scrollbars")
for folder, name in DECKS.items():
    d = webdriver.Chrome(options=o); d.get("file://" + str(ROOT / "slides" / folder / "index.html")); time.sleep(2)
    d.execute_script("var s=document.createElement('style'); s.textContent=arguments[0]; document.head.appendChild(s);", CSS); time.sleep(1.5)
    r = d.execute_cdp_cmd("Page.printToPDF", {"printBackground": True, "preferCSSPageSize": True, "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0, "scale": 1})
    (OUT / f"{name}.pdf").write_bytes(base64.b64decode(r["data"])); d.quit()
    print(name, round((OUT / f"{name}.pdf").stat().st_size / 1e6, 1), "MB")
