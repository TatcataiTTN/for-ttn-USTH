# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from hx import *
from qcore import Bank, audit, balance_length
from sitelib import module_page

B=Bank('m4',seed=4)
SRC='Deng, Li, Li, Du, He (2026), arXiv:2602.04770v2, "Generative Modeling via Drifting" (full-text verify) + lịch sử generative model chuẩn ngành (Kingma&Welling 2013, Goodfellow 2014, Sohl-Dickstein 2015, Lipman 2022)'

B.add('"Pushforward" trong generative modeling, theo định nghĩa paper Drifting, nghĩa là gì?',
    'q = f#pε — mạng f biến đổi phân phối nguồn (noise) pε thành phân phối q, với mục tiêu q xấp xỉ phân phối dữ liệu p_data',
    ['f là một phép chiếu từ không gian 3D xuống 2D để giảm chiều dữ liệu','f#pε là ký hiệu cho đạo hàm của f theo tham số ε','Pushforward chỉ áp dụng được cho phân phối rời rạc, không áp dụng phân phối liên tục'],
    'Paper định nghĩa chính xác: với f:R^C→R^D, x=f(ε)~q, ta gọi q=f#pε là pushforward distribution của pε dưới f — mục tiêu generative modeling là tìm f sao cho f#pε ≈ p_data.',level=1,topic='Pushforward')
B.add('Diffusion Model và Flow Matching thực hiện pushforward theo cách nào, khác Drifting Model ra sao?',
    'Diffusion/Flow Matching thực hiện pushforward LẶP LẠI NHIỀU BƯỚC tại thời điểm inference (sinh mẫu); Drifting Model học sự tiến hoá của pushforward trong lúc HUẤN LUYỆN, nên chỉ cần 1 bước (1-NFE) khi inference',
    ['Diffusion không hề thực hiện pushforward, chỉ Drifting mới có khái niệm này','Cả hai đều cần đúng 1000 bước inference, không có sự khác biệt','Flow Matching chỉ áp dụng được cho dữ liệu dạng văn bản, không áp dụng ảnh'],
    'Đây là sự khác biệt triết lý cốt lõi: Diffusion/Flow Matching phân rã 1 phép biến đổi phức tạp thành NHIỀU bước nhỏ dễ học hơn, thực hiện LẶP LẠI khi sinh mẫu; Drifting chuyển sự "lặp lại" đó sang quá trình HUẤN LUYỆN (các iteration SGD), nên mạng f cuối cùng chỉ cần áp dụng 1 lần duy nhất để sinh mẫu.',level=2,topic='Drifting-vs-Diffusion')
B.add('"Drift" của một mẫu x tại iteration huấn luyện i, theo định nghĩa paper, là gì?',
    'Δxᵢ := f_{i+1}(ε) − f_i(ε) — độ dịch chuyển của mẫu do cập nhật tham số của mạng f qua 1 bước huấn luyện',
    ['Δxᵢ là nhiễu Gaussian cộng thêm vào x ở mỗi bước lấy mẫu','Δxᵢ là gradient của loss function theo tham số θ','Δxᵢ là sai số làm tròn số học khi tính trên GPU'],
    'Khi mạng f được cập nhật từ bước i sang i+1 (do SGD), một mẫu x=f_i(ε) cố định ε sẽ dịch chuyển thành f_{i+1}(ε) — paper gọi độ dịch chuyển này là "drift" của mẫu, hệ quả trực tiếp của việc cập nhật tham số, KHÔNG phải một bước lấy mẫu lặp riêng biệt.',level=2,topic='Drift-definition')
