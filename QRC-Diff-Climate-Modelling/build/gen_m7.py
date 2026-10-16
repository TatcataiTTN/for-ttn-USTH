# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit
from sitelib import module_page

B=Bank('m7',seed=7)
SRC='08_The_He_Mo_Hinh_Thoi_Tiet/README.md + GiaiThich.md (8 thế hệ, verify demo.ipynb chạy thật). Dữ liệu thật dùng chung: NOAA OISST v2.1, vùng Biển Đông/SEA (5-25°N,100-120°E), 12 ngày đại diện năm 2020, tải qua AWS Open Data bucket noaa-cdr-sea-surface-temp-optimum-interpolation-pds.'

GENS=[('1','Thống kê/synoptic cổ điển','trước ~1950','Không giải phương trình vật lý: vẽ tay bản đồ synoptic + hồi quy thống kê/persistence trên lịch sử quan trắc','Không có cơ chế vật lý ràng buộc → thất bại hoàn toàn với hình thế chưa từng xảy ra trong lịch sử'),
 ('2','NWP nguyên thuỷ (Richardson→Charney)','1922→1950s','Giải trực tiếp phương trình nguyên thuỷ (Navier-Stokes xấp xỉ thuỷ tĩnh) bằng sai phân hữu hạn; Charney 1950 đơn giản hoá xuống mô hình barotropic 1 tầng để chạy ổn định trên ENIAC','Chỉ 1 tầng, miền nhỏ, không tham số hoá vật lý (mây/bức xạ/đối lưu) → không dự báo được thời tiết chi tiết'),
 ('3','General Circulation Models (GCM)','từ cuối 1950s (Phillips 1956)','Mở rộng NWP sang toàn cầu, nhiều tầng khí quyển, chạy dài hạn; dùng tham số hoá vật lý (parameterization) cho quá trình dưới lưới','Độ phân giải thô (~100-200km) → mất chi tiết vùng/đảo nhỏ, đặc biệt nghiêm trọng ở Đông Nam Á'),
 ('4','Coupled Earth System Model / CMIP3-6','CMIP1 1995 → CMIP6 nay','Ghép khí quyển+đại dương+băng+đất+carbon thành 1 Earth System Model, chạy ensemble đa mô hình theo kịch bản SSP chung để định lượng độ bất định cấu trúc mô hình','Vẫn thô như GCM (~100-250km) — ensemble đo được độ bất định nhưng KHÔNG giải quyết thiếu chi tiết không gian'),
 ('5','RCM / Dynamical Downscaling / CORDEX','từ 1990s, chuẩn hoá qua CORDEX (2009)','Lấy biên (lateral boundary) từ 1 GCM thô, giải lại đầy đủ phương trình động lực trên lưới mịn hơn CHỈ trong 1 vùng; spectral nudging giữ hoàn lưu lớn khớp GCM mẹ','Tốn HPC rất lớn — bài #2 cần 3 RCM×11 GCM×8 cấu hình = 62 lượt chạy, hàng nghìn giờ CPU mỗi lượt'),
 ('6','Statistical Downscaling / Bias Correction','song song RCM từ 1990s','Học quan hệ thống kê giữa phân phối mô hình thô và quan trắc thật; kỹ thuật kinh điển: Quantile Mapping (map theo quantile thực nghiệm, không giả định dạng phân phối)','Rẻ hơn RCM rất nhiều nhưng giả định quan hệ thống kê ổn định theo thời gian (stationarity) — có thể sai khi khí hậu đổi cấu trúc'),
 ('7','ML Data-Driven Weather (GraphCast/FourCastNet/Pangu)','2022-nay','Học end-to-end từ dữ liệu reanalysis (ERA5) bằng mạng neural lớn (GNN/Fourier neural operator/transformer), không giải phương trình động lực tường minh; inference nhanh hơn NWP vật lý ~1000x','Cần dữ liệu huấn luyện khổng lồ + hàng trăm triệu tham số; khó đảm bảo bảo toàn vật lý ở trường hợp cực đoan ngoài phân phối huấn luyện'),
 ('8','QRC & Drifting (hướng dự án)','2026, chưa trưởng thành','QRC: thay reservoir cổ điển bằng tiến hoá Hamiltonian lượng tử, tránh vanishing-gradient vì reservoir không huấn luyện gradient. Drifting: học trường drift tiến hoá theo thời gian HUẤN LUYỆN để sinh mẫu 1 bước (1-NFE)','Cả 2 chưa có benchmark trên dữ liệu khí hậu thật (QRC gốc: NARMA-10/Santa Fe; Drifting gốc: ảnh ImageNet) — đây chính là khoảng trống nghiên cứu dự án nhắm tới')]

