// Nội dung tĩnh: chương trình, lý thuyết, giảng viên — trích từ 01_ly_thuyet_va_giang_vien.md
const PROGRAM_DAYS = [
  {
    day: "Thứ Hai, 7/9 — Khai mạc & Nadir altimetry",
    rows: [
      ["08:00–08:35", "Khai mạc, giới thiệu mục tiêu khóa học", "Jean Tran Thanh Van, Denis Fourmeau, Laetitia Gal, Adrien Paris"],
      ["08:35–10:30", "Giới thiệu 5 tổ chức đối tác: USTH, CNES, VNSC, PSA, MRC", "Binh Pham Duc, Linda Tomasini, Pham Thi Mai Thy, Ariel Blanco, Mathias Boun Hen"],
      ["10:30–11:00", "Giải lao + ảnh tập thể", "—"],
      ["11:00–12:00", "Học viên trình bày & Poster", "—"],
      ["13:30–15:00", "Tổng quan sứ mệnh Nadir altimetry / Dữ liệu", "Adrien Paris, Laetitia Gal"],
      ["15:30–17:00", "Thực hành: tải & phân tích dữ liệu Nadir", "—"],
    ],
  },
  {
    day: "Thứ Ba, 8/9 — SWOT mission",
    rows: [
      ["08:30–10:00", "Tổng quan sứ mệnh SWOT + sản phẩm dữ liệu", "Daniel Moreira, Sabrine Amzil, Binh Pham Duc"],
      ["10:30–12:00", "Thực hành 1: tải dữ liệu SWOT", "—"],
      ["13:30–15:00", "Thực hành 2: trích xuất & trực quan hóa", "—"],
      ["15:30–17:00", "Ứng dụng SWOT & thảo luận", "—"],
    ],
  },
  {
    day: "Thứ Tư, 9/9 — Thực địa & mô hình thủy văn",
    rows: [
      ["08:00–12:00", "Thực địa: quan sát mực nước hồ chứa", "—"],
      ["13:30–15:00", "Chuyển tiếp dữ liệu vệ tinh sang mô hình thủy văn", "Laetitia Gal, Adrien Paris"],
      ["15:30–17:00", "Thực hành: mô phỏng thủy văn", "—"],
    ],
  },
  {
    day: "Thứ Năm, 10/9 — Hydroweb-next & Data assimilation",
    rows: [
      ["08:30–10:00", "Giới thiệu Hydroweb-next", "Charlotte Emery"],
      ["10:30–12:00", "Thực hành 1: dùng Hydroweb / trích chuỗi thời gian", "—"],
      ["13:30–15:00", "Nguyên lý đồng hóa dữ liệu (data assimilation)", "Charlotte Emery, Jacques Verron"],
      ["15:30–17:00", "Thực hành 2: đồng hóa dữ liệu", "—"],
    ],
  },
  {
    day: "Thứ Sáu, 11/9 — Flood monitoring & bế mạc",
    rows: [
      ["08:30–10:00", "Giám sát lũ lụt & quản lý thảm họa", "Sabrine Amzil, Adrien Paris"],
      ["10:30–12:00", "Thực hành: trường hợp lũ lụt", "—"],
      ["13:30–15:00", "Bàn tròn / phản hồi / bế mạc", "—"],
    ],
  },
];

