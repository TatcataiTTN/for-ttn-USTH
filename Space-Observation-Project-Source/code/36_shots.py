# -*- coding: utf-8 -*-
"""Chụp ảnh các slide chọn: python3 code/36_shots.py <index.html> <out_dir> n1 n2 ... (số slide bắt đầu từ 1). Dùng để xem bằng mắt."""
import os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options(); o.add_argument("--headless=new"); o.add_argument("--window-size=1400,900"); o.add_argument("--hide-scrollbars")
d = webdriver.Chrome(options=o); d.get("file://" + os.path.abspath(sys.argv[1])); time.sleep(2)
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for a in sys.argv[3:]:
    i = int(a) - 1
    d.execute_script("var all=document.querySelectorAll('.mdeck-slide');for(var j=0;j<all.length;j++){all[j].classList.toggle('active',j===arguments[0]);}", i)
    time.sleep(0.4); d.save_screenshot(f"{out}/s{int(a):03d}.png")
d.quit()
