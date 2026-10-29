# -*- coding: utf-8 -*-
"""Lớp 2/3: kiểm thử tương tác thật trong Chrome (Selenium). Dùng: python3 browser_test.py BASE_URL [thư_mục_ảnh]"""
import sys, time, os, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
BASE = sys.argv[1].rstrip('/') + '/'; SHOTS = sys.argv[2] if len(sys.argv) > 2 else None
if SHOTS: os.makedirs(SHOTS, exist_ok=True)
o = Options(); o.add_argument('--headless=new'); o.add_argument('--window-size=1280,900'); o.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
d = webdriver.Chrome(options=o); d.set_page_load_timeout(40); fails = []; N = 0
def ok(c, msg):
    global N; N += 1
    if not c: fails.append(msg); print('FAIL', msg)
def go(p): d.get(BASE + p); time.sleep(0.4)
def errs():
    return [l['message'] for l in d.get_log('browser') if l['level'] == 'SEVERE' and 'favicon' not in l['message']]
def broken(): return d.execute_script("return [].filter.call(document.images,function(i){return i.complete&&i.naturalWidth===0&&i.loading!=='lazy'||(i.complete&&i.naturalWidth===0)}).map(function(i){return i.src})")
slugs = ['00-core-knowledge', '01-sinks-lifetime', '02-light-matter', '03-passive-trace-gas', '04-pointing-geometries', '05-averaging-kernels', '06-passive-aerosol', '07-scattering-regimes', '08-aerosol-altitude']
pages = ['index.html', 'calculators.html', 'exam.html', 'reference.html', 'resources.html'] + [f'lessons/{s}/index.html' for s in slugs] + [f'lessons/{s}/bank.html' for s in slugs] + ['slides/pa.html'] + [f'slides/m{i}.html' for i in range(1, 9)] + ['slides-gallery.html']
for p in pages:
    go(p); d.execute_script('window.scrollTo(0,document.body.scrollHeight)'); time.sleep(0.1)
    e = errs(); b = broken()
    ok(not e, f'{p}: console errors {e[:2]}'); ok(not b, f'{p}: broken images {b[:3]}')
    ok(len(d.title) > 3, f'{p}: no title')
