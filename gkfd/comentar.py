#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PRIMEIRO COMENTARIO COM O LINK — o feed nao carrega link, o comentario sim.

    py comentar.py <ig_media_id> <fb_post_id> "<tema da peca>"
    py comentar.py 18144384151503408 1336325419554251_1220961371 "chargeback"

POR QUE ISTO EXISTE — 19/08/2026.
Imagem de post do Instagram nao clica. A instrucao ja proibe escrever "clique"
ou desenhar seta na arte justamente por isso. Mas o COMENTARIO clica — e ate
hoje a gente publicava e nao deixava link em lugar nenhum.

Este script publica o primeiro comentario nos dois destinos, com o link wa.me
que carrega a origem (veja links.py). Assim a pessoa que quer falar tem para
onde ir, e voce sabe de onde ela veio.

FIXAR o comentario nao e possivel pela API — nao existe endpoint. Fixar e no
aplicativo, dois toques, e so vale a pena nas pecas que engrenarem.

Nao imprime o token. Falhando, nao derruba nada: a peca ja esta publicada.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(BASE, "config_publicacao.json")
API = "https://graph.facebook.com/v21.0"

sys.path.insert(0, BASE)
try:
    import links as L
except Exception:
    L = None


def post(caminho, campos):
    d = urllib.parse.urlencode(campos).encode("utf-8")
    req = urllib.request.Request("%s/%s" % (API, caminho), data=d, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        try:
            m = json.loads(e.read().decode("utf-8")).get("error", {})
            return None, "%s %s: %s" % (m.get("type"), m.get("code"), m.get("message"))
        except Exception:
            return None, "HTTP %s" % e.code
    except Exception as e:
        return None, str(e)


def main():
    if len(sys.argv) < 3:
        sys.exit("uso: py comentar.py <ig_media_id> <fb_post_id> \"<tema>\"")
    ig_id, fb_id = sys.argv[1], sys.argv[2]
    tema = sys.argv[3] if len(sys.argv) > 3 else ""

    if not os.path.exists(CFG):
        sys.exit("Nao achei o config_publicacao.json.")
    cfg = json.load(open(CFG, encoding="utf-8"))
    token = (cfg.get("facebook") or {}).get("page_token") or cfg.get("access_token")
    if not token:
        sys.exit("Sem token no config.")

    placar = []
    for destino, alvo in (("instagram", ig_id), ("facebook", fb_id)):
        if not alvo or alvo in ("-", "0"):
            continue
        url = L.link("carrossel", destino, tema) if L else "https://wa.me/5511977237113"
        texto = "Quer que eu olhe o seu caso? %s" % url
        if L and L.MARCA == "GKFD":
            texto = "Quer que eu olhe a sua operação? %s" % url
        d, erro = post("%s/comments" % alvo,
                       {"message": texto, "access_token": token})
        if d:
            placar.append("%s ok" % destino)
        else:
            placar.append("%s FALHOU (%s)" % (destino, erro))

    print(" | ".join(placar) if placar else "nenhum id valido recebido")
    print("Fixar o comentario e no aplicativo — a API nao fixa.")


if __name__ == "__main__":
    main()
