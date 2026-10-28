# -*- coding: utf-8 -*-
"""Khung dựng site Atmospheric-Remote-Sensing (mẫu DSES-USTH): trang bài học, deck 1280x720, ngân hàng câu hỏi, trang chủ."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(__file__))
from hx import esc, callout as hx_callout, table as hx_table, ul as hx_ul, ex, formula, code
from deck_helpers import slide, tbl, callout, tblock, cols as qcols, apply_usth_theme, deck_html
from deck_components import img, card, cards, ul as dul, cols as dcols, table as dtable, matrix, CHIP, pipeline_svg

_here = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(_here, '..', 'site')) if os.path.isdir(os.path.join(_here, '..', 'site')) else os.path.abspath(os.path.join(_here, '..'))   # trong repo triển khai, build/ nằm cạnh index.html
SITE_TITLE = 'Atmospheric Remote Sensing · USTH'
SITE_URL = 'https://tatcataittn.github.io/for-ttn-USTH/Atmospheric-Remote-Sensing/'
class VN(float):
    """Số thực in ra với dấu phẩy thập phân (quy ước tiếng Việt của site) khi dùng trong f-string; giữ kiểu qua các phép tính cơ bản."""
    def __format__(self, spec): return float.__format__(float(self), spec).replace('.', ',')
    def __str__(self): return repr(float(self)).replace('.', ',')
    def _w(op): return lambda a, b: VN(op(float(a), float(b)))
    __add__ = _w(lambda a, b: a + b); __radd__ = _w(lambda a, b: b + a); __sub__ = _w(lambda a, b: a - b); __rsub__ = _w(lambda a, b: b - a)
    __mul__ = _w(lambda a, b: a * b); __rmul__ = _w(lambda a, b: b * a); __truediv__ = _w(lambda a, b: a / b); __rtruediv__ = _w(lambda a, b: b / a)
    def __neg__(self): return VN(-float(self))
VERIFIED = json.load(open(os.path.join(ROOT, 'data', 'verified.json'), encoding='utf-8'), parse_float=VN)
MODULES = [  # (id, slug, tiêu đề ngắn, tiêu đề EN)
    ('m1', '01-sinks-lifetime', 'M1 · Bể chứa & thời gian sống', 'Sinks and lifetime of air pollutants'),
    ('m2', '02-light-matter', 'M2 · Tương tác ánh sáng – vật chất', 'Interaction between light and matter'),
    ('m3', '03-passive-trace-gas', 'M3 · Truy hồi khí vết: cột và profil', 'Passive remote sensing of trace gases'),
    ('m4', '04-pointing-geometries', 'M4 · Hình học quan sát', 'Pointing geometries of spaceborne sensors'),
    ('m5', '05-averaging-kernels', 'M5 · Độ nhạy: averaging kernel', 'Sensitivity of passive retrievals'),
    ('m6', '06-passive-aerosol', 'M6 · Viễn thám aerosol thụ động', 'Passive remote sensing of aerosols'),
    ('m7', '07-scattering-regimes', 'M7 · Các chế độ tán xạ', 'Scattering regimes of light by particles'),
    ('m8', '08-aerosol-altitude', 'M8 · Độ cao aerosol', 'Retrieving aerosol altitude'),
]
NAV = [('Trang chủ', '{r}index.html'), ('Bài tập tính toán', '{r}calculators.html'), ('Đề thi thử', '{r}exam.html'),
       ('Công thức & từ viết tắt', '{r}reference.html'), ('Tài liệu gốc', '{r}resources.html')]
FOOT = ('<p><b>Nguồn:</b> bộ tài liệu <i>Satellite Remote Sensing of Atmospheric Composition — Study Guide</i> (đề cương 8 câu + đề thi mẫu, '
        'kèm hình và mã vẽ hình) mà học viên cung cấp. Mọi con số tính toán trên trang được chạy lại bằng Python (numpy/scipy) và đối chiếu '
        'bằng công thức thứ hai; xem thư mục <code>notebooks/</code> và <code>data/verified.json</code>. Đây là tài liệu tự học không chính thức của học viên USTH, '
        'không thay thế giáo trình hay bài giảng của giảng viên. Logo USTH chính thức; màu xanh #273896, đỏ #ED1C24 đã đọc từ pixel logo.</p>')

def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)

def page(title, body, depth, desc='', scripts=(), extra_head=''):
    r = '../' * depth
    nav = ''.join(f'<a href="{u.format(r=r)}">{t}</a>' for t, u in NAV)
    sc = ''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {SITE_TITLE}</title><meta name="description" content="{esc(desc)}">
<link rel="icon" href="{r}assets/images/usth_logo.png">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{r}_shared/common.css"><link rel="stylesheet" href="{r}_shared/usth_theme.css"><link rel="stylesheet" href="{r}_shared/ars.css">{extra_head}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{r}index.html"><img src="{r}assets/images/usth_logo.png" alt="USTH"> Atmospheric Remote Sensing</a><nav>{nav}
<details class="menu"><summary>🎨 Giao diện</summary><div class="pop"><button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><hr><button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button></div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap">{FOOT}</div></footer>
<script src="{r}_shared/theme.js"></script>{sc}</body></html>'''

# ---------- thành phần cho slide (đơn vị px trên canvas 1280x720, chữ >= 20 px) ----------
def fm(html, size=None):
    st = f' style="font-size:{size}px"' if size else ''
    return f'<div class="fm"{st}>{html}</div>'
def legend(pairs, cols=2):
    return f'<ul class="lg2 c{cols}">' + ''.join(f'<li><b>{k}</b> {v}</li>' for k, v in pairs) + '</ul>'
def fig(name, w, cap, ext='png'):
    return (f'<figure class="fig ctr"><img src="../assets/images/{name}.{ext}" alt="" style="width:{w}px">'
            f'<div class="cap">{cap}</div></figure>')
def cover(title, sub, meta):
    return (f'<div class="mdeck-slide"><h2>{title}</h2><div class="cover-sub">{sub}</div>'
            f'<div class="cover-meta">{meta}</div></div>')
def S(title, body): return slide(title, body)
def finalize(slides):
    """Gắn theme USTH, thay hai logo tự chèn bằng chip trắng (logo navy mất chữ nếu đặt lên băng navy)."""
    out = apply_usth_theme(slides)
    res = []
    for i, s in enumerate(out):
        s = re.sub(r'<img class="usth-emblem[^>]*>', '', s)
        chip = CHIP.replace('class="logo-chip"', 'class="logo-chip cover-chip"') if (i == 0 or i == len(out) - 1) else CHIP
        s = s.replace('</h2>', '</h2>' + chip, 1)
        res.append(s)
    return res

def deck_page(mid, title, slides):
    sl = finalize(slides)
    head = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Slide · {esc(title)} · {SITE_TITLE}</title>
<link rel="stylesheet" href="../_shared/deck_usth_theme.css"><link rel="stylesheet" href="../_shared/deck_sizing.css"><link rel="stylesheet" href="../_shared/ars_deck.css"></head><body>'''
    return head + deck_html(sl) + '<script src="../_shared/deck.js"></script></body></html>'

# ---------- ngân hàng câu hỏi ----------
def write_bank(mid, slug, title, B, status):
    items = []
    for i, it in enumerate(B.items):
        items.append(dict(id=f'{mid}-{i+1:03d}', q=it['q'], opts=it['opts'], correct=it['correct'], explain=it['explain'],
                          level=it['level'], topic=it['topic'], origin=it['origin'], src=it['src']))
    essays = [dict(id=f'{mid}-E{i+1:02d}', q=e['q'], sol=e['sol'], level=e['level'], topic=e['topic'], origin=e['origin'], src=e['src'])
              for i, e in enumerate(B.essays)]
    data = dict(module=mid, items=items, essays=essays)
    body = (f'<p class="crumbs"><a href="../../index.html">Trang chủ</a> › <a href="index.html">{esc(title)}</a> › Ngân hàng câu hỏi</p>'
            f'<h1>Ngân hàng câu hỏi — {esc(title)}</h1><p class="lead">{len(items)} câu trắc nghiệm + {len(essays)} bài tự luận. {esc(status)}</p>'
            f'<div id="bank"></div><script id="bank-data" type="application/json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>')
    write(f'vi/{slug}/bank.html', page('Ngân hàng câu hỏi · ' + title, body, 2, scripts=['theme.js', 'bank.js']))
    return data

def quiz_block(root_id, items):
    data = json.dumps(dict(items=[dict(q=i['q'], opts=i['opts'], correct=i['correct'], explain=i['explain']) for i in items]),
                      ensure_ascii=False).replace('</', '<\\/')
    return f'<div class="quiz"><div id="{root_id}"></div></div><script type="application/json" class="quiz-data" data-root="{root_id}">{data}</script>'

def lesson_page(mod, B, bank_status):
    """mod: dict(id, slug, title, en, question, sections[(h,html)], checklist[], summary[], calcs[(anchor,label)], figs)."""
    mid, slug = mod['id'], mod['slug']
    idx = [m[0] for m in MODULES].index(mid)
    prev_l = f'<a href="../{MODULES[idx-1][1]}/index.html">← {esc(MODULES[idx-1][2])}</a>' if idx > 0 else '<span></span>'
    next_l = f'<a href="../{MODULES[idx+1][1]}/index.html">{esc(MODULES[idx+1][2])} →</a>' if idx < len(MODULES) - 1 else '<span></span>'
    secs = ''.join(f'<h2 id="s{i+1}">{h}</h2>{b}' for i, (h, b) in enumerate(mod['sections']))
    toc = '<div class="toc"><b>Mục lục:</b> ' + ' · '.join(f'<a href="#s{i+1}">{h}</a>' for i, (h, _) in enumerate(mod['sections'])) + \
          ' · <a href="#checklist">Exam checklist</a> · <a href="#slides">Slide</a> · <a href="#quiz">Quiz</a></div>'
    chk = '<ul class="chk">' + ''.join(f'<li>{c}</li>' for c in mod['checklist']) + '</ul>'
    summ = '<ul>' + ''.join(f'<li>{s}</li>' for s in mod['summary']) + '</ul>'
    calcs = ''
    if mod.get('calcs'):
        calcs = '<h2>Thực hành tính toán</h2><p>Các công cụ dưới đây chạy ngay trong trình duyệt, đã đối chiếu với Python:</p><p>' + \
                ' '.join(f'<a class="btn" href="../../calculators.html#{a}">{esc(l)}</a>' for a, l in mod['calcs']) + '</p>'
    quiz = quiz_block(mid + '-qz', B.items[:10])
    body = f'''<p class="crumbs"><a href="../../index.html">Trang chủ</a> › {esc(mod['title'])}</p>
<div class="usth-banner"><img src="../../assets/images/usth_logo.png" alt="USTH"><div><div class="t">{esc(mod['title'])}</div><div class="s">{esc(mod['en'])} · Đề cương chương {idx+1}</div></div></div>
<div class="callout"><b class="t">Đề bài (câu hỏi lý thuyết {idx+1}, gốc tiếng Anh)</b>{mod['question']}</div>
{toc}
{secs}
<h2 id="checklist">Exam checklist — phải nêu được</h2>{chk}
<div class="callout good"><b class="t">Ý chính (tóm tắt tiếng Việt)</b>{summ}</div>
{calcs}
<h2 id="slides">Slide bài giảng ({mod['n_slides']} slide, phím ← → hoặc nút)</h2>
<div class="deckframe"><iframe src="../../slides/{mid}.html" title="Slide {esc(mod['title'])}" loading="lazy" allow="fullscreen" allowfullscreen></iframe></div>
<p><a href="../../slides/{mid}.html" target="_blank" rel="noopener">⛶ Mở slide toàn trang</a></p>
<h2 id="quiz">Tự kiểm tra nhanh (10/{len(B.items)} câu)</h2>{quiz}
<p><a class="btn" href="bank.html">Mở ngân hàng đầy đủ: {len(B.items)} trắc nghiệm + {len(B.essays)} tự luận →</a></p>
<p class="modnav">{prev_l}{next_l}</p>'''
    write(f'vi/{slug}/index.html', page(mod['title'], body, 2, desc=mod['en'], scripts=['theme.js', 'quiz.js']))
    write_bank(mid, slug, mod['title'], B, bank_status)

# ---------- hình vừa khít ô nội dung ----------
from PIL import Image as _PIL
def figfit(name, cap, hmax=500, wmax=1160, ext='png', folder='fig'):
    p = os.path.join(ROOT, 'assets', 'images', folder, f'{name}.{ext}')
    W, H = _PIL.open(p).size
    w = int(min(wmax, hmax * W / H))
    return (f'<figure class="fig ctr"><img src="../assets/images/{folder}/{name}.{ext}" alt="" style="width:{w}px">'
            f'<div class="cap">{cap}</div></figure>')
def lfig(name, cap, ext='png', folder='fig', w=None):
    st = f' style="max-width:{w}px"' if w else ''
    return (f'<figure class="lf"><img src="../../assets/images/{folder}/{name}.{ext}" alt="{esc(cap)}" loading="lazy"{st}>'
            f'<figcaption>{cap}</figcaption></figure>')
def eq(label, html): return f'<div class="eq"><small>{label}</small>{html}</div>'
def model_en(html): return f'<div class="model-en"><div class="lbl">Đáp án mẫu (English model answer)</div>{html}</div>'
def keyans(html): return f'<div class="keyans">{html}</div>'
def finish(mod, slides, B, status):
    """Ghi trang bài học, ngân hàng, slide; trả về dữ liệu ngân hàng để gom đề thi."""
    from qcore import audit
    mod['n_slides'] = len(slides)
    write(f"slides/{mod['id']}.html", deck_page(mod['id'], mod['title'], slides))
    lesson_page(mod, B, status)
    return audit(B.items)

cols = dcols

def ulb(items, size=34, gap=28):
    """Danh sách chữ lớn để lấp đầy slide ít ý (>= 30 px)."""
    return '<ul>' + ''.join(f'<li style="font-size:{size}px;margin:{gap}px 0;line-height:1.3">{i}</li>' for i in items) + '</ul>'

def cards2(h, *cs, cols=3):
    """Lưới thẻ có chiều cao tùy chọn (khi slide còn khối khác)."""
    return f'<div class="cards" style="grid-template-columns:repeat({cols},1fr);height:{h}px">' + ''.join(cs) + '</div>'

def chk(items):
    """Slide checklist: mỗi ý một dòng có số, dàn đều chiều cao (lấp đầy vùng nội dung)."""
    rows = ''.join(f'<div class="chk-row"><span class="chk-n">{i+1}</span><div class="chk-t">{t}</div></div>' for i, t in enumerate(items))
    return f'<div class="chk">{rows}</div>'
