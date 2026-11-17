# -*- coding: utf-8 -*-
"""Selenium test of the whole site (local server or the real URL). Usage: python3 -u tests/browser_test.py <base_url_with_trailing_slash>"""
import sys, time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8791/'
SLUGS = ['start-here', '01-light-in-water', '02-pure-water', '03-absorption', '04-particle-scattering', '05-measuring-iops', '06-iop-biogeochemistry', '07-light-field', '08-new-platforms']
MIDS = ['p0', 'ma', 'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mh']
PAGES = ['index.html', 'calculators.html', 'exam.html', 'reference.html', 'resources.html', 'lecture-slides.html'] + [f'lessons/{s}/index.html' for s in SLUGS] + [f'lessons/{s}/bank.html' for s in SLUGS] + [f'slides/{m}.html' for m in MIDS]
o = Options(); o.add_argument('--headless=new'); o.add_argument('--window-size=1400,1000'); o.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
d = webdriver.Chrome(options=o)
n = bad = 0
def ck(name, ok, info=''):
    global n, bad; n += 1
    if not ok: bad += 1; print('FAIL', name, info)
def logs(): return [l for l in d.get_log('browser') if l['level'] == 'SEVERE' and 'favicon' not in l['message']]
for p in PAGES:
    d.get(BASE + p); time.sleep(0.8)
    ck('load ' + p, len(d.find_elements(By.CSS_SELECTOR, 'h1, h2')) > 0)
    broken = d.execute_script("return [].filter.call(document.images,function(i){return i.complete&&i.naturalWidth===0}).length")
    ck('images ' + p, broken == 0, broken)
    ck('console ' + p, not logs(), logs()[:1])
# decks
for m in MIDS:
    d.get(BASE + f'slides/{m}.html'); time.sleep(0.6)
    ck('deck slides ' + m, d.execute_script("return document.querySelectorAll('.mdeck-slide').length") >= 7)
# banks
for s in SLUGS:
    d.get(BASE + f'lessons/{s}/bank.html'); time.sleep(0.6)
    ck('bank items ' + s, d.execute_script("return document.querySelectorAll('#bank .qitem, #bank .item, #bank > *').length") > 5)
# module quiz click
d.get(BASE + 'lessons/01-light-in-water/index.html'); time.sleep(0.8)
d.execute_script("document.querySelector('.quiz .qitem .opt').click()")
ck('module quiz answers', 'answered' in d.find_element(By.CSS_SELECTOR, '.quiz-score').text and '1/' in d.find_element(By.CSS_SELECTOR, '.quiz-score').text)
# Big 12 gate: answer all 12 correctly through the UI
d.get(BASE + 'lessons/start-here/index.html'); time.sleep(0.8)
data = d.execute_script("return JSON.parse(document.querySelector('script.quiz-data').textContent)")
items = d.find_elements(By.CSS_SELECTOR, '.quiz .qitem')
ck('big12 has 12 questions', len(items) == 12, len(items))
for it, q in zip(items, data['items']):
    d.execute_script('arguments[0].click()', it.find_elements(By.CSS_SELECTOR, '.opt')[q['correct']])
sc = d.find_element(By.CSS_SELECTOR, '.quiz-score').text; ck('big12 score 12/12', sc.startswith('Score: 12/12'), sc)
d.get(BASE + 'lessons/02-pure-water/index.html'); time.sleep(0.8)
ck('gate green banner', len(d.find_elements(By.CSS_SELECTOR, '.gate.ok')) == 1)
# calculators
d.get(BASE + 'calculators.html'); time.sleep(1)
secs = d.find_elements(By.CSS_SELECTOR, 'section.calc')
ck('10 calculators', len(secs) == 10, len(secs))
for s in secs:
    t = s.find_element(By.CSS_SELECTOR, '.res').text
    ck('calc output ' + s.get_attribute('id'), len(t) > 10 and 'NaN' not in t and 'undefined' not in t, t[:80])
# exam page: MCQ set and written paper
d.get(BASE + 'exam.html'); time.sleep(1)
qs = d.find_elements(By.CSS_SELECTOR, '#exam .qitem'); ck('exam set 15 questions', len(qs) == 15, len(qs))
for q in qs: d.execute_script('arguments[0].click()', q.find_elements(By.CSS_SELECTOR, '.opt')[0])
d.execute_script('arguments[0].click()', [b for b in d.find_elements(By.CSS_SELECTOR, '#exam button') if b.text.strip() == 'Submit'][0]); time.sleep(0.5)
ck('exam result shown', 'Result:' in d.find_element(By.ID, 'res').text, d.find_element(By.ID, 'res').text)
papers = d.find_elements(By.CSS_SELECTOR, 'section.paper'); ck('5 written papers', len(papers) == 5, len(papers))
inp = papers[0].find_element(By.CSS_SELECTOR, 'input.sg'); d.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].value='1.5'; arguments[0].dispatchEvent(new Event('input'))", inp); time.sleep(0.3)
ck('self-grade total', papers[0].find_element(By.CSS_SELECTOR, '.mk_total').text.startswith('Total: 1.5/'), papers[0].find_element(By.CSS_SELECTOR, '.mk_total').text)
print(f'browser_test.py: {n-bad}/{n} checks OK'); d.quit(); sys.exit(1 if bad else 0)
