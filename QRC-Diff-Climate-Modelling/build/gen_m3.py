# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit, balance_length
from sitelib import module_page

B=Bank('m3',seed=3)
SRC='Jaeger (2001, ESN), Maass et al. (2002, LSM), Fujii & Nakajima (2017, QRC) — lịch sử ngành, đối chiếu kiến trúc spin-chain đã học ở M2 (Ramon-Escandell et al. 2026, arXiv:2608.28440v1)'

B.add('Năm 2001, Herbert Jaeger đề xuất Echo State Network để giải quyết vấn đề gì của RNN?',
    'Vanishing/exploding gradient khi lan truyền ngược qua nhiều bước thời gian (BPTT)',
    ['Thiếu dữ liệu huấn luyện đủ lớn cho RNN','Chi phí lưu trữ RAM khi huấn luyện RNN trên GPU','Không có framework phần mềm nào hỗ trợ RNN khi đó'],
    'ESN (Jaeger 2001) né hoàn toàn backpropagation through time: giữ 1 "reservoir" ngẫu nhiên CỐ ĐỊNH, chỉ huấn luyện 1 lớp readout tuyến tính bằng hồi quy — loại bỏ vanishing gradient vì reservoir không bao giờ nhận gradient.',level=1,topic='ESN')
B.add('Liquid State Machine (Maass, Natschläger & Markram, 2002) khác ESN ở điểm nào về "chất liệu" reservoir?',
    'LSM dùng mạng nơ-ron xung (spiking neural network) sinh học làm reservoir, còn ESN dùng mạng nơ-ron hồi quy liên tục (continuous-valued)',
    ['LSM không có readout, chỉ có reservoir đơn thuần','LSM chỉ xử lý được ảnh tĩnh, không xử lý chuỗi thời gian','LSM yêu cầu huấn luyện toàn bộ reservoir bằng gradient descent'],
    'LSM và ESN ra đời độc lập năm 2001-2002, hội tụ về cùng 1 nguyên lý chung (reservoir cố định + readout tuyến tính) nhưng từ 2 xuất phát khác nhau: LSM lấy cảm hứng sinh học (neuron xung), ESN lấy cảm hứng kỹ thuật (mạng hồi quy liên tục) — cả 2 cùng đặt nền cho thuật ngữ chung "Reservoir Computing".',level=1,topic='LSM')
B.add('"Echo state property" là điều kiện gì đối với một reservoir?',
    'Trạng thái reservoir phải hội tụ về cùng 1 quỹ đạo, bất kể trạng thái khởi tạo ban đầu, miễn là input giống nhau đủ lâu',
    ['Reservoir phải có đúng 100 neuron để hoạt động ổn định','Reservoir phải được huấn luyện bằng gradient trước khi dùng readout','Reservoir phải chỉ nhận input nhị phân 0/1, không nhận giá trị liên tục'],
    'Echo state property đảm bảo reservoir "quên" được điều kiện khởi tạo tuỳ ý của nó — nếu không có tính chất này, output sẽ phụ thuộc vào trạng thái ban đầu ngẫu nhiên thay vì chỉ phụ thuộc vào input, khiến reservoir vô dụng cho việc huấn luyện 1 readout chung.',level=2,topic='Theory')
B.add('Vì sao "fading memory" (trí nhớ phai dần) là điều kiện CẦN cho một reservoir tốt, không phải "nhớ mãi mãi"?',
    'Vì nếu reservoir nhớ mãi mọi input cũ (không suy giảm), nó sẽ không phân biệt được trạng thái hiện tại với quá khứ xa, mất khả năng phản ứng với input mới',
    ['Vì phần cứng máy tính không đủ RAM để lưu trữ vĩnh viễn','Vì luật pháp về bảo mật dữ liệu yêu cầu xoá dữ liệu cũ','Vì "nhớ mãi mãi" chỉ khả thi với reservoir lượng tử, không khả thi với reservoir cổ điển'],
    'Một reservoir lý tưởng cần suy giảm ảnh hưởng input cũ dần (không đột ngột, không vĩnh viễn) — đây là sự cân bằng giữa "nhớ đủ để hữu ích" và "không bị kẹt vào quá khứ", khác hẳn lý do kỹ thuật về phần cứng.',level=2,topic='Theory')
