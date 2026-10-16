import nbformat as nbf, numpy as np, os

OUT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','notebooks'))
os.makedirs(OUT,exist_ok=True)

def mk_m1():
    nb=nbf.v4.new_notebook(); c=nb['cells']
    c.append(nbf.v4.new_markdown_cell(
"""# Notebook verify — Module 1 (ENSO-PDO-EASM)

Verify các CONG THUC/DINH NGHIA trich tu paper #1 (Nguyen-Le & Ngo-Duc 2025, J. Climate,
DOI 10.1175/JCLI-D-24-0626.1) bang code thuc su chay duoc, KHONG dung lai bo du lieu goc
COBE-SST2/20CRv3 (165 nam, khong tai duoc trong pham vi notebook nay).

CANH BAO: moi so lieu trong notebook nay la minh hoa CACH TINH DUNG cong thuc (EASMI,
N_eff Bretherton 1999) tren du lieu tong hop/gia lap co cau truc hop ly, KHONG phai tai
lap duoc chinh xac cac con so -0.28 / -0.51 / 0.09 cua paper #1 (can dung 165 nam
COBE-SST2 + 20CRv3 thuc de tai lap)."""))
    c.append(nbf.v4.new_code_cell(
"""import numpy as np
print('numpy', np.__version__)"""))
    c.append(nbf.v4.new_markdown_cell(
"""## 1. Verify N_eff theo Bretherton et al. (1999)

Paper #1 dung kiem dinh t hai phia voi so bac tu do hieu dung N_eff dieu chinh theo tu
tuong quan tre-1 (lag-1 autocorrelation) cua 2 bien x, y:

N_eff = N * (1 - r1x*r1y) / (1 + r1x*r1y)"""))
    c.append(nbf.v4.new_code_cell(
"""def neff_bretherton(x, y):
    n = len(x)
    r1x = np.corrcoef(x[:-1], x[1:])[0, 1]
    r1y = np.corrcoef(y[:-1], y[1:])[0, 1]
    return n * (1 - r1x * r1y) / (1 + r1x * r1y), r1x, r1y

rng = np.random.default_rng(0)
n = 200
x = np.zeros(n); y = np.zeros(n)
for i in range(1, n):
    x[i] = 0.7 * x[i-1] + rng.normal(0, 1)
    y[i] = 0.5 * y[i-1] + rng.normal(0, 1)
neff, r1x, r1y = neff_bretherton(x, y)
print(f"N={n}, r1x={r1x:.3f}, r1y={r1y:.3f}, N_eff={neff:.1f}")
assert neff < n
print("OK: N_eff < N khi 2 chuoi co tu tuong quan duong, dung chieu cong thuc Bretherton 1999.")"""))
    c.append(nbf.v4.new_markdown_cell(
"""## 2. Verify dinh nghia EASMI (Wang & Fan 1999)

EASMI = chuan hoa[ U850(5-15N,90-130E) - U850(22.5-32.5N,110-140E) ], JJA(0).

Notebook nay KHONG co du lieu U850 thuc (chi co SST OISST o module khac) - minh hoa
bang CONG THUC tren du lieu gia lap co cau truc khong gian hop ly, de verify code tinh
dung logic "lay trung binh vung A tru vung B roi chuan hoa"."""))
    c.append(nbf.v4.new_code_cell(
"""rng = np.random.default_rng(1)
years = 30
regionA = rng.normal(5, 2, years)
regionB = rng.normal(-3, 2, years)
raw = regionA - regionB
easmi = (raw - raw.mean()) / raw.std()
print("EASMI chuan hoa (gia lap), 5 nam dau:", np.round(easmi[:5], 2))
print("mean~0, std~1:", round(easmi.mean(), 3), round(easmi.std(), 3))
print("EASMI < 0 => hoan luu nghich dao bat thuong => gio mua yeu (dung dinh nghia dau).")"""))
    nb['cells']=c
    nbf.write(nb, os.path.join(OUT,'m1_verify_enso_easm.ipynb'))
    print('OK m1 notebook')

