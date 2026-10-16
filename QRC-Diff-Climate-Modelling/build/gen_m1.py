import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit, balance_length
from sitelib import module_page

B=Bank('m1',seed=1)
SRC='Nguyen-Le & Ngo-Duc (2025), "Modulation of PDO and the Victoria Mode on the ENSO-EASM relationship", J. Climate 38(20):5655-5670, DOI 10.1175/JCLI-D-24-0626.1 (bài #1, full-text verify) + Hartmann, Global Physical Climatology; Ding (1994), Monsoon over China'

# ---- câu hỏi gốc (bám trực tiếp nội dung paper #1 đã đọc full-text) ----
B.add('EASMI (Wang and Fan 1999) được định nghĩa dựa trên đại lượng nào?',
    'Độ lệch (shear) ngang chuẩn hoá của gió vĩ hướng 850-hPa giữa 2 vùng (5-15°N,90-130°E) và (22.5-32.5°N,110-140°E) trong JJA(0)',
    ['Áp suất mực biển trung bình JJA tại Đông Á','Lượng mưa tích luỹ mùa hè toàn Trung Quốc','Nhiệt độ mặt biển trung bình Biển Đông mùa hè'],
    'Paper #1 định nghĩa EASMI (Wang & Fan 1999; Wang et al. 2008) là độ lệch ngang chuẩn hoá của U850 giữa hai vùng nhiệt đới/cận nhiệt đới Đông Á trong JJA(0); EASMI âm = hoàn lưu nghịch đảo (anticyclonic) bất thường = gió mùa hè yếu.',level=1,topic='EASMI')
B.add('Hệ số tương quan giữa EASMI JJA(0) và chỉ số Niño-3.4 mùa đông trước NDJ(-1/0), tính trên toàn bộ 165 năm quan sát (không phân biệt pha ENSO), là bao nhiêu?',
    '-0.28 (p<0.01)',['+0.28 (p<0.01)','-0.51 (p<0.01)','+0.09 (không có ý nghĩa)'],
    'Paper #1 báo cáo tương quan âm -0.28 (p<0.01) trên toàn bộ 165 năm (COBE-SST2 + 20CRv3), xác nhận quan hệ ENSO-EASM nghịch tổng thể.',level=1,topic='ENSO-EASM')
B.add('Khi phân theo pha ENSO, tương quan EASMI-Niño3.4 mạnh hơn rõ rệt ở giai đoạn nào?',
    'Các mùa hè sau El Niño (hệ số đạt -0.51)',['Các mùa hè sau La Niña (hệ số đạt -0.51)','Cả hai pha đều bằng -0.51','Không có khác biệt giữa El Niño và La Niña'],
    'Bài báo chỉ ra r=-0.51 (p<0.01) ở các mùa hè sau El Niño, chỉ r=0.09 (không ý nghĩa) sau La Niña — thể hiện tính bất đối xứng trong tiến triển ENSO, nên phải tách riêng pha ENSO khi phân tích.',level=2,topic='ENSO-EASM')
B.add('Dữ liệu SST quan trắc dùng trong paper #1 là bộ nào, độ phân giải bao nhiêu?',
    'COBE-SST2 (Hirahara et al. 2014), lưới 1°×1°',['ERSSTv5, lưới 2°×2°','OISST, lưới 0.25°×0.25°','HadISST, lưới 1°×1°'],
    'Paper #1 dùng Centennial In Situ Observation-Based Estimates of SST version 2 (COBE-SST2; Hirahara et al. 2014) trên lưới 1°×1°.',level=1,topic='Dataset')
B.add('Dữ liệu tái phân tích hoàn lưu khí quyển dùng trong paper #1 là phiên bản nào?',
    'Ensemble mean của 20th Century Reanalysis version 3 (20CRv3)',['ERA5','JRA-55','MERRA-2'],
    'Paper #1 dùng ensemble mean của NOAA 20CRv3 cho hoàn lưu khí quyển, phối hợp với COBE-SST2 cho đại dương, trải dài 165 năm quan sát.',level=1,topic='Dataset')
