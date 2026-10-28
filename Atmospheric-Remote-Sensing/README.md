# Atmospheric-Remote-Sensing (USTH)

Hệ thống tự học và ôn thi cho môn *Satellite Remote Sensing of Atmospheric Composition*, dựng từ bộ tài liệu
`Atmospheric_Remote_Sensing_Study_Guide.zip` (đề cương 8 câu hỏi lý thuyết, đề thi mẫu, hình, mã vẽ hình).
Theo mẫu DSES-USTH: màu USTH đã đọc từ pixel logo chính thức (xanh `#273896`, đỏ `#ED1C24`), slide 1280×720 chữ ≥ 20 px.

Trang web: https://tatcataittn.github.io/for-ttn-USTH/Atmospheric-Remote-Sensing/

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `index.html` | Trang chủ, lộ trình ôn tập, trạng thái và giới hạn |
| `vi/NN-slug/index.html` | Bài giảng của module (nôm na → kỹ thuật → công thức → ví dụ), exam checklist, slide nhúng, quiz nhanh |
| `vi/NN-slug/bank.html` | Ngân hàng câu hỏi: trắc nghiệm có giải thích + tự luận có lời giải; lọc, làm lại, lưu tiến độ |
| `slides/mN.html` | Slide module (canvas 1280×720, phím ← →, toàn màn hình) |
| `calculators.html` | 9 công cụ tính toán chạy trong trình duyệt |
| `exam.html` | Đề thi mẫu gốc 120 phút (tự chấm) và 8 đề trắc nghiệm 15 câu / 30 phút |
| `reference.html` | Công thức và từ viết tắt (phụ lục đề cương) |
| `resources.html`, `resources/` | Đề cương, đề thi mẫu (PDF, DOCX), 18 hình, 4 ảnh slide |
| `data/verified.json` | Mọi con số tính bằng Python (nguồn sự thật duy nhất) |
| `notebooks/verify_numbers.ipynb` | Tính lại độc lập toàn bộ số liệu (đã chạy, 41 phép so sánh `OK`) |

## 8 module

1. Bể chứa và thời gian sống · 2. Tương tác ánh sáng – vật chất · 3. Truy hồi khí vết: cột và profil · 4. Hình học quan sát ·
5. Averaging kernel và DOFS · 6. Viễn thám aerosol thụ động · 7. Các chế độ tán xạ · 8. Độ cao aerosol

## Kiểm chứng

- `build/verify_numbers.py` tính mọi số bằng hai cách độc lập (ví dụ Wien so với cực đại số của Planck; DOFS so với tổng trị riêng; Q_ext Mie so với công thức Rayleigh).
- `tests/test_calc.js` (Node): hàm tính JavaScript so với Python, 455 phép so sánh, gồm cả ma trận averaging kernel 12×12.
- `tests/browser_test.py` (Selenium): tải mọi trang, ảnh hỏng, lỗi console, quiz, ngân hàng, công cụ tính, đề thi.
- `build/check_deck.py` (Selenium): slide không tràn khung, chữ ≥ 20 px, không trống đáy.

## Dựng lại

```bash
cd build && python3 verify_numbers.py && python3 build_all.py && python3 make_notebook.py
node ../tests/test_calc.js
```

Nguồn dựng (Python) nằm ở `build/`; nội dung mỗi module ở `build/m1.py` … `m8.py`.
