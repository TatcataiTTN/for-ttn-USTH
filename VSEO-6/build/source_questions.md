# Perspective 1 — Nadir Satellite Altimetry (Q1–Q8)

### Q1. Nguyên lý cơ bản của radar altimetry nadir là gì?
A. Đo thời gian bay đi–về của xung radar phát thẳng xuống (nadir) để tính khoảng cách vệ tinh–mặt nước
B. Đo cường độ ánh sáng phản xạ từ mặt nước bằng cảm biến quang học
C. Đo nhiệt độ bề mặt nước bằng cảm biến hồng ngoại nhiệt
D. Đo độ mặn nước bằng cảm biến vi sóng thụ động
**Answer: A.** **Framework:** Altimetry nadir = radar chủ động đo time-of-flight của xung phát thẳng xuống, suy ra khoảng cách rồi ra cao độ mặt nước.

### Q2. "Virtual station" trong nadir altimetry là gì?
A. Trạm khí tượng ảo mô phỏng bằng AI
B. Điểm giao cắt giữa vệt bay (ground track) của vệ tinh và một con sông/hồ, nơi chuỗi thời gian mực nước được trích xuất
C. Trạm đo mưa vệ tinh
D. Trung tâm điều khiển mặt đất của vệ tinh
**Answer: B.** **Framework:** Vì nadir chỉ đo dọc một đường hẹp, dữ liệu thủy văn chỉ có tại các điểm vệt bay cắt ngang sông/hồ — gọi là virtual station.

### Q3. Hạn chế chính của nadir altimetry so với công nghệ wide-swath (như SWOT) là gì?
A. Không đo được cao độ tuyệt đối
B. Độ phủ không gian thưa — chỉ đo tại các điểm vệt bay cắt sông, không cho ảnh 2D toàn bộ mặt nước
C. Chỉ hoạt động ban ngày
D. Không thể đo hồ, chỉ đo sông
**Answer: B.** **Framework:** Nadir cho time series tại điểm rời rạc; wide-swath (SWOT/KaRIn) cho ảnh 2D liên tục của mặt nước.

### Q4. Các sứ mệnh nadir altimetry tiêu biểu trong lịch sử gồm:
A. Landsat, MODIS, VIIRS
B. TOPEX/Poseidon, Jason series, Sentinel-6
C. GRACE, GRACE-FO
D. QuikSCAT, ASCAT
**Answer: B.** **Framework:** Chuỗi TOPEX/Poseidon → Jason-1/2/3 → Sentinel-6 là dòng sứ mệnh altimetry nadir đại dương/lục địa kế thừa liên tục từ 1992.

### Q5. Chu kỳ lặp lại (revisit) của một vệ tinh nadir altimetry quyết định điều gì?
A. Độ phân giải không gian ngang của ảnh
B. Tần suất một virtual station có thêm một điểm dữ liệu mới trong chuỗi thời gian mực nước
C. Màu sắc hiển thị trên bản đồ
D. Độ chính xác đo độ mặn
**Answer: B.** **Framework:** Quỹ đạo lặp cố định (vd 10 hoặc 35 ngày) quyết định tần suất lấy mẫu time series tại mỗi virtual station.

### Q6. Trong chương trình VSEO6, buổi "Tổng quan sứ mệnh Nadir / Dữ liệu" do ai trình bày?
A. Charlotte Emery, Jacques Verron
B. Adrien Paris, Laetitia Gal
C. Daniel Moreira, Sabrine Amzil
D. Ariel Blanco, Mathias Boun Hen
**Answer: B.** **Framework:** Theo chương trình ngày Thứ Hai 7/9, phiên 13:30–15:00 "Tổng quan sứ mệnh Nadir" do Adrien Paris và Laetitia Gal trình bày.

### Q7. Sản phẩm chính rút ra từ dữ liệu nadir altimetry cho một con sông là gì?
A. Bản đồ thực vật ven sông
B. Chuỗi thời gian cao độ mực nước tại virtual station
C. Nhiệt độ nước theo độ sâu
D. Tốc độ dòng chảy bề mặt tức thời trên toàn bộ chiều rộng sông
**Answer: B.** **Framework:** Sản phẩm cốt lõi của nadir altimetry thủy văn là time series mực nước (water level) tại từng virtual station.