B.add('4 nhóm pha tổ hợp PDO×Victoria Mode (VM) được dùng để phân tích composite trong paper #1 là gì?',
    'pPDO_pVM, pPDO_nVM, nPDO_pVM, nPDO_nVM',['pENSO_pVM, pENSO_nVM, nENSO_pVM, nENSO_nVM','pPDO_pENSO, pPDO_nENSO, nPDO_pENSO, nPDO_nENSO','Chỉ 2 nhóm: pPDO và nPDO'],
    'Bài báo chia dữ liệu thành 4 tổ hợp pha PDO (p/n) × VM (p/n) để kiểm tra quan hệ ENSO-EASM có bị điều biến bởi 2 dao động thập kỷ này không (Hình 1-8 của bài).',level=1,topic='Composite')
B.add('Phương pháp kiểm định ý nghĩa thống kê cho hệ số tương quan/hồi quy trong paper #1 dựa trên nguyên tắc nào?',
    'Kiểm định t hai phía, điều chỉnh số bậc tự do hiệu dụng N_eff theo tự tương quan trễ-1 (Bretherton et al. 1999)',['Kiểm định Mann-Kendall không tham số','Bootstrap 1000 lần không điều chỉnh tự tương quan','Kiểm định chi-bình phương trên bảng tần suất'],
    'Paper #1 dùng t-test hai phía với N_eff tính theo Bretherton et al. (1999), xét tự tương quan trễ-1 của cả 2 biến x,y — cách chuẩn để tránh phóng đại ý nghĩa khi dữ liệu khí hậu có tương quan thời gian.',level=2,topic='Statistics')
B.add('Victoria Mode (VM), giống PDO, được mô tả trong paper #1 có vai trò gì đối với tín hiệu khí quyển ngoại nhiệt đới?',
    'Đóng vai trò "cầu nối đại dương" (ocean bridge), truyền tải biến động khí quyển ngoại nhiệt đới vào vùng nhiệt đới',['Chỉ ảnh hưởng tới nhiệt độ bề mặt đất liền Trung Quốc','Không có vai trò vật lý, chỉ là chỉ số thống kê thuần','Chặn hoàn toàn tương tác ENSO-gió mùa'],
    'Theo bài báo, VM tương tự PDO, có thể hoạt động như "ocean bridge" truyền biến động ngoại nhiệt đới Thái Bình Dương vào vùng nhiệt đới, từ đó điều biến quan hệ ENSO-EASM.',level=2,topic='VM-PDO')
B.add('Ngưỡng dùng để xác định năm El Niño/La Niña trong paper #1 (dựa trên chỉ số ENSO) là gì?',
    '±0.5 (chuẩn hoá)',['±1.0','±1.5','±0.25'],
    'Paper #1 xác định El Niño và La Niña bằng ngưỡng ±0.5 trên chỉ số ENSO đã chuẩn hoá — ngưỡng phổ biến trong nhiều nghiên cứu ENSO.',level=1,topic='ENSO-EASM')
B.add('Paper #1 dùng dữ liệu mô phỏng mô hình nào để đối chiếu (so sánh quan trắc vs mô hình) cho quan hệ ENSO-EASM-PDO-VM?',
    'CESM2, ensemble 10 thành viên (CMIP5-class large ensemble)',['CMIP6 multi-model ensemble 30 mô hình','WRF khu vực độ phân giải cao','Chỉ dùng mô hình thống kê tuyến tính, không có mô hình động lực'],
    'Bài báo đối chiếu kết quả quan trắc với mô phỏng CESM2 10-member ensemble để kiểm tra tính bền vững của cơ chế điều biến PDO/VM trong mô hình động lực, không chỉ dựa vào thống kê quan trắc.',level=2,topic='Model')
# ---- kiến thức nền khí hậu (giáo trình Hartmann/kiến thức chuẩn, không trích trực tiếp số liệu bài báo) ----
B.add('Phản hồi Bjerknes (Bjerknes feedback) trong động lực ENSO mô tả cơ chế khuếch đại nào?',
    'SST ấm phía đông → yếu gió Tín phong → giảm trồi nước lạnh → SST ấm hơn (vòng khuếch đại dương-khí quyển)',['Gió mùa mùa hè mạnh lên làm giảm nhiệt độ đại dương','Băng cực tan làm tăng mực nước biển toàn cầu','Áp suất khí quyển tăng tuyến tính theo vĩ độ'],
    'Bjerknes feedback: SSTA dương ở Đông Thái Bình Dương làm yếu gió Tín phong (do giảm gradient áp suất Walker), gió yếu lại giảm trồi nước lạnh (upwelling), khiến SST ấm thêm — vòng phản hồi dương là lõi vật lý của ENSO.',level=1,topic='ENSO-theory')