for n,name,period,principle,limit in GENS:
    B.add(f'Thế hệ {n} ("{name}") hoạt động theo nguyên lý nào?',
        principle,
        [g[3] for g in GENS if g[0]!=n][:3],
        f'Thế hệ {n} ({period}): {principle}. Hạn chế thúc đẩy thế hệ sau: {limit}',level=1,topic=f'Gen{n}')
    B.add(f'Hạn chế cốt lõi nào của thế hệ {n} ("{name}") đã thúc đẩy thế hệ tiếp theo ra đời?',
        limit,
        [g[4] for g in GENS if g[0]!=n][:3],
        f'Theo README 08_The_He_Mo_Hinh_Thoi_Tiet: {limit}.',level=2,topic=f'Gen{n}')

B.add('Dữ liệu SST thật dùng chung cho demo của 8 thế hệ là bộ nào, vùng nào?',
    'NOAA OISST v2.1, vùng Biển Đông/SEA (5-25°N, 100-120°E), 12 ngày đại diện năm 2020',
    ['ERA5, toàn cầu, 40 năm 1980-2020','COBE-SST2, vùng Bắc Thái Bình Dương, 165 năm','CMIP6 ensemble thật, toàn cầu, 1960-2099'],
    'README 08_The_He_Mo_Hinh_Thoi_Tiet ghi rõ: NOAA OISST v2.1, 12 tháng năm 2020 (1 ngày đại diện/tháng), vùng Biển Đông/SEA, tải qua AWS Open Data bucket công khai.',level=1,topic='Data')
B.add('Vì sao demo thế hệ 4 (CMIP Coupled ESM) KHÔNG dùng dữ liệu CMIP6 thật?',
    'Vì ESGF (nơi phân phối CMIP6) cần đăng ký/API phức tạp, không khả thi trong phạm vi demo nhanh — notebook dùng nhiễu thống kê (bootstrap+Gaussian) trên nền SST thật để minh hoạ khái niệm ensemble spread, có ghi rõ cảnh báo ⚠️',
    ['Vì CMIP6 không tồn tại dữ liệu công khai nào','Vì CMIP6 chỉ có dữ liệu cho Bắc Mỹ','Vì notebook không cho phép dùng dữ liệu NetCDF'],
    'Đây là một flag minh bạch quan trọng ghi trong GiaiThich.md thế hệ 4: KHÔNG phải dữ liệu CMIP6 thật, chỉ là minh hoạ khái niệm ensemble bằng nhiễu thống kê giả lập trên nền 1 chuỗi SST thật.',level=2,topic='Flag-minh-bach')
B.add('Vì sao demo thế hệ 5 (RCM/CORDEX) không chạy lại RegCM4/CCAM/HadREM3 thật?',
    'Vì chạy RCM thật cần tài nguyên siêu tính toán (HPC) rất lớn — minh hoạ sư phạm bằng nội suy + cấu trúc small-scale lấy từ OISST độ phân giải cao thật thay thế',
    ['Vì RegCM4/CCAM/HadREM3 là phần mềm đóng, không thể cài đặt','Vì RCM chỉ chạy được trên Windows','Vì bài báo #2 không công bố mã nguồn nào'],
    'GiaiThich.md thế hệ 5 ghi rõ: không chạy lại 3 mô hình RCM thật (cần HPC); thay vào đó minh hoạ bằng coarsen+nội suy+thêm cấu trúc small-scale từ OISST thật, đo RMSE để minh hoạ hiệu quả của downscaling.',level=2,topic='Flag-minh-bach')
