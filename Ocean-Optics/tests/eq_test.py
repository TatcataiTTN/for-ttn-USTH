# -*- coding: utf-8 -*-
"""Clicks every symbol of every interactive equation (lesson pages and slides): checks that a callout, a frame and an arrow appear,
that on slides the callout does not overlap the equation and stays inside the 720 px canvas. Usage: python3 -u tests/eq_test.py <base_url>"""
import sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8791/'
o = Options(); o.add_argument('--headless=new'); o.add_argument('--window-size=1400,1000')
d = webdriver.Chrome(options=o); n = bad = 0
def ck(name, ok, info=''):
    global n, bad; n += 1
    if not ok: bad += 1; print('FAIL', name, info)
LESSONS = ['start-here', '01-light-in-water', '02-pure-water', '03-absorption', '04-particle-scattering', '05-measuring-iops', '06-iop-biogeochemistry', '07-light-field']
PAGES = [f'lessons/{s}/index.html' for s in LESSONS] + ['reference.html', 'calculators.html']
for s in PAGES:
    d.get(BASE + s); time.sleep(3)
    names = d.execute_script("return [].map.call(document.querySelectorAll('.eqbig'),function(b){return b.dataset.eq})")
    for nm in names:
        keys = d.execute_script("return JSON.parse(document.querySelector('.eqbig[data-eq=\"%s\"] script.eqdata').textContent)._order" % nm)
        clip = d.execute_script("""var b=document.querySelector('.eqbig[data-eq="%s"]'), st=b.querySelector('.eqstage'), sr=st.getBoundingClientRect(), bad=0;
          st.querySelectorAll('.katex-html *').forEach(function(g){ if(g.children.length||!g.textContent.replace(/[\\u200b\\u00a0\\s]/g,'')) return; var q=g.getBoundingClientRect(); if(q.width&&(q.right>sr.right+2||q.left<sr.left-2)) bad++; }); return bad""" % nm)
        ck(f'no clipping {s}/{nm}', clip == 0, clip)
        rend = d.execute_script("return document.querySelectorAll('.eqbig[data-eq=\"%s\"] .katex').length" % nm); ck(f'katex {s}/{nm}', rend >= 1, rend)
        for k in keys:
            ok = d.execute_script("""var b=document.querySelector('.eqbig[data-eq="%s"]'), e=b.querySelector('.ks-%s'); if(!e) return 'nosym'; e.click();
              return [!!b.querySelector('.eqcall'), b.querySelectorAll('.ksframe').length, b.querySelectorAll('svg.eqarrows path').length>1]""" % (nm, k))
            ck(f'lesson {s}/{nm}/{k}', ok != 'nosym' and ok[0] and ok[1] >= 1 and ok[2], ok)
MODS = {'p0': 'p0', 'ma': 'ma', 'mb': 'mb', 'mc': 'mc', 'md': 'md', 'me': 'me', 'mf': 'mf', 'mg': 'mg'}
for m in MODS:
    d.get(BASE + f'slides/{m}.html'); time.sleep(2.5)
    idxs = d.execute_script("var o=[];document.querySelectorAll('.mdeck-slide').forEach(function(s,k){if(s.querySelector('.eqbig'))o.push(k)});return o")
    for i in idxs:
        d.execute_script("document.querySelectorAll('.mdeck-slide').forEach(function(s,k){s.classList.toggle('active',k==%d)})" % i); time.sleep(0.6)
        nm = d.execute_script("return document.querySelector('.mdeck-slide.active .eqbig').dataset.eq")
        keys = d.execute_script("return JSON.parse(document.querySelector('.mdeck-slide.active .eqbig script.eqdata').textContent)._order")
        for k in keys:
            r = d.execute_script("""var sl=document.querySelector('.mdeck-slide.active'), b=sl.querySelector('.eqbig'), e=b.querySelector('.ks-%s'); if(!e) return null; e.click();
              var c=b.querySelector('.eqcall'); if(!c) return [0];
              var sr=sl.getBoundingClientRect(), k=sr.width/1280, cr=c.getBoundingClientRect(), over=0;
              b.querySelectorAll('.katex-html *').forEach(function(g){ if(g.children.length||!g.textContent.replace(/[\\u200b\\u00a0\\s]/g,'')) return; var q=g.getBoundingClientRect(); if(!q.width) return;
                 var w=Math.min(cr.right,q.right)-Math.max(cr.left,q.left), h=Math.min(cr.bottom,q.bottom)-Math.max(cr.top,q.top); if(w>2&&h>2) over++; });
              var bb=b.getBoundingClientRect(); return [1, over, Math.round((cr.bottom-sr.top)/k), Math.round((bb.bottom-sr.top)/k)];""" % k)
            ck(f'slide {m}#{i}/{nm}/{k} exists', r is not None and r[0] == 1, r)
            if r and r[0] == 1:
                ck(f'slide {m}#{i}/{nm}/{k} no overlap', r[1] == 0, r); ck(f'slide {m}#{i}/{nm}/{k} inside canvas', r[2] <= 720 and r[3] <= 720, r)
print(f'eq_test.py: {n-bad}/{n} checks OK'); d.quit(); sys.exit(1 if bad else 0)