B.add('"Drifting field" Vp,q(x) được paper định nghĩa dưới dạng kỳ vọng nào?',
    'Vp,q(x) = E_{y+~p} E_{y-~q} [K(x, y+, y-)] — kỳ vọng của 1 kernel K theo cả phân phối đích p và phân phối hiện tại q',
    ['Vp,q(x) = p(x) - q(x) (hiệu trực tiếp 2 hàm mật độ)','Vp,q(x) = ∇log p(x) (score function của phân phối đích, giống diffusion)','Vp,q(x) là 1 hằng số không đổi cho mọi x'],
    'Paper định nghĩa trường drift qua kỳ vọng kép trên mẫu dương y+ từ p (thường là p_data) và mẫu âm y- từ q (phân phối hiện tại của mạng): Vp,q(x)=E_{y+~p}E_{y-~q}[K(x,y+,y-)] — khác hẳn score function ∇log p(x) của diffusion (không cần ước lượng gradient log-density).',level=2,topic='Drifting-field')
B.add('Tính chất "anti-symmetric" (Proposition 3.1) của trường drift, Vp,q(x) = −Vq,p(x), dẫn tới điều gì khi p=q?',
    'Khi p=q thì V=0 — các mẫu ngừng "trôi" (dừng cập nhật), đạt trạng thái cân bằng vì mạng đã tạo ra đúng phân phối dữ liệu',
    ['Khi p=q thì V tiến tới vô cực, mạng phát nổ (diverge)','Tính chất này chỉ đúng cho dữ liệu rời rạc, không đúng cho ảnh liên tục','Anti-symmetric nghĩa là trường luôn âm, không bao giờ dương'],
    'Đây là điều kiện "điểm cân bằng" cốt lõi của thiết kế: Vp,q=-Vq,p kéo theo V=0 khi q=p (đổi vai trò 2 phân phối giống nhau phải cho kết quả đối nhau, chỉ 0 thoả mãn cả 2 chiều) — đúng mục tiêu generative modeling: mạng "ngừng học thêm" khi đã khớp đúng phân phối dữ liệu.',level=3,topic='Theory')
B.add('Loss function huấn luyện Drifting Model dùng kỹ thuật "stop-gradient" ở đâu, và vì sao?',
    'Stop-gradient áp lên phần Vp,q(fθ(ε)) trong công thức loss — vì back-propagate trực tiếp qua 1 trường phụ thuộc vào phân phối (q) là rất khó/không khả thi',
    ['Stop-gradient áp lên toàn bộ input ε, khiến mạng không học được gì cả','Stop-gradient chỉ dùng khi huấn luyện trên GPU, không cần khi dùng CPU','Stop-gradient thay thế hoàn toàn cho thuật toán SGD, không cần tối ưu hoá nào khác'],
    'Vì V phụ thuộc vào q_θ (phân phối sinh ra bởi chính mạng đang huấn luyện) nên lan truyền gradient trực tiếp QUA V là không đơn giản (gradient qua một phân phối). Giải pháp: dùng stop-gradient trên phần "đích" (fθ(ε)+V), chỉ để gradient chảy qua fθ(ε) ở phần "dự đoán" — khiến việc huấn luyện trở thành bài toán hồi quy đơn giản: kéo fθ(ε) về gần đích đã bị "đóng băng gradient".',level=3,topic='Loss-function')
B.add('Trên benchmark ImageNet 256×256, paper Drifting đạt FID bao nhiêu ở cấu hình latent và pixel?',
    'FID 1.54 (latent) / 1.61 (pixel)',['FID 15.4 (latent) / 16.1 (pixel)','FID 0.154 (latent) / 0.161 (pixel)','FID không được báo cáo cho ImageNet, chỉ có CIFAR-10'],
    'Paper báo cáo FID 1.54 (không gian latent) và 1.61 (không gian pixel) trên ImageNet 256×256 — tốt nhất trong nhóm phương pháp sinh một bước (1-NFE) tại thời điểm công bố, cạnh tranh với các phương pháp đa bước.',level=1,topic='Benchmark')
