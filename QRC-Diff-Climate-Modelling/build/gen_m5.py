# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit, balance_length
from sitelib import module_page

B=Bank('m5',seed=5)
SRC='NOTE_hieu_va_mo_rong_QRC.md (03_Papers_3_Thay_De_Phat_Trien/01_PDO_Victoria_ENSO_EASM_QRC/) + NOTE_hieu_va_mo_rong_Drifting.md (03_Papers_3_Thay_De_Phat_Trien/02_CORDEX_SEA_Downscaling_Drifting/) — thiết kế mở rộng đã có sẵn, dựng lại thành slide+quiz, không tự nghĩ lại từ đầu'

# ---- QRC x paper 1 ----
B.add('Theo NOTE_hieu_va_mo_rong_QRC.md, bài toán cốt lõi về mặt toán học của paper #1 (PDO/VM điều biến ENSO-EASM) là gì?',
    'Quan hệ ENSO↔EASM không dừng (non-stationary) theo thời gian, thay đổi theo pha PDO/VM biến đổi chậm — một dạng điều biến phi tuyến giữa nhiều chuỗi khí hậu có thang thời gian khác nhau',
    ['Quan hệ ENSO-EASM là tuyến tính và không đổi qua mọi thời kỳ','Bài toán chỉ đơn giản là thiếu dữ liệu quan trắc, không có vấn đề toán học nào khác','PDO và VM là 2 tên gọi khác nhau của cùng 1 hiện tượng duy nhất'],
    'NOTE ghi rõ: bài toán cốt lõi là tính KHÔNG DỪNG (non-stationary) của quan hệ ENSO-EASM, bị điều biến bởi PDO/VM biến đổi ở thang thời gian thập kỷ khác hẳn ENSO (thang mùa/năm) — đây chính xác là lý do composite analysis (chia nhóm rời rạc) được paper gốc dùng, và cũng là lý do QRC được đề xuất thay thế.',level=1,topic='Bai-toan-goc')
B.add('Vấn đề/hạn chế của phương pháp "composite analysis" (chia 8 tổ hợp pha rồi tính riêng từng nhóm) mà NOTE chỉ ra là gì?',
    'Giả định quan hệ tuyến tính trong từng nhóm pha, bỏ qua khả năng có trễ phi tuyến thực sự và trí nhớ đa thang thời gian; ngoài ra 165 năm chia 8 nhóm khiến mỗi nhóm chỉ còn ~15-25 năm dữ liệu',
    ['Composite analysis không có hạn chế nào, là phương pháp hoàn hảo','Composite analysis chỉ áp dụng được cho dữ liệu vệ tinh, không áp dụng dữ liệu tái phân tích','Composite analysis yêu cầu máy tính lượng tử để tính toán'],
    'NOTE nêu 2 hạn chế cụ thể: (1) giả định tuyến tính trong từng nhóm, bỏ qua trễ phi tuyến/trí nhớ đa thang thời gian; (2) chia 165 năm thành 8 nhóm làm mỗi nhóm chỉ còn rất ít năm dữ liệu — đây chính là lý do đề xuất QRC học TRỰC TIẾP trên chuỗi liên tục, không rời rạc hoá.',level=1,topic='Han-che')
B.add('Thiết kế QRC cụ thể trong NOTE đề xuất mã hoá bao nhiêu kênh input, và là những kênh nào?',
    '3 kênh: chỉ số ENSO (Niño3.4/ONI), chỉ số PDO, chỉ số VM — mỗi kênh vào 1 nhóm qubit riêng trong explicit register',
    ['1 kênh duy nhất: chỉ gộp cả 3 chỉ số thành 1 số trung bình','5 kênh: thêm cả nhiệt độ không khí và độ ẩm','2 kênh: chỉ ENSO và EASM, bỏ qua PDO/VM'],
    'NOTE đề xuất cụ thể: 3 kênh input (ENSO, PDO, VM) mã hoá riêng vào các nhóm qubit khác nhau trong explicit register — để reservoir có thể học cách TRỘN các chuỗi có thang thời gian khác nhau, thay vì tách riêng như composite analysis gốc.',level=2,topic='Thiet-ke-QRC')