B.add('Fujii & Nakajima (2017) đề xuất Quantum Reservoir Computing dựa trên ý tưởng gì?',
    'Thay reservoir cổ điển (mạng nơ-ron ngẫu nhiên) bằng một hệ lượng tử nhiều hạt tiến hoá unitary, giữ nguyên nguyên tắc "chỉ huấn luyện readout"',
    ['Thay readout tuyến tính bằng 1 mạng nơ-ron sâu nhiều lớp','Bỏ hoàn toàn khái niệm reservoir, chỉ dùng thuật toán lượng tử thuần','Dùng máy tính lượng tử để tăng tốc huấn luyện gradient của RNN cổ điển'],
    'QRC (Fujii & Nakajima 2017) là bước chuyển trực tiếp từ ESN/LSM: giữ đúng triết lý "reservoir cố định, chỉ train readout", nhưng thay "chất liệu" reservoir từ mạng nơ-ron cổ điển sang một hệ lượng tử N qubit tiến hoá theo động lực unitary, không gian trạng thái 2^N chiều.',level=1,topic='QRC-origin')
B.add('Kiến trúc spin-chain tunable memory đã học ở Module 2 (Ramon-Escandell et al. 2026) phát triển THÊM gì so với QRC gốc của Fujii & Nakajima (2017)?',
    'Thêm khả năng điều chỉnh (tunable) tỉ lệ giữa trí nhớ tường minh (explicit register) và trí nhớ lượng tử ngầm (quantum memory register) bằng cách thay đổi độ dài mã hoá lại w',
    ['Thay hoàn toàn mô hình Ising bằng mô hình Heisenberg','Loại bỏ readout tuyến tính, dùng readout phi tuyến sâu','Chuyển từ reservoir lượng tử về lại reservoir cổ điển hoàn toàn'],
    'Đây là điểm nối tiếp trực tiếp giữa M2 và M3: QRC gốc (2017) đã có ý tưởng "reservoir lượng tử", còn paper ở M2 (2026) đóng góp thêm cơ chế TUNABLE — cho phép đánh đổi linh hoạt giữa 2 dạng trí nhớ tại CÙNG kích thước hệ N, thống nhất luôn QRC và QELM vào 1 kiến trúc.',level=3,topic='Lien-ket-M2')
B.add('Dạng bài toán vật lý cổ điển nào đã dùng Reservoir Computing TRƯỚC khi có QRC (ví dụ gợi ý từ tên "Reservoir Computing trong vật lý")?',
    'Dự báo chuỗi thời gian hỗn loạn (chaotic time-series), ví dụ hệ Lorenz-63, dao động phi tuyến',
    ['Phân loại ảnh y tế 2 chiều tĩnh','Giải phương trình đại số tuyến tính thuần','Mô phỏng Monte Carlo cho bài toán tổ hợp rời rạc'],
    'RC cổ điển (ESN) được áp dụng rộng cho các hệ động lực hỗn loạn/phi tuyến (Lorenz-63, laser chaotic...) từ trước khi QRC ra đời — đây chính là lý do RC (cả cổ điển và lượng tử) phù hợp tự nhiên với chuỗi khí hậu ENSO/PDO có đặc tính chaotic tương tự.',level=2,topic='RC-physics')

print('M3 added:',len(B.items))
balance_length(B.items)
print('AUDIT (after balance):',audit(B.items))