### Q8. Vì sao dữ liệu in-situ (trạm đo thủy văn mặt đất) ngày càng khan hiếm, khiến vai trò của nadir altimetry tăng lên?
A. Vì trạm đo mặt đất bị cấm trên toàn cầu
B. Vì chi phí vận hành/bảo trì mạng lưới trạm đo giảm dần theo thời gian ở nhiều nước, và chia sẻ dữ liệu xuyên biên giới gặp rào cản chính trị
C. Vì vệ tinh rẻ hơn xây trạm đo 100 lần
D. Vì trạm đo mặt đất không đo được mực nước
**Answer: B.** **Framework:** Theo nghiên cứu của A. Paris và cộng sự, mạng lưới in-situ suy giảm và rào cản chia sẻ dữ liệu xuyên biên giới là động lực chính thúc đẩy altimetry vệ tinh thay thế/bổ sung.

# Perspective 2 — SWOT Mission (Q9–Q18)

### Q9. SWOT là viết tắt của cụm từ nào?
A. Satellite Water Ocean Tracking
B. Surface Water and Ocean Topography
C. Surface Weather Observation Technology
D. Space Water Optical Telemetry
**Answer: B.** **Framework:** SWOT = Surface Water and Ocean Topography, sứ mệnh hợp tác NASA–CNES.

### Q10. SWOT là hợp tác giữa các cơ quan không gian nào?
A. NASA và CNES (có đóng góp CSA, UKSA)
B. Chỉ riêng ESA
C. JAXA và ISRO
D. Roscosmos và CNSA
**Answer: A.** **Framework:** SWOT do NASA và CNES phát triển chính, với đóng góp của Canadian Space Agency (CSA) và UK Space Agency (UKSA).

### Q11. Thiết bị chủ lực của SWOT là gì và có đặc điểm gì đột phá?
A. LIDAR quang học đo độ cao mây
B. KaRIn — radar giao thoa băng Ka, đo wide-swath (dải rộng 120 km) thay vì chỉ một đường nadir
C. Cảm biến hồng ngoại nhiệt độ nước
D. Máy đo gió tán xạ (scatterometer)
**Answer: B.** **Framework:** KaRIn (Ka-band Radar Interferometer) là bước nhảy công nghệ: đo đồng thời cao độ, độ dốc, độ rộng mặt nước trên dải quét rộng, không chỉ một đường hẹp như altimetry cổ điển.

### Q12. Dải quét (swath) của KaRIn trên SWOT rộng bao nhiêu và có đặc điểm gì ở giữa?
A. 500 km, phủ liên tục không gián đoạn
B. 120 km tổng cộng (hai dải 50 km hai bên), có khoảng trống (gap) ở giữa dọc theo vệt bay (nadir track)
C. 10 km, chỉ đo được sông rất hẹp
D. 1000 km, toàn cầu mỗi lần bay
**Answer: B.** **Framework:** KaRIn quét hai dải 50 km hai bên vệt bay, tổng 120 km, với một khoảng trống ở giữa đúng tại đường nadir.

### Q13. SWOT phóng vào thời gian nào và bằng phương tiện phóng nào?
A. 16/12/2022, tên lửa SpaceX Falcon 9
B. 2010, tàu con thoi Space Shuttle
C. 2018, tên lửa Ariane 5
D. 2025, tên lửa Long March
**Answer: A.** **Framework:** SWOT phóng ngày 16/12/2022 bằng Falcon 9 từ Vandenberg.

### Q14. Ba đại lượng chính mà KaRIn đo đồng thời trên mặt nước sông/hồ là gì?
A. Nhiệt độ, độ mặn, độ đục
B. Cao độ (elevation), độ dốc (slope), độ rộng (width) mặt nước
C. Gió, sóng, dòng chảy ngầm
D. pH, oxy hòa tan, chất diệp lục
**Answer: B.** **Framework:** Bộ ba elevation–slope–width là đầu vào để tính lưu lượng dòng chảy (discharge) qua công thức thủy lực kiểu Manning.

