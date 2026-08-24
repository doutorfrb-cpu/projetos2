#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marca TODA peca ja existente como publicada, para o publicar_pendentes.py
nao republicar o acervo.

MOTIVO (23/08/2026): nenhuma pasta de peca da GKFD tinha o arquivo .publicado.
O proprio publicar_pendentes.py avisa disso no cabecalho — "as pecas antigas,
publicadas antes deste script existir, nao tem a marca; na primeira vez, rode
--ver e marque as antigas" — e ninguem nunca fez essa marcacao. Resultado: na
primeira vez que alguem rodou o script achando que ele reenviaria a peca do
dia, ele comecou a republicar o acervo inteiro, do mais antigo para o mais
novo. Cinco pecas sairam de novo no Facebook e quatro no Instagram antes de
ser morto.

As do Facebook foram apagadas pela API. As do Instagram nao tem endpoint de
exclusao e ficaram para o aplicativo.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
PADRAO = re.compile(r"^\d{4}-\d{2}-\d{2}_")

for d in sorted(os.listdir(BASE)):
    cam = os.path.join(BASE, d)
    if not os.path.isdir(cam) or not PADRAO.match(d):
        continue
    marca = os.path.join(cam, ".publicado")
    if os.path.exists(marca):
        print("ja tinha:", d)
        continue
    with open(marca, "w", encoding="utf-8") as f:
        f.write("marcada em 23/08/2026: peca ja publicada antes desta marcacao\n")
    print("MARCADA :", d)
