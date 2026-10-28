# -*- coding: utf-8 -*-
"""M1 — Bể chứa và thời gian sống (đề cương Ch.1)."""
from lib import *
from lib import _PIL
from qcore import Bank
V = VERIFIED
CO = V['co_oh']

def build():
    B = Bank('m1', seed=1)
    G = dict(origin='goc')
    # ---------------- QUIZ ----------------
    B.add('Thời gian sống τ của một chất ô nhiễm được định nghĩa như thế nào?',
          'τ = lượng tồn trữ trong khí quyển M chia cho tốc độ mất tổng cộng L (τ = M / L)',
          ['τ = tốc độ phát thải chia cho nồng độ nền của chất đó',
           'τ = thời gian để một nửa lượng chất bị mất đi, tức τ = ln 2 / k',
           'τ = khoảng cách mà phân tử bị gió mang đi chia cho tốc độ gió'],
          'Đề cương Ch.1: τ = M / L (ở trạng thái dừng τ = M / P). Với bể chứa bậc nhất, τ = 1/k′. Thời gian bán rã t½ = τ·ln 2 ≈ 0,69 τ, khác với τ.',
          1, 'Thời gian sống', origin='goc', src='Đề thi mẫu Q1(a)')
    B.add('Khi nhiều bể chứa bậc nhất cùng tác động song song, thời gian sống tổng hợp được tính bằng cách nào?',
          'Cộng các nghịch đảo: 1/τ = 1/τ₁ + 1/τ₂ + …',
          ['Cộng thẳng các thời gian sống: τ = τ₁ + τ₂ + …',
           'Lấy thời gian sống dài nhất, vì bể chứa chậm nhất quyết định',
           'Lấy trung bình cộng của các thời gian sống thành phần'],
          'Các tốc độ mất bậc nhất cộng lại, nên 1/τ = Σ 1/τᵢ. Hệ quả: τ tổng luôn NGẮN HƠN bể chứa nhanh nhất.',
          1, 'Thời gian sống', origin='goc', src='Đề thi mẫu Q1(a); Đề cương 1.1')
    B.add('Chọn đúng danh sách các bể chứa (sink) chính của chất ô nhiễm trong khí quyển.',
          'Oxy hóa bởi OH, quang phân, lắng đọng khô, lắng đọng ướt, hóa học dị thể, vận chuyển ra khỏi vùng',
          ['Phát thải từ nhà máy, cháy rừng, núi lửa, đồng cỏ và đại dương',
           'Tán xạ Rayleigh, tán xạ Mie, hấp thụ, phát xạ nhiệt và phản xạ bề mặt',
           'Hình học nadir, limb, che khuất, quỹ đạo địa tĩnh và quỹ đạo cực'],
          'Đề cương 1.1 liệt kê: oxy hóa pha khí (chủ yếu OH), quang phân, lắng đọng khô, lắng đọng ướt, hóa học dị thể/đa pha và vận chuyển ra khỏi miền xét. Phát thải là NGUỒN, không phải bể chứa.',
          1, 'Bể chứa', origin='goc', src='Đề cương Ch.1 (checklist: ≥ 4 bể chứa)')
    B.add('Gốc OH được gọi là "chất tẩy rửa của khí quyển" vì lý do nào?',
          'Nó oxy hóa và loại bỏ phần lớn các khí phản ứng như CO, CH₄, NO₂',
          ['Nó hấp thụ tia cực tím và bảo vệ tầng đối lưu khỏi bức xạ Mặt Trời',
           'Nó tạo mưa bằng cách làm hạt aerosol trở thành nhân ngưng tụ mây',
           'Nó trung hòa các hạt bụi mịn bằng điện tích để chúng rơi xuống đất'],
          'OH là chất oxy hóa chính của pha khí: CO + OH → CO₂ + H; CH₄ + OH → CH₃ + H₂O; NO₂ + OH + M → HNO₃. Vì vậy OH quyết định thời gian sống của nhiều khí.',
          1, 'Bể chứa', src='Đề cương 1.1')
    B.add('Phản ứng NO₂ + hν (λ < 420 nm) → NO + O thuộc loại bể chứa nào?',
          'Quang phân (photolysis)', ['Lắng đọng khô (dry deposition)', 'Lắng đọng ướt (wet deposition)', 'Hóa học dị thể trên hạt aerosol'],
          'Phân tử bị phá vỡ bởi photon UV/khả kiến nên là quang phân. HCHO + hν và CFC bị quang phân trong tầng bình lưu cũng cùng loại.',
          1, 'Bể chứa', src='Đề cương 1.1')
    B.add('Bể chứa nào là cơ chế mất CHÍNH đối với phần lớn aerosol và các khí tan trong nước như HNO₃, NH₃?',
          'Lắng đọng ướt qua mây và mưa (rainout/washout)', ['Quang phân bởi tia UV mạnh', 'Phản ứng với gốc OH ở pha khí', 'Vận chuyển ra tầng bình lưu rồi quang phân'],
          'Đề cương: lắng đọng ướt gồm rainout (trong mây, hạt làm nhân ngưng tụ) và washout (dưới mây); là bể chứa chính của khí tan và đa số aerosol.',
          1, 'Bể chứa', src='Đề cương 1.1')
    B.add('Lắng đọng khô được mô tả bằng đại lượng nào, và công thức thông lượng là gì?',
          'Vận tốc lắng đọng v_d, với thông lượng F = −v_d · C',
          ['Hằng số vận tốc phản ứng k, với thông lượng F = −k · [OH]',
           'Độ dày quang học τ, với thông lượng F = I₀ · e^(−τ)',
           'Hệ số Ångström α, với thông lượng F = τ₀ · λ^(−α)'],
          'Đề cương 1.1: dung nạp trực tiếp tại bề mặt (khí khổng, đất, nước, công trình) mà không cần mưa, mô tả bằng v_d; F = −v_d·C.',
          2, 'Bể chứa', src='Đề cương 1.1')
    B.add('Tại sao phản ứng N₂O₅ + H₂O (trên hạt) → HNO₃ được gọi là hóa học dị thể?',
          'Phản ứng xảy ra trên bề mặt hoặc bên trong hạt/giọt chứ không thuần pha khí',
          ['Phản ứng cần ánh sáng nên chỉ xảy ra ban ngày', 'Phản ứng tạo ra hai sản phẩm có trạng thái khác nhau', 'Phản ứng chỉ xảy ra ở tầng bình lưu'],
          'Dị thể (multiphase) = có pha rắn/lỏng tham gia. Chuyển khí → hạt (tạo hạt, ngưng tụ) là bể chứa của khí nhưng lại là NGUỒN của aerosol.',
          2, 'Bể chứa', src='Đề cương 1.1')
    # ---- tính toán (đáp án lấy từ verified.json) ----
    d = CO['tau_days']
    B.add('Với k(CO+OH) ≈ 2×10⁻¹³ cm³ molecule⁻¹ s⁻¹ và [OH] ≈ 1×10⁶ molecule cm⁻³, thời gian sống của CO theo OH xấp xỉ bao nhiêu?',
          f'≈ {d:.0f} ngày (≈ 5×10⁶ s, khoảng 2 tháng)',
          ['≈ 5,8 ngày (nhầm hệ số chuyển giây sang ngày)', '≈ 1 390 ngày (chia cho 3 600 rồi gọi là ngày)', '≈ 5×10⁶ ngày (quên đổi giây sang ngày)'],
          f'τ = 1/(k[OH]) = 1/(2×10⁻¹³ × 1×10⁶) = 5×10⁶ s; chia 86 400 s/ngày được {d:.2f} ngày. Đã tính lại bằng Python (data/verified.json).',
          1, 'Tính toán', origin='goc', src='Đề thi mẫu Q1(b)')
    p = V['par_example']
    B.add('Một khí bị mất do hóa học (τ = 2 ngày), lắng đọng khô (τ = 3 ngày) và lắng đọng ướt (τ = 6 ngày). Thời gian sống tổng hợp là bao nhiêu?',
          f'{p["total"]:.0f} ngày', ['11 ngày (cộng các thời gian sống)', '3,67 ngày (trung bình cộng)', '2 ngày (chọn bể chứa nhanh nhất)'],
          '1/τ = 1/2 + 1/3 + 1/6 = 1 ngày⁻¹ nên τ = 1 ngày. Kết quả ngắn hơn cả bể chứa nhanh nhất (2 ngày).',
          2, 'Tính toán', src='Đề cương 1.1 (công thức 1/τ = Σ 1/τᵢ)')
    pl = V['plume']
    B.add('Dọc theo hướng gió, cột NO₂ sau một nguồn điểm giảm theo hàm mũ với độ dài e-fold 50 km. Gió trung bình 5 m/s. Thời gian sống NO₂ ước tính là bao nhiêu?',
          f'≈ {pl["tau_h"]:.1f} giờ', ['≈ 10 giờ', '≈ 0,28 giờ (nhầm đơn vị km thành m)', '≈ 27,8 giờ'],
          'C(x) ∝ exp(−x/(U·τ)) nên τ = L/U = 50 000 m / 5 m s⁻¹ = 10 000 s ≈ 2,8 h, nằm trong khoảng 2–6 h của NO₂ theo đề cương.',
          2, 'Tính toán', src='Đề cương 1.2 (phương pháp plume decay)')
    B.add('Một bể chứa bậc nhất có τ = 10 ngày. Sau 10 ngày, phần còn lại của lượng ban đầu là bao nhiêu?',
          f'≈ {V["decay"]["e1"]*100:.0f}% (e⁻¹)', ['50% (một nửa)', '10% (một phần mười)', '0% (đã mất hết)'],
          'C/C₀ = e^(−t/τ). Tại t = τ còn e⁻¹ ≈ 36,8%. Một nửa chỉ mất sau t½ = τ ln 2 ≈ 6,9 ngày.',
          2, 'Tính toán', src='Đề cương hình 3 (đường suy giảm e^(−t/τ))')
    B.add('Quãng đường điển hình một phân tử bị gió mang đi trong thời gian sống τ được ước lượng bằng công thức nào?',
          'L ≈ U · τ (U là tốc độ gió ngang)', ['L ≈ τ / U', 'L ≈ U / τ²', 'L ≈ τ · [OH]'],
          'Đề cương 1.2: L ≈ U·τ với U ≈ 5–10 m/s. So L với kích thước nguồn và khoảng cách trộn để biết bản đồ vệ tinh giống bản đồ nguồn hay đã trộn đều.',
          1, 'Đọc bản đồ', src='Đề cương 1.2')
    B.add('Bản đồ vệ tinh NO₂ có các điểm nóng nhỏ trên thành phố, còn bản đồ CH₄ gần như đồng đều. Giải thích đúng là gì?',
          'NO₂ sống vài giờ nên bị phân hủy trước khi kịp khuếch tán; CH₄ sống ~10 năm, dài hơn thời gian trộn toàn cầu (~1 năm) nên trộn đều',
          ['NO₂ được đo bằng cảm biến có độ phân giải cao hơn cảm biến đo CH₄ nên thấy nhiều chi tiết hơn',
           'CH₄ hầu như không có nguồn phát thải trên mặt đất nên phân bố đều khắp',
           'NO₂ sống lâu hơn CH₄ nên tích tụ ở khu vực đô thị trong nhiều năm'],
          'Đề cương 1.2 và đáp án gợi ý Q1(c): τ ngắn → bản đồ giống bản đồ nguồn; τ ≫ thời gian trộn → phân bố đồng đều (biến thiên chỉ cỡ 1%).',
          2, 'Đọc bản đồ', origin='goc', src='Đề thi mẫu Q1(c)')
    B.add('Loài nào dưới đây có bản đồ vệ tinh "giống bản đồ nguồn" nhất (điểm nóng sắc nét, suy giảm nhanh trong vài chục đến vài trăm km)?',
          'NO₂ trong lớp biên (thời gian sống vài giờ)', ['CO₂ (thời gian sống từ một thế kỷ)', 'CH₄ (thời gian sống 9–12 năm)', 'N₂O (thời gian sống 50–120 năm)'],
          'Càng ngắn τ càng giống bản đồ nguồn. NO₂, SO₂, HCHO là loài sống ngắn; CO₂, CH₄, N₂O trộn đều và chỉ biến thiên cỡ ~1%.',
          1, 'Đọc bản đồ', src='Đề cương 1.2')
    B.add('Theo quan hệ Junge mà đề cương nêu, độ biến thiên không gian tương đối σ/C liên hệ với thời gian sống τ như thế nào?',
          'Tỉ lệ nghịch: σ/C ≈ 0,14/τ (τ tính bằng năm)', ['Tỉ lệ thuận: σ/C ≈ 0,14 · τ', 'Không phụ thuộc vào τ', 'Tỉ lệ nghịch với bình phương τ'],
          'Chất sống càng lâu càng đồng đều. Với CH₄ (τ ≈ 10 năm) σ/C ≈ 1,4%, phù hợp bản đồ gần như đồng đều. Đây là quy tắc gần đúng.',
          2, 'Đọc bản đồ', src='Đề cương 1.2 (quan hệ Junge)')
    B.add('Chất nào có thời gian sống điển hình theo thứ tự GIỜ?',
          'NO₂ và HCHO trong lớp biên', ['CO', 'CH₄', 'N₂O'],
          'Bảng Ch.1: NO₂ 2–12 h; HCHO/glyoxal vài giờ; CO ≈ 1–2 tháng; CH₄ ≈ 9–12 năm; N₂O ≈ 50–120 năm.',
          1, 'Bậc độ lớn', src='Đề cương 1.3')
    B.add('Xếp theo thứ tự thời gian sống TĂNG DẦN nào là đúng?',
          'NO₂ < SO₂ < aerosol tầng đối lưu < CO < CH₄ < N₂O',
          ['SO₂ < NO₂ < CO < aerosol < N₂O < CH₄', 'CO < NO₂ < SO₂ < CH₄ < aerosol < N₂O', 'CH₄ < CO < aerosol < SO₂ < NO₂ < N₂O'],
          'Giờ (NO₂) → 1–2 ngày (SO₂) → ~1 tuần (aerosol) → 1–2 tháng (CO) → ~10 năm (CH₄) → 50–120 năm (N₂O).',
          2, 'Bậc độ lớn', origin='goc', src='Đề cương Ch.1 (checklist bậc độ lớn)')
    B.add('Thời gian sống của SO₂ ở tầng đối lưu và ở tầng bình lưu khác nhau thế nào?',
          'Khoảng 1–2 ngày ở tầng đối lưu, nhưng cỡ vài tuần ở tầng bình lưu',
          ['Dài hơn ở tầng đối lưu vì có nhiều hơi nước để hòa tan', 'Bằng nhau, vì cơ chế mất giống hệt', 'Khoảng 1–2 năm ở cả hai tầng'],
          'Trong tầng đối lưu SO₂ bị OH, oxy hóa pha nước và lắng đọng khô loại nhanh; lên tầng bình lưu không còn mưa và độ ẩm nên sống lâu hơn (vài tuần).',
          3, 'Bậc độ lớn', src='Đề cương 1.3')
    B.add('CO₂ khác các khí khác ở điểm nào khi nói về thời gian sống?',
          'Không có một thời gian sống đơn lẻ vì được hấp thụ bởi cả đại dương lẫn sinh quyển với tốc độ khác nhau',
          ['Thời gian sống chỉ vài ngày vì bị OH oxy hóa nhanh', 'Thời gian sống đúng bằng 1 năm vì bằng thời gian trộn liên bán cầu', 'Thời gian sống vô hạn vì không có bể chứa nào'],
          'Bảng Ch.1 ghi CO₂ "~100+ năm (không có một thời gian sống đơn lẻ)", bể chứa chính là đại dương và sinh quyển; bản đồ gần như đồng đều (±2%).',
          3, 'Bậc độ lớn', src='Đề cương 1.3')
    B.add('Thời gian trộn khoảng nào đúng để so sánh với thời gian sống?',
          'Vài tuần để trộn quanh một dải vĩ độ, khoảng 1 năm để trộn giữa hai bán cầu',
          ['Vài giờ cho dải vĩ độ, vài ngày cho liên bán cầu', 'Vài năm cho dải vĩ độ, vài thập kỷ cho liên bán cầu', 'Vài phút cho dải vĩ độ, 1 tháng cho liên bán cầu'],
          'Đề cương 1.2. Chất có τ ≪ vài tuần chưa kịp trộn quanh dải vĩ độ; chất có τ ≫ 1 năm đã trộn đều toàn cầu.',
          2, 'Đọc bản đồ', src='Đề cương 1.2')
    B.add('Mô hình nào mô tả đúng quan hệ giữa một nguồn điểm NO₂ và hình ảnh vệ tinh phía sau gió?',
          'Cột NO₂ cao nhất tại nguồn rồi giảm hàm mũ theo khoảng cách với độ dài e-fold bằng U·τ',
          ['Cột NO₂ thấp nhất tại nguồn rồi tăng dần theo khoảng cách phía sau gió', 'Cột NO₂ giữ nguyên trên toàn tuyến vì NO₂ không bị mất', 'Cột NO₂ dao động tuần hoàn theo bước sóng'],
          'Hình 2 trong đề cương: τ càng ngắn thì vệt khói giảm càng nhanh; khớp hàm mũ cho τ_NO₂ ≈ 2–6 h.',
          2, 'Đọc bản đồ', src='Đề cương 1.2, hình 2')
    B.essay('(a) Định nghĩa thời gian sống τ của một chất ô nhiễm và nêu cách gộp nhiều bể chứa song song.\n(b) Tính thời gian sống của CO theo OH (k = 2×10⁻¹³ cm³ molecule⁻¹ s⁻¹, [OH] = 1×10⁶ cm⁻³), đổi ra ngày.\n(c) Giải thích vì sao bản đồ NO₂ có điểm nóng còn bản đồ CH₄ gần như đồng đều.',
            '(a) τ = M / L (lượng tồn trữ chia tốc độ mất). Với bể chứa bậc nhất τ = 1/k′. Song song: 1/τ = Σ 1/τᵢ (hóa học, quang phân, lắng đọng khô và ướt).\n'
            f'(b) τ = 1/(k[OH]) = 1/(2×10⁻¹³ × 1×10⁶) = 5×10⁶ s ≈ {d:.0f} ngày ≈ 2 tháng.\n'
            '(c) NO₂ sống vài giờ, bị phân hủy trước khi gió kịp trải đều nên bản đồ ≈ bản đồ nguồn. CH₄ sống ~10 năm ≫ thời gian trộn toàn cầu (~1 năm) nên trộn đều, biến thiên chỉ ~1%.',
            3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q1 (2,5 điểm) + đáp án gợi ý')
    B.essay('Liệt kê ít nhất bốn bể chứa của chất ô nhiễm khí quyển, mỗi bể chứa nêu một ví dụ chất và cơ chế.',
            'Oxy hóa bởi OH (CO + OH → CO₂ + H). Quang phân (NO₂ + hν → NO + O). Lắng đọng khô (O₃, SO₂ trên bề mặt, F = −v_d C). Lắng đọng ướt (HNO₃, NH₃, aerosol qua rainout/washout). '
            'Ngoài ra: hóa học dị thể (N₂O₅ → HNO₃ trên hạt) và vận chuyển lên tầng bình lưu (N₂O, CFC).',
            2, 'Bể chứa', origin='goc', src='Đề cương Ch.1 (Question + checklist)')
    B.essay('Cột NO₂ giảm theo hàm mũ phía sau gió từ một nguồn điểm: ở khoảng cách x = 0, 50 và 100 km, tỉ lệ C/C₀ là 1, 0,61 và 0,37. Gió 5 m/s. Tính τ.',
            'ln(C/C₀) = −x/(Uτ). Từ x = 100 km: ln 0,37 ≈ −0,99 ≈ −1 nên Uτ ≈ 100 km. Vậy τ = 100 000 m / 5 m s⁻¹ = 2×10⁴ s ≈ 5,6 giờ. '
            'Kiểm tra với x = 50 km: exp(−0,5) = 0,61 ✓. Kết quả thuộc khoảng 2–6 h của NO₂.',
            3, 'Tính toán', src='Đề cương 1.2 (bài tập sinh thêm, số đã kiểm bằng Python)')
    # ---------------- SLIDES ----------------
    tp = V['co_oh']
    sl = [
        cover('Bể chứa và thời gian sống của chất ô nhiễm',
              'Sinks and lifetime of air pollutants — Đề cương chương 1',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Satellite Remote Sensing of Atmospheric Composition<br>Đọc thời gian sống từ bản đồ vệ tinh'),
        S('Sáu bể chứa của chất ô nhiễm', cards(
            card('Oxy hóa bởi OH', 'Bể chứa chính của khí phản ứng.<br>CO + OH → CO₂ + H'),
            card('Quang phân', 'Photon UV/khả kiến phá phân tử.<br>NO₂ + hν → NO + O'),
            card('Lắng đọng khô', 'Hấp thụ tại bề mặt, không cần mưa.<br>F = −v<sub>d</sub>·C'),
            card('Lắng đọng ướt', 'Rainout (trong mây) và washout (dưới mây).<br>Khí tan và aerosol'),
            card('Hóa học dị thể', 'Phản ứng trên hạt hoặc giọt mây.<br>N₂O₅ → HNO₃'),
            card('Vận chuyển ra khỏi vùng', 'Lên tầng bình lưu rồi quang phân.<br>N₂O, CFC'), cols=3)),
        S('Thời gian sống và bể chứa song song',
          fm('<span class="l">Định nghĩa</span>τ = M / L &nbsp;&nbsp; (ổn định: τ = M / P)') +
          fm('<span class="l">Nhiều bể chứa song song</span>1/τ = 1/τ<sub>chem</sub> + 1/τ<sub>phot</sub> + 1/τ<sub>dry</sub> + 1/τ<sub>wet</sub>') +
          fm('<span class="l">Hóa học bậc nhất</span>τ<sub>chem</sub> = 1 / (k·[OH])') +
          '<p class="note"><b>M</b>: lượng tồn trữ (khối lượng hoặc số phân tử). <b>L</b>: tốc độ mất tổng. Các tốc độ mất cộng lại, nên τ tổng luôn <b>ngắn hơn</b> bể chứa nhanh nhất.</p>' +
          callout('info', 'Hình dung', 'Bồn nước có nhiều lỗ thoát: các <b>tốc độ</b> thoát cộng lại, các <b>thời gian</b> thì không cộng.')),
        S('Ví dụ: thời gian sống của CO theo OH',
          cols(fm(f'k ≈ 2×10<sup>−13</sup> cm³ s<sup>−1</sup><br>[OH] ≈ 1×10<sup>6</sup> cm<sup>−3</sup>', 34) +
               fm(f'τ = 1/(k[OH]) = 5×10<sup>6</sup> s<br>≈ <b>{tp["tau_days"]:.0f} ngày</b> ≈ 2 tháng', 36),
               ul_([ 'Đổi giây sang ngày: chia cho 86 400', 'Có OH nhiều (nhiệt đới) thì CO sống ngắn hơn', 'Sống ≈ 2 tháng: đủ để CO cháy rừng vượt đại dương'], 34), flex=[1.1, 1]) +
          callout('info', 'Ví dụ song song', 'Hóa học 2 ngày, lắng đọng khô 3 ngày, lắng đọng ướt 6 ngày: 1/τ = 1/2 + 1/3 + 1/6 = 1 → <b>τ = 1 ngày</b>.') + '<p class="note">Kiểm bằng Python: τ = 57,87 ngày cho CO; tổng song song = 1,000 ngày.</p>'),
        S('Thời gian sống và thời gian vận chuyển', cards(
            card('Sống ngắn (giờ – ngày)', 'Bản đồ ≈ <b>bản đồ nguồn</b>: điểm nóng ở thành phố, nhà máy, tàu, cháy.<br>NO₂, SO₂, HCHO'),
            card('Sống vừa (tuần – tháng)', 'Thấy <b>vệt khói quy mô lục địa</b>: CO cháy rừng, bụi vượt Đại Tây Dương.'),
            card('Sống dài (năm – thế kỷ)', 'Trộn đều: bản đồ gần đồng nhất, biến thiên ~1%. Cần độ chính xác cao.<br>CO₂, CH₄, N₂O'), cols=3) +
          '<p class="note">Quãng đường <b>L ≈ U·τ</b> (U ≈ 5–10 m/s). Trộn quanh dải vĩ độ: vài tuần; liên bán cầu: ~1 năm.</p>'),
        S('Thời gian sống theo quy mô biến động', figfit('f1_lifetime', 'Hình 1 (đề cương): thời gian sống so với quy mô không gian của biến động — bậc độ lớn.', 520)),
        S('Suy ra thời gian sống từ vệt khói', figfit('f12_plume', 'Hình 2: NO₂ giảm hàm mũ phía sau gió; vệt càng ngắn thì τ càng nhỏ.', 340) +
          fm('τ = L / U = 50 000 m / 5 m s<sup>−1</sup> = 10<sup>4</sup> s ≈ <b>2,8 giờ</b>', 34) + '<p class="note">Đo độ dài e-fold L của vệt NO₂; khớp hàm mũ C(x) ∝ exp(−x/(U·τ)).</p>'),
        S('Đường suy giảm bậc nhất', figfit('f18_decay', 'Hình 3: C/C₀ = e<sup>−t/τ</sup> cho NO₂, SO₂, aerosol, CO, CH₄ (trục thời gian logarit).', 470) +
          '<p class="note">Tại t = τ còn e<sup>−1</sup> ≈ 36,8%; một nửa mất sau t<sub>½</sub> = τ ln 2 ≈ 0,69 τ.</p>'),
        S('Thời gian sống điển hình (bậc độ lớn)', dtable(tbl(['Loài', 'Thời gian sống', 'Bể chứa chính', 'Trên bản đồ'], [
            ['NO₂ (lớp biên)', '2–12 giờ', 'OH → HNO₃; N₂O₅', 'Điểm nóng'], ['SO₂', '1–2 ngày', 'OH, pha nước, khô', 'Nguồn điểm, núi lửa'],
            ['Aerosol (đối lưu)', '~1 tuần', 'Lắng đọng khô và ướt', 'Vệt vùng'], ['CO', '1–2 tháng', 'OH', 'Vệt liên lục địa'],
            ['CH₄', '9–12 năm', 'OH, đất, bình lưu', 'Gần đồng đều'], ['N₂O, CFC', '50–120 năm', 'Quang phân bình lưu', 'Trộn đều']]), 'xl')),
        S('Exam checklist — Chương 1', chk([
            'Liệt kê ≥ 4 bể chứa: OH, quang phân, lắng đọng khô, lắng đọng ướt (+ dị thể, vận chuyển)',
            'Định nghĩa τ = M/L; gộp bằng 1/τ = Σ 1/τᵢ',
            'So sánh τ với thời gian vận chuyển: τ ngắn → bản đồ nguồn; τ dài → đồng đều',
            'Bậc độ lớn: giờ (NO₂), ngày (SO₂), tuần (aerosol), tháng (CO), chục năm (CH₄), thế kỷ (N₂O, CO₂)'])),
        S('Ý chính', dul([
            'Sáu bể chứa: OH, quang phân, lắng đọng khô/ướt, dị thể, vận chuyển',
            'τ = M/L và 1/τ = Σ 1/τᵢ',
            'τ ngắn → bản đồ giống nguồn; τ dài → đồng đều',
            'NO₂ giờ · SO₂ ngày · CO tháng · CH₄ chục năm']))]
    mod = dict(id='m1', slug='01-sinks-lifetime', title='M1 · Bể chứa & thời gian sống', en='Sinks and lifetime of air pollutants',
               question='<ul><li>What are possible sinks of air pollutants in the atmosphere?</li><li>How do we understand the typical lifetime of an air pollutant by inspecting its spatial distribution from space?</li><li>Provide examples of typical lifetime (orders of magnitude) of air pollutants.</li></ul>',
               calcs=[('lifetime', 'Máy tính thời gian sống'), ('plume', 'Suy τ từ vệt khói')],
               checklist=['Liệt kê ≥ 4 bể chứa: OH, quang phân, lắng đọng khô, lắng đọng ướt (+ hóa học dị thể, vận chuyển).',
                          'Định nghĩa τ = burden / loss rate; gộp bể chứa bằng 1/τ = Σ 1/τᵢ.',
                          'Lifetime vs transport time: τ ngắn → bản đồ nguồn; τ dài → trộn đều.',
                          'Cho bậc độ lớn: giờ (NO₂), ngày (SO₂), tuần (aerosol), tháng (CO), chục năm (CH₄), thế kỷ (N₂O, CO₂).'],
               summary=['Bể chứa: oxy hóa bởi OH, quang phân, lắng đọng khô, lắng đọng ướt, phản ứng dị thể, vận chuyển ra khỏi vùng.',
                        'Thời gian sống τ = lượng tồn trữ / tốc độ mất; nhiều quá trình song song: 1/τ = Σ 1/τᵢ.',
                        'So τ với thời gian vận chuyển: τ ngắn → bản đồ trùng nguồn (NO₂ đô thị); τ dài → đồng đều (CO₂, CH₄).',
                        'Bậc độ lớn: giờ (NO₂), ngày (SO₂), tuần (aerosol, O₃), tháng (CO), chục năm (CH₄), thế kỷ (N₂O, CO₂).'],
               sections=[
        ('Bể chứa là gì?', '<p><b>Hình dung:</b> khí quyển như một bồn nước. Phát thải là vòi cấp; <b>bể chứa (sink)</b> là các lỗ thoát. Chất ô nhiễm ở lại bao lâu phụ thuộc vào việc các lỗ thoát nhanh hay chậm.</p>'
         '<p>Về kỹ thuật, bể chứa là mọi quá trình loại một chất khỏi khối không khí đang xét. Đề cương chia thành sáu loại:</p>' +
         hx_table(['Bể chứa', 'Cơ chế', 'Ví dụ', 'Quan trọng với'], [
             ['Oxy hóa pha khí', 'Gốc OH (cũng O₃, NO₃ ban đêm, halogen)', 'CO + OH → CO₂ + H; CH₄ + OH → CH₃ + H₂O; NO₂ + OH + M → HNO₃', 'Hầu hết khí phản ứng'],
             ['Quang phân', 'Photon UV/khả kiến phá phân tử', 'NO₂ + hν (λ &lt; 420 nm) → NO + O; HCHO + hν; CFC ở bình lưu', 'NO₂, HCHO, CFC'],
             ['Lắng đọng khô', 'Hấp thụ tại bề mặt (khí khổng, đất, nước), v<sub>d</sub>; F = −v<sub>d</sub>·C', 'O₃, SO₂, NH₃, HNO₃, hạt thô', 'Khí tan và hạt thô'],
             ['Lắng đọng ướt', 'Rainout (trong mây, hạt thành CCN) và washout (dưới mây)', 'HNO₃, SO₂, NH₃, aerosol', 'Khí tan, đa số aerosol'],
             ['Hóa học dị thể', 'Phản ứng trên/ trong hạt và giọt mây; khí → hạt', 'N₂O₅ → HNO₃; SO₂ → sulfate trong nước', 'Chuyển khí sang hạt'],
             ['Vận chuyển ra khỏi vùng', 'Đưa lên tầng đối lưu tự do hoặc bình lưu', 'N₂O, CFC lên bình lưu rồi quang phân', 'Khí sống lâu']], 'left') +
         callout('info', 'Phân biệt', '<b>Nguồn</b> (phát thải, sinh học, cháy rừng) khác <b>bể chứa</b>. Chuyển khí thành hạt vừa là bể chứa của khí, vừa là nguồn của aerosol.')),
        ('Thời gian sống τ và cách gộp bể chứa',
         '<p>Thời gian sống cho biết "trung bình một phân tử ở lại bao lâu". Công thức trong đề cương:</p>' + eq('Định nghĩa', 'τ = M / L = M / (F<sub>out</sub> + L<sub>chem</sub> + D<sub>dry</sub> + D<sub>wet</sub>) &nbsp;; trạng thái dừng: τ = M / P') +
         eq('Gộp song song', '1/τ = 1/τ<sub>chem</sub> + 1/τ<sub>photolysis</sub> + 1/τ<sub>dry</sub> + 1/τ<sub>wet</sub> &nbsp;; &nbsp; τ<sub>chem</sub> = 1/(k·[OH])') +
         '<p><b>Cách nhớ:</b> các <i>tốc độ</i> mất cộng lại, các <i>thời gian</i> không cộng. Hai cống thoát cùng chảy thì bồn cạn nhanh hơn từng cống riêng.</p>'
         f'<div class="ex"><div class="exh">Ví dụ 1 · CO theo OH</div><p>k ≈ 2×10⁻¹³ cm³ s⁻¹, [OH] ≈ 1×10⁶ cm⁻³ ⇒ τ = 1/(k[OH]) = 5×10⁶ s ≈ <b>{tp["tau_days"]:.1f} ngày</b> ≈ 2 tháng. (Python: 57,87 ngày.)</p></div>'
         '<div class="ex"><div class="exh">Ví dụ 2 · Ba bể chứa song song</div><p>τ = 2, 3, 6 ngày ⇒ 1/τ = 0,5 + 0,333 + 0,167 = 1,0 ⇒ <b>τ = 1 ngày</b>.</p></div>'
         '<div class="ex"><div class="exh">Ví dụ 3 · Thời gian bán rã khác thời gian sống</div><p>Với bể chứa bậc nhất, nồng độ giảm C/C₀ = e<sup>−t/τ</sup>. Tại t = τ còn e⁻¹ ≈ 36,8%; một nửa mất sau t<sub>½</sub> = τ ln 2 ≈ 0,69 τ.</p></div>' +
         callout('warn', 'Lỗi hay gặp', 'Nhầm τ với thời gian bán rã; cộng thẳng các τ thay vì cộng nghịch đảo; quên đổi giây sang ngày (chia 86 400).')),
        ('Đọc thời gian sống từ bản đồ vệ tinh',
         '<p>Ý tưởng cốt lõi: <b>cuộc đua giữa thời gian sống τ và thời gian vận chuyển</b>. Trong thời gian τ, phân tử đi được quãng đường L ≈ U·τ (U ≈ 5–10 m/s). Trộn quanh một dải vĩ độ mất vài tuần, trộn giữa hai bán cầu mất khoảng một năm.</p>' +
         hx_table(['Loại', 'Hình ảnh vệ tinh', 'Ví dụ'], [
             ['Sống ngắn (giờ – ngày)', 'Bản đồ ≈ bản đồ nguồn: điểm nóng ở thành phố, nhà máy, tàu, cháy rừng; giảm nhanh trong vài chục đến vài trăm km', 'NO₂ (TROPOMI), SO₂, HCHO theo isoprene'],
             ['Sống vừa (tuần – tháng)', 'Thấy vệt khói quy mô lục địa; chênh lệch chủ yếu giữa các bán cầu', 'CO cháy rừng châu Phi/Amazon vượt đại dương; bụi Đại Tây Dương'],
             ['Sống dài (năm – thế kỷ)', 'Gần đồng đều (biến thiên ~1%), chút chênh bắc–nam và chu kỳ mùa; cần độ chính xác rất cao để thấy nguồn', 'CO₂ (OCO-2), CH₄, N₂O']], 'left') +
         lfig('f1_lifetime', 'Hình 1 (đề cương): thời gian sống và quy mô không gian của biến động.') +
         '<p><b>Quy tắc định lượng (quan hệ Junge):</b> σ/C ≈ 0,14/τ với τ tính bằng năm — chất sống càng lâu càng đồng đều. Với CH₄ (τ ≈ 10 năm): σ/C ≈ 1,4%.</p>'
         '<p><b>Suy τ trực tiếp từ vệt khói:</b> phía sau một nguồn điểm, cột NO₂ giảm C(x) ∝ exp(−x/(U·τ)). Khớp hàm mũ cho độ dài e-fold L = U·τ, nên τ = L/U. Ví dụ L = 50 km, U = 5 m/s ⇒ τ = 10⁴ s ≈ <b>2,8 giờ</b> (đề cương: τ<sub>NO₂</sub> ≈ 2–6 h).</p>' +
         lfig('f12_plume', 'Hình 2 (đề cương): suy giảm NO₂ theo chiều gió → suy ra τ.') + lfig('f18_decay', 'Hình 3 (đề cương): đường suy giảm e<sup>−t/τ</sup> cho NO₂, SO₂, aerosol, CO, CH₄.')),
        ('Bảng thời gian sống điển hình (bậc độ lớn)', hx_table(['Loài', 'Thời gian sống', 'Bể chứa chính', 'Hình ảnh từ vũ trụ'], [
            ['OH, NO₃', '~1 s đến vài phút', 'Hóa học rất nhanh', 'Không đo bản đồ trực tiếp'],
            ['NO₂/NOₓ (lớp biên)', 'giờ (2–12 h; dài hơn vào mùa đông)', 'OH → HNO₃, thủy phân N₂O₅', 'Điểm nóng tại nguồn'],
            ['HCHO, glyoxal', 'giờ', 'Quang phân, OH', 'Theo nguồn VOC/cháy'],
            ['SO₂', '~1–2 ngày (vài tuần ở bình lưu)', 'OH, oxy hóa pha nước, lắng đọng khô', 'Nguồn điểm, vệt núi lửa'],
            ['NH₃', 'giờ – 1 ngày', 'Chuyển thành NH₄⁺, lắng đọng', 'Điểm nóng nông nghiệp'],
            ['Aerosol (đối lưu)', '~1 tuần (vài ngày – 2 tuần)', 'Lắng đọng khô và ướt', 'Vệt vùng (bụi, khói)'],
            ['O₃ (đối lưu)', '~3 tuần (ngày ở lớp biên – tháng ở đối lưu tự do)', 'Quang phân + H₂O, NO, HO₂, lắng đọng', 'Nền bán cầu'],
            ['CO', '~1–2 tháng', 'OH', 'Vệt liên lục địa'],
            ['CH₄', '~9–12 năm', 'OH, đất, bình lưu', 'Gần đồng đều, gradient ~1%'],
            ['N₂O, CFC', '~50–120 năm', 'Quang phân bình lưu', 'Trộn đều'],
            ['CO₂', '~100+ năm (không có một τ đơn lẻ)', 'Đại dương và sinh quyển', 'Trộn đều (±2%)']], 'left'))])
    return mod, sl, B

def ul_(items, size=28):
    return '<ul class="tight-ul">' + ''.join(f'<li style="font-size:{size}px">{i}</li>' for i in items) + '</ul>'

def fig2(a, b, ca, cb, hmax=440):
    pa = _PIL.open(os.path.join(ROOT, 'assets/images/fig', a + '.png')).size
    pb = _PIL.open(os.path.join(ROOT, 'assets/images/fig', b + '.png')).size
    wa = int(min(570, hmax * pa[0] / pa[1])); wb = int(min(570, hmax * pb[0] / pb[1]))
    f = lambda n, w, c: f'<figure class="fig ctr" style="flex:1"><img src="../assets/images/fig/{n}.png" alt="" style="width:{w}px"><div class="cap">{c}</div></figure>'
    return f'<div style="display:flex;gap:20px;align-items:flex-start;justify-content:center;margin-top:30px">{f(a, wa, ca)}{f(b, wb, cb)}</div>' + \
           '<p class="note" style="margin-top:36px">Đo độ dài e-fold L của vệt NO₂, rồi τ = L / U. Với U = 5 m/s và L = 50 km: τ ≈ 2,8 giờ.</p>'
