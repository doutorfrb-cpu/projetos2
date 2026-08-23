#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara a pasta de trabalho da rodada.

Descompacta o gerador-gkfd.zip e, em seguida, COPIA POR CIMA os .py da raiz.
Motivo (licao de 21/08/2026 no pautas-publicadas.md): o zip esta desatualizado
— os .py dele sao anteriores ao medidor por regra e ao conserto do nome
pessoal. O zip continua util pelas FONTES (node_modules) e pelas fotos.
"""
import os
import shutil
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "work22b")

os.makedirs(WORK, exist_ok=True)

with zipfile.ZipFile(os.path.join(BASE, "gerador-gkfd.zip")) as z:
    z.extractall(WORK)
    print("zip:", len(z.namelist()), "entradas")

for nome in ("machine.py", "reel.py", "story_ad.py", "fundo_numerico.py",
             "medir.py", "retrato.py", "repor_fotos.py", "selo-platinum.png"):
    org = os.path.join(BASE, nome)
    if os.path.exists(org):
        shutil.copy2(org, os.path.join(WORK, nome))
        print("da raiz:", nome)

for pasta in ("node_modules", "fotos_banco"):
    if not os.path.isdir(os.path.join(WORK, pasta)):
        shutil.copytree(os.path.join(BASE, pasta), os.path.join(WORK, pasta))
        print("copiado da raiz:", pasta)

print("conteudo:", sorted(os.listdir(WORK)))