### Q15. Vì sao SWOT có thể ước tính được lưu lượng dòng chảy (discharge) sông mà nadir altimetry cổ điển không làm được trực tiếp?
A. Vì SWOT đo trực tiếp tốc độ dòng chảy bằng Doppler
B. Vì SWOT đo đồng thời cao độ + độ dốc + độ rộng, đủ input cho công thức thủy lực ước tính discharge; nadir chỉ có cao độ tại điểm rời rạc
C. Vì SWOT bay thấp hơn nên nhìn rõ dòng nước hơn
D. Vì SWOT dùng camera quang học độ phân giải cao
**Answer: B.** **Framework:** Discharge ước tính gián tiếp qua mô hình thủy lực cần tối thiểu elevation, slope, width — chỉ wide-swath altimetry mới cung cấp đủ cả ba theo không gian.

### Q16. Sản phẩm dữ liệu SWOT cấp L2 HR liên quan sông thường được gọi là gì?
A. RiverSP / PIXC (pixel cloud)
B. MODIS NDVI
C. Sentinel-1 GRD
D. Landsat Collection 2
**Answer: A.** **Framework:** RiverSP (River Single-Pass) và PIXC (pixel cloud) là các sản phẩm L2 HR chính của SWOT dùng cho phân tích sông.

### Q17. Chu kỳ lặp lại quỹ đạo khoa học của SWOT là bao nhiêu ngày?
A. 5 ngày
B. 21 ngày
C. 100 ngày
D. 365 ngày
**Answer: B.** **Framework:** Quỹ đạo khoa học SWOT có chu kỳ lặp 21 ngày, phủ ~0.5% diện tích Trái Đất mỗi giờ.

### Q18. Theo chương trình VSEO6, ai trình bày "Tổng quan SWOT + sản phẩm dữ liệu"?
A. Jean Tran Thanh Van, Denis Fourmeau
B. Daniel Moreira, Sabrine Amzil, Binh Pham Duc
C. Charlotte Emery, Jacques Verron
D. Pham Thi Mai Thy, Ariel Blanco
**Answer: B.** **Framework:** Sáng Thứ Ba 8/9 (08:30–10:00), Daniel Moreira, Sabrine Amzil và Binh Pham Duc trình bày tổng quan SWOT.

# Perspective 3 — Copernicus Programme & Sentinel Data (Q19–Q24)

### Q19. Copernicus là chương trình quan sát Trái Đất của tổ chức nào?
A. NASA (Hoa Kỳ)
B. Liên minh Châu Âu (EU/ESA)
C. Cơ quan Vũ trụ Nga (Roscosmos)
D. Cơ quan Vũ trụ Nhật Bản (JAXA)
**Answer: B.** **Framework:** Copernicus là chương trình quan sát Trái Đất hàng đầu của Liên minh Châu Âu, vận hành với ESA.

### Q20. Vệ tinh Sentinel-1 sử dụng loại cảm biến nào, phù hợp cho việc gì trong giám sát nước?
A. Cảm biến quang học VNIR, chỉ dùng ban ngày quang mây
B. Radar khẩu độ tổng hợp (SAR), hoạt động cả ngày/đêm và xuyên mây — dùng lập bản đồ diện tích ngập lụt
C. LIDAR, đo độ cao rừng
D. Cảm biến hồng ngoại nhiệt, đo nhiệt độ mặt biển
**Answer: B.** **Framework:** SAR của Sentinel-1 không phụ thuộc ánh sáng mặt trời hay mây — lý tưởng để lập bản đồ ngập lụt nhanh trong điều kiện thời tiết xấu (thường đi kèm mưa lớn/bão).

### Q21. Sản phẩm "SurfWater" trong hệ sinh thái dữ liệu Theia/hydroweb.next được tạo từ nguồn dữ liệu vệ tinh nào?
A. Sentinel-1 và Sentinel-2
B. Landsat 5 only
C. SWOT KaRIn only
D. GRACE-FO
**Answer: A.** **Framework:** SurfWater (diện tích mặt nước) do các trung tâm sản xuất Theia vận hành từ ảnh Sentinel-1 (SAR) và Sentinel-2 (quang học).

