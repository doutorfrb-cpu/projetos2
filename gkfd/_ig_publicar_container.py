#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chama media_publish num container ja FINISHED, com espera crescente.

Nao imprime token. Uso:  py _ig_publicar_container.py <container_id>
"""
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import publicar_instagram as pi

cid = sys.argv[1]
cfg = pi.carregar_config(BASE)

for i, espera in enumerate([0, 30, 60, 90, 120, 180, 180, 180], 1):
    if espera:
        print(f"esperando {espera}s...", flush=True)
        time.sleep(espera)
    try:
        mid = pi.publicar(cfg, cid)
    except Exception as e:
        print(f"tentativa {i}: {pi.erro_meta(e)}", flush=True)
        continue
    print("IG CARROSSEL PUBLICADO. media id:", mid)
    sys.exit(0)

print("nao publicou: limite do app ainda ativo")
sys.exit(1)
