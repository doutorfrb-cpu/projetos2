import os, shutil, glob

dst = '2026-09-03_agravo-sistema-amortizacao'
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob('work0309/pc_0309_agravo_amortizacao/*.png')):
    shutil.copy(f, os.path.join(dst, os.path.basename(f)))
print(sorted(os.listdir(dst)))