print('pages checked:', len(pages))
# trang chủ
go('index.html'); ok(len(d.find_elements(By.CSS_SELECTOR, 'a.mod-card')) == 9, 'index: 9 module cards')
if SHOTS: d.save_screenshot(f'{SHOTS}/index.png')
# bài học: quiz
go('lessons/01-sinks-lifetime/index.html'); ok(d.find_element(By.CSS_SELECTOR, '.deckframe iframe').is_displayed(), 'lesson: iframe slide hiển thị')
opts = d.find_elements(By.CSS_SELECTOR, '#m1-qz .qitem')[0].find_elements(By.CSS_SELECTOR, '.opt')
d.execute_script('arguments[0].click()', opts[0]); time.sleep(0.2)
q0 = d.find_elements(By.CSS_SELECTOR, '#m1-qz .qitem')[0]
ok('show' in q0.find_element(By.CSS_SELECTOR, '.explain').get_attribute('class'), 'quiz: giải thích hiện sau khi chọn')
ok(len(q0.find_elements(By.CSS_SELECTOR, '.opt.correct')) == 1, 'quiz: đúng 1 đáp án được tô đúng')
d.execute_script('arguments[0].click()', q0.find_element(By.CSS_SELECTOR, 'button.btn.alt')); time.sleep(0.2)
ok('show' not in q0.find_element(By.CSS_SELECTOR, '.explain').get_attribute('class'), 'quiz: làm lại câu xóa kết quả')
if SHOTS: d.save_screenshot(f'{SHOTS}/lesson_top.png')
# iframe deck điều hướng
fr = d.find_element(By.CSS_SELECTOR, '.deckframe iframe'); d.execute_script('arguments[0].scrollIntoView({block:"center"})', fr); time.sleep(2.5)
d.switch_to.frame(fr); time.sleep(0.6)
ok(d.execute_script("return document.querySelectorAll('.mdeck-slide').length") >= 8, 'iframe: có các slide')
d.find_element(By.CSS_SELECTOR, '.mdeck-next').click(); time.sleep(0.2)
ok(d.find_element(By.CSS_SELECTOR, '.mdeck-count').text.startswith('2 /'), 'iframe: nút Sau chuyển sang slide 2'); d.switch_to.default_content()
# bank
go('lessons/01-sinks-lifetime/bank.html'); items = d.find_elements(By.CSS_SELECTOR, '#bank .qitem'); ok(len(items) == 15, f'bank: trang đầu 15 câu, thấy {len(items)}')
d.execute_script('arguments[0].click()', items[0].find_elements(By.CSS_SELECTOR, '.opt')[1]); time.sleep(0.2)
ok('Progress: answered 1/' in d.find_element(By.CSS_SELECTOR, '#bank .quiz-score').text, 'bank: tiến độ cập nhật')
d.refresh(); time.sleep(0.8); ok('answered 1/' in d.find_element(By.CSS_SELECTOR, '#bank .quiz-score').text, 'bank: tiến độ lưu qua tải lại (localStorage)')
tabs = d.find_elements(By.CSS_SELECTOR, '#bank > .row button'); d.execute_script('arguments[0].click()', tabs[1]); time.sleep(0.1)
ok(len(d.find_elements(By.CSS_SELECTOR, '#bank .qitem')) >= 2, 'bank: tab tự luận có bài')
if SHOTS: d.save_screenshot(f'{SHOTS}/bank_essay.png')
# calculators
go('calculators.html')
def txt(i): return d.find_element(By.ID, i).text
ok('57.87 days' in txt('lt_out'), 'calc: CO lifetime 57.87 days — ' + txt('lt_out')[:80]); ok('τ = 1.000' in txt('lt_out'), 'calc: song song = 1')
ok('0.3679' in txt('be_out'), 'calc: Beer T=0.3679'); ok('3.1547' in txt('do_out'), 'calc: AMF 3.1547')
ok('2.034' in txt('an_out'), 'calc: alpha 2.034'); ok('Mie' in txt('sz_out'), 'calc: size regime')
ok('11.46' in txt('ti_out') and '2.51' in txt('ti_out'), 'calc: TIR 2.51 and 11.46 K — ' + txt('ti_out')[:120]); ok('4.34' in txt('ak_out'), 'calc: DOFS 4.34 — ' + txt('ak_out')[:80])
el = d.find_element(By.ID, 'sz_r'); d.execute_script("arguments[0].value='0.0002';arguments[0].dispatchEvent(new Event('input'))", el); ok('Rayleigh' in txt('sz_out'), 'calc: r=0,0002 → Rayleigh')
el = d.find_element(By.ID, 'ak_w'); d.execute_script("arguments[0].value='0.3';arguments[0].dispatchEvent(new Event('input'))", el)
el = d.find_element(By.ID, 'ak_se'); d.execute_script("arguments[0].value='0.01';arguments[0].dispatchEvent(new Event('input'))", el); ok('11.99' in txt('ak_out'), 'calc: ideal → DOFS ≈ 12 — ' + txt('ak_out')[:60])
if SHOTS: d.save_screenshot(f'{SHOTS}/calculators.png')
ok('0.1000' in txt('op_out') and '0.9048' in txt('op_out'), 'calc: optical depth 0.1 / t 0.9048 — ' + txt('op_out')[:60])
ok('0.00200' in txt('dd_out'), 'calc: DOAS D = 0.002 — ' + txt('dd_out')[:60]); ok('0.00414' in txt('ln_out'), 'calc: Doppler 0.00414 — ' + txt('ln_out')[:60])
go('slides-gallery.html'); ok(len(d.find_elements(By.CSS_SELECTOR, 'figure.ph')) == 11, 'gallery: 11 photos')
go('lessons/00-core-knowledge/index.html'); ok(len(d.find_elements(By.CSS_SELECTOR, '.phgrid figure.ph')) == 7, 'part A: 7 lecture photos'); ok(len(d.find_elements(By.CSS_SELECTOR, '.qa-i')) == 6, 'part A: 6 quick Q&A')
if SHOTS: d.save_screenshot(f'{SHOTS}/partA.png')
# exam
go('exam.html'); ok(len(d.find_elements(By.CSS_SELECTOR, '.qitem.mock')) == 10, 'exam: 10 mock questions')
sg = d.find_elements(By.CSS_SELECTOR, 'input.sg'); d.execute_script("arguments[0].value='2';arguments[0].dispatchEvent(new Event('input'))", sg[0]); ok('2/25' in txt('mk_total'), 'exam: tổng điểm tự chấm')
qs = d.find_elements(By.CSS_SELECTOR, '#exam .qitem'); ok(len(qs) == 15, f'exam: đề trắc nghiệm 15 câu, thấy {len(qs)}')
for q in qs[:3]: d.execute_script('arguments[0].click()', q.find_elements(By.CSS_SELECTOR, '.opt')[0])
d.execute_script('arguments[0].click()', [b for b in d.find_elements(By.CSS_SELECTOR, '#exam .sim .btn') if b.text == 'Submit'][0]); time.sleep(0.4)
ok('Result:' in d.find_element(By.ID, 'res').text, 'exam: nộp bài ra kết quả')
if SHOTS: d.save_screenshot(f'{SHOTS}/exam.png')
# theme
go('index.html'); d.execute_script("document.querySelector('[data-set-theme=dark]').click()"); ok(d.execute_script("return document.documentElement.getAttribute('data-theme')") == 'dark', 'theme: dark')
if SHOTS: d.save_screenshot(f'{SHOTS}/index_dark.png')
d.quit(); print(f'{N} checks, {len(fails)} failures'); sys.exit(1 if fails else 0)