### Q22. Sentinel-6 (Michael Freilich) thuộc loại altimetry nào?
A. Wide-swath giống SWOT/KaRIn
B. Nadir altimetry, kế thừa dòng Jason
C. Altimetry laser (LIDAR)
D. Altimetry thụ động không phát tín hiệu
**Answer: B.** **Framework:** Sentinel-6 tiếp nối chuỗi TOPEX–Jason, là radar altimeter nadir băng Ku/C, không phải công nghệ wide-swath như SWOT.

### Q23. Vì sao dữ liệu Copernicus (Sentinel) được xem là phù hợp cho các nước đang phát triển như Việt Nam trong giám sát tài nguyên nước?
A. Vì chỉ Việt Nam mới được quyền truy cập
B. Vì chính sách mở, miễn phí, độ phủ toàn cầu và tần suất lặp lại thường xuyên
C. Vì Copernicus chỉ hoạt động ở châu Âu
D. Vì dữ liệu Copernicus có độ phân giải thấp hơn ảnh máy bay nên dễ xử lý
**Answer: B.** **Framework:** Chính sách "free & open data" của Copernicus là lý do chính khiến nó trở thành nguồn dữ liệu chủ lực cho các trung tâm ít nguồn lực.

### Q24. Trong bối cảnh VSEO6, dữ liệu Copernicus được kết hợp cùng SWOT để phục vụ ứng dụng nào là chủ yếu?
A. Giám sát núi lửa
B. Giám sát lũ lụt và quản lý thảm họa (kết hợp SAR Sentinel-1 + wide-swath SWOT)
C. Dự báo động đất
D. Giám sát rừng nhiệt đới Amazon riêng biệt, không liên quan nước
**Answer: B.** **Framework:** Chương trình VSEO6 nêu rõ ứng dụng giám sát lũ lụt dựa trên kết hợp SAR (mở rộng vùng ngập) và SWOT (cao độ/độ dốc mặt nước).

# Perspective 4 — hydroweb.next Platform (Q25–Q30)

### Q25. hydroweb.next là nền tảng gì và do tổ chức nào phát triển?
A. Nền tảng WebGIS mở cho thủy văn học, do CNES/Theia phát triển
B. Ứng dụng thời tiết thương mại của tư nhân Mỹ
C. Cơ sở dữ liệu bản đồ địa chính Việt Nam
D. Phần mềm mô phỏng khí hậu của NOAA
**Answer: A.** **Framework:** hydroweb.next là nền tảng open-data WebGIS do CNES phối hợp hạ tầng Data Terra/Theia xây dựng, dành cho cộng đồng thủy văn học.

### Q26. hydroweb.next ra đời gắn liền với chương trình nào?
A. Chương trình Apollo
B. Chương trình SWOT Early Adopters
C. Chương trình ISS
D. Chương trình Artemis
**Answer: B.** **Framework:** Nền tảng phát triển nhờ động lực từ chương trình SWOT Early Adopters và hạ tầng Theia/Data Terra.

### Q27. Mục tiêu chính hydroweb.next muốn giải quyết là gì?
A. Tăng độ phân giải ảnh vệ tinh lên gấp 10 lần
B. Gỡ bỏ rào cản: định dạng dữ liệu không đồng nhất, điểm truy cập phân tán, chi phí xử lý cao
C. Thay thế hoàn toàn các mô hình thủy văn số trị
D. Cung cấp dịch vụ dự báo thời tiết 15 ngày
**Answer: B.** **Framework:** hydroweb.next tập trung hóa dữ liệu, chuẩn hóa định dạng, và giảm chi phí xử lý cho nhà thủy văn học — đúng 3 rào cản được nêu trong tài liệu công bố nền tảng.

