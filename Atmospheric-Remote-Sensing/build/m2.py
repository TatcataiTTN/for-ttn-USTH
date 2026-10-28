# -*- coding: utf-8 -*-
"""M2 — Tương tác ánh sáng và vật chất (đề cương Ch.2)."""
from lib import *
from lib import _PIL
from m1 import ul_
from qcore import Bank
V = VERIFIED

def build():
    B = Bank('m2', seed=2)
    be = V['beer']; w = V['wien']; st = V['stefan']
    B.add('Viết định luật Beer–Lambert cho một chùm sáng đi qua môi trường vừa hấp thụ vừa tán xạ.',
          'I = I₀ · e^(−τ), với τ = ∫ (k_a + k_s) ds là độ dày quang học dọc đường truyền',
          ['I = I₀ · (1 − τ), với τ là tổng số phân tử trên đường truyền', 'I = I₀ / τ², với τ là bước sóng chia cho kích thước hạt', 'I = I₀ + τ · B(T), với B là hàm Planck'],
          'dI = −k_e·I·ds với k_e = k_a + k_s = Σ σᵢ nᵢ nên I = I₀ exp(−τ). Độ truyền qua T = I/I₀ = e^(−τ).',
          1, 'Beer–Lambert', origin='goc', src='Đề thi mẫu Q2(a)')
    B.add('Độ truyền qua (transmittance) T của một lớp có độ dày quang học τ là bao nhiêu?',
          'T = e^(−τ)', ['T = 1 / τ', 'T = 1 − τ²', 'T = τ · e'],
          'T = I/I₀ = exp(−τ). Với τ = 1, T = 0,37; với τ = 3, T = 0,05.', 1, 'Beer–Lambert', origin='goc', src='Đề thi mẫu Q2(a)')
    B.add('Định luật Kirchhoff (trạng thái cân bằng nhiệt cục bộ, LTE) phát biểu điều gì?',
          'Tại mỗi bước sóng, độ phát xạ bằng độ hấp thụ: ε_λ = α_λ',
          ['Tổng hấp thụ và tán xạ bằng không tại mọi bước sóng', 'Độ phát xạ tỉ lệ nghịch với nhiệt độ của vật', 'Cường độ phát xạ bằng cường độ Mặt Trời tại đỉnh khí quyển'],
          'Một khí hấp thụ ở bước sóng nào thì cũng phát xạ B_λ(T) ở bước sóng đó. Vì vậy phổ hồng ngoại nhiệt mang thông tin về cả nồng độ lẫn nhiệt độ.',
          1, 'Phát xạ', origin='goc', src='Đề thi mẫu Q2(b)')
    B.add('Tại sao định luật Kirchhoff quan trọng đối với viễn thám hồng ngoại nhiệt?',
          'Vì khí hấp thụ ở một vạch phổ cũng phát xạ ở vạch đó, nên phổ mã hóa cả nồng độ khí lẫn nhiệt độ lớp phát xạ',
          ['Vì nó chứng minh khí quyển không phát xạ ở hồng ngoại nên chỉ đo được phản xạ', 'Vì nó cho phép bỏ qua tán xạ trong mọi trường hợp', 'Vì nó cho biết nhiệt độ bề mặt luôn bằng nhiệt độ tầng bình lưu'],
          'Đáp án gợi ý Q2(b): ε_λ = α_λ nên thông tin về T(z) và n(z) cùng nằm trong phổ TIR.', 2, 'Phát xạ', origin='goc', src='Đề thi mẫu Q2(b)')
    B.add('Một chùm đi qua lớp có độ dày quang học thẳng đứng τ = 0,5 ở góc thiên đỉnh Mặt Trời 60°. Phần chùm trực tiếp còn lại là bao nhiêu?',
          f'≈ {be["T"]*100:.0f}% (τ nghiêng = 1,0)', ['≈ 61% (dùng τ = 0,5 không hiệu chỉnh góc)', '≈ 22% (nhân thay vì chia cho cos 60°)', '≈ 50% (nhầm với τ nghiêng bằng một nửa)'],
          f'τ_nghiêng = τ_đứng / cos θ = 0,5 / 0,5 = 1,0 nên T = e^(−1) = {be["T"]:.4f}. Đã tính lại bằng Python.', 1, 'Beer–Lambert', origin='goc', src='Đề thi mẫu Q2(c)')
    B.add('Ba cơ chế làm thay đổi cường độ bức xạ đến cảm biến là gì?',
          'Hấp thụ, tán xạ và phát xạ (kèm phản xạ bề mặt)', ['Nhiễu xạ, giao thoa và phân cực', 'Quang phân, lắng đọng và vận chuyển', 'Nadir, limb và che khuất'],
          'Đề cương Ch.2: hấp thụ + tán xạ = suy giảm (extinction); phát xạ và tán xạ vào hướng nhìn là phần cộng thêm.', 1, 'Ba cơ chế', origin='goc', src='Đề cương Ch.2 (checklist)')
    B.add('Chuyển mức điện tử gây hấp thụ ở vùng phổ nào, và ví dụ khí nào?',
          'Tử ngoại – khả kiến; ví dụ O₃ (Hartley–Huggins 250–350 nm), NO₂ (400–450 nm), SO₂ (300–320 nm)',
          ['Hồng ngoại; ví dụ CO₂ ở 15 µm và O₃ ở 9,6 µm', 'Vi sóng; ví dụ O₂ ở 60 GHz và ClO', 'Tia X; ví dụ N₂ và Ar'],
          'Điện tử → UV/khả kiến. Dao động–quay → hồng ngoại (CO₂ 15 và 4,3 µm; O₃ 9,6 µm; CH₄ 7,7 và 2,3 µm; CO 4,6 và 2,3 µm). Quay thuần → vi sóng/hồng ngoại xa.',
          1, 'Hấp thụ', src='Đề cương 2.1')
    B.add('Dạng vạch phổ trong khí quyển thấp bị chi phối bởi cơ chế mở rộng nào?',
          'Mở rộng Lorentz do áp suất', ['Mở rộng Doppler do nhiệt độ', 'Mở rộng Zeeman do từ trường', 'Mở rộng Stark do điện trường lệch'],
          'Đề cương 2.1: Lorentz (áp suất) chiếm ưu thế ở khí quyển thấp; Doppler (nhiệt độ) chiếm ưu thế ở độ cao lớn.', 2, 'Hấp thụ', src='Đề cương 2.1')
    B.add('Tán xạ Rayleigh có sự phụ thuộc bước sóng và hàm pha như thế nào?',
          'σ_R ∝ λ⁻⁴, hàm pha P(Θ) = ¾(1 + cos²Θ) đối xứng trước–sau', ['σ_R ∝ λ⁻¹, hàm pha có đỉnh nhọn về phía trước', 'σ_R không phụ thuộc λ, hàm pha đẳng hướng', 'σ_R ∝ λ⁴, hàm pha chỉ có đỉnh phía sau'],
          'Đề cương 2.2: phân tử (x ≪ 1) tán xạ ∝ λ⁻⁴ nên trời xanh, hoàng hôn đỏ; tán xạ trước–sau đối xứng.', 1, 'Tán xạ', src='Đề cương 2.2')
    B.add(f'Tán xạ Rayleigh ở 450 nm mạnh gấp bao nhiêu lần ở 650 nm?',
          f'≈ {V["rayleigh_450_650"]:.1f} lần ((650/450)⁴)', ['≈ 1,4 lần ((650/450)¹)', '≈ 2,1 lần ((650/450)²)', '≈ 0,23 lần (tán xạ ở 450 nm yếu hơn)'],
          f'σ ∝ λ⁻⁴ nên tỉ số = (650/450)⁴ = {V["rayleigh_450_650"]:.3f}. Giải thích vì sao ánh sáng xanh bị tán xạ nhiều hơn ánh sáng đỏ.', 2, 'Tán xạ', src='Đề cương 2.2 (số tính bằng Python)')
    B.add('Tán xạ Raman quay bởi N₂ và O₂ gây ra hiệu ứng nào quan trọng với truy hồi DOAS tử ngoại–khả kiến?',
          'Hiệu ứng Ring: làm đầy các vạch Fraunhofer', ['Hiệu ứng nhà kính: giữ nhiệt trong tầng đối lưu', 'Hiệu ứng Doppler: dịch bước sóng vạch', 'Hiệu ứng Faraday: quay mặt phẳng phân cực'],
          'Raman là tán xạ không đàn hồi (đổi bước sóng) nên điền đầy các vạch hấp thụ Fraunhofer của Mặt Trời. Đề cương 2.2.', 3, 'Tán xạ', src='Đề cương 2.2')
    B.add('Albedo tán xạ đơn ω₀ được định nghĩa thế nào, và ω₀ = 1 có nghĩa là gì?',
          'ω₀ = σ_s / (σ_s + σ_a); ω₀ = 1 nghĩa là hạt chỉ tán xạ, không hấp thụ', ['ω₀ = σ_a / (σ_s + σ_a); ω₀ = 1 nghĩa là hạt chỉ hấp thụ', 'ω₀ = σ_s · σ_a; ω₀ = 1 nghĩa là hạt có kích thước bằng bước sóng', 'ω₀ = τ_a / τ_s; ω₀ = 1 nghĩa là không có aerosol'],
          'Đề cương 2.2: ω₀ ≈ 1 với hạt không hấp thụ; khoảng 0,85 với khói (smoke), tức hấp thụ khoảng 15% tổng suy giảm.', 2, 'Tán xạ', src='Đề cương 2.2')
    B.add('Định luật dịch chuyển Wien cho bước sóng cực đại bức xạ của Mặt Trời (≈ 5778 K) khoảng bao nhiêu?',
          f'≈ {w["sun"]["lam_max_um"]:.2f} µm (khả kiến)', ['≈ 10 µm (hồng ngoại nhiệt)', '≈ 0,05 µm (cực tím xa)', '≈ 5 µm (hồng ngoại trung)'],
          f'λ_max = 2898 µm·K / T = 2898/5778 = {w["sun"]["lam_max_um"]:.3f} µm. Python cũng tìm cực đại số của hàm Planck cho {w["sun"]["lam_max_numeric_um"]:.3f} µm.', 1, 'Phát xạ', src='Đề cương 2.3')
    B.add('Với Trái Đất ở khoảng 288 K, bước sóng cực đại phát xạ nằm ở đâu?',
          f'≈ {w["earth"]["lam_max_um"]:.1f} µm (hồng ngoại nhiệt)', ['≈ 0,5 µm (xanh lục)', '≈ 1,0 µm (cận hồng ngoại)', '≈ 100 µm (vi sóng)'],
          f'2898/288 = {w["earth"]["lam_max_um"]:.2f} µm. Đây là lý do cửa sổ khí quyển 8–12 µm quan trọng với viễn thám nhiệt.', 1, 'Phát xạ', src='Đề cương 2.3')
    B.add('Phát xạ nhiệt chiếm ưu thế còn phản xạ ánh sáng Mặt Trời chiếm ưu thế ở những vùng phổ nào?',
          'Phát xạ nhiệt khi λ > khoảng 4 µm; phản xạ Mặt Trời ở UV–khả kiến–cận hồng ngoại', ['Phát xạ nhiệt ở UV; phản xạ Mặt Trời ở hồng ngoại xa', 'Cả hai ngang nhau ở mọi bước sóng', 'Phát xạ nhiệt chỉ ban ngày; phản xạ chỉ ban đêm'],
          'Đề cương 2.3, hình 6: hai đường Planck của Mặt Trời và Trái Đất cắt nhau quanh 4 µm.', 2, 'Phát xạ', src='Đề cương 2.3, hình 6')
    B.add(f'Theo định luật Stefan–Boltzmann M = σT⁴, công suất phát xạ của vật đen 288 K khoảng bao nhiêu?',
          f'≈ {st["M_earth"]:.0f} W m⁻²', ['≈ 240 W m⁻²', '≈ 1 361 W m⁻²', '≈ 5,67 W m⁻²'],
          f'M = 5,67×10⁻⁸ × 288⁴ = {st["M_earth"]:.1f} W m⁻². Đã tính bằng Python.', 2, 'Phát xạ', src='Đề cương 2.3 (công thức); số tính bằng Python')
    B.add('Trong phương trình truyền bức xạ, số hạng k_a·B_λ(T) mô tả điều gì?',
          'Phát xạ nhiệt của môi trường thêm vào chùm tia', ['Mất năng lượng do tán xạ ra khỏi chùm', 'Tán xạ từ mọi hướng khác vào đường ngắm', 'Phản xạ của bề mặt Lambert'],
          'RTE: dI/ds = −k_e I + k_a B + (k_s/4π)∫P I dΩ′. Số hạng 1 = suy giảm; số hạng 2 = phát xạ; số hạng 3 = tán xạ vào đường ngắm.', 2, 'RTE', src='Đề cương 2.5')
    B.add('Phương trình Schwarzschild áp dụng cho trường hợp nào?',
          'Hồng ngoại nhiệt không tán xạ: bức xạ ở đỉnh khí quyển là phát xạ bề mặt bị suy giảm cộng phát xạ từng lớp có trọng số truyền qua',
          ['Tử ngoại có tán xạ nhiều lần mạnh', 'Viễn thám bằng laser chủ động (lidar)', 'Che khuất Mặt Trời qua rìa khí quyển'],
          'I(TOA) = ε_s B(T_s) T(0,∞) + ∫ B(T(z)) ∂T(z,∞)/∂z dz. Đề cương 2.5.', 3, 'RTE', src='Đề cương 2.5')
    B.add('Với bề mặt Lambert, bức xạ phản xạ được tính bằng công thức nào?',
          'I = A·F₀·cos θ₀ / π', ['I = A·F₀·cos θ₀ · π', 'I = F₀ / (A·cos θ₀)', 'I = A · B(T)'],
          'A là albedo bề mặt, F₀ là thông lượng Mặt Trời, θ₀ góc thiên đỉnh Mặt Trời. Lambert: phản xạ đẳng hướng.', 3, 'RTE', src='Đề cương 2.5')
    B.essay('(a) Viết định luật Beer–Lambert và định nghĩa độ dày quang học, độ truyền qua.\n(b) Giải thích định luật Kirchhoff và vì sao nó quan trọng cho viễn thám hồng ngoại nhiệt.\n(c) Một chùm đi qua lớp τ = 0,5 ở góc thiên đỉnh 60°: bao nhiêu phần trăm chùm trực tiếp truyền qua?',
            '(a) dI = −k_e I ds, I = I₀ e^(−τ), τ = ∫(k_a + k_s) ds = ∫Σσᵢnᵢ ds; T = I/I₀ = e^(−τ).\n(b) Trong LTE, ε_λ = α_λ: khí hấp thụ ở λ thì phát xạ B_λ(T) ở λ → phổ TIR mang thông tin về cả nồng độ và nhiệt độ.\n'
            f'(c) τ nghiêng = 0,5 / cos 60° = 1,0 → T = e^(−1) = {be["T"]:.3f} ≈ 37%.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q2 (2,5 điểm) + đáp án gợi ý')
    B.essay('Mô tả ba cơ chế tương tác ánh sáng – vật chất và các phương trình chính của từng cơ chế.',
            'Hấp thụ: E = hν = E₂ − E₁; k_a = σ_a(λ)·n; dấu vân tay phổ (điện tử UV-vis, dao động–quay IR, quay thuần vi sóng). Tán xạ: đổi hướng không đổi λ; hàm pha P(Θ); Rayleigh (x ≪ 1, ∝ λ⁻⁴), Mie (x ~ 1), Raman (Ring); ω₀ = σ_s/(σ_s + σ_a). '
            'Phát xạ: B_λ(T) = (2hc²/λ⁵)/(exp(hc/λk_BT) − 1); Kirchhoff ε = α; Wien λ_max T = 2898 µm·K; Stefan–Boltzmann M = σT⁴. Gộp lại: Beer–Lambert và RTE.', 2, 'Ba cơ chế', origin='goc', src='Đề cương Ch.2 (Question)')
    B.essay('Viết phương trình truyền bức xạ đầy đủ và nhận diện từng số hạng; nêu hai trường hợp rút gọn dùng trong viễn thám.',
            'dI/ds = −k_e I + k_a B_λ(T) + (k_s/4π)∫P(Θ) I(Ω′) dΩ′: suy giảm (mất), phát xạ nhiệt (được), tán xạ từ hướng khác vào đường ngắm (được). '
            'Rút gọn: (1) hồng ngoại nhiệt không tán xạ → phương trình Schwarzschild; (2) UV–khả kiến Mặt Trời → DOAS: ln(I₀/I) = Σσᵢ·SCDᵢ + đa thức trơn; bề mặt Lambert: I = A F₀ cos θ₀/π.', 3, 'RTE', origin='goc', src='Đề cương 2.5')
    # -------- slides --------
    sl = [
        cover('Tương tác ánh sáng và vật chất', 'Interaction between light and matter — Đề cương chương 2',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Hấp thụ · tán xạ · phát xạ · Beer–Lambert · phương trình truyền bức xạ'),
        S('Ba cơ chế thay đổi cường độ bức xạ', cards(
            card('Hấp thụ', 'Photon bị nuốt khi E = hν = E₂ − E₁.<br>Mỗi khí có <b>dấu vân tay</b> σ(λ).'),
            card('Tán xạ', 'Đổi hướng, không đổi bước sóng.<br>Rayleigh (phân tử), Mie (hạt).'),
            card('Phát xạ', 'Vật ở nhiệt độ T phát xạ ε·B<sub>λ</sub>(T).<br>Trội ở λ &gt; ~4 µm.'), cols=3) +
          '<p class="note" style="margin-top:14px"><b>Hấp thụ + tán xạ = suy giảm (extinction)</b>; phát xạ và tán xạ vào đường ngắm làm tăng.</p>'),
        S('Hấp thụ: ba loại chuyển mức', dtable(tbl(['Chuyển mức', 'Vùng phổ', 'Ví dụ'], [
            ['Điện tử', 'UV – khả kiến', 'O₃ Hartley–Huggins 250–350 nm; NO₂ 400–450 nm; SO₂ 300–320 nm'],
            ['Dao động – quay', 'Hồng ngoại', 'CO₂ 15 và 4,3 µm; O₃ 9,6 µm; CH₄ 7,7 và 2,3 µm; CO 4,6 µm'],
            ['Quay thuần', 'Vi sóng / hồng ngoại xa', 'H₂O, O₂ 60 GHz, ClO']]), 'xl') +
          '<p class="note" style="margin-top:20px">k<sub>a</sub>(λ) = σ<sub>a</sub>(λ)·n. Vạch rộng do <b>áp suất</b> (Lorentz, khí quyển thấp) và do <b>nhiệt độ</b> (Doppler, trên cao).</p>'),
        S('Tán xạ: Rayleigh, Mie và Raman', cols(
            ulb(['<b>Rayleigh</b> (phân tử, x ≪ 1): σ ∝ λ<sup>−4</sup> → trời xanh', '<b>Mie</b> (aerosol, x ~ 1): phụ thuộc λ yếu, đỉnh tới trước', '<b>Raman</b>: tán xạ không đàn hồi → hiệu ứng Ring'], 33, 42),
            fm('<span class="l">Hàm pha Rayleigh</span>P(Θ) = ¾ (1 + cos²Θ)', 32) + fm('<span class="l">Albedo tán xạ đơn</span>ω₀ = σ<sub>s</sub> / (σ<sub>s</sub> + σ<sub>a</sub>)', 32) +
            '<p class="note" style="font-size:28px">ω₀ = 1: không hấp thụ; ω₀ ≈ 0,85: khói (hấp thụ ~15%).</p>', flex=[1.15, 1])),
        S('Hàm pha tính bằng lý thuyết Mie', figfit('f11_phase', 'Hình 5 (đề cương): hàm pha tính từ lý thuyết Mie — đối xứng với phân tử, đỉnh tới trước với hạt lớn.', 440) +
          '<p class="note">Hạt càng lớn, tán xạ càng dồn về phía trước (tham số bất đối xứng g ≈ 0,6–0,8 với aerosol).</p>'),
        S('Phát xạ: Planck, Wien, Kirchhoff', figfit('f8_planck', 'Hình 6 (đề cương): đường Planck của Mặt Trời (khoảng 5778 K) và Trái Đất (khoảng 288 K).', 420) +
          fm(f'λ<sub>max</sub>T = 2898 µm·K → Mặt Trời ≈ {w["sun"]["lam_max_um"]:.2f} µm; Trái Đất ≈ {w["earth"]["lam_max_um"]:.1f} µm', 28)),
        S('Beer–Lambert: suy giảm hàm mũ', fm('<span class="l">Định luật suy giảm</span>dI<sub>λ</sub> = −k<sub>e</sub> I<sub>λ</sub> ds &nbsp;,&nbsp; k<sub>e</sub> = k<sub>a</sub> + k<sub>s</sub> = Σ σ<sub>i</sub> n<sub>i</sub>', 30) +
          fm('I<sub>λ</sub>(s) = I<sub>λ</sub>(0) · e<sup>−τ</sup> &nbsp;,&nbsp; τ = ∫ k<sub>e</sub> ds &nbsp;,&nbsp; T = e<sup>−τ</sup>', 32) +
          legend([('τ', 'độ dày quang học'), ('T', 'độ truyền qua'), ('τ<sub>nghiêng</sub>', 'τ<sub>đứng</sub> / cos θ'), ('Ví dụ', f'τ = 0,5, θ = 60° → τ<sub>nghiêng</sub> = 1 → T = {be["T"]:.2f}')], 2)),
        S('Ba cơ chế trên một hình', figfit('f2_interactions', 'Hình 4 (đề cương): hấp thụ, tán xạ, phát xạ và đường suy giảm Beer–Lambert.', 420) +
          ulb(['Hấp thụ và tán xạ lấy năng lượng khỏi chùm', 'Phát xạ và tán xạ từ hướng khác cộng thêm vào chùm'], 30, 14)),
        S('Phương trình truyền bức xạ (RTE)', fm('dI<sub>λ</sub>/ds = −k<sub>e</sub> I<sub>λ</sub> + k<sub>a</sub> B<sub>λ</sub>(T) + (k<sub>s</sub>/4π) ∫ P(Θ) I<sub>λ</sub>(Ω′) dΩ′', 28) +
          cards2(330, card('Số hạng 1: suy giảm', 'Mất năng lượng do hấp thụ và tán xạ ra ngoài chùm'), card('Số hạng 2: phát xạ', 'Môi trường phát xạ nhiệt theo hàm Planck'),
                card('Số hạng 3: tán xạ vào', 'Ánh sáng từ mọi hướng khác tán xạ vào đường ngắm'), cols=3)),
        S('Các trường hợp rút gọn trong viễn thám', cols(
            fm('<span class="l">Hồng ngoại nhiệt (Schwarzschild)</span>I(TOA) = ε<sub>s</sub> B(T<sub>s</sub>) T(0,∞) + ∫ B(T(z)) ∂T(z,∞)/∂z dz', 27) +
            '<p style="font-size:33px">Phát xạ bề mặt bị suy giảm cộng phát xạ từng lớp, có trọng số truyền qua đến vũ trụ.</p>',
            fm('<span class="l">UV – khả kiến Mặt Trời (DOAS)</span>ln(I<sub>0</sub>/I) = Σ σ<sub>i</sub>′ SCD<sub>i</sub> + đa thức', 27) +
            '<p style="font-size:33px">Bề mặt Lambert: I = A F<sub>0</sub> cos θ<sub>0</sub> / π.</p>') + callout('info', 'Nhớ', 'DOAS cho UV–khả kiến (Mặt Trời tán xạ ngược); Schwarzschild cho hồng ngoại nhiệt không tán xạ.')),
        S('Exam checklist — Chương 2', chk([
            'Ba cơ chế: hấp thụ (σ(λ)), tán xạ (Rayleigh/Mie, P(Θ), ω₀), phát xạ (Planck, Kirchhoff)',
            'Beer–Lambert: I = I₀ e<sup>−τ</sup>, τ = ∫ k<sub>e</sub> ds, k<sub>e</sub> = k<sub>a</sub> + k<sub>s</sub>',
            'Viết đầy đủ RTE và nhận diện từng số hạng; Schwarzschild cho TIR',
            'Vẽ: tấm hấp thụ, hạt tán xạ với mũi tên mọi hướng, lớp phát xạ, đường mũ'])),
        S('Ý chính', dul(['Hấp thụ + tán xạ = suy giảm theo Beer–Lambert I = I₀e<sup>−τ</sup>', 'Phát xạ tuân theo Planck; Kirchhoff ε = α', 'RTE: suy giảm − phát xạ + tán xạ vào đường ngắm', 'Rayleigh ∝ λ<sup>−4</sup> nên trời xanh']))]
    mod = dict(id='m2', slug='02-light-matter', title='M2 · Tương tác ánh sáng – vật chất', en='Interaction between light and matter',
               question='<ul><li>Describe the main physical mechanisms of interaction between light and matter that modify the intensity of radiation reaching a radiometric sensor.</li><li>Provide a clear description, the main equations, and schematics of each of these mechanisms.</li></ul>',
               calcs=[('beer', 'Beer–Lambert và góc thiên đỉnh'), ('planck', 'Planck, Wien và nhiệt độ sáng')],
               checklist=['Three mechanisms: absorption (quantised transitions, σ(λ) fingerprint), scattering (Rayleigh/Mie, phase function, ω₀), emission (Planck, Kirchhoff).',
                          'Beer–Lambert: I = I₀ e^−τ, τ = ∫ k_e ds, k_e = k_a + k_s.', 'Write the full RTE and identify each term; Schwarzschild for thermal IR.',
                          'Draw: absorbing slab, scattering particle with arrows in all directions, emitting layer, exponential decay curve.'],
               summary=['Ba cơ chế: hấp thụ (chuyển mức năng lượng điện tử, dao động, quay → mỗi khí có dấu vân tay phổ), tán xạ (đổi hướng photon: Rayleigh ∝ λ⁻⁴, Mie), phát xạ nhiệt (Planck, Kirchhoff ε = α).',
                        'Hấp thụ + tán xạ = suy giảm (extinction), tuân theo định luật Beer–Lambert I = I₀·e^(−τ).', 'Phương trình truyền bức xạ: suy giảm − phát xạ + tán xạ vào hướng nhìn.'],
               sections=[
        ('Ba cơ chế, nói nôm na', '<p>Ánh sáng đi từ nguồn (Mặt Trời hoặc mặt đất) tới cảm biến chịu <b>ba tác động</b>. <b>Hấp thụ</b> như tấm kính màu nuốt bớt ánh sáng. <b>Tán xạ</b> như sương mù làm tia sáng bẻ sang hướng khác. <b>Phát xạ</b> như chính khí quyển ấm và tự phát ánh sáng hồng ngoại.</p>'
         '<p>Hấp thụ và tán xạ cùng <b>lấy</b> năng lượng khỏi chùm (gộp thành <i>suy giảm / extinction</i>); phát xạ và tán xạ từ hướng khác <b>thêm</b> năng lượng vào chùm. Phản xạ bề mặt cũng quan trọng với bức xạ nhìn từ vũ trụ.</p>' +
         lfig('f2_interactions', 'Hình 4 (đề cương): ba cơ chế và định luật Beer–Lambert.') +
         model_en('<p>Radiation travelling from the source to the sensor is modified by three processes: absorption and scattering (together forming extinction) remove energy from the beam, while emission and scattering into the beam add energy. Surface reflection also matters for the radiance seen from space.</p>')),
        ('Hấp thụ (absorption)', '<p>Một phân tử hấp thụ photon khi năng lượng khớp một bước chuyển: <b>E = hν = E₂ − E₁</b>. Mỗi khí có phổ hấp thụ riêng σ(λ) — chính là “dấu vân tay” để nhận ra khí.</p>' +
         hx_table(['Loại chuyển mức', 'Vùng phổ', 'Ví dụ'], [['Điện tử', 'UV – khả kiến', 'O₃ Hartley–Huggins 250–350 nm; NO₂ 400–450 nm; SO₂ 300–320 nm'],
                                                       ['Dao động – quay', 'Hồng ngoại', 'CO₂ 15 µm và 4,3 µm; O₃ 9,6 µm; CH₄ 7,7 và 2,3 µm; CO 4,6 và 2,3 µm; H₂O'],
                                                       ['Quay thuần', 'Vi sóng / hồng ngoại xa', 'H₂O, O₂ 60 GHz, ClO']], 'left') +
         eq('Hệ số hấp thụ', 'k<sub>a</sub>(λ) = σ<sub>a</sub>(λ) · n &nbsp; (n: mật độ số, molecule cm⁻³)') +
         '<p>Dạng vạch phụ thuộc <b>áp suất</b> (mở rộng Lorentz, trội ở khí quyển thấp) và <b>nhiệt độ</b> (mở rộng Doppler, trội ở độ cao lớn).</p>'),
        ('Tán xạ (scattering)', '<p>Photon bị đổi hướng nhưng <b>giữ nguyên bước sóng</b> (đàn hồi). Phân bố góc mô tả bởi hàm pha P(Θ). Chế độ phụ thuộc tham số kích thước x = 2πr/λ (xem module 7).</p>' +
         hx_table(['Loại', 'Hạt', 'Đặc điểm'], [['Rayleigh (x ≪ 1)', 'Phân tử N₂, O₂', 'σ ∝ λ⁻⁴; P(Θ) = ¾(1 + cos²Θ) đối xứng; trời xanh'],
                                               ['Mie (x ~ 1)', 'Aerosol, giọt mây', 'Phụ thuộc λ yếu (τ ∝ λ^−α); đỉnh mạnh về phía trước'],
                                               ['Raman (không đàn hồi)', 'N₂, O₂ (quay)', 'Đổi bước sóng; gây hiệu ứng Ring (làm đầy vạch Fraunhofer) trong DOAS']], 'left') +
         eq('Albedo tán xạ đơn', 'ω<sub>0</sub> = σ<sub>s</sub> / (σ<sub>s</sub> + σ<sub>a</sub>) &nbsp; (= 1 với hạt không hấp thụ; ≈ 0,85 với khói)') +
         f'<div class="ex"><div class="exh">Ví dụ · Rayleigh</div><p>Tỉ số tán xạ ở 450 nm so với 650 nm = (650/450)⁴ = <b>{V["rayleigh_450_650"]:.2f}</b> lần, vì thế ánh sáng xanh bị tán xạ nhiều hơn đỏ.</p></div>' +
         lfig('f11_phase', 'Hình 5 (đề cương): hàm pha tính bằng lý thuyết Mie.')),
        ('Phát xạ (emission)', '<p>Mọi vật có T &gt; 0 K đều phát xạ. Vật đen phát xạ theo hàm Planck; môi trường thật phát xạ ε·B. Ở LTE, <b>định luật Kirchhoff</b>: ε<sub>λ</sub> = α<sub>λ</sub> — khí hấp thụ ở bước sóng nào thì cũng phát xạ ở bước sóng đó.</p>' +
         eq('Planck', 'B<sub>λ</sub>(T) = (2hc² / λ⁵) · 1 / (exp(hc / λk<sub>B</sub>T) − 1)') + eq('Wien và Stefan–Boltzmann', 'λ<sub>max</sub> · T = 2898 µm·K &nbsp;;&nbsp; M = σ<sub>SB</sub> T⁴') +
         f'<div class="ex"><div class="exh">Ví dụ · số đã kiểm bằng Python</div><ul><li>Mặt Trời (5778 K): λ<sub>max</sub> = {w["sun"]["lam_max_um"]:.2f} µm (khả kiến).</li><li>Trái Đất (288 K): λ<sub>max</sub> = {w["earth"]["lam_max_um"]:.1f} µm (hồng ngoại nhiệt); M = {st["M_earth"]:.0f} W m⁻².</li></ul></div>'
         '<p>Phát xạ trội ở λ &gt; ~4 µm (hồng ngoại nhiệt, vi sóng), còn phản xạ ánh sáng Mặt Trời trội ở UV – khả kiến – cận hồng ngoại.</p>' + lfig('f8_planck', 'Hình 6 (đề cương): đường Planck của Mặt Trời và Trái Đất.')),
        ('Beer–Lambert và độ dày quang học', eq('Suy giảm', 'dI<sub>λ</sub> = −k<sub>e</sub>(λ) I<sub>λ</sub> ds &nbsp;;&nbsp; k<sub>e</sub> = k<sub>a</sub> + k<sub>s</sub> = Σ σ<sub>i</sub> n<sub>i</sub>') +
         eq('Nghiệm', 'I<sub>λ</sub>(s) = I<sub>λ</sub>(0) · e<sup>−τ<sub>λ</sub></sup> &nbsp;;&nbsp; τ<sub>λ</sub> = ∫ k<sub>e</sub>(λ,s) ds &nbsp;;&nbsp; T = e<sup>−τ</sup>') +
         '<p>Đường nghiêng: τ<sub>nghiêng</sub> = τ<sub>đứng</sub> / cos θ (mặt phẳng song song).</p>' +
         f'<div class="ex"><div class="exh">Ví dụ 1 · đề thi mẫu Q2(c)</div><ol class="steps"><li>τ<sub>đứng</sub> = 0,5; θ = 60°; cos 60° = 0,5</li><li>τ<sub>nghiêng</sub> = 0,5 / 0,5 = 1,0</li><li>T = e<sup>−1</sup> = <b>{be["T"]:.4f}</b> ≈ 37%</li></ol></div>' +
         lfig('s4_solar', 'Hình 7 (đề cương, ảnh slide bài giảng): bức xạ Mặt Trời ở đỉnh khí quyển so với mực nước biển — phần thiếu là hấp thụ (O₃, O₂, H₂O, CO₂) và tán xạ.', ext='jpg', folder='slides', w=640)),
        ('Phương trình truyền bức xạ (RTE)', eq('RTE', 'dI<sub>λ</sub>/ds = −k<sub>e</sub> I<sub>λ</sub> + k<sub>a</sub> B<sub>λ</sub>(T) + (k<sub>s</sub>/4π) ∫ P(Θ) I<sub>λ</sub>(Ω′) dΩ′') +
         '<ul><li><b>Số hạng 1</b> = suy giảm (mất).</li><li><b>Số hạng 2</b> = phát xạ nhiệt (được).</li><li><b>Số hạng 3</b> = ánh sáng từ các hướng khác tán xạ vào đường ngắm (được).</li></ul>'
         '<h3>Hai trường hợp rút gọn thường dùng</h3>' + eq('Hồng ngoại nhiệt không tán xạ (Schwarzschild)', 'I<sub>λ</sub>(TOA) = ε<sub>s</sub> B<sub>λ</sub>(T<sub>s</sub>) T<sub>λ</sub>(0,∞) + ∫ B<sub>λ</sub>(T(z)) ∂T<sub>λ</sub>(z,∞)/∂z dz') +
         eq('UV – khả kiến (DOAS)', 'ln(I<sub>0</sub>/I) = Σ σ<sub>i</sub>′ · SCD<sub>i</sub> + đa thức trơn') + '<p>Bề mặt Lambert: I = A·F<sub>0</sub>·cos θ<sub>0</sub> / π (A: albedo).</p>')])
    return mod, sl, B
