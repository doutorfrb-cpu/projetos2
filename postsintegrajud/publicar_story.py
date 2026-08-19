#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica um STORY no @integrajud pela API da Meta.

    py publicar_story.py caminho/da/imagem_9x16.png

POR QUE ISTO EXISTE — 17/08/2026.
O carrossel constroi acervo, mas so aparece para quem ja segue e abre o feed.
O story aparece no topo da tela de quem segue, todo dia, e custa zero a mais:
a arte 9:16 sai do MESMO spec da peca, pelo story_ad.py que ja existia parado
na pasta desde o comeco.

COMO FUNCIONA
Igual ao carrossel: a imagem sobe na propria Pagina do Facebook como NAO
PUBLICADA e TEMPORARIA, a Meta devolve uma URL de CDN, e essa URL vira o
image_url do container. A unica diferenca e media_type=STORIES.
Nenhum FTP, nenhuma pasta no site, nenhum navegador.

O story vive 24 horas. Nao entra no perfil, nao tem legenda e nao aceita
hashtag — quem quiser o texto vai no post. Por isso a arte 9:16 tem que se
bastar sozinha: e o gancho, nao a peca inteira.

O QUE ELE NAO FAZ
Nao poe link, nao poe enquete, nao poe figurinha. A API nao publica nenhum
desses elementos interativos — eles so existem pelo aplicativo. Precisando de
link no story, publique por aqui e depois adicione a figurinha pelo celular.

NUNCA receber, ver, colar ou guardar token. O script le do
config_publicacao.json e nao imprime nada dele.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import publicar_instagram as pi   # noqa: E402

API = pi.API


def log(msg):
    print("[story] %s" % msg, flush=True)


def esperar(container, token, tentativas=20):
    """Imagem costuma ficar pronta na hora, mas conferimos assim mesmo."""
    for _ in range(tentativas):
        try:
            d = pi.http_get("%s/%s" % (API, container),
                            {"fields": "status_code,status",
                             "access_token": token})
        except urllib.error.HTTPError as e:
            log("aviso ao consultar o container: %s" % pi.erro_meta(e))
            return True
        st = d.get("status_code", "")
        if st == "FINISHED":
            return True
        if st == "ERROR":
            log("a Meta recusou a midia: %s" % d.get("status", ""))
            return False
        time.sleep(3)
    return True


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: py publicar_story.py caminho/da/imagem_9x16.png")

    arquivo = sys.argv[1]
    if not os.path.exists(arquivo):
        sys.exit("ERRO: nao achei o arquivo %s" % arquivo)

    cfg = pi.carregar_config(BASE)
    token = cfg["access_token"]
    ig = str(cfg["ig_user_id"])

    print("=" * 62)
    print("STORY: %s" % os.path.basename(arquivo))
    print("=" * 62)

    urls = pi.hospedar(cfg, cfg["host"], [arquivo])
    if not urls:
        sys.exit("ERRO: nao consegui hospedar a imagem.")
    log("imagem hospedada na Meta")

    try:
        d = pi.http_post("%s/%s/media" % (API, ig),
                         {"image_url": urls[0],
                          "media_type": "STORIES",
                          "access_token": token})
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao criar o container do story: %s" % pi.erro_meta(e))

    container = d.get("id")
    if not container:
        sys.exit("ERRO: a Meta nao devolveu id de container.")
    log("container %s criado" % container)

    if not esperar(container, token):
        sys.exit("ERRO: a midia nao ficou pronta.")

    try:
        d = pi.http_post("%s/%s/media_publish" % (API, ig),
                         {"creation_id": container, "access_token": token})
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao publicar o story: %s" % pi.erro_meta(e))

    print("=" * 62)
    print("STORY PUBLICADO — id %s" % d.get("id"))
    print("Ele fica no ar por 24 horas.")
    print("=" * 62)


if __name__ == "__main__":
    main()
