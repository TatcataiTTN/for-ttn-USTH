# -*- coding: utf-8 -*-
"""Timeline SVG don lane, mau co dinh (khong dung CSS var, vi <img> load SVG doc lap)."""
import os, html
OUT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','diagrams'))
os.makedirs(OUT,exist_ok=True)
def esc(s): return html.escape(str(s), quote=False)

def timeline(nodes, y0, y1, step=78, ml=40, title=''):
    H=170; W=ml+(y1-y0)*step+160
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" font-family="sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    s.append(f'<text x="{W/2}" y="20" font-size="15" font-weight="800" fill="#273896" text-anchor="middle">{esc(title)}</text>')
    laneY=95
    s.append(f'<line x1="{ml}" y1="{laneY}" x2="{W-40}" y2="{laneY}" stroke="#ED1C24" stroke-width="2.5" opacity=".6"/>')
    def X(year): return ml+(year-y0)*step
    for i,(year,name,sub,up) in enumerate(nodes):
        x=X(year)
        s.append(f'<circle cx="{x}" cy="{laneY}" r="6" fill="#273896" stroke="#fff" stroke-width="1.5"/>')
        ty = laneY-16 if up else laneY+34
        s.append(f'<text x="{x}" y="{ty}" font-size="12.5" font-weight="700" fill="#1d2433" text-anchor="middle">{esc(name)}</text>')
        s.append(f'<text x="{x}" y="{ty+15 if up else ty-15}" font-size="10.5" fill="#5d6678" text-anchor="middle">{esc(sub)}</text>')
    for yr in range(int(y0),int(y1)+1,2 if (y1-y0)>12 else 1):
        s.append(f'<text x="{X(yr)}" y="{H-14}" font-size="10" fill="#9aa2b1" text-anchor="middle">{yr}</text>')
    s.append('</svg>')
    return ''.join(s)

rc_nodes=[
 (1990,'RNN/BPTT','vanishing gradient',True),
 (2001,'ESN','Jaeger — reservoir ngẫu nhiên cố định',False),
 (2002,'LSM','Maass — mạng xung sinh học',True),
 (2010,'Fading memory','điều kiện lý thuyết RC',False),
 (2017,'QRC','Fujii & Nakajima — reservoir lượng tử',True),
 (2026,'Spin-chain tunable','Ramon-Escandell — explicit/memory register',False),
]
open(os.path.join(OUT,'rc_lineage.svg'),'w',encoding='utf-8').write(
    timeline(rc_nodes,1989,2027,step=46,title='Dòng lịch sử Reservoir Computing: RNN → ESN/LSM → QRC → spin-chain tunable memory'))

gen_nodes=[
 (2013,'VAE','Kingma & Welling — ELBO',True),
 (2014,'GAN','Goodfellow — đối kháng',False),
 (2015,'Diffusion/DDPM','Sohl-Dickstein / Ho — nhiều bước',True),
 (2018,'Normalizing Flows','song song, ánh xạ khả nghịch',False),
 (2022,'Flow Matching','Lipman — ODE liên tục',True),
 (2026,'Drifting Model','Deng et al. — pushforward train-time, 1-NFE',False),
]
open(os.path.join(OUT,'generative_lineage.svg'),'w',encoding='utf-8').write(
    timeline(gen_nodes,2012,2028,title='Dòng lịch sử Generative Model: VAE/GAN → Diffusion/Flow → Drifting (1-step)'))

def pipeline(title, rows):
    """rows: list of (lane_label, lane_color, [box_labels]) — 1 hang = 1 luong, box noi tiep bang mui ten."""
    BW,BH,GAP,LX = 230,66,26,170
    H = 70+len(rows)*(BH+54)
    maxlen = max(len(r[2]) for r in rows)
    W = LX+maxlen*(BW+GAP)+40
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" font-family="sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    s.append(f'<text x="{W/2}" y="26" font-size="15" font-weight="800" fill="#273896" text-anchor="middle">{esc(title)}</text>')
    cols={r[1] for r in rows}
    s.append('<defs>'+''.join(f'<marker id="ph{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in cols)+'</defs>')
    for ri,(label,color,boxes) in enumerate(rows):
        y = 60+ri*(BH+54)
        s.append(f'<text x="14" y="{y+BH/2+5}" font-size="12.5" font-weight="700" fill="{color}">{esc(label)}</text>')
        for bi,btxt in enumerate(boxes):
            x = LX+bi*(BW+GAP)
            s.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="9" fill="{color}" opacity="0.12" stroke="{color}" stroke-width="2"/>')
            s.append(f'<foreignObject x="{x+6}" y="{y+4}" width="{BW-12}" height="{BH-8}"><div xmlns="http://www.w3.org/1999/xhtml" style="height:100%;display:flex;align-items:center;justify-content:center;text-align:center;font-size:12.5px;font-weight:600;color:#1d2433;line-height:1.25;white-space:pre-line">{esc(btxt)}</div></foreignObject>')
            if bi < len(boxes)-1:
                ax=x+BW; s.append(f'<line x1="{ax+4}" y1="{y+BH/2}" x2="{ax+GAP-6}" y2="{y+BH/2}" stroke="{color}" stroke-width="2.5" marker-end="url(#ph{color[1:]})"/>')
    s.append('</svg>')
    return ''.join(s)

pipe_rows=[
 ('Hướng QRC\n(paper #1)','#273896',['ENSO/PDO/VM\nindex (165 năm)','Encode 3 kênh vào\nexplicit register','Reservoir update\n(Hamiltonian cố định)','Memory register\ngiữ ngữ cảnh chậm','Readout tuyến tính\n→ dự báo EASMI']),
 ('Hướng Drifting\n(paper #2)','#ED1C24',['CMIP6 thô\n(input ε/condition)','Network f\n(U-Net/ViT, 1-pass)','Pushforward\nq=f#p','So khớp 15 mô phỏng\nRCM đã benchmark','1 bước sinh\ntrường độ phân giải cao']),
]
open(os.path.join(OUT,'m5_pipeline.svg'),'w',encoding='utf-8').write(
    pipeline('Pipeline thiết kế mở rộng: QRC cho ENSO-EASM (paper #1) và Drifting cho CORDEX-SEA (paper #2)', pipe_rows))
print('3 SVG diagrams written to', OUT)
