# -*- coding: utf-8 -*-
"""Các trang cấp site: trang chủ, bài tập tính toán, đề thi thử, công thức & từ viết tắt, tài liệu gốc."""
import random, json, os
from lib import *
import mock_exam as ME

def inp(i, label, v, step='any', w=None):
    st = f' style="width:{w}px"' if w else ''
    return f'<label>{label}<input id="{i}" type="number" step="{step}" value="{v}"{st}></label>'

def calculators_page():
    def box(cid, title, intro, inputs, out, cv=False):
        c = f'<canvas id="{out[:2]}_cv" width="760" height="300"></canvas>' if cv else ''
        return f'<section class="calc" id="{cid}"><h2>{title}</h2><p>{intro}</p><div>{inputs}</div><div class="res" id="{out}"></div>{c}</section>'
    body = '<p class="crumbs"><a href="index.html">Trang chủ</a> › Bài tập tính toán</p><h1>Bài tập tính toán</h1>' \
           '<p class="lead">Chín công cụ chạy ngay trong trình duyệt (không cần máy chủ). Mọi công thức lấy từ đề cương; kết quả được kiểm thử tự động so với Python (455 phép so sánh, gồm cả ma trận averaging kernel) — xem <code>tests/test_calc.js</code> và notebook.</p>' + \
        '<div id="lifetime"></div>' + box('lifetime-box', '1 · Thời gian sống và bể chứa song song (Ch.1)', 'τ<sub>chem</sub> = 1/(k·[OH]); gộp bể chứa 1/τ = Σ 1/τ<sub>i</sub>. Mặc định là ví dụ CO + OH trong đề thi mẫu.',
            inp('lt_k', 'k (cm³ s⁻¹)', '2e-13') + inp('lt_oh', '[OH] (cm⁻³)', '1e6') + inp('lt_t1', 'τ₁ (ngày)', 2) + inp('lt_t2', 'τ₂ (ngày)', 3) + inp('lt_t3', 'τ₃ (ngày)', 6), 'lt_out') + \
        box('plume', '2 · Suy thời gian sống từ vệt khói (Ch.1)', 'C(x) ∝ exp(−x/(U·τ)) ⇒ τ = L/U với L là độ dài e-fold quan sát được.', inp('pl_U', 'Tốc độ gió U (m/s)', 5) + inp('pl_L', 'Độ dài e-fold L (km)', 50), 'pl_out', True) + \
        box('beer', '3 · Beer–Lambert và góc thiên đỉnh (Ch.2)', 'τ<sub>nghiêng</sub> = τ<sub>đứng</sub>/cos θ; T = e<sup>−τ</sup>. Mặc định: đề thi mẫu Q2(c).', inp('be_tau', 'τ đứng', 0.5) + inp('be_sza', 'Góc thiên đỉnh θ (độ)', 60), 'be_out', True) + \
        box('planck', '4 · Planck, Wien, Stefan–Boltzmann (Ch.2)', 'Thử 5778 K (Mặt Trời) và 288 K (Trái Đất): λ<sub>max</sub> khoảng 0,50 µm và 10,06 µm.', inp('pk_T', 'Nhiệt độ T (K)', 288) + inp('pk_lam', 'Bước sóng λ (µm)', 10), 'pk_out', True) + \
        box('doas', '5 · DOAS: AMF, VCD và Dobson Unit (Ch.3)', 'AMF ≈ 1/cos θ₀ + 1/cos θ; VCD = (SCD − SCD<sub>strat</sub>)/AMF. SCD nhập theo đơn vị 10¹⁵ molecule cm⁻².',
            inp('do_sza', 'θ₀ Mặt Trời (độ)', 60) + inp('do_vza', 'θ cảm biến (độ)', 30) + inp('do_scd', 'SCD (×10¹⁵)', 8) + inp('do_str', 'SCD bình lưu (×10¹⁵)', 3), 'do_out') + \
        box('ak', '6 · Averaging kernel và DOFS (Ch.5)', 'Mô hình 12 mực: K là các đường Gauss rộng w mực; S<sub>ε</sub> = σ<sub>ε</sub>²I; tiên nghiệm tương quan theo độ cao. A = (KᵀS<sub>ε</sub>⁻¹K + S<sub>a</sub>⁻¹)⁻¹KᵀS<sub>ε</sub>⁻¹K; DOFS = tr(A).',
            inp('ak_w', 'Độ rộng kernel w (mực)', 3) + inp('ak_se', 'σ<sub>ε</sub> (nhiễu)', 0.1) + inp('ak_sa', 'σ<sub>a</sub> (tiên nghiệm)', 1) + inp('ak_L', 'Độ dài tương quan', 3), 'ak_out', True) + \
        box('angstrom', '7 · Số mũ Ångström và AOD theo bước sóng (Ch.6)', 'α = ln(τ₁/τ₂)/ln(λ₂/λ₁); τ(λ) = τ₁(λ/λ₁)<sup>−α</sup>. Mặc định: 0,60 ở 440 nm và 0,15 ở 870 nm.',
            inp('an_t1', 'AOD₁', 0.6) + inp('an_l1', 'λ₁ (nm)', 440) + inp('an_t2', 'AOD₂', 0.15) + inp('an_l2', 'λ₂ (nm)', 870) + inp('an_lq', 'AOD tại λ (nm)', 550), 'an_out', True) + \
        box('size', '8 · Tham số kích thước và chế độ tán xạ (Ch.7)', 'x = 2πr/λ. Thử r = 0,0002 µm (N₂), 0,2 µm (sulfate), 5 µm (bụi) với λ = 0,55 µm.', inp('sz_r', 'Bán kính r (µm)', 0.2) + inp('sz_lam', 'Bước sóng λ (µm)', 0.55), 'sz_out') + \
        box('tir', '9 · Độ giảm nhiệt độ sáng theo độ cao lớp bụi (Ch.8)', 'I = B(T<sub>s</sub>)e<sup>−τ</sup> + B(T<sub>layer</sub>)(1 − e<sup>−τ</sup>) ở 10 µm; T<sub>layer</sub> = T<sub>s</sub> − gradient × z. Mô hình đơn giản, không tán xạ, không hơi nước.',
            inp('ti_Ts', 'T bề mặt (K)', 300) + inp('ti_tau', 'τ aerosol (10 µm)', 0.5) + inp('ti_lap', 'Gradient (K/km)', 6.5), 'ti_out', True)
    body = body.replace('<div id="lifetime"></div>', '')
    body = body.replace('id="lifetime-box"', 'id="lifetime"')
    write('calculators.html', page('Bài tập tính toán', body, 0, desc='Công cụ tính toán viễn thám khí quyển chạy trong trình duyệt', scripts=['theme.js', 'calc.js']))

