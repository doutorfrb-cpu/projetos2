import zipfile, os, shutil

os.makedirs('work31', exist_ok=True)
zipfile.ZipFile('gerador-integrajud.zip').extractall('work31')
print('unzip ok')

for f in ['machine.py', 'reel.py', 'story_ad.py', 'fundo_numerico.py',
          'retrato.py', 'repor_fotos.py', 'ffmpeg.exe']:
    shutil.copy(f, os.path.join('work31', f))
print('scripts vivos da raiz copiados por cima')

src, dst = 'fotos_banco', os.path.join('work31', 'fotos_banco')
os.makedirs(dst, exist_ok=True)
n = 0
for f in os.listdir(src):
    if not os.path.exists(os.path.join(dst, f)):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
        n += 1
print('fotos completadas:', n)
print('total fotos:', len(os.listdir(dst)))
