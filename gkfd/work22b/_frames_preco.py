#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai tres quadros do reel para conferencia visual."""
import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(BASE, "ffmpeg.exe")
SRC = os.path.join(BASE, "pc_gkfd14", "gkfd_piso_de_preco_reel.mp4")
OUT = os.path.join(BASE, "_frames_preco")
os.makedirs(OUT, exist_ok=True)

for seg in (1.5, 6.0, 11.0):
    dst = os.path.join(OUT, f"q{seg}.png")
    r = subprocess.run([FF, "-v", "error", "-ss", str(seg), "-i", SRC,
                        "-frames:v", "1", "-y", dst], capture_output=True)
    print(seg, "ok" if os.path.exists(dst) else "falhou",
          r.stderr.decode(errors="replace")[:200])
