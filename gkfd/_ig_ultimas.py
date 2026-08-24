#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lista as ultimas midias do perfil do Instagram. Nao imprime token.

Uso:  py _ig_ultimas.py [quantas]
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import publicar_instagram as pi

n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
cfg = pi.carregar_config(BASE)

try:
    r = pi.http_get(f"{pi.API}/{cfg['ig_user_id']}/media", {
        "fields": "id,media_type,timestamp,caption",
        "limit": str(n),
        "access_token": cfg["access_token"],
    })
except Exception as e:
    print("erro:", pi.erro_meta(e))
    sys.exit(1)

for m in r.get("data", []):
    cap = (m.get("caption") or "").replace("\n", " ")[:70]
    print(m["timestamp"], m["media_type"], m["id"], "|", cap)
