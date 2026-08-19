#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica um REEL no @integrajud pela API da Meta.

    py publicar_reel.py caminho/do/reel.mp4
    py publicar_reel.py caminho/do/reel.mp4 caminho/da/legenda.txt

POR QUE ISTO EXISTE — 17/08/2026.
Em conta pequena, reel alcanca muito mais que carrossel: o Instagram distribui
reel para quem NAO segue, e carrossel praticamente so para quem ja segue. Com
o perfil marcando de 0 a 3 visualizacoes por post organico, esse e o unico
caminho gratuito com chance real de sair da bolha.

O reel.py, que ja existia, anima o MESMO sistema visual da peca em 9:16 — os
numeros entrando em cena. Nao e video de IA com escritorio generico: e a
demonstracao acontecendo.

COMO FUNCIONA — e aqui e diferente da foto.
Video nao passa pela hospedagem na Pagina. A Meta tem um caminho proprio, o
upload RETOMAVEL: o script pede um container, recebe um endereco de upload, e
manda os bytes do arquivo direto para la. Sem URL publica, sem FTP, sem site.

Depois de subir, o video NAO fica pronto na hora — a Meta transcodifica. O
script fica perguntando de dez em dez segundos ate a Meta responder FINISHED,
e so entao publica. Reel de vinte segundos costuma levar de meio minuto a dois.

REQUISITOS DO ARQUIVO, segundo a Meta:
    MP4 com video H.264 e audio AAC (mesmo mudo, o container precisa ser MP4)
    9:16, entre 3 segundos e 15 minutos
    ate 1 GB

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
    print("[reel] %s" % msg, flush=True)


def subir_bytes(uri, token, caminho):
    """Upload retomavel: manda o arquivo inteiro de uma vez."""
    tamanho = os.path.getsize(caminho)
    with open(caminho, "rb") as f:
        corpo = f.read()
    req = urllib.request.Request(uri, data=corpo, method="POST")
    req.add_header("Authorization", "OAuth %s" % token)
    req.add_header("offset", "0")
    req.add_header("file_size", str(tamanho))
    req.add_header("Content-Type", "application/octet-stream")
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao enviar o video: %s" % pi.erro_meta(e))


def esperar(container, token, minutos=10):
    """A Meta transcodifica. Sem esperar, o media_publish falha."""
    limite = time.time() + minutos * 60
    ultimo = ""
    while time.time() < limite:
        try:
            d = pi.http_get("%s/%s" % (API, container),
                            {"fields": "status_code,status",
                             "access_token": token})
        except urllib.error.HTTPError as e:
            sys.exit("ERRO ao consultar o container: %s" % pi.erro_meta(e))
        st = d.get("status_code", "")
        if st != ultimo:
            log("estado: %s" % (st or "?"))
            ultimo = st
        if st == "FINISHED":
            return True
        if st == "ERROR":
            log("a Meta recusou o video: %s" % d.get("status", ""))
            return False
        time.sleep(10)
    log("passou de %d minutos esperando a Meta processar." % minutos)
    return False


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: py publicar_reel.py caminho/do/reel.mp4 [legenda.txt]")

    video = sys.argv[1]
    if not os.path.exists(video):
        sys.exit("ERRO: nao achei o arquivo %s" % video)

    legenda = ""
    if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
        legenda = open(sys.argv[2], encoding="utf-8").read().strip()
    else:
        irmao = os.path.join(os.path.dirname(os.path.abspath(video)),
                             "legenda.txt")
        if os.path.exists(irmao):
            legenda = open(irmao, encoding="utf-8").read().strip()

    if len(legenda) > 2200:
        log("legenda com %d caracteres, cortando para 2200." % len(legenda))
        legenda = legenda[:2197].rstrip() + "..."

    cfg = pi.carregar_config(BASE)
    token = cfg["access_token"]
    ig = str(cfg["ig_user_id"])
    mb = os.path.getsize(video) / (1024.0 * 1024.0)

    print("=" * 62)
    print("REEL: %s  (%.1f MB)" % (os.path.basename(video), mb))
    print("legenda com %d caracteres" % len(legenda))
    print("=" * 62)

    campos = {"media_type": "REELS",
              "upload_type": "resumable",
              "access_token": token}
    if legenda:
        campos["caption"] = legenda
    try:
        d = pi.http_post("%s/%s/media" % (API, ig), campos)
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao criar o container do reel: %s" % pi.erro_meta(e))

    container = d.get("id")
    uri = d.get("uri")
    if not container or not uri:
        sys.exit("ERRO: a Meta nao devolveu container e endereco de upload.")
    log("container %s criado" % container)

    log("enviando o video...")
    resp = subir_bytes(uri, token, video)
    if not resp.get("success", True):
        sys.exit("ERRO: a Meta recusou o upload: %s" % json.dumps(resp))
    log("video enviado, aguardando a Meta processar")

    if not esperar(container, token):
        sys.exit("ERRO: o video nao ficou pronto.")

    try:
        d = pi.http_post("%s/%s/media_publish" % (API, ig),
                         {"creation_id": container, "access_token": token})
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao publicar o reel: %s" % pi.erro_meta(e))

    print("=" * 62)
    print("REEL PUBLICADO — id %s" % d.get("id"))
    print("=" * 62)


if __name__ == "__main__":
    main()
