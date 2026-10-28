# Đề cương ôn tập – Satellite Remote Sensing of Atmospheric Composition

Bộ tài liệu ôn thi gồm **đề cương 8 câu hỏi lý thuyết** (đáp án mẫu tiếng Anh + tóm tắt tiếng Việt), **1 đề thi mẫu có đáp án gợi ý**, toàn bộ **hình vẽ** và **mã nguồn** để tạo lại mọi thứ.

## Cấu trúc thư mục

```
Remote_Sensing_Study_Guide/
├── README.md                        ← file này
├── 01_De_cuong/
│   ├── De_cuong_Remote_Sensing_Atmosphere.docx   (25 trang, mở bằng Word để sửa)
│   └── De_cuong_Remote_Sensing_Atmosphere.pdf    (bản in / xem nhanh)
├── 02_De_thi_mau/
│   ├── De_thi_mau_Remote_Sensing.docx            (8 câu, 20 điểm, 120 phút + đáp án gợi ý)
│   └── De_thi_mau_Remote_Sensing.pdf
├── 03_Hinh/
│   ├── hinh_ve_bang_code/           18 hình PNG (170 dpi) vẽ bằng Python
│   └── anh_slide_bai_giang/         4 ảnh slide (đã thu nhỏ, dùng trong đề cương)
│       └── goc/                     4 ảnh gốc độ phân giải đầy đủ
└── 04_Code/
    ├── ve_hinh_1.py                 vẽ 7 hình sơ đồ cơ bản (f1–f7)
    ├── ve_hinh_2.py                 vẽ 11 hình đồ thị (f8–f18) + thu nhỏ ảnh slide
    ├── tao_de_cuong.js              tạo file Word đề cương
    ├── tao_de_thi_mau.js            tạo file Word đề thi mẫu
    ├── chay_tat_ca.sh               chạy lại toàn bộ (hình → đề cương → đề mẫu → PDF)
    ├── requirements.txt             thư viện Python cần cài
    └── package.json                 thư viện Node.js cần cài
```

## Nội dung đề cương (01_De_cuong)

Mỗi chương ứng với một câu hỏi, gồm: đề bài gốc → đáp án mẫu (tiếng Anh) → phương trình chính → hình minh họa → hộp **Exam checklist** (ý bắt buộc phải nêu) → hộp **Ý chính** (tóm tắt tiếng Việt).

| Chương | Chủ đề |
|---|---|
| 1 | Bể chứa (sink) và thời gian sống của chất ô nhiễm; đọc thời gian sống từ bản đồ vệ tinh |
| 2 | Tương tác ánh sáng – vật chất: hấp thụ, tán xạ, phát xạ, Beer–Lambert, phương trình truyền bức xạ |
| 3 | Đại lượng đo của cảm biến thụ động; truy hồi cột (DOAS, AMF) và profil (Optimal Estimation) |
| 4 | Hình học quan sát: nadir, limb, che khuất (occultation) – ưu và nhược điểm |
| 5 | Độ nhạy: ma trận averaging kernel, DOFS; trường hợp lý tưởng và thực tế (O₃ nadir) |
| 6 | Viễn thám aerosol thụ động: AOD, Ångström, ω₀…; so sánh với lidar (chủ động) |
| 7 | Các chế độ tán xạ: Rayleigh, Mie, quang hình; aerosol thô trong ánh sáng khả kiến |
| 8 | Xác định độ cao aerosol: hồng ngoại nhiệt và dải O₂ A (cận hồng ngoại) |
| Phụ lục | Bảng công thức và từ viết tắt |

## Danh sách hình (03_Hinh/hinh_ve_bang_code)

