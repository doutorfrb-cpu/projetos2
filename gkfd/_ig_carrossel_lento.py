#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica o carrossel no Instagram com PAUSA entre as chamadas.

Motivo (23/08/2026): o publicar_instagram.py faz 12 chamadas a Graph API em
poucos segundos (5 hospedagens, 5 filhos, o pai e o status). Com a cota do app
ja gasta, a rajada estoura OAuthException 4 justamente no primeiro status do
container pai, e o container morre com "Media upload has failed". As mesmas
chamadas, espacadas, passam.

Nao imprime token. Uso:  py _ig_carrossel_lento.py <pasta_da_peca>
"""
import os
import re
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import publicar_instagram as pi

PAUSA = 20


def slides(pasta):
    def num(nome):
        b = nome.lower()
        if b.startswith("_") or "story" in b or "reel" in b:
            return None
        m = re.search(r"_(\d+)\.png$", b)
        return int(m.group(1)) if m else None
    nomes = sorted((f for f in os.listdir(pasta) if num(f) is not None),
                   key=num)
    return [os.path.join(pasta, n) for n in nomes]


def main():
    pasta = os.path.abspath(sys.argv[1])
    cfg = pi.carregar_config(BASE)
    caminhos = slides(pasta)
    print("slides:", [os.path.basename(c) for c in caminhos], flush=True)

    legenda = open(os.path.join(pasta, "legenda.txt"), encoding="utf-8").read().strip()
    alts = []
    alt_path = os.path.join(pasta, "alt.txt")
    if os.path.exists(alt_path):
        alts = [l.strip() for l in open(alt_path, encoding="utf-8")
                if l.strip()]

    urls = pi.hospedar(cfg, cfg.get("host", {}), caminhos)
    print("hospedadas:", len(urls), flush=True)

    filhos = []
    for i, u in enumerate(urls):
        time.sleep(PAUSA)
        alt = alts[i] if i < len(alts) else ""
        fid = pi.criar_filho(cfg, u, alt)
        filhos.append(fid)
        print(f"filho {i+1}/{len(urls)}: {fid}", flush=True)

    time.sleep(PAUSA)
    pai = pi.criar_pai(cfg, filhos, legenda)
    print("container pai:", pai, flush=True)

    for tentativa in range(1, 16):
        time.sleep(PAUSA)
        try:
            r = pi.http_get(f"{pi.API}/{pai}", {
                "fields": "status_code,status",
                "access_token": cfg["access_token"],
            })
        except Exception as e:
            print("status falhou:", pi.erro_meta(e), flush=True)
            continue
        st = r.get("status_code")
        print(f"container {pai}: {st} ({tentativa}/15)", flush=True)
        if st == "FINISHED":
            break
        if st == "ERROR":
            print("container em ERROR:", r.get("status"))
            sys.exit(1)
    else:
        print("nao ficou pronto")
        sys.exit(1)

    time.sleep(PAUSA)
    try:
        mid = pi.publicar(cfg, pai)
    except Exception as e:
        print("erro ao publicar:", pi.erro_meta(e))
        sys.exit(1)
    print("IG CARROSSEL PUBLICADO. media id:", mid)


main()