B.add('Vai trò của "quantum memory register" trong thiết kế QRC mở rộng cho paper #1 được NOTE ví như gì?',
    'Giữ "trạng thái điều biến" — đúng vai trò của PDO/VM (biến đổi chậm, thập kỷ) trong khi ENSO biến đổi nhanh (năm); lợi thế là không cần tách pha PDO rồi composite riêng, để reservoir tự học cách trộn trí nhớ nhanh/chậm',
    ['Chỉ dùng để lưu trữ tạm kết quả tính toán trung gian, không có ý nghĩa vật lý nào','Thay thế hoàn toàn vai trò của explicit register, không cần explicit register nữa','Chỉ áp dụng được nếu dữ liệu đã được rời rạc hoá thành 8 nhóm như bài gốc'],
    'Đây là điểm mạnh riêng mà NOTE nhấn mạnh: quantum memory register (không reset) tự nhiên đóng vai trò lưu "ngữ cảnh chậm" (PDO/VM) trong khi explicit register xử lý "input nhanh" (ENSO) — tránh hoàn toàn bước rời rạc hoá 8 nhóm pha của bài gốc.',level=2,topic='Thiet-ke-QRC')
B.add('NOTE yêu cầu baseline nào PHẢI có khi đánh giá thiết kế QRC mở rộng cho paper #1?',
    'Composite/SVD analysis gốc của bài báo, CỘNG THÊM ESN cổ điển (reservoir computing không lượng tử) — để tách riêng "lợi ích của QRC" khỏi "lợi ích của cách tiếp cận reservoir nói chung"',
    ['Chỉ cần so sánh với chính nó ở các siêu tham số khác nhau, không cần baseline ngoài','Chỉ cần baseline là mạng LSTM sâu 50 lớp','Không cần baseline nào, chỉ cần báo cáo kết quả QRC là đủ'],
    'NOTE nêu rõ yêu cầu 2 tầng baseline: (1) phương pháp gốc của bài báo (composite/SVD), và (2) ESN cổ điển — điều này rất quan trọng về mặt khoa học: nếu QRC chỉ thắng composite analysis nhưng thua/bằng ESN cổ điển, thì "lợi ích" chủ yếu đến từ ý tưởng reservoir computing nói chung, không phải từ phần lượng tử.',level=3,topic='Baseline')

# ---- Drifting x paper 2 ----
B.add('Theo NOTE_hieu_va_mo_rong_Drifting.md, vì sao downscaling khí hậu "đúng bài toán gốc" mà Drifting Model nhắm tới?',
    'Vì downscaling về bản chất toán học CŨNG là một pushforward: x_highres = f(x_lowres) hoặc f(ε) với điều kiện trên trường thô CMIP6 — đúng dạng bài toán Drifting Model được thiết kế để giải',
    ['Vì downscaling không có công thức toán học nào, chỉ là quy tắc kinh nghiệm','Vì Drifting Model chỉ hoạt động với dữ liệu dạng văn bản, giống downscaling xử lý text','Vì downscaling và Drifting đều cần đúng 62 lượt chạy mô hình để huấn luyện'],
    'NOTE lập luận: downscaling (biến trường thô GCM/CMIP6 thành trường chi tiết RCM) là một phép pushforward — cùng cấu trúc toán học q=f#p mà Drifting Model nhắm tới, chỉ khác "miền ứng dụng" (khí hậu thay vì ảnh tự nhiên).',level=1,topic='Bai-toan-goc')
