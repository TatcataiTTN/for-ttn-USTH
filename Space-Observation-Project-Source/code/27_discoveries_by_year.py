# -*- coding: utf-8 -*-
"""Bước 27 - Số hành tinh đã xác nhận theo năm phát hiện và theo phương pháp, cùng số hành tinh của từng cơ sở (NASA Exoplanet Archive, bảng pscomppars, TAP).
Ra: data/raw/discoveries_by_year.csv, data/raw/discoveries_by_facility.csv, results/discoveries_summary.json, figures/paper/exo_discoveries.png
Chỉ gửi truy vấn công khai tới NASA; không gửi thông tin cá nhân. Ngày truy vấn ghi trong JSON."""
import datetime
import io
import json
import pathlib
import urllib.parse
import urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = {"User-Agent": "student-project-script"}


def tap(q):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode({"format": "csv", "query": q})
    return pd.read_csv(io.StringIO(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read().decode()))


Y = tap("select disc_year, discoverymethod, count(*) as n from pscomppars group by disc_year, discoverymethod order by disc_year")
Y.to_csv(ROOT / "data" / "raw" / "discoveries_by_year.csv", index=False)
Fc = tap("select disc_facility, count(*) as n, min(disc_year) as first_year, max(disc_year) as last_year from pscomppars group by disc_facility order by n desc")
Fc.to_csv(ROOT / "data" / "raw" / "discoveries_by_facility.csv", index=False)
tot = int(Y.n.sum()); bym = Y.groupby("discoverymethod").n.sum().sort_values(ascending=False)
fac = {k: int(Fc[Fc.disc_facility.str.contains(k, case=False, regex=False, na=False)].n.sum()) for k in ("Kepler", "K2", "Transiting Exoplanet Survey Satellite", "CoRoT", "SuperWASP", "HATNet", "KELT", "MEarth", "OGLE", "La Silla", "Haute-Provence")}
json.dump(dict(date=str(datetime.date.today()), total=tot, by_method=bym.to_dict(), facilities=fac, years=[int(Y.disc_year.min()), int(Y.disc_year.max())]), open(ROOT / "results" / "discoveries_summary.json", "w"), indent=1)

main = ["Transit", "Radial Velocity", "Microlensing", "Imaging"]
Y["grp"] = Y.discoverymethod.where(Y.discoverymethod.isin(main), "Other")
P = Y.pivot_table(index="disc_year", columns="grp", values="n", aggfunc="sum", fill_value=0).reindex(columns=main + ["Other"], fill_value=0)
P = P.reindex(range(1992, int(P.index.max()) + 1), fill_value=0)
cols = {"Transit": "#273896", "Radial Velocity": "#ED1C24", "Microlensing": "#d98e00", "Imaging": "#0f9d58", "Other": "#9aa3b5"}
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 14.5, "ytick.labelsize": 14.5, "legend.fontsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
fig, ax = plt.subplots(figsize=(7.4, 4.7), constrained_layout=True)
bot = np.zeros(len(P))
for c in main + ["Other"]:
    ax.bar(P.index, P[c], bottom=bot, color=cols[c], width=0.8, label=c); bot += P[c].values
for yr, lab in ((2006, "CoRoT"), (2009, "Kepler"), (2018, "TESS")):
    ax.axvline(yr, color="black", lw=1, ls=":"); ax.text(yr - 0.4, ax.get_ylim()[1] * 0.97, lab, rotation=90, va="top", ha="right", fontsize=14.5)
ax.set(xlabel="Year of discovery", ylabel="Confirmed planets per year", xlim=(1991, P.index.max() + 1)); ax.legend(loc="upper left", frameon=False, bbox_to_anchor=(0.0, 0.88))
fig.savefig(ROOT / "figures" / "paper" / "exo_discoveries.png"); plt.close(fig)
print(tot, "planets;", bym.to_dict()); print(fac); print(Fc.head(8).to_string(index=False))