B.add('VAE (Kingma & Welling, 2013) huấn luyện bằng cách tối ưu hoá đại lượng gì?',
    'ELBO (Evidence Lower Bound) — gồm 1 số hạng reconstruction loss và 1 số hạng KL divergence',['Chỉ tối ưu reconstruction loss thuần, không có số hạng nào khác','Adversarial loss giữa generator và discriminator (giống GAN)','Score matching loss (giống diffusion/score-based model)'],
    'VAE tối ưu ELBO = reconstruction loss (dữ liệu tái tạo gần dữ liệu gốc) + KL divergence (phân phối latent gần phân phối tiên nghiệm, thường Gaussian chuẩn) — khác biệt rõ với GAN (đối kháng) và Diffusion (score/denoising).',level=1,topic='Lineage-VAE')
B.add('GAN (Goodfellow et al., 2014) khác Drifting Model ở điểm nào về cách huấn luyện?',
    'GAN huấn luyện qua tối ưu hoá đối kháng (minimax) giữa generator và discriminator; Drifting KHÔNG dùng tối ưu hoá đối kháng, chỉ dùng 1 loss hồi quy đơn (có stop-gradient)',
    ['GAN và Drifting dùng chung đúng 1 loss function, không có khác biệt','GAN không có khái niệm generator, chỉ có discriminator','Drifting cũng cần 1 discriminator riêng như GAN'],
    'Bài báo Drifting nêu rõ: "unlike GANs, our method does not rely on adversarial optimization" — đây là một trong những điểm khác biệt được paper tự nhấn mạnh khi so sánh với GAN.',level=2,topic='Lineage-GAN')

print('M4 added:',len(B.items))
balance_length(B.items)
print('AUDIT (after balance):',audit(B.items))

