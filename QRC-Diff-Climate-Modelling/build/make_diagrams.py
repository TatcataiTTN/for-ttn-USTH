# -*- coding: utf-8 -*-
"""Timeline SVG don lane, mau co dinh (khong dung CSS var, vi <img> load SVG doc lap)."""
import os
OUT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','diagrams'))
os.makedirs(OUT,exist_ok=True)

def timeline(nodes, y0, y1, step=78, ml=40, title=''):
    H=170; W=ml+(y1-y0)*step+160
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" font-family="sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    s.append(f'<text x="{W/2}" y="20" font-size="15" font-weight="800" fill="#273896" text-anchor="middle">{title}</text>')
    laneY=95
    s.append(f'<line x1="{ml}" y1="{laneY}" x2="{W-40}" y2="{laneY}" stroke="#ED1C24" stroke-width="2.5" opacity=".6"/>')
    def X(year): return ml+(year-y0)*step
    for i,(year,name,sub,up) in enumerate(nodes):
        x=X(year)
        s.append(f'<circle cx="{x}" cy="{laneY}" r="6" fill="#273896" stroke="#fff" stroke-width="1.5"/>')
        ty = laneY-16 if up else laneY+34
        s.append(f'<text x="{x}" y="{ty}" font-size="12.5" font-weight="700" fill="#1d2433" text-anchor="middle">{name}</text>')
        s.append(f'<text x="{x}" y="{ty+15 if up else ty-15}" font-size="10.5" fill="#5d6678" text-anchor="middle">{sub}</text>')
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
    timeline(rc_nodes,1988,2028,title='Dòng lịch sử Reservoir Computing: RNN → ESN/LSM → QRC → spin-chain tunable memory'))

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
print('2 SVG diagrams written to', OUT)