### Q28. Sản phẩm "THEIA river/lake water level" trên hydroweb.next có đặc điểm gì về độ dài chuỗi thời gian?
A. Chỉ có dữ liệu 1 năm gần nhất
B. Một số chuỗi có thể dài hơn 30 năm
C. Chỉ cập nhật 1 lần/năm
D. Không có dữ liệu lịch sử, chỉ real-time
**Answer: B.** **Framework:** Nhờ kế thừa liên tục các sứ mệnh nadir altimetry từ TOPEX/Poseidon 1992, một số chuỗi mực nước sông/hồ trên hydroweb.next dài hơn 30 năm.

### Q29. Ngoài mực nước sông/hồ, hydroweb.next còn cung cấp sản phẩm nào sau đây?
A. Let It Snow (tuyết phủ) và OBS2CO (chất lượng nước) từ Sentinel-2
B. Dự báo bão 10 ngày
C. Bản đồ địa chấn
D. Dữ liệu giá nông sản
**Answer: A.** **Framework:** Ngoài SurfWater/water level, hydroweb.next tích hợp Let It Snow (tuyết) và OBS2CO (chất lượng nước) — đều xử lý từ Sentinel-2.

### Q30. Theo chương trình VSEO6, ai giới thiệu hydroweb.next?
A. Charlotte Emery
B. Jean Tran Thanh Van
C. Ariel Blanco
D. Mathias Boun Hen
**Answer: A.** **Framework:** Sáng Thứ Năm 10/9 (08:30–10:00), Charlotte Emery giới thiệu hydroweb.next.

# Perspective 5 — Data Assimilation trong Thủy văn học (Q31–Q38)

### Q31. Data assimilation (đồng hóa dữ liệu) trong thủy văn học là gì?
A. Kỹ thuật kết hợp quan trắc vệ tinh với mô hình số trị để hiệu chỉnh trạng thái/tham số mô hình theo thời gian thực
B. Kỹ thuật nén dữ liệu ảnh vệ tinh để giảm dung lượng lưu trữ
C. Kỹ thuật mã hóa dữ liệu để bảo mật truyền tin vệ tinh
D. Kỹ thuật ghép nhiều ảnh vệ tinh thành một ảnh toàn cảnh (mosaic)
**Answer: A.** **Framework:** Data assimilation = kết hợp có trọng số giữa quan trắc và dự báo mô hình để giảm sai số ước tính trạng thái hệ thống (ở đây là mực nước/lưu lượng).

### Q32. Phương pháp đồng hóa dữ liệu phổ biến được nền tảng SEQUOIA (LEGOS) sử dụng là gì?
A. Random Forest
B. Ensemble Kalman Filter (EnKF)
C. Support Vector Machine
D. Fourier Transform thuần túy
**Answer: B.** **Framework:** SEQUOIA tại LEGOS dùng kernel Ensemble Kalman Filter (EnKF) — phương pháp đồng hóa dựa trên tập hợp (ensemble) các mô phỏng để ước tính sai số.

### Q33. Trong nghiên cứu của Charlotte Emery và cộng sự (HESS 2020), dữ liệu gì được đồng hóa vào mô hình định tuyến dòng chảy quy mô lớn?
A. Dữ liệu nhiệt độ không khí
B. Dị thường cao độ mặt nước từ wide-swath altimetry (SWOT-like)
C. Dữ liệu độ ẩm đất từ radar
D. Dữ liệu gió bề mặt biển
**Answer: B.** **Framework:** Nghiên cứu "Assimilation of wide-swath altimetry water elevation anomalies..." đồng hóa dị thường cao độ mặt nước để hiệu chỉnh tham số mô hình river routing quy mô lớn.

### Q34. Vì sao cần đồng hóa dữ liệu thay vì chỉ chạy mô hình thủy văn thuần túy (không dùng quan trắc)?
A. Vì mô hình thuần túy luôn chính xác hơn quan trắc nên không cần
B. Vì mô hình số trị luôn tích lũy sai số theo thời gian do bất định về tham số/điều kiện biên; quan trắc vệ tinh giúp "kéo" mô hình về gần thực tế hơn
C. Vì luật pháp quốc tế yêu cầu bắt buộc dùng vệ tinh
D. Vì mô hình thuần túy không thể chạy trên máy tính hiện đại
**Answer: B.** **Framework:** Mọi mô hình số trị có sai số tích lũy; đồng hóa định kỳ đưa mô hình về gần trạng thái quan trắc thực, cải thiện độ tin cậy dự báo.