def exam_sets(all_items, nsets=8, per=15):
    rng = random.Random(2026)
    by = {}
    for it in all_items: by.setdefault(it['mod'], []).append(it)
    for k in by: rng.shuffle(by[k])
    sets = []; ptr = {k: 0 for k in by}; mods = sorted(by)
    for s in range(nsets):
        pick = []
        order = mods[s % len(mods):] + mods[:s % len(mods)]
        while len(pick) < per:
            for m in order:
                if len(pick) >= per: break
                if ptr[m] < len(by[m]): pick.append(by[m][ptr[m]]); ptr[m] += 1
            if all(ptr[m] >= len(by[m]) for m in mods): break
        rng.shuffle(pick)
        sets.append([dict(q=p['q'], opts=p['opts'], correct=p['correct'], explain=p['explain'], src=f"{p['mod'].upper()} · {p['src']}") for p in pick])
    return sets

def exam_page(all_items):
    sets = exam_sets(all_items)
    data = json.dumps(dict(sets=sets), ensure_ascii=False).replace('</', '<\\/')
    qs = ''
    for q in ME.Q:
        parts = ''.join(f'<p>{p}</p>' for p in q['parts'])
        key = ''.join(f'<p>{k}</p>' for k in q['key'])
        qs += (f'<div class="qitem mock" data-q="{q["n"]}"><b>Question {q["n"]} ({q["pts"]} pts)</b> — <a href="vi/{MODULES[q["ch"]-1][1]}/index.html">xem Ch.{q["ch"]}</a>{parts}'
               f'<details class="ans"><summary>Xem đáp án gợi ý (Suggested answer key)</summary><div class="keyans">{key}</div></details>'
               f'<label class="selfgrade">Tự chấm (0–{str(q["pts"]).replace(".", ",")}): <input type="number" min="0" max="{q["pts"]}" step="0.25" class="sg" data-q="{q["n"]}" value=""></label></div>')
    instr = '<ul>' + ''.join(f'<li>{i}</li>' for i in ME.INSTR) + '</ul>'
    grading = '<ul>' + ''.join(f'<li>{g}</li>' for g in ME.GRADING) + '</ul>'
    body = f'''<p class="crumbs"><a href="index.html">Trang chủ</a> › Đề thi thử</p><h1>Đề thi thử</h1>
<p class="lead">Hai phần: <a href="#mock">Đề thi mẫu gốc 120 phút (8 câu tự luận, 20 điểm)</a> và <a href="#mcq">luyện đề trắc nghiệm 15 câu / 30 phút</a> sinh từ ngân hàng câu hỏi của 8 module.</p>
<h2 id="mock">Đề thi mẫu gốc — Mock exam (120 phút, 8 câu, 20 điểm)</h2>
<div class="callout"><b class="t">Instructions</b>{instr}<p>Closed book, calculator allowed.</p></div>
<div class="sim"><div class="simh">Đồng hồ và tổng điểm</div><span class="quiz-score" id="mk_timer">Thời gian: 120:00</span>
<button class="btn" id="mk_start">Bắt đầu</button> <button class="btn alt" id="mk_stop">Dừng</button> <button class="btn alt" id="mk_reset">Đặt lại</button>
<span class="quiz-score" id="mk_total" style="margin-left:14px">Tổng: 0/20</span></div>
{qs}
<div class="callout good"><b class="t">Grading hints — Cách chấm thường gặp</b>{grading}</div>
<h2 id="mcq">Luyện đề trắc nghiệm (15 câu, 30 phút)</h2>
<p>Tám đề, mỗi đề lấy câu từ cả 8 module; nộp bài để xem điểm và giải thích từng câu.</p><div id="exam"></div>
<script id="exam-data" type="application/json">{data}</script>'''
    write('exam.html', page('Đề thi thử', body, 0, desc='Đề thi mẫu gốc và đề trắc nghiệm luyện tập', scripts=['theme.js', 'exam.js', 'mock.js']))