B.add('Vì sao demo thế hệ 8 (QRC) dùng Echo State Network cổ điển thay vì mạch lượng tử qiskit thật?',
    'Vì cần nhiều thời gian hơn để debug đúng kiến trúc spin-chain lượng tử theo paper — ESN minh hoạ đúng NGUYÊN LÝ chung của reservoir computing (fixed reservoir + readout tuyến tính train bằng ridge regression closed-form), không mô phỏng mạch lượng tử thật',
    ['Vì qiskit không tồn tại trên Python','Vì ESN cho kết quả tốt hơn QRC thật nên được ưu tiên dùng luôn','Vì paper QRC gốc cũng chỉ dùng ESN, không có mạch lượng tử nào'],
    'GiaiThich.md thế hệ 8 nêu rõ: demo dùng ESN cổ điển (fixed random reservoir, spectral radius <1, readout ridge regression) để minh hoạ nguyên lý RC chung — đây là một sự đơn giản hoá có chủ đích, có ghi flag, KHÔNG phải mạch lượng tử qiskit theo đúng Hamiltonian MFIM của paper QRC.',level=2,topic='Flag-minh-bach')
B.add('Quantile Mapping (thế hệ 6) hoạt động theo nguyên tắc nào?',
    'Map từng giá trị mô hình theo đúng quantile của nó trong phân phối mô hình, sang giá trị tương ứng ở quantile đó trong phân phối quan trắc — dùng hàm phân phối tích luỹ thực nghiệm, không giả định dạng phân phối tham số',
    ['Cộng thêm 1 hằng số bias trung bình cố định vào mọi giá trị mô hình','Nhân mọi giá trị mô hình với 1 hệ số khuếch đại cố định duy nhất','Thay toàn bộ giá trị mô hình bằng trung bình của quan trắc'],
    'Quantile Mapping (phi tham số) là kỹ thuật bias-correction kinh điển nhất của thế hệ 6: khác với cộng/nhân hằng số đơn giản, nó map theo ĐÚNG VỊ TRÍ QUANTILE trong phân phối thực nghiệm, nên sửa được cả lệch trung bình và lệch hình dạng phân phối (variance, extremes).',level=2,topic='Gen6')
B.add('Điều kiện ổn định số CFL (Courant-Friedrichs-Lewy) mà Richardson 1922 đã vi phạm có dạng gì?',
    'U·Δt/Δx < 1 (tốc độ truyền tin số phải theo kịp tốc độ truyền tin vật lý)',
    ['Δt > Δx (bước thời gian phải lớn hơn bước không gian)','U = Δt·Δx (vận tốc bằng tích 2 bước lưới)','N > 2^k với N là số qubit (điều kiện lượng tử, không liên quan NWP)'],
    'CFL: U·Δt/Δx < 1 — nếu bước thời gian Δt quá lớn so với bước không gian Δx và tốc độ U, sơ đồ sai phân hữu hạn mất ổn định số (nhiễu khuếch đại vô hạn) — đúng lỗi Richardson 1922 gặp phải, mãi tới Charney 1950 mới sửa bằng đơn giản hoá mô hình.',level=3,topic='Gen2')

print('M7 added:',len(B.items))
print('AUDIT:',audit(B.items))

def gen_slide(n,name,period,principle,limit,nxt):
    return sl(formula(f'Thế hệ {n} — {name}',period,[('Nguyên lý',principle),('Hạn chế cốt lõi',limit),('Thúc đẩy ra đời',nxt)]),
        f'PHẦN {n} · 8 THẾ HỆ','Thế hệ {} — {}'.format(n,name))

NXT=['Richardson/Charney đề xuất tính trực tiếp từ phương trình vật lý thay vì ngoại suy thống kê','Cần mở rộng toàn cầu, nhiều tầng, chạy dài hạn → GCM',
     'Cần ghép đủ khí quyển-đại dương-băng-đất-carbon + ensemble đa mô hình → Coupled ESM/CMIP','Cần "downscale" về độ phân giải đủ chi tiết cho tác động địa phương → RCM/CORDEX',
     'Cần phương án rẻ hơn khi không có HPC đủ lớn → Statistical downscaling/bias correction','Cần học trực tiếp ánh xạ phức tạp hơn từ dữ liệu lớn (ERA5) → ML weather model',
     'QRC (tránh vanishing-gradient) + Drifting (sinh mẫu 1 bước) — hướng cân bằng tốc độ/dữ liệu/mở rộng khác','(hướng nghiên cứu hiện tại của dự án — chưa có thế hệ 9 xác định)']

