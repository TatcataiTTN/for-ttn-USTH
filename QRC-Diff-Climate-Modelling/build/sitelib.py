import os, json
from hx import *
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
SITE_TITLE='QRC-Diff-Climate-Modelling · USTH Phenikaa'
MODULES=[
 ('m1','01-nen-tang-enso-pdo-easm','M1 · Nền tảng ENSO-PDO-EASM'),
 ('m2','02-reservoir-computing-qrc','M2 · Reservoir Computing & QRC'),
 ('m3','03-reservoir-computing-lineage','M3 · Lịch sử Reservoir Computing'),
 ('m4','04-generative-model-drifting','M4 · Lịch sử Generative Model & Drifting'),
 ('m5','05-ung-dung-mo-rong-2-bai-bao','M5 · Ứng dụng mở rộng (QRC + Drifting)'),
 ('m6','06-literature-textbook','M6 · Literature review & Textbook'),
 ('m7','07-cac-the-he-mo-hinh-thoi-tiet','M7 · Các thế hệ mô hình thời tiết'),
]
NAV=[('Trang chủ','{r}index.html')]
def logo_img(cls=''): return f'<img src="{{r}}../assets/logos/usth_logo.png" alt="USTH" class="{cls}">'
def page(title,body,depth,desc='',scripts=(),extra_head=''):
    r='../'*depth
    nav=''.join(f'<a href="{u.format(r=r)}">{t}</a>' for t,u in NAV)
    sc=''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    logo=f'<img src="{r}assets/logos/usth_logo.png" alt="USTH">'
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {SITE_TITLE}</title><meta name="description" content="{esc(desc)}">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{r}_shared/common.css"><link rel="stylesheet" href="{r}_shared/usth_theme.css">{extra_head}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{r}index.html">{logo} QRC-Diff-Climate-Modelling</a><nav>{nav}
<details class="menu"><summary>🎨 Giao diện</summary><div class="pop"><button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><hr><button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button></div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p><b>Dự án:</b> QRC-Diff-Climate-Modelling — mở rộng Quantum Reservoir Computing &amp; Drifting Generative Model cho nghiên cứu khí hậu của 3 giảng viên USTH (PGS.TS Ngô Đức Thành, TS Nguyễn Lê Dũng, TS Nguyễn Xuân Thành). Tài liệu tự học không chính thức của học viên, dựa trên các bài báo/sách đã verify trong thư mục dự án. Logo USTH chính thức, xác minh bằng đọc pixel thật từ logo_usth.png: xanh #273896, đỏ #ED1C24.</p></div></footer>
<script src="{r}_shared/theme.js"></script>{sc}</body></html>'''
def write(relpath,content):
    p=os.path.join(ROOT,relpath); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf-8').write(content)
def module_page(mid,slug,title,subtitle,source,status,parts,quiz_items,notes='',notebook_links=None):
    """parts: list of dict(title,bullets,slides[list of html]). quiz_items: list of dict(q,opts,correct,explain,source)."""
    s=[]
    cover=sl(f'<h1 style="color:#fff;font-size:1.1em">{esc(title)}</h1><p style="opacity:.9">{esc(subtitle)}</p>'
             f'<p style="font-size:.8em;opacity:.8">Nguồn: {esc(source)}</p>','','', '')
    s.append((cover,False))
    for p_i,part in enumerate(parts,1):
        s.append((divider(p_i,len(parts),part['title'],part['bullets']),True))
        for sh in part['slides']:
            s.append((sh,False))
    deck_html=deck(s,deck_id=mid+'-deck')
    qb=quiz_block(mid+'-qz',quiz_items[:10],title='Tự kiểm tra nhanh (10/{} câu, xem đầy đủ ở Ngân hàng câu hỏi)'.format(len(quiz_items)))
    nb_html=''
    if notebook_links:
        items=''.join(f'<li><a href="{href}" target="_blank" rel="noopener">{esc(lbl)}</a></li>' for lbl,href in notebook_links)
        nb_html=f'<h2>Notebook verify</h2><ul>{items}</ul><p style="font-size:.82rem;color:var(--muted)">Mở trực tiếp trên GitHub (xem JSON đã chạy) hoặc tải về chạy lại bằng Jupyter/Colab.</p>'
    body=f'''<div class="usth-banner"><img src="../assets/logos/usth_logo.png"><div><div class="t">{esc(title)}</div><div class="s">{esc(subtitle)} · {esc(status)}</div></div></div>
<p class="lead">Nguồn: {esc(source)}</p>
{deck_html}
<h2>Ngân hàng câu hỏi ({len(quiz_items)} câu)</h2>
{qb}
<p><a href="bank.html">→ Mở ngân hàng đầy đủ {len(quiz_items)} câu (lọc/làm lại)</a></p>
{nb_html}
{notes}
<p class="modnav"><a href="../index.html">← Về trang chủ các module</a></p>'''
    write(f'vi/{slug}/index.html',page(title,body,2,desc=subtitle,scripts=['theme.js','deck.js','quiz.js']))
    os.makedirs(os.path.join(ROOT,'data','qbank'),exist_ok=True)
    bank_items=[]
    for i,it in enumerate(quiz_items):
        bank_items.append(dict(id=f'{mid}-{i+1:03d}',q=it['q'],opts=it['opts'],correct=it['correct'],explain=it['explain'],
            level=it.get('level',1),topic=it.get('topic',''),origin=it.get('origin','goc'),src=it.get('src','')))
    bank_data=dict(module=mid,items=bank_items,essays=[])
    bank_body=(f'<h1>Ngân hàng câu hỏi — {esc(title)}</h1><p class="lead">{len(bank_items)} câu, {esc(status)}.</p>'
        f'<div id="bank"></div><script id="bank-data" type="application/json">'
        + json.dumps(bank_data,ensure_ascii=False).replace('</','<\\/') + '</script>')
    write(f'vi/{slug}/bank.html',page('Ngân hàng câu hỏi · '+title,bank_body,2,scripts=['theme.js','bank.js']))
