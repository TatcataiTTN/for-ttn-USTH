import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit, balance_length
from sitelib import module_page

B=Bank('m2',seed=2)
SRC='Ramon-Escandell, Riera & Płodzień (2026), arXiv:2608.28440v1, "From quantum reservoirs to quantum extreme learning machines through a nearest-neighbor spin chain with tunable quantum memory" (full-text verify) + lịch sử Reservoir Computing (Jaeger 2001, Maass 2002)'

B.add('Hamiltonian của quantum reservoir trong paper (Mixed-Field Ising Model, Eq.1) có dạng nào?',
    'H = J·Σ XᵢXᵢ₊₁ + h_z·Σ Zᵢ + h_x·Σ Xᵢ (tương tác lân cận gần nhất + 2 trường đồng nhất)',
    ['H = J·Σ ZᵢZᵢ₊₁ (chỉ tương tác Ising thuần, không có trường ngoài)','H = Σ Xᵢ⊗Xⱼ cho mọi cặp i,j (tương tác toàn kết nối, không phải lân cận gần)','H = h·Σ Yᵢ (chỉ có 1 trường theo trục Y)'],
    'Paper định nghĩa chính xác H=JΣXᵢXᵢ₊₁+h_zΣZᵢ+h_xΣXᵢ — mô hình Mixed-Field Ising (MFIM) 1 chiều, biên hở (open boundary), với J là coupling lân cận gần theo trục x, h_x/h_z là 2 trường đồng nhất.',level=1,topic='Hamiltonian')
B.add('"Explicit register" trong kiến trúc QRC của paper này dùng để làm gì?',
    'Giữ w qubit bị ghi đè (reset) mỗi bước thời gian, mã hoá tường minh các input gần nhất (trí nhớ ngắn hạn)',['Lưu trữ vĩnh viễn toàn bộ lịch sử input từ đầu tới cuối, không bao giờ reset','Chỉ dùng để đo lường kết quả cuối cùng, không tham gia mã hoá input','Là một register cổ điển (classical register), không phải qubit'],
    'Explicit register gồm w qubit được ghi đè lại (re-encode) ở MỖI bước — giữ "trí nhớ tường minh" về các input gần nhất; phần còn lại (N-w qubit) không bị reset, tạo thành "quantum memory register" giữ trí nhớ dài hạn qua trạng thái lượng tử tiến hoá.',level=1,topic='Architecture')
B.add('Khi độ dài mã hoá w tăng (explicit register rộng hơn), điều gì xảy ra với "quantum memory register"?',
    'Quantum memory register hẹp lại (N-w qubit), đánh đổi trí nhớ lượng tử ngầm lấy trí nhớ tường minh ngắn hạn',['Quantum memory register không đổi vì 2 phần độc lập hoàn toàn','Toàn bộ hệ chuyển thành classical reservoir','Số qubit tổng N tự động tăng lên để bù lại'],
    'Ở kích thước hệ N cố định, w (explicit) và N-w (memory) là 2 phần bù nhau của cùng N qubit — tăng w nghĩa là giảm memory register, đánh đổi trực tiếp giữa 2 dạng lưu trữ trí nhớ.',level=2,topic='Architecture')
B.add('Paper phát hiện trí nhớ lượng tử ngầm (quantum memory register) là "essential" (cần thiết) khi nào?',
    'Khi bài toán cần "nhìn xa vào quá khứ" (long-range memory task)',['Luôn luôn cần thiết, bất kể đặc tính bài toán','Chỉ cần thiết khi N nhỏ hơn 4 qubit','Không bao giờ cần thiết, giới hạn reset luôn tốt hơn'],
    'Kết quả chính: với tác vụ cần trí nhớ dài (long memory), reservoir cần quantum memory register (N-w lớn); với tác vụ chỉ cần lịch sử ngắn, giới hạn "memoryless reset" (w=N, không còn memory register) đã đủ tốt.',level=2,topic='Architecture')
B.add('Hai benchmark chuẩn được dùng để đánh giá QRC trong paper này là gì?',
    'NARMA-10 và Santa Fe laser series',['MNIST và CIFAR-10','ImageNet và COCO','ENSO index và PDO index (dữ liệu khí hậu)'],
    'Paper dùng 2 benchmark time-series kinh điển của reservoir computing: NARMA-10 (chuỗi phi tuyến tổng hợp bậc 10) và Santa Fe laser series (chuỗi hỗn loạn thực nghiệm) — KHÔNG phải dữ liệu khí hậu; việc áp dụng sang ENSO/PDO là phần MỞ RỘNG của dự án này, chưa có trong paper gốc.',level=1,topic='Benchmark')