def reference_page():
    F = [('Thời gian sống', 'τ = M / L ; 1/τ = Σ 1/τᵢ ; τ_chem = 1/(k[OH])', 'Ch.1'), ('Beer–Lambert', 'I = I₀ exp(−τ), τ = ∫ (σ_a + σ_s) n ds ; T = e^(−τ)', 'Ch.2'),
         ('Planck / Wien', 'B_λ(T) = 2hc²/λ⁵ · 1/(e^(hc/λkT) − 1) ; λ_max T = 2898 µm K', 'Ch.2'), ('Stefan–Boltzmann', 'M = σ_SB T⁴', 'Ch.2'),
         ('RTE', 'dI/ds = −k_e I + k_a B(T) + (k_s/4π) ∫ P(Θ) I(Ω′) dΩ′', 'Ch.2'), ('DOAS', 'ln(I₀/I) = Σ σᵢ′ SCDᵢ + polynomial ; VCD = SCD / AMF', 'Ch.3'),
         ('Optimal estimation', 'x̂ = x_a + G(y − K x_a) ; A = GK ; DOFS = tr(A)', 'Ch.3, 5'), ('Averaging kernel', 'x̂ = x_a + A(x − x_a) + Gε', 'Ch.5'),
         ('Kích thước, Rayleigh', 'x = 2πr/λ ; σ ∝ r⁶/λ⁴ ; Q_ext → 2 (x ≫ 1)', 'Ch.7'), ('Ångström', 'τ(λ) = τ(λ₀)(λ/λ₀)^−α', 'Ch.6'),
         ('Albedo tán xạ đơn', 'ω₀ = σ_s / (σ_s + σ_a)', 'Ch.2, 6'), ('Dobson Unit', '1 DU = 2,69 × 10¹⁶ molecules cm⁻²', 'Ch.3'),
         ('TIR có lớp aerosol', 'I ≈ B(T_s) e^(−τ_aer) + B(T_layer) (1 − e^(−τ_aer))', 'Ch.8')]
    A = [('AOD', 'Aerosol Optical Depth'), ('AMF / SCD / VCD', 'Air Mass Factor / Slant / Vertical Column Density'), ('AK, DOFS', 'Averaging Kernel, Degrees Of Freedom for Signal'),
         ('DOAS', 'Differential Optical Absorption Spectroscopy'), ('TOA', 'Top Of Atmosphere'), ('RTE', 'Radiative Transfer Equation'), ('LUT', 'Look-Up Table'),
         ('ALH', 'Aerosol Layer Height'), ('UVAI', 'UV Absorbing Aerosol Index'), ('TROPOMI, OMI, GOME-2', 'Máy quang phổ nadir UV–vis–SWIR'), ('IASI, AIRS, CrIS', 'Máy thăm dò nadir hồng ngoại nhiệt'),
         ('MLS, MIPAS, OSIRIS', 'Máy thăm dò limb'), ('SAGE, ACE-FTS', 'Che khuất Mặt Trời'), ('CALIOP, ATLID', 'Lidar không gian (chủ động)')]
    t1 = hx_table(['Khái niệm', 'Công thức / giá trị', 'Chương'], [[a, f'<span class="mono">{b}</span>', c] for a, b, c in F], 'left')
    t2 = hx_table(['Viết tắt', 'Nghĩa'], [[a, b] for a, b in A], 'left')
    body = f'''<p class="crumbs"><a href="index.html">Trang chủ</a> › Công thức & từ viết tắt</p><h1>Công thức và từ viết tắt</h1>
<p class="lead">Phụ lục của đề cương (Appendix — Key formulas and acronyms), có ô lọc nhanh.</p>
<p><input id="flt" placeholder="Lọc theo từ khoá…" style="width:100%;max-width:420px;padding:6px 10px;font:inherit;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text)"></p>
<h2>Công thức chính</h2><div id="t1">{t1}</div><h2>Từ viết tắt</h2><div id="t2">{t2}</div>
<script>document.getElementById('flt').addEventListener('input',function(){{var q=this.value.toLowerCase();document.querySelectorAll('#t1 tr,#t2 tr').forEach(function(r,i){{if(r.querySelector('th'))return;r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''}})}});</script>'''
    write('reference.html', page('Công thức và từ viết tắt', body, 0, desc='Bảng công thức và từ viết tắt viễn thám khí quyển', scripts=['theme.js']))