B.add('Lợi thế thực tế quan trọng nhất của việc dùng Drifting Model thay thế 1 phần pipeline RCM, theo NOTE, là gì?',
    'Sau khi huấn luyện xong trên 62 mô phỏng RCM đã có, Drifting Model inference chỉ cần 1 bước mạng neural — không cần chạy lại RCM (tốn nhiều tuần trên siêu máy tính) cho mỗi ensemble member mới',
    ['Drifting Model cho kết quả chính xác tuyệt đối 100%, không có sai số nào','Drifting Model không cần bất kỳ dữ liệu huấn luyện nào, học hoàn toàn từ số 0','Drifting Model giúp loại bỏ hoàn toàn nhu cầu dùng CMIP6 làm input'],
    'NOTE nhấn mạnh lợi thế chi phí tính toán: bài báo gốc đã tốn kém chạy 62 mô phỏng RCM (nhiều tuần/lượt trên HPC) — nếu Drifting Model học được ánh xạ từ các mô phỏng này, việc sinh thêm ensemble member mới chỉ cần 1 lần forward pass, rẻ hơn RẤT nhiều so với chạy lại RCM.',level=1,topic='Loi-ich')
B.add('Phát hiện "các mô phỏng cùng họ RCM có cấu trúc sai lệch (bias) giống nhau" của paper #2 được NOTE liên hệ thế nào với Drifting Model?',
    'Đây là lý do để thử Drifting: nếu học được mapping thay vì chạy lại đúng RCM cụ thể, có thể tạo ensemble members đa dạng hơn (giảm phụ thuộc cấu hình RCM cụ thể) với chi phí thấp hơn',
    ['Phát hiện này cho thấy Drifting Model hoàn toàn không áp dụng được cho bài toán này','Phát hiện này không liên quan gì đến thiết kế mở rộng, chỉ là chi tiết phụ','Phát hiện này chứng minh chỉ cần dùng đúng 1 RCM duy nhất là đủ, không cần ensemble'],
    'NOTE chỉ ra: vì các RCM cùng họ chia sẻ bias hệ thống (hạn chế của paper gốc), một mapping học được (Drifting) có thể tạo đa dạng ensemble mà KHÔNG bị ràng buộc vào bias riêng của 1 cấu hình RCM cụ thể — một hướng giảm phụ thuộc cấu trúc mô hình.',level=2,topic='Lien-he-thiet-ke')
B.add('Vùng địa lý nào được NOTE xác định là "test case khó và có giá trị khoa học nhất" để đánh giá Drifting Model so với RCM truyền thống?',
    'Maritime Continent (vùng quần đảo Đông Nam Á) — nơi biến thiên không gian mưa lớn khiến RCM truyền thống khó mô phỏng nhất',
    ['Cao nguyên Tây Tạng — vùng núi cao nhất châu Á','Sa mạc Sahara — vùng khô hạn nhất thế giới','Bắc Cực — vùng có biến đổi khí hậu nhanh nhất toàn cầu'],
    'Paper #2 (gốc) đã chỉ ra Maritime Continent là vùng khó mô phỏng nhất do biến thiên không gian mưa lớn (đảo, eo biển hẹp); NOTE xác định đây chính là test case có giá trị khoa học cao nhất để xem Drifting Model có vượt được hạn chế này không.',level=2,topic='Test-case')
B.add('"Network f" trong thiết kế Drifting mở rộng cho downscaling CORDEX-SEA được NOTE đề xuất dùng kiến trúc nào làm backbone?',
    'U-Net hoặc Vision Transformer, thay cho kiến trúc ảnh tự nhiên của paper gốc',
    ['Chỉ dùng 1 lớp tuyến tính đơn giản duy nhất, không có kiến trúc deep learning nào','Buộc phải dùng chính xác kiến trúc ảnh ImageNet của paper gốc, không được thay đổi','Cây quyết định (decision tree), không dùng mạng neural'],
    'NOTE đề xuất network f có kiến trúc 1-pass (không lặp, giống paper gốc) nhưng đổi backbone phù hợp dữ liệu khí hậu dạng lưới không gian: U-Net hoặc Vision Transformer, thay cho kiến trúc tối ưu cho ảnh tự nhiên (ImageNet) của paper Drifting gốc.',level=2,topic='Kien-truc')