### Q35. Công trình của Jacques Verron về "Wide-Swath Altimetric Satellite Data Assimilation With Correlated-Error Reduction" (Frontiers in Marine Science, 2020) giải quyết vấn đề gì đặc thù của dữ liệu wide-swath?
A. Sai số ngẫu nhiên độc lập từng điểm ảnh, dễ lọc bằng trung bình đơn giản
B. Sai số có cấu trúc không gian (correlated/structured errors) đặc trưng của swath rộng, cần kỹ thuật giảm sai số chuyên biệt
C. Thiếu hoàn toàn dữ liệu ở vùng xích đạo
D. Độ trễ truyền dữ liệu vệ tinh quá lớn (>24h)
**Answer: B.** **Framework:** Dữ liệu wide-swath (KaRIn) có sai số cấu trúc theo không gian (không độc lập từng pixel như nadir), nên cần các kỹ thuật giảm sai số tương quan chuyên biệt trước khi đồng hóa.

### Q36. "Ocean Next" và LEGOS, nơi Jacques Verron công tác, đặt tại thành phố nào của Pháp?
A. Paris
B. Toulouse
C. Grenoble
D. Marseille
**Answer: C.** **Framework:** Jacques Verron gắn với Université Grenoble Alpes / CNRS / IRD / IGE và Ocean Next, đều tại Grenoble (LEGOS ở Toulouse là nơi nền tảng SEQUOIA phát triển).

### Q37. Theo chương trình VSEO6, buổi "Nguyên lý đồng hóa dữ liệu" do ai đồng trình bày?
A. Charlotte Emery, Jacques Verron
B. Adrien Paris, Laetitia Gal
C. Binh Pham Duc, Linda Tomasini
D. Sabrine Amzil, Ariel Blanco
**Answer: A.** **Framework:** Chiều Thứ Năm 10/9 (13:30–15:00), Charlotte Emery và Jacques Verron cùng trình bày nguyên lý đồng hóa dữ liệu.

### Q38. Đồng hóa dữ liệu altimetry mang lại lợi ích thực tiễn nào rõ nhất cho quản lý tài nguyên nước xuyên biên giới?
A. Giảm giá vé máy bay khảo sát thực địa
B. Cải thiện độ tin cậy ước tính lưu lượng/mực nước ở các đoạn sông thiếu trạm đo mặt đất hoặc số liệu không được chia sẻ giữa các quốc gia
C. Tăng tốc độ truyền hình ảnh vệ tinh về mặt đất
D. Loại bỏ hoàn toàn nhu cầu mô hình thủy văn
**Answer: B.** **Framework:** Ở các lưu vực xuyên biên giới (như Mekong), số liệu in-situ thường không được chia sẻ đầy đủ — đồng hóa dữ liệu vệ tinh độc lập giúp các bên có ước tính đáng tin cậy hơn mà không phụ thuộc số liệu quốc gia khác.

# Perspective 6 — Flood Monitoring & Transboundary River Management (Q39–Q44)

### Q39. Vì sao SAR Sentinel-1 thường được ưu tiên hơn ảnh quang học để lập bản đồ ngập lụt khẩn cấp?
A. SAR có độ phân giải màu tốt hơn
B. SAR xuyên qua mây và không cần ánh sáng mặt trời, trong khi lũ lụt thường đi kèm mây dày/mưa lớn khiến ảnh quang học vô dụng
C. SAR rẻ hơn ảnh quang học
D. SAR chỉ hoạt động vào ban đêm nên tránh nhiễu mặt trời
**Answer: B.** **Framework:** Điều kiện thời tiết khi lũ xảy ra (mây dày, mưa) làm ảnh quang học không dùng được; SAR không phụ thuộc ánh sáng/mây nên là công cụ chính cho flood mapping khẩn cấp.

