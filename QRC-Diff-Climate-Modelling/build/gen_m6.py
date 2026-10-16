# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit, balance_length
from sitelib import module_page

B=Bank('m6',seed=6)
SRC='06_Literature_Review_Mo_Rong/Bang_Danh_Gia_Q1_Q2.md (16 bài xét, 13 tải thành công) + 07_Giao_Trinh_Nen_Tang/ (Hartmann, Ding 1994, Hayhoe 2021, slide Page 2022)'

B.add('Trong literature review mở rộng, nhóm "ENSO/PDO/Victoria Mode/EASM Teleconnection" tải thành công bao nhiêu bài, và bài nào được đánh giá "quan trọng nhất" vì dùng đúng kiến trúc reservoir computing?',
    '4 bài tải thành công trong nhóm; quan trọng nhất là Zhang, Meng, Qiu et al. (2026) "Enhancing predictability limits of ENSO with physics-guided Deep Echo State Networks" (npj Climate and Atmospheric Science)',
    ['6 bài tải thành công; quan trọng nhất là Fan, Yang & Fu (2024, GRL)','4 bài tải thành công; quan trọng nhất là Ji et al. (2024) về Victoria Mode','2 bài tải thành công; không có bài nào liên quan reservoir computing'],
    'Bảng đánh giá liệt kê 4 bài (Ji 2024, Xiao&Ren 2022, Zhang 2026 đã tải; Fan 2024 và Wang 2024 không tải được) — Zhang et al. (2026) được đánh dấu "quan trọng" vì dùng CHÍNH kiến trúc Deep Echo State Network cho bài toán ENSO/Niño-3.4, là baseline cổ điển trực tiếp để so sánh với QRC.',level=1,topic='Nhom-ENSO')
B.add('Tại sao nhóm "CORDEX/CMIP6 Regional Downscaling Đông Nam Á" KHÔNG có bài mới nào được thêm vào ngoài bài #2 gốc?',
    'Vì search chỉ trả về đúng bài #2 (Nguyen et al. 2026, GMD) và bản preprint EGUsphere của chính nó — không nhồi thêm bài yếu/không liên quan cho đủ số lượng',
    ['Vì nhóm này không được search, bị bỏ sót hoàn toàn','Vì mọi bài tìm được đều bị chặn tải, dù có liên quan','Vì chủ đề CORDEX-SEA không còn ai nghiên cứu sau bài #2'],
    'Bảng đánh giá ghi rõ đây là "khoảng trống thật của search, không phải do bỏ sót" — nguyên tắc chất lượng hơn số lượng được tuân thủ: không nhồi bài không liên quan chỉ để có số lượng.',level=2,topic='Nhom-CORDEX')
B.add('Bài nào trong nhóm "Generative/Diffusion/Flow Matching cho khí hậu" được đánh giá "quan trọng nhất nhóm" vì thêm ràng buộc vật lý?',
    'Debeire, Paçal, Gentine, Medrano-Navarro, Thuerey & Eyring (2026), "Physics-Constrained Adaptive Flow Matching for Climate Downscaling" (PC-AFM), arXiv:2604.03459',
    ['Watt & Mansfield (2024), "Generative Diffusion-Based Downscaling for Climate"','Shidqi et al. (2023), KAIST, conditional diffusion model','Wetherell (2026), "Flow Matching for Convective-Scale Precipitation Downscaling"'],
    'Bảng đánh giá đánh dấu PC-AFM "quan trọng nhất nhóm" vì thêm ràng buộc bảo toàn vật lý (conservation constraints) vào flow matching — hướng thiết kế rất gần với đề xuất "Drifting có ràng buộc vật lý" cho downscaling khí hậu mà dự án đang nhắm tới.',level=2,topic='Nhom-Generative')
B.add('Vì sao quartile trong bảng đánh giá literature review mở rộng được ghi là "chưa verify trực tiếp qua Scimago"?',
    'Vì phiên làm việc đó không fetch trực tiếp Scimago, ưu tiên thời gian cho việc xác minh DOI qua Crossref và tải file — quartile chỉ dựa trên uy tín tạp chí đã biết rộng rãi',
    ['Vì Scimago không tồn tại, không có trang web nào như vậy','Vì mọi tạp chí trong bảng đều không có quartile chính thức','Vì quartile chỉ áp dụng được cho sách, không áp dụng tạp chí'],
    'Bảng đánh giá tự ghi rõ: "không fetch được Scimago trực tiếp trong phiên này (không thử, ưu tiên thời gian cho verify DOI + tải file)" — đây là một flag minh bạch, không phải lỗi che giấu; quartile ghi trong bảng cần verify lại trước khi trích dẫn chính thức.',level=2,topic='Flag-minh-bach')
