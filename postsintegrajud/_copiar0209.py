import os, shutil, glob

dst = '2026-09-02_conversao-sacas-laudo'
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob('work0209/pc_0209_conversao_sacas/*.png')):
    shutil.copy(f, os.path.join(dst, os.path.basename(f)))
print(sorted(os.listdir(dst)))
