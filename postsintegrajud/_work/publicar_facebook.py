#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica a peça na Página do Facebook do IntegraJud, pela Graph API.

DIFERENÇA IMPORTANTE PARA O INSTAGRAM: aqui a API aceita o ARQUIVO direto.
Não precisa hospedar as imagens em lugar nenhum — some a dependência de FTP
e de pasta pública no site. É por isso que o Facebook costuma ficar pronto
antes do Instagram.

    Instagram: sobe para o site -> manda a URL -> a Meta baixa
    Facebook:  manda o arquivo -> pronto

USO
    python3 publicar_facebook.py PASTA_DA_PECA

    A pasta é a mesma do Instagram: os três PNGs e o legenda.txt.
    Se existir legenda_facebook.txt, ele usa essa no lugar — e é o certo,
    porque no Facebook o link é clicável e a hashtag não serve de nada.

CONFIGURAÇÃO — no mesmo config_publicacao.json, um bloco novo:

    "facebook": {
      "page_id": "123456789",
      "page_token": "EAA..."
    }

O page_token é o token DA PÁGINA, não o do usuário. Sai de:
    GET /me/accounts   -> campo access_token de cada página

ESSE ARQUIVO GUARDA SEGREDO. Não versionar, não colar em conversa, não
mandar para ninguém. O script lê e nunca imprime o conteúdo.
"""

import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://graph.facebook.com/v21.0"


def log(msg):
    print(f"[facebook] {msg}", flush=True)


# ---------------------------------------------------------------- utilidades

def carregar_config(raiz):
    p = os.path.join(raiz, "config_publicacao.json")
    if not os.path.exists(p):
        sys.exit(f"ERRO: falta {p}. Veja o cabeçalho deste arquivo.")
    with open(p, encoding="utf-8") as f:
        cfg = json.load(f)
    fb = cfg.get("facebook")
    if not fb:
        sys.exit("ERRO: config_publicacao.json sem o bloco 'facebook'. "
                 "A publicação no Facebook ainda não foi configurada.")
    for chave in ("page_id", "page_token"):
        if not fb.get(chave) or str(fb[chave]).startswith("COLE_AQUI"):
            sys.exit(f"ERRO: bloco 'facebook' sem '{chave}'.")
    return fb


def erro_meta(e):
    try:
        corpo = json.loads(e.read().decode())
        m = corpo.get("error", {})
        return f"{m.get('type')} {m.get('code')}: {m.get('message')}"
    except Exception:
        return str(e)


def multipart(campos, arquivo_campo, caminho):
    """Monta um corpo multipart/form-data à mão, sem dependência externa."""
    limite = f"----integrajud{uuid.uuid4().hex}"
    linhas = []
    for k, v in campos.items():
        linhas.append(f"--{limite}\r\n"
                      f'Content-Disposition: form-data; name="{k}"\r\n\r\n'
                      f"{v}\r\n".encode())
    nome = os.path.basename(caminho)
    tipo = mimetypes.guess_type(nome)[0] or "application/octet-stream"
    linhas.append(f"--{limite}\r\n"
                  f'Content-Disposition: form-data; name="{arquivo_campo}"; '
                  f'filename="{nome}"\r\n'
                  f"Content-Type: {tipo}\r\n\r\n".encode())
    with open(caminho, "rb") as f:
        linhas.append(f.read())
    linhas.append(f"\r\n--{limite}--\r\n".encode())
    return b"".join(linhas), f"multipart/form-data; boundary={limite}"


# ------------------------------------------------------------------ publicar

def subir_foto(fb, caminho):
    """Sobe a foto SEM publicar e devolve o id, para virar anexo do post."""
    corpo, content_type = multipart(
        {"published": "false", "access_token": fb["page_token"]},
        "source", caminho)
    req = urllib.request.Request(f"{API}/{fb['page_id']}/photos", data=corpo)
    req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())["id"]


def publicar_post(fb, ids, legenda):
    campos = {"message": legenda, "access_token": fb["page_token"]}
    for i, mid in enumerate(ids):
        campos[f"attached_media[{i}]"] = json.dumps({"media_fbid": mid})
    dados = urllib.parse.urlencode(campos).encode()
    req = urllib.request.Request(f"{API}/{fb['page_id']}/feed", data=dados)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())["id"]


def legenda_da_pasta(pasta):
    """legenda_facebook.txt tem prioridade; senão adapta a do Instagram."""
    fb_txt = os.path.join(pasta, "legenda_facebook.txt")
    if os.path.exists(fb_txt):
        return open(fb_txt, encoding="utf-8").read().strip(), "legenda_facebook.txt"

    ig_txt = os.path.join(pasta, "legenda.txt")
    if not os.path.exists(ig_txt):
        return "", "nenhuma"

    linhas = open(ig_txt, encoding="utf-8").read().splitlines()
    # tira o bloco de hashtags: no Facebook não serve para nada
    limpas = [l for l in linhas if not l.strip().startswith("#")]
    texto = "\n".join(limpas).rstrip()
    log("adaptei a legenda do Instagram: hashtags removidas. "
        "O ideal é escrever uma legenda_facebook.txt com o link no CTA.")
    return texto, "legenda.txt adaptada"


# ---------------------------------------------------------------------- main

def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 publicar_facebook.py PASTA_DA_PECA")

    pasta = os.path.abspath(sys.argv[1])
    if not os.path.isdir(pasta):
        sys.exit(f"ERRO: pasta não encontrada: {pasta}")
    raiz = os.path.dirname(pasta)

    pngs = sorted(f for f in os.listdir(pasta) if f.lower().endswith(".png"))
    if not pngs:
        sys.exit("ERRO: nenhuma imagem na pasta.")
    if len(pngs) > 10:
        sys.exit("ERRO: no máximo 10 imagens por post.")
    caminhos = [os.path.join(pasta, n) for n in pngs]

    for c in caminhos:
        mb = os.path.getsize(c) / 1048576
        if mb > 10:
            sys.exit(f"ERRO: {os.path.basename(c)} tem {mb:.1f} MB. O limite é 10 MB.")

    legenda, origem = legenda_da_pasta(pasta)
    fb = carregar_config(raiz)

    log(f"{len(caminhos)} imagens · legenda de {origem} "
        f"({len(legenda)} caracteres)")

    try:
        ids = []
        for c in caminhos:
            ids.append(subir_foto(fb, c))
            log(f"enviada: {os.path.basename(c)}")
        post_id = publicar_post(fb, ids, legenda)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO da Meta: {erro_meta(e)}")

    log(f"PUBLICADO na Página. id do post: {post_id}")
    print(post_id)


if __name__ == "__main__":
    main()
