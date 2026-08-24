#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copia story 9:16 e reel para a pasta da peca, com os nomes que o extras.py espera."""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "work22b")
DST = os.path.join(BASE, "2026-08-23_troca-de-contador")

alvos = {
    "gkfd_troca_de_contador_916.png": "story_916.png",
    "gkfd_troca_de_contador_reel.mp4": "reel.mp4",
}

for origem, destino in alvos.items():
    achou = None
    for raiz, _dirs, arqs in os.walk(WORK):
        if origem in arqs:
            achou = os.path.join(raiz, origem)
            break
    if achou:
        shutil.copy2(achou, os.path.join(DST, destino))
        print("copiado:", achou, "->", destino)
    else:
        print("NAO ENCONTRADO:", origem)

print("pasta:", sorted(os.listdir(DST)))