const THEORY_TOPICS = [
  {
    tag: "1.1",
    title: "Nadir (radar) altimetry — nguyên lý & phương trình đo khoảng cách",
    body: `Kỹ thuật đo cao cổ điển: vệ tinh phát xung radar thẳng xuống, đo thời gian xung phản xạ về để tính khoảng cách vệ tinh–mặt nước, từ đó suy ra độ cao mặt nước tuyệt đối. Hạn chế lớn nhất: chỉ đo được dọc theo một <strong>vệt hẹp</strong> (ground track) vài km, nên với sông/hồ, dữ liệu chỉ có tại các điểm giao cắt cố định giữa quỹ đạo vệ tinh và thân nước — độ phủ không gian rất thưa nhưng bù lại có chuỗi thời gian dài (nhiều thập kỷ, từ TOPEX/Poseidon, Jason, Sentinel-3...).
    <div class="formula-box">
      <p><strong>Phương trình khoảng cách (range equation):</strong></p>
      <p class="formula">R = c · Δt / 2</p>
      <p class="formula-note">c: vận tốc ánh sáng · Δt: thời gian đi–về của xung radar</p>
      <p><strong>Độ cao mặt nước tuyệt đối (so với ellipsoid tham chiếu):</strong></p>
      <p class="formula">h = H<sub>sat</sub> − (R + Σ hiệu chỉnh)</p>
      <p class="formula-note">H<sub>sat</sub>: độ cao quỹ đạo vệ tinh (từ quỹ đạo học chính xác — precise orbit determination)</p>
    </div>
    <p>Trước khi ra <em>h</em>, khoảng cách R thô phải qua <strong>retracking</strong> (làm khớp lại dạng sóng phản xạ — waveform — vì bề mặt nước lục địa gây méo dạng sóng khác biển) và cộng thêm các <strong>hiệu chỉnh địa vật lý</strong>:</p>
    <ul class="bullets">
      <li><strong>Tầng đối lưu khô</strong> (dry troposphere): ~2.3m, tính từ áp suất khí quyển bề mặt — ổn định, mô hình hoá tốt.</li>
      <li><strong>Tầng đối lưu ướt</strong> (wet troposphere): vài cm–dm, phụ thuộc hơi nước — biến động mạnh, khó nhất trong các hiệu chỉnh.</li>
      <li><strong>Tầng điện ly</strong> (ionosphere): 2–8cm, phụ thuộc tần số — đo bằng cách kết hợp 2 băng tần (Ku + C/S) để tách ảnh hưởng.</li>
      <li><strong>Thủy triều</strong> (đại dương, cực, tải trọng khí quyển) — với sông/hồ nội địa thường bỏ qua hoặc hiệu chỉnh nhỏ.</li>
    </ul>
    <p class="formula-note">Nguồn: <a href="https://www.sciencedirect.com/science/article/pii/S0034425720305228" target="_blank" rel="noopener">ScienceDirect — vai trò tầng đối lưu trong đo cao vệ tinh</a></p>`,
  },
  {
    tag: "1.2",
    title: "SWOT — Surface Water and Ocean Topography",
    body: `Sứ mệnh hợp tác NASA–CNES (cùng CSA, UKSA), phóng 16/12/2022. Mang thiết bị <strong>KaRIn</strong> (Ka-band Radar Interferometer) — hai ăng-ten radar giao thoa gắn ở hai đầu cần dài 10m, cho phép quét một dải rộng 120km liên tục thay vì chỉ một điểm như altimetry cổ điển. SWOT phủ hơn 90% diện tích nước bề mặt Trái Đất, quan sát lại một điểm sau ~21 ngày, đo được sông rộng hơn ~100m và hồ/vùng ngập > 250×250m với độ chính xác cỡ decimet. Đây là bước nhảy vọt: từ "đo tại điểm" sang "bản đồ 2D mực nước".
    <br><br>Nguồn: <a href="https://swot.jpl.nasa.gov/" target="_blank" rel="noopener">NASA SWOT</a>, <a href="https://cnes.fr/en/projects/swot" target="_blank" rel="noopener">CNES SWOT</a>, <a href="https://www.eoportal.org/satellite-missions/swot" target="_blank" rel="noopener">eoPortal SWOT</a>`,
  },
  {
    tag: "1.3",
    title: "KaRIn — nguyên lý giao thoa radar (interferometry), phương trình pha → độ cao",
    body: `KaRIn không đo khoảng cách trực tiếp như altimetry cổ điển, mà đo <strong>độ lệch pha</strong> giữa tín hiệu phản xạ nhận được ở hai ăng-ten đặt cách nhau một khoảng gọi là <strong>đường nền (baseline) B</strong> = 10m. Vì hai ăng-ten nhìn cùng một điểm trên mặt đất từ hai vị trí hơi khác nhau, quãng đường tín hiệu đi về có sai khác nhỏ → lệch pha Δφ. Từ Δφ suy ra góc nhìn (look angle) θ, rồi suy ra độ cao h.
    <div class="formula-box">
      <p><strong>Pha → góc nhìn:</strong></p>
      <p class="formula">Δφ = k · B · sin(θ)</p>
      <p class="formula-note">k = 2π/λ (số sóng, λ: bước sóng Ka-band) · B: đường nền 10m · θ: góc nhìn</p>
      <p><strong>Góc nhìn → độ cao:</strong></p>
      <p class="formula">h = H − r₁ · cos(θ)</p>
      <p class="formula-note">H: độ cao vệ tinh · r₁: khoảng cách từ ăng-ten 1 đến điểm đo</p>
    </div>
    <p>Vì pha chỉ đo được modulo 2π (lặp lại theo chu kỳ), tồn tại <strong>độ cao mơ hồ (altitude of ambiguity) E<sub>a</sub></strong> — chênh 2π trong pha tương ứng với một khoảng chênh cao cố định — cần xử lý gỡ mơ hồ pha (phase unwrapping) trong bước xử lý dữ liệu.</p>
    <p class="formula-note">Nguồn: <a href="https://www.researchgate.net/publication/224199848_KaRIn_-_the_Ka-band_radar_interferometer_on_SWOT_Measurement_principle_processing_and_data_specificities" target="_blank" rel="noopener">KaRIn — Measurement principle, processing and data specificities</a></p>`,
  },
  {
    tag: "1.4",
    title: "Copernicus programme",
    body: `Chương trình quan sát Trái Đất của Liên minh Châu Âu (ESA/EU vận hành), cung cấp dữ liệu vệ tinh miễn phí, mở (họ vệ tinh Sentinel). Trong bối cảnh khóa học: Sentinel-3 (radar altimeter) là nguồn dữ liệu nadir altimetry chính đang hoạt động, dùng song song với dữ liệu SWOT.`,
  },
  {
    tag: "1.5",
    title: "Hydroweb-next (hydroweb.next)",
    body: `Nền tảng dữ liệu mở về thủy văn lục địa do CNES/Theia vận hành, gộp dữ liệu từ nhiều sứ mệnh altimetry (nadir + SWOT) thành chuỗi thời gian mực nước sông/hồ/hồ chứa sẵn sàng dùng, không cần xử lý thô. Đây là công cụ thực hành chính trong buổi giảng của Charlotte Emery (10/9).
    <br><br>Nguồn: <a href="https://hydroweb.next.theia-land.fr/" target="_blank" rel="noopener">hydroweb.next.theia-land.fr</a>, <a href="https://github.com/CNES/py-hydroweb" target="_blank" rel="noopener">GitHub CNES/py-hydroweb</a>`,
  },
  {
    tag: "1.6",
    title: "SWOT L2 HR — các sản phẩm dữ liệu (PIXC, RiverSP, LakeSP, PIXCVec)",
    body: `Dữ liệu KaRIn thô được xử lý qua nhiều tầng sản phẩm trước khi thành số liệu thủy văn dùng được:
    <ul class="bullets">
      <li><strong>L2_HR_PIXC</strong> (Pixel Cloud): "đám mây điểm ảnh" — tập hợp phi cấu trúc các pixel phát hiện có nước, độ phân giải gốc ~15–25m (cross-track) × ~5–10m (along-track). Đây là dữ liệu nền, chưa gán vào sông/hồ cụ thể nào.</li>
      <li><strong>L2_HR_PIXCVec</strong>: bản PIXC đã lọc nhiễu, định vị lại chính xác hơn theo ràng buộc độ cao, và gán mỗi pixel vào sông/hồ tương ứng trong cơ sở dữ liệu tham chiếu (Prior River & Lake Database — PRD/PLD).</li>
      <li><strong>L2_HR_RiverSP</strong> (River Single-Pass): sản phẩm vector cấp sông, gồm 2 loại — <em>Node</em> (điểm dọc sông, ~200m) và <em>Reach</em> (đoạn sông ~10km) — mỗi đơn vị có độ cao, độ rộng, độ dốc mặt nước.</li>
      <li><strong>L2_HR_LakeSP</strong> (Lake Single-Pass): sản phẩm vector cấp hồ/hồ chứa, gồm hồ quan trắc được (Obs), hồ theo cơ sở dữ liệu tiên nghiệm (Prior), và đối tượng chưa gán (Unassigned).</li>
    </ul>
    <p>Học viên thực hành trong khóa dùng chính chuỗi sản phẩm này: tải PIXC → trực quan hoá → trích Reach/Node cho một đoạn sông cụ thể.</p>
    <p class="formula-note">Nguồn: <a href="https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_PIXC_D" target="_blank" rel="noopener">NASA PO.DAAC — SWOT L2 HR PIXC</a>, <a href="https://www.theia-land.fr/en/blog/swot-understanding-our-rivers-lakes-and-floodplains/" target="_blank" rel="noopener">Theia — SWOT rivers/lakes/floodplains</a></p>`,
  },
  {
    tag: "1.7",
    title: "Ước tính lưu lượng dòng chảy (discharge) từ vệ tinh — phương trình Manning & AMHG",
    body: `SWOT không đo lưu lượng Q (m³/s) trực tiếp — chỉ đo độ rộng W, độ cao h, độ dốc mặt nước S dọc sông. Lưu lượng phải được <strong>suy luận</strong> bằng mô hình thủy lực, phổ biến nhất dựa trên phương trình Manning:
    <div class="formula-box">
      <p><strong>Phương trình Manning (vận tốc dòng chảy):</strong></p>
      <p class="formula">V = (1/n) · R<sub>h</sub><sup>2/3</sup> · S<sup>1/2</sup></p>
      <p class="formula-note">n: hệ số nhám Manning · R<sub>h</sub>: bán kính thủy lực (≈ độ sâu với sông rộng) · S: độ dốc mặt nước</p>
      <p><strong>Lưu lượng:</strong></p>
      <p class="formula">Q = A · V</p>
      <p class="formula-note">A: diện tích mặt cắt ướt — vấn đề là A và n <em>không đo được trực tiếp từ vệ tinh</em>, chỉ ước lượng gián tiếp từ W, h, S theo thời gian</p>
    </div>
    <p>Hai hướng thuật toán chính trong đội khoa học SWOT:</p>
    <ul class="bullets">
      <li><strong>MetroMan / BAM</strong> (Bayesian AMHG-Manning): ước lượng đồng thời các tham số Manning ẩn bằng suy luận Bayes từ chuỗi thời gian W–h–S.</li>
      <li><strong>AMHG</strong> (At-Many-stations Hydraulic Geometry): giả định quan hệ lũy thừa giữa W và Q ổn định dọc sông, giảm số tham số cần ước lượng bằng cách ràng buộc lưu lượng bằng nhau giữa các mặt cắt lân cận.</li>
    </ul>
    <p class="formula-note">Nguồn: <a href="https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017WR021626" target="_blank" rel="noopener">Hagemann et al. 2017, BAM — WRR</a>, <a href="https://doi.org/10.3390/rs15061672" target="_blank" rel="noopener">Discharge từ độ rộng SWOT + AMHG — Remote Sensing 2023</a></p>`,
  },
  {
    tag: "1.8",
    title: "Dữ liệu đồng hóa: Kalman Filter — phương trình cốt lõi",
    body: `<strong>Bộ lọc Kalman</strong> là công cụ toán học nền tảng của data assimilation: kết hợp tối ưu một dự báo mô hình (forecast) với một quan sát thực đo (observation), có trọng số theo độ bất định (sai số) của từng nguồn.
    <div class="formula-box">
      <p><strong>Bước phân tích (analysis step):</strong></p>
      <p class="formula">z<sup>a</sup> = z<sup>f</sup> + K(y − H·z<sup>f</sup>)</p>
      <p class="formula-note">z<sup>f</sup>: trạng thái dự báo (forecast) · y: quan sát (ví dụ mực nước từ altimetry) · H: toán tử quan sát (chuyển trạng thái mô hình sang không gian quan sát) · z<sup>a</sup>: trạng thái sau phân tích</p>
      <p><strong>Hệ số Kalman (Kalman gain):</strong></p>
      <p class="formula">K = P·H<sup>T</sup> (H·P·H<sup>T</sup> + R)<sup>−1</sup></p>
      <p class="formula-note">P: ma trận hiệp phương sai sai số của mô hình · R: ma trận hiệp phương sai sai số quan sát</p>
    </div>
    <p>Trực giác: nếu mô hình rất bất định (P lớn) so với quan sát (R nhỏ) → K lớn → phân tích nghiêng mạnh về phía quan sát, và ngược lại. Đây là lĩnh vực nghiên cứu cốt lõi của Jacques Verron trong hải dương học, đang được mở rộng sang thủy văn lục địa với dữ liệu SWOT.</p>`,
  },
  {
    tag: "1.9",
    title: "Ensemble Kalman Filter (EnKF) — vì sao cần cho bài toán quy mô lớn",
    body: `Với mô hình thủy văn/thủy lực quy mô lưu vực, ma trận hiệp phương sai P có kích thước quá lớn để tính tường minh. <strong>EnKF</strong> giải quyết bằng cách thay P bằng hiệp phương sai mẫu ước lượng từ một <em>tập hợp (ensemble)</em> N thành viên mô hình chạy song song, mỗi thành viên nhiễu động khác nhau.
    <div class="formula-box">
      <p><strong>Bước dự báo (forecast — chạy N thành viên qua mô hình M):</strong></p>
      <p class="formula">z<sub>i</sub><sup>f</sup> = M(z<sub>i</sub>),&nbsp; i = 1…N</p>
      <p><strong>Bước phân tích (mỗi thành viên, quan sát nhiễu động ngẫu nhiên):</strong></p>
      <p class="formula">K<sub>j</sub> = Ĉ<sub>j</sub>·H<sub>j</sub><sup>T</sup> (H<sub>j</sub>·Ĉ<sub>j</sub>·H<sub>j</sub><sup>T</sup> + Γ<sub>j</sub>)<sup>−1</sup></p>
      <p class="formula-note">Ĉ<sub>j</sub>: hiệp phương sai <em>mẫu</em> tính từ ensemble dự báo · Γ<sub>j</sub>: hiệp phương sai sai số quan sát</p>
    </div>
    <p>Với dữ liệu wide-swath (SWOT), sai số quan sát có <strong>cấu trúc không gian tương quan</strong> (không độc lập theo từng pixel như altimetry cổ điển) — nên ma trận Γ không thể coi là đường chéo đơn giản, cần kỹ thuật giảm sai số tương quan chuyên biệt trước khi đưa vào vòng lặp EnKF. Đây là hướng nghiên cứu đang mở rộng của nhóm CNRS/LEGOS (Jacques Verron) sang thủy văn lục địa.</p>
    <p class="formula-note">Nguồn: <a href="https://journals.ametsoc.org/view/journals/mwre/130/1/1520-0493_2002_130_0103_hdawte_2.0.co_2.xml" target="_blank" rel="noopener">Reichle et al. 2002, EnKF trong thủy văn — Monthly Weather Review</a></p>`,
  },
  {
    tag: "1.10",
    title: "Data assimilation (đồng hóa dữ liệu) — bức tranh tổng quan",
    body: `Kỹ thuật kết hợp tối ưu giữa (a) đầu ra mô hình số (mô hình thủy văn/thủy lực dự báo dòng chảy) và (b) quan sát thực đo (độ cao mực nước từ altimetry), có trọng số theo độ bất định của từng nguồn, nhằm cho ra ước lượng trạng thái hệ thống chính xác hơn cả hai nguồn riêng lẻ. Xem chi tiết toán học tại mục <strong>1.8 Kalman Filter</strong> và <strong>1.9 Ensemble Kalman Filter</strong> ở trên.`,
  },
  {
    tag: "1.11",
    title: "Datum thẳng đứng & geoid — vì sao \"độ cao\" cần định nghĩa rõ",
    body: `Độ cao đo bởi vệ tinh (h trong mục 1.1/1.3) là so với một <strong>ellipsoid tham chiếu</strong> toán học (ví dụ WGS84/GRS80) — không phải mực nước biển thực. Để so sánh với bản đồ địa hình hoặc trạm đo tại chỗ (dùng mực nước biển trung bình làm gốc — mean sea level), cần chuyển qua <strong>geoid</strong> — bề mặt đẳng thế trọng lực gần đúng với mực nước biển trung bình nếu không có gió/dòng chảy.
    <div class="formula-box">
      <p class="formula">Độ cao chính (orthometric, H) = h<sub>ellipsoid</sub> − N<sub>geoid</sub></p>
      <p class="formula-note">N<sub>geoid</sub>: độ lệch geoid–ellipsoid tại vị trí đó, tra từ mô hình geoid toàn cầu (ví dụ EGM2008)</p>
    </div>
    <p>Sai số chọn sai mô hình geoid hoặc datum không đồng nhất giữa dữ liệu vệ tinh và dữ liệu trạm đo tại chỗ là một nguồn lỗi phổ biến khi so sánh/hiệu chỉnh (validate) dữ liệu altimetry với số liệu thực địa — một chủ đề được nhấn mạnh trong buổi thực địa quan sát mực nước hồ chứa (9/9) của khóa học.</p>`,
  },
  {
    tag: "1.12",
    title: "Sai số & độ chính xác trong altimetry — retracking là gì",
    body: `Xung radar phản xạ từ mặt nước sông/hồ (bề mặt hẹp, có thể bị che bởi thảm thực vật/bờ sông) tạo ra <strong>dạng sóng (waveform)</strong> phản xạ khác nhiều so với dạng sóng chuẩn trên đại dương phẳng — bộ theo dõi (tracker) trên vệ tinh có thể khóa sai điểm tham chiếu. <strong>Retracking</strong> là bước xử lý mặt đất, làm khớp lại mô hình toán học với waveform thực đo để xác định chính xác thời điểm xung tới bờ nước, từ đó tính lại Δt chính xác hơn cho phương trình ở mục 1.1.
    <p>Với sông hẹp và bị nhiễu bởi bờ/thực vật, các thuật toán retracker chuyên biệt cho nước lục địa (ví dụ dạng sóng đơn đỉnh — OCOG, threshold retracker) cho kết quả tốt hơn retracker chuẩn đại dương (Brown model) vốn thiết kế cho mặt biển rộng và đồng nhất.</p>`,
  },
  {
    tag: "1.13",
    title: "Transboundary river management (quản lý sông xuyên biên giới)",
    body: `Khi một lưu vực sông chảy qua nhiều quốc gia (Mekong là ví dụ điển hình, qua Mekong River Commission), dữ liệu in-situ thường không được chia sẻ đầy đủ vì lý do chủ quyền/an ninh nước. Dữ liệu vệ tinh (altimetry, SWOT) cung cấp một nguồn quan sát trung lập, nhất quán xuyên biên giới, hỗ trợ giám sát lũ lụt và điều phối vận hành hồ chứa giữa các quốc gia.`,
  },
];

