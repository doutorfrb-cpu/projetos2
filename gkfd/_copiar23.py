#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copia os PNGs renderizados da pasta de trabalho para a pasta da peca."""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.join(BASE, "work22b", "pc_gkfd13")
DST = os.path.join(BASE, "2026-08-23_troca-de-contador")

os.makedirs(DST, exist_ok=True)
for nome in sorted(os.listdir(ORG)):
    if nome.endswith(".png"):
        shutil.copy2(os.path.join(ORG, nome), os.path.join(DST, nome))
        print("copiado:", nome)
print("pasta:", sorted(os.listdir(DST)))