B.add('Hoàn lưu Walker là hoàn lưu khí quyển theo hướng nào, liên kết vùng nào của Thái Bình Dương?',
    'Hoàn lưu theo chiều đông-tây (zonal) dọc xích đạo Thái Bình Dương, liên kết đối lưu Tây Thái Bình Dương ấm với giáng khí Đông Thái Bình Dương lạnh',['Hoàn lưu theo chiều bắc-nam (meridional) giữa 2 cực','Hoàn lưu chỉ tồn tại trong lớp biên khí quyển dưới 1km','Hoàn lưu đối lưu thẳng đứng không liên quan SST'],
    'Hoàn lưu Walker là vòng hoàn lưu đông-tây dọc xích đạo: không khí bốc lên ở vùng ấm/đối lưu mạnh (Tây TBD, Indonesia), di chuyển trên cao về phía đông, giáng xuống ở Đông TBD lạnh hơn, rồi gió Tín phong bề mặt thổi về tây khép vòng.',level=1,topic='ENSO-theory')
B.add('WNPAAC (Western North Pacific Anomalous Anticyclone) thường xuất hiện ở pha nào của ENSO và ảnh hưởng gì tới EASM?',
    'Xuất hiện ở mùa hè sau El Niño (decaying phase), gây hoàn lưu nghịch đảo bất thường làm suy yếu gió mùa hè Đông Á',['Chỉ xuất hiện độc lập với ENSO, không liên quan El Niño/La Niña','Luôn làm MẠNH gió mùa hè Đông Á bất kể pha ENSO','Chỉ ảnh hưởng tới Nam Bán cầu'],
    'WNPAAC là hoàn lưu nghịch đảo (anticyclonic) bất thường ở Tây Bắc Thái Bình Dương, thường hình thành mùa hè sau El Niño (decaying El Niño summer), góp phần gây EASMI âm (gió mùa yếu) — cơ chế được paper #1 kế thừa từ các nghiên cứu trước (Wang et al.).',level=2,topic='Teleconnection')
B.add('Hiệu ứng "IPOC" (Indo-western Pacific Ocean Capacitor) mô tả điều gì?',
    'Ấn Độ Dương tích trữ (hoạt động như "tụ điện") nhiệt từ El Niño và giải phóng chậm, kéo dài ảnh hưởng của El Niño sang mùa hè năm sau dù El Niño đã suy yếu ở Thái Bình Dương',['Ấn Độ Dương không có vai trò gì trong điều biến gió mùa','IPOC là hiện tượng chỉ xảy ra ở Đại Tây Dương','IPOC mô tả dòng điện đại dương tốc độ cao'],
    'Cơ chế IPOC (Xie et al. 2009): sau El Niño, SST ấm lan sang Ấn Độ Dương và được "tích trữ" (capacitor effect), duy trì ảnh hưởng ấm sang hè năm sau dù ENSO ở Thái Bình Dương đã trung hoà — một trong các con đường ENSO ảnh hưởng EASM mùa hè sau El Niño.',level=3,topic='Teleconnection')
B.add('Phản hồi WES (Wind-Evaporation-SST feedback) hoạt động theo chiều nào?',
    'Gió yếu → giảm bốc hơi/làm lạnh bề mặt → SST ấm hơn → duy trì/khuếch đại dị thường gió-SST ban đầu',['Gió mạnh luôn làm giảm SST không có vòng phản hồi','WES chỉ xảy ra ở vùng cực','Chỉ liên quan tới lượng mưa, không liên quan gió hay SST'],
    'WES feedback: gió bề mặt yếu đi làm giảm bốc hơi (evaporation) và giảm làm lạnh cơ học bề mặt biển, khiến SST ấm hơn; SST ấm lại có xu hướng duy trì gió yếu — một phản hồi dương quan trọng ở vùng nhiệt đới ngoài xích đạo (vd Bắc Ấn Độ Dương, liên quan IPOC).',level=3,topic='Teleconnection')