def mk_m2():
    nb=nbf.v4.new_notebook(); c=nb['cells']
    c.append(nbf.v4.new_markdown_cell(
"""# Notebook verify — Module 2 (Reservoir Computing & QRC)

Verify nguyen ly Reservoir Computing (fixed reservoir + readout tuyen tinh) bang mot
Echo State Network CO DIEN thuc su chay duoc, tren chuoi NARMA-10 tong hop (dung benchmark
GOC cua paper QRC, khong phai du lieu khi hau).

CANH BAO: day la ESN CO DIEN (ma tran trong so ngau nhien thuc), KHONG phai mach luong tu
qiskit theo dung Hamiltonian MFIM (Eq. 1) cua paper arXiv:2608.28440v1 - minh hoa dung
NGUYEN TAC chung cua Reservoir Computing (reservoir co dinh, chi train readout)."""))
    c.append(nbf.v4.new_code_cell(
"""import numpy as np
rng = np.random.default_rng(42)

def make_narma10(n, rng):
    u = rng.uniform(0, 0.5, n)
    y = np.zeros(n)
    for t in range(10, n):
        y[t] = (0.3*y[t-1] + 0.05*y[t-1]*np.sum(y[t-10:t])
                + 1.5*u[t-1]*u[t-10] + 0.1)
    return u, y

u, y = make_narma10(2000, rng)
print("NARMA-10 series, shape:", u.shape, y.shape, "range y:", y.min(), y.max())"""))
    c.append(nbf.v4.new_markdown_cell(
"""## Echo State Network (fixed reservoir, chi train readout)

Day la kien truc GOC (Jaeger 2001) ma QRC thay reservoir co dien bang tien hoa Hamiltonian
luong tu: reservoir KHONG BAO GIO duoc huan luyen bang gradient, chi lop readout tuyen tinh
phia sau duoc train (closed-form ridge regression) - dung nguyen tac nay la dieu can verify."""))
    c.append(nbf.v4.new_code_cell(
"""N_RES = 100
W_in = rng.uniform(-1, 1, N_RES)
W_res = rng.uniform(-1, 1, (N_RES, N_RES))
# chuan hoa spectral radius < 1 - DIEU KIEN BAT BUOC cho echo state property
eigvals = np.linalg.eigvals(W_res)
W_res = W_res / (np.max(np.abs(eigvals)) + 1e-9) * 0.9
print("Spectral radius sau chuan hoa:", np.max(np.abs(np.linalg.eigvals(W_res))))
assert np.max(np.abs(np.linalg.eigvals(W_res))) < 1.0, "Echo state property yeu cau spectral radius < 1"

states = np.zeros((len(u), N_RES))
s = np.zeros(N_RES)
for t in range(len(u)):
    s = np.tanh(W_in * u[t] + W_res @ s)
    states[t] = s
print("OK: reservoir co dinh da tien hoa", len(u), "buoc, KHONG co gradient nao duoc tinh cho W_in/W_res.")"""))
    c.append(nbf.v4.new_code_cell(
"""# Readout tuyen tinh: ridge regression closed-form (giong cach train chuan cua MOI RC, ca QRC)
train_n = 1500
X_tr, y_tr = states[200:train_n], y[200:train_n]
X_te, y_te = states[train_n:], y[train_n:]
lam = 1e-6
W_out = np.linalg.solve(X_tr.T @ X_tr + lam*np.eye(N_RES), X_tr.T @ y_tr)
pred = X_te @ W_out
nrmse = np.sqrt(np.mean((pred - y_te)**2)) / np.std(y_te)
print(f"NRMSE tren test set NARMA-10 (ESN co dien, {N_RES} reservoir units): {nrmse:.4f}")
assert nrmse < 1.0, "Readout phai hoc duoc gi do (NRMSE < 1 nghia la tot hon du doan = trung binh)"
print("OK: readout tuyen tinh hoc duoc tu reservoir co dinh - dung nguyen tac RC ma QRC ke thua.")"""))
    nb['cells']=c
    nbf.write(nb, os.path.join(OUT,'m2_verify_rc_narma10.ipynb'))
    print('OK m2 notebook')

mk_m1(); mk_m2()
