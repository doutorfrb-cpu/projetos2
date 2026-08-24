#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retoma a publicacao de um container pai do Instagram que ja foi criado.

Nao imprime token. Uso:  py _retomar_ig.py <container_id>
"""
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import publicar_instagram as pi

cid = sys.argv[1]
cfg = pi.carregar_config(BASE)

for tentativa in range(1, 21):
    try:
        r = pi.http_get(f"{pi.API}/{cid}", {
            "fields": "status_code,status",
            "access_token": cfg["access_token"],
        })
    except Exception as e:
        print("erro ao consultar status:", pi.erro_meta(e))
        sys.exit(1)
    st = r.get("status_code")
    print(f"container {cid}: {st} ({tentativa}/20)", flush=True)
    if st == "FINISHED":
        break
    if st == "ERROR":
        print("container em ERROR:", r.get("status"))
        sys.exit(1)
    time.sleep(6)
else:
    print("container nao ficou pronto")
    sys.exit(1)

try:
    mid = pi.publicar(cfg, cid)
except Exception as e:
    print("erro ao publicar:", pi.erro_meta(e))
    sys.exit(1)

print("IG PUBLICADO. media id:", mid)