B.add('Đáp ứng Matsuno-Gill là mô hình lý thuyết mô tả điều gì?',
    'Đáp ứng hoàn lưu khí quyển nhiệt đới (gió, áp suất) đối với một nguồn nhiệt đối lưu định xứ, gồm cấu trúc sóng Kelvin phía đông và Rossby phía tây nguồn nhiệt',['Mô hình tan băng ở 2 cực','Phương trình trạng thái khí lý tưởng cho khí quyển','Mô hình lan truyền sóng âm trong đại dương'],
    'Mô hình Matsuno (1966)-Gill (1980): một nguồn nhiệt đối lưu định xứ ở xích đạo kích thích đáp ứng hoàn lưu bất đối xứng đông-tây — sóng Kelvin xích đạo lan về đông, cặp xoáy Rossby lan về tây — khung lý thuyết chuẩn để giải thích teleconnection nhiệt đới do ENSO gây ra.',level=3,topic='Teleconnection')
B.add('PDO (Pacific Decadal Oscillation) khác ENSO chủ yếu ở điểm nào?',
    'PDO là dao động với thang thời gian thập kỷ-đa thập kỷ (10-30 năm), còn ENSO có thang thời gian liên năm (2-7 năm)',['PDO chỉ xảy ra ở Nam Bán cầu, ENSO chỉ ở Bắc Bán cầu','PDO không liên quan gì tới SST Thái Bình Dương','PDO và ENSO là cùng một hiện tượng, chỉ khác tên gọi'],
    'PDO là mode biến động khí hậu thập kỷ-đa thập kỷ của SST Bắc Thái Bình Dương (pattern tương tự ENSO nhưng chậm hơn nhiều, Mantua et al. 1997), khác về thang thời gian so với ENSO liên-năm — đây là lý do paper #1 cần tách riêng pha PDO khi phân tích quan hệ ENSO-EASM liên năm.',level=1,topic='VM-PDO')
B.add('Hoàn lưu chung khí quyển (atmospheric general circulation) ở vùng nhiệt đới được duy trì chủ yếu bởi quá trình nào?',
    'Đối lưu ẩm sâu (deep moist convection) giải phóng nhiệt ngưng kết, là nguồn năng lượng chính cho hoàn lưu Hadley và Walker',['Sự chênh lệch áp suất do thuỷ triều','Dòng chảy đại dương sâu (thermohaline) duy nhất','Lực Coriolis tác động độc lập không cần nguồn nhiệt'],
    'Theo Hartmann (Global Physical Climatology), hoàn lưu nhiệt đới (Hadley, Walker) chủ yếu được "cấp năng lượng" bởi giải phóng nhiệt ẩn trong đối lưu sâu ở vùng đối lưu mạnh (ITCZ, Tây TBD ấm) — khác với vùng cực nơi cân bằng xạ chiếm ưu thế hơn.',level=2,topic='Climatology-nen-tang')
B.add('Theo Ding (1994, "Monsoon over China"), gió mùa hè Đông Á về cơ bản là kết quả của sự tương phản nhiệt nào?',
    'Tương phản nhiệt độ/áp suất giữa lục địa châu Á nóng lên nhanh và Thái Bình Dương/Ấn Độ Dương lạnh hơn vào mùa hè, tạo gradient áp suất hướng vào lục địa',['Tương phản nhiệt giữa Bắc Cực và Nam Cực','Chênh lệch độ cao giữa cao nguyên Tây Tạng và mực nước biển là nguyên nhân duy nhất','Không liên quan tới nhiệt độ, chỉ do lực Coriolis'],
    'Gió mùa cổ điển (kinh điển, Ding 1994) là hệ quả của tương phản nhiệt lục địa-đại dương theo mùa: mùa hè lục địa châu Á nóng nhanh hơn đại dương lân cận, tạo vùng áp thấp lục địa hút gió ẩm từ biển vào — đây là cơ chế nền mà các nghiên cứu hiện đại như paper #1 thêm lớp điều biến ENSO/PDO/VM lên trên.',level=1,topic='Monsoon-nen-tang')

