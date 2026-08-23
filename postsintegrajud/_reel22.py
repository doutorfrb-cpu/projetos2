# -*- coding: utf-8 -*-
# Envelope do reel.py para ESTA maquina: o ffmpeg nao esta no PATH do sistema,
# e o reel.py chama "ffmpeg" direto. Aqui a raiz da pasta (onde mora o
# ffmpeg.exe copiado em 22/08/2026) entra no PATH antes de o reel.py rodar.
# Uso:  py _reel22.py spec_18h_22ago.json
import os, sys, runpy
os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ.get("PATH", "")
spec = sys.argv[1] if len(sys.argv) > 1 else "spec.json"
sys.argv = ["reel.py", spec]
runpy.run_path("reel.py", run_name="__main__")
