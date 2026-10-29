# Đề cương ôn tập – Satellite Remote Sensing of Atmospheric Composition (Version 2)

## Có gì mới trong v2

- **Phần A – Kiến thức nền** (lấy từ 7 slide bài giảng mới): phương trình truyền bức xạ dI/dl = −k_ext·I + J; cân bằng photon được/mất dọc tia nhìn; lớp khí không tán xạ (J = α·B, phương trình dạng tích phân, biên bề mặt với ε_s và albedo); độ dày quang học τ = σ·N·L (phổ liên tục và phổ vạch); độ rộng vạch Doppler/Lorentz/Voigt theo độ cao; nguyên lý DOAS (σ = σ_b + σ′).
- **Bố cục mới**: Phần A (kiến thức nền) → Phần B (8 câu hỏi, mở đầu bằng sơ đồ liên kết các câu) → Phần C (bảng công thức, từ viết tắt).
- **Mỗi câu có thêm 3 khối**: *Worked example* (ví dụ có số liệu), *Quick Q&A* (hỏi nhanh – đáp nhanh), *Liên tưởng* (cách nhớ bằng hình ảnh đời thường).
- **6 hình mới** (f19–f24) và **7 ảnh slide mới** (s5–s11).
- **Đề thi mẫu**: thêm 2 câu về Phần A → 10 câu, 25 điểm.

Bộ tài liệu ôn thi gồm **đề cương 8 câu hỏi lý thuyết** (đáp án mẫu tiếng Anh + tóm tắt tiếng Việt), **1 đề thi mẫu có đáp án gợi ý**, toàn bộ **hình vẽ** và **mã nguồn** để tạo lại mọi thứ.

## Cấu trúc thư mục