### Q40. MRC (Mekong River Commission) gồm những quốc gia thành viên nào?
A. Việt Nam, Lào, Campuchia, Thái Lan
B. Việt Nam, Trung Quốc, Myanmar, Thái Lan
C. Việt Nam, Lào, Campuchia, Trung Quốc
D. Thái Lan, Myanmar, Lào, Trung Quốc
**Answer: A.** **Framework:** MRC gồm 4 nước hạ lưu Mekong: Thái Lan, Lào, Campuchia, Việt Nam (Trung Quốc và Myanmar là đối tác đối thoại, không phải thành viên chính thức).

### Q41. Công cụ "Mekong Dam Monitor" sử dụng viễn thám để làm gì?
A. Dự báo giá điện thủy điện
B. Tạo "virtual gauge" tại đập/hồ chứa để theo dõi độc lập chỉ số môi trường/thủy văn hàng tuần trên toàn lưu vực
C. Giám sát chất lượng không khí quanh đập
D. Kiểm tra kết cấu bê tông đập bằng radar xuyên đất
**Answer: B.** **Framework:** Mekong Dam Monitor dùng viễn thám/GIS tạo "virtual gauge" tại các đập, cung cấp báo cáo môi trường hàng tuần độc lập với số liệu do quốc gia vận hành đập cung cấp.

### Q42. Vì sao viễn thám vệ tinh đặc biệt có giá trị trong quản lý sông xuyên biên giới như Mekong?
A. Vì vệ tinh miễn phí hoàn toàn cho mọi ứng dụng
B. Vì nó cung cấp số liệu độc lập, nhất quán trên toàn lưu vực bất kể biên giới quốc gia, tăng minh bạch và năng lực đàm phán giữa các bên
C. Vì vệ tinh có thể thay thế hoàn toàn ngoại giao giữa các nước
D. Vì chỉ vệ tinh mới đo được nhiệt độ nước
**Answer: B.** **Framework:** Số liệu vệ tinh không phụ thuộc việc quốc gia thượng nguồn có chia sẻ số liệu in-situ hay không — tạo cơ sở minh bạch chung cho quản lý xuyên biên giới.

### Q43. Trong chương trình VSEO6, buổi "Giám sát lũ lụt & quản lý thảm họa" do ai trình bày?
A. Sabrine Amzil, Adrien Paris
B. Jean Tran Thanh Van, Denis Fourmeau
C. Pham Thi Mai Thy, Linda Tomasini
D. Jacques Verron, Charlotte Emery
**Answer: A.** **Framework:** Sáng Thứ Sáu 11/9 (08:30–10:00), Sabrine Amzil và Adrien Paris trình bày về giám sát lũ lụt và quản lý thảm họa.

### Q44. Dự án "StockWater" (CNES, SCO/SWOT Downstream) nhằm mục đích gì?
A. Giám sát dung tích nước trong các hồ chứa/đập
B. Sản xuất nước đóng chai từ nước biển
C. Theo dõi giá cổ phiếu ngành nước
D. Dự báo động đất gần đập thủy điện
**Answer: A.** **Framework:** StockWater do CNES chủ trì cùng CS-Group, SERTIT, CESBIO, GET, LISAH — xây hệ thống giám sát dung tích nước hồ chứa/đập dựa trên dữ liệu SWOT/vệ tinh.

# Perspective 7 — Tổ chức, Chương trình & Giảng viên VSEO6 (Q45–Q52)

### Q45. VSEO6 được tổ chức bởi đơn vị nào và có mối liên hệ gì với UNESCO?
A. Rencontres du Vietnam — tổ chức phi lợi nhuận, đối tác chính thức của UNESCO
B. Bộ Khoa học và Công nghệ Việt Nam trực tiếp tổ chức
C. NASA chi nhánh Đông Nam Á
D. Một trường đại học tư nhân của Singapore
**Answer: A.** **Framework:** Rencontres du Vietnam, sáng lập 1993 bởi GS. Trần Thanh Vân, là tổ chức phi lợi nhuận và đối tác chính thức UNESCO, đơn vị đứng sau ICISE và chuỗi VSEO.