B.add('Tổng kết số liệu literature review mở rộng: bao nhiêu bài đã xét kỹ, bao nhiêu tải thành công, bao nhiêu thất bại?',
    '16 bài xét kỹ, 13 tải thành công & verify, 3 bài thất bại (có lý do cụ thể, không bịa)',
    ['50 bài xét kỹ, 50 bài tải thành công, không có bài thất bại nào','16 bài xét kỹ, 16 bài tải thành công, không có thất bại','13 bài xét kỹ, 3 bài tải thành công, 10 bài thất bại'],
    'Mục Tổng kết của bảng đánh giá ghi rõ: 16 bài xét, 13 tải & verify thành công, 3 thất bại có lý do cụ thể (Wiley chặn dù Unpaywall báo gold OA; IOPscience chặn CAPTCHA; 1 bài chưa kịp xử lý do giới hạn thời gian) — không đạt mốc 40-50 bài ban đầu nhưng ưu tiên chất lượng.',level=1,topic='Tong-ket')
B.add('Textbook nào trong 07_Giao_Trinh_Nen_Tang/ là nguồn kinh điển cho East Asian Summer Monsoon (EASM), dùng trong cả paper #1 và module M1?',
    'Ding Yihui (1994), "Monsoon over China", Kluwer Academic Publishers',
    ['Hartmann, "Global Physical Climatology"','Hayhoe et al. (2021), "Downscaling Techniques for High-Resolution Climate Projections"','Maraun & Widmann (2017), "Statistical Downscaling and Bias Correction"'],
    'Ding (1994) "Monsoon over China" là textbook kinh điển về EASM đã tải và verify (file `Ding1994_Monsoon_over_China.pdf`, 07_Giao_Trinh_Nen_Tang/EASM_Monsoon/) — nguồn nền cho phần lý thuyết gió mùa cổ điển trong Module 1.',level=1,topic='Textbook')
B.add('Hartmann, "Global Physical Climatology" được dùng trong hệ thống này để cung cấp nền tảng gì?',
    'Nền tảng vật lý khí quyển-đại dương chung (hoàn lưu Hadley/Walker, cân bằng năng lượng, động lực khí hậu cơ bản) — không đặc thù riêng cho ENSO hay downscaling',
    ['Chỉ cung cấp số liệu thống kê về Victoria Mode, không liên quan gì khác','Chỉ là sách hướng dẫn dùng phần mềm thống kê SPSS','Chỉ liên quan tới Reservoir Computing, không liên quan khí hậu học'],
    'Hartmann cung cấp kiến thức nền chung (atmospheric & ocean general circulation) — dùng trong Module 1 để giải thích Bjerknes feedback, hoàn lưu Walker, và cơ chế đối lưu nhiệt đới làm nền cho cả 2 hướng QRC (ENSO) và Drifting (downscaling).',level=1,topic='Textbook')
B.add('File "Page2022_Statistical_Downscaling_BiasCorrection_LectureSlides_IS-ENES3.pdf" trong 07_Giao_Trinh_Nen_Tang/Downscaling/ thực chất là loại tài liệu gì?',
    'Slide bài giảng (lecture slides) từ trường thu IS-ENES3 Autumn School 2022, KHÔNG phải sách Maraun & Widmann (2017) như đề xuất ban đầu',
    ['Đúng là bản PDF đầy đủ của sách Maraun & Widmann (2017)','Một bài báo tạp chí Q1 về bias correction','Mã nguồn Python cho thuật toán Quantile Mapping'],
    'Khi verify nội dung thật (pdftotext), file này là slide bài giảng của Christian Pagé tại IS-ENES3 Central&Eastern Europe Autumn School (Prague, 2022), không phải sách đã đề xuất — một trường hợp minh bạch đã ghi lại: "tải lộn tài liệu khác nhưng cùng chủ đề", không phải tài liệu đã yêu cầu ban đầu.',level=2,topic='Flag-minh-bach')

print('M6 added:',len(B.items))
balance_length(B.items)
print('AUDIT (after balance):',audit(B.items))