parts=[]
for i,(n,name,period,principle,limit) in enumerate(GENS):
    parts.append(dict(title=f'Thế hệ {n}: {name}',bullets=[period,'Nguyên lý','Hạn chế → thế hệ sau'],
        slides=[gen_slide(n,name,period,principle,limit,NXT[i])]))

parts.append(dict(title='Minh bạch dữ liệu/mô hình trong demo',bullets=['Thật vs minh hoạ','Flags theo từng thế hệ'],slides=[
   sl(table(['Thế hệ','Dùng dữ liệu/mô hình gì trong demo.ipynb'],
      [['1,2,3,6,7,8 (phần dữ liệu)','SST thật OISST v2.1 2020, vùng Biển Đông/SEA — có áp phép toán thật (hồi quy, coarsen, quantile mapping, CNN toy, ESN) lên dữ liệu thật'],
       ['4 (CMIP ensemble)','⚠️ KHÔNG có CMIP6 thật — nhiễu thống kê giả lập (bootstrap+Gaussian) trên nền SST thật, do ESGF cần đăng ký phức tạp'],
       ['5 (RCM/CORDEX)','⚠️ KHÔNG chạy lại RegCM4/CCAM/HadREM3 thật (cần HPC) — minh hoạ bằng nội suy + cấu trúc small-scale từ OISST thật'],
       ['7 (ML weather)','CNN toy ~20 tham số (không phải GraphCast/Pangu hàng trăm triệu tham số) — nhưng huấn luyện THẬT, loss giảm thật, verify trong code'],
       ['8 (QRC/Drifting)','⚠️ ESN cổ điển thay mạch lượng tử qiskit thật; toy drift field (Gaussian-kernel) thay mạng neural Drifting đầy đủ']]),
    'PHẦN 9 · Minh bạch','Bảng tổng hợp: chỗ nào là dữ liệu/mô hình thật, chỗ nào là minh hoạ rút gọn',
    explain='Nguyên tắc tối thượng của toàn bộ hệ thống tự học này là KHÔNG bịa số liệu và KHÔNG che giấu phần rút gọn. Bảng này tồn tại để không ai đọc nhầm demo rút gọn thành kết quả nghiên cứu đầy đủ.'),
]))

quiz=B.items
module_page('m7','07-cac-the-he-mo-hinh-thoi-tiet',
  title='M7 · Các thế hệ mô hình thời tiết/khí hậu',
  subtitle='8 thế hệ: thống kê cổ điển → NWP → GCM → CMIP ESM → RCM/CORDEX → statistical downscaling → ML weather → QRC/Drifting',
  source=SRC, status=f'HOÀN CHỈNH — {len(quiz)} câu quiz, bám sát README + 8 file GiaiThich.md + flag minh bạch demo.ipynb',
  parts=parts, quiz_items=quiz,
  notes='<h2>Ghi chú</h2><p>Toàn bộ nguyên lý/giới hạn/lý do chuyển thế hệ trích trực tiếp từ 8 file GiaiThich.md (đã verify tồn tại, mỗi file 18-28 dòng, có demo.ipynb kèm theo đã chạy thật không lỗi theo khai báo của nguồn). Các cảnh báo "⚠️ KHÔNG phải dữ liệu/mô hình thật" được giữ nguyên, không lược bỏ, theo đúng yêu cầu minh bạch.</p>',
  notebook_links=[(f'{i:02d}_{n}.ipynb','../../notebooks/m7_the_he_mo_hinh/'+fn) for i,n,fn in [
    (1,'Thong_Ke_Co_Dien','01_Thong_Ke_Co_Dien.ipynb'),(2,'NWP_Nguyen_Thuy','02_NWP_Nguyen_Thuy.ipynb'),
    (3,'GCM','03_GCM.ipynb'),(4,'CMIP_Coupled_ESM','04_CMIP_Coupled_ESM.ipynb'),
    (5,'RCM_Dynamical_Downscaling','05_RCM_Dynamical_Downscaling.ipynb'),(6,'Statistical_Downscaling_BiasCorrection','06_Statistical_Downscaling_BiasCorrection.ipynb'),
    (7,'ML_Data_Driven_Weather','07_ML_Data_Driven_Weather.ipynb'),(8,'QRC_Drifting','08_QRC_Drifting.ipynb')]])
print('Module 7 xong.')
