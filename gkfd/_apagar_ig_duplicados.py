#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tenta apagar as republicacoes acidentais de 23/08/2026 no Instagram.

A Graph API historicamente NAO expoe DELETE para midia do Instagram publicada
pela API de conteudo. Este script tenta mesmo assim: se responder erro, a
exclusao tem de ser feita no aplicativo, a mao, e os ids ficam registrados
aqui e no pautas-publicadas.md para isso.
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
    ("18423935884194137", "16:50:06  ACOS  (dup de 18/08 ads-acos-margem)"),
    ("18117448900931099", "16:51:19  R$ 300 no painel  (dup de 17-18/08 repasse-receita-bruta)"),
    ("18126311983704583", "16:52:26  saldo retido  (dup de 18/08 saldo-retido)"),
    ("18212556574346735", "16:53:36  Fator R  (dup de 19/08 anexo-fator-r)"),
]

for mid, descricao in DUPLICADOS:
    url = f"https://graph.facebook.com/v21.0/{mid}?" + urllib.parse.urlencode(
        {"access_token": TOK})
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print(f"APAGADO  {descricao}  ->  {r.read().decode()[:80]}")
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")
        print(f"NAO DEU  {descricao}  ->  HTTP {e.code}: {corpo[:200]}")
