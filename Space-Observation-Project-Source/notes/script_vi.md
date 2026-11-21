# Kịch bản thuyết trình 25 phút (tiếng Việt) — deck `slides/deck/index.html`, 31 slide

Phím: ← → đổi slide, F hoặc nút "Fullscreen" để toàn màn hình. Mở nhanh slide n bằng `index.html#n`.
Tổng: Phần 1 (slide 1–15) 7 phút · Phần 2 (16–25) 10 phút · Phần 3 (26–28) 4 phút · Phần 4 (29–31) 4 phút.

## Phần 1 — Phương pháp (7 phút)

**Slide 1 – Bìa (0:20).** "Em/chúng em trình bày đề tài đo bán kính và chu kỳ quỹ đạo của ngoại hành tinh từ dữ liệu TESS. Dữ liệu hoàn toàn công khai: đường cong ánh sáng SPOC trên MAST và danh mục NASA Exoplanet Archive."

**Slide 2 – Mục tiêu và kế hoạch (0:40).** Câu hỏi: từ một đường cong ánh sáng thô, ta khôi phục bán kính và chu kỳ chính xác đến đâu so với giá trị đã công bố? Một pipeline duy nhất cho mọi hành tinh. Đọc nhanh bảng 25 phút: 7 – 10 – 4 – 4.

**Slide 3 – Vật lý transit (0:50).** Hành tinh đi qua đĩa sao che một phần ánh sáng: độ sâu δ ≈ (Rp/R★)². Sao Mộc trước Mặt Trời 1 %, Trái Đất 84 ppm. Khoảng cách giữa các lần che cho chu kỳ P. Thời lượng T và hình dạng cho a/R★ và tham số va chạm b. Lưu ý then chốt: ánh sáng chỉ cho **tỉ số** Rp/R★; muốn ra bán kính phải nhân với R★ lấy từ catalog.

**Slide 4 – Pipeline 3 khối (0:50).** Khối A theo tutorial "Quick fits for TESS light curves": tải, làm phẳng, BLS, fit, nhân R★. Em đổi PyMC3 thành batman + emcee (cùng mô hình vật lý, thư viện hiện đại hơn). Khối B là phần thêm: 3 cách làm phẳng khác nhau để ước lượng sai số hệ thống, so với catalog. Khối C là phần chọn mẫu, benchmark, demo.

**Slide 5 – Phễu chọn mẫu (0:50).** 4.826 hành tinh transit có TIC ID. Sau các lát cắt (đủ thông số catalog 4.573; Tmag < 11 còn 877; P < 15 ngày còn 680; độ sâu > 500 ppm còn 482; S/N ước lượng > 12) còn **471** hành tinh đo được. Từ 471 này chọn 10 đại diện và 2 hành tinh "stress test".

**Slide 6 – Trục nhóm (0:40).** Sáu trục: kích thước (5 lớp), quỹ đạo (4 lớp), loại sao (M/K/G/F), khoảng cách, vị trí trên bầu trời (CVZ / cao / thấp theo vĩ độ hoàng đạo), hệ đa hành tinh hay đơn. Quy tắc: mỗi đại diện phải thêm một lớp chưa có.

**Slide 7–9 – Ba hình tổng quan (1:00).** Slide 7 (bán kính–chu kỳ): 10 điểm đỏ phủ từ Trái Đất-size đến Sao Mộc-size, từ USP đến 6 ngày. Slide 8 (bản đồ trời): có hành tinh ở vùng CVZ phía nam (số 5, WASP-62 b), phía bắc cao, và gần hoàng đạo. Slide 9 (khoảng cách – loại sao): từ sao M ở 7 pc (số 8) đến sao F ở 176 pc.

**Slide 10 – Bảng 10 đại diện (0:30).** Bảng này là "bản đồ" cho 10 slide hành tinh tiếp theo; số hiệu 1–10 trùng với các hình.

**Slide 11 – Dữ liệu và làm phẳng (0:40).** PDCSAP đã loại hệ thống của tàu; ta chuẩn hóa từng sector, cắt outlier (flare), lọc Savitzky–Golay cửa sổ 1,5 ngày. Lượt sau làm phẳng lại **có che transit** để bộ lọc không ăn mất độ sâu.

