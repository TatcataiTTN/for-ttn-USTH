# -*- coding: utf-8 -*-
"""M5 — Độ nhạy của truy hồi thụ động: averaging kernel, DOFS (đề cương Ch.5)."""
from lib import *
from qcore import Bank
V = VERIFIED
OE = V['oe']

def build():
    B = Bank('m5', seed=5)
    di, dr, dn = OE['ideal']['dofs'], OE['realistic']['dofs'], OE['noisy']['dofs']
    B.add('Đại lượng nào được dùng để định lượng độ nhạy của truy hồi thụ động?',
          'Ma trận averaging kernel A = ∂x̂/∂x (độ nhạy của trạng thái truy hồi theo trạng thái thật)', ['Hệ số Ångström α, mô tả sự phụ thuộc phổ của độ dày quang học aerosol', 'Hệ số khối khí AMF = SCD/VCD, mô tả độ dài đường truyền của ánh sáng', 'Ma trận hiệp phương sai sai số đo S_ε, mô tả độ lớn nhiễu của cảm biến'],
          'Đề cương 5.1: A = ∂x̂/∂x = G·K, với G = (KᵀS_ε⁻¹K + S_a⁻¹)⁻¹KᵀS_ε⁻¹ là ma trận khuếch đại (gain).', 1, 'Averaging kernel', origin='goc', src='Đề cương Ch.5 (checklist)')
    B.add('Mối quan hệ giữa profil truy hồi, profil thật và tiên nghiệm qua averaging kernel là gì?',
          'x̂ = x_a + A (x_thật − x_a) + G ε', ['x̂ = x_thật + A x_a + G', 'x̂ = A⁻¹ x_thật', 'x̂ = x_a · A / ε'],
          'Profil truy hồi là phiên bản làm mượt của profil thật, trộn với tiên nghiệm, cộng nhiễu đo được khuếch đại bởi G.', 1, 'Averaging kernel', origin='goc', src='Đề thi mẫu Q5(a)')
    B.add('DOFS (Degrees Of Freedom for Signal) tính bằng công thức nào và có nghĩa gì?',
          'DOFS = tr(A) (vết của A): số mẩu thông tin độc lập về profil thẳng đứng', ['DOFS = det(A), định thức của A: thể tích bất định còn lại của profil thẳng đứng', 'DOFS = ΣS_ε, tổng phương sai nhiễu: độ lớn nhiễu đo trên toàn bộ các kênh phổ', 'DOFS = A⁻¹, nghịch đảo của A: độ nhạy nghịch của phép đo đối với profil thẳng đứng'],
          'Đề cương 5.1: DOFS = tr(A). DOFS bằng số lớp khi A là ma trận đơn vị; bằng 0 nếu truy hồi chỉ trả lại tiên nghiệm.', 1, 'DOFS', origin='goc', src='Đề cương Ch.5 (checklist)')
    B.add('Một hàng của averaging kernel cho biết điều gì?',
          'Giá trị truy hồi tại một mực là trung bình có trọng số của profil thật ở mọi mực; độ rộng FWHM là phân giải thẳng đứng', ['Độ cao mà khí có nồng độ lớn nhất trong profil thật, cùng độ dày của lớp khí đó', 'Sai số ngẫu nhiên của phép đo tại mực đó, cộng với sai số hệ thống của mô hình thuận', 'Hệ số hấp thụ của khí tại mực đó theo bước sóng, nhân với mật độ số của nó tại mực đó'],
          'Đề cương 5.1: đỉnh hàng cho biết thông tin thực sự đến từ độ cao nào; độ rộng (FWHM) là phân giải thẳng đứng.', 2, 'Averaging kernel', src='Đề cương 5.1')
    B.add('Diện tích (tổng) của một hàng averaging kernel gần 1 nghĩa là gì?',
          'Giá trị truy hồi ở mực đó chủ yếu đến từ phép đo', ['Giá trị truy hồi ở mực đó chủ yếu bằng giá trị tiên nghiệm, ít phụ thuộc phép đo', 'Sai số đo tại mực đó đang bằng không nên không cần chính quy hóa nữa', 'Phân giải thẳng đứng tại mực đó đã đạt giá trị tối đa mà thiết bị có thể có'],
          'Đề cương 5.1: diện tích ≈ 1 → đo chiếm ưu thế; ≈ 0 → giá trị truy hồi chỉ bằng tiên nghiệm.', 2, 'Averaging kernel', src='Đề cương 5.1')
    B.add('Trường hợp lý tưởng (độ nhạy hoàn hảo) có averaging kernel như thế nào?',
          'A = ma trận đơn vị: mỗi hàng là hàm delta bằng 1 tại mực của nó và 0 ở nơi khác', ['A = ma trận không: phép đo không cho thông tin nào về profil thật ở bất kỳ mực nào', 'A là ma trận đường chéo mà mọi phần tử bằng 0,5: mỗi mực chỉ nhận một nửa thông tin', 'A có mọi phần tử bằng nhau nên mọi mực cho cùng một giá trị trung bình của profil'],
          'Đề cương 5.2(a): truy hồi tái tạo chính xác profil thật, không phụ thuộc tiên nghiệm, phân giải thẳng đứng vô hạn, DOFS bằng số mực.', 1, 'Ideal vs thực', origin='goc', src='Đề cương Ch.5 (checklist)')
    B.add('Đặc điểm nào đúng với averaging kernel của truy hồi ozone nadir thực tế (UV 270–330 nm hoặc IASI 9,6 µm)?',
          'Kernel rộng (FWHM ~7–15 km), chồng nhau, đỉnh lệch khỏi mực danh nghĩa, biên độ < 1 (~0,3–0,6)', ['Kernel là các hàm delta hẹp 1–2 km tại từng mực', 'Kernel có biên độ lớn hơn 1 ở gần mặt đất', 'Kernel giống hệt nhau ở mọi mực'],
          'Đề cương 5.2(b): độ nhạy thấp gần bề mặt (tán xạ Rayleigh, hấp thụ O₃ phía trên, mây) nên giá trị gần mặt đất chủ yếu từ tiên nghiệm.', 2, 'Ideal vs thực', src='Đề cương 5.2')
    B.add('DOFS điển hình của truy hồi O₃ nadir trong UV và trong IASI là bao nhiêu?',
          'Khoảng 4–6 trong UV (≈ 1 ở đối lưu), khoảng 3–4 với IASI', ['Khoảng 20–30 cho cả hai', 'Khoảng 1 cho UV và 10 cho IASI', 'Bằng 0 vì nadir không có thông tin thẳng đứng'],
          'Đề cương 5.2(b): biết bình lưu trong ~3–4 lớp dày cộng khoảng 1 mẩu thông tin đối lưu. Limb: kernel hẹp ~2–3 km, DOFS ≈ 20–30.', 2, 'Ideal vs thực', src='Đề cương 5.2')
    B.add('Một truy hồi CO từ máy thăm dò hồng ngoại nhiệt có DOFS = 1,2. Điều này có nghĩa gì?',
          'Khoảng một mẩu thông tin độc lập: về bản chất là một cột, nhạy nhất ở đối lưu giữa (~3–8 km), ít nhạy gần mặt đất', ['Biết CO ở 1,2 mực độc lập ngay sát mặt đất, nơi tương phản nhiệt là lớn nhất', 'Sai số truy hồi bằng 1,2 lần độ bất định của profil tiên nghiệm ban đầu', 'Có 12 mực độc lập nhưng mỗi mực bị nhiễu khoảng 10% so với tín hiệu'],
          'Đáp án gợi ý Q5(b): tương phản nhiệt với bề mặt lớn nhất ở đối lưu giữa; gần mặt đất tương phản nhiệt thấp nên kém nhạy.', 2, 'DOFS', origin='goc', src='Đề thi mẫu Q5(b)')
    B.add('Khi so sánh truy hồi vệ tinh với mô hình hóa học – vận chuyển, cần làm gì với averaging kernel?',
          'Làm mượt profil mô hình: x_m,smooth = x_a + A (x_model − x_a), rồi so với x̂', ['Cộng thêm nhiễu đo vào profil mô hình rồi lấy trung bình với tiên nghiệm', 'Chỉ so sánh ở các mực mà A bằng 0 để tránh ảnh hưởng của phép đo', 'Chia profil mô hình cho DOFS rồi nhân với hệ số khối khí trung bình'],
          'Đáp án gợi ý Q5(c): phép làm mượt này loại hiệu ứng của làm mượt và tiên nghiệm, nên so sánh là "cùng loại".', 2, 'Ứng dụng AK', origin='goc', src='Đề thi mẫu Q5(c)')
    B.add('Averaging kernel của cột a(z) = ∂VCD̂/∂n(z) lý tưởng bằng bao nhiêu?',
          'Bằng 1 ở mọi độ cao', ['Bằng 0 ở mọi độ cao', 'Bằng 1 chỉ ở mặt đất', 'Bằng AMF tại mọi độ cao'],
          'Đề cương 5.1: trong DOAS, a(z) = AMF_lớp / AMF_tổng. Lý tưởng = 1 tại mọi độ cao (cột nhạy đều).', 3, 'Averaging kernel', src='Đề cương 5.1')
    B.add('Sai số truy hồi gồm hai thành phần nào?',
          'Sai số làm mượt (I − A) S_a (I − A)ᵀ và sai số nhiễu G S_ε Gᵀ', ['Sai số AMF do giả định đường truyền và sai số khớp phổ DOAS do tiết diện', 'Sai số Ångström do kích thước hạt và sai số ω₀ do hấp thụ của hạt', 'Sai số quỹ đạo do vị trí vệ tinh và sai số hiệu chuẩn do thiết bị'],
          'Đề cương 5.1: Ŝ = (I − A) S_a (I − A)ᵀ + G S_ε Gᵀ.', 3, 'Sai số', src='Đề cương 5.1')
    B.add(f'Mô hình tính toán 12 mực với kernel rất hẹp và nhiễu rất nhỏ cho DOFS bằng bao nhiêu?',
          f'≈ {di:.1f} (tức A gần ma trận đơn vị)', [f'≈ {dr:.1f} (như trường hợp thực tế với kernel rộng 3 mực)', '≈ 1,0 (một cột duy nhất, không có thông tin về độ cao)', '≈ 0 (không có thông tin nào, chỉ còn lại tiên nghiệm)'],
          f'Đã chạy bằng Python: w = 0,3 mực, σ_ε = 0,01 → DOFS = {di:.3f}. Khi kernel hẹp và đo chính xác, A → I và DOFS → số mực.', 2, 'DOFS', src='Mô phỏng tự dựng bằng Python (data/verified.json)')
    B.add('Trong cùng mô hình 12 mực, tăng nhiễu đo từ 0,1 lên 1,0 (kernel rộng 3 mực) thì DOFS thay đổi thế nào?',
          f'Giảm từ ≈ {dr:.1f} xuống ≈ {dn:.1f}', [f'Tăng từ ≈ {dn:.1f} lên ≈ {dr:.1f}', 'Không đổi vì DOFS chỉ phụ thuộc kernel', 'Tăng lên 12 vì nhiễu làm thêm thông tin'],
          f'Nhiễu lớn → kết quả dựa nhiều vào tiên nghiệm → A thu nhỏ → DOFS giảm. Số liệu: {dr:.3f} → {dn:.3f} (Python).', 3, 'DOFS', src='Mô phỏng tự dựng bằng Python (data/verified.json)')
    B.add('Tại sao truy hồi limb ozone gần với trường hợp lý tưởng hơn nadir?',
          'Vì hình học limb cho kernel hẹp (~2–3 km) và DOFS ≈ 20–30', ['Vì limb nhìn thẳng xuống nên không chịu tán xạ Rayleigh của khí quyển phía trên', 'Vì limb dùng nhiều thông tin tiên nghiệm hơn nadir nên kết quả ít bất định', 'Vì limb đo trực tiếp nồng độ khí bằng một xung laser phát ra từ vệ tinh'],
          'Đề cương 5.2: limb ozone gần lý tưởng ở tầng bình lưu.', 2, 'Ideal vs thực', src='Đề cương 5.2')
    B.essay('(a) Viết quan hệ giữa profil truy hồi, profil thật và tiên nghiệm qua averaging kernel.\n(b) Truy hồi CO từ thiết bị hồng ngoại nhiệt có DOFS = 1,2. Nghĩa là gì? Độ nhạy cao nhất ở đâu và vì sao?\n(c) Dùng averaging kernel thế nào khi so sánh vệ tinh với mô hình hóa học – vận chuyển?',
            '(a) x̂ = x_a + A(x_thật − x_a) + Gε; A = ∂x̂/∂x = GK; DOFS = tr(A).\n(b) ≈ một mẩu thông tin độc lập → về cơ bản là một cột, nhạy nhất ở đối lưu giữa (~3–8 km) nơi tương phản nhiệt với bề mặt lớn nhất; gần mặt đất gần như bằng tiên nghiệm.\n'
            '(c) Làm mượt profil mô hình: x_m,smooth = x_a + A(x_model − x_a), rồi so với x̂ để loại ảnh hưởng của làm mượt và tiên nghiệm.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q5 (2,5 điểm) + đáp án gợi ý')
    B.essay('Vẽ và so sánh averaging kernel lý tưởng với kernel thực tế của truy hồi ozone nadir.',
            'Lý tưởng: A = I, các hàm delta tại mỗi mực, DOFS bằng số mực, không phụ thuộc tiên nghiệm. Thực tế (nadir O₃): kernel rộng 7–15 km, chồng nhau, đỉnh lệch, biên độ 0,3–0,6, DOFS ≈ 4–6 (≈ 1 ở đối lưu), kém nhạy gần mặt đất (Rayleigh, hấp thụ phía trên, mây) và ở trên 50 km; vì vậy phân giải thẳng đứng ~6–10 km ở bình lưu, kém hơn ở đối lưu.', 2, 'Ideal vs thực', origin='goc', src='Đề cương 5.2 / hình 16')
    sl = [
        cover('Độ nhạy của truy hồi: averaging kernel', 'Sensitivity of passive retrievals — Đề cương chương 5',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>A = ∂x̂/∂x · DOFS = tr(A) · ideal và thực tế'),
        S('Ma trận averaging kernel', fm('<span class="l">Định nghĩa</span>A = ∂x̂/∂x = G K &nbsp;,&nbsp; G = (K<sup>T</sup>S<sub>ε</sub><sup>−1</sup>K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup>K<sup>T</sup>S<sub>ε</sub><sup>−1</sup>', 26) +
          fm('<span class="l">Truy hồi = làm mượt + tiên nghiệm + nhiễu</span>x̂ = x<sub>a</sub> + A (x<sub>thật</sub> − x<sub>a</sub>) + G ε', 30) +
          '<p class="note">Mỗi hàng của A: giá trị tại một mực là trung bình có trọng số của profil thật; <b>độ rộng FWHM</b> = phân giải thẳng đứng, <b>đỉnh</b> = nơi thông tin thực sự đến.</p>'),
        S('Diện tích hàng và DOFS', cards2(330, card('Diện tích hàng ≈ 1', 'Giá trị truy hồi chủ yếu từ <b>phép đo</b>.'), card('Diện tích hàng ≈ 0', 'Giá trị truy hồi gần bằng <b>tiên nghiệm</b>.'),
          card('DOFS = tr(A)', 'Số mẩu thông tin độc lập về profil. DOFS = số mực khi A = I.'), cols=3) + fm('Ŝ = (I − A) S<sub>a</sub> (I − A)<sup>T</sup> + G S<sub>ε</sub> G<sup>T</sup>', 28)),
        S('Cột: averaging kernel của cột', figfit('f14_colavk', 'Hình 15 (đề cương): kernel của cột — lý tưởng (= 1) so với UV-vis điển hình, có mây và hồng ngoại nhiệt.', 480) +
          '<p class="note">a(z) = ∂VCD̂/∂n(z) = AMF<sub>lớp</sub> / AMF<sub>tổng</sub>; lý tưởng bằng 1 ở mọi độ cao.</p>'),
        S('Lý tưởng so với thực tế (O₃ nadir)', figfit('f4_avk', 'Hình 16 (đề cương): (a) A = I; (b) truy hồi profil ozone nadir điển hình.', 500)),
        S('Đặc điểm của truy hồi ozone nadir', cols(
            ulb(['Kernel rộng ~7–15 km, chồng nhau', 'Đỉnh lệch khỏi mực danh nghĩa', 'Biên độ < 1 (~0,3–0,6)', 'DOFS ≈ 4–6 (UV), ≈ 3–4 (IASI)'], 33, 44),
            ulb(['Gần mặt đất: kém nhạy (Rayleigh, hấp thụ phía trên, mây) → <b>từ tiên nghiệm</b>', 'Trên 50 km: ít ozone nên mất nhạy', 'Limb: kernel ~2–3 km, DOFS ≈ 20–30'], 33, 44))),
        S('Mô phỏng 12 mực (Python)', dtable(tbl(['Trường hợp', 'Độ rộng kernel', 'Nhiễu σ<sub>ε</sub>', 'DOFS'], [
            ['Lý tưởng', '0,3 mực', '0,01', f'{di:.2f}'], ['Thực tế', '3 mực', '0,1', f'{dr:.2f}'], ['Nhiễu lớn', '3 mực', '1,0', f'{dn:.2f}']]), 'xl') +
          '<p class="note" style="margin-top:20px">Tiên nghiệm tương quan theo độ cao (độ dài 3 mực). DOFS = tr(A) = tổng trị riêng của A; kernel hẹp và đo chính xác → A → I.</p>'),
        S('Dùng averaging kernel khi so sánh với mô hình', fm('x<sub>m,smooth</sub> = x<sub>a</sub> + A (x<sub>model</sub> − x<sub>a</sub>)', 34) +
          ulb(['Làm mượt profil mô hình bằng chính A của vệ tinh', 'Rồi so với x̂ để loại ảnh hưởng của làm mượt và tiên nghiệm', 'Không làm bước này: lệch có thể do độ nhạy chứ không do mô hình'], 33, 30)),
        S('Exam checklist — Chương 5', chk(['Tên: ma trận averaging kernel A = ∂x̂/∂x; DOFS = trace(A)', 'x̂ = x<sub>a</sub> + A (x − x<sub>a</sub>) + G ε', 'Độ rộng hàng = phân giải thẳng đứng; diện tích = đóng góp của phép đo', 'Vẽ hàm delta (lý tưởng) và kernel rộng, chồng nhau, lệch đỉnh (O₃ nadir, DOFS ≈ 4–6)'])),
        S('Ý chính', dul(['Độ nhạy đo bằng A = ∂x̂/∂x; DOFS = tr(A)', 'Lý tưởng: A = I, không phụ thuộc tiên nghiệm', 'Thực tế O₃ nadir: kernel rộng, DOFS ≈ 4–6', 'So sánh với mô hình: làm mượt bằng A']))]
    mod = dict(id='m5', slug='05-averaging-kernels', title='M5 · Độ nhạy: averaging kernel', en='Sensitivity of passive retrievals: averaging kernels',
               question='<ul><li>Which magnitude is used to quantify the sensitivity of passive remote sensing methods for retrieving the concentration of trace gases?</li><li>Explain the general concept and illustrate with drawings a case of ideally perfect sensitivity and a realistic case (such as the retrieval of the ozone profiles using satellite spectral measurements in nadir pointing geometry).</li></ul>',
               calcs=[('ak', 'Averaging kernel và DOFS (mô phỏng 12 mực)')],
               checklist=['Name: averaging kernel matrix A = ∂x̂/∂x; DOFS = trace(A).', 'x̂ = x_a + A(x − x_a) + Gε — retrieval = smoothed truth + a priori contribution.', 'Row width = vertical resolution; area = measurement contribution.', 'Draw delta functions (ideal) vs broad, overlapping, peak-shifted kernels (nadir O₃, DOFS ≈ 4–6).'],
               summary=['Đại lượng đo độ nhạy: ma trận hạt nhân trung bình (averaging kernel) A = ∂x̂/∂x; vết của A = số bậc tự do tín hiệu (DOFS).', 'Trường hợp lý tưởng: A = ma trận đơn vị → hàm delta tại mỗi độ cao, không phụ thuộc tiên nghiệm.', 'Thực tế (O₃ nadir): hạt nhân rộng 7–15 km, chồng lên nhau, biên độ < 1, DOFS ≈ 4–6; gần mặt đất độ nhạy thấp → kết quả phụ thuộc nhiều vào profil tiên nghiệm.'],
               sections=[
        ('Averaging kernel, nói nôm na', '<p>Truy hồi profil giống như vẽ lại một bức tranh từ một bức ảnh mờ: bạn thu được phiên bản <b>làm mượt</b> của bức tranh thật, và chỗ nào ảnh quá mờ thì bạn phải điền bằng <b>phỏng đoán có sẵn (tiên nghiệm)</b>. Ma trận <b>averaging kernel A</b> cho biết mức độ “mờ” đó ở từng độ cao.</p>' +
         eq('Định nghĩa', 'A = ∂x̂ / ∂x = G K &nbsp;;&nbsp; G = (K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup> K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> (gain)') +
         eq('Hệ quả', 'x̂ = x<sub>a</sub> + A (x<sub>thật</sub> − x<sub>a</sub>) + G ε') +
         '<ul><li><b>Mỗi hàng</b> của A: giá trị truy hồi tại một mực là trung bình có trọng số của profil thật ở mọi mực. <b>Độ rộng (FWHM)</b> = phân giải thẳng đứng; <b>đỉnh</b> = nơi thông tin thực sự đến.</li>'
         '<li><b>Diện tích hàng</b>: ≈ 1 → phép đo chiếm ưu thế; ≈ 0 → giá trị chỉ bằng tiên nghiệm.</li><li><b>DOFS = tr(A)</b> = số mẩu thông tin độc lập về profil.</li>'
         '<li><b>Cột</b>: a(z) = ∂VCD̂/∂n(z) (trong DOAS: AMF<sub>lớp</sub>/AMF<sub>tổng</sub>); lý tưởng bằng 1 ở mọi độ cao.</li></ul>' +
         eq('Sai số truy hồi', 'Ŝ = (I − A) S<sub>a</sub> (I − A)<sup>T</sup> [làm mượt] + G S<sub>ε</sub> G<sup>T</sup> [nhiễu]') + lfig('f14_colavk', 'Hình 15 (đề cương): kernel của cột — lý tưởng so với UV-vis, có mây, và hồng ngoại nhiệt.')),
        ('Trường hợp lý tưởng và thực tế', '<p><b>(a) Lý tưởng: A = I.</b> Mỗi kernel là hàm delta bằng 1 tại đúng mực của nó, 0 ở nơi khác: truy hồi tái tạo chính xác profil thật, không phụ thuộc tiên nghiệm, phân giải vô hạn, DOFS = số mực.</p>'
         '<p><b>(b) Thực tế: ozone nadir</b> (UV 270–330 nm của GOME-2/OMI hoặc IASI 9,6 µm):</p><ul><li>Kernel rộng (FWHM ~7–15 km) và chồng nhau → phân giải thẳng đứng ~6–10 km ở bình lưu, kém hơn ở đối lưu.</li><li>Đỉnh lệch khỏi mực danh nghĩa; biên độ &lt; 1 (≈ 0,3–0,6).</li>'
         '<li>DOFS ≈ 4–6 trong UV (≈ 1 ở đối lưu), ≈ 3–4 với IASI: biết bình lưu trong ~3–4 lớp dày cộng khoảng 1 mẩu thông tin đối lưu.</li><li>Kém nhạy gần mặt đất (Rayleigh, hấp thụ O₃ phía trên, mây) và ở trên 50 km (ít ozone) → các giá trị này chủ yếu lấy từ tiên nghiệm.</li></ul>'
         '<p>Ngược lại, truy hồi ozone <b>limb</b> có kernel hẹp (~2–3 km), DOFS ≈ 20–30, gần với lý tưởng ở tầng bình lưu.</p>' + lfig('f4_avk', 'Hình 16 (đề cương): (a) độ nhạy hoàn hảo A = I; (b) truy hồi profil ozone nadir điển hình.')),
        ('Mô phỏng 12 mực (kiểm chứng bằng Python)', '<p>Mô hình tự dựng: N = 12 mực; hàm trọng số K là các đường Gauss có độ rộng w mực; nhiễu S<sub>ε</sub> = σ<sub>ε</sub>²I; tiên nghiệm S<sub>a</sub> tương quan theo độ cao (độ dài 3 mực, σ<sub>a</sub> = 1). Kết quả:</p>' +
         hx_table(['Trường hợp', 'Độ rộng kernel w', 'σ<sub>ε</sub>', 'DOFS = tr(A)'], [['Lý tưởng', '0,3 mực', '0,01', f'<b>{di:.2f}</b>'], ['Thực tế', '3 mực', '0,1', f'<b>{dr:.2f}</b>'], ['Nhiễu lớn', '3 mực', '1,0', f'<b>{dn:.2f}</b>']]) +
         '<p>Quan sát: kernel hẹp và đo chính xác → A → I, DOFS → số mực. Tăng nhiễu hoặc làm kernel rộng ra → DOFS giảm, kết quả dựa nhiều hơn vào tiên nghiệm. Hãy tự thử trong <a href="../../calculators.html#ak">công cụ averaging kernel</a>. (DOFS = tr(A) cũng bằng tổng các trị riêng của A; đã kiểm bằng numpy.)</p>'
         '<p><b>Dùng AK khi so sánh với mô hình:</b> x<sub>m,smooth</sub> = x<sub>a</sub> + A (x<sub>model</sub> − x<sub>a</sub>), sau đó so với x̂; nếu bỏ bước này, chênh lệch có thể do độ nhạy chứ không phải do mô hình.</p>')])
    return mod, sl, B
