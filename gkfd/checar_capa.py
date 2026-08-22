import sys
from PIL import Image
import numpy as np

p = sys.argv[1]
im = Image.open(p).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# 1) achar a borda accent (#4FA3F7) de largura inteira
acc = np.array([0x4F, 0xA3, 0xF7])
d = np.abs(a - acc).sum(axis=2)
mask = d < 60
frac = mask[:, 80:W - 80].mean(axis=1)
rows = np.where(frac > 0.9)[0]
if len(rows) == 0:
    print("borda accent de largura inteira: NAO ENCONTRADA")
    sys.exit(0)
# agrupar
grupos = []
ini = rows[0]
prev = rows[0]
for r in rows[1:]:
    if r - prev > 3:
        grupos.append((ini, prev))
        ini = r
    prev = r
grupos.append((ini, prev))
print("bordas accent (y0,y1):", grupos)

# 2) linha do split: a que estiver entre 700 e 900
split = [g for g in grupos if 650 < g[0] < 950]
if not split:
    print("nenhuma borda na faixa do split L5 — ok")
    sys.exit(0)
y0, y1 = split[0]

# 3) texto claro na banda ao redor da borda
banda = a[max(0, y0 - 40):min(H, y1 + 40), 84:W - 84]
lum = banda.mean(axis=2)
# texto claro (>200) sobre fundo escuro
tex = (lum > 200)
for i, row in enumerate(tex):
    yy = max(0, y0 - 40) + i
    if y0 <= yy <= y1:
        continue
    pass
# conta pixels de texto imediatamente acima e abaixo da borda
acima = (a[max(0, y0 - 14):y0, 84:W - 84].mean(axis=2) > 200).sum()
abaixo = (a[y1 + 1:y1 + 15, 84:W - 84].mean(axis=2) > 200).sum()
print(f"split y={y0}..{y1}  pixels de texto 14px ACIMA={acima}  14px ABAIXO={abaixo}")
if acima > 400 or abaixo > 400:
    print(">>> RISCADO: texto encosta na borda do split")
else:
    print(">>> LIMPO: a borda do split cai em vao")
