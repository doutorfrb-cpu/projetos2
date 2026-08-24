# Extrai alguns quadros do mp4 para conferencia visual antes de publicar.
# Usa o ffmpeg.exe da raiz, como o envelope do reel.
import os, sys, subprocess

RAIZ = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(RAIZ, "ffmpeg.exe")
mp4 = sys.argv[1]
tempos = sys.argv[2:] or ["0.5", "4", "8", "12", "16"]
for i, t in enumerate(tempos, 1):
    saida = os.path.join(RAIZ, "_frame_%02d.jpg" % i)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", t, "-i", mp4, "-frames:v", "1", "-q:v", "3", saida],
                   check=True)
    print(saida)