def resources_page():
    figs = [('f1_lifetime', 'Thời gian sống và quy mô biến động (Ch.1)'), ('f12_plume', 'Vệt NO₂ suy ra τ (Ch.1)'), ('f18_decay', 'Đường suy giảm e^(−t/τ) (Ch.1)'),
            ('f2_interactions', 'Hấp thụ, tán xạ, phát xạ, Beer–Lambert (Ch.2)'), ('f8_planck', 'Planck Mặt Trời và Trái Đất (Ch.2)'), ('f11_phase', 'Hàm pha tính bằng Mie (Ch.2, 7)'),
            ('f6_wf', 'Hàm trọng số theo độ cao (Ch.3)'), ('f13_doas', 'Nguyên lý DOAS (Ch.3)'), ('f3_geometries', 'Nadir / limb / che khuất (Ch.4)'), ('f15_tradeoff', 'Phân giải ngang – thẳng đứng (Ch.4)'),
            ('f4_avk', 'Averaging kernel lý tưởng và thực tế (Ch.5)'), ('f14_colavk', 'Kernel cột (Ch.5)'), ('f9_angstrom', 'Phụ thuộc phổ của AOD (Ch.6)'), ('f16_surface', 'Ảnh hưởng bề mặt (Ch.6)'),
            ('f5_regimes', 'Các chế độ tán xạ theo x (Ch.7)'), ('f10_mie_qext', 'Q_ext tính bằng Mie (Ch.7)'), ('f7_altitude', 'Nguyên lý đo độ cao aerosol (Ch.8)'), ('f17_height_sens', 'Độ nhạy theo độ cao lớp (Ch.8)')]
    sl = [('s1_gome', 'GOME: irradiance Mặt Trời và radiance Trái Đất'), ('s2_tropomi', 'TROPOMI L1b một pixel so với VIIRS'), ('s3_wavelengths', 'Cửa sổ bước sóng cho từng khí'), ('s4_solar', 'Bức xạ Mặt Trời ở đỉnh khí quyển và mực biển')]
    gal = ''.join(f'<figure class="lf" style="display:inline-block;width:48%;vertical-align:top"><a href="assets/images/fig/{n}.png"><img src="assets/images/fig/{n}.png" loading="lazy" alt="{esc(c)}"></a><figcaption>{c}</figcaption></figure>' for n, c in figs)
    gal2 = ''.join(f'<figure class="lf" style="display:inline-block;width:48%;vertical-align:top"><a href="assets/images/slides/{n}.jpg"><img src="assets/images/slides/{n}.jpg" loading="lazy" alt="{esc(c)}"></a><figcaption>{c} (ảnh slide bài giảng)</figcaption></figure>' for n, c in sl)
    body = f'''<p class="crumbs"><a href="index.html">Trang chủ</a> › Tài liệu gốc</p><h1>Tài liệu gốc và hình</h1>
<p class="lead">Bộ tài liệu học viên cung cấp. Các file được giữ nguyên để tải về, in hoặc chỉnh sửa.</p>
<div class="grid">
<a class="mod-card" href="resources/De_cuong_Remote_Sensing_Atmosphere.pdf"><div class="num">PDF</div><h3>Đề cương ôn tập (25 trang)</h3><p>8 câu hỏi lý thuyết, đáp án mẫu tiếng Anh, tóm tắt tiếng Việt.</p></a>
<a class="mod-card" href="resources/De_cuong_Remote_Sensing_Atmosphere.docx"><div class="num">DOCX</div><h3>Đề cương (Word)</h3><p>Bản chỉnh sửa được.</p></a>
<a class="mod-card" href="resources/De_thi_mau_Remote_Sensing.pdf"><div class="num">PDF</div><h3>Đề thi mẫu (4 trang)</h3><p>8 câu, 20 điểm, 120 phút, đáp án gợi ý.</p></a>
<a class="mod-card" href="resources/De_thi_mau_Remote_Sensing.docx"><div class="num">DOCX</div><h3>Đề thi mẫu (Word)</h3><p>Bản chỉnh sửa được.</p></a>
<a class="mod-card" href="resources/README_Study_Guide.md"><div class="num">MD</div><h3>README của bộ tài liệu</h3><p>Cấu trúc thư mục, danh sách hình, cách tạo lại.</p></a>
<a class="mod-card" href="notebooks/verify_numbers.ipynb"><div class="num">IPYNB</div><h3>Notebook kiểm chứng số liệu</h3><p>Python tính lại mọi con số dùng trong site (chạy thật, đã lưu kết quả).</p></a>
</div>
<h2>18 hình vẽ bằng mã (đề cương)</h2><p style="font-size:.88rem;color:var(--muted)">Planck và Mie (f8, f10, f11) được tính từ phương trình thật; các hình khác là sơ đồ minh họa theo ghi chú của đề cương.</p>{gal}
<h2>4 ảnh slide bài giảng</h2>{gal2}'''
    write('resources.html', page('Tài liệu gốc', body, 0, desc='Đề cương, đề thi mẫu và hình', scripts=['theme.js']))

