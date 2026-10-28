# -*- coding: utf-8 -*-
"""M6 — Viễn thám aerosol thụ động (đề cương Ch.6)."""
from lib import *
from qcore import Bank
V = VERIFIED
AN = V['angstrom']

def build():
    B = Bank('m6', seed=6)
    al = AN['alpha']
    B.add('Kể ba tính chất của aerosol có thể đo từ cảm biến vệ tinh thụ động.',
          'Độ dày quang học AOD, số mũ Ångström (kích thước hạt), albedo tán xạ đơn ω₀ (hấp thụ)', ['Nhiệt độ hạt, áp suất hạt, khối lượng riêng', 'Độ truyền qua, độ phát xạ, độ sáng nhiệt', 'Tốc độ rơi, điện tích hạt, độ pH'],
          'Đề cương 6.1: còn loại aerosol, chiết suất, độ cao lớp (ALH), chỉ số aerosol UV (UVAI). Đáp án chuẩn gồm ≥ 3 tính chất.', 1, 'Tính chất', origin='goc', src='Đề cương Ch.6 (checklist)')
    B.add('Độ dày quang học aerosol (AOD) được định nghĩa thế nào?',
          'τ_a = ∫ k_ext,aer(z) dz: tích phân hệ số suy giảm của aerosol theo độ cao', ['τ_a = I / I₀, tỉ số cường độ', 'τ_a = λ / r, tỉ số bước sóng với bán kính', 'τ_a = σ_s / σ_a, tỉ số tán xạ với hấp thụ'],
          'Đề cương 6.1/Q6(a). AOD là sản phẩm bền vững nhất và là chỉ báo của lượng aerosol, liên hệ với PM2.5.', 1, 'Tính chất', origin='goc', src='Đề thi mẫu Q6(a)')
    B.add('Số mũ Ångström α được định nghĩa qua quan hệ nào?',
          'τ(λ) = τ(λ₀)·(λ/λ₀)^(−α)', ['τ(λ) = τ(λ₀)·(λ/λ₀)^(+4)', 'τ(λ) = τ(λ₀)·exp(−α·λ)', 'τ(λ) = α/λ'],
          'α đo độ phụ thuộc phổ của AOD. Rayleigh ứng với α ≈ 4; aerosol thô α gần 0; aerosol mịn α lớn.', 1, 'Ångström', origin='goc', src='Đề thi mẫu Q6(a)')
    B.add('Số mũ Ångström α = 1,8 cho biết gì về hạt?',
          'Hạt mịn (khói, đô thị, sulfate)', ['Hạt thô (bụi sa mạc, muối biển)', 'Hạt hoàn toàn không tán xạ', 'Hạt có kích thước đúng bằng bước sóng'],
          'Đáp án gợi ý Q6(a): α ≈ 1,5–2,5 là hạt mịn; α ≈ 0–0,5 là hạt thô.', 1, 'Ångström', origin='goc', src='Đề thi mẫu Q6(a)')
    B.add('Hạt thô như bụi sa mạc và muối biển thường có số mũ Ångström khoảng bao nhiêu?',
          'α ≈ 0–0,5', ['α ≈ 1,5–2,5', 'α ≈ 4', 'α ≈ −2'],
          'Hạt thô tán xạ gần như không phụ thuộc bước sóng nên AOD thay đổi rất ít theo λ.', 1, 'Ångström', src='Đề cương 6.1')
    B.add(f'AOD đo được là 0,60 ở 440 nm và 0,15 ở 870 nm. Số mũ Ångström bằng bao nhiêu?',
          f'α ≈ {al:.2f}', ['α ≈ 0,5', 'α ≈ 1,0', 'α ≈ 4,0'],
          f'α = ln(0,60/0,15) / ln(870/440) = {al:.4f}. Đã kiểm bằng hồi quy log–log (Python). Giá trị ≈ 2 chỉ ra hạt mịn.', 2, 'Ångström', src='Đề cương 6.1 (công thức); số tính bằng Python')
    B.add(f'Với α = {al:.2f} và AOD(440) = 0,60, AOD ở 550 nm xấp xỉ bao nhiêu?',
          f'≈ {AN["tau550"]:.2f}', ['≈ 0,75', '≈ 0,60 (không đổi)', '≈ 0,05'],
          f'τ(550) = 0,60 × (550/440)^(−{al:.3f}) = {AN["tau550"]:.4f}. Bước sóng dài hơn → AOD nhỏ hơn.', 2, 'Ångström', src='Số tính bằng Python')
    B.add('Đại lượng đo trực tiếp của cảm biến thụ động trong viễn thám aerosol là gì?',
          'Hệ số phản xạ phổ (có thể đa góc, phân cực) ở đỉnh khí quyển', ['Hệ số suy giảm dọc theo tia laser', 'Nhiệt độ hạt aerosol', 'Chiết suất phức của hạt'],
          'Đề cương 6.2: ρ(λ,θ₀,θ,φ) = πI/(μ₀E₀). Aerosol tán xạ ánh sáng về vũ trụ nên làm bề mặt tối trở nên sáng hơn.', 1, 'Nguyên lý', origin='goc', src='Đề cương Ch.6 (checklist)')
    B.add('Bốn bước của quy trình truy hồi AOD kiểu MODIS Dark Target / Deep Blue là gì?',
          'Lọc mây và chọn pixel; ước lượng phản xạ bề mặt; tra bảng LUT từ mô hình truyền bức xạ; nghịch đảo tìm AOD và mô hình aerosol khớp nhất', ['Tính AMF; khớp DOAS; trừ bình lưu; chia VCD', 'Phát xung; đo thời gian trễ; nhân tốc độ ánh sáng; chia đôi', 'Lấy log; khớp Planck; đổi sang nhiệt độ sáng; hiệu chỉnh'],
          'Đề cương 6.2: LUT chứa phản xạ đỉnh khí quyển cho tập mô hình aerosol (phân bố kích thước, chiết suất → ω₀, P(Θ)), AOD và hình học.', 2, 'Nguyên lý', origin='goc', src='Đề cương Ch.6 (checklist)')
    B.add('Vì sao truy hồi AOD trên đại dương dễ hơn trên sa mạc trong vùng khả kiến?',
          'Đại dương tối nên tín hiệu aerosol chiếm ưu thế; sa mạc sáng che mất đóng góp của aerosol', ['Đại dương phát xạ mạnh nên nhìn rõ hơn', 'Sa mạc không có aerosol để đo', 'Đại dương có mây nhiều hơn sa mạc'],
          'Đáp án gợi ý Q6(b). Trên bề mặt sáng dùng kênh xanh sâu (412 nm, bề mặt tối), đa góc/phân cực hoặc hồng ngoại nhiệt.', 2, 'Bề mặt', origin='goc', src='Đề thi mẫu Q6(b)')
    B.add('Chiến lược nào được dùng trên bề mặt sáng như sa mạc?',
          'Kênh xanh sâu 412 nm (bề mặt tối ở bước sóng đó), đa góc/phân cực, hoặc hồng ngoại nhiệt', ['Tăng bước sóng lên 10 µm để tăng tán xạ', 'Giả định bề mặt phản xạ bằng 0', 'Chỉ dùng ảnh ban đêm'],
          'Đề cương 6.2 (bước 2) và Q6(b). Deep Blue của MODIS là ví dụ.', 2, 'Bề mặt', origin='goc', src='Đề thi mẫu Q6(b)')
    B.add('Phương pháp thụ động có ưu điểm nào so với lidar chủ động?',
          'Dải quét rộng, phủ toàn cầu hằng ngày, chuỗi dữ liệu dài từ năm 2000, chi phí thấp', ['Cho profil thẳng đứng với phân giải 30–60 m', 'Hoạt động ngày và đêm trên mọi bề mặt', 'Đo trực tiếp độ khử cực của hạt'],
          'Đề cương 6.3. Hai nhóm bổ sung nhau: thụ động cho bản đồ ngang và AOD; chủ động cho cấu trúc thẳng đứng (A-Train: MODIS + CALIOP).', 1, 'Thụ động vs chủ động', origin='goc', src='Đề thi mẫu Q6(c)')
    B.add('Hạn chế chính của phương pháp thụ động là gì?',
          'Ít hoặc không có thông tin thẳng đứng; chỉ ban ngày và trời không mây; phụ thuộc phản xạ bề mặt', ['Chỉ phủ một dải hẹp ~100 m rộng', 'Cần giả định tỉ số lidar để suy ra suy giảm', 'Chu kỳ lặp lại ~16 ngày'],
          'Đề cương 6.3. Còn bất định về loại aerosol và ω₀ do bài toán đa trị.', 1, 'Thụ động vs chủ động', origin='goc', src='Đề thi mẫu Q6(c)')
    B.add('Ưu điểm chính của lidar không gian (CALIOP, ATLID) là gì?',
          'Cho profil thẳng đứng, hoạt động ngày đêm kể cả trên bề mặt sáng hoặc trên mây, và độ khử cực cho biết hình dạng hạt', ['Phủ toàn cầu mỗi ngày với độ rộng quét hàng nghìn km', 'Không cần mô hình hay giả định nào', 'Chi phí thấp, công suất nhỏ'],
          'Đề cương 6.3. Nhược điểm: chân dấu rất hẹp (~100 m, rèm), lặp ~16 ngày; phải giả định tỉ số lidar; S/N thấp ban ngày; đắt.', 2, 'Thụ động vs chủ động', origin='goc', src='Đề thi mẫu Q6(c)')
    B.add('So sánh MODIS và CALIOP cho một vệt bụi Sahara trên Đại Tây Dương: kết luận đúng là gì?',
          'MODIS cho bản đồ AOD hằng ngày và thông tin kích thước nhưng không có độ cao; CALIOP cho profil, ngày đêm, độ khử cực nhưng chỉ một “rèm” hẹp', ['CALIOP cho bản đồ AOD toàn cầu hằng ngày còn MODIS cho profil thẳng đứng', 'Cả hai chỉ hoạt động ban ngày', 'MODIS cho độ khử cực và CALIOP cho bản đồ ngang'],
          'Đáp án gợi ý Q6(c).', 2, 'Thụ động vs chủ động', origin='goc', src='Đề thi mẫu Q6(c)')
    B.add('Chỉ số aerosol UV (UVAI) dùng để làm gì?',
          'Phát hiện định tính aerosol hấp thụ (khói, bụi) kể cả phía trên mây', ['Đo chính xác kích thước hạt', 'Đo độ cao lớp aerosol bằng thời gian trễ', 'Đo độ dày quang học của mây'],
          'Đề cương 6.1: UVAI (ví dụ OMI) nhạy với hấp thụ trong UV, hữu ích khi aerosol nằm trên mây.', 3, 'Tính chất', src='Đề cương 6.1')
    B.add('Cảm biến nào cho thêm thông tin về hàm pha và chiết suất để truy hồi nhiều tính chất hơn?',
          'Đa góc (MISR) và phân cực (POLDER, SPEXone, HARP2)', ['Chỉ cảm biến nadir một kênh', 'Chỉ lidar hồng ngoại nhiệt', 'Chỉ cảm biến vi sóng thụ động'],
          'Đề cương 6.2: đa góc và phân cực thêm thông tin về ω₀, phân bố kích thước, hình dạng.', 3, 'Nguyên lý', src='Đề cương 6.2')
    B.essay('(a) Định nghĩa AOD và số mũ Ångström. α = 1,8 cho biết gì về hạt?\n(b) Vì sao truy hồi AOD trên đại dương dễ hơn trên sa mạc trong vùng khả kiến? Chiến lược trên bề mặt sáng?\n(c) So sánh MODIS và CALIOP cho vệt bụi Sahara trên Đại Tây Dương.',
            '(a) AOD = ∫ k_ext,aer dz; τ(λ) ∝ λ^(−α). α ≈ 1,8 → hạt mịn (khói, đô thị, sulfate).\n(b) Đại dương tối → phản xạ aerosol chiếm ưu thế ở TOA; sa mạc sáng che đóng góp aerosol. Dùng kênh xanh sâu 412 nm, đa góc/phân cực, hoặc hồng ngoại nhiệt.\n'
            '(c) MODIS: dải rộng, bản đồ AOD hằng ngày, thông tin kích thước, nhưng không có độ cao, chỉ ban ngày. CALIOP: profil, ngày đêm, độ khử cực (bụi không cầu), nhưng rèm hẹp, lặp 16 ngày.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q6 (2,5 điểm) + đáp án gợi ý')
    B.essay('Trình bày nguyên lý viễn thám aerosol thụ động: đại lượng đo, các bước truy hồi, ưu và nhược điểm so với phương pháp chủ động.',
            'Đo: phản xạ phổ đỉnh khí quyển ρ = πI/(μ₀E₀) (có thể đa góc, phân cực). ρ_TOA = ρ_Rayleigh + ρ_aer + T·ρ_surf/(1 − Sρ_surf); ρ_aer ≈ ω₀τ_a P(Θ)/(4μ₀μ). Bước: lọc mây → ước lượng phản xạ bề mặt → LUT từ RT → nghịch đảo (bình phương tối thiểu/OE) ra AOD(λ), α, tỉ lệ mode mịn, (ω₀, loại). '
            'Thụ động: toàn cầu, hằng ngày, chuỗi dài, nhưng thiếu thông tin thẳng đứng, chỉ ban ngày/trời quang, phụ thuộc bề mặt. Chủ động: profil, ngày đêm, nhưng phủ hẹp.', 3, 'Tổng hợp', origin='goc', src='Đề cương Ch.6 (Question)')
    B.essay(f'AOD(440) = 0,60 và AOD(870) = 0,15. Tính α và AOD(550); nhận xét về loại hạt.',
            f'α = ln(0,60/0,15)/ln(870/440) = {al:.3f}; AOD(550) = 0,60·(550/440)^(−{al:.3f}) = {AN["tau550"]:.3f}. α ≈ 2 → hạt mịn (khói, đô thị, sulfate), AOD giảm nhanh khi bước sóng tăng.', 2, 'Ångström', src='Đề cương 6.1 (bài tập sinh thêm, số kiểm bằng Python)')
    sl = [
        cover('Viễn thám aerosol thụ động', 'Passive remote sensing of aerosols — Đề cương chương 6',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>AOD · Ångström · ω₀ · LUT · so sánh với lidar'),
        S('Tính chất aerosol đo được từ vệ tinh', cards(
            card('AOD', 'Độ dày quang học, thường ở 550 nm. Chỉ báo lượng aerosol, liên hệ PM2.5.'),
            card('Số mũ Ångström α', 'τ ∝ λ<sup>−α</sup>: α ≈ 0–0,5 hạt thô; α ≈ 1,5–2,5 hạt mịn.'),
            card('Albedo tán xạ đơn ω<sub>0</sub>', 'Mức hấp thụ; từ UV hoặc đa góc, phân cực.'),
            card('Loại và chiết suất', 'Bụi, khói, sulfate, muối biển; MISR, POLDER, 3MI.'),
            card('Độ cao lớp (ALH)', 'Dải A của O₂ (TROPOMI), MISR, TIR cho bụi.'),
            card('Chỉ số aerosol UV', 'Phát hiện aerosol hấp thụ, kể cả trên mây.'), cols=3)),
        S('Nguyên lý: phản xạ đỉnh khí quyển', fm('<span class="l">Đại lượng đo</span>ρ(λ, θ<sub>0</sub>, θ, φ) = π I / (μ<sub>0</sub> E<sub>0</sub>)', 32) +
          fm('<span class="l">Mô hình đơn giản</span>ρ<sub>TOA</sub> = ρ<sub>Rayleigh</sub> + ρ<sub>aer</sub> + T·ρ<sub>surf</sub> / (1 − S ρ<sub>surf</sub>)', 28) +
          fm('ρ<sub>aer</sub> ≈ ω<sub>0</sub> τ<sub>a</sub> P(Θ) / (4 μ<sub>0</sub> μ) &nbsp;(tán xạ đơn)', 28)),
        S('Bốn bước truy hồi', cards(card('1. Lọc mây', 'Chọn pixel không mây, không chói Mặt Trời, không tuyết.'), card('2. Phản xạ bề mặt', 'Đại dương tối; thực vật dùng kênh 2,1 µm; sa mạc dùng 412 nm.'),
          card('3. Bảng tra LUT', 'Mô hình truyền bức xạ cho tập mô hình aerosol, AOD và hình học.'), card('4. Nghịch đảo', 'Tìm AOD và mô hình aerosol khớp nhất → α, tỉ lệ mịn, ω<sub>0</sub>.'), cols=4)),
        S('Số mũ Ångström', figfit('f9_angstrom', 'Hình 17 (đề cương): phụ thuộc phổ của độ dày quang học — Rayleigh và Ångström.', 400) + fm(f'α = ln(τ₁/τ₂) / ln(λ₂/λ₁) = {al:.2f} &nbsp;(AOD 0,60 ở 440 nm; 0,15 ở 870 nm)', 28)),
        S('Ảnh hưởng của bề mặt', figfit('f16_surface', 'Hình 18 (đề cương): phản xạ đỉnh khí quyển theo AOD — nhạy trên đại dương tối, gần như không nhạy trên sa mạc sáng.', 500)),
        S('Thụ động và chủ động: ưu điểm', two6(
            card('Thụ động (MODIS, VIIRS, MISR, POLDER, TROPOMI)', '• Dải quét rộng, phủ toàn cầu hằng ngày<br>• Chuỗi dài từ 2000<br>• Chi phí thấp, nhiều kênh<br>• Cột: AOD, α, ω<sub>0</sub>'),
            card('Chủ động (CALIOP, ATLID)', '• Profil thẳng đứng 30–60 m<br>• Ngày đêm, bề mặt sáng, trên mây<br>• Độ khử cực → hình dạng hạt<br>• Ít giả định về bề mặt'))),
        S('Thụ động và chủ động: hạn chế', two6(
            card('Thụ động', '• Ít hoặc không có thông tin thẳng đứng<br>• Chỉ ban ngày, trời không mây<br>• Phụ thuộc phản xạ bề mặt<br>• Đa trị: bất định loại và ω<sub>0</sub>'),
            card('Chủ động', '• Chân dấu hẹp ~100 m, lặp ~16 ngày<br>• Phải giả định tỉ số lidar<br>• S/N thấp ban ngày<br>• Đắt, công suất lớn'))),
        S('Exam checklist — Chương 6', chk(['≥ 3 tính chất: AOD, α / kích thước, ω<sub>0</sub>, loại, độ cao, UVAI', 'Đo: phản xạ phổ đỉnh khí quyển; aerosol làm bề mặt tối sáng lên', 'Phương pháp: lọc mây → phản xạ bề mặt → LUT → AOD + mô hình khớp nhất', 'Thụ động: phủ toàn cầu, không có thông tin thẳng đứng; chủ động: profil, phủ hẹp'])),
        S('Ý chính', dul(['AOD, α, ω<sub>0</sub>, loại, độ cao lớp', 'Đo phản xạ phổ, truy hồi bằng LUT', 'Bề mặt sáng làm khó: dùng 412 nm, đa góc, TIR', 'Thụ động và lidar bổ sung nhau (A-Train)']))]
    mod = dict(id='m6', slug='06-passive-aerosol', title='M6 · Viễn thám aerosol thụ động', en='Passive remote sensing of aerosols',
               question='<ul><li>What properties of aerosols can be measured from passive satellite sensors (mention at least 3 aerosol properties)?</li><li>Explain the principle of passive remote sensing of aerosols, including the quantity directly measured and how aerosol properties are derived.</li><li>What are the advantages and limitations of this passive approach as compared to active methods?</li></ul>',
               calcs=[('angstrom', 'Ångström và AOD theo bước sóng')],
               checklist=['≥3 properties: AOD, Ångström exponent / size (fine-mode fraction), ω₀ / absorption, type, layer height, UV aerosol index.', 'Measured: TOA spectral (multi-angle, polarised) reflectance; aerosols brighten dark surfaces.',
                          'Method: cloud mask → surface reflectance → LUT from RT model → best-fit AOD + aerosol model.', 'Passive: global coverage, no vertical info, daytime/cloud-free only. Active: profiles, day+night, narrow coverage.'],
               summary=['Tính chất đo được: độ dày quang học AOD, số mũ Ångström (kích thước hạt), albedo tán xạ đơn ω₀ (hấp thụ), loại aerosol, độ cao lớp aerosol, chỉ số aerosol UV.', 'Đại lượng đo: hệ số phản xạ phổ (đa góc, phân cực) ở đỉnh khí quyển; aerosol làm bề mặt tối sáng lên.',
                        'Truy hồi: loại mây → ước lượng phản xạ bề mặt → bảng tra (LUT) từ mô hình truyền bức xạ → chọn AOD + mô hình aerosol phù hợp nhất.', 'Thụ động: phủ toàn cầu, nhưng thiếu thông tin thẳng đứng, chỉ ban ngày & trời quang. Chủ động (lidar): có profil, ngày-đêm, nhưng vùng phủ rất hẹp.'],
               sections=[
        ('Aerosol đo được những gì?', '<p>Aerosol là các hạt lơ lửng (bụi, khói, muối biển, sulfate). Từ vũ trụ ta đo được:</p>' + hx_table(['Tính chất', 'Ý nghĩa', 'Cách đo'], [
            ['AOD τ<sub>a</sub> (ví dụ ở 550 nm)', 'Lượng aerosol trong cột; τ<sub>a</sub> = ∫ k<sub>ext,aer</sub>(z) dz; chỉ báo PM2.5', 'Phản xạ phổ — sản phẩm bền vững nhất'],
            ['Số mũ Ångström α', 'Kích thước hạt: α ≈ 0–0,5 thô (bụi, muối biển); α ≈ 1,5–2,5 mịn (khói, đô thị); tỉ lệ mode mịn', 'Độ phụ thuộc phổ τ ∝ λ<sup>−α</sup>'],
            ['Albedo tán xạ đơn ω<sub>0</sub>', 'Mức hấp thụ', 'UV (OMI UV Aerosol Index) hoặc đa góc/phân cực'],
            ['Loại và chiết suất, tính không cầu', 'Bụi, khói, sulfate, muối biển', 'Đa góc và phân cực: MISR, POLDER/PARASOL, 3MI'],
            ['Độ cao lớp (ALH)', 'Phát tán xa, hiệu ứng bức xạ', 'Dải A của O₂ (TROPOMI), MISR (stereo), TIR cho bụi — xem module 8'],
            ['Chỉ số aerosol UV (UVAI)', 'Phát hiện định tính aerosol hấp thụ', 'UV; hữu ích cả trên mây']], 'left') +
         lfig('f9_angstrom', 'Hình 17 (đề cương): phụ thuộc phổ của độ dày quang học — số mũ Ångström phân biệt hạt mịn và hạt thô.') +
         f'<div class="ex"><div class="exh">Ví dụ · tính α (số kiểm bằng Python)</div><ol class="steps"><li>AOD(440) = 0,60; AOD(870) = 0,15</li><li>α = ln(0,60/0,15) / ln(870/440) = <b>{al:.3f}</b> → hạt mịn</li><li>AOD(550) = 0,60 × (550/440)<sup>−{al:.3f}</sup> = <b>{AN["tau550"]:.3f}</b></li></ol></div>'),
        ('Nguyên lý truy hồi', '<p><b>Đại lượng đo:</b> phản xạ phổ đỉnh khí quyển ρ(λ, θ₀, θ, φ) = πI/(μ₀E₀) — có thể đa góc và phân cực. Aerosol tán xạ ánh sáng về vũ trụ nên làm bề mặt tối sáng lên.</p>' +
         eq('Mô hình đơn giản', 'ρ<sub>TOA</sub>(λ) = ρ<sub>Rayleigh</sub> + ρ<sub>aer</sub> + T(λ) · ρ<sub>surf</sub> / (1 − S ρ<sub>surf</sub>) &nbsp;;&nbsp; ρ<sub>aer</sub> ≈ ω<sub>0</sub> τ<sub>a</sub> P(Θ) / (4 μ<sub>0</sub> μ)') +
         '<ol class="steps"><li><b>Lọc mây</b> và chọn pixel thích hợp (không mây, không chói Mặt Trời, không tuyết).</li><li><b>Ước lượng phản xạ bề mặt</b>: đại dương tối (≈ 0 ở đỏ/NIR); thực vật dùng quan hệ với kênh 2,1 µm; sa mạc sáng dùng “xanh sâu” 412 nm khi bề mặt tối.</li>'
         '<li><b>Bảng tra LUT</b>: mô hình truyền bức xạ tính phản xạ đỉnh khí quyển cho tập mô hình aerosol (phân bố kích thước, chiết suất → ω₀, P(Θ)), AOD và mọi hình học.</li><li><b>Nghịch đảo</b>: tìm mô hình + AOD khớp nhất với phản xạ đa phổ (đa góc) đo được (bình phương tối thiểu / OE) → AOD(λ), α, tỉ lệ mode mịn, (ω₀, loại).</li></ol>' +
         lfig('f16_surface', 'Hình 18 (đề cương): phản xạ đỉnh khí quyển theo AOD — nhạy trên đại dương tối, gần như không nhạy trên sa mạc sáng.')),
        ('Thụ động và chủ động', hx_table(['', 'Thụ động (MODIS, VIIRS, MISR, POLDER, TROPOMI, IASI)', 'Chủ động (CALIOP/CALIPSO, ATLID/EarthCARE)'], [
            ['Ưu điểm', '• Dải quét rộng → phủ toàn cầu hằng ngày, phân giải ngang km<br>• Chuỗi dài, trưởng thành (từ 2000)<br>• Chi phí thấp, công suất nhỏ, nhiều kênh<br>• Đặc tính cột (AOD, α, ω₀)', '• Cho profil thẳng đứng (phân giải ~30–60 m)<br>• Ngày và đêm; trên bề mặt sáng và trên mây<br>• Độ khử cực → hình dạng hạt (bụi hay hạt cầu)<br>• Ít giả định về bề mặt'],
            ['Hạn chế', '• Ít hoặc không có thông tin thẳng đứng<br>• Chỉ ban ngày, trời không mây<br>• Phụ thuộc mạnh phản xạ bề mặt (khó trên sa mạc, tuyết)<br>• Bài toán đa trị: bất định loại, ω₀; nhiễm mây', '• Chân dấu rất hẹp (“rèm” ~100 m), lặp lại ~16 ngày<br>• Phải giả định tỉ số lidar → bất định AOD<br>• S/N thấp ban ngày; bị suy giảm bởi lớp dày<br>• Đắt, công suất lớn']], 'left') +
         callout('good', 'Bổ sung nhau', 'Thụ động cho bản đồ ngang và AOD; chủ động cho cấu trúc thẳng đứng (khái niệm A-Train: MODIS + CALIOP).'))])
    return mod, sl, B

def two6(a, b): return cards(a, b, cols=2)
