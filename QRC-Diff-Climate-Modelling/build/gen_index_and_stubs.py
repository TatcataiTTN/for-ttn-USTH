import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from sitelib import page, write, MODULES

STATUS={
 'm1':('HOÀN CHỈNH (phần lõi)','13 slide, 21 câu quiz, bám full-text paper #1 + nền tảng khí hậu'),
 'm2':('HOÀN CHỈNH (phần lõi)','13 slide, 12 câu quiz, bám full-text paper QRC + lịch sử Reservoir Computing'),
 'm3':('HOÀN CHỈNH (phần lõi)','5 slide + 1 sơ đồ lineage SVG, 7 câu quiz, lịch sử RC đầy đủ nối tiếp M2'),
 'm4':('HOÀN CHỈNH (phần lõi)','5 slide + 1 sơ đồ lineage SVG, 9 câu quiz, bám full-text paper Drifting + lịch sử generative model'),
 'm5':('HOÀN CHỈNH (phần lõi)','5 slide, 11 câu quiz, dựng từ 2 NOTE thiết kế mở rộng đã có sẵn'),
 'm6':('HOÀN CHỈNH (phần lõi)','3 phần, 8 câu quiz, bám bảng đánh giá Q1/Q2 thật + 5 textbook đã verify'),
 'm7':('HOÀN CHỈNH','9 phần (8 thế hệ + bảng minh bạch), 22 câu quiz, bám sát README + 8 GiaiThich.md + flag minh bạch demo.ipynb'),
}
cards=''
for mid,slug,title in MODULES:
    st,desc=STATUS[mid]
    cards+=f'<a class="mod-card" href="vi/{slug}/index.html"><div class="num">{mid.upper()}</div><h3>{esc(title)}</h3><p>{esc(desc)}</p><p class="tag">{esc(st)}</p></a>'
body=f'''<div class="usth-banner"><img src="assets/logos/usth_logo.png"><div><div class="t">QRC-Diff-Climate-Modelling</div><div class="s">Quantum Reservoir Computing &amp; Drifting Generative Model — mở rộng nghiên cứu khí hậu USTH Phenikaa</div></div></div>
<p class="lead">Hệ thống tự học mở, 7 module theo dòng lịch sử kiến thức: nền tảng khí hậu (M1) → QRC + lịch sử Reservoir Computing (M2-M3) → Generative model + Drifting (M4) → ứng dụng mở rộng 2 bài báo chính (M5) → literature review + textbook (M6) → 8 thế hệ mô hình thời tiết/khí hậu (M7).</p>
<div class="grid">{cards}</div>
<h2>Trạng thái dự án (trung thực, không che giấu phần chưa xong)</h2>
<p>Cả 7 module đã có nội dung THẬT bám nguồn (paper full-text, NOTE thiết kế có sẵn, bảng literature review, GiaiThich.md) — không còn module nào ở dạng khung/placeholder. <b>Số câu quiz mỗi module (7-22 câu) vẫn CHƯA đạt mục tiêu ban đầu ~150 câu/module</b> — ưu tiên câu có nguồn thật, không nhồi câu filler. Quiz-bias audit: M1 (0.81) và M2 (0.92) có length-bias cần sửa (việc đang làm tiếp); M3-M7 ở mức 0.59-1.0, một số module nhỏ (M3: 7 câu) chưa đủ mẫu để audit ổn định. Notebook verify: M1, M2 (chạy thật, 0 lỗi), M7 (8 notebook demo đã verify từ nguồn). 2 sơ đồ lineage SVG cho M3, M4.</p>
'''
write('index.html',page('Trang chủ',body,0,desc='Hệ thống tự học QRC-Diff-Climate-Modelling, USTH Phenikaa',scripts=['theme.js']))
print('Index cập nhật — không còn module placeholder/stub.')