**Slide 12 – BLS (0:35).** Trượt một cái hộp qua đường cong đã gấp pha, với mọi chu kỳ thử 0,26–15 ngày. Đỉnh cao nhất cho P, t0, độ sâu, thời lượng. Với HD 118203 b, BLS mù đã ra đúng chu kỳ catalog trước khi fit.

**Slide 13 – Fit và MCMC (0:35).** Mô hình Mandel–Agol (batman), tối rìa bậc hai với tham số Kipping q1, q2; 7 tham số; emcee 32 walker. Báo cáo Rp/R★ và P từ hậu nghiệm.

**Slide 14 – Ngân sách sai số (0:40).** Ba nguồn: MCMC, chọn cách làm phẳng, và R★. Thông điệp: với sao sáng, sai số bán kính do **R★** (tới 6–7 %) và **cách làm phẳng** quyết định, không phải nhiễu photon. LTT 9779 b sai số 13 % vì chuyển động sượt qua rìa sao (b = 0,91).

**Slide 15 – Benchmark (0:40).** HD 118203 b là hành tinh của chính tutorial. Em được Rp/R★ = 0,0553 so với 0,0554 của tutorial, chu kỳ trùng catalog tới 10⁻⁵. Chênh 3,8 % ở bán kính vật lý là do R★: bảng tổng hợp ghi 2,04 R☉, trong khi bán kính catalog ngầm dùng 2,10 R☉. Vì vậy em so cả Rp/R★ chứ không chỉ Rp.

## Phần 2 — Mười hành tinh (10 phút, ~1 phút mỗi hành tinh)

Mỗi slide đọc theo khuôn: nhóm → số liệu (đo/catalog/Δ) → một điều đáng chú ý → chế độ tìm (blind/guided).

- **S16 · 1 HD 118203 b** — chuẩn; 7 transit; Rp = 12,30 ± 0,35 R⊕ (catalog 12,78, −3,8 %). Tìm mù.
- **S17 · 2 HD 189733 b** — sao sáng nhất (Tmag 6,9), 20 pc; 12 transit trong một sector; Rp/R★ chính xác 0,4 %. Rp = 12,61 ± 0,18 (catalog 12,67).
- **S18 · 3 HD 209458 b** — hành tinh đầu tiên được thấy transit; 8 transit; Rp = 15,74 ± 0,27 (catalog 15,58, +1,0 %).
- **S19 · 4 WASP-18 b** — chu kỳ 22,6 giờ; 97 transit trong 4 sector; Rp/R★ chính xác 0,2 % nhưng Rp sai số 4,6 % vì R★. Rp = 14,18 ± 0,66 (catalog 13,90).
- **S20 · 5 WASP-62 b** — vĩ độ hoàng đạo −87°, vùng CVZ phía nam, TESS có rất nhiều sector; em dùng 4. Rp = 14,82 ± 0,97 (catalog 14,80).
- **S21 · 6 LTT 9779 b** — "Neptune nóng" trong sa mạc Neptune; b = 0,91 nên sai số 13 % (lớn nhất). Rp = 4,55 ± 0,59 (catalog 4,72). **Chế độ guided.**
- **S22 · 7 TOI-270 c** — sub-Neptune quanh sao M 3.500 K, R★ = 0,38 R☉; 11 transit; Rp = 2,38 ± 0,07 (catalog 2,33).
- **S23 · 8 LTT 1445 A b** — hệ gần nhất (6,9 pc); chỉ 4 transit trong 1 sector; Rp = 1,39 ± 0,12 (catalog 1,34). **Guided.**
- **S24 · 9 GJ 1132 b** — cỡ Trái Đất quanh sao M 0,22 R☉; độ sâu chỉ 2,2 ppt; Rp = 1,14 ± 0,05 (catalog 1,19, −4,1 %). Tìm mù, 26 transit.
- **S25 · 10 K2-141 b** — "hành tinh dung nham" quay 6,7 giờ, độ sâu ~350 ppm, SNR 15; Rp = 1,40 ± 0,10 (catalog 1,51, −7,3 %). **Guided**, đây là giới hạn của một sector.

## Phần 3 — Tổng kết và giới hạn (4 phút)