B.add('Việc cần làm "trước khi code" được NOTE liệt kê cho hướng Drifting-CORDEX bao gồm bước nào?',
    'Trích xuất bộ 62 (hoặc 15 đã qua benchmark) mô phỏng từ Zenodo records công bố kèm bài, và xác định đúng cặp input-output theo config đã benchmark (tránh trộn lẫn các RCM có bias khác hệ thống)',
    ['Không cần làm gì thêm, có thể code ngay lập tức mà không cần dữ liệu','Phải tự chạy lại toàn bộ 62 mô phỏng RCM từ đầu trên máy cá nhân','Phải chờ paper #2 công bố phiên bản mới trước khi bắt đầu'],
    'NOTE liệt kê rõ các bước chuẩn bị: lấy dữ liệu từ Zenodo (đã công bố kèm bài, không cần tự chạy RCM), xác định đúng cặp dữ liệu theo config đã benchmark, và trao đổi với đồng tác giả (thầy Thành) về khả năng tiếp cận dữ liệu/code gốc trước khi downscale lại.',level=1,topic='Viec-can-lam')

print('M5 added:',len(B.items))
balance_length(B.items)
print('AUDIT (after balance):',audit(B.items))

parts=[
 dict(title='Paper #1 + QRC: bài toán và hạn chế cũ',bullets=['Non-stationary ENSO-EASM','Composite analysis & hạn chế'],slides=[
   sl(callout('info','Bài toán cốt lõi (NOTE)','Quan hệ ENSO↔EASM KHÔNG DỪNG (non-stationary) theo thời gian — bị điều biến bởi PDO/VM (thang thời gian thập kỷ) trong khi ENSO biến đổi theo mùa/năm. Đây là dạng "điều biến phi tuyến giữa nhiều chuỗi khí hậu có thang thời gian khác nhau".')
    +callout('warn','Hạn chế của composite analysis gốc','(1) Giả định tuyến tính trong từng nhóm pha; (2) 165 năm chia 8 nhóm ⇒ mỗi nhóm chỉ còn ~15-25 năm dữ liệu — dữ liệu quá ít để học quan hệ phi tuyến phức tạp.'),
    'PHẦN 1 · Paper #1','Vì sao cần phương pháp mới hơn composite analysis'),
 ]),
 dict(title='Thiết kế QRC mở rộng cho paper #1',bullets=['3 kênh input','Explicit vs memory register','Baseline bắt buộc'],slides=[
   sl(table(['Thành phần thiết kế','Vai trò'],
      [['Explicit register (3 kênh)','ENSO (Niño3.4/ONI), PDO, VM — mỗi chỉ số 1 nhóm qubit riêng, giữ ký ức ngắn hạn tường minh'],
       ['Quantum memory register','Giữ "trạng thái điều biến" chậm (PDO/VM) — không cần tách pha rồi composite như bài gốc'],
       ['Readout','Hồi quy tuyến tính dự báo EASM index / mưa mùa hè, lead time 1-2 mùa'],
       ['Baseline bắt buộc','Composite/SVD gốc + ESN cổ điển (tách "lợi ích QRC" khỏi "lợi ích RC nói chung")']]),
    'PHẦN 2 · Thiết kế QRC','4 thành phần thiết kế (từ NOTE_hieu_va_mo_rong_QRC.md)',
    explain='Ý tưởng cốt lõi: để reservoir TỰ HỌC cách trộn 1 chuỗi nhanh (ENSO) với 2 chuỗi chậm (PDO, VM), thay vì nhà nghiên cứu phải tự tay chia 8 nhóm rồi phân tích riêng từng nhóm như bài gốc.'),
   sl(callout('warn','Việc chưa xong (trung thực)','Đây mới là THIẾT KẾ Ý TƯỞNG — NOTE gốc đánh dấu rõ 3 mục "chưa làm": (1) đọc Methods lấy chính xác công thức VM index + nguồn SST (HadISST hay ERSST?); (2) xác nhận train trên chuỗi liên tục 165 năm, không rời rạc hoá 8 nhóm; (3) liên hệ thầy Dũng/thầy Thành xin index đã xử lý sẵn.'),
    'PHẦN 2 · Thiết kế QRC','Checklist trước khi code (chưa hoàn thành)'),
 ]),
 dict(title='Paper #2 + Drifting: downscaling là 1 pushforward',bullets=['x_highres=f(x_lowres)','62 mô phỏng RCM có sẵn','Bias hệ thống theo họ RCM'],slides=[
   sl(formula('Downscaling như pushforward (NOTE)','x_highres = f(x_lowres)  hoặc  x_highres = f(ε | x_lowres)',
      [('x_lowres','trường CMIP6 thô (điều kiện/conditioning)'),('x_highres','trường độ phân giải cao, mục tiêu khớp RCM output thật'),('62 mô phỏng','đã có sẵn từ paper #2 — dùng làm "ground truth" huấn luyện, không cần chạy RCM lại sau khi train xong')]),
    'PHẦN 3 · Thiết kế Drifting','Downscaling = bài toán pushforward đúng dạng Drifting Model'),
   sl(callout('good','Lợi ích chi phí tính toán','62 mô phỏng RCM (nhiều tuần/lượt trên HPC) dùng 1 LẦN để huấn luyện Drifting; sau đó sinh ensemble member mới chỉ cần 1 forward pass — rẻ hơn rất nhiều so với chạy lại RCM.')
    +callout('info','Vùng test khó nhất','Maritime Continent (quần đảo Đông Nam Á) — RCM truyền thống khó mô phỏng nhất do biến thiên không gian mưa lớn — NOTE xác định đây là test case giá trị khoa học cao nhất.'),
    'PHẦN 3 · Thiết kế Drifting','Lợi ích và test case ưu tiên'),
   sl(ul(['Network f: U-Net hoặc Vision Transformer (thay backbone ảnh tự nhiên của paper gốc)','Input: trường CMIP6 thô + conditioning (model ID, kịch bản phát thải)','Output: trường RCM (dùng 15 mô phỏng đã qua benchmark — "đáng tin cậy nhất")','Đánh giá: FID/CRPS/RMSE so với RCM thật, đặc biệt ở Maritime Continent'])
    +callout('warn','Việc chưa xong (trung thực)','Chưa trích xuất dữ liệu 62 mô phỏng từ Zenodo, chưa xác định cặp input-output đúng theo config benchmark, chưa liên hệ thầy Thành về khả năng tiếp cận dữ liệu/code gốc.'),
    'PHẦN 3 · Thiết kế Drifting','Kiến trúc cụ thể + checklist chưa hoàn thành'),
 ]),
]

quiz=B.items
module_page('m5','05-ung-dung-mo-rong-2-bai-bao',
  title='M5 · Ứng dụng mở rộng: QRC cho paper #1, Drifting cho paper #2',
  subtitle='Dựng từ thiết kế đã có sẵn trong NOTE_hieu_va_mo_rong_QRC.md và NOTE_hieu_va_mo_rong_Drifting.md',
  source=SRC, status=f'HOÀN CHỈNH — {len(quiz)} câu quiz, dùng lại nguyên thiết kế đã có, không tự nghĩ lại',
  parts=parts, quiz_items=quiz,
  notes='<h2>Ghi chú</h2><p>Toàn bộ nội dung module này lấy TRỰC TIẾP từ 2 file NOTE đã có sẵn trong dự án (không tự thiết kế lại từ đầu). Cả 2 thiết kế đều còn ở mức Ý TƯỞNG — chưa code, chưa chạy benchmark — các checklist "việc chưa xong" được giữ nguyên trung thực trong slide, không che giấu.</p>')
print('Module 5 xong.')
