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
    title: "Nadir (radar) altimetry",
    body: `Kỹ thuật đo cao cổ điển: vệ tinh phát xung radar thẳng xuống, đo thời gian xung phản xạ về để tính khoảng cách vệ tinh–mặt nước, từ đó suy ra độ cao mặt nước tuyệt đối. Hạn chế lớn nhất: chỉ đo được dọc theo một <strong>vệt hẹp</strong> (ground track) vài km, nên với sông/hồ, dữ liệu chỉ có tại các điểm giao cắt cố định giữa quỹ đạo vệ tinh và thân nước — độ phủ không gian rất thưa nhưng bù lại có chuỗi thời gian dài (nhiều thập kỷ, từ TOPEX/Poseidon, Jason, Sentinel-3...).`,
  },
  {
    tag: "1.2",
    title: "SWOT — Surface Water and Ocean Topography",
    body: `Sứ mệnh hợp tác NASA–CNES (cùng CSA, UKSA), phóng 16/12/2022. Mang thiết bị <strong>KaRIn</strong> (Ka-band Radar Interferometer) — hai ăng-ten radar giao thoa gắn ở hai đầu cần dài 10m, cho phép quét một dải rộng 120km liên tục thay vì chỉ một điểm như altimetry cổ điển. SWOT phủ hơn 90% diện tích nước bề mặt Trái Đất, quan sát lại một điểm sau ~21 ngày, đo được sông rộng hơn ~100m và hồ/vùng ngập > 250×250m với độ chính xác cỡ decimet. Đây là bước nhảy vọt: từ "đo tại điểm" sang "bản đồ 2D mực nước".
    <br><br>Nguồn: <a href="https://swot.jpl.nasa.gov/" target="_blank" rel="noopener">NASA SWOT</a>, <a href="https://cnes.fr/en/projects/swot" target="_blank" rel="noopener">CNES SWOT</a>, <a href="https://www.eoportal.org/satellite-missions/swot" target="_blank" rel="noopener">eoPortal SWOT</a>`,
  },
  {
    tag: "1.3",
    title: "Copernicus programme",
    body: `Chương trình quan sát Trái Đất của Liên minh Châu Âu (ESA/EU vận hành), cung cấp dữ liệu vệ tinh miễn phí, mở (họ vệ tinh Sentinel). Trong bối cảnh khóa học: Sentinel-3 (radar altimeter) là nguồn dữ liệu nadir altimetry chính đang hoạt động, dùng song song với dữ liệu SWOT.`,
  },
  {
    tag: "1.4",
    title: "Hydroweb-next (hydroweb.next)",
    body: `Nền tảng dữ liệu mở về thủy văn lục địa do CNES/Theia vận hành, gộp dữ liệu từ nhiều sứ mệnh altimetry (nadir + SWOT) thành chuỗi thời gian mực nước sông/hồ/hồ chứa sẵn sàng dùng, không cần xử lý thô. Đây là công cụ thực hành chính trong buổi giảng của Charlotte Emery (10/9).
    <br><br>Nguồn: <a href="https://hydroweb.next.theia-land.fr/" target="_blank" rel="noopener">hydroweb.next.theia-land.fr</a>, <a href="https://github.com/CNES/py-hydroweb" target="_blank" rel="noopener">GitHub CNES/py-hydroweb</a>`,
  },
  {
    tag: "1.5",
    title: "Data assimilation (đồng hóa dữ liệu)",
    body: `Kỹ thuật kết hợp tối ưu giữa (a) đầu ra mô hình số (mô hình thủy văn/thủy lực dự báo dòng chảy) và (b) quan sát thực đo (độ cao mực nước từ altimetry), có trọng số theo độ bất định của từng nguồn, nhằm cho ra ước lượng trạng thái hệ thống chính xác hơn cả hai nguồn riêng lẻ (ví dụ: bộ lọc Kalman/Ensemble Kalman Filter). Đây là lĩnh vực nghiên cứu cốt lõi của Jacques Verron trong hải dương học và đang được mở rộng sang thủy văn lục địa với dữ liệu SWOT.`,
  },
  {
    tag: "1.6",
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