B.add('Phương pháp tối ưu siêu tham số (Δt, J, h_x, h_z) dùng trong paper là gì?',
    'Bayesian Optimization qua Tree-Parzen Estimator (TPE)',['Grid search toàn bộ không gian tham số','Random search thuần','Thuật toán di truyền (genetic algorithm)'],
    'Paper dùng Bayesian Optimization (cây Tree-Parzen) để tối ưu riêng thời gian tiến hoá Δt và các tham số Hamiltonian cho MỖI độ dài mã hoá w khác nhau, đảm bảo so sánh công bằng giữa các cấu hình.',level=2,topic='Optimization')
B.add('Toán tử tiến hoá thời gian U trong 1 bước QRC được biểu diễn như thế nào?',
    'U = e^(−iHΔt), với H là Hamiltonian cố định của reservoir, Δt là thời gian tiến hoá giữa các bước input',['U = H·Δt (toán tử tuyến tính đơn giản, không có mũ)','U là ma trận ngẫu nhiên thay đổi mỗi bước, không liên quan H','U chỉ áp dụng cho explicit register, không áp dụng cho memory register'],
    'Toàn bộ chuỗi qubit (cả explicit và memory register) tiến hoá CÙNG dưới U=e^{-iHΔt} theo cùng 1 Hamiltonian cố định — đây chính là nguyên lý "fixed reservoir" của QRC: không có tham số nào trong H/U được huấn luyện bằng gradient, chỉ phần readout tuyến tính phía sau được huấn luyện.',level=2,topic='Hamiltonian')

# ---- lineage RC (kiến thức nền, không trích riêng số liệu paper) ----
B.add('Reservoir Computing (RC) ra đời để giải quyết vấn đề gì của huấn luyện RNN truyền thống?',
    'Vanishing/exploding gradient khi lan truyền ngược qua nhiều bước thời gian (backpropagation through time)',['Thiếu dữ liệu huấn luyện','Chi phí lưu trữ RAM của GPU','Không có framework nào hỗ trợ RNN'],
    'RNN cổ điển huấn luyện bằng BPTT (backpropagation through time) gặp vanishing/exploding gradient khi chuỗi dài. Reservoir Computing né vấn đề này bằng cách CỐ ĐỊNH phần "reservoir" (không huấn luyện gradient), chỉ huấn luyện 1 lớp đọc (readout) tuyến tính phía sau — ý tưởng gốc của Echo State Network (Jaeger 2001) và Liquid State Machine (Maass 2002).',level=1,topic='RC-lineage')
B.add('Echo State Network (Jaeger, 2001) và Liquid State Machine (Maass, 2002) có điểm chung nền tảng nào?',
    'Cả hai dùng một mạng động lực cố định (không huấn luyện) làm reservoir, chỉ huấn luyện lớp đọc tuyến tính — đặt nền cho khái niệm Reservoir Computing nói chung',['Cả hai đều là mô hình lượng tử','Cả hai chỉ hoạt động trên ảnh tĩnh, không xử lý chuỗi thời gian','Cả hai yêu cầu huấn luyện end-to-end bằng gradient descent'],
    'ESN (mạng nơ-ron hồi quy ngẫu nhiên, liên tục) và LSM (mạng nơ-ron xung sinh học) là 2 dòng độc lập cùng dẫn tới khái niệm chung "Reservoir Computing": một hệ động lực phức tạp, cố định, có "fading memory" (trí nhớ phai dần), kết hợp 1 readout tuyến tính dễ huấn luyện.',level=1,topic='RC-lineage')
B.add('"Fading memory" (trí nhớ phai dần) là thuộc tính gì của một reservoir tốt?',
    'Ảnh hưởng của input cũ giảm dần theo thời gian nhưng không biến mất đột ngột — đủ "nhớ" quá khứ gần mà không "kẹt" vào trạng thái cũ mãi mãi',['Reservoir quên hoàn toàn mọi input ngay sau 1 bước','Reservoir nhớ y nguyên mọi input từ đầu tới cuối, không suy giảm','Thuộc tính chỉ áp dụng cho dữ liệu hình ảnh, không áp dụng chuỗi thời gian'],
    'Fading memory (cùng với echo state property) là điều kiện lý thuyết để 1 reservoir hoạt động ổn định: ảnh hưởng của input ở xa quá khứ phải suy giảm dần, không được khuếch đại vô hạn hay đứng yên vĩnh viễn — nếu không hệ sẽ hỗn loạn (chaotic, mất khả năng dự đoán) hoặc "đông cứng" (mất khả năng phân biệt input mới).',level=2,topic='RC-lineage')