parts=[
 dict(title='Lịch sử Generative Model: VAE → GAN → Flow',bullets=['VAE (ELBO)','GAN (đối kháng)','Normalizing Flows'],slides=[
   sl(table(['Phương pháp','Năm','Cách huấn luyện chính'],
      [['VAE (Kingma & Welling)','2013','Tối ưu ELBO = reconstruction + KL divergence'],
       ['GAN (Goodfellow et al.)','2014','Minimax đối kháng generator vs discriminator'],
       ['Normalizing Flows','~2015-2018','Chuỗi ánh xạ khả nghịch, tính exact likelihood']]),
    'PHẦN 1 · Lịch sử','Ba hướng đầu tiên của generative modeling hiện đại',
    explain='VAE dễ huấn luyện ổn định nhưng ảnh sinh ra thường mờ hơn GAN; GAN sinh ảnh sắc nét nhưng huấn luyện bất ổn định (mode collapse); Normalizing Flows cho phép tính likelihood chính xác nhưng kiến trúc bị hạn chế vì cần khả nghịch.'),
 ]),
 dict(title='Diffusion & Flow Matching: pushforward nhiều bước',bullets=['DDPM/score-based','Flow Matching','Hạn chế: nhiều bước inference'],slides=[
   sl(formula('Pushforward (định nghĩa chung, Eq.1 paper Drifting)','q = f#pε  (mạng f biến noise ε thành phân phối q, mục tiêu q ≈ p_data)',
      [('pε','phân phối nguồn, vd Gaussian'),('f','mạng neural, input noise, output dữ liệu'),('f#','ký hiệu pushforward do f gây ra')])
    +'<p>Diffusion (Sohl-Dickstein 2015, Ho 2020) và Flow Matching (Lipman 2022) đều thực hiện pushforward này bằng cách PHÂN RÃ thành nhiều bước nhỏ tại thời điểm <b>inference</b> (sinh mẫu) — mỗi bước biến đổi nhẹ mẫu nhiễu thành mẫu sạch hơn.</p>',
    'PHẦN 2 · Diffusion/Flow','Pushforward kiểu "nhiều bước lúc sinh mẫu"',
    explain='Hình dung: giống việc đi từ A đến B bằng nhiều bước nhỏ an toàn, mỗi bước dễ "tính toán đúng hướng" hơn là nhảy thẳng 1 bước lớn — đổi lại phải lặp hàng chục/hàng trăm bước mỗi lần sinh ảnh, rất chậm.'),
 ]),
 dict(title='Drifting Model: pushforward lúc huấn luyện',bullets=['Trường drift Vp,q','Tính chất anti-symmetric','Loss với stop-gradient'],slides=[
   sl(diag('../../diagrams/generative_lineage.svg','Dòng lịch sử Generative Model','VAE/GAN (2013-14) → Diffusion/Flow (2015-22) → Drifting (2026, 1-NFE)'),
    'PHẦN 3 · Drifting','Sơ đồ dòng lịch sử: từ VAE tới Drifting'),
   sl(formula('Trường drift (Eq.2, paper)','Vp,q(x) = E_{y+~p} E_{y-~q} [K(x, y+, y-)]',
      [('p','phân phối đích, thường = p_data'),('q','phân phối hiện tại của mạng'),('Tính chất','anti-symmetric: Vp,q = −Vq,p ⇒ V=0 khi p=q (điểm cân bằng)')]),
    'PHẦN 3 · Drifting','Trường drift và điểm cân bằng'),
   sl(formula('Loss huấn luyện (Eq. gần Eq.5, paper, rút gọn)','L = E_ε [ ‖ fθ(ε) − stopgrad( fθ(ε) + Vp,q(fθ(ε)) ) ‖² ]',
      [('stopgrad','chặn gradient chảy qua phần "đích" vì V phụ thuộc phân phối q, khó lan truyền ngược trực tiếp'),('Giá trị loss','bằng chính E‖V(f(ε))‖² — bình phương chuẩn của trường drift')])
    +callout('good','Kết quả','Mạng f cuối cùng chỉ cần 1 lần forward pass (1-NFE) để sinh mẫu — vì toàn bộ "sự lặp lại" đã xảy ra trong các bước SGD lúc huấn luyện, không phải lúc inference.'),
    'PHẦN 3 · Drifting','Loss function và vì sao sinh mẫu chỉ cần 1 bước'),
   sl(diag('../../figures/m4_drifting/fig1_pushforward.png','Fig. 1, Deng, Li, Li, Du & He 2026','q=f#p_prior (cam) tiến dần về p_data (xanh) qua các iteration huấn luyện 0→80; loss (trục y, log-scale) giảm tương ứng'),
    'PHẦN 3 · Drifting','Hình gốc: pushforward tiến hoá theo iteration huấn luyện'),
 ]),
 dict(title='References',bullets=['Hình đã dùng trong module này'],slides=[
   sl(ul(['Fig. 1 — Deng, M., Li, H., Li, T., Du, Y. & He, K. (2026). "Generative Modeling via Drifting." arXiv:2602.04770v2. Trang 1.']),
    'PHẦN 4 · References','Nguồn hình ảnh'),
 ]),
]

quiz=B.items
module_page('m4','04-generative-model-drifting',
  title='M4 · Lịch sử Generative Model & Drifting',
  subtitle='VAE → GAN → Normalizing Flows → Diffusion/Flow Matching → Drifting Model (pushforward train-time, 1-NFE)',
  source=SRC, status=f'HOÀN CHỈNH — {len(quiz)} câu quiz bám full-text paper Drifting + lịch sử generative model chuẩn ngành',
  parts=parts, quiz_items=quiz,
  notes='<h2>Ghi chú</h2><p>Pushforward q=f#pε, trường drift Vp,q, tính chất anti-symmetric (Prop 3.1), loss với stop-gradient, FID 1.54/1.61 ImageNet: trích trực tiếp từ bản PDF full-text arXiv:2602.04770v2 đã verify. Lịch sử VAE/GAN/Flow là kiến thức chuẩn ngành (Kingma&Welling 2013; Goodfellow 2014; Lipman 2022), không trích số liệu riêng của paper Drifting.</p>')
print('Module 4 xong.')
