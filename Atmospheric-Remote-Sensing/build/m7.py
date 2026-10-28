# -*- coding: utf-8 -*-
"""M7 — Các chế độ tán xạ của ánh sáng bởi hạt (đề cương Ch.7)."""
from lib import *
from qcore import Bank
V = VERIFIED
SZ = V['size']; MQ = V['mie_qext_m133']

def build():
    B = Bank('m7', seed=7)
    B.add('Tham số kích thước x được định nghĩa thế nào?',
          'x = 2πr / λ (r: bán kính hạt, λ: bước sóng)', ['x = λ / (2πr)', 'x = r · λ', 'x = 4π r² / λ'],
          'Chế độ tán xạ do x và chiết suất phức m = n + ik quyết định. Đề cương Ch.7.', 1, 'Tham số x', origin='goc', src='Đề cương Ch.7 (checklist)')
    B.add('Ba chế độ tán xạ theo tham số kích thước là gì?',
          'Rayleigh (x ≪ 1), Mie (x ≈ 0,1–50), quang hình học (x ≫ 1)', ['Rayleigh (x ≫ 1), Mie (x ≈ 1), quang hình học (x ≪ 1)', 'Raman, Rayleigh, Brillouin', 'Nadir, limb, che khuất'],
          'Đề cương Ch.7: Rayleigh x < ~0,1; Mie x ≈ 0,1–50; quang hình học x > ~50–100.', 1, 'Chế độ', origin='goc', src='Đề cương Ch.7 (checklist)')
    B.add('Tính tham số kích thước của một phân tử N₂ (r ≈ 0,2 nm) ở λ = 0,55 µm và chế độ tán xạ.',
          f'x ≈ {SZ["N2"]:.3f} → Rayleigh', [f'x ≈ {SZ["sulfate"]:.1f} → Mie', f'x ≈ {SZ["dust"]:.0f} → Mie rộng/quang hình', 'x ≈ 0,5 → Mie'],
          f'x = 2π × 2×10⁻⁴ µm / 0,55 µm = {SZ["N2"]:.5f} ≪ 1 (Python).', 1, 'Tham số x', origin='goc', src='Đề thi mẫu Q7(a)(i)')
    B.add('Tính tham số kích thước hạt sulfate r = 0,2 µm ở λ = 0,55 µm và chế độ tán xạ.',
          f'x ≈ {SZ["sulfate"]:.1f} → Mie', [f'x ≈ {SZ["N2"]:.3f} → Rayleigh', f'x ≈ {SZ["dust"]:.0f} → quang hình học', 'x ≈ 0,023 → Rayleigh'],
          f'x = 2π × 0,2 / 0,55 = {SZ["sulfate"]:.4f}. Cỡ 1–2 nên là chế độ Mie (cộng hưởng).', 1, 'Tham số x', origin='goc', src='Đề thi mẫu Q7(a)(ii)')
    B.add('Tính tham số kích thước hạt bụi r = 5 µm ở λ = 0,55 µm và chế độ tán xạ.',
          f'x ≈ {SZ["dust"]:.0f} → phần trên của Mie, tiến gần quang hình học', [f'x ≈ {SZ["N2"]:.3f} → Rayleigh', f'x ≈ {SZ["sulfate"]:.1f} → Mie dưới', 'x ≈ 570 → quang hình học thuần'],
          f'x = 2π × 5 / 0,55 = {SZ["dust"]:.2f}. Mie vẫn áp dụng (đúng cho cầu) nhưng quang hình học là xấp xỉ tốt cho hạt lớn nhất. Bụi không cầu cần T-matrix.', 2, 'Tham số x', origin='goc', src='Đề thi mẫu Q7(a)(iii)')
    B.add('Chế độ tán xạ của aerosol thô (bụi, muối biển, r ≈ 1–10 µm) với ánh sáng khả kiến là gì?',
          f'Mie phần trên (x ≈ {SZ["coarse_1"]:.0f}–{SZ["coarse_10"]:.0f}), gần quang hình học; Ångström α ≈ 0–0,5', ['Rayleigh vì hạt nhỏ hơn bước sóng', 'Raman vì hạt đổi bước sóng', 'Quang hình học thuần, không cần Mie'],
          f'x = 2π × (1 đến 10) / 0,55 = {SZ["coarse_1"]:.1f} đến {SZ["coarse_10"]:.1f}. Đề cương 7.4.', 2, 'Aerosol thô', origin='goc', src='Đề cương 7.4 (câu hỏi gốc của chương)')
    B.add('Tán xạ Rayleigh có hệ phụ thuộc kích thước và bước sóng nào?',
          'σ_s ∝ r⁶ / λ⁴', ['σ_s ∝ r² / λ²', 'σ_s ∝ r / λ', 'σ_s ∝ r⁴ λ⁶'],
          'σ_s = (8π/3) k⁴ r⁶ |(m²−1)/(m²+2)|². Gấp đôi bán kính thì tăng 2⁶ = 64 lần; giảm một nửa bước sóng thì tăng 2⁴ = 16 lần.', 2, 'Rayleigh', src='Đề cương 7.1')
    B.add('Nếu bán kính hạt Rayleigh tăng gấp đôi (giữ nguyên λ), tiết diện tán xạ tăng bao nhiêu lần?',
          '64 lần (2⁶)', ['4 lần (2²)', '16 lần (2⁴)', '8 lần (2³)'],
          'σ_s ∝ r⁶ nên (2r)⁶ / r⁶ = 64.', 2, 'Rayleigh', src='Đề cương 7.1 (số tính)')
    B.add('Tại sao bầu trời xanh còn mây trắng?',
          'Phân tử (x ≪ 1) tán xạ ∝ λ⁻⁴ nên xanh bị tán xạ nhiều hơn; giọt mây (x ≫ 1) có Q_ext ≈ 2 không phụ thuộc λ nên mọi màu như nhau → trắng', ['Bầu trời phản xạ màu đại dương; mây phản xạ băng', 'Phân tử hấp thụ ánh sáng đỏ còn giọt mây hấp thụ xanh', 'Mây phát xạ nhiệt trắng còn bầu trời phát xạ xanh'],
          'Đáp án gợi ý Q7(b).', 1, 'Rayleigh và Mie', origin='goc', src='Đề thi mẫu Q7(b)')
    B.add('Hàm pha Rayleigh có dạng nào?',
          'P(Θ) = ¾(1 + cos²Θ): đối xứng trước–sau, tán xạ 90° phân cực hoàn toàn', ['P(Θ) = 1/(4π): đẳng hướng', 'Đỉnh nhọn mạnh về phía trước, thùy sau yếu', 'P(Θ) = cos³Θ chỉ có thùy trước'],
          'Đề cương 7.1 và hình hàm pha trong chương 2. Hạt lớn thì đỉnh về phía trước mạnh.', 1, 'Rayleigh', origin='goc', src='Đề thi mẫu Q7(c)')
    B.add('Hàm pha của hạt lớn (Mie hoặc quang hình) khác Rayleigh thế nào?',
          'Có đỉnh rất mạnh về phía trước, thùy bên và sau yếu (g ≈ 0,6–0,8 với aerosol)', ['Đối xứng trước–sau như Rayleigh', 'Đẳng hướng ở mọi góc', 'Chỉ có tán xạ ngược'],
          'Đáp án gợi ý Q7(c).', 2, 'Mie', origin='goc', src='Đề thi mẫu Q7(c)')
    B.add('Hiệu suất suy giảm Q_ext = σ_ext / (πr²) tiến tới giá trị nào khi x rất lớn?',
          'Tiến tới 2 ("nghịch lý suy giảm")', ['Tiến tới 0', 'Tiến tới 1', 'Tiến tới vô hạn'],
          f'Một nửa do nhiễu xạ, một nửa do phản xạ/khúc xạ; độc lập bước sóng. Tính Mie cho giọt nước m = 1,33: Q_ext(x=200) = {MQ["200"]:.2f}, Q_ext(x=50) = {MQ["50"]:.2f}.', 2, 'Mie', src='Đề cương 7.2–7.3; Q_ext tính bằng Python')
    B.add(f'Với giọt nước (m = 1,33), Q_ext theo tính toán Mie đạt cực đại bao nhiêu quanh x ≈ 5?',
          f'≈ {MQ["5"]:.1f} (lớn hơn 2, rồi dao động và hội tụ về 2)', ['≈ 0,01 (rất nhỏ)', '≈ 2,0 đúng và không dao động', '≈ 10'],
          f'Python (Bohren–Huffman): Q_ext(0,5) = {MQ["0.5"]:.4f}; (1) = {MQ["1"]:.3f}; (2) = {MQ["2"]:.3f}; (5) = {MQ["5"]:.3f}; (10) = {MQ["10"]:.3f}; (50) = {MQ["50"]:.3f}. Dao động rồi tiến về 2.', 3, 'Mie', src='Số tính bằng Python (tự cài Lorenz–Mie)')
    B.add('Trong chế độ Rayleigh, Q_ext tăng theo x như thế nào?',
          f'Tăng theo x⁴ (ví dụ x từ 0,1 đến 0,5 làm Q_ext tăng ~600 lần)', ['Tăng tuyến tính theo x', 'Giảm theo x⁻¹', 'Không đổi theo x'],
          f'Đề cương hình 20: x⁴ ở Rayleigh. Tính Mie: Q_ext(0,1) = {MQ["0.1"]:.2e}; Q_ext(0,5) = {MQ["0.5"]:.2e}; tỉ số ≈ {MQ["0.5"]/MQ["0.1"]:.0f} (5⁴ = 625).', 3, 'Rayleigh', src='Đề cương hình 20; số tính bằng Python')
    B.add('Cầu vồng ở góc 42° và quầng ở 22° thuộc chế độ nào?',
          'Quang hình học (hạt rất lớn: giọt mưa; tinh thể băng lục giác)', ['Rayleigh', 'Raman', 'Mie phần dưới'],
          'Đề cương 7.3: giọt mưa → cầu vồng 42°; tinh thể băng lục giác → quầng 22°; đỉnh nhiễu xạ tới trước rất mạnh.', 2, 'Quang hình học', src='Đề cương 7.3')
    B.add('Với hạt không cầu như bụi, lý thuyết nào thay cho Lorenz–Mie?',
          'T-matrix hoặc phương pháp lưỡng cực rời rạc (discrete dipole)', ['Lý thuyết Rayleigh–Jeans', 'Định luật Beer–Lambert', 'Hàm Planck'],
          'Đề cương 7.2/7.4: Mie cho cầu đồng nhất; bụi, băng cần spheroid/T-matrix.', 3, 'Mie', src='Đề cương 7.2, 7.4')
    B.essay('(a) Tính tham số kích thước x của (i) phân tử N₂ (r ≈ 0,2 nm), (ii) hạt sulfate r = 0,2 µm, (iii) hạt bụi r = 5 µm, đều ở λ = 0,55 µm; cho biết chế độ tán xạ.\n(b) Vì sao bầu trời xanh còn mây trắng?\n(c) Phác hàm pha ở chế độ Rayleigh và với hạt lớn.',
            f'(a) x = 2πr/λ: (i) {SZ["N2"]:.4f} → Rayleigh; (ii) {SZ["sulfate"]:.2f} → Mie; (iii) {SZ["dust"]:.1f} → Mie phần trên/tiến gần quang hình học.\n(b) Phân tử: σ ∝ λ⁻⁴ nên xanh bị tán xạ mạnh hơn. Giọt mây x ≫ 1: Q_ext ≈ 2 không phụ thuộc λ → mọi màu như nhau → trắng.\n'
            '(c) Rayleigh: ¾(1 + cos²Θ) đối xứng trước–sau. Hạt lớn: đỉnh rất mạnh về phía trước, thùy bên/sau yếu.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q7 (2,5 điểm) + đáp án gợi ý')
    B.essay('Chế độ tán xạ của aerosol thô với ánh sáng khả kiến là gì? Hệ quả đối với AOD và hàm pha?',
            f'r ≈ 1–10 µm, λ = 0,55 µm → x ≈ {SZ["coarse_1"]:.0f}–{SZ["coarse_10"]:.0f}: phần trên của chế độ Mie, tiến gần quang hình học. Hệ quả: AOD gần như không phụ thuộc bước sóng (α ≈ 0–0,5), tán xạ tới trước mạnh, Q_ext ≈ 2. Bụi không cầu: Mie chỉ là xấp xỉ, dùng spheroid/T-matrix.', 2, 'Aerosol thô', origin='goc', src='Đề cương 7.4')
    sl = [
        cover('Các chế độ tán xạ của ánh sáng bởi hạt', 'Scattering regimes of light by particles — Đề cương chương 7',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Rayleigh · Mie · quang hình học · aerosol thô'),
        S('Tham số kích thước x = 2πr / λ', fm('x = 2π r / λ &nbsp;&nbsp; (r: bán kính hạt) &nbsp;&nbsp; + &nbsp; chiết suất phức m = n + ik', 32) +
          figfit('f5_regimes', 'Hình 19 (đề cương): các chế độ tán xạ theo tham số kích thước x (ánh sáng khả kiến, λ ≈ 0,5 µm).', 330)),
        S('Ba chế độ tán xạ', dtable(tbl(['Chế độ', 'x', 'Hạt', 'Đặc điểm'], [
            ['Rayleigh', '≪ 1 (< 0,1)', 'Phân tử, hạt rất mịn', 'σ ∝ r<sup>6</sup>/λ<sup>4</sup>; đối xứng'],
            ['Mie', '≈ 0,1–50', 'Aerosol, giọt mây', 'Phụ thuộc λ yếu; đỉnh tới trước'],
            ['Quang hình học', '≫ 1 (> 50–100)', 'Giọt mưa, tinh thể băng', 'Q<sub>ext</sub> → 2; không phụ thuộc λ']]), 'xl') + '<p class="note" style="margin-top:26px">Chế độ do <b>x = 2πr/λ</b> và chiết suất phức <b>m = n + ik</b> quyết định.</p>'),
        S('Rayleigh: phân tử và hạt rất mịn', fm('σ<sub>s</sub> = (8π/3) k<sup>4</sup> r<sup>6</sup> |(m² − 1)/(m² + 2)|² ∝ r<sup>6</sup> / λ<sup>4</sup>', 28) + fm('P(Θ) = ¾ (1 + cos²Θ)', 32) +
          ulb(['Gấp đôi bán kính → <b>64 lần</b> (2<sup>6</sup>)', 'Giảm một nửa λ → <b>16 lần</b> (2<sup>4</sup>)', 'Trời xanh, hoàng hôn đỏ'], 28, 10)),
        S('Mie: hạt cỡ bước sóng', cols(ulb(['Nghiệm Maxwell cho cầu (Lorenz–Mie)', 'Q<sub>ext</sub> dao động theo x rồi tiến về 2', 'Phụ thuộc λ yếu (Ångström α ≈ 0–2)', 'Đỉnh tới trước: g ≈ 0,6–0,8', 'Không cầu: T-matrix'], 27, 14),
          dtable(tbl(['x', 'Q<sub>ext</sub> (m = 1,33)'], [['0,1', f'{MQ["0.1"]:.1e}'], ['1', f'{MQ["1"]:.3f}'], ['5', f'{MQ["5"]:.2f}'], ['10', f'{MQ["10"]:.2f}'], ['50', f'{MQ["50"]:.2f}'], ['200', f'{MQ["200"]:.2f}']]), 'mid'), flex=[1.1, 1])),
        S('Hiệu suất suy giảm theo x', figfit('f10_mie_qext', 'Hình 20 (đề cương): Q_ext theo x (tính Lorenz–Mie): x⁴ (Rayleigh), cộng hưởng (Mie), giới hạn 2 (quang hình học).', 470) + '<p class="note">Bảng trước: Python tính độc lập bằng Lorenz–Mie, khớp hình.</p>'),
        S('Quang hình học: hạt rất lớn', cards(card('Giọt mưa', 'Cầu vồng ở góc 42°.'), card('Tinh thể băng lục giác', 'Quầng 22°.'), card('Q<sub>ext</sub> → 2', 'Một nửa nhiễu xạ, một nửa phản xạ/khúc xạ; màu trắng vì không phụ thuộc λ.'), cols=3)),
        S('Aerosol thô trong ánh sáng khả kiến', fm(f'λ = 0,55 µm: &nbsp; r = 1 µm → x ≈ {SZ["coarse_1"]:.0f} &nbsp;;&nbsp; r = 10 µm → x ≈ {SZ["coarse_10"]:.0f}', 30) +
          ulb(['Phần trên của Mie, tiến gần quang hình học', 'AOD gần như không phụ thuộc λ: α ≈ 0–0,5', 'Tán xạ tới trước mạnh; Q<sub>ext</sub> ≈ 2', 'Bụi không cầu: spheroid, T-matrix'], 29, 16)),
        S('Ba hạt trong đề thi mẫu', dtable(tbl(['Hạt', 'r', 'x ở 0,55 µm', 'Chế độ'], [
            ['Phân tử N₂', '0,2 nm', f'{SZ["N2"]:.4f}', 'Rayleigh'], ['Sulfate', '0,2 µm', f'{SZ["sulfate"]:.2f}', 'Mie'], ['Bụi', '5 µm', f'{SZ["dust"]:.1f}', 'Mie trên / quang hình']]), 'xl') + '<p class="note" style="margin-top:30px">x = 2πr/λ với λ = 0,55 µm. Aerosol thô mịn nhất (1 µm) đã có x ≈ 11.</p>'),
        S('Exam checklist — Chương 7', chk(['Tham số kích thước x = 2πr/λ (và chiết suất m)', 'Rayleigh x ≪ 1: λ<sup>−4</sup>, hàm pha đối xứng', 'Mie x ~ 1: tới trước, Q<sub>ext</sub> dao động → 2', 'Quang hình học x ≫ 1: không phụ thuộc λ', 'Aerosol thô trong khả kiến: x ~ 10–100, α ≈ 0'])),
        S('Ý chính', dul(['Chế độ do x = 2πr/λ quyết định', 'Rayleigh: λ<sup>−4</sup> → trời xanh', 'Mie: hạt mịn, đỉnh tới trước', 'Aerosol thô: x ≈ 10–100, α ≈ 0']))]
    mod = dict(id='m7', slug='07-scattering-regimes', title='M7 · Các chế độ tán xạ', en='Scattering regimes of light by particles',
               question='<ul><li>What are the different regimes of scattering of light by particles?</li><li>Explain each of them and under which conditions they are encountered.</li><li>What is the regime for coarse aerosols scattering visible light?</li></ul>',
               calcs=[('size', 'Tham số kích thước và chế độ tán xạ')],
               checklist=['Size parameter x = 2πr/λ (+ refractive index m).', 'Rayleigh x ≪ 1 (molecules), λ⁻⁴, symmetric P(Θ).', 'Mie x ~ 1 (fine aerosols), Lorenz–Mie theory, forward peak, Q_ext oscillates → 2.', 'Geometric optics x ≫ 1 (raindrops, ice), wavelength-independent.', 'Coarse aerosol in visible: x ~ 10–100 → Mie (large-particle limit, near geometric optics), α ≈ 0.'],
               summary=['Chế độ tán xạ phụ thuộc thông số kích thước x = 2πr/λ.', 'Rayleigh (x ≪ 1): phân tử khí, ∝ λ⁻⁴, trời xanh. Mie (x ≈ 1): aerosol mịn, tán xạ mạnh về phía trước. Quang hình (x ≫ 1): giọt mưa, tinh thể băng, không phụ thuộc bước sóng.', 'Aerosol thô (bụi, muối biển, r ≈ 1–10 µm) với ánh sáng khả kiến: x ≈ 10–100 → chế độ Mie (phần trên, tiến gần quang hình), số mũ Ångström ≈ 0.'],
               sections=[
        ('Hạt to hay nhỏ so với bước sóng?', '<p>Cách ánh sáng tán xạ phụ thuộc vào <b>kích thước hạt so với bước sóng</b>. Phân tử khí nhỏ hơn bước sóng rất nhiều; hạt aerosol cỡ bước sóng; giọt mưa lớn hơn bước sóng cả nghìn lần. Hai con số quyết định chế độ: tham số kích thước và chiết suất phức m = n + ik.</p>' +
         eq('Tham số kích thước', 'x = 2π r / λ') + lfig('f5_regimes', 'Hình 19 (đề cương): các chế độ tán xạ theo x với ánh sáng khả kiến (λ ≈ 0,5 µm).') +
         hx_table(['Chế độ', 'Điều kiện', 'Gặp ở', 'Đặc điểm'], [['Rayleigh', 'x ≪ 1 (thường < 0,1)', 'Phân tử N₂, O₂ (UV–IR); hạt rất mịn r < 0,03 µm trong khả kiến; giọt mây với vi sóng/radar', 'σ ∝ r⁶/λ⁴; P(Θ) = ¾(1 + cos²Θ)'],
                                                              ['Mie (cộng hưởng)', 'x ≈ 0,1–50', 'Aerosol mode tích tụ (0,1–1 µm) trong khả kiến; giọt mây trong IR; cả aerosol thô', 'Lorenz–Mie; Q_ext dao động rồi → 2; α ≈ 0–2; đỉnh tới trước (g ≈ 0,6–0,8)'],
                                                              ['Quang hình học', 'x ≫ 1 (thường > 50–100)', 'Giọt mưa, giọt mây lớn, tinh thể băng, bụi lớn trong khả kiến', 'Tia: phản xạ, khúc xạ, nhiễu xạ; Q_ext → 2; không phụ thuộc λ']], 'left')),
        ('Rayleigh: phân tử và hạt rất mịn', '<p>Hạt nhỏ hơn bước sóng rất nhiều hoạt động như một <b>lưỡng cực dao động</b> trong trường đều.</p>' + eq('Tiết diện và hàm pha', 'σ<sub>s</sub> = (8π/3) k⁴ r⁶ |(m² − 1)/(m² + 2)|² ∝ r⁶ / λ⁴ &nbsp;;&nbsp; P(Θ) = ¾ (1 + cos²Θ)') +
         '<ul><li>Phụ thuộc mạnh λ⁻⁴ → bầu trời xanh, hoàng hôn đỏ.</li><li>Tán xạ tới trước và ra sau đối xứng; ánh sáng tán xạ 90° phân cực hoàn toàn.</li></ul>' +
         '<div class="ex"><div class="exh">Ví dụ · số tính</div><ul><li>Gấp đôi bán kính (giữ λ): σ tăng 2⁶ = <b>64</b> lần.</li><li>Giảm một nửa bước sóng: σ tăng 2⁴ = <b>16</b> lần.</li><li>450 nm so với 650 nm: (650/450)⁴ = <b>4,35</b> lần.</li></ul></div>'),
        ('Mie và quang hình học', '<p><b>Mie</b> (x ≈ 0,1–50) là nghiệm chính xác phương trình Maxwell cho một cầu đồng nhất, dưới dạng chuỗi đa cực vô hạn. Hiệu suất suy giảm Q<sub>ext</sub> = σ<sub>ext</sub>/(πr²) dao động theo x và tiến về 2 khi x lớn (“nghịch lý suy giảm”). Phụ thuộc bước sóng yếu nên khói mù và mây có màu trắng/xám; đỉnh tới trước mạnh (g ≈ 0,6–0,8), cấu trúc góc phức tạp (glory, cầu vồng). Hạt không cầu (bụi, băng) cần T-matrix hoặc lưỡng cực rời rạc.</p>'
         f'<div class="ex"><div class="exh">Q<sub>ext</sub> tính bằng Python (Lorenz–Mie, giọt nước m = 1,33)</div>' + hx_table(['x', '0,1', '0,5', '1', '2', '5', '10', '50', '200'], [['Q<sub>ext</sub>'] + [f'{MQ[k]:.3g}' for k in ['0.1', '0.5', '1', '2', '5', '10', '50', '200']]]) +
         '<p style="margin:4px 0">Kiểm: ở x = 0,05 kết quả khớp công thức Rayleigh trong 2%; ở x = 200 giá trị ≈ 2,06 (≈ 2).</p></div>' + lfig('f10_mie_qext', 'Hình 20 (đề cương): Q_ext theo x — x⁴ (Rayleigh), cộng hưởng (Mie), giới hạn Q_ext → 2 (quang hình học).') +
         '<p><b>Quang hình học</b> (x ≫ 1): coi ánh sáng là tia (Snell, Fresnel) cộng nhiễu xạ. Q<sub>ext</sub> → 2 (một nửa nhiễu xạ, một nửa phản xạ/khúc xạ), độc lập bước sóng nên mây màu trắng; hiện tượng: cầu vồng 42°, quầng 22° quanh tinh thể băng lục giác; đỉnh nhiễu xạ tới trước rất mạnh.</p>'),
        ('Aerosol thô trong ánh sáng khả kiến', '<p>Bụi khoáng và muối biển có r ≈ 1–10 µm; ở λ ≈ 0,55 µm:</p>' + eq('Tham số kích thước', f'x = 2π × (1 đến 10 µm) / 0,55 µm ≈ <b>{SZ["coarse_1"]:.0f} đến {SZ["coarse_10"]:.0f}</b>') +
         '<p>→ phần <b>trên của chế độ Mie</b>, tiến gần quang hình học (Mie vẫn đúng; quang hình học là xấp xỉ tốt cho hạt lớn nhất). Hệ quả: AOD gần như không phụ thuộc bước sóng (<b>α ≈ 0–0,5</b>), tán xạ tới trước mạnh, Q<sub>ext</sub> ≈ 2. Bụi không cầu nên Mie cho cầu chỉ là xấp xỉ.</p>' +
         f'<div class="ex"><div class="exh">Ví dụ · đề thi mẫu Q7(a), số kiểm bằng Python</div>' + hx_table(['Hạt', 'r', 'x ở 0,55 µm', 'Chế độ'], [['Phân tử N₂', '0,2 nm', f'{SZ["N2"]:.4f}', 'Rayleigh'], ['Sulfate', '0,2 µm', f'{SZ["sulfate"]:.2f}', 'Mie'], ['Bụi', '5 µm', f'{SZ["dust"]:.1f}', 'Mie trên / gần quang hình']]) + '</div>' +
         callout('info', 'Trời xanh, mây trắng', 'Phân tử (Rayleigh, ∝ λ⁻⁴) tán xạ xanh nhiều hơn đỏ. Giọt mây (x ≫ 1) tán xạ mọi màu như nhau (Q<sub>ext</sub> ≈ 2) nên có màu trắng.'))])
    return mod, sl, B