B.add('Quantum Reservoir Computing (QRC, Fujii & Nakajima 2017) khác Echo State Network cổ điển ở điểm cốt lõi nào?',
    'Reservoir là một hệ lượng tử nhiều hạt tiến hoá unitary (không gian Hilbert tăng theo 2^N), thay cho mạng nơ-ron cổ điển với không gian trạng thái tuyến tính theo kích thước',['QRC không có readout, chỉ có reservoir','QRC không xử lý được chuỗi thời gian, chỉ xử lý ảnh tĩnh','QRC luôn cần huấn luyện gradient toàn bộ reservoir như RNN'],
    'QRC thay "biển neuron cổ điển" bằng một hệ lượng tử N qubit tiến hoá theo động lực unitary cố định — không gian trạng thái khả dụng tăng theo 2^N (lợi thế biểu diễn tiềm năng), trong khi vẫn giữ nguyên tắc RC cốt lõi: reservoir cố định, chỉ readout được huấn luyện.',level=2,topic='RC-lineage')
B.add('Quantum Extreme Learning Machine (QELM) liên hệ với QRC như thế nào, theo paper đang xét?',
    'QRC và QELM là 2 giới hạn của CÙNG một kiến trúc spin-chain, chỉ khác nhau ở độ dài mã hoá lại (re-encoding length) w',['QELM và QRC là 2 phương pháp hoàn toàn tách biệt, không có liên hệ toán học','QELM chỉ dùng cho bài toán phân loại ảnh, QRC chỉ dùng cho time-series, không thể thống nhất','QELM là phiên bản cổ điển (không lượng tử) của QRC'],
    'Đây là một trong những đóng góp lý thuyết quan trọng của paper: cùng kiến trúc explicit/memory register, khi w=N (reset toàn bộ mỗi bước, không có memory register) hệ trở thành QELM (extreme learning machine lượng tử — không có trí nhớ qua các bước); khi w<N có giữ lại memory register, hệ là QRC đầy đủ.',level=3,topic='Architecture')

print('M2 added:',len(B.items))
balance_length(B.items)
print('AUDIT (after balance):',audit(B.items))

