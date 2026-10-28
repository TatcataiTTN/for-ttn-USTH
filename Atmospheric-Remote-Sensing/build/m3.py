# -*- coding: utf-8 -*-
"""M3 — Truy hồi khí vết thụ động: đại lượng đo, cột tổng, profil (đề cương Ch.3)."""
from lib import *
from m1 import ul_
from qcore import Bank
V = VERIFIED

def build():
    B = Bank('m3', seed=3)
    A = V['amf']; du = V['DU']
    B.add('Cảm biến thụ động vệ tinh đo trực tiếp đại lượng nào khi nghiên cứu khí vết?',
          'Bức xạ phổ (spectral radiance) đến cảm biến, theo nhiều kênh bước sóng', ['Nồng độ khí tại từng độ cao', 'Cột khí thẳng đứng đã hiệu chỉnh', 'Nhiệt độ phân tử của khí cần tìm'],
          'Cảm biến thụ động không phát xạ và không đo nồng độ trực tiếp; nồng độ được "truy hồi" bằng cách nghịch đảo mô hình truyền bức xạ. Đề cương 3.1.', 1, 'Đại lượng đo', origin='goc', src='Đề cương Ch.3 (checklist)')
    B.add('Trong vùng UV–khả kiến–SWIR (tán xạ ngược Mặt Trời), đại lượng thường dùng để truy hồi là gì?',
          'Hệ số phản xạ R(λ) = π·I(λ) / (μ₀·E₀(λ)), tức radiance chuẩn hóa bằng bức xạ Mặt Trời', ['Nhiệt độ sáng T_B của khí quyển', 'Độ truyền qua I/I₀ qua rìa khí quyển', 'Số mũ Ångström của aerosol'],
          'Đề cương 3.1: đo Earthshine radiance rồi chuẩn hóa với irradiance Mặt Trời → reflectance. Thiết bị: GOME-2, OMI, TROPOMI, OCO-2.', 1, 'Đại lượng đo', src='Đề cương 3.1')
    B.add('Trong hồng ngoại nhiệt, bức xạ thường được biểu diễn dưới dạng nào, và thiết bị nào đo?',
          'Nhiệt độ sáng (brightness temperature); IASI, AIRS, CrIS', ['Hệ số phản xạ; OMI, GOME-2', 'Độ truyền qua; SAGE, ACE-FTS', 'Độ dày quang học; MODIS, VIIRS'],
          'Đề cương 3.1: TIR đo bức xạ phát ra từ bề mặt và khí quyển, hay biểu diễn bằng T_B. Chế độ che khuất đo I/I₀ (ACE-FTS, SAGE).', 1, 'Đại lượng đo', src='Đề cương 3.1')
    B.add('Mô hình thuận (forward model) y = F(x, b) + ε: các ký hiệu có nghĩa gì?',
          'y là phổ đo, x là trạng thái (lượng khí cần tìm), b là tham số khác (nhiệt độ, bề mặt, mây, aerosol), ε là sai số', ['y là trạng thái, x là phổ đo, b là nhiễu, ε là hằng số', 'y là AMF, x là SCD, b là VCD, ε là tán xạ', 'y là tiên nghiệm, x là Jacobian, b là gain, ε là DOFS'],
          'Truy hồi là nghịch đảo F để tìm x từ y. Đề cương 3.1.', 2, 'Đại lượng đo', src='Đề cương 3.1')
    B.add('Cột thẳng đứng VCD được định nghĩa thế nào, và đơn vị thường dùng?',
          'VCD = ∫ n(z) dz, đơn vị molecule cm⁻² (hoặc Dobson Unit cho O₃)', ['VCD = ∫ n(s) ds dọc đường ánh sáng, đơn vị µm', 'VCD = SCD · AMF, đơn vị W m⁻²', 'VCD = n(0) tại mặt đất, đơn vị ppm'],
          'Đề cương 3.2: 1 DU = 2,69×10¹⁶ molecule cm⁻². SCD mới là tích phân dọc đường ánh sáng.', 1, 'Cột tổng', src='Đề cương 3.2')
    B.add(f'Cột O₃ là 300 DU. Quy đổi ra molecule cm⁻² (1 DU ≈ 2,69×10¹⁶).',
          f'≈ {du["example_300DU"]:.2e} molecule cm⁻²'.replace('e+18', '×10¹⁸'), ['≈ 8,1×10¹⁶ molecule cm⁻²', '≈ 1,1×10¹⁴ molecule cm⁻²', '≈ 2,69×10¹⁹ molecule cm⁻²'],
          f'300 × 2,687×10¹⁶ = {du["example_300DU"]:.3e} (Python). Với 2,69×10¹⁶ cho 8,07×10¹⁸.', 2, 'Cột tổng', src='Đề cương 3.2 (hằng số DU); số tính bằng Python')
    B.add('Ba bước chính của truy hồi DOAS cho cột NO₂ đối lưu là gì?',
          '(1) khớp phổ → cột nghiêng SCD; (2) trừ phần bình lưu; (3) chia cho AMF đối lưu để ra VCD', ['(1) tính AMF; (2) lọc mây; (3) khớp hàm Planck', '(1) chọn tiên nghiệm; (2) tính Jacobian; (3) tính DOFS', '(1) đo độ truyền qua; (2) lấy log; (3) vẽ đường cong tăng trưởng'],
          'Đáp án gợi ý Q3(a): khớp ln(I₀/I) = Σσᵢ′SCDᵢ + đa thức; tách bình lưu (sector tham chiếu, mô hình hóa học–vận chuyển); VCD = (SCD − SCD_strat)/AMF_trop.', 2, 'DOAS', origin='goc', src='Đề thi mẫu Q3(a)')
    B.add('Trong DOAS, vì sao dùng tiết diện vi sai σ′ và đa thức?',
          'Đa thức hấp thụ phần biến thiên trơn (Rayleigh, Mie, bề mặt); σ′ khớp các cấu trúc hẹp đặc trưng của khí', ['Để loại bỏ hoàn toàn nhiễu thiết bị', 'Để chuyển bước sóng sang tần số', 'Để biến nghiệm thành ma trận đơn vị'],
          'Đề cương 3.2: ln(I₀/I) = Σ σᵢ′ SCDᵢ + Σ aₚλᵖ. Phần trơn bị tách đi; phần nhanh (cấu trúc phân tử) được khớp bình phương tối thiểu.', 2, 'DOAS', src='Đề cương 3.2')
    B.add('Hệ số khối khí AMF được định nghĩa thế nào?',
          'AMF = SCD / VCD, phản ánh độ dài đường truyền ánh sáng', ['AMF = VCD / SCD, phản ánh nồng độ nền', 'AMF = I₀ / I, phản ánh độ truyền qua', 'AMF = τ / ω₀, phản ánh phần tán xạ'],
          'AMF phụ thuộc hình học Mặt Trời–cảm biến, albedo bề mặt, mây, aerosol và dạng tiên nghiệm của profil. Xấp xỉ hình học: AMF ≈ 1/cos θ₀ + 1/cos θ.', 1, 'AMF', src='Đề cương 3.2')
    B.add(f'Xấp xỉ hình học AMF ≈ 1/cos θ₀ + 1/cos θ với θ₀ = 60° và θ = 30°. Giá trị là bao nhiêu?',
          f'≈ {A["amf"]:.2f}', ['≈ 1,50', '≈ 2,00', '≈ 5,20'],
          f'1/cos 60° = 2; 1/cos 30° = 1,1547 → tổng {A["amf"]:.4f}. (Khi cả hai góc bằng 0: AMF = 2.)', 2, 'AMF', src='Đề cương 3.2; số tính bằng Python')
    B.add(f'SCD = 8×10¹⁵, phần bình lưu SCD_strat = 3×10¹⁵ molecule cm⁻², AMF đối lưu = {A["amf"]:.2f}. Cột đối lưu VCD bằng bao nhiêu?',
          f'≈ {A["vcd"]:.2e} molecule cm⁻²'.replace('e+15', '×10¹⁵'), ['≈ 2,5×10¹⁵ molecule cm⁻² (quên trừ phần bình lưu)', '≈ 1,6×10¹⁶ molecule cm⁻² (nhân thay vì chia)', '≈ 5,0×10¹⁵ molecule cm⁻² (quên chia AMF)'],
          f'VCD = (SCD − SCD_strat)/AMF = 5×10¹⁵ / {A["amf"]:.4f} = {A["vcd"]:.3e}. Đã tính lại bằng Python.', 2, 'AMF', src='Đề cương 3.2 (công thức VCD); số tính bằng Python')
    B.add('Tại sao AMF phụ thuộc vào dạng profil tiên nghiệm và mây?',
          'Vì độ nhạy ánh sáng thay đổi theo độ cao: thấp gần mặt đất, bị che dưới mây, tăng trên mây; kết quả phụ thuộc giả định khí nằm ở đâu', ['Vì mây và tiên nghiệm làm thay đổi số phân tử khí thực tế trong khí quyển', 'Vì AMF chỉ phụ thuộc cấu hình quỹ đạo vệ tinh', 'Vì mây phát xạ nhiệt thay cho khí'],
          'Đáp án gợi ý Q3(b): AMF = SCD/VCD đo độ dài đường truyền; nhạy khác nhau theo độ cao nên cần giả định phân bố thẳng đứng.', 2, 'AMF', origin='goc', src='Đề thi mẫu Q3(b)')
    B.add('Để truy hồi profil theo độ cao, phương pháp chuẩn của Rodgers là gì?',
          'Ước lượng tối ưu (Optimal Estimation) với Jacobian K và profil tiên nghiệm x_a', ['Hồi quy tuyến tính bội không có tiên nghiệm', 'Biến đổi Fourier của phổ phát xạ', 'Phép đo trực tiếp bằng kính thiên văn'],
          'Đề cương 3.3: tối thiểu χ² = (y−F(x))ᵀS_ε⁻¹(y−F(x)) + (x−x_a)ᵀS_a⁻¹(x−x_a). Bài toán đa trị, nên cần chính quy hóa.', 2, 'Profil', src='Đề cương 3.3')
    B.add('Công thức nghiệm tuyến tính của ước lượng tối ưu là gì?',
          'x̂ = x_a + (KᵀS_ε⁻¹K + S_a⁻¹)⁻¹ KᵀS_ε⁻¹ (y − K·x_a)', ['x̂ = x_a · K / y', 'x̂ = (y − x_a) · S_a · S_ε', 'x̂ = K⁻¹ y không cần tiên nghiệm'],
          'Trong đó x_a: tiên nghiệm, S_a: hiệp phương sai của nó, S_ε: hiệp phương sai nhiễu đo. Nếu phi tuyến thì lặp Gauss–Newton.', 3, 'Profil', src='Đề cương 3.3')
    B.add('Thông tin độ cao của khí đến từ đâu khi cảm biến nhìn thẳng xuống (nadir)? Chọn đáp án đầy đủ nhất.',
          'Độ hấp thụ mạnh yếu theo bước sóng (xuyên sâu khác nhau), mở rộng vạch theo áp suất, tương phản nhiệt độ T(z)', ['Chỉ từ độ trễ thời gian của xung laser', 'Chỉ từ góc quan sát thay đổi theo tiếp tuyến', 'Chỉ từ kích thước mặt đất của pixel'],
          'Đề cương 3.4: UV (BUV/SBUV: 270 nm nhạy tầng bình lưu cao, 310–330 nm xuống đối lưu); TIR (rộng vạch ∝ áp suất: tâm vạch nhìn cao, cánh vạch nhìn thấp); T(z) tạo tương phản phát xạ. Limb thì nhờ hình học.', 2, 'Thông tin thẳng đứng', origin='goc', src='Đề thi mẫu Q3(c)')
    B.add('Trong hồng ngoại nhiệt, phần nào của vạch phổ nhìn vào độ cao thấp?',
          'Cánh vạch (wings), vì mở rộng áp suất làm vạch rộng ở khí quyển thấp', ['Tâm vạch, vì áp suất thấp làm vạch hẹp', 'Cả vạch như nhau', 'Không có phần nào, vạch không mang thông tin độ cao'],
          'Độ rộng vạch Lorentz ∝ áp suất: tâm vạch (hấp thụ mạnh) bị bão hòa ở độ cao lớn và nhìn cao; cánh vạch (hấp thụ yếu) xuyên xuống thấp. Đề cương 3.4.', 3, 'Thông tin thẳng đứng', src='Đề cương 3.4')
    B.add('Vì sao tia UV 270 nm nhạy với tầng bình lưu cao còn 310–330 nm nhạy đến đối lưu (phương pháp BUV)?',
          'Ở 270 nm O₃ hấp thụ rất mạnh nên photon không xuyên sâu; ở 310–330 nm hấp thụ yếu nên photon xuống thấp hơn', ['Vì O₃ chỉ tồn tại trên 40 km nên 270 nm nhìn thấy nó', 'Vì tia 310–330 nm bị phản xạ hoàn toàn trên mây', 'Vì 270 nm có bước sóng dài hơn nên xuyên sâu hơn'],
          'Đề cương 3.4: độ mạnh hấp thụ khác nhau theo λ → độ sâu xuyên khác nhau → hàm trọng số đỉnh ở độ cao khác nhau.', 3, 'Thông tin thẳng đứng', src='Đề cương 3.4')
    B.add('Trường hợp nào dưới đây cảm biến KHÔNG đo trực tiếp nồng độ mà phải truy hồi?',
          'Mọi trường hợp viễn thám thụ động: đo radiance rồi nghịch đảo mô hình truyền bức xạ', ['Chỉ khi có mây', 'Chỉ ở hồng ngoại nhiệt', 'Chỉ trong chế độ limb'],
          'Nguyên tắc cốt lõi của Ch.3: đại lượng đo là bức xạ phổ, không phải nồng độ.', 1, 'Đại lượng đo', src='Đề cương 3.1')
    B.essay('(a) Giải thích ba bước của truy hồi DOAS cho cột NO₂ đối lưu từ thiết bị nadir UV–khả kiến.\n(b) Vì sao AMF phụ thuộc dạng profil tiên nghiệm và mây?\n(c) Nêu hai lý do vật lý để cảm biến nadir có thông tin về phân bố thẳng đứng của khí.',
            '(a) 1) Khớp phổ ln(I₀/I) = Σσᵢ′SCDᵢ + đa thức bằng bình phương tối thiểu → SCD. 2) Trừ phần bình lưu (sector tham chiếu hoặc mô hình hóa học–vận chuyển). 3) Chia cho AMF đối lưu từ mô hình truyền bức xạ → VCD.\n'
            '(b) AMF = SCD/VCD là độ dài đường truyền; độ nhạy thay đổi theo độ cao (thấp gần bề mặt, che dưới mây, tăng trên mây) nên kết quả phụ thuộc nơi khí được giả định nằm.\n'
            '(c) Độ hấp thụ mạnh yếu theo λ (độ xuyên sâu khác nhau); mở rộng vạch theo áp suất; tương phản nhiệt độ T(z) trong TIR.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q3 (2,5 điểm) + đáp án gợi ý')
    B.essay('Trình bày nguyên lý truy hồi cột tổng và profil của khí vết; thông tin về độ cao đến từ đâu?',
            'Đại lượng đo: bức xạ phổ I(λ) (hoặc phản xạ, nhiệt độ sáng), không phải nồng độ. Cột: DOAS → SCD, VCD = SCD/AMF. Profil: y = y₀ + K(x − x₀) + ε, K = ∂F/∂x (Jacobian/hàm trọng số); ill-posed nên chính quy hóa bằng Optimal Estimation (Rodgers). '
            'Thông tin độ cao: hấp thụ mạnh yếu theo λ, mở rộng áp suất, tương phản nhiệt độ, hình học limb/che khuất.', 3, 'Tổng hợp', origin='goc', src='Đề cương Ch.3 (Question)')
    B.essay(f'Tính AMF hình học và VCD: θ₀ = 60°, θ = 30°, SCD = 8×10¹⁵, SCD_strat = 3×10¹⁵ molecule cm⁻².',
            f'AMF ≈ 1/cos 60° + 1/cos 30° = 2 + 1,1547 = {A["amf"]:.4f}. VCD = (SCD − SCD_strat)/AMF = 5×10¹⁵ / {A["amf"]:.4f} ≈ {A["vcd"]:.3e} molecule cm⁻². Đổi ra DU nếu là O₃: chia cho 2,687×10¹⁶.', 3, 'AMF', src='Đề cương 3.2 (bài tập sinh thêm, số kiểm bằng Python)')
    sl = [
        cover('Truy hồi khí vết: cột tổng và profil', 'Passive remote sensing of trace gases — Đề cương chương 3',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Bức xạ phổ · DOAS · AMF · Optimal Estimation'),
        S('Đại lượng đo: bức xạ phổ, không phải nồng độ', cards(
            card('UV – khả kiến – SWIR', 'Radiance Mặt Trời tán xạ ngược → reflectance R(λ).<br>GOME-2, OMI, TROPOMI, OCO-2'),
            card('Hồng ngoại nhiệt', 'Bức xạ phát ra, biểu diễn bằng nhiệt độ sáng T<sub>B</sub>.<br>IASI, AIRS, CrIS'),
            card('Che khuất', 'Độ truyền qua I/I<sub>0</sub> của Mặt Trời hoặc sao qua rìa khí quyển.<br>ACE-FTS, SAGE'), cols=3)),
        S('Mô hình thuận và truy hồi', fm('<span class="l">Mô hình thuận</span>y = F(x, b) + ε', 38) +
          legend([('y', 'phổ đo được'), ('x', 'trạng thái: lượng khí cần tìm'), ('b', 'nhiệt độ, bề mặt, mây, aerosol'), ('ε', 'sai số đo')], 2) +
          fm('<span class="l">Phản xạ</span>R(λ) = π I(λ) / (μ<sub>0</sub> E<sub>0</sub>(λ))', 32)),
        S('Ảnh slide: GOME và TROPOMI', cols(figfit('s1_gome', 'Hình 8: GOME — irradiance Mặt Trời và radiance Trái Đất; tỉ số là reflectance.', 500, 560, 'jpg', 'slides'),
                                           figfit('s2_tropomi', 'Hình 9: radiance L1b một pixel TROPOMI (siêu phổ) so với kênh rộng VIIRS.', 500, 560, 'jpg', 'slides'))),
        S('Cột tổng: DOAS bước 1', fm('<span class="l">Khớp phổ → cột nghiêng</span>ln( I<sub>0</sub>(λ) / I(λ) ) = Σ<sub>i</sub> σ<sub>i</sub>′(λ) · SCD<sub>i</sub> + Σ<sub>p</sub> a<sub>p</sub> λ<sup>p</sup>', 30) +
          figfit('f13_doas', 'Hình 10: DOAS — bỏ phần trơn, khớp cấu trúc hẹp bằng tiết diện phòng thí nghiệm.', 380) + '<p class="note">SCD = ∫ n ds dọc đường ánh sáng; σ′ lấy từ phòng thí nghiệm.</p>'),
        S('Cột tổng: AMF và VCD', fm('<span class="l">Cột thẳng đứng</span>VCD = (SCD − SCD<sub>strat</sub>) / AMF<sub>trop</sub> &nbsp;,&nbsp; AMF = SCD / VCD', 30) +
          fm('<span class="l">Xấp xỉ hình học</span>AMF ≈ 1/cos θ<sub>0</sub> + 1/cos θ', 30) +
          callout('info', f'Ví dụ θ₀ = 60°, θ = 30°', f'AMF = 2 + 1,155 = <b>{A["amf"]:.2f}</b>; SCD = 8×10<sup>15</sup>, SCD<sub>strat</sub> = 3×10<sup>15</sup> → VCD ≈ <b>{A["vcd"]/1e15:.2f}×10<sup>15</sup></b> molecule cm<sup>−2</sup>')),
        S('Profil: ước lượng tối ưu (Optimal Estimation)', fm('<span class="l">Tuyến tính hóa</span>y = y<sub>0</sub> + K (x − x<sub>0</sub>) + ε &nbsp;,&nbsp; K = ∂F/∂x', 28) +
          fm('<span class="l">Nghiệm</span>x̂ = x<sub>a</sub> + (K<sup>T</sup>S<sub>ε</sub><sup>−1</sup>K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup> K<sup>T</sup>S<sub>ε</sub><sup>−1</sup> (y − K x<sub>a</sub>)', 26) +
          '<p class="note">x<sub>a</sub>: profil tiên nghiệm · S<sub>a</sub>: hiệp phương sai của nó · S<sub>ε</sub>: hiệp phương sai nhiễu đo. Bài toán đa trị nên phải chính quy hóa.</p>'),
        S('Thông tin độ cao đến từ đâu?', cols(figfit('f6_wf', 'Hình 12: hàm trọng số đỉnh ở các độ cao khác nhau.', 480, 480),
          ulb(['<b>Hấp thụ mạnh yếu</b> theo λ: xuyên sâu khác nhau', '<b>Mở rộng áp suất</b>: tâm vạch nhìn cao, cánh vạch nhìn thấp', '<b>Nhiệt độ T(z)</b> tạo tương phản phát xạ', '<b>Hình học limb</b>: độ cao tiếp tuyến'], 27, 20), flex=[0.8, 1.2])),
        S('Cửa sổ bước sóng cho từng khí', figfit('s3_wavelengths', 'Hình 11 (ảnh slide): cửa sổ bước sóng cho SO₂, HCHO, BrO, NO₂, O₃, OClO, O₂–O₂, H₂O, O₂, aerosol.', 520, 700, 'jpg', 'slides')),
        S('Exam checklist — Chương 3', chk(['Đại lượng đo = bức xạ phổ (reflectance, T<sub>B</sub>, độ truyền qua), không phải nồng độ', 'Cột: DOAS → SCD; AMF từ mô hình truyền bức xạ → VCD = SCD/AMF',
            'Profil: mô hình thuận + Jacobian K + Optimal Estimation với tiên nghiệm', 'Thông tin độ cao: λ, mở rộng áp suất, tương phản nhiệt độ, hình học limb'])),
        S('Ý chính', dul(['Đo bức xạ phổ, truy hồi bằng nghịch đảo mô hình truyền bức xạ', 'Cột: SCD từ DOAS rồi chia AMF', 'Profil: Optimal Estimation, tiên nghiệm x<sub>a</sub>', 'Thông tin độ cao từ λ, áp suất, nhiệt độ, hình học']))]
    mod = dict(id='m3', slug='03-passive-trace-gas', title='M3 · Truy hồi khí vết: cột và profil', en='Passive remote sensing of trace gases',
               question='<ul><li>What is the quantity directly measured by passive satellite sensors for remote sensing of atmospheric trace gases?</li><li>Explain the principle to derive the abundance of a trace gas in terms of (i) integrated concentration over the atmospheric column and (ii) vertical profile of gas concentration.</li><li>Where is the information on the vertical distribution of the gas coming from?</li></ul>',
               calcs=[('doas', 'DOAS: AMF → VCD → DU')],
               checklist=['Measured quantity = spectral radiance (reflectance / brightness temperature / transmission), NOT concentration.', 'Column: DOAS fit → SCD; AMF from RT model → VCD = SCD/AMF.',
                          'Profile: forward model + Jacobian K + Optimal Estimation with a priori.', 'Vertical information: different penetration depths vs λ, pressure broadening of lines, temperature contrast, limb geometry.'],
               summary=['Cảm biến thụ động đo bức xạ phổ (radiance) — không đo nồng độ trực tiếp; nồng độ được “truy hồi” bằng cách nghịch đảo mô hình truyền bức xạ.', 'Cột tổng: DOAS → cột nghiêng SCD; hệ số khối khí AMF → cột thẳng đứng VCD = SCD/AMF.',
                        'Profil thẳng đứng: ước lượng tối ưu (Optimal Estimation) dùng ma trận Jacobian K và profil tiên nghiệm.', 'Thông tin độ cao đến từ: độ hấp thụ mạnh/yếu theo bước sóng, mở rộng vạch theo áp suất, tương phản nhiệt độ, và hình học quan sát limb.'],
               sections=[
        ('Đại lượng đo trực tiếp', '<p>Cảm biến thụ động <b>không tự phát sáng</b>; nó chỉ ghi <b>bức xạ phổ I(λ)</b> (W m⁻² sr⁻¹ µm⁻¹) đến từ một hướng ngắm, trên nhiều kênh bước sóng (một phổ). Nồng độ khí <b>không bao giờ</b> được đo trực tiếp.</p>' +
         hx_table(['Vùng phổ', 'Đại lượng', 'Thiết bị'], [['UV – khả kiến – SWIR (Mặt Trời tán xạ ngược)', 'Radiance chuẩn hóa → reflectance R(λ) = π I / (μ₀ E₀)', 'GOME-2, OMI, TROPOMI, OCO-2'],
                                                          ['Hồng ngoại nhiệt', 'Nhiệt độ sáng T_B', 'IASI, AIRS, CrIS'], ['Che khuất', 'Độ truyền qua I/I₀', 'ACE-FTS, SAGE']], 'left') +
         eq('Mô hình thuận', 'y = F(x, b) + ε') + '<p>Truy hồi (retrieval) là <b>nghịch đảo</b> mô hình truyền bức xạ F để tìm trạng thái x (lượng khí) từ phổ đo y, trong khi b (nhiệt độ, bề mặt, mây, aerosol) là tham số khác.</p>' +
         lfig('s1_gome', 'Hình 8 (ảnh slide bài giảng): GOME — irradiance Mặt Trời và radiance Trái Đất; tỉ số là reflectance.', ext='jpg', folder='slides', w=560) +
         lfig('s2_tropomi', 'Hình 9 (ảnh slide bài giảng): radiance L1b một pixel TROPOMI (siêu phổ) so với các kênh rộng của VIIRS.', ext='jpg', folder='slides', w=560)),
        ('(i) Cột tổng: DOAS', '<p><b>Cột thẳng đứng</b> VCD = ∫ n(z) dz (molecule cm⁻²; O₃ dùng Dobson Unit, 1 DU = 2,69×10¹⁶ molecule cm⁻²). Cách làm chuẩn trong UV–khả kiến là <b>DOAS</b> (Differential Optical Absorption Spectroscopy), ba bước:</p>'
         '<ol class="steps"><li><b>Khớp phổ → cột nghiêng (SCD).</b> Từ Beer–Lambert, tách độ dày quang học thành phần biến thiên nhanh (cấu trúc hấp thụ phân tử) và phần trơn (Rayleigh, Mie, bề mặt).</li>'
         '<li><b>Hệ số khối khí (AMF).</b> Mô hình truyền bức xạ tính AMF = SCD / VCD, phụ thuộc hình học, albedo, mây, aerosol và dạng tiên nghiệm của profil.</li>'
         '<li><b>Tách bình lưu – đối lưu</b> (cho khí đối lưu): sector tham chiếu trên đại dương sạch hoặc đồng hóa mô hình hóa học–vận chuyển.</li></ol>' +
         eq('Khớp phổ', 'ln( I<sub>0</sub>(λ) / I(λ) ) = Σ<sub>i</sub> σ<sub>i</sub>′(λ) · SCD<sub>i</sub> + Σ<sub>p</sub> a<sub>p</sub> λ<sup>p</sup> &nbsp;;&nbsp; SCD = ∫ n ds') + eq('Cột đối lưu', 'VCD = (SCD − SCD<sub>strat</sub>) / AMF<sub>trop</sub> &nbsp;;&nbsp; AMF ≈ 1/cos θ<sub>0</sub> + 1/cos θ (xấp xỉ hình học)') +
         lfig('f13_doas', 'Hình 10 (đề cương): DOAS — phần trơn bị bỏ, cấu trúc hẹp được khớp với tiết diện phòng thí nghiệm để ra SCD.') +
         f'<div class="ex"><div class="exh">Ví dụ · AMF và VCD (số đã kiểm bằng Python)</div><ol class="steps"><li>θ₀ = 60°, θ = 30° → AMF = 2 + 1,1547 = <b>{A["amf"]:.4f}</b></li><li>SCD = 8×10¹⁵; SCD<sub>strat</sub> = 3×10¹⁵ molecule cm⁻²</li><li>VCD = 5×10¹⁵ / {A["amf"]:.4f} = <b>{A["vcd"]:.3e}</b> molecule cm⁻²</li></ol></div>' +
         lfig('s3_wavelengths', 'Hình 11 (ảnh slide bài giảng): cửa sổ bước sóng chọn cho từng khí (SO₂, HCHO, BrO, NO₂, O₃, OClO, O₂–O₂, H₂O, O₂, aerosol).', ext='jpg', folder='slides', w=620) +
         '<p><b>Phương pháp khác:</b> Optimal Estimation với co giãn profil tiên nghiệm (CO ở SWIR/TIR) hoặc phương pháp tỉ số cho khí nhà kính (XCO₂ = cột CO₂ / cột không khí khô, dùng dải A của O₂).</p>'),
        ('(ii) Profil thẳng đứng: Optimal Estimation', '<p>Chia khí quyển thành N lớp, trạng thái x = (x₁…x_N). Tuyến tính hóa quanh điểm tham chiếu:</p>' + eq('Tuyến tính hóa', 'y = y<sub>0</sub> + K (x − x<sub>0</sub>) + ε &nbsp;;&nbsp; K = ∂F/∂x (Jacobian, hàm trọng số)') +
         '<p>Bài toán <b>đa trị (ill-posed)</b>: nhiều ẩn hơn lượng thông tin độc lập, lại có nhiễu — nên phải chính quy hóa. Phương pháp chuẩn là <b>Optimal Estimation</b> (Rodgers):</p>' +
         eq('Hàm mục tiêu', 'χ² = (y − F(x))<sup>T</sup> S<sub>ε</sub><sup>−1</sup> (y − F(x)) + (x − x<sub>a</sub>)<sup>T</sup> S<sub>a</sub><sup>−1</sup> (x − x<sub>a</sub>)') +
         eq('Nghiệm tuyến tính', 'x̂ = x<sub>a</sub> + (K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup> K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> (y − K x<sub>a</sub>)') +
         '<p>x<sub>a</sub>: profil tiên nghiệm; S<sub>a</sub>: hiệp phương sai của nó; S<sub>ε</sub>: hiệp phương sai nhiễu đo. Nếu phi tuyến thì lặp Gauss–Newton. Phương pháp khác: chính quy hóa Tikhonov, “bóc hành” (onion peeling) cho dữ liệu limb.</p>'),
        ('Thông tin về độ cao đến từ đâu?', '<p>Từ việc <b>các phép đo nhạy ở các độ cao khác nhau</b>, tức hàm trọng số K(z) có đỉnh ở các độ cao khác nhau:</p>' +
         hx_table(['Nguồn thông tin', 'Cách hoạt động', 'Ví dụ'], [
             ['Độ mạnh hấp thụ theo λ (nadir)', 'Hấp thụ mạnh → photon không xuyên sâu → tín hiệu từ trên cao; hấp thụ yếu → từ thấp', 'O₃ UV: 270 nm nhạy bình lưu cao; 310–330 nm xuống đối lưu (BUV/SBUV)'],
             ['Dạng vạch phụ thuộc áp suất và nhiệt độ (TIR)', 'Độ rộng vạch ∝ áp suất: tâm vạch nhìn cao, cánh vạch nhìn thấp; T(z) tạo tương phản phát xạ', 'Profil O₃/CO của IASI'],
             ['Hình học quan sát (limb, che khuất)', 'Mỗi tia có độ cao tiếp tuyến; quét limb cho phân giải thẳng đứng 1–3 km', 'Bóc hành (onion peeling)'],
             ['Khác', 'Tiết diện phụ thuộc nhiệt độ, nhiều góc nhìn, Raman/Rayleigh', 'Thêm một ít thông tin']], 'left') +
         lfig('f6_wf', 'Hình 12 (đề cương): hàm trọng số có đỉnh ở các độ cao khác nhau khi độ mạnh hấp thụ khác nhau.', w=460))])
    return mod, sl, B
