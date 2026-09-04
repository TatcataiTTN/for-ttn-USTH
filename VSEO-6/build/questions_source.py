"""
Ngân hàng câu hỏi MCQ cho VSEO6 quiz. KHÔNG chứa vị trí đáp án cố định ("A"/"B"...).
Mỗi câu: correct (str), distractors (list[str]) tách biệt — generate_questions.py sẽ
xáo trộn bằng random.Random(SEED) rồi remap thành A/B/C/D lúc build JSON.
"""

QUESTIONS = [
    # --- Nadir altimetry vs SWOT ---
    dict(
        id="nadir-def",
        topic="Nadir altimetry",
        question="Nadir altimetry đo độ cao mặt nước bằng cách nào?",
        correct="Phát xung radar thẳng xuống dưới vệ tinh và đo thời gian phản xạ về",
        distractors=[
            "Chụp ảnh quang học mặt nước rồi ước lượng độ cao từ bóng đổ",
            "Dùng hai ăng-ten radar giao thoa quét một dải rộng 120 km",
            "Đo nhiệt độ bề mặt nước bằng cảm biến hồng ngoại",
        ],
        explain="Nadir altimetry là kỹ thuật radar cổ điển: đo khoảng cách vệ tinh–mặt nước theo phương thẳng đứng.",
    ),
    dict(
        id="nadir-limit",
        topic="Nadir altimetry",
        question="Hạn chế lớn nhất của nadir altimetry so với SWOT là gì?",
        correct="Chỉ đo được dọc theo một vệt hẹp (ground track), độ phủ không gian thưa",
        distractors=[
            "Không thể đo được sông hay hồ, chỉ đo được đại dương",
            "Không có chuỗi thời gian dài, dữ liệu mới bắt đầu từ 2022",
            "Không được các cơ quan vũ trụ như CNES, NASA hỗ trợ",
        ],
        explain="Nadir chỉ có dữ liệu tại các điểm giao cắt cố định giữa quỹ đạo vệ tinh và thân nước.",
    ),
    dict(
        id="swot-def",
        topic="SWOT",
        question="SWOT (Surface Water and Ocean Topography) là hợp tác giữa những cơ quan nào?",
        correct="NASA và CNES (cùng CSA, UKSA)",
        distractors=[
            "Chỉ riêng ESA (Cơ quan Vũ trụ Châu Âu)",
            "USTH và Mekong River Commission",
            "Google Earth Engine và Copernicus",
        ],
        explain="SWOT là sứ mệnh hợp tác NASA–CNES, phóng ngày 16/12/2022.",
    ),
    dict(
        id="swot-karin",
        topic="SWOT",
        question="Thiết bị KaRIn trên vệ tinh SWOT hoạt động theo nguyên lý nào?",
        correct="Interferometry băng Ka với hai ăng-ten radar ở hai đầu cần dài 10m, quét dải rộng 120km",
        distractors=[
            "Một ăng-ten radar duy nhất đo thẳng xuống dưới vệ tinh",
            "Cảm biến quang học đa phổ chụp ảnh mặt nước",
            "LIDAR laser đo khoảng cách bằng ánh sáng",
        ],
        explain="KaRIn (Ka-band Radar Interferometer) là bước nhảy vọt từ đo điểm sang bản đồ 2D mực nước.",
    ),
    dict(
        id="swot-coverage",
        topic="SWOT",
        question="SWOT phủ lại một điểm quan sát sau khoảng bao lâu, và đo được sông rộng tối thiểu bao nhiêu mét?",
        correct="Khoảng 21 ngày; sông rộng hơn khoảng 100 mét",
        distractors=[
            "Khoảng 1 ngày; mọi con sông bất kể độ rộng",
            "Khoảng 90 ngày; chỉ sông rộng hơn 5 km",
            "Khoảng 6 giờ; chỉ hồ chứa lớn hơn 10 km²",
        ],
        explain="SWOT quan sát lại sau ~21 ngày, đo sông > 100m và vùng nước > 250×250m.",
    ),
    # --- Copernicus / Hydroweb-next ---
    dict(
        id="copernicus-def",
        topic="Copernicus",
        question="Copernicus là chương trình quan sát Trái Đất do ai vận hành, cung cấp dữ liệu qua họ vệ tinh nào?",
        correct="Liên minh Châu Âu/ESA, cung cấp dữ liệu mở miễn phí qua họ vệ tinh Sentinel",
        distractors=[
            "NASA, cung cấp dữ liệu trả phí qua vệ tinh Landsat",
            "CNES, chỉ dành riêng cho nghiên cứu nội bộ Pháp",
            "Mekong River Commission, chỉ phủ khu vực Đông Nam Á",
        ],
        explain="Copernicus (EU/ESA) cung cấp dữ liệu Sentinel mở, miễn phí; Sentinel-3 là nguồn nadir altimetry chính đang hoạt động.",
    ),
    dict(
        id="hydroweb-def",
        topic="Hydroweb-next",
        question="Hydroweb-next (hydroweb.next) là gì?",
        correct="Nền tảng dữ liệu mở do CNES/Theia vận hành, gộp dữ liệu nadir + SWOT thành chuỗi thời gian sẵn dùng",
        distractors=[
            "Một mô hình thủy văn số trị chạy trên siêu máy tính",
            "Vệ tinh radar thế hệ mới thay thế SWOT",
            "Ứng dụng di động cảnh báo lũ cho người dân",
        ],
        explain="Hydroweb-next giúp người dùng lấy chuỗi thời gian mực nước mà không cần tự xử lý dữ liệu thô.",
    ),
    dict(
        id="hydroweb-speaker",
        topic="Hydroweb-next",
        question="Ai trình bày phần giới thiệu và thực hành Hydroweb-next trong chương trình VSEO6?",
        correct="Charlotte Emery",
        distractors=["Jacques Verron", "Ariel Blanco", "Binh Pham Duc"],
        explain="Charlotte Emery (LEGOS/CNES) phụ trách buổi sáng thứ Năm 10/9 về Hydroweb-next.",
    ),
    # --- Data assimilation ---
    dict(
        id="da-def",
        topic="Data assimilation",
        question="Data assimilation (đồng hóa dữ liệu) trong bối cảnh khóa học là gì?",
        correct="Kết hợp có trọng số giữa đầu ra mô hình số và quan sát thực đo để ước lượng trạng thái hệ thống chính xác hơn",
        distractors=[
            "Việc gộp nhiều ảnh vệ tinh khác nhau thành một ảnh có độ phân giải cao hơn",
            "Quá trình hiệu chỉnh quỹ đạo vệ tinh cho đúng với lịch bay dự kiến",
            "Kỹ thuật nén dữ liệu vệ tinh để giảm dung lượng lưu trữ",
        ],
        explain="Data assimilation dùng kỹ thuật như Kalman filter/Ensemble Kalman Filter, trọng số theo độ bất định mỗi nguồn.",
    ),
    dict(
        id="da-speaker",
        topic="Data assimilation",
        question="Ai là nhà khoa học kỳ cựu về đồng hóa dữ liệu hải dương học, giảng nguyên lý data assimilation trong VSEO6?",
        correct="Jacques Verron",
        distractors=["Adrien Paris", "Daniel Moreira", "Denis Fourmeau"],
        explain="Jacques Verron (CNRS/LEGOS) là người đặt nền móng đồng hóa dữ liệu altimetry vào mô hình đại dương.",
    ),
    dict(
        id="da-technique",
        topic="Data assimilation",
        question="Kỹ thuật toán học kinh điển nào thường dùng trong đồng hóa dữ liệu hải dương/thủy văn?",
        correct="Kalman filter / Ensemble Kalman Filter",
        distractors=[
            "Thuật toán mã hóa RSA",
            "Biến đổi Fourier nhanh (FFT) thuần túy",
            "Cây quyết định (decision tree)",
        ],
        explain="Verron là người tiên phong áp dụng (Ensemble) Kalman Filter cho đồng hóa dữ liệu altimetry.",
    ),
    # --- Transboundary / MRC ---
    dict(
        id="transboundary-def",
        topic="Quản lý xuyên biên giới",
        question="Tại sao dữ liệu vệ tinh đặc biệt hữu ích cho quản lý sông xuyên biên giới như Mekong?",
        correct="Vì nó cung cấp nguồn quan sát trung lập, nhất quán xuyên biên giới, không phụ thuộc việc các quốc gia chia sẻ dữ liệu in-situ",
        distractors=[
            "Vì dữ liệu vệ tinh luôn chính xác hơn tuyệt đối so với trạm đo tại chỗ",
            "Vì chỉ có vệ tinh mới đo được các con sông có chiều rộng lớn hơn 1km",
            "Vì Mekong River Commission sở hữu vệ tinh riêng của mình",
        ],
        explain="Dữ liệu in-situ thường không được chia sẻ đầy đủ xuyên biên giới vì lý do chủ quyền/an ninh nước.",
    ),
    dict(
        id="mrc-def",
        topic="Tổ chức",
        question="MRC là viết tắt của tổ chức nào, và vai trò của nó trong VSEO6 là gì?",
        correct="Mekong River Commission — tổ chức liên chính phủ quản lý sông Mê Kông xuyên biên giới",
        distractors=[
            "Marine Remote sensing Center — trung tâm viễn thám biển của Philippines",
            "Ministry of Rural and Climate affairs — bộ quản lý khí hậu Việt Nam",
            "Mekong Research Consortium — nhóm nghiên cứu học thuật tư nhân",
        ],
        explain="MRC là tổ chức liên chính phủ, đại diện bởi Mathias Boun Hen trong phần giới thiệu tổ chức.",
    ),
    # --- Organizations ---
    dict(
        id="org-usth",
        topic="Tổ chức",
        question="USTH trong VSEO6 đóng vai trò gì và ai là đại diện nghiên cứu chính?",
        correct="Đơn vị Việt Nam về viễn thám nước, đại diện bởi TS. Binh Pham Duc",
        distractors=[
            "Cơ quan vũ trụ quốc gia Việt Nam, đại diện bởi Pham Thi Mai Thy",
            "Tổ chức tài trợ tài chính chính cho toàn bộ khóa học",
            "Đơn vị vận hành vệ tinh SWOT tại Đông Nam Á",
        ],
        explain="USTH (Đại học Khoa học & Công nghệ Hà Nội) — Binh Pham Duc nghiên cứu viễn thám hồ/sông tại Việt Nam.",
    ),
    dict(
        id="org-cnes",
        topic="Tổ chức",
        question="CNES là cơ quan vũ trụ của quốc gia nào, và liên quan gì đến SWOT?",
        correct="Pháp — CNES đồng vận hành sứ mệnh SWOT cùng NASA và vận hành Hydroweb-next",
        distractors=[
            "Việt Nam — CNES là tên cũ của VNSC",
            "Philippines — CNES hợp tác với PhilSA đo cỏ biển",
            "Canada — CNES tương đương với CSA",
        ],
        explain="CNES (Centre National d'Études Spatiales) là cơ quan vũ trụ Pháp.",
    ),
    dict(
        id="org-vnsc",
        topic="Tổ chức",
        question="VNSC là gì?",
        correct="Vietnam National Space Center — Trung tâm Vũ trụ Việt Nam",
        distractors=[
            "Vietnam Natural Sciences Council — hội đồng khoa học tự nhiên Việt Nam",
            "Viện Nghiên cứu Sông Cửu Long",
            "Một công ty tư nhân về ảnh vệ tinh thương mại",
        ],
        explain="Đại diện VNSC trong chương trình khai mạc là Pham Thi Mai Thy.",
    ),
    dict(
        id="org-psa",
        topic="Tổ chức",
        question="PSA/PhilSA trong chương trình VSEO6 là cơ quan của quốc gia nào và đại diện là ai?",
        correct="Philippines (Philippine Space Agency) — đại diện Ariel Blanco",
        distractors=[
            "Thái Lan (Public Space Agency) — đại diện Sabrine Amzil",
            "Indonesia (Pacific Space Alliance) — đại diện Daniel Moreira",
            "Nhật Bản (Pacific Satellite Association) — đại diện Denis Fourmeau",
        ],
        explain="Ariel Blanco là Director IV/PhilSA, chuyên viễn thám biển/nước (seagrass, coral bleaching).",
    ),
    # --- Program / schedule ---
    dict(
        id="prog-day1",
        topic="Chương trình",
        question="Ngày đầu tiên (thứ Hai 7/9) của VSEO6 tập trung chủ yếu vào nội dung nào (buổi chiều)?",
        correct="Tổng quan sứ mệnh Nadir altimetry và thực hành tải/phân tích dữ liệu Nadir",
        distractors=[
            "Thực địa quan sát mực nước hồ chứa",
            "Giới thiệu và thực hành Hydroweb-next",
            "Bàn tròn tổng kết và bế mạc khóa học",
        ],
        explain="Buổi sáng thứ Hai là khai mạc + giới thiệu tổ chức; buổi chiều là Nadir altimetry.",
    ),
    dict(
        id="prog-day3",
        topic="Chương trình",
        question="Hoạt động thực địa (field trip) trong VSEO6 diễn ra vào ngày nào, nội dung gì?",
        correct="Thứ Tư 9/9 — quan sát mực nước hồ chứa tại thực địa",
        distractors=[
            "Thứ Ba 8/9 — khảo sát vùng ngập lũ ở đồng bằng sông Cửu Long",
            "Thứ Sáu 11/9 — tham quan trụ sở Mekong River Commission",
            "Thứ Hai 7/9 — tham quan phòng thí nghiệm ICISE",
        ],
        explain="Sáng thứ Tư (9/9) dành trọn cho thực địa hồ chứa, chiều chuyển sang lý thuyết mô hình thủy văn.",
    ),
    dict(
        id="prog-day5",
        topic="Chương trình",
        question="Chủ đề chính của ngày cuối (thứ Sáu 11/9) là gì?",
        correct="Giám sát lũ lụt và quản lý thảm họa, kèm bài tập tình huống lũ lụt thực tế",
        distractors=[
            "Giới thiệu tổng quan sứ mệnh SWOT",
            "Nguyên lý đồng hóa dữ liệu cơ bản",
            "Khai mạc và giới thiệu 6 tổ chức đối tác",
        ],
        explain="Sabrine Amzil và Adrien Paris giảng flood monitoring buổi sáng, bàn tròn bế mạc buổi chiều.",
    ),
    dict(
        id="prog-swot-day",
        topic="Chương trình",
        question="Chủ đề SWOT mission được giảng dạy chính vào ngày nào trong tuần?",
        correct="Thứ Ba 8/9",
        distractors=["Thứ Hai 7/9", "Thứ Tư 9/9", "Thứ Năm 10/9"],
        explain="Daniel Moreira, Sabrine Amzil, Binh Pham Duc giảng tổng quan SWOT sáng thứ Ba.",
    ),
    # --- Lecturers ---
    dict(
        id="lect-adrien",
        topic="Giảng viên",
        question="Adrien Paris có nền tảng học thuật ban đầu là gì trước khi chuyển sang thủy văn không gian?",
        correct="Kỹ sư cơ khí (tốt nghiệp ENSAM)",
        distractors=[
            "Kỹ sư hàng không vũ trụ tại CNES",
            "Bác sĩ thú y chuyên về sinh thái sông",
            "Chuyên gia công nghệ thông tin tại Google",
        ],
        explain="Adrien Paris tốt nghiệp ENSAM (cơ khí) rồi chuyển hướng nghiên cứu thủy văn/altimetry.",
    ),
    dict(
        id="lect-laetitia",
        topic="Giảng viên",
        question="Dr. Laetitia Gal, người điều phối chính VSEO6, thuộc tổ chức nào và từng tham gia hoạt động gì với SWOT?",
        correct="Hydro Matters — tham gia hoạt động cal/val (hiệu chỉnh/xác thực) SWOT tại Brazil",
        distractors=[
            "NASA JPL — thiết kế phần cứng vệ tinh SWOT",
            "Mekong River Commission — vận hành trạm đo tại Lào",
            "PhilSA — lập bản đồ cỏ biển ở Philippines",
        ],
        explain="Laetitia Gal (Hydro Matters) khảo sát địa hình hồ chứa nông nghiệp bán khô hạn tại Brazil cho SWOT cal/val.",
    ),
    dict(
        id="lect-binh",
        topic="Giảng viên",
        question="TS. Binh Pham Duc (USTH) từng công bố nghiên cứu giám sát hồ nào bằng dữ liệu vệ tinh?",
        correct="Hồ Tonle Sap (Campuchia) và hồ chứa Thác Mơ (Việt Nam)",
        distractors=[
            "Hồ Baikal (Nga) và hồ Titicaca (Peru/Bolivia)",
            "Hồ Victoria (Đông Phi) và hồ Chad",
            "Hồ Geneva (Thụy Sĩ) và hồ Como (Ý)",
        ],
        explain="Binh Pham Duc công bố về Tonle Sap (Sentinel-1 + altimetry) và Thác Mơ (Remote Sensing 2022).",
    ),
]