const LECTURERS = [
  {
    name: "Laetitia Gal",
    org: "Hydro Matters — điều phối chính khóa học",
    bio: "Chuyên gia thủy văn & khí hậu, chuyên sâu giám sát sông bằng vệ tinh đo cao và ảnh viễn thám. Tham gia hoạt động cal/val SWOT tại Brazil.",
    pubs: [
      { t: "Larnier et al. (2025), \"Estimating Channel Parameters and Discharge at River Network Scale Using Hydrological-Hydraulic Models, SWOT and Multi-Satellite Data\", Water Resources Research", u: "https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2024WR038455" },
      { t: "\"Satellite altimetry for hydrology: a review\"", u: "https://www.researchgate.net/publication/280592849_Satellite_altimetry_for_hydrology_a_review" },
    ],
  },
  {
    name: "Adrien Paris",
    org: "Hydro Matters / Ocean Next — cựu LEGOS, Đại học Toulouse III",
    bio: "Kỹ sư cơ khí (ENSAM), chuyển hướng sang thủy văn không gian. Nghiên cứu mô hình hóa thủy văn, altimetry, lưu vực Amazon và Congo.",
    pubs: [
      { t: "\"Hydro-climatology study of the Ogooué River basin using hydrological modeling and satellite altimetry\"", u: "https://www.researchgate.net/publication/340898004_Hydro-climatology_study_of_the_Ogooue_River_basin_using_hydrological_modeling_and_satellite_altimetry" },
    ],
  },
  {
    name: "Binh Pham Duc",
    org: "USTH — Đại học Khoa học & Công nghệ Hà Nội",
    bio: "Nghiên cứu viễn thám quang học & radar cho giám sát mặt nước, hồ và biên giới Mekong; bibliometrics.",
    pubs: [
      { t: "(2023) Monitoring monthly variation of Tonle Sap Lake water volume using Sentinel-1 imagery and satellite altimetry data, J. Water and Climate Change" },
      { t: "(2022) Monitoring lake volume variation from space — case study Thac Mo Reservoir (Vietnam), Remote Sensing" },
      { t: "(2020) Surface water evolution (2001–2017) at the Cambodia/Vietnam Border, Upper Mekong Delta, Remote Sensing" },
    ],
    pubLink: "https://scholar.google.com/citations?hl=en&user=1qZ9n6AAAAAJ",
  },
  {
    name: "Charlotte Emery",
    org: "LEGOS / CNES (hiện cùng CS-Group)",
    bio: "Hydroweb-next & AVISO updates; đồng hóa dữ liệu quy mô lớn kiểu SWOT (ensemble-based).",
    pubs: [
      { t: "\"Updates from hydroweb.next and AVISO\" (2025), SWOT Applications Meeting", u: "https://swot.jpl.nasa.gov/internal_resources/811/20250630-0835-Emery-Hnext_Aviso_updates.pdf" },
      { t: "\"Variance-based Sensitivity Analysis of Large-scale Hydrological Model to Prepare Ensemble-based SWOT-like Data Assimilation Experiments\", AGU Fall Meeting 2015", u: "https://agu.confex.com/agu/fm15/webprogram/Paper64397.html" },
    ],
  },
  {
    name: "Jacques Verron",
    org: "CNRS / LEGOS, Toulouse (cựu LGGE, Đại học Joseph Fourier Grenoble)",
    bio: "Người đặt nền móng đồng hóa dữ liệu altimetry vào mô hình đại dương (Kalman/Ensemble Kalman Filter); hiện mở rộng sang wide-swath (SWOT).",
    pubs: [
      { t: "Verron (1990), \"Altimeter data assimilation into an ocean circulation model: Sensitivity to orbital parameters\", JGR: Oceans", u: "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/JC095iC07p11443" },
      { t: "\"Joint altimetric and in-situ data assimilation using the GRACE mean dynamic topography\", Ocean Dynamics", u: "https://link.springer.com/article/10.1007/s10236-007-0131-4" },
    ],
    pubLink: "https://www.researchgate.net/profile/Jacques-Verron",
  },
  {
    name: "Ariel Blanco",
    org: "PSA / PhilSA — Director IV, Space Information Infrastructure Bureau",
    bio: "Viễn thám và GIS ứng dụng biển/nước: lập bản đồ cỏ biển toàn quốc bằng Sentinel-2, phát hiện tẩy trắng san hô bằng ảnh siêu phổ PRISMA.",
    pubs: [
      { t: "\"Towards Nationwide Mapping of Seagrasses in the Philippines\" (dự án BlueCARES, Sentinel-2)" },
      { t: "\"Coral Bleaching Detection Using PRISMA Hyperspectral Satellite Imagery in Calatagan, Batangas\"" },
    ],
    pubLink: "https://philsa.gov.ph/publications-research/page/2/",
  },
];
