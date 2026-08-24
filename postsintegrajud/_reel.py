# Envelope: poe a raiz da pasta no PATH (onde mora o ffmpeg.exe) antes de
# chamar o reel.py. Sem isso o reel quebra em FileNotFoundError [WinError 2].
# Recebe o spec por argumento, para nao precisar de um envelope novo por rodada.
import os, sys, runpy

RAIZ = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = RAIZ + os.pathsep + os.environ.get("PATH", "")
os.chdir(RAIZ)
sys.argv = ["reel.py"] + sys.argv[1:]
runpy.run_path(os.path.join(RAIZ, "reel.py"), run_name="__main__")
