import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from sitelib import page, write, MODULES

STATUS={
 'm1':('HOÀN CHỈNH (phần lõi)','13 slide, 21 câu quiz, bám full-text paper #1 + nền tảng khí hậu'),
 'm2':('HOÀN CHỈNH (phần lõi)','13 slide, 12 câu quiz, bám full-text paper QRC + lịch sử Reservoir Computing'),
 'm3':('KHUNG CƠ BẢN — chưa đủ sâu','Slide outline + vài câu quiz nền; cần bổ sung nhiều hơn từ 3 bài Drifting'),
 'm4':('KHUNG CƠ BẢN — chưa làm','Chỉ có outline; cần ghép nội dung paper #1 + NOTE_hieu_va_mo_rong_QRC.md thành slide+quiz riêng'),
 'm5':('KHUNG CƠ BẢN — chưa làm','Chỉ có outline; cần ghép nội dung paper #2 (CORDEX-SEA) + NOTE_hieu_va_mo_rong_Drifting.md'),
 'm6':('KHUNG CƠ BẢN — chưa làm','Chỉ có outline; cần ghép 13 bài literature review mở rộng + 4 textbook đã tải'),
 'm7':('HOÀN CHỈNH','9 phần (8 thế hệ + bảng minh bạch), 22 câu quiz, bám sát README + 8 GiaiThich.md + flag minh bạch demo.ipynb'),
}
cards=''
for mid,slug,title in MODULES:
    st,desc=STATUS[mid]
    cards+=f'<a class="mod-card" href="vi/{slug}/index.html"><div class="num">{mid.upper()}</div><h3>{esc(title)}</h3><p>{esc(desc)}</p><p class="tag">{esc(st)}</p></a>'
body=f'''<div class="usth-banner"><img src="assets/logos/usth_logo.png"><div><div class="t">QRC-Diff-Climate-Modelling</div><div class="s">Quantum Reservoir Computing &amp; Drifting Generative Model — mở rộng nghiên cứu khí hậu USTH Phenikaa</div></div></div>
<p class="lead">Hệ thống tự học mở, 7 module theo dòng lịch sử kiến thức: nền tảng khí hậu → lịch sử reservoir computing/generative model → toán lượng tử/Drifting → 2 bài báo ứng dụng của 3 giảng viên USTH → literature review mở rộng → các thế hệ mô hình thời tiết.</p>
<div class="grid">{cards}</div>
<h2>Trạng thái dự án (trung thực, không che giấu phần chưa xong)</h2>
<p>M1, M2 đã có nội dung đầy đủ bám sát full-text 2 bài báo phương pháp (QRC gốc, bài #1 paper ENSO/EASM). M3–M7 hiện ở mức khung/outline hoặc placeholder — <b>chưa đạt độ sâu và số lượng câu hỏi (~150/module) như mục tiêu ban đầu</b> do khối lượng công việc vượt quá thời gian 1 lượt build. Notebook verify số liệu: có cho M1, M2 (data/notebooks/).</p>
'''
write('index.html',page('Trang chủ',body,0,desc='Hệ thống tự học QRC-Diff-Climate-Modelling, USTH Phenikaa',scripts=['theme.js']))

# ---- stub modules m3-m7 ----
STUBS=[
 ('m3','03-generative-model-drifting','M3 · Generative Model & Drifting',
  'VAE→GAN→Flow→Diffusion→Drifting; trường drift Vp,q và pushforward q=f#pε',
  'Drifting Model gốc (arXiv:2602.04770v2) + 2 bài mở rộng Boltzmann sampling (arXiv:2603.05527v1, 2603.17579v1)'),
 ('m4','04-paper1-ung-dung-qrc','M4 · Bài báo #1 + mở rộng QRC',
  'Áp dụng QRC cho chuỗi PDO/ENSO/Victoria Mode/EASMI — thiết kế cụ thể',
  'Nguyen-Le & Ngo-Duc (2025), J. Climate + NOTE_hieu_va_mo_rong_QRC.md'),
 ('m5','05-paper2-ung-dung-drifting','M5 · Bài báo #2 + mở rộng Drifting',
  'Áp dụng Drifting cho downscaling CORDEX-SEA — thiết kế cụ thể',
  'Nguyen et al. (2026), GMD CORDEX-SEA + NOTE_hieu_va_mo_rong_Drifting.md'),
 ('m6','06-literature-textbook','M6 · Literature review & Textbook',
  '13 bài literature review mở rộng (Q1/Q2 2020-2026) + 4 textbook nền tảng',
  '06_Literature_Review_Mo_Rong/ + 07_Giao_Trinh_Nen_Tang/'),
]
for mid,slug,title,subtitle,source in STUBS:
    st,desc=STATUS[mid]
    body=f'''<div class="usth-banner"><img src="../assets/logos/usth_logo.png"><div><div class="t">{esc(title)}</div><div class="s">{esc(subtitle)}</div></div></div>
<p class="lead">Nguồn dự kiến: {esc(source)}</p>
<div class="callout warn"><b class="t">⚠️ {esc(st)}</b>{esc(desc)}. Trang này là khung placeholder, KHÔNG phải nội dung hoàn chỉnh — không dùng để học/ôn thi ở trạng thái hiện tại.</div>
<p class="modnav"><a href="../../index.html">← Về trang chủ các module</a></p>'''
    write(f'vi/{slug}/index.html',page(title,body,2,desc=subtitle,scripts=['theme.js']))
print('Index + 5 stub pages (m3-m7) đã ghi.')