**Slide 26 (1:00).** Trái: chênh lệch bán kính so với catalog, đều nằm trong ±1,4σ. Phải: sai khác chu kỳ rất nhỏ (thang log, hầu hết dưới 0,01 %).

**Slide 27 (1:00).** Bảng tóm tắt: chu kỳ lệch tối đa 0,03 % (K2-141 b); bán kính lệch tối đa 7,3 %, phần lớn dưới 4 %; "pull" cột cuối cho thấy các lệch này nhất quán với sai số công bố.

**Slide 28 (2:00) — các bài học thất bại (nhấn mạnh tính trung thực).**
1. Tìm mù có thể bắt nhầm tín hiệu: K2-141 b mù ra 5,70 ngày thay vì 0,280 ngày; demo trình duyệt trả về 2×P cho LTT 1445 A b. Cách sửa: chế độ *guided* (chỉ tìm ±3 % quanh chu kỳ catalog) và thu hẹp khoảng tìm. Mọi slide hành tinh đều ghi rõ blind/guided.
2. Sao hoạt động phá bước làm phẳng: **AU Mic b** (vết sao, flare) cho Rp/R★ = 0,25 ± 0,11 trong khi catalog 0,050; **DS Tuc A b** sai số hệ thống ±0,12 — không dùng được. Hướng tiếp: Gaussian process (tutorial stellar-variability).
3. Ít transit thì giới hạn độ chính xác: AU Mic b chỉ 3 transit trong 1 sector và có biến thiên thời gian transit; LTT 1445 A b chỉ 4.

## Phần 4 — Demo và kết luận (4 phút)

**Slide 29 – Demo (2:30).** Mở `slides/demo/index.html` (không cần server). Thao tác: (1) chọn HD 189733 b; (2) bấm ① BLS — vài giây ra P = 2,21858 ngày; (3) bấm ② Fit — bảng bên dưới so với catalog; (4) bấm ③ để xem kết quả MCMC của pipeline đầy đủ. Rồi chọn K2-141 b, BLS mặc định sai → đổi khoảng tìm 0,26–0,5 ngày → ra 0,28035 ngày. Đây chính là bài học slide 28 được chạy sống.

**Slide 30 – Kết luận (1:00).** Chu kỳ của 10 hành tinh (0,28–6,1 ngày) khớp catalog tới 0,03 %; bán kính (1,1–15,7 R⊕) trong ~4 %, nhất quán với sai số. Điểm hạn chế chính: R★, cách làm phẳng, số lượng transit. Hướng tiếp: mật độ sao và độ lệch tâm, TTV, ghép nhiều sector, GP cho sao hoạt động.

**Slide 31 – Tài liệu (0:20).** Dừng ở đây, mời câu hỏi.

## Câu hỏi có thể gặp

- **Vì sao Rp lệch catalog tới 3,8 % ở HD 118203 b dù Rp/R★ khớp?** Vì catalog ngầm dùng R★ khác bảng tổng hợp (2,10 so với 2,04 R☉). Phần lệch nằm ở R★, không ở ánh sáng.
- **Vì sao không dùng đúng PyMC3 + exoplanet như tutorial?** Cùng mô hình vật lý (Mandel–Agol + tối rìa bậc hai); batman + emcee cài đặt được trên môi trường hiện tại. Kiểm chứng bằng chính hành tinh benchmark.
- **Có phải "gian lận" khi dùng chu kỳ catalog (guided)?** Guided chỉ giới hạn khoảng tìm; chu kỳ, bán kính vẫn đo từ dữ liệu. Em ghi rõ trên slide và nêu cả trường hợp mù bị sai.
- **Sai số hệ thống tính thế nào?** Làm phẳng 3 biến thể (che transit, cửa sổ khác nhau); nửa khoảng của Rp/R★ là sai số hệ thống, cộng bình phương với sai số MCMC.
- **Vì sao chỉ dùng 1–4 sector?** Giữ thời gian chạy hợp lý và tránh baseline quá dài làm BLS chậm; thêm sector chủ yếu cải thiện chu kỳ, còn bán kính bị R★ giới hạn.
- **Bán kính có phụ thuộc tối rìa không?** Có, q1, q2 được fit tự do; trong demo trình duyệt tối rìa cố định nên sai lệch lớn hơn (một vài %).
