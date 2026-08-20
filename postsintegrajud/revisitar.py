#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REVISITAR — republica a capa de uma peca antiga como story.

    py revisitar.py            escolhe sozinho a peca mais antiga nao revisitada
    py revisitar.py --lista    so mostra o que existe, nao publica
    py revisitar.py 2026-08-18_saldo-retido

POR QUE ISTO EXISTE — 19/08/2026.
Cada peca vive 48 horas e morre. Uma peca de tres semanas atras e NOVA para
quem comecou a seguir semana passada — e a conta cresce todo dia. Hoje nada
recicla: e material ja pago, ja produzido, ja revisado, indo para o lixo.

Um story de arquivo por dia e alcance de graca. E o story vai para quem JA
segue, que e o publico mais qualificado que existe.

Guarda quem ja foi em .revisitados.txt para nao repetir. Nao toca no feed,
nao altera peca nenhuma, nao imprime token.
"""
import io
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MARCA = os.path.join(BASE, ".revisitados.txt")


def pastas():
    fs = []
    for n in sorted(os.listdir(BASE)):
        d = os.path.join(BASE, n)
        if not os.path.isdir(d) or not n[:4].isdigit():
            continue
        capa = [f for f in os.listdir(d)
                if f.lower().endswith("_1.png") and not f.startswith("_")]
        if capa:
            fs.append((n, os.path.join(d, capa[0])))
    return fs


def ja_foram():
    if not os.path.exists(MARCA):
        return set()
    return set(l.strip() for l in io.open(MARCA, encoding="utf-8") if l.strip())


def main():
    todas = pastas()
    if not todas:
        sys.exit("Nenhuma peca com capa encontrada.")
    feitas = ja_foram()

    if "--lista" in sys.argv:
        for n, _ in todas:
            print("%s  %s" % ("[ja]" if n in feitas else "    ", n))
        print("\n%d pecas, %d ja revisitadas" % (len(todas), len(feitas)))
        return

    alvo = None
    pedido = [a for a in sys.argv[1:] if not a.startswith("-")]
    if pedido:
        alvo = next((t for t in todas if t[0] == pedido[0]), None)
        if not alvo:
            sys.exit("Nao achei a pasta %s" % pedido[0])
    else:
        # a mais antiga que ainda nao foi; esgotando, recomeca do inicio
        alvo = next((t for t in todas if t[0] not in feitas), None)
        if not alvo:
            print("Todas ja foram revisitadas. Zerando a marcacao e recomecando.")
            os.remove(MARCA)
            alvo = todas[0]

    nome, capa = alvo
    print("Revisitando: %s" % nome)
    r = subprocess.run([sys.executable, os.path.join(BASE, "publicar_story.py"), capa])
    if r.returncode != 0:
        sys.exit("publicar_story.py falhou. Nada foi marcado.")
    with io.open(MARCA, "a", encoding="utf-8") as fh:
        fh.write(nome + "\n")
    print("Story publicado e marcado. Proxima vez pega outra.")


if __name__ == "__main__":
    main()
