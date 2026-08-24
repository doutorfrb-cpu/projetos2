#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apaga as 4 republicacoes acidentais do carrossel PRECO (23/08/2026, 18h).

Fica de pe o mais antigo: 18109247228171455 (18:23:04 UTC).
A Graph API historicamente responde (#10) Insufficient permissions para DELETE
em midia do Instagram. Tenta mesmo assim; falhando, os ids ficam registrados
para a exclusao a mao no aplicativo.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(BASE, "config_publicacao.json"), encoding="utf-8"))
TOK = cfg["facebook"]["page_token"]

DUPLICADOS = [
    ("17900832531555220", "18:24:53"),
    ("18064155941509836", "18:29:33"),
    ("18172067257450074", "18:31:05"),
    ("17920669449202947", "18:35:02"),
]

for mid, quando in DUPLICADOS:
    url = f"https://graph.facebook.com/v21.0/{mid}?" + urllib.parse.urlencode(
        {"access_token": TOK})
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print(f"APAGADO  {mid}  {quando}  ->  {r.read().decode()[:80]}")
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")
        print(f"NAO DEU  {mid}  {quando}  ->  HTTP {e.code}: {corpo[:200]}")