B.add('Trong bối cảnh dự án này, vì sao chuỗi PDO/ENSO/EASMI 165 năm (COBE-SST2+20CRv3) là bài toán phù hợp để thử nghiệm QRC (Quantum Reservoir Computing) hơn là QNN phân loại không gian?',
    'Vì đây là bài toán time-series có nhớ dài hạn (teleconnection kéo dài nhiều mùa) và tính chaotic/phi tuyến — đúng đặc tính QRC khai thác (fading memory tự nhiên của reservoir), không phải bài toán phân loại không gian tĩnh',['Vì dữ liệu có dạng ảnh 2 chiều cần CNN','Vì QRC chỉ hoạt động được với dữ liệu phân loại nhị phân','Vì EASMI là biến rời rạc không có cấu trúc thời gian'],
    'Theo heuristic phân loại quantum method (đã dùng trong skill nghiên cứu QML): time-series có nhớ ngắn/dài hạn, phi tuyến/chaotic → QRC phù hợp hơn QNN/hybrid CNN-QNN (dành cho phân loại không gian tĩnh). Chuỗi PDO/ENSO/EASMI đúng dạng time-series teleconnection đa thang thời gian.',level=2,topic='Lien-he-QRC')
B.add('"Composite analysis" theo 4 tổ hợp pha PDO×VM trong paper #1 có thể gợi ý cấu trúc nào khi thiết kế reservoir QRC cho chuỗi ENSO-EASM?',
    'Có thể dùng cấu trúc "explicit register" mã hoá pha PDO/VM hiện tại (ngắn hạn, hay thay đổi) và "quantum memory register" lưu lịch sử ENSO dài hạn hơn — tương tự phân chia explicit/memory register trong paper QRC spin-chain',['Không có liên hệ nào giữa 2 bài báo','Phải bỏ hoàn toàn thông tin PDO/VM khi đưa vào QRC','Chỉ dùng được nếu chuyển toàn bộ dữ liệu sang ảnh vệ tinh'],
    'Đây là ý tưởng thiết kế mở rộng (ghi trong NOTE_hieu_va_mo_rong_QRC.md): vì paper #1 đã chứng minh quan hệ ENSO-EASM bị điều biến bởi pha PDO/VM (thang thời gian khác nhau), kiến trúc QRC có explicit register (ngắn hạn) + quantum memory register (dài hạn, không reset) của paper QRC là một ẩn dụ tự nhiên để mã hoá đúng cấu trúc đa thang thời gian này.',level=3,topic='Lien-he-QRC')

print('M1 added:',len(B.items))
balance_length(B.items)
a=audit(B.items)
print('AUDIT (after balance):',a)