def index_page(stats, ncalc=9):
    cards = ''
    for (mid, slug, title, en), st in zip(MODULES, stats):
        cards += (f'<a class="mod-card" href="vi/{slug}/index.html"><div class="num">Đề cương chương {mid[1]}</div><h3>{esc(title)}</h3><p>{esc(en)}</p>'
                  f'<p class="tag">{st["slides"]} slide</p><p class="tag">{st["mcq"]} trắc nghiệm</p><p class="tag">{st["ess"]} tự luận</p></a>')
    tot = lambda k: sum(s[k] for s in stats)
    body = f'''<div class="usth-banner"><img src="assets/images/usth_logo.png" alt="USTH"><div><div class="t">Atmospheric Remote Sensing</div><div class="s">Satellite Remote Sensing of Atmospheric Composition · hệ thống tự học và ôn thi — USTH</div></div></div>
<p class="lead">Tám module bám đúng tám câu hỏi lý thuyết của đề cương: bể chứa và thời gian sống, tương tác ánh sáng – vật chất, truy hồi khí vết, hình học quan sát, averaging kernel, aerosol thụ động, các chế độ tán xạ và độ cao aerosol. Mỗi module có bài giảng, slide, ngân hàng câu hỏi có giải thích, và công cụ tính toán đã kiểm chứng bằng Python.</p>
<div class="kpis"><div class="kpi"><b>8</b><span>module</span></div><div class="kpi"><b>{tot("slides")}</b><span>slide</span></div><div class="kpi"><b>{tot("mcq")}</b><span>câu trắc nghiệm</span></div><div class="kpi"><b>{tot("ess")}</b><span>bài tự luận</span></div><div class="kpi"><b>{ncalc}</b><span>công cụ tính</span></div><div class="kpi"><b>8</b><span>đề luyện 15 câu</span></div></div>
<h2>Các module</h2><div class="grid">{cards}</div>
<h2>Lộ trình ôn tập gợi ý</h2>
<ol class="steps"><li><b>Đọc bài giảng</b> của một module (phần “nôm na” trước, rồi công thức và ví dụ), xem slide.</li><li><b>Làm quiz nhanh</b> cuối trang rồi vào <b>ngân hàng câu hỏi</b>; lọc theo “Câu gốc” để làm các câu từ đề thi mẫu trước.</li><li><b>Thực hành tính</b> ở <a href="calculators.html">Bài tập tính toán</a> với các số trong đề thi mẫu.</li><li><b>Tự luận</b>: làm nháp 8 câu của <a href="exam.html">đề thi mẫu</a> trong 120 phút, rồi đối chiếu đáp án gợi ý và tự chấm.</li><li>Cuối cùng làm <a href="exam.html#mcq">đề trắc nghiệm 30 phút</a>; câu sai thì quay lại module tương ứng.</li></ol>
<h2>Trạng thái và giới hạn (trung thực)</h2>
<ul><li><b>Nguồn duy nhất</b> là bộ tài liệu học viên cung cấp (đề cương 25 trang, đề mẫu, hình, mã vẽ hình). Không có giáo trình gốc kèm theo, nên site không trích số trang sách và không thêm kiến thức ngoài đề cương, trừ phần tính toán minh họa được ghi rõ là “tự dựng, tính bằng Python”.</li>
<li><b>Số liệu</b>: mọi con số tính toán được Python (numpy/scipy) tính lại bằng hai cách độc lập; công cụ JavaScript đối chiếu với Python qua 455 phép so sánh. Mô hình đơn giản (độ giảm nhiệt độ sáng TIR, O₂ phía trên lớp, mô phỏng 12 mực averaging kernel) là minh họa, không phải dữ liệu đo thật.</li>
<li><b>Câu hỏi</b>: nhãn “Câu gốc” là câu lấy từ đề thi mẫu/checklist/nội dung đề cương (có ghi nguồn từng câu); “Bổ sung” là câu sinh thêm bám đề cương. Đã kiểm tra lệch vị trí và lệch độ dài đáp án (xem báo cáo cuối repo).</li>
<li><b>Ngôn ngữ</b>: tiếng Việt, giữ thuật ngữ và đề bài tiếng Anh vì đề thi bằng tiếng Anh. Chưa có bản tiếng Trung.</li>
<li><b>Hình</b>: 18 hình và 4 ảnh slide là của bộ tài liệu gốc; một số hình rộng bị thu nhỏ khi đặt trên slide nên chữ trong hình có thể nhỏ hơn 20 px (chữ HTML của slide đều ≥ 20 px).</li>
<li>Tiến độ làm bài lưu trong <code>localStorage</code> của trình duyệt (mất khi xóa dữ liệu hoặc dùng cửa sổ ẩn danh).</li></ul>'''
    write('index.html', page('Trang chủ', body, 0, desc='Hệ thống tự học Atmospheric Remote Sensing USTH', scripts=['theme.js']))
