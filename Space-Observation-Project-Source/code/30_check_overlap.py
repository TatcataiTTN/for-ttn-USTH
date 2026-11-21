# -*- coding: utf-8 -*-
"""Bước 30 - Kiểm tra bố cục thật của từng slide: chữ/hình thấp nhất phải nằm trên 716 px (phần thấp hơn bị cắt khỏi khung nhìn),
và dòng nguồn (.src) không chồng lên chữ nào của nội dung. Dùng: python3 code/30_check_overlap.py <index.html>. check_deck.py không bắt được lỗi này."""
import os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
JS = """var idx=arguments[0]; var all=document.querySelectorAll('.mdeck-slide'); for (var i=0;i<all.length;i++){all[i].classList.toggle('active', i===idx);}
var s=all[idx]; var r0=s.getBoundingClientRect(), k=r0.width/1280; var src=s.querySelector('.src'); var st = src ? (src.getBoundingClientRect().top-r0.top)/k : 0;
var maxB=0;
s.querySelectorAll('*').forEach(function(e){ if(e.closest('.src')||e.classList.contains('pg')||e.tagName==='H2'||e.closest('.logo-chip')||(e.tagName==='SPAN'&&e.parentElement.tagName==='H2')) return;
  var own=[].some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>0}); var isImg=(e.tagName==='IMG'||e.tagName==='svg');
  if(!own && !isImg) return; var r=e.getBoundingClientRect(); if(!r.width||!r.height) return; var b=(r.bottom-r0.top)/k; if(b>maxB) maxB=b; });
var h=s.querySelector('h2');
return [r0.height/k, st, maxB, h? h.textContent.slice(0,44) : 'cover'];"""
o = Options(); o.add_argument("--headless=new"); o.add_argument("--window-size=1400,900"); o.add_argument("--hide-scrollbars")
d = webdriver.Chrome(options=o); d.get("file://" + os.path.abspath(sys.argv[1])); time.sleep(2)
n = d.execute_script("return document.querySelectorAll('.mdeck-slide').length"); bad = 0
for i in range(n):
    h, st, mb, title = d.execute_script(JS, i); time.sleep(0.05)
    if mb > 716 or (st and mb > st + 8):
        bad += 1; print(f"slide {i+1:2d}: height {h:.0f}, source top {st:.0f}, content bottom {mb:.0f} | {title}")
print("slides with a layout problem:", bad, "of", n); d.quit()
