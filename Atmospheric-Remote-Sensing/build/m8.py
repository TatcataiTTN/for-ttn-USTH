# -*- coding: utf-8 -*-
"""M8 — Xác định độ cao aerosol bằng cảm biến thụ động (đề cương Ch.8)."""
from lib import *
from qcore import Bank
V = VERIFIED
T = V['tir']; D = V['tir_degenerate']; OX = V['oxygen_above']

def build():
    B = Bank('m8', seed=8)
    d1, d5 = T['z1']['dBT'], T['z5']['dBT']
    B.add('Nguyên lý xác định độ cao aerosol bằng hồng ngoại nhiệt (TIR) là gì?',
          'Lớp aerosol phát xạ ở nhiệt độ của chính nó; nhiệt độ giảm theo độ cao nên lớp càng cao càng lạnh và nhiệt độ sáng đo được càng thấp', ['Lớp aerosol càng cao thì hấp thụ O₂ càng mạnh', 'Độ trễ của xung laser tỉ lệ với độ cao', 'Độ khử cực tăng theo độ cao của lớp'],
          'Đề cương 8.1: I ≈ B(T_s)·e^(−τ_aer) + B(T_layer)·(1 − e^(−τ_aer)); gradient nhiệt ≈ −6,5 K/km.', 1, 'TIR', origin='goc', src='Đề cương Ch.8 (checklist)')
    B.add('Viết biểu thức đơn giản của bức xạ TIR đo được khi có lớp aerosol (không tán xạ).',
          'I ≈ B(T_s)·e^(−τ_aer) + B(T_layer)·(1 − e^(−τ_aer))', ['I ≈ B(T_s)·τ_aer + B(T_layer)', 'I ≈ B(T_s) / B(T_layer)', 'I ≈ I₀·e^(+τ_aer)'],
          'Lớp thay một phần phát xạ ấm của bề mặt bằng phát xạ của chính nó ở nhiệt độ lớp.', 2, 'TIR', src='Đề cương 8.1')
    B.add('Hai lớp bụi có cùng AOD, một ở 5 km và một ở 1 km. Lớp nào gây độ giảm nhiệt độ sáng lớn hơn và vì sao?',
          'Lớp 5 km, vì lạnh hơn (~6,5 K/km) nên tương phản nhiệt với bề mặt lớn hơn', ['Lớp 1 km, vì ấm hơn nên phát xạ nhiều hơn bề mặt', 'Hai lớp như nhau vì cùng AOD', 'Lớp 1 km, vì gần mặt đất nên hấp thụ O₂ mạnh hơn'],
          f'Đáp án gợi ý Q8(b). Mô hình đơn giản (T_s = 300 K, τ = 0,5, 10 µm): ΔBT = {d1:.2f} K (1 km) và {d5:.2f} K (5 km), tính bằng Python.', 1, 'TIR', origin='goc', src='Đề thi mẫu Q8(b)')
    B.add(f'Trong mô hình đơn giản (T_s = 300 K, τ_aer = 0,5, 10 µm, gradient 6,5 K/km), độ giảm nhiệt độ sáng của lớp bụi ở 5 km là bao nhiêu?',
          f'≈ {d5:.1f} K', [f'≈ {d1:.1f} K', '≈ 32,5 K (bằng chênh nhiệt độ lớp và bề mặt)', '≈ 0 K'],
          f'T_layer = 300 − 6,5×5 = 267,5 K; I = B(300)e^(−0,5) + B(267,5)(1 − e^(−0,5)); đảo Planck ra BT = {T["z5"]["BT"]:.2f} K → ΔBT = {d5:.2f} K. Nhỏ hơn 32,5 K vì lớp chưa đen (ε = 1 − e^(−τ) = 0,39).', 2, 'TIR', src='Mô hình đơn giản tự dựng, tính bằng Python')
    B.add('Vì sao cùng một độ giảm nhiệt độ sáng có thể do lớp mỏng–cao hoặc lớp dày–thấp?',
          'Vì tín hiệu phụ thuộc τ_aer × (T_s − T_layer): AOD và độ cao suy biến, nên phải truy hồi đồng thời', ['Vì nhiệt độ lớp không ảnh hưởng đến tín hiệu', 'Vì hồng ngoại không nhạy với độ dày quang học', 'Vì bề mặt luôn phát xạ bằng lớp'],
          f'Ví dụ Python: lớp 5 km có τ = 0,1 cho ΔBT = {D["high_thin"]["dBT"]:.2f} K; lớp 1 km cần τ = {D["low_thick"]["tau"]:.2f} để cho cùng ΔBT. Cần dạng phổ cửa sổ 8–12 µm và thông tin nhiệt độ từ dải CO₂.', 2, 'TIR', src='Đề cương 8.1; số tính bằng Python')
    B.add('Khi nào phương pháp TIR thất bại?',
          'Khi tương phản nhiệt thấp (lớp thấp, nghịch nhiệt ban đêm, bề mặt lạnh)', ['Khi có nhiều ánh sáng Mặt Trời', 'Khi hạt là khói mịn, vì khi đó tương phản lớn nhất', 'Khi lớp aerosol rất cao'],
          'Đáp án gợi ý Q8(b); đề cương 8.1: nhạy với độ phát xạ bề mặt; chủ yếu cho hạt thô hấp thụ (bụi, tro) chứ không phải khói/sulfate mịn.', 2, 'TIR', origin='goc', src='Đề thi mẫu Q8(b)')
    B.add('Ưu điểm của TIR để tìm độ cao bụi là gì?',
          'Hoạt động ngày và đêm, trên sa mạc sáng nơi phương pháp khả kiến thất bại, nhạy với hạt thô', ['Chỉ cần ban ngày và trời quang', 'Không phụ thuộc độ phát xạ bề mặt', 'Nhạy với khói mịn hơn bụi'],
          'Đề cương 8.1 (IASI, AIRS; bụi sa mạc, tro núi lửa).', 1, 'TIR', src='Đề cương 8.1')
    B.add('Nguyên lý dải A của O₂ (khoảng 760 nm) để tìm độ cao aerosol là gì?',
          'Lớp aerosol cao phản xạ photon sớm nên đường đi qua O₂ ngắn → hấp thụ O₂ yếu hơn (vạch nông hơn)', ['Lớp aerosol cao phát xạ nhiều ở 760 nm', 'Lớp aerosol cao làm O₂ tăng hấp thụ', 'Độ sâu dải không phụ thuộc độ cao lớp'],
          'Đề cương 8.2: lớp thấp → photon xuống sâu → hấp thụ O₂ mạnh. Tỉ số radiance trong dải so với liên tục (755 nm) phụ thuộc áp suất lớp tán xạ.', 1, 'O₂ A-band', origin='goc', src='Đề thi mẫu Q8(a)')
    B.add('Tại sao dùng O₂ mà không phải khí khác để tìm độ cao?',
          'Vì O₂ phân bố đều với tỉ lệ biết trước (21%, theo áp suất), nên đường hấp thụ phản ánh trực tiếp đường đi photon', ['Vì O₂ phát xạ mạnh ở 760 nm', 'Vì O₂ có nồng độ thay đổi mạnh theo vị trí', 'Vì O₂ không hấp thụ ở dải này'],
          'Đáp án gợi ý Q8(a): không cần tiên nghiệm về khí; dải/nhánh khác nhau có độ hấp thụ khác nhau → thông tin về phân bố thẳng đứng.', 2, 'O₂ A-band', origin='goc', src='Đề thi mẫu Q8(a)')
    B.add('Ưu điểm và hạn chế của dải A O₂ là gì?',
          'Ưu: độ phân giải ngang cao, mọi loại aerosol; hạn chế: chỉ ban ngày, cần AOD đủ lớn, nhạy albedo bề mặt, giả định một lớp', ['Ưu: ngày và đêm; hạn chế: chỉ hạt thô', 'Ưu: không nhạy albedo; hạn chế: cần ban đêm', 'Ưu: đo trực tiếp profil; hạn chế: chỉ trên đại dương'],
          'Đề cương 8.2: TROPOMI ALH có độ chính xác ~0,5–1 km, trên đại dương và đất tối; cần AOD > ~0,3–0,5.', 2, 'O₂ A-band', src='Đề cương 8.2')
    B.add('Độ chính xác điển hình của độ cao lớp aerosol TROPOMI (ALH) là bao nhiêu?',
          '~0,5–1 km (trên đại dương và đất tối)', ['~10–20 km', '~50 m', '~5 K'],
          'Đề cương 8.2. Truy hồi bằng Optimal Estimation với mô hình RT đầy đủ, giả định lớp dày ~1 km.', 3, 'O₂ A-band', src='Đề cương 8.2')
    B.add('Kể một kỹ thuật thụ động khác cho độ cao vệt khói/bụi.',
          'Stereo/thị sai đa góc (MISR), phụ thuộc độ cao của UVAI, hoặc phức O₂–O₂ ở 477 nm (OMI)', ['Lidar hai bước sóng của CALIOP', 'Radar mưa Doppler', 'Độ trễ xung của GPS'],
          'Đáp án gợi ý Q8(c). Thị sai MISR đặc biệt hữu ích cho khói cháy và núi lửa.', 1, 'Khác', origin='goc', src='Đề thi mẫu Q8(c)')
    B.add('Tại sao độ cao aerosol quan trọng?',
          'Phân biệt PM bề mặt với vận chuyển trên cao, vận chuyển xa, hiệu ứng bức xạ, an toàn hàng không (tro núi lửa)', ['Chỉ để tính tán xạ Rayleigh', 'Chỉ để hiệu chuẩn lidar', 'Không có ý nghĩa thực tiễn'],
          'Đề cương Ch.8 mở đầu. Cảm biến thụ động chỉ suy ra độ cao gián tiếp qua hiệu ứng phụ thuộc độ cao.', 1, 'Khác', src='Đề cương Ch.8 (mở đầu)')
    B.add(f'Trong khí quyển đẳng nhiệt theo mũ (độ cao tỉ lệ 7 km), tỉ lệ O₂ còn phía trên lớp ở 5 km so với 1 km là gần nhất với giá trị nào?',
          f'≈ {OX["5"]:.2f} so với {OX["1"]:.2f}', [f'≈ {OX["1"]:.2f} so với {OX["5"]:.2f}', '≈ 1,0 cho cả hai', '≈ 0 cho cả hai'],
          f'p(z)/p₀ = e^(−z/7) → 1 km: {OX["1"]:.3f}; 3 km: {OX["3"]:.3f}; 5 km: {OX["5"]:.3f}; 8 km: {OX["8"]:.3f} (mô hình minh họa). Ít O₂ phía trên → vạch A-band nông hơn.', 3, 'O₂ A-band', src='Mô hình đơn giản tự dựng (H = 7 km), tính bằng Python')
    B.essay('(a) Giải thích vì sao dải A của O₂ (~760 nm) phù hợp để truy hồi độ cao aerosol hoặc mây. Tại sao O₂ mà không phải khí khác?\n(b) Trong hồng ngoại nhiệt, lớp bụi ở 5 km và lớp ở 1 km cùng AOD. Lớp nào cho độ giảm nhiệt độ sáng lớn hơn và vì sao? Khi nào phương pháp thất bại?\n(c) Nêu một kỹ thuật thụ động khác cho độ cao vệt khói.',
            f'(a) O₂ phân bố đều, profil biết trước (theo áp suất); lớp tán xạ cao rút ngắn đường đi photon → hấp thụ O₂ yếu hơn; độ sâu/hình dạng dải ↔ áp suất lớp.\n(b) Lớp 5 km: lạnh hơn (~6,5 K/km) → tương phản nhiệt với bề mặt lớn hơn → ΔBT lớn (mô hình: {d5:.1f} K so với {d1:.1f} K). Thất bại khi tương phản nhiệt thấp (lớp thấp, nghịch nhiệt ban đêm, bề mặt lạnh).\n(c) Thị sai/đa góc MISR; UVAI; O₂–O₂ 477 nm.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q8 (2,5 điểm) + đáp án gợi ý')
    B.essay('So sánh nguyên lý, ưu và nhược điểm của hai phương pháp xác định độ cao aerosol thụ động: hồng ngoại nhiệt và dải A của O₂.',
            'TIR (IASI, AIRS; bụi/tro): phát xạ ở nhiệt độ lớp, T giảm theo độ cao → BT thấp hơn khi lớp cao; ưu: ngày-đêm, trên sa mạc; nhược: cần tương phản nhiệt, nhạy độ phát xạ bề mặt, chủ yếu hạt thô. '
            'O₂ A-band (TROPOMI, EPIC, GOSAT, OCO-2): lớp cao → đường đi O₂ ngắn → hấp thụ yếu; ưu: phân giải ngang cao, mọi loại aerosol, O₂ biết trước; nhược: chỉ ban ngày, AOD > ~0,3–0,5, nhạy albedo, giả định một lớp. Cả hai truy hồi độ cao cùng AOD bằng mô hình RT/OE.', 3, 'Tổng hợp', origin='goc', src='Đề cương Ch.8 (Question)')
    B.essay(f'Mô hình đơn giản: T_s = 300 K, τ_aer = 0,5 ở 10 µm, gradient 6,5 K/km. Tính T_layer và so sánh độ giảm nhiệt độ sáng cho lớp ở 1 km và 5 km.',
            f'T_layer = 300 − 6,5 z: 293,5 K (1 km) và 267,5 K (5 km). I = B(T_s)e^(−τ) + B(T_layer)(1 − e^(−τ)); đảo hàm Planck ở 10 µm: BT = {T["z1"]["BT"]:.2f} K (1 km), {T["z5"]["BT"]:.2f} K (5 km) → ΔBT = {d1:.2f} K và {d5:.2f} K. Lớp cao cho độ giảm lớn hơn ~{d5/d1:.1f} lần.', 3, 'TIR', src='Mô hình tự dựng, số kiểm bằng Python')
    sl = [
        cover('Xác định độ cao aerosol bằng cảm biến thụ động', 'Retrieving aerosol altitude with passive sensors — Đề cương chương 8',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Hồng ngoại nhiệt · dải A của O₂ · phương pháp khác'),
        S('Vì sao cần độ cao aerosol', cards(card('Chất lượng không khí', 'Phân biệt PM bề mặt với aerosol vận chuyển trên cao.'), card('Vận chuyển xa', 'Lớp cao đi xa hơn.'),
          card('Hiệu ứng bức xạ', 'Độ cao quyết định cân bằng bức xạ.'), card('An toàn hàng không', 'Tro núi lửa.'), cols=4) + '<p class="note">Cảm biến thụ động chỉ suy ra độ cao <b>gián tiếp</b>, qua một hiệu ứng phụ thuộc độ cao.</p>'),
        S('Hai nguyên lý một hình', figfit('f7_altitude', 'Hình 21 (đề cương): (i) TIR — lớp phát xạ ở nhiệt độ của nó; (ii) dải A của O₂ — lớp cao thì ít O₂ phía trên.', 420) + '<p class="note">Cả hai truy hồi <b>độ cao cùng AOD</b> bằng cách khớp phổ với mô hình truyền bức xạ.</p>'),
        S('Hồng ngoại nhiệt: nguyên lý', fm('<span class="l">Phát xạ có lớp</span>I ≈ B(T<sub>s</sub>) e<sup>−τ<sub>aer</sub></sup> + B(T<sub>layer</sub>) (1 − e<sup>−τ<sub>aer</sub></sup>)', 28) +
          ulb(['Gradient nhiệt ≈ −6,5 K/km: lớp càng cao càng lạnh', 'Lớp càng cao → nhiệt độ sáng càng thấp', 'Tín hiệu ∝ τ<sub>aer</sub> × (T<sub>s</sub> − T<sub>layer</sub>)'], 33, 26)),
        S('Ví dụ số: lớp ở 1 km và 5 km', dtable(tbl(['Lớp', 'T<sub>layer</sub> (K)', 'BT đo (K)', 'ΔBT = T<sub>s</sub> − BT'], [
            ['1 km', f'{T["z1"]["Tl"]:.1f}', f'{T["z1"]["BT"]:.2f}', f'<b>{d1:.2f} K</b>'], ['5 km', f'{T["z5"]["Tl"]:.1f}', f'{T["z5"]["BT"]:.2f}', f'<b>{d5:.2f} K</b>']]), 'xl') +
          '<p class="note" style="margin-top:30px">T<sub>s</sub> = 300 K, τ = 0,5 ở 10 µm. Mô hình đơn giản (không tán xạ, không H₂O); Python đảo Planck ở 10 µm. Lớp 5 km cho ΔBT lớn gấp ~4,6 lần lớp 1 km.</p>'),
        S('Suy biến AOD và độ cao', dtable(tbl(['Lớp', 'Độ cao', 'τ', 'ΔBT'], [['Mỏng – cao', '5 km', f'{D["high_thin"]["tau"]:.2f}', f'{D["high_thin"]["dBT"]:.2f} K'], ['Dày – thấp', '1 km', f'{D["low_thick"]["tau"]:.2f}', f'{D["low_thick"]["dBT"]:.2f} K']]), 'xl') +
          '<p class="note" style="margin-top:22px">Cùng độ giảm nhiệt độ sáng: phải truy hồi đồng thời AOD và độ cao, dùng dạng phổ trong cửa sổ 8–12 µm và nhiệt độ từ dải CO₂.</p>'),
        S('Hồng ngoại nhiệt: ưu và nhược', cards(card('Ưu điểm', '• Ngày và đêm<br>• Trên sa mạc sáng<br>• Nhạy hạt thô: bụi, tro<br>• IASI, AIRS'), card('Nhược điểm', '• Cần tương phản nhiệt (thất bại: lớp thấp, nghịch nhiệt, bề mặt lạnh)<br>• Nhạy độ phát xạ bề mặt<br>• Không hợp khói, sulfate mịn'), cols=2)),
        S('Dải A của O₂ (khoảng 760 nm)', cols(ulb(['O₂ phân bố đều, profil biết trước', 'Lớp aerosol cao → photon phản xạ sớm', 'Đường đi qua O₂ ngắn → hấp thụ yếu, vạch nông', 'Lớp thấp → hấp thụ O₂ mạnh'], 28, 14),
          fm('R(λ) ≈ R<sub>aer</sub>(λ) · exp( −σ<sub>O₂</sub>(λ) N<sub>O₂</sub>(trên lớp) · AMF ) + …', 24) + dtable(tbl(['Độ cao', 'O₂ trên lớp'], [['1 km', f'{OX["1"]:.2f}'], ['3 km', f'{OX["3"]:.2f}'], ['5 km', f'{OX["5"]:.2f}'], ['8 km', f'{OX["8"]:.2f}']]), 'mid'), flex=[1.2, 1])),
        S('Độ nhạy theo độ cao của lớp', figfit('f17_height_sens', 'Hình 22 (đề cương): mô hình đơn giản — độ nhạy của tín hiệu TIR và dải A của O₂ theo độ cao lớp aerosol.', 420) + '<p class="note">Bảng phía trước dùng mô hình mũ H = 7 km, minh họa.</p>'),
        S('Dải A của O₂: ưu và nhược', cards(card('Ưu điểm', '• Không cần tiên nghiệm khí<br>• Phân giải ngang cao<br>• Mọi loại aerosol, cả khói và sulfate<br>• TROPOMI ALH ~0,5–1 km'), card('Nhược điểm', '• Chỉ ban ngày<br>• Cần AOD đủ lớn (> ~0,3–0,5)<br>• Nhạy albedo bề mặt<br>• Loại mây; giả định một lớp'), cols=2)),
        S('Phương pháp thụ động khác', cards(card('Thị sai đa góc', 'MISR: độ cao vệt khói cháy và núi lửa.'), card('Chỉ số UVAI', 'UVAI phụ thuộc độ cao lớp.'), card('Phức O₂–O₂ 477 nm', 'OMI: va chạm O₂–O₂.'), cols=3)),
        S('Exam checklist — Chương 8', chk(['TIR: phát xạ ở nhiệt độ lớp; T(z) giảm → lớp cao = lạnh = BT thấp; cần tương phản nhiệt; ngày-đêm; bụi/tro', 'Dải A O₂: O₂ trộn đều; lớp cao → đường đi ngắn → hấp thụ yếu; ban ngày; nhạy albedo', 'Cả hai truy hồi độ cao cùng AOD bằng mô hình RT / OE'])),
        S('Ý chính', dul(['TIR: lớp cao → lạnh → ΔBT lớn', 'O₂ A-band: lớp cao → ít O₂ phía trên', 'Truy hồi độ cao cùng AOD', 'Bổ sung: MISR, UVAI, O₂–O₂']))]
    mod = dict(id='m8', slug='08-aerosol-altitude', title='M8 · Độ cao aerosol', en='Retrieving aerosol altitude with passive sensors',
               question='<ul><li>Explain the principle to derive the altitude of aerosols employing passive remote sensing from space: (i) in the thermal infrared and (ii) in the near infrared.</li></ul>',
               calcs=[('tir', 'Độ giảm nhiệt độ sáng theo độ cao lớp bụi')],
               checklist=['TIR: emission at layer temperature; T(z) decreases with height → higher layer = colder = lower brightness temperature; needs thermal contrast; works day/night; dust/ash.', 'NIR O₂ A-band: well-mixed O₂ absorber; higher aerosol layer shortens photon path → weaker O₂ absorption; daytime, sensitive to surface albedo.', 'Both retrieve height together with AOD by fitting spectra with an RT model / optimal estimation.'],
               summary=['Hồng ngoại nhiệt: lớp bụi phát xạ theo nhiệt độ của chính nó; nhiệt độ giảm theo độ cao → lớp càng cao càng lạnh → nhiệt độ sáng đo được càng thấp. Cần tương phản nhiệt với bề mặt; đo được cả đêm và trên sa mạc.', 'Cận hồng ngoại (dải A của O₂, 760 nm): O₂ phân bố đều và đã biết; lớp aerosol càng cao → photon bị phản xạ sớm → đường đi qua O₂ ngắn → hấp thụ O₂ yếu hơn. Chỉ ban ngày, nhạy với albedo bề mặt.', 'Cả hai đều truy hồi đồng thời độ cao và AOD bằng mô hình truyền bức xạ.'],
               sections=[
        ('Vì sao đo độ cao, và đo bằng cách nào?', '<p>Biết aerosol nằm <b>ở đâu theo chiều thẳng đứng</b> quan trọng cho chất lượng không khí (PM bề mặt hay vận chuyển trên cao), vận chuyển xa, hiệu ứng bức xạ và an toàn hàng không (tro núi lửa). Cảm biến thụ động không đo độ cao trực tiếp; nó suy ra <b>gián tiếp</b> từ một hiệu ứng vật lý phụ thuộc độ cao.</p>' +
         lfig('f7_altitude', 'Hình 21 (đề cương): (i) TIR — lớp phát xạ ở nhiệt độ riêng; (ii) dải A của O₂ — lớp càng cao thì O₂ phía trên càng ít.')),
        ('(i) Hồng ngoại nhiệt (IASI, AIRS: chủ yếu bụi sa mạc, tro núi lửa)', '<p>Trong TIR, bức xạ chủ yếu là phát xạ. Hạt thô (bụi, tro) hấp thụ và phát xạ trong cửa sổ khí quyển 8–12 µm (dải silicat quanh 9–10 µm). Một lớp bụi thay một phần phát xạ ấm của bề mặt bằng phát xạ của chính nó ở nhiệt độ lớp:</p>' +
         eq('Phát xạ có lớp', 'I ≈ B(T<sub>s</sub>) · e<sup>−τ<sub>aer</sub></sup> + B(T<sub>layer</sub>) · (1 − e<sup>−τ<sub>aer</sub></sup>)') +
         '<ul><li>Nhiệt độ giảm theo độ cao (≈ −6,5 K/km ở đối lưu) → lớp càng cao càng lạnh → nhiệt độ sáng TOA càng thấp (độ giảm so với trời quang càng lớn).</li><li>Tín hiệu ∝ τ<sub>aer</sub> × (T<sub>s</sub> − T<sub>layer</sub>) nên <b>AOD và độ cao suy biến</b>: phải truy hồi cùng nhau, dùng dạng phổ trong cửa sổ và nhiệt độ từ dải CO₂.</li><li>Truy hồi: mô hình RT (hoặc LUT/mạng nơ-ron) với tính chất quang học IR → AOD 10 µm và độ cao trung bình.</li></ul>' +
         f'<div class="ex"><div class="exh">Ví dụ · số kiểm bằng Python (mô hình đơn giản, không tán xạ, 10 µm)</div>' +
         hx_table(['Lớp', 'T<sub>layer</sub>', 'BT đo', 'ΔBT = T<sub>s</sub> − BT'], [['1 km', f'{T["z1"]["Tl"]:.1f} K', f'{T["z1"]["BT"]:.2f} K', f'<b>{d1:.2f} K</b>'], ['5 km', f'{T["z5"]["Tl"]:.1f} K', f'{T["z5"]["BT"]:.2f} K', f'<b>{d5:.2f} K</b>']]) +
         f'<p style="margin:4px 0">T<sub>s</sub> = 300 K, τ = 0,5. Lớp 5 km cho độ giảm lớn hơn ~{d5/d1:.1f} lần. <b>Suy biến:</b> lớp 5 km với τ = {D["high_thin"]["tau"]:.2f} cho {D["high_thin"]["dBT"]:.2f} K; lớp 1 km cần τ = {D["low_thick"]["tau"]:.2f} để cho đúng giá trị đó.</p></div>' +
         hx_table(['Ưu điểm', 'Hạn chế'], [['Ngày và đêm; trên sa mạc sáng (nơi phương pháp khả kiến thất bại); nhạy hạt thô', 'Cần tương phản nhiệt (thất bại khi T lớp ≈ T bề mặt: lớp thấp, nghịch nhiệt ban đêm); nhạy độ phát xạ bề mặt; chủ yếu bụi/tro hấp thụ, không phải khói/sulfate mịn']], 'left') +
         '<p>Kỹ thuật liên quan: CO₂ slicing / chênh lệch nhiệt độ sáng (11–12 µm) cho tro núi lửa và độ cao đỉnh mây.</p>'),
        ('(ii) Cận hồng ngoại: dải A của O₂ (TROPOMI ALH, EPIC, GOSAT, OCO-2)', '<p>O₂ phân bố đều (21%, theo áp suất). Trong dải A (759–771 nm), hấp thụ O₂ phụ thuộc <b>độ dài đường đi của photon</b>. Aerosol tán xạ photon về vũ trụ trước khi chúng xuống thấp:</p>' +
         '<ul><li>Lớp cao → photon phản xạ ở trên cao → đường đi qua O₂ ngắn (ít O₂ phía trên lớp) → hấp thụ yếu (vạch nông).</li><li>Lớp thấp → photon xuống sâu → hấp thụ O₂ mạnh.</li><li>Tỉ số radiance trong dải so với liên tục (755 nm) hoặc khớp toàn dải phụ thuộc áp suất lớp tán xạ; các vạch mạnh yếu khác nhau cho độ xuyên khác nhau → hình dạng dải mang thông tin phân bố thẳng đứng.</li></ul>' +
         eq('Mô hình', 'R(λ) ≈ R<sub>aer</sub>(λ) · exp( −σ<sub>O₂</sub>(λ) · N<sub>O₂</sub>(phía trên lớp) · AMF ) + …') +
         f'<div class="ex"><div class="exh">Ví dụ minh họa · khí quyển mũ H = 7 km (tính bằng Python)</div>' + hx_table(['Độ cao lớp', '1 km', '3 km', '5 km', '8 km'], [['O₂ phía trên (so với mặt đất)', f'{OX["1"]:.2f}', f'{OX["3"]:.2f}', f'{OX["5"]:.2f}', f'{OX["8"]:.2f}']]) + '</div>' +
         '<p><b>Truy hồi:</b> Optimal Estimation với RT đầy đủ (tán xạ nhiều lần), truy hồi độ cao (hoặc áp suất) lớp và AOD, giả định mô hình aerosol và lớp dày ~1 km. TROPOMI ALH: độ chính xác ~0,5–1 km trên đại dương và đất tối.</p>' +
         hx_table(['Ưu điểm', 'Hạn chế'], [['Phân bố O₂ biết trước (không cần tiên nghiệm khí); phân giải ngang cao; mọi loại aerosol kể cả khói và sulfate', 'Chỉ ban ngày; cần AOD đủ lớn (> ~0,3–0,5); rất nhạy albedo bề mặt (đất sáng che tín hiệu); phải loại mây; giả định một lớp']], 'left') +
         lfig('f17_height_sens', 'Hình 22 (đề cương): mô hình đơn giản — độ nhạy của tín hiệu TIR và dải A của O₂ theo độ cao lớp aerosol.') +
         '<p><b>Phương pháp thụ động khác:</b> thị sai/đa góc (MISR, độ cao vệt khói cháy và núi lửa); sự phụ thuộc độ cao của UVAI; phức O₂–O₂ ở 477 nm (OMI).</p>')])
    return mod, sl, B
