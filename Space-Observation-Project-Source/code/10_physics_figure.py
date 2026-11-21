"""Bước 10 - Hình minh họa vật lý transit 1160x300 cho slide 3."""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.size": 15, "figure.dpi": 100, "savefig.dpi": 100})
NAVY, RED = "#273896", "#ED1C24"
fig, ax = plt.subplots(figsize=(11.6, 3.0), constrained_layout=True)
P, T, d = 6.0, 1.6, 0.012
t = np.linspace(-3.5, 9.5, 2000)
def dip(x):
    y = np.ones_like(x)
    for c in (0.0, P):
        u = np.abs(x - c) / (T / 2)
        y -= np.where(u < 1, d * np.clip((1 - u) / 0.12, 0, 1), 0)
    return y
ax.plot(t, dip(t), color=NAVY, lw=3)
ax.set_ylim(0.972, 1.009); ax.set_xlim(-3.5, 9.5)
ax.annotate("", xy=(0, 1.0030), xytext=(P, 1.0030), arrowprops=dict(arrowstyle="<->", color=RED, lw=2))
ax.text(P / 2, 1.0042, "period P", ha="center", va="bottom", color=RED, fontsize=16, fontweight="bold")
ax.annotate("", xy=(-T / 2, 0.9855), xytext=(T / 2, 0.9855), arrowprops=dict(arrowstyle="<->", color=RED, lw=2))
ax.text(0, 0.9835, "duration T", ha="center", va="top", color=RED, fontsize=16, fontweight="bold")
ax.annotate("", xy=(2.2, 1 - d), xytext=(2.2, 1.0), arrowprops=dict(arrowstyle="<->", color=RED, lw=2))
ax.text(2.45, 1 - d / 2, "depth δ ≈ (R$_p$/R$_★$)$^2$", va="center", color=RED, fontsize=16, fontweight="bold")
ax.set(xlabel="Time (days)", ylabel="Relative flux", xticks=[], yticks=[1.0], yticklabels=["1"])
fig.savefig(ROOT / "slides" / "assets" / "images" / "phys_transit.png")
print("ok")