```
Remote_Sensing_Study_Guide/
├── README.md                        ← file này
├── 01_De_cuong/
│   ├── De_cuong_Remote_Sensing_Atmosphere_v2.docx   (40 trang, mở bằng Word để sửa)
│   └── De_cuong_Remote_Sensing_Atmosphere_v2.pdf    (bản in / xem nhanh)
├── 02_De_thi_mau/
│   ├── De_thi_mau_Remote_Sensing_v2.docx         (10 câu, 25 điểm, 120 phút + đáp án gợi ý)
│   └── De_thi_mau_Remote_Sensing_v2.pdf
├── 03_Hinh/
│   ├── hinh_ve_bang_code/           24 hình PNG (170 dpi) vẽ bằng Python
│   └── anh_slide_bai_giang/         11 ảnh slide (đã thu nhỏ, dùng trong đề cương)
│       └── goc/                     11 ảnh gốc độ phân giải đầy đủ
└── 04_Code/
    ├── ve_hinh_1.py                 vẽ 7 hình sơ đồ cơ bản (f1–f7)
    ├── ve_hinh_2.py                 vẽ 11 hình đồ thị (f8–f18) + thu nhỏ ảnh slide s1–s4
    ├── ve_hinh_3.py                 (v2) vẽ 6 hình Phần A (f19–f24) + thu nhỏ ảnh slide s5–s11
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
| Phần A | Kiến thức nền: phương trình truyền bức xạ, cân bằng photon, lớp khí, độ dày quang học, độ rộng vạch, DOAS |
| Phần C | Bảng công thức và từ viết tắt |

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
| f19_budget.png | Cân bằng photon: được (phản xạ, tán xạ, phát xạ) / mất (hấp thụ, tán xạ ra) | A.2 |
| f20_line_widths.png | Độ rộng vạch Doppler, Lorentz, Voigt theo độ cao (tính từ công thức thật) | A.5 |
| f21_doas_principle.png | Nguyên lý DOAS: I₀, I′₀, D, σ_b và σ′ | A.6 |
| f22_rte_layers.png | Phương trình truyền bức xạ dạng tích phân cho lớp khí | A.3 |
| f23_concept_map.png | Sơ đồ liên kết 8 câu hỏi và Phần A | Mở đầu Phần B |
| f24_o3_transmission.png | Ví dụ: độ truyền qua ozone ở 4 bước sóng UV | 2 |

**Lưu ý về hình:** Planck, Mie và độ rộng vạch (f8, f10, f11, f20) được **tính từ phương trình thật**. Các hình khác là **sơ đồ minh họa** (có ghi "schematic" trên hình nếu cần) để hiểu nguyên lý và vẽ lại khi đi thi, không phải dữ liệu đo thật. Ảnh slide (s1–s4) là ảnh chụp bài giảng trên lớp.

## Ảnh slide bài giảng (03_Hinh/anh_slide_bai_giang)

| File | Nội dung | Dùng ở |
|---|---|---|
| s1_gome.jpg | Phổ GOME: bức xạ Mặt Trời và bức xạ Trái Đất | Câu 3 |
| s2_tropomi.jpg | Phổ TROPOMI một pixel, kênh VIIRS | Câu 3 |
| s3_wavelengths.jpg | Chọn bước sóng cho từng chất | Câu 3 |
| s4_solar.jpg | Bức xạ Mặt Trời ở đỉnh khí quyển và mặt biển | Câu 2 |
| s5_rte_equation.jpg | Phương trình truyền bức xạ (1/5) | A.1 |
| s6_gains_losses.jpg | Tương tác ánh sáng – vật chất: được / mất | A.2 |
| s7_rte_gas_layer.jpg | Phương trình truyền bức xạ cho lớp khí (2/5) | A.3 |
| s8_optical_depth.jpg | Độ dày quang học: phổ liên tục và phổ vạch (5/5) | A.4 |
| s9_blackboard.jpg | Bảng đen: t = e^(−τ), τ = σ·N·l | A.4 |
| s10_line_widths.jpg | Độ rộng vạch theo độ cao, phổ limb | A.5 |
| s11_doas.jpg | DOAS | A.6 |

## Tạo lại tài liệu (nếu muốn sửa nội dung)

Cần: Python 3, Node.js 18+, (tùy chọn) LibreOffice để xuất PDF.

```bash
cd Remote_Sensing_Study_Guide/04_Code
pip install -r requirements.txt
npm install
bash chay_tat_ca.sh
```

- Sửa nội dung đề cương: mở `tao_de_cuong.js`, tìm phần cần sửa (`// ---- PART A`, `// ---- Q1 ----` … `// ---- Q8 ----`). Các khối mới dùng hàm `EX(...)` (ví dụ), `QA(...)` (hỏi đáp), `ANA(...)` (liên tưởng).
- Sửa đề mẫu: sửa mảng `QUESTIONS` trong `tao_de_thi_mau.js`.
- Sửa hình: sửa `ve_hinh_1.py`, `ve_hinh_2.py` hoặc `ve_hinh_3.py`, chạy lại script.
- Đường dẫn trong code là tương đối, nên có thể chuyển cả thư mục sang máy khác mà vẫn chạy được.

Khi mở file Word, nếu được hỏi **cập nhật trường (update fields)** thì chọn **Yes** để mục lục hiện ra.

## Ảnh từ Internet (chưa chèn được)

Môi trường làm việc chặn tải ảnh từ Wikimedia/NASA/ESA, nên chưa chèn được ảnh web. Các ảnh dùng tự do nên bổ sung thủ công:

- Phổ bức xạ Mặt Trời ở đỉnh khí quyển và mặt biển – Wikimedia Commons, CC BY-SA 3.0: https://commons.wikimedia.org/wiki/File:Solar_spectrum_en.svg
- Độ truyền qua của khí quyển theo bước sóng – NASA, public domain: https://commons.wikimedia.org/wiki/File:Atmospheric_electromagnetic_opacity.svg
- Bản đồ NO₂ TROPOMI – ESA: https://www.esa.int/ESA_Multimedia/Images/2018/07/Nitrogen_dioxide_from_Sentinel-5P
- Bản đồ AOD toàn cầu MODIS – NASA Earth Observatory: https://earthobservatory.nasa.gov/global-maps/MODAL2_M_AER_OD
