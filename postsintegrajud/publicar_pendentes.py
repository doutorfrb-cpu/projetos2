#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica toda peca que ainda NAO foi publicada, e marca as que ja foram.

    py publicar_pendentes.py            publica as pendentes
    py publicar_pendentes.py --ver      so lista, sem publicar
    py publicar_pendentes.py --marcar 2026-08-16_alimentos-renda-socio
                                        marca como publicada sem publicar

POR QUE EXISTE
a tarefa agendada gera a peca e publica. Se ela gerar e falhar na publicacao —
internet caiu, Meta fora do ar, token expirado —, a peca fica na pasta e
ninguem repara. Este script varre as subpastas de peca, acha as que nao tem a
marca de publicada, e publica.

COMO ELE SABE o que ja saiu: ao publicar, grava um arquivo .publicado dentro da
pasta da peca. Peca com essa marca e ignorada para sempre. E por isso que ele
pode rodar de hora em hora sem republicar nada.

ATENCAO: as pecas antigas, publicadas antes deste script existir, nao tem a
marca. Na primeira vez, rode --ver e marque as antigas com --marcar, ou ele vai
republicar tudo.
"""

import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
PY_EXE = sys.executable or "python"
PADRAO = re.compile(r"^\d{4}-\d{2}-\d{2}_")
MARCA = ".publicado"


def pecas():
    saida = []
    for d in sorted(os.listdir(BASE)):
        cam = os.path.join(BASE, d)
        if not os.path.isdir(cam) or not PADRAO.match(d):
            continue
        pngs = [f for f in os.listdir(cam) if f.lower().endswith(".png")]
        if not pngs:
            continue
        saida.append((d, cam, os.path.exists(os.path.join(cam, MARCA)), len(pngs)))
    return saida


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg == "--marcar":
        if len(sys.argv) < 3:
            sys.exit("uso: py publicar_pendentes.py --marcar <pasta>")
        alvo = os.path.join(BASE, sys.argv[2])
        if not os.path.isdir(alvo):
            sys.exit(f"pasta nao encontrada: {sys.argv[2]}")
        open(os.path.join(alvo, MARCA), "w").write("marcada a mao\n")
        print(f"[pendentes] {sys.argv[2]} marcada como publicada")
        return

    lista = pecas()
    pend = [x for x in lista if not x[2]]

    print("=" * 62)
    print(f"PECAS NA PASTA: {len(lista)}   |   PENDENTES: {len(pend)}")
    print("=" * 62)
    for nome, _, publicada, n in lista:
        print(f"  {'[ja saiu]' if publicada else '[PENDENTE]'}  {nome}  ({n} imagens)")

    if arg == "--ver":
        print("\n(modo --ver: nada foi publicado)")
        return

    if not pend:
        print("\nNada a publicar.")
        return

    for nome, cam, _, _ in pend:
        print("\n" + "-" * 62)
        print(f"PUBLICANDO {nome}")
        print("-" * 62)
        r = subprocess.run([PY_EXE, os.path.join(BASE, "postar.py"), cam])
        if r.returncode == 0:
            open(os.path.join(cam, MARCA), "w").write("publicada\n")
            print(f"[pendentes] {nome} marcada como publicada")
        else:
            print(f"[pendentes] {nome} FALHOU — fica pendente para a proxima")


if __name__ == "__main__":
    main()
