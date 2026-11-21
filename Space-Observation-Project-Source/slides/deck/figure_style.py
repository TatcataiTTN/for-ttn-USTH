# -*- coding: utf-8 -*-
"""Kiểu matplotlib để chữ trong hình luôn >= 20 px khi đặt lên slide 1280x720.
Nguyên lý: 1 pixel hình = 1 pixel slide. Đặt dpi=100 và figsize = (px_rộng/100, px_cao/100) đúng bằng ô sẽ chiếm trên slide,
rồi chèn ảnh với width đúng bằng px_rộng (KHÔNG để trình duyệt thu nhỏ). 1 pt = 100/72 px, nên 14,4 pt = 20 px.
Dùng:  from figure_style import apply_slide_style, SIZES;  apply_slide_style();  fig = plt.figure(figsize=SIZES["full"])
"""
import matplotlib.pyplot as plt

SIZES = {                      # (inch rộng, inch cao) ở dpi 100 -> px bằng inch*100
    "full": (11.6, 5.3),       # chiếm cả bề ngang nội dung (1160 px) và ~530 px chiều cao: bản đồ, biểu đồ chính
    "wide": (11.6, 3.9),       # hình bẹt phía dưới một đoạn chữ
    "half": (5.7, 4.7),        # hai hình cạnh nhau (570 + 590 px)
    "text_side": (7.0, 4.6),   # hình bên trái, cột chữ bên phải
}

def apply_slide_style(base=15, tick=14.5):
    plt.rcParams.update({"font.size": base, "axes.titlesize": base + 1, "axes.labelsize": base,
                         "xtick.labelsize": tick, "ytick.labelsize": tick, "legend.fontsize": tick,
                         "figure.dpi": 100, "savefig.dpi": 100})

def tidy_ticks(ax, n=4, fmt="%.2f"):
    """Số trên trục không chồng lên nhau: ít vạch hơn, định dạng cố định (tránh nhãn offset kiểu +1.059e2)."""
    ax.xaxis.set_major_locator(plt.MaxNLocator(n)); ax.yaxis.set_major_locator(plt.MaxNLocator(n))
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter(fmt)); ax.yaxis.set_major_formatter(plt.FormatStrFormatter(fmt))

# Lưu ý: không vẽ chú thích dài, nguồn dữ liệu hay ghi công vào TRONG ảnh (sẽ nhỏ hơn 20 px); đặt chúng ở caption HTML 20 px dưới ảnh.
# Dùng constrained_layout=True; dùng sharey=True khi hai ô cạnh nhau; legend đặt ngoài ô vẽ nếu đè dữ liệu.