### Q46. ICISE — nơi tổ chức VSEO6 — tọa lạc ở đâu và thành lập năm nào?
A. Hà Nội, thành lập 2005
B. Quy Nhơn, thành lập 2013
C. Đà Nẵng, thành lập 2010
D. TP. Hồ Chí Minh, thành lập 2018
**Answer: B.** **Framework:** ICISE (International Centre for Interdisciplinary Science Education) đặt tại Quy Nhơn, thành lập năm 2013 bởi Rencontres du Vietnam.

### Q47. Buổi thực địa (field trip) trong VSEO6 diễn ra vào ngày nào và nội dung gì?
A. Thứ Ba 8/9 — thăm trụ sở CNES tại Pháp
B. Thứ Tư 9/9 — quan sát mực nước hồ chứa thực địa
C. Thứ Sáu 11/9 — tham quan bảo tàng khoa học
D. Thứ Hai 7/9 — lặn biển Quy Nhơn
**Answer: B.** **Framework:** Sáng Thứ Tư 9/9 (08:00–12:00) là buổi thực địa quan sát mực nước hồ chứa, cầu nối giữa lý thuyết altimetry và thực hành ngoài trời.

### Q48. Trong phiên khai mạc, các tổ chức nào được giới thiệu (ngoài USTH)?
A. CNES, VNSC, PSA, MRC
B. NASA, ESA, JAXA, ISRO
C. UNDP, WHO, UNICEF
D. World Bank, IMF, ADB
**Answer: A.** **Framework:** Phiên 08:35–10:30 ngày khai mạc giới thiệu 5 tổ chức: USTH (Việt Nam), CNES (Pháp), VNSC (Việt Nam), PSA (Philippines), MRC (Mekong River Commission).

### Q49. Binh Pham Duc, giảng viên VSEO6, công tác tại đơn vị nào và có công bố tiêu biểu nào về Việt Nam?
A. USTH; nghiên cứu giám sát biến động hồ Tonle Sap và hồ Đại Lải bằng ảnh vệ tinh/altimetry
B. VNSC; nghiên cứu về vệ tinh viễn thông
C. CNES; nghiên cứu về đại dương Bắc Cực
D. MRC; nghiên cứu chính sách thương mại Mekong
**Answer: A.** **Framework:** Binh Pham Duc (USTH, lab Remosat) có công bố về giám sát Tonle Sap Lake (Sentinel-1 + altimetry) và Dai Lai Lake (Việt Nam) bằng đa nguồn viễn thám.

### Q50. Ariel Blanco, đại diện phía Philippines trong VSEO6, là chuyên gia về lĩnh vực nào?
A. Vật lý hạt nhân
B. Remote sensing hệ sinh thái ven biển (rừng ngập mặn, cỏ biển) tại Đại học Philippines Diliman
C. Kỹ thuật hàng không vũ trụ động cơ tên lửa
D. Kinh tế học tài nguyên nước
**Answer: B.** **Framework:** Ariel Blanco là Giáo sư Kỹ thuật Trắc địa tại UP Diliman, nổi bật với công trình về chỉ số thực vật rừng ngập mặn (MVI) và lập bản đồ cỏ biển bằng viễn thám.

### Q51. Đầu mối liên hệ chính thức cho câu hỏi/đăng ký VSEO6 là ai?
A. Dr. Laetitia Gal (laetitia.gal@hydro-matters.fr)
B. GS. Trần Thanh Vân trực tiếp qua điện thoại
C. Văn phòng tuyển sinh USTH
D. Đại sứ quán Pháp tại Hà Nội
**Answer: A.** **Framework:** Trang đăng ký VSEO6 nêu rõ liên hệ chính là Dr. Laetitia Gal, email laetitia.gal@hydro-matters.fr.

### Q52. Buổi cuối cùng của VSEO6 (chiều Thứ Sáu 11/9) có nội dung gì?
A. Thi trắc nghiệm tổng kết bắt buộc
B. Bàn tròn / phản hồi học viên / bế mạc
C. Chuyến bay tham quan bằng máy bay không người lái
D. Lễ trao giải cuộc thi lập trình
**Answer: B.** **Framework:** 13:30–15:00 ngày cuối là phiên bàn tròn, thu thập phản hồi học viên và bế mạc khóa học.