| File | Nội dung | Dùng ở câu |
|---|---|---|
| f1_lifetime.png | Thời gian sống và quy mô biến động không gian | 1 |
| f12_plume.png | Suy giảm NO₂ theo chiều gió → suy ra τ | 1 |
| f18_decay.png | Đường suy giảm e^(−t/τ) cho NO₂, SO₂, aerosol, CO, CH₄ | 1 |
| f2_interactions.png | Sơ đồ hấp thụ, tán xạ, phát xạ, Beer–Lambert | 2 |
| f8_planck.png | Đường cong Planck của Mặt Trời và Trái Đất | 2 |
| f11_phase.png | Hàm pha tán xạ (tính bằng lý thuyết Mie) | 2, 7 |
| f6_wf.png | Hàm trọng số theo độ cao | 3 |
| f13_doas.png | Nguyên lý DOAS | 3 |
| f3_geometries.png | Ba hình học quan sát nadir / limb / occultation | 4 |
| f15_tradeoff.png | So sánh độ phân giải ngang – thẳng đứng của các thiết bị | 4 |
| f4_avk.png | Averaging kernel lý tưởng và thực tế | 5 |
| f14_colavk.png | Kernel trung bình của cột theo độ cao | 5 |
| f9_angstrom.png | Phụ thuộc phổ của độ dày quang học (Rayleigh, Ångström) | 6 |
| f16_surface.png | Ảnh hưởng của bề mặt sáng/tối lên tín hiệu aerosol | 6 |
| f5_regimes.png | Các chế độ tán xạ theo thông số kích thước x | 7 |
| f10_mie_qext.png | Hiệu suất suy giảm Q_ext (tính bằng lý thuyết Mie) | 7 |
| f7_altitude.png | Nguyên lý đo độ cao aerosol (TIR và O₂ A-band) | 8 |
| f17_height_sens.png | Độ nhạy của tín hiệu theo độ cao lớp aerosol | 8 |

**Lưu ý về hình:** Planck và Mie (f8, f10, f11) được **tính từ phương trình thật**. Các hình khác là **sơ đồ minh họa** (có ghi "schematic" trên hình nếu cần) để hiểu nguyên lý và vẽ lại khi đi thi, không phải dữ liệu đo thật. Ảnh slide (s1–s4) là ảnh chụp bài giảng trên lớp.

## Tạo lại tài liệu (nếu muốn sửa nội dung)

Cần: Python 3, Node.js 18+, (tùy chọn) LibreOffice để xuất PDF.

```bash
cd Remote_Sensing_Study_Guide/04_Code
pip install -r requirements.txt
npm install
bash chay_tat_ca.sh
```

- Sửa nội dung đề cương: mở `tao_de_cuong.js`, tìm chương cần sửa (`// ---- Q1 ----` … `// ---- Q8 ----`).
- Sửa đề mẫu: sửa mảng `QUESTIONS` trong `tao_de_thi_mau.js`.
- Sửa hình: sửa `ve_hinh_1.py` hoặc `ve_hinh_2.py`, chạy lại script.
- Đường dẫn trong code là tương đối, nên có thể chuyển cả thư mục sang máy khác mà vẫn chạy được.

Khi mở file Word, nếu được hỏi **cập nhật trường (update fields)** thì chọn **Yes** để mục lục hiện ra.

## Ảnh từ Internet (chưa chèn được)

Môi trường làm việc chặn tải ảnh từ Wikimedia/NASA/ESA, nên chưa chèn được ảnh web. Các ảnh dùng tự do nên bổ sung thủ công:

- Phổ bức xạ Mặt Trời ở đỉnh khí quyển và mặt biển – Wikimedia Commons, CC BY-SA 3.0: https://commons.wikimedia.org/wiki/File:Solar_spectrum_en.svg
- Độ truyền qua của khí quyển theo bước sóng – NASA, public domain: https://commons.wikimedia.org/wiki/File:Atmospheric_electromagnetic_opacity.svg
- Bản đồ NO₂ TROPOMI – ESA: https://www.esa.int/ESA_Multimedia/Images/2018/07/Nitrogen_dioxide_from_Sentinel-5P
- Bản đồ AOD toàn cầu MODIS – NASA Earth Observatory: https://earthobservatory.nasa.gov/global-maps/MODAL2_M_AER_OD