parts=[
 dict(title='Vấn đề của RNN cổ điển',bullets=['BPTT','Vanishing/exploding gradient'],slides=[
   sl(ul(['RNN huấn luyện bằng backpropagation through time (BPTT): lan truyền gradient ngược qua MỌI bước thời gian','Chuỗi dài → gradient nhân lặp lại nhiều lần → tiến về 0 (vanishing) hoặc bùng nổ (exploding)','Hệ quả: RNN cổ điển khó học được quan hệ phụ thuộc xa (long-range dependency)']),
    'PHẦN 1 · Vấn đề gốc','Vì sao RNN cổ điển khó huấn luyện với chuỗi dài',
    explain='Hình dung: mỗi bước thời gian là 1 lớp mạng. Chuỗi 1000 bước ≈ mạng 1000 lớp — lan truyền gradient qua 1000 lớp liên tiếp hầu như luôn làm gradient "chết" hoặc "nổ" nếu không có kỹ thuật đặc biệt (LSTM/GRU cũng chỉ giảm nhẹ vấn đề, không loại bỏ hoàn toàn).'),
 ]),
 dict(title='Reservoir Computing ra đời: ESN & LSM',bullets=['Jaeger 2001','Maass 2002','Nguyên tắc chung'],slides=[
   sl(table(['','Echo State Network (Jaeger, 2001)','Liquid State Machine (Maass, 2002)'],
      [['Chất liệu reservoir','Mạng nơ-ron hồi quy liên tục, trọng số ngẫu nhiên cố định','Mạng nơ-ron xung (spiking), lấy cảm hứng sinh học'],
       ['Huấn luyện','Chỉ readout, bằng hồi quy tuyến tính (ridge regression)','Chỉ readout, tương tự ESN'],
       ['Nguyên tắc chung','"Reservoir cố định + readout tuyến tính" → tránh BPTT hoàn toàn','Giống ESN']]),
    'PHẦN 2 · ESN & LSM','Hai dòng độc lập, cùng hội tụ về 1 nguyên lý',
    explain='Điều thú vị: 2 nhóm nghiên cứu độc lập (kỹ thuật vs sinh học) cùng phát hiện ra ý tưởng giống nhau trong vòng 1 năm — dấu hiệu cho thấy đây là một nguyên lý toán học sâu, không phải trùng hợp.'),
   sl(formula('Hai điều kiện lý thuyết nền tảng','Echo state property + Fading memory',
      [('Echo State Property','trạng thái hội tụ về 1 quỹ đạo bất kể khởi tạo, khi input giống nhau đủ lâu'),('Fading memory','ảnh hưởng input cũ suy giảm dần — không mất ngay, không tồn tại vĩnh viễn')]),
    'PHẦN 2 · ESN & LSM','Điều kiện để reservoir "đáng tin cậy"'),
 ]),
 dict(title='Từ RC cổ điển trong vật lý tới QRC',bullets=['RC cho hệ chaotic','QRC (Fujii & Nakajima 2017)','Nối tiếp sang M2'],slides=[
   sl('<p>Trước QRC, Reservoir Computing cổ điển đã được dùng rộng rãi để dự báo các hệ ĐỘNG LỰC HỖN LOẠN trong vật lý (Lorenz-63, dao động phi tuyến, laser chaotic...) — cùng một lớp bài toán "time-series có trí nhớ, phi tuyến, nhạy điều kiện ban đầu" mà sau này QRC và cả chuỗi khí hậu ENSO/PDO (Module 1) đều thuộc về.</p>'
    +callout('good','Fujii & Nakajima (2017)','Thay "chất liệu" reservoir từ mạng nơ-ron cổ điển sang hệ lượng tử N qubit tiến hoá unitary — giữ NGUYÊN nguyên tắc "chỉ train readout", chỉ đổi không gian trạng thái từ N chiều (cổ điển) sang 2^N chiều (lượng tử).'),
    'PHẦN 3 · QRC','RC cổ điển trong vật lý → QRC lượng tử'),
   sl(diag('../../diagrams/rc_lineage.svg','Dòng lịch sử Reservoir Computing','RNN/BPTT (vấn đề) → ESN/LSM (2001-02) → fading memory (lý thuyết) → QRC (2017) → spin-chain tunable (2026, Module 2)')
    +callout('info','Nối tiếp Module 2','Kiến trúc spin-chain explicit/memory register đã học ở M2 (Ramon-Escandell 2026) là điểm MỚI NHẤT của dòng lịch sử này: thống nhất QRC và QELM vào 1 kiến trúc tunable — không lặp lại chi tiết Hamiltonian ở đây, xem lại M2.'),
    'PHẦN 3 · QRC','Sơ đồ dòng lịch sử đầy đủ (xem M2 để biết chi tiết Hamiltonian)'),
 ]),
]

quiz=B.items
module_page('m3','03-reservoir-computing-lineage',
  title='M3 · Lịch sử Reservoir Computing: RNN → ESN/LSM → QRC',
  subtitle='Dòng lịch sử đầy đủ dẫn tới kiến trúc spin-chain tunable memory đã học ở M2 — không lặp lại nội dung M2',
  source=SRC, status=f'HOÀN CHỈNH — {len(quiz)} câu quiz, bám lịch sử RC chuẩn ngành + đối chiếu paper QRC M2',
  parts=parts, quiz_items=quiz,
  notebook_links=[('m2_verify_rc_narma10.ipynb (ESN cổ điển — dùng chung với M2, minh hoạ đúng nguyên tắc "reservoir cố định + readout tuyến tính" của cả dòng lịch sử này)','../../notebooks/m2_verify_rc_narma10.ipynb')],
  notes='<h2>Ghi chú</h2><p>Module này KHÔNG lặp lại Hamiltonian/explicit-memory register đã trình bày chi tiết ở M2 — chỉ đặt kiến trúc đó vào đúng vị trí trong dòng lịch sử (1990s BPTT problem → 2001-02 ESN/LSM → 2017 QRC → 2026 spin-chain tunable). Muốn xem chi tiết công thức, quay lại M2.</p>')
print('Module 3 xong.')
