#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica STORY e REEL da peca nos QUATRO lugares, com um comando so.

    py extras.py 2026-08-17_impugnacao-penhora-faturamento
    py extras.py <pasta> --sem-reel        (peca das 12h)
    py extras.py <pasta> --so-reel

POR QUE ISTO EXISTE — 17/08/2026.
Publicar story e reel a mao sao quatro comandos, e quatro comandos numa rotina
automatica sao quatro lugares para falhar em silencio. Aqui e um so, e cada
destino que falha aparece no placar sem derrubar os outros — a mesma regra do
postar.py: um destino nao segura o outro.

O QUE ELE ESPERA ENCONTRAR na pasta da peca:
    story_916.png     arte 9:16, gerada pelo story_ad.py com --limpo
    reel.mp4          video 9:16, gerado pelo reel.py
    legenda.txt          legenda do Instagram
    legenda_facebook.txt legenda da Pagina, sem hashtag

Faltando um dos arquivos, ele avisa e pula — nao inventa e nao para o resto.

CADENCIA: story em toda peca; reel so na peca das 18h. Na das 12h, use
--sem-reel. Dois reels por dia saturam o perfil e demoram a renderizar.
"""

import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))


def roda(descricao, argumentos):
    print("\n" + "-" * 62)
    print(">> %s" % descricao)
    print("-" * 62)
    r = subprocess.run([sys.executable] + argumentos, cwd=BASE)
    ok = r.returncode == 0
    print("   %s" % ("OK" if ok else "FALHOU"))
    return ok


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        sys.exit("uso: py extras.py <pasta_da_peca> [--sem-reel] [--so-reel]")

    pasta = args[0]
    if not os.path.isdir(pasta):
        pasta2 = os.path.join(BASE, args[0])
        if os.path.isdir(pasta2):
            pasta = pasta2
        else:
            sys.exit("ERRO: nao achei a pasta %s" % args[0])

    quer_story = "--so-reel" not in flags
    quer_reel = "--sem-reel" not in flags

    story = os.path.join(pasta, "story_916.png")
    reel = os.path.join(pasta, "reel.mp4")

    print("=" * 62)
    print("EXTRAS: %s" % os.path.basename(os.path.abspath(pasta)))
    print("story: %s | reel: %s"
          % ("sim" if quer_story else "nao", "sim" if quer_reel else "nao"))
    print("=" * 62)

    placar = []

    if quer_story:
        if os.path.exists(story):
            placar.append(("Story Instagram",
                           roda("Story no Instagram",
                                ["publicar_story.py", story])))
            placar.append(("Story Pagina",
                           roda("Story na Pagina do Facebook",
                                ["publicar_fb_extras.py", "--story", story])))
        else:
            print("\n!! nao achei story_916.png na pasta — story pulado")
            placar.append(("Story", None))

    if quer_reel:
        if os.path.exists(reel):
            placar.append(("Reel Instagram",
                           roda("Reel no Instagram",
                                ["publicar_reel.py", reel])))
            placar.append(("Reel Pagina",
                           roda("Reel na Pagina do Facebook",
                                ["publicar_fb_extras.py", "--reel", reel])))
        else:
            print("\n!! nao achei reel.mp4 na pasta — reel pulado")
            placar.append(("Reel", None))

    print("\n" + "=" * 62)
    print("PLACAR DOS EXTRAS")
    for nome, ok in placar:
        estado = "PUBLICADO" if ok else ("PULADO" if ok is None else "FALHOU")
        print("  %-18s: %s" % (nome, estado))
    print("=" * 62)
    print("O carrossel nao depende disto. Falhando aqui, a rodada esta feita.")

    if any(ok is False for _, ok in placar):
        sys.exit(1)


if __name__ == "__main__":
    main()
