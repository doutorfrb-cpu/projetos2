#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lista os ultimos posts da Pagina. Nao imprime token.

Uso:  py _fb_ultimos.py [quantos]
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import json
import publicar_facebook as pf

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
cfg = json.load(open(os.path.join(BASE, "config_publicacao.json"), encoding="utf-8"))
fb = dict(cfg["facebook"])
tok = pf.resolver_page_token(cfg, fb)

r = pf.pega(f"{fb['page_id']}/published_posts", {
    "fields": "id,created_time,message",
    "limit": str(n),
    "access_token": tok,
})
for p in r.get("data", []):
    msg = (p.get("message") or "").replace("\n", " ")[:70]
    print(p["created_time"], p["id"], "|", msg)