parts=[
 dict(title='Lịch sử & nền tảng khí hậu nhiệt đới',bullets=['Hoàn lưu Walker & Bjerknes feedback','Matsuno-Gill response','PDO vs ENSO: thang thời gian'],slides=[
   sl(formula('Phản hồi Bjerknes (mô tả định tính)','SSTA(Đông TBD)↑ → Gió Tín phong↓ → Upwelling↓ → SSTA↑ (vòng khuếch đại)',
      [('SSTA','dị thường nhiệt độ mặt biển'),('Upwelling','trồi nước lạnh từ sâu')])
    +'<p>Đây là lõi vật lý của ENSO: một vòng phản hồi dương giữa đại dương và khí quyển dọc xích đạo Thái Bình Dương.</p>',
    'PHẦN 1 · Nền tảng','Hoàn lưu Walker và phản hồi Bjerknes',
    explain='Khi nước biển phía đông Thái Bình Dương ấm lên bất thường, gió thổi từ đông sang tây (gió Tín phong) yếu đi. Gió yếu thì ít đẩy nước lạnh từ sâu lên mặt (upwelling), nên nước mặt lại ấm thêm — một vòng tự khuếch đại, đó là lý do El Niño một khi bắt đầu thường tự lớn lên.'),
   sl(table(['Hiện tượng','Thang thời gian','Vùng trung tâm'],
      [['ENSO','2-7 năm','Xích đạo Thái Bình Dương'],['PDO','10-30 năm','Bắc Thái Bình Dương'],['Victoria Mode (VM)','Đa năm-thập kỷ','Bắc Thái Bình Dương, liên quan PDO'],['EASM (gió mùa hè Đông Á)','Theo mùa (JJA) + biến động liên năm','Đông Á, Tây Bắc Thái Bình Dương']]),
    'PHẦN 1 · Nền tảng','So sánh thang thời gian: ENSO, PDO, VM, EASM'),
 ]),
 dict(title='Teleconnection ENSO → Đông Á',bullets=['WNPAAC','IPOC','WES feedback'],slides=[
   sl(callout('info','WNPAAC (Western North Pacific Anomalous Anticyclone)','Hoàn lưu nghịch đảo bất thường ở Tây Bắc Thái Bình Dương, hình thành điển hình vào mùa hè SAU El Niño (decaying phase) — một trong các cơ chế chính khiến El Niño để lại dấu ấn làm suy yếu EASM mùa hè năm sau.')
    +callout('info','IPOC (Indo-western Pacific Ocean Capacitor)','Ấn Độ Dương "tích trữ" nhiệt ấm từ El Niño và giải phóng chậm, qua đó kéo dài ảnh hưởng El Niño sang mùa hè năm sau dù tín hiệu ở Thái Bình Dương đã suy yếu (Xie et al. 2009).'),
    'PHẦN 2 · Teleconnection','Hai con đường chính: WNPAAC và IPOC',
    explain='Hiểu đơn giản: El Niño mùa đông không "tắt" ngay khi hết mùa đông — nó để lại 2 "dư chấn" mùa hè năm sau: (1) một xoáy khí nghịch ở Tây Bắc Thái Bình Dương (WNPAAC) làm gió mùa yếu đi, và (2) hơi ấm "trữ" trong Ấn Độ Dương tiếp tục ảnh hưởng xa hơn về thời gian.'),
   sl(formula('EASMI (Wang & Fan 1999)','EASMI = chuẩn hoá[ U850(5-15°N,90-130°E) − U850(22.5-32.5°N,110-140°E) ], tính cho JJA(0)',
      [('U850','gió vĩ hướng tại 850 hPa'),('EASMI<0','hoàn lưu nghịch đảo bất thường ⇒ gió mùa yếu')])
    +'<p>Paper #1 dùng chính xác định nghĩa này để đo cường độ EASM khi đối chiếu với Niño-3.4 mùa đông trước.</p>',
    'PHẦN 2 · Teleconnection','Định nghĩa EASMI dùng trong paper #1'),
 ]),
 dict(title='Kết quả chính paper #1: PDO/VM điều biến quan hệ ENSO-EASM',bullets=['Số liệu 165 năm','4 tổ hợp pha PDO×VM','Bất đối xứng El Niño/La Niña'],slides=[
   sl(table(['Thống kê','Giá trị','Ý nghĩa'],
      [['Tương quan EASMI-Niño3.4, toàn bộ 165 năm','-0.28 (p<0.01)','Quan hệ ENSO-EASM nghịch, có ý nghĩa tổng thể'],
       ['Tương quan, chỉ mùa hè sau El Niño','-0.51 (p<0.01)','Quan hệ mạnh hơn nhiều sau El Niño'],
       ['Tương quan, chỉ mùa hè sau La Niña','0.09 (không ý nghĩa)','Hầu như không có quan hệ sau La Niña']]),
    'PHẦN 3 · Kết quả chính','Bất đối xứng El Niño vs La Niña (số liệu thật từ paper #1)',
    explain='Đây là phát hiện thú vị: nếu chỉ nhìn số liệu trộn cả El Niño và La Niña, quan hệ ENSO-gió mùa có vẻ yếu (-0.28). Nhưng tách riêng El Niño thì quan hệ rất mạnh (-0.51) — còn La Niña gần như không để lại dấu ấn gì rõ. Paper #1 còn đi xa hơn: tách tiếp theo pha PDO/VM mới thấy đầy đủ bức tranh.'),
   sl(ul(['Dữ liệu: COBE-SST2 (1°×1°, Hirahara 2014) + 20CRv3 ensemble mean, 165 năm quan sát','4 nhóm composite: pPDO_pVM, pPDO_nVM, nPDO_pVM, nPDO_nVM','Đối chiếu bằng CESM2, 10-member ensemble (kiểm tra cơ chế có bền vững trong mô hình động lực không)','Kiểm định: t-test 2 phía, N_eff theo Bretherton et al. (1999)']),
    'PHẦN 3 · Kết quả chính','Phương pháp & dữ liệu (tóm tắt để tái tạo lại)',
    explain='Đây là danh sách những gì cần nếu muốn tự tái tạo lại composite analysis của bài báo bằng Python, bước đầu tiên của lộ trình phát triển QRC.'),
   sl(diag('../../figures/m1_m5_enso/fig2_composite_pdo_vm.png','Fig. 2, Nguyen-Le & Ngo-Duc 2025, J. Climate','4 tổ hợp pha PDO×VM: pPDO_pVM, pPDO_nVM, nPDO_pVM, nPDO_nVM — hồi quy SSTA/gió MAM(0) theo Niño-3.4 NDJ(−1/0)'),
    'PHẦN 3 · Kết quả chính','Bản đồ gốc: phản hồi SST/gió theo 4 tổ hợp pha PDO×VM'),
 ]),
 dict(title='Vì sao chuỗi ENSO-EASM hợp với QRC',bullets=['Time-series chaotic vs spatial','Explicit vs memory register','Hướng mở rộng cụ thể'],slides=[
   sl(table(['Dạng bài toán','Ví dụ','Method quantum phù hợp'],
      [['Time-series, nhớ dài hạn, phi tuyến/chaotic','Chuỗi PDO/ENSO/EASMI liên năm-thập kỷ (paper #1)','QRC (reservoir cố định + readout tuyến tính)'],
       ['Phân loại không gian tĩnh','Bản đồ nguy cơ lũ/sạt lở từ ảnh vệ tinh','QNN/hybrid CNN-QNN (không phải QRC)']]),
    'PHẦN 4 · Liên hệ QRC','Heuristic phân loại: vì sao chọn QRC cho bài toán này',
    explain='Nguyên tắc chung: nếu bài toán là "dự đoán số tiếp theo trong 1 chuỗi có trí nhớ" thì QRC phù hợp; nếu là "phân loại 1 bức ảnh/bản đồ tĩnh" thì QRC không có gì để khai thác (không có chiều thời gian), nên cần quantum method khác.'),
   sl(callout('info','Ý tưởng thiết kế (NOTE_hieu_va_mo_rong_QRC.md)','Explicit register ↔ pha PDO/VM hiện tại (thay đổi thập kỷ-niên, "làm mới" theo từng điểm thời gian lớn); Quantum memory register ↔ lịch sử ENSO tích lũy nhiều mùa trước, không bị reset — ánh xạ trực tiếp từ kiến trúc 2 vùng qubit của paper QRC spin-chain sang cấu trúc đa thang thời gian PDO/VM/ENSO.')
    +callout('warn','Việc còn phải làm (chưa chạy thật)','Thiết kế này mới ở mức ý tưởng/giấy — chưa code, chưa chạy benchmark, chưa so sánh với baseline LSTM/ARIMA. Đây là input cho Module 4 (ứng dụng paper #1 + mở rộng QRC).'),
    'PHẦN 4 · Liên hệ QRC','Ánh xạ kiến trúc QRC sang bài toán ENSO-EASM'),
 ]),
 dict(title='References',bullets=['Hình đã dùng trong module này'],slides=[
   sl(ul(['Fig. 2 — Nguyen-Le, D. & Ngo-Duc, T. (2025). "Modulation of PDO and the Victoria Mode on the ENSO–East Asian Summer Monsoon Relationship." <i>Journal of Climate</i>, 38(20), 5655–5670. DOI: 10.1175/JCLI-D-24-0626.1. Trang 5657 (trang 3 của file PDF).']),
    'PHẦN 5 · References','Nguồn hình ảnh'),
 ]),
]

quiz=B.items
module_page('m1','01-nen-tang-enso-pdo-easm',
  title='M1 · Nền tảng ENSO-PDO-EASM',
  subtitle='Teleconnection ENSO-gió mùa hè Đông Á, cơ sở cho thiết kế QRC mở rộng paper #1',
  source=SRC, status=f'HOÀN CHỈNH — {len(quiz)} câu quiz bám sát nội dung đã đọc full-text',
  parts=parts, quiz_items=quiz,
  notes='<h2>Ghi chú</h2><p>Toàn bộ số liệu (tương quan, ngưỡng, định nghĩa EASMI, dataset) trích trực tiếp từ bản PDF full-text paper #1 đã verify (không suy diễn từ abstract). Phần lý thuyết nền (Bjerknes, Walker, Matsuno-Gill, WNPAAC, IPOC, WES) là kiến thức khí hậu học chuẩn (Hartmann; các review ENSO kinh điển), không trích số liệu riêng của paper #1.</p>',
  notebook_links=[('m1_verify_enso_easm.ipynb (verify N_eff Bretherton 1999 + công thức EASMI, đã chạy thật 0 lỗi)','../../notebooks/m1_verify_enso_easm.ipynb')])
print('Module 1 xong.')
