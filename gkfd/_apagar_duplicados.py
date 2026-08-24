#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apaga as republicacoes acidentais de 23/08/2026 na Pagina do Facebook.

CONTEXTO: nesta rodada eu rodei `publicar_pendentes.py` para tentar reenviar o
carrossel do dia ao Instagram. Aquele script nao reenvia UMA peca — ele varre
todas as subpastas e publica toda peca sem o arquivo .publicado. As pecas
antigas nunca tinham essa marca, entao ele comecou a republicar o acervo.
Foi morto no meio, depois de cinco pecas no Facebook e quatro no Instagram.

Os ids abaixo foram conferidos um a um contra o created_time (todos entre
16:49 e 16:54 UTC de 23/08) e contra a legenda, que repete peca de 18 e 19/08.
NAO estao na lista, de proposito:
    ...122099463495451002  carrossel legitimo de hoje (16:45)
    ...122099465613451002  reel legitimo de hoje (16:49)
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
    ("1336325419554251_122099466057451002", "16:49:16  ACOS  (dup de 18/08 ads-acos-margem)"),
    ("1336325419554251_122099467899451002", "16:50:20  R$ 300 no painel  (dup de 17-18/08 repasse-receita-bruta)"),
    ("1336325419554251_122099469297451002", "16:51:35  saldo retido  (dup de 18/08 saldo-retido)"),
    ("1336325419554251_122099471769451002", "16:52:41  Fator R  (dup de 19/08 anexo-fator-r)"),
    ("1336325419554251_122099473515451002", "16:53:51  chargeback  (dup de 19/08 chargeback-venda-desfeita)"),
]

for pid, descricao in DUPLICADOS:
    url = f"https://graph.facebook.com/v21.0/{pid}?" + urllib.parse.urlencode(
        {"access_token": TOK})
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print(f"APAGADO  {descricao}  ->  {r.read().decode()[:80]}")
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")
        print(f"FALHOU   {descricao}  ->  HTTP {e.code}: {corpo[:200]}")
