#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Roda o reel.py com o ffmpeg empacotado no PATH.

Motivo (22/08/2026): esta maquina Windows nao tem ffmpeg no PATH, e o reel.py
chama "ffmpeg" pelo nome para cortar o preto de entrada e converter o webm do
playwright em mp4. O binario vem do pacote imageio-ffmpeg e e copiado para
work22b/ffmpeg.exe; aqui so se antecipa a pasta no PATH do processo.
"""
import os
import runpy
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = BASE + os.pathsep + os.environ.get("PATH", "")

sys.argv = ["reel.py"] + sys.argv[1:]
runpy.run_path(os.path.join(BASE, "reel.py"), run_name="__main__")
