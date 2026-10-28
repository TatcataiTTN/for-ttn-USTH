# -*- coding: utf-8 -*-
"""M4 — Hình học quan sát của cảm biến vệ tinh (đề cương Ch.4)."""
from lib import *
from qcore import Bank
V = VERIFIED
two = lambda a, b: cards(a, b, cols=2)

def build():
    B = Bank('m4', seed=4)
    B.add('Ba hình học quan sát chính của cảm biến vệ tinh thăm dò thành phần khí quyển là gì?',
          'Nadir (nhìn xuống), limb (nhìn tiếp tuyến qua rìa), che khuất (occultation)', ['Nadir, zenith và cực (polar)', 'Limb, quỹ đạo địa tĩnh và quỹ đạo elip', 'Nadir, off-nadir và quét ngang (whiskbroom)'],
          'Đề cương Ch.4: nadir (kể cả off-nadir/quét ngang), limb (tán xạ hoặc phát xạ), che khuất (Mặt Trời, Mặt Trăng, sao, GNSS).', 1, 'Ba hình học', origin='goc', src='Đề cương Ch.4 (checklist)')
    B.add('Chế độ nadir hoạt động theo cách nào?',
          'Cảm biến nhìn thẳng xuống Trái Đất (hoặc quét ngang quỹ đạo) và đo ánh sáng tán xạ ngược hoặc phát xạ nhiệt', ['Cảm biến nhìn tiếp tuyến qua rìa khí quyển và đo bức xạ tán xạ về phía trước', 'Cảm biến nhìn thẳng vào Mặt Trời khi mọc hoặc lặn để đo độ truyền qua', 'Cảm biến phát xung laser và đo thời gian phản hồi của xung'],
          'Đề cương 4.1: ví dụ TROPOMI, OMI, GOME-2, IASI, MOPITT, OCO-2. Trường nhìn thẳng cắt qua cả khí quyển một lần.', 1, 'Nadir', src='Đề cương 4.1')
    B.add('Chế độ limb: cảm biến nhìn như thế nào, và quét độ cao ra sao?',
          'Nhìn tiếp tuyến qua rìa khí quyển phía trên đường chân trời, quét đường ngắm theo chiều thẳng đứng (độ cao tiếp tuyến ~5 đến 100 km)', ['Nhìn thẳng đứng xuống bề mặt, độ cao suy ra từ độ trễ xung', 'Nhìn Mặt Trời mọc, độ cao suy ra từ thời điểm quan sát', 'Nhìn theo góc 45° so với thiên đỉnh, độ cao suy ra từ nhiệt độ'],
          'Đề cương 4.2: đo ánh sáng tán xạ (OSIRIS, OMPS-LP, SCIAMACHY limb) hoặc phát xạ nhiệt (MIPAS, MLS vi sóng).', 1, 'Limb', src='Đề cương 4.2')
    B.add('Che khuất (occultation) khác limb ở điểm nào?',
          'Cảm biến nhìn một nguồn sáng (Mặt Trời, Mặt Trăng, sao, tín hiệu GPS) xuyên qua rìa khí quyển và đo độ truyền qua I/I₀', ['Cảm biến đo phát xạ nhiệt của khí quyển bằng vi sóng', 'Cảm biến nhìn thẳng xuống nên không có đường ngắm qua rìa', 'Cảm biến phát nguồn sáng riêng và đo tán xạ ngược của nó'],
          'Đề cương 4.3: SAGE II/III, ACE-FTS (Mặt Trời), GOMOS (sao), GNSS radio occultation (nhiệt độ/độ ẩm).', 1, 'Che khuất', src='Đề cương 4.3')
    B.add('Ưu điểm chính của nadir là gì?',
          'Phân giải ngang tốt (vài km, TROPOMI 5,5×3,5 km²), phủ toàn cầu hằng ngày, thấy được đối lưu/lớp biên', ['Phân giải thẳng đứng 1–3 km nhờ hình học', 'Tự hiệu chuẩn nhờ tỉ số I/I₀', 'Không chịu ảnh hưởng của bề mặt hay mây'],
          'Đề cương 4.4: nadir hợp với chất lượng không khí và phát thải. Nhược điểm: phân giải thẳng đứng kém (cột hoặc 1–6 mẩu thông tin) và nhạy bề mặt, mây, aerosol.', 1, 'So sánh', src='Đề cương 4.4')
    B.add('Nhược điểm chính của nadir là gì?',
          'Phân giải thẳng đứng kém, nhạy với albedo/độ phát xạ bề mặt, mây, aerosol; đường đi qua khí quyển ngắn nên tín hiệu mỗi lớp yếu', ['Chỉ phủ vài chục profil mỗi ngày', 'Không nhìn được tầng đối lưu', 'Phân giải ngang rất kém (200–400 km)'],
          'Đề cương 4.4. Nadir mạnh ở phân giải ngang nhưng yếu ở phân giải thẳng đứng, ngược với limb và che khuất.', 2, 'So sánh', src='Đề cương 4.4')
    B.add('Ưu điểm chính của limb là gì?',
          'Phân giải thẳng đứng tốt (1–3 km), đường đi dài nên rất nhạy, không có nền bề mặt (nền không gian tối)', ['Phân giải ngang vài km và phủ toàn cầu hằng ngày', 'Nhìn được lớp biên khí quyển', 'Truy hồi đơn giản, không cần mô hình truyền bức xạ phức tạp'],
          'Đề cương 4.4. Nhược điểm: phân giải ngang dọc đường ngắm kém (~200–400 km), không nhìn xuống dưới ~5–10 km, RT phức tạp, cần biết chính xác hướng ngắm.', 1, 'So sánh', src='Đề cương 4.4')
    B.add('Nhược điểm chính của limb là gì?',
          'Phân giải ngang kém (~200–400 km), không nhìn xuống dưới ~5–10 km nên không phù hợp lớp biên; RT phức tạp', ['Phân giải thẳng đứng chỉ đạt vài chục km', 'Nhạy mạnh với albedo bề mặt', 'Chỉ có vài profil mỗi ngày do phụ thuộc mặt trời mọc lặn'],
          'Đề cương 4.4. Đường ngắm dài vài trăm km nên phân giải ngang kém; mây và bão hòa đường đi chặn tầm nhìn dưới đối lưu trên.', 2, 'So sánh', src='Đề cương 4.4')
    B.add('Vì sao che khuất được gọi là "tự hiệu chuẩn" (self-calibrating)?',
          'Vì tỉ số I/I₀ (đo ngoài khí quyển và xuyên khí quyển) loại bỏ trôi của thiết bị, rất chính xác cho xu hướng dài hạn', ['Vì thiết bị tự thay đổi bước sóng để khớp vạch', 'Vì nó dùng chuẩn Mặt Trăng làm hiệu chuẩn bên ngoài', 'Vì nó không cần mô hình truyền bức xạ nào cả'],
          'Đề cương 4.4: tín hiệu Mặt Trời mạnh, phân giải thẳng đứng ~1 km, S/N cao, RT đơn giản (Beer–Lambert).', 2, 'So sánh', src='Đề cương 4.4')
    B.add('Nhược điểm lớn nhất của che khuất Mặt Trời là gì?',
          f'Độ phủ rất kém: chỉ ~30 profil mỗi ngày (2 mỗi quỹ đạo), phụ thuộc quỹ đạo và vĩ độ', ['Độ chính xác kém hơn limb nhiều lần', 'Không nhìn được tầng bình lưu', 'Phụ thuộc mạnh vào albedo bề mặt'],
          '30 profil/ngày ÷ 2 profil/quỹ đạo ngầm hiểu khoảng 15 quỹ đạo/ngày — phù hợp quỹ đạo thấp. Đề cương 4.4.', 1, 'So sánh', src='Đề cương 4.4')
    B.add('Hình học nào phù hợp nhất để theo dõi xu hướng dài hạn ozone tầng bình lưu với độ chính xác cao nhất?',
          'Che khuất Mặt Trời: tự hiệu chuẩn (I/I₀), phân giải thẳng đứng cao, chất lượng xu hướng tốt', ['Nadir: phủ toàn cầu và phân giải ngang tốt nhất', 'Limb phát xạ: hoạt động cả ngày lẫn đêm', 'Quỹ đạo địa tĩnh: quan sát hằng giờ'],
          'Đáp án gợi ý Q4(b-i). Chấp nhận đổi lấy độ phủ kém, vì mục tiêu là xu hướng chính xác.', 2, 'Chọn hình học', origin='goc', src='Đề thi mẫu Q4(b)(i)')
    B.add('Hình học nào phù hợp nhất để lập bản đồ phát thải NO₂ của từng thành phố?',
          'Nadir: phân giải ngang cỡ km, phủ toàn cầu hằng ngày, nhạy với lớp biên', ['Che khuất: độ chính xác cao nhất', 'Limb: phân giải thẳng đứng 1–3 km', 'Limb phát xạ: đo cả ngày lẫn đêm'],
          'Đáp án gợi ý Q4(b-ii): phát xạ đô thị cần phân giải ngang tốt và sự nhạy với lớp biên mà limb/che khuất không có.', 2, 'Chọn hình học', origin='goc', src='Đề thi mẫu Q4(b)(ii)')
    B.add('So với quỹ đạo thấp đồng bộ Mặt Trời (LEO), quỹ đạo địa tĩnh đem lại lợi ích gì cho giám sát chất lượng không khí?',
          'Quan sát một lục địa mỗi giờ nên thấy chu kỳ ngày đêm (giờ cao điểm, quang hóa) và có nhiều cảnh không mây hơn', ['Phủ toàn cầu mỗi giờ bao gồm cả hai cực', 'Phân giải ngang tốt hơn LEO vì ở xa hơn', 'Có thể dùng chế độ limb bao phủ toàn cầu'],
          'Đáp án gợi ý Q4(c). LEO chỉ qua một lần/ngày ở giờ địa phương cố định nhưng phủ toàn cầu; GEO (GEMS, TEMPO, Sentinel-4) chỉ nhìn một vùng.', 2, 'Quỹ đạo', origin='goc', src='Đề thi mẫu Q4(c)')
    B.add('Làm thế nào để thu cột đối lưu từ kết hợp nadir và limb (như SCIAMACHY, OMPS)?',
          'Cột đối lưu = cột tổng (nadir) trừ cột bình lưu (limb)', ['Cột đối lưu = cột limb nhân với AMF của nadir', 'Cột đối lưu = cột tổng cộng cột bình lưu', 'Cột đối lưu = cột che khuất chia cho hệ số Ångström'],
          'Đề cương, ghi chú cuối 4.4: nadir thấy toàn cột, limb thấy phần bình lưu; hiệu số là đối lưu.', 2, 'Quỹ đạo', src='Đề cương 4.4 (ghi chú)')
    B.add('Quỹ đạo LEO đồng bộ Mặt Trời có đặc điểm nào?',
          'Phủ toàn cầu một lần mỗi ngày tại giờ địa phương cố định', ['Quan sát một lục địa liên tục mỗi giờ', 'Phủ đều toàn cầu mỗi giờ', 'Đứng yên trên một điểm của xích đạo'],
          'Đề cương 4.4: LEO sun-synchronous (TROPOMI, OMI, GOME-2) qua mỗi nơi cùng giờ địa phương; địa tĩnh thì đứng yên so với mặt đất.', 1, 'Quỹ đạo', src='Đề cương 4.4 (ghi chú)')
    B.add('Cặp nào đúng về phân giải ngang và thẳng đứng điển hình?',
          'Nadir: ngang vài km, thẳng đứng thô; limb: ngang ~200–400 km, thẳng đứng ~1–3 km', ['Nadir: ngang ~200–400 km, thẳng đứng ~1 km; limb: ngang vài km, thẳng đứng thô', 'Cả hai đều ngang vài km và thẳng đứng ~1 km', 'Nadir: ngang ~1 000 km; limb: ngang ~1 km'],
          'Đề cương hình 14: có sự đánh đổi (trade-off) giữa phân giải ngang và thẳng đứng; che khuất: thẳng đứng ~1 km nhưng ngang kém.', 2, 'So sánh', src='Đề cương 4.4, hình 14')
    B.add('Phương pháp nào KHÔNG dùng để đo độ cao trực tiếp qua hình học?',
          'Nadir: độ cao suy từ hàm trọng số, không từ hình học', ['Limb: độ cao tiếp tuyến của từng tia', 'Che khuất Mặt Trời: độ cao tiếp tuyến lúc mọc/lặn', 'Che khuất GNSS: góc uốn cong của tia tín hiệu'],
          'Hình học limb và che khuất cho phân giải thẳng đứng trực tiếp từ độ cao tiếp tuyến; nadir cần hàm trọng số và tiên nghiệm.', 3, 'So sánh', src='Đề cương 4.2–4.4')
    B.essay('(a) Vẽ phác nadir, limb và che khuất Mặt Trời.\n(b) Chọn hình học để (i) theo dõi xu hướng dài hạn ozone bình lưu chính xác nhất, (ii) lập bản đồ phát thải NO₂ từng thành phố. Giải thích.\n(c) Quỹ đạo địa tĩnh bổ sung điều gì so với LEO đồng bộ Mặt Trời?',
            '(a) Vẽ Trái Đất, vỏ khí quyển, đường ngắm: nadir xuyên thẳng xuống; limb tiếp tuyến với rìa; che khuất: từ Mặt Trời xuyên rìa khí quyển tới cảm biến (xem hình 13 trong đề cương).\n'
            '(b)(i) Che khuất Mặt Trời: tự hiệu chuẩn I/I₀, phân giải thẳng đứng ~1 km, S/N cao → xu hướng tốt. (b)(ii) Nadir: phân giải ngang cỡ km, phủ hằng ngày, nhạy lớp biên.\n'
            '(c) Quan sát hằng giờ một lục địa → chu kỳ ngày đêm, giờ cao điểm, quang hóa, nhiều cảnh không mây hơn; LEO: một lần/ngày cố định giờ nhưng phủ toàn cầu.', 3, 'Đề thi mẫu', origin='goc', src='Đề thi mẫu Q4 (2,5 điểm) + đáp án gợi ý')
    B.essay('Lập bảng ưu – nhược điểm của nadir, limb và che khuất.',
            'Nadir: + phân giải ngang tốt, phủ toàn cầu, thấy đối lưu, ngày (UV-vis) và ngày-đêm (TIR); − thẳng đứng kém, nhạy bề mặt/mây/aerosol, đường đi ngắn. '
            'Limb: + thẳng đứng 1–3 km, đường dài nên nhạy, không nền bề mặt, phát xạ cả ngày đêm; − ngang kém ~200–400 km, không nhìn dưới 5–10 km, RT phức tạp. '
            'Che khuất: + tự hiệu chuẩn, chính xác, thẳng đứng ~1 km, S/N cao, RT đơn giản; − chỉ ~30 profil/ngày, ngang kém, chỉ đối lưu trên và bình lưu.', 2, 'So sánh', origin='goc', src='Đề cương Ch.4 (bảng 4.4)')
    sl = [
        cover('Hình học quan sát của cảm biến vệ tinh', 'Pointing geometries of spaceborne sensors — Đề cương chương 4',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Nadir · limb · che khuất · quỹ đạo thấp và địa tĩnh'),
        S('Ba hình học quan sát', figfit('f3_geometries', 'Hình 13 (đề cương): nadir, limb và che khuất.', 360) + ulb(['<b>Nadir</b>: nhìn xuống — TROPOMI, OMI, GOME-2, IASI, OCO-2', '<b>Limb</b>: nhìn tiếp tuyến — OSIRIS, MIPAS, MLS', '<b>Che khuất</b>: nhìn Mặt Trời qua rìa — SAGE, ACE-FTS'], 27, 12)),
        S('Nadir: ưu và nhược điểm', two(
            card('Ưu điểm', '• Phân giải ngang vài km (TROPOMI 5,5×3,5 km²)<br>• Phủ toàn cầu hằng ngày<br>• Thấy đối lưu/lớp biên<br>• Ngày (UV-vis), ngày-đêm (TIR)'),
            card('Nhược điểm', '• Phân giải thẳng đứng kém (cột hoặc 1–6 mẩu thông tin)<br>• Nhạy albedo, độ phát xạ bề mặt, mây, aerosol<br>• Đường đi ngắn → tín hiệu mỗi lớp yếu'))),
        S('Limb: ưu và nhược điểm', two(
            card('Ưu điểm', '• Phân giải thẳng đứng 1–3 km<br>• Đường đi dài → rất nhạy<br>• Không có nền bề mặt<br>• Limb phát xạ: ngày và đêm'),
            card('Nhược điểm', '• Phân giải ngang ~200–400 km<br>• Không nhìn dưới ~5–10 km<br>• RT phức tạp (cầu, tán xạ nhiều lần)<br>• Cần biết hướng ngắm chính xác'))),
        S('Che khuất: ưu và nhược điểm', two(
            card('Ưu điểm', '• Tự hiệu chuẩn: tỉ số I/I<sub>0</sub> loại trôi thiết bị<br>• Rất chính xác, hợp xu hướng dài hạn<br>• Tín hiệu mạnh, thẳng đứng ~1 km, S/N cao<br>• RT đơn giản (Beer–Lambert)'),
            card('Nhược điểm', '• Độ phủ rất kém: ~30 profil/ngày (2 mỗi quỹ đạo)<br>• Dải vĩ độ phụ thuộc quỹ đạo<br>• Phân giải ngang kém dọc đường<br>• Chỉ đối lưu trên và bình lưu'))),
        S('Đánh đổi phân giải ngang – thẳng đứng', figfit('f15_tradeoff', 'Hình 14 (đề cương): phân giải ngang và thẳng đứng xấp xỉ của các thiết bị tiêu biểu theo hình học.', 480) + '<p class="note">Nadir thắng ở ngang, limb và che khuất thắng ở thẳng đứng.</p>'),
        S('Quỹ đạo: LEO và địa tĩnh', cards(card('LEO đồng bộ Mặt Trời', 'Phủ toàn cầu một lần mỗi ngày, giờ địa phương cố định.<br>TROPOMI, OMI, GOME-2'),
          card('Địa tĩnh (GEO)', 'Quan sát một lục địa mỗi giờ → chu kỳ ngày đêm của ô nhiễm.<br>GEMS, TEMPO, Sentinel-4'),
          card('Nadir + limb', 'Cột đối lưu = cột tổng (nadir) − cột bình lưu (limb).<br>SCIAMACHY, OMPS'), cols=3)),
        S('Chọn hình học theo mục tiêu', dtable(tbl(['Mục tiêu', 'Hình học', 'Lý do'], [
            ['Xu hướng ozone bình lưu chính xác', 'Che khuất Mặt Trời', 'Tự hiệu chuẩn, S/N cao, ~1 km'],
            ['Phát xạ NO₂ từng thành phố', 'Nadir', 'Phân giải ngang km, nhạy lớp biên'],
            ['Profil bình lưu hóa học', 'Limb', 'Thẳng đứng 1–3 km, nhiều loài'],
            ['Chu kỳ ngày đêm ô nhiễm', 'Nadir địa tĩnh', 'Quan sát hằng giờ']]), 'xl')),
        S('Exam checklist — Chương 4', chk(['Ba hình học: nadir, limb (tán xạ/phát xạ), che khuất (Mặt Trời, sao, Mặt Trăng, GNSS)', 'Đánh đổi: phân giải ngang và độ nhạy đối lưu (nadir) ↔ phân giải thẳng đứng và độ chính xác (limb/che khuất)', 'Che khuất = tự hiệu chuẩn, chính xác nhất, phủ kém nhất', 'Vẽ ba hình học với Trái Đất, vỏ khí quyển và đường ngắm'])),
        S('Ý chính', dul(['Nadir: ngang tốt, thẳng đứng kém', 'Limb: thẳng đứng tốt, ngang kém, không xuống thấp', 'Che khuất: tự hiệu chuẩn, chính xác nhưng ít profil', 'Địa tĩnh: quan sát hằng giờ chu kỳ ngày đêm']))]
    mod = dict(id='m4', slug='04-pointing-geometries', title='M4 · Hình học quan sát', en='Pointing geometries of spaceborne sensors',
               question='<ul><li>What are the possible pointing geometries of spaceborne sensors for sounding the atmospheric composition?</li><li>What are the advantages and disadvantages of each case?</li></ul>',
               calcs=[], checklist=['Three geometries: nadir, limb (scattering/emission), occultation (solar/stellar/lunar/GNSS).', 'Trade-off: horizontal resolution & tropospheric sensitivity (nadir) ↔ vertical resolution & accuracy (limb/occultation).',
                                    'Occultation = self-calibrating, best accuracy, worst coverage.', 'Draw the three geometries with Earth, atmosphere shell, lines of sight.'],
               summary=['Nadir: nhìn thẳng xuống → độ phân giải ngang tốt, phủ toàn cầu hằng ngày, nhìn thấy tầng đối lưu; nhưng độ phân giải thẳng đứng kém, nhạy với mây/bề mặt.',
                        'Limb: nhìn tiếp tuyến qua rìa khí quyển → độ phân giải thẳng đứng tốt (1–3 km), không có nền bề mặt; nhưng độ phân giải ngang kém, không xuống thấp dưới ~5–10 km.',
                        'Che khuất (occultation): nhìn Mặt Trời/sao qua rìa khí quyển → tự hiệu chuẩn, rất chính xác; nhưng số lượng phép đo rất ít.'],
               sections=[
        ('Ba hình học, nói nôm na', '<p>Cùng một khí quyển nhưng có ba cách nhìn: <b>nhìn thẳng xuống</b> như chụp ảnh từ máy bay (nadir); <b>nhìn ngang qua rìa</b> như nhìn một lát bánh theo chiều ngang (limb); và <b>nhìn Mặt Trời mọc/lặn xuyên qua bầu khí quyển</b> (che khuất).</p>' +
         lfig('f3_geometries', 'Hình 13 (đề cương): nadir, limb và che khuất.') +
         hx_table(['Hình học', 'Cách nhìn', 'Ví dụ thiết bị'], [['Nadir (và off-nadir/quét ngang)', 'Nhìn xuống; đo ánh sáng tán xạ ngược (UV-vis-SWIR) hoặc phát xạ nhiệt (TIR)', 'TROPOMI, OMI, GOME-2, IASI, MOPITT, OCO-2'],
             ['Limb', 'Nhìn tiếp tuyến trên đường chân trời, quét độ cao tiếp tuyến ~5 đến 100 km; đo ánh sáng tán xạ hoặc phát xạ nhiệt', 'OSIRIS, OMPS-LP, SCIAMACHY limb (tán xạ); MIPAS, MLS (phát xạ)'],
             ['Che khuất', 'Nhìn Mặt Trời, Mặt Trăng, sao hoặc tín hiệu GNSS qua rìa lúc mọc/lặn; đo I/I₀', 'SAGE II/III, ACE-FTS, GOMOS (sao), GNSS radio occultation']], 'left')),
        ('So sánh ưu – nhược điểm', hx_table(['Hình học', 'Ưu điểm', 'Nhược điểm'], [
            ['Nadir', '• Phân giải ngang tốt (vài km; TROPOMI 5,5×3,5 km²), phủ toàn cầu hằng ngày<br>• Thấy đối lưu và lớp biên → chất lượng không khí, phát thải<br>• Ngày (UV-vis) và ngày-đêm (TIR)', '• Phân giải thẳng đứng kém (cột hoặc 1–6 mẩu thông tin)<br>• Nhạy albedo/độ phát xạ bề mặt, mây, aerosol<br>• Đường đi ngắn → tín hiệu mỗi lớp yếu'],
            ['Limb', '• Phân giải thẳng đứng tốt (1–3 km) nhờ hình học<br>• Đường đi dài → rất nhạy, nhiều loài bình lưu<br>• Không có nền bề mặt (nền không gian tối)<br>• Limb phát xạ: ngày và đêm', '• Phân giải ngang dọc đường ngắm kém (~200–400 km)<br>• Không nhìn dưới ~5–10 km (mây, bão hòa) → không hợp lớp biên<br>• RT phức tạp (cầu, tán xạ nhiều lần); cần biết hướng ngắm rất chính xác'],
            ['Che khuất', '• Tự hiệu chuẩn: I/I₀ loại trôi thiết bị → rất chính xác, hợp xu hướng<br>• Tín hiệu Mặt Trời mạnh, thẳng đứng ~1 km, S/N cao<br>• RT đơn giản (Beer–Lambert)', '• Độ phủ rất kém: ~30 profil/ngày (2 mỗi quỹ đạo với Mặt Trời)<br>• Dải vĩ độ phụ thuộc quỹ đạo; ngang kém dọc đường<br>• Chỉ đối lưu trên và bình lưu']], 'left') +
         lfig('f15_tradeoff', 'Hình 14 (đề cương): phân giải ngang và thẳng đứng xấp xỉ của từng loại thiết bị.')),
        ('Quỹ đạo cũng quan trọng', '<p>Hình học chỉ là một nửa; <b>quỹ đạo</b> là nửa còn lại:</p><ul><li><b>LEO đồng bộ Mặt Trời</b>: phủ toàn cầu một lần mỗi ngày tại giờ địa phương cố định.</li><li><b>Địa tĩnh</b> (GEMS, TEMPO, Sentinel-4): quan sát nadir một lục địa mỗi giờ → thấy <b>chu kỳ ngày đêm</b> của ô nhiễm (giờ cao điểm, quang hóa) và dễ tìm cảnh không mây.</li><li><b>Nadir + limb</b> (SCIAMACHY, OMPS): cột đối lưu = cột tổng (nadir) − cột bình lưu (limb).</li></ul>' +
         callout('info', 'Chọn theo mục tiêu', 'Xu hướng ozone bình lưu chính xác → che khuất Mặt Trời. Phát xạ NO₂ từng thành phố → nadir. Profil hóa học bình lưu chi tiết → limb.'))])
    return mod, sl, B