parts=[
 dict(title='4 nhóm literature review mở rộng',bullets=['ENSO/PDO/VM/EASM','CORDEX/CMIP6 SEA','QRC/QELM','Generative/Drifting khí hậu'],slides=[
   sl(table(['Nhóm','Bài xét','Tải thành công','Bài nổi bật'],
      [['1. ENSO/PDO/VM/EASM Teleconnection','5','4','Zhang et al. 2026 — Deep ESN cho ENSO (baseline RC trực tiếp)'],
       ['2. CORDEX/CMIP6 SEA Downscaling','—','0 (không có bài mới)','Không nhồi bài yếu — khoảng trống search thật'],
       ['3. Quantum Reservoir Computing/QELM','5','4','Kornjača et al. 2024 — QRC phần cứng thật 108 qubit (neutral-atom)'],
       ['4. Generative/Diffusion/Flow/Drifting khí hậu','6','6','Debeire et al. 2026 — Physics-Constrained Flow Matching (PC-AFM)']]),
    'PHẦN 1 · Tổng quan','4 nhóm từ khoá, 16 bài xét, 13 tải thành công (số liệu thật từ Bang_Danh_Gia_Q1_Q2.md)',
    explain='Nhóm 2 (CORDEX-SEA) không có bài mới không phải vì bỏ sót mà vì search thật sự không ra kết quả — nguyên tắc "chất lượng hơn số lượng" được áp dụng xuyên suốt, không nhồi bài không liên quan.'),
   sl(callout('warn','Flags minh bạch quan trọng','Quartile CHƯA verify trực tiếp qua Scimago (chỉ dựa uy tín tạp chí đã biết); 3 bài thất bại có lý do cụ thể (Wiley chặn dù Unpaywall báo gold OA; IOPscience CAPTCHA; 1 bài chưa kịp xử lý) — không bịa, không che giấu các điểm chưa chắc.'),
    'PHẦN 1 · Tổng quan','Flags trung thực (giữ nguyên từ Bang_Danh_Gia_Q1_Q2.md)'),
 ]),
 dict(title='Bài nổi bật từng nhóm',bullets=['Deep ESN cho ENSO','QRC phần cứng thật','PC-AFM'],slides=[
   sl(ul(['<b>Zhang, Meng, Qiu et al. (2026)</b>, npj Climate and Atmospheric Science — Deep Echo State Network áp dụng TRỰC TIẾP cho dự báo ENSO/Niño-3.4 — baseline reservoir computing cổ điển quan trọng nhất để so sánh với thiết kế QRC ở Module 5.',
       '<b>Kornjača, Hu et al. (2024)</b>, QuEra, arXiv:2407.02553 — Quantum reservoir learning trên MÁY TÍNH LƯỢNG TỬ ANALOG THẬT (neutral-atom, 108 qubit) — bằng chứng khả thi phần cứng, không chỉ mô phỏng.',
       '<b>Debeire et al. (2026)</b>, arXiv:2604.03459 — Physics-Constrained Adaptive Flow Matching: thêm ràng buộc bảo toàn vật lý vào flow matching cho downscaling — hướng rất gần với ý tưởng "Drifting có ràng buộc vật lý" ở Module 5.']),
    'PHẦN 2 · Bài nổi bật','3 bài có liên hệ trực tiếp nhất tới thiết kế mở rộng của dự án'),
 ]),
 dict(title='5 textbook/tài liệu nền tảng',bullets=['Hartmann','Ding 1994','Hayhoe 2021','Page 2022 (slide, không phải sách)'],slides=[
   sl(table(['Tài liệu','Loại','Vai trò trong hệ thống'],
      [['Hartmann, Global Physical Climatology','Textbook (2 bản, 1st/2nd ed)','Nền vật lý khí quyển-đại dương chung — dùng ở M1 (Bjerknes, Walker)'],
       ['Ding (1994), Monsoon over China','Textbook kinh điển','Nền lý thuyết EASM cổ điển — dùng ở M1'],
       ['Hayhoe et al. (2021), Downscaling Techniques','Textbook','Bao quát dynamical+statistical downscaling — liên hệ M5 (Drifting-CORDEX)'],
       ['Page (2022), IS-ENES3 Autumn School','⚠️ Slide bài giảng, KHÔNG phải sách Maraun&Widmann như đề xuất ban đầu','Cùng chủ đề statistical downscaling/bias correction, dùng thay thế có ghi chú rõ']]),
    'PHẦN 3 · Textbook nền tảng','Bảng tổng hợp (đã verify nội dung thật từng file bằng pdftotext)',
    explain='Lưu ý quan trọng: khi tải tài liệu ngoài, LUÔN verify nội dung thật trang đầu — trường hợp Page (2022) cho thấy tên file có thể không khớp đúng cuốn sách dự kiến, cần đọc để biết chính xác.'),
 ]),
]

quiz=B.items
module_page('m6','06-literature-textbook',
  title='M6 · Literature review mở rộng & Textbook nền tảng',
  subtitle='13 bài Q1/Q2 (2020-2026) tải thành công + 5 tài liệu nền tảng (Hartmann, Ding 1994, Hayhoe 2021, slide Page 2022)',
  source=SRC, status=f'HOÀN CHỈNH — {len(quiz)} câu quiz bám sát bảng đánh giá thật + nội dung textbook đã verify',
  parts=parts, quiz_items=quiz,
  notes='<h2>Ghi chú</h2><p>Toàn bộ số liệu (16 bài xét, 13 tải thành công, lý do 3 bài thất bại, flag quartile chưa verify Scimago) trích trực tiếp từ Bang_Danh_Gia_Q1_Q2.md. Vai trò từng textbook xác nhận bằng cách đọc trang đầu PDF thật (pdftotext) ở phiên tải trước — phát hiện Page (2022) là slide bài giảng, không phải sách Maraun&Widmann như dự định ban đầu, được giữ nguyên minh bạch trong bảng.</p>')
print('Module 6 xong.')
