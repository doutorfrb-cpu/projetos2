#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STORY e REEL na PAGINA do Facebook, pela API.

    py publicar_fb_extras.py --story caminho/da/imagem_9x16.png
    py publicar_fb_extras.py --reel  caminho/do/reel.mp4 [legenda.txt]

POR QUE ISTO EXISTE — 17/08/2026.
A Pagina tem os dois formatos, com endpoints proprios e diferentes dos do
Instagram. O reel da Pagina importa: o Facebook distribui reel para quem NAO
segue, e o publico dele e mais velho — que e justamente a faixa do advogado
com escritorio montado, ao contrario do publico de 18 a 24 anos que o anuncio
aberto andava comprando. O mesmo mp4 serve nos dois destinos: gera uma vez,
publica em dois lugares.

O story da Pagina rende pouco — quase ninguem assiste story de Pagina. Ficou
implementado porque o custo era baixo, mas nao espere numero dele.

COMO FUNCIONA — sao dois caminhos distintos.

STORY  e em duas etapas: a foto sobe na Pagina como NAO PUBLICADA (nao vira
post, nao aparece no feed), e o id dela e entregue ao /photo_stories.

REEL   e em tres fases: pede-se o container (upload_phase=start), mandam-se os
bytes para o endereco que a Meta devolve, e fecha-se com upload_phase=finish e
video_state=PUBLISHED. O Facebook tambem transcodifica, entao o finish pode
demorar; o script tenta de novo por alguns minutos antes de desistir.

NUNCA receber, ver, colar ou guardar token. O script le do
config_publicacao.json e nao imprime nada dele.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import publicar_facebook as pf        # noqa: E402
import publicar_instagram as pi       # noqa: E402

API = pf.API


def log(msg):
    print("[fb] %s" % msg, flush=True)


def contexto():
    cfg = pi.carregar_config(BASE)
    fb = cfg.get("facebook") or {}
    if not fb.get("page_id") or str(fb["page_id"]).startswith("COLE_AQUI"):
        sys.exit("ERRO: falta o page_id no bloco 'facebook' do config.")
    token = pf.resolver_page_token(cfg, dict(fb))
    return str(fb["page_id"]), token


# ------------------------------------------------------------------- story

def story(caminho):
    page, token = contexto()

    corpo, tipo = pf.multipart(
        {"published": "false", "access_token": token}, "source", caminho)
    req = urllib.request.Request("%s/%s/photos" % (API, page), data=corpo)
    req.add_header("Content-Type", tipo)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao subir a foto do story: %s" % pf.erro_meta(e))

    foto = resp.get("id")
    if not foto:
        sys.exit("ERRO: a Meta nao devolveu id da foto.")
    log("foto %s enviada (nao publicada)" % foto)

    try:
        d = pi.http_post("%s/%s/photo_stories" % (API, page),
                         {"photo_id": foto, "access_token": token})
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao publicar o story da Pagina: %s" % pf.erro_meta(e))

    print("STORY DA PAGINA PUBLICADO — %s" % (d.get("post_id") or d))


# -------------------------------------------------------------------- reel

def reel(caminho, legenda):
    page, token = contexto()
    tamanho = os.path.getsize(caminho)

    try:
        d = pi.http_post("%s/%s/video_reels" % (API, page),
                         {"upload_phase": "start", "access_token": token})
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao abrir o upload do reel: %s" % pf.erro_meta(e))

    video_id = d.get("video_id")
    destino = d.get("upload_url")
    if not video_id or not destino:
        sys.exit("ERRO: a Meta nao devolveu video_id e upload_url.")
    log("container %s aberto" % video_id)

    with open(caminho, "rb") as f:
        dados = f.read()
    req = urllib.request.Request(destino, data=dados, method="POST")
    req.add_header("Authorization", "OAuth %s" % token)
    req.add_header("offset", "0")
    req.add_header("file_size", str(tamanho))
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            r.read()
    except urllib.error.HTTPError as e:
        sys.exit("ERRO ao enviar os bytes do reel: %s" % pf.erro_meta(e))
    log("video enviado (%.1f MB)" % (tamanho / 1e6))

    campos = {"upload_phase": "finish",
              "video_id": video_id,
              "video_state": "PUBLISHED",
              "access_token": token}
    if legenda:
        campos["description"] = legenda

    # O Facebook tambem transcodifica. Enquanto nao termina, o finish recusa.
    limite = time.time() + 8 * 60
    ultimo = ""
    while True:
        try:
            d = pi.http_post("%s/%s/video_reels" % (API, page), campos)
            break
        except urllib.error.HTTPError as e:
            ultimo = pf.erro_meta(e)
            if time.time() > limite:
                sys.exit("ERRO ao fechar o reel: %s" % ultimo)
            log("ainda processando, tentando de novo em 15s")
            time.sleep(15)

    print("REEL DA PAGINA PUBLICADO — video %s" % video_id)


# --------------------------------------------------------------------- cli

def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("--story", "--reel"):
        sys.exit("uso: py publicar_fb_extras.py --story img.png\n"
                 "     py publicar_fb_extras.py --reel reel.mp4 [legenda.txt]")

    modo, caminho = sys.argv[1], sys.argv[2]
    if not os.path.exists(caminho):
        sys.exit("ERRO: nao achei %s" % caminho)

    if modo == "--story":
        story(caminho)
        return

    legenda = ""
    alvo = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
        os.path.dirname(os.path.abspath(caminho)), "legenda_facebook.txt")
    if os.path.exists(alvo):
        legenda = open(alvo, encoding="utf-8").read().strip()
    reel(caminho, legenda)


if __name__ == "__main__":
    main()