parts=[
 dict(title='Lịch sử Reservoir Computing',bullets=['Vấn đề BPTT/vanishing gradient','ESN & LSM','Fading memory & echo state property'],slides=[
   sl(ul(['RNN cổ điển huấn luyện bằng BPTT → vanishing/exploding gradient khi chuỗi dài','Echo State Network (Jaeger, 2001): reservoir ngẫu nhiên cố định + readout tuyến tính huấn luyện bằng hồi quy tuyến tính (ridge regression)','Liquid State Machine (Maass, 2002): mạng nơ-ron xung sinh học làm reservoir, cùng nguyên lý "chỉ huấn luyện readout"','Cả 2 hội tụ về khái niệm chung: Reservoir Computing']),
    'PHẦN 1 · Lịch sử','Từ vanishing gradient tới Reservoir Computing',
    explain='Ý tưởng cốt lõi của RC rất đơn giản: thay vì cố huấn luyện TOÀN BỘ mạng (dễ gặp vanishing gradient), ta giữ phần "não giữa" (reservoir) cố định ngẫu nhiên — chỉ cần nó đủ "giàu" về động lực — rồi chỉ huấn luyện 1 lớp đọc tuyến tính rất đơn giản ở cuối.'),
   sl(formula('Điều kiện lý thuyết cho reservoir tốt','Fading memory + Echo State Property',
      [('Fading memory','ảnh hưởng input cũ suy giảm dần, không biến mất đột ngột, không khuếch đại vô hạn'),('Echo State Property','trạng thái reservoir hội tụ về 1 quỹ đạo duy nhất bất kể trạng thái khởi tạo, khi đủ thời gian')]),
    'PHẦN 1 · Lịch sử','Hai điều kiện lý thuyết nền tảng'),
 ]),
 dict(title='Từ Echo State Network tới QRC',bullets=['Hệ lượng tử nhiều hạt làm reservoir','QRC (Fujii & Nakajima 2017)','QRC ↔ QELM: cùng 1 kiến trúc'],slides=[
   sl('<p>QRC thay mạng nơ-ron cổ điển bằng một hệ lượng tử N qubit tiến hoá unitary — không gian Hilbert 2^N tăng theo cấp lũy, lợi thế biểu diễn tiềm năng cho cùng N "đơn vị tính toán".</p>'+table(['','Reservoir cổ điển (ESN)','Quantum Reservoir (QRC)'],
      [['Không gian trạng thái','N chiều (tuyến tính)','2^N chiều (Hilbert space)'],['Động lực','Mạng nơ-ron ngẫu nhiên cố định','Hamiltonian cố định, tiến hoá unitary'],['Huấn luyện','Chỉ readout tuyến tính (ridge regression)','Chỉ readout tuyến tính (giống ESN)']]),
    'PHẦN 2 · QRC','So sánh ESN cổ điển và QRC'),
   sl(callout('good','Kết nối lý thuyết của paper đang xét','QRC và Quantum Extreme Learning Machine (QELM) là 2 giới hạn CÙNG một kiến trúc spin-chain, khác nhau ở độ dài mã hoá lại w: w=N (reset toàn bộ) ⇒ QELM (không trí nhớ); w<N (giữ memory register) ⇒ QRC đầy đủ.'),
    'PHẦN 2 · QRC','QRC ↔ QELM: một kiến trúc, hai giới hạn'),
 ]),
 dict(title='Hamiltonian & kiến trúc explicit/memory register',bullets=['Mixed-Field Ising Model','Explicit vs memory register','Bayesian Optimization siêu tham số'],slides=[
   sl(formula('Hamiltonian reservoir (Eq. 1, paper)','H = J·Σᵢ XᵢXᵢ₊₁ + h_z·Σᵢ Zᵢ + h_x·Σᵢ Xᵢ',
      [('J','coupling lân cận gần theo trục x'),('h_x, h_z','2 trường đồng nhất (longitudinal/transverse)'),('N qubit, biên hở','Mixed-Field Ising Model 1 chiều')])
    +formula('Toán tử tiến hoá 1 bước','U = e^{-iHΔt}',[('Δt','thời gian tiến hoá giữa 2 bước input, tối ưu bằng Bayesian Optimization')]),
    'PHẦN 3 · Hamiltonian','Hamiltonian MFIM và toán tử tiến hoá',
    explain='H ở đây đóng vai trò giống "trọng số cố định ngẫu nhiên" của ESN cổ điển, nhưng thay vì là ma trận số thực, nó là một toán tử lượng tử — việc "chạy reservoir 1 bước" là cho hệ tiến hoá theo U trong thời gian Δt.'),
   sl('<p>Trong mỗi bước: w qubit gần nhất (<b>explicit register</b>) bị RESET và mã hoá lại input mới; N−w qubit còn lại (<b>quantum memory register</b>) KHÔNG bị reset, mang trạng thái lượng tử đã tiến hoá từ các bước trước — đây là nơi "trí nhớ dài hạn ngầm" được lưu trữ.</p>'
    +callout('warn','Phát hiện chính của paper','Quantum memory register là THIẾT YẾU khi tác vụ cần nhớ xa vào quá khứ (ví dụ Santa Fe laser); với tác vụ chỉ cần lịch sử ngắn, giới hạn w=N (không còn memory register, tương đương QELM) đã đủ tốt.'),
    'PHẦN 3 · Hamiltonian','Explicit register và Quantum memory register'),
 ]),
]

quiz=B.items
module_page('m2','02-reservoir-computing-qrc',
  title='M2 · Reservoir Computing & QRC',
  subtitle='Từ vanishing gradient tới spin-chain lượng tử có trí nhớ điều chỉnh được',
  source=SRC, status=f'HOÀN CHỈNH phần lõi — {len(quiz)} câu quiz bám sát nội dung đã đọc full-text',
  parts=parts, quiz_items=quiz,
  notes='<h2>Ghi chú</h2><p>Hamiltonian Eq.(1), kiến trúc explicit/memory register, 2 benchmark NARMA-10/Santa Fe, phương pháp Bayesian Optimization: trích trực tiếp từ bản PDF full-text đã verify. Phần lịch sử RC (BPTT, ESN, LSM, fading memory) là kiến thức chuẩn ngành (Jaeger 2001; Maass 2002), không trích số liệu riêng của paper.</p>',
  notebook_links=[('m2_verify_rc_narma10.ipynb (ESN cổ điển train thật trên NARMA-10, đã chạy 0 lỗi)','../../notebooks/m2_verify_rc_narma10.ipynb')])
print('Module 2 xong.')
