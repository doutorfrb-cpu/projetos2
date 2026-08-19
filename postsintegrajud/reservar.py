#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reserva a pauta ANTES de produzir, para duas sessoes nao colidirem.

    py reservar.py --ver
    py reservar.py "A18 consumidor | ACAO REVISIONAL | SE ISSO ESTA NO SEU PROCESSO"
    py reservar.py --liberar

POR QUE ISTO EXISTE — 16/08/2026.
O pautas-publicadas.md coordena a antirrepeticao, mas ele so recebe a linha
DEPOIS de publicar. Naquele dia, duas producoes rodaram na mesma janela de dois
minutos: uma tarefa agendada e uma sessao de teste. As duas leram o mesmo log,
as duas viram que a area A18 e a peca ACAO REVISIONAL estavam livres, e as duas
escolheram o mesmo tema. Sairam dois posts gemeos, lado a lado no perfil, com a
mesma tarja e a mesma frase de efeito.

O log resolve repeticao ao longo do tempo. Ele nao resolve producao simultanea.
Este arquivo resolve: quem escolhe a pauta RESERVA primeiro, e quem chegar
depois enxerga a reserva e escolhe outra coisa.

REGRA DE USO, na ordem:
  1. ler o log
  2. `py reservar.py --ver`  -> se houver reserva viva, NAO repetir aquela area,
     aquela peca processual nem aquela frase de efeito
  3. escolher a pauta e RESERVAR
  4. produzir e publicar
  5. gravar a linha no log e `py reservar.py --liberar`

A reserva VENCE SOZINHA em 45 minutos. Producao que travar no meio nao deixa o
proximo disparo bloqueado para sempre.
"""

import json
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(BASE, "pauta-em-producao.json")
VALIDADE = 45 * 60  # segundos


def ler():
    if not os.path.exists(ARQ):
        return None
    try:
        d = json.load(open(ARQ, encoding="utf-8"))
    except Exception:
        return None
    if time.time() - float(d.get("em", 0)) > VALIDADE:
        return None          # reserva vencida, vale como inexistente
    return d


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "--ver"

    if arg == "--liberar":
        if os.path.exists(ARQ):
            os.remove(ARQ)
            print("[reserva] liberada")
        else:
            print("[reserva] nao havia reserva")
        return

    if arg == "--ver":
        d = ler()
        if not d:
            print("[reserva] NENHUMA reserva viva — o caminho esta livre")
        else:
            idade = int((time.time() - float(d["em"])) / 60)
            print(f"[reserva] EM PRODUCAO ha {idade} min por outra sessao:")
            print(f"          {d['pauta']}")
            print("          NAO use esta area, esta peca processual nem esta frase.")
        return

    d = ler()
    if d:
        print("[reserva] ATENCAO: ja existe reserva viva:")
        print(f"          {d['pauta']}")
        print("[reserva] escolha outra pauta e reserve de novo.")
        sys.exit(1)

    json.dump({"pauta": arg, "em": time.time()},
              open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[reserva] reservado: {arg}")
    print("[reserva] lembre de rodar  py reservar.py --liberar  ao final")


if __name__ == "__main__":
    main()
