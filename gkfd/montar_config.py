#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MONTAR CONFIG — voce cola o token, ele descobre o resto sozinho.

    py montar_config.py

POR QUE ISTO EXISTE — 18/08/2026.
Montar o config a mao pede tres coisas que ninguem sabe de cabeca: o numero da
Pagina, o numero da conta do Instagram, e qual dos dois vai em qual campo. Em
16/08 isso custou tres tentativas e um erro chato — o ig_user_id foi
sobrescrito com o numero da Pagina, e a Meta respondeu que o objeto nao
existia.

Aqui voce cola UMA coisa: o token. O script pergunta a Meta quem e esse token,
descobre o numero da Pagina, descobre qual conta de Instagram esta pendurada
nela, e escreve o arquivo inteiro. Depois confere e diz em portugues se a
corrente esta fechada.

COMO USAR
1. Crie o config_publicacao.json copiando o config_publicacao_MODELO.json
2. Cole o token no campo "page_token", dentro do bloco "facebook"
3. Rode este script

Ele NAO imprime o token. Nunca. Nem pedaco dele.

SE O TOKEN FOR DE USUARIO em vez de ser da Pagina, ele tenta se virar: lista as
Paginas que voce administra e escolhe a que combina com o nome da marca. Dando
certo, grava o token da PAGINA — que e o que nao expira.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(BASE, "config_publicacao.json")
MODELO = os.path.join(BASE, "config_publicacao_MODELO.json")
API = "https://graph.facebook.com/v21.0/"

# Pedaco do nome da Pagina desta marca. Serve so para escolher entre varias
# Paginas quando o token colado for de usuario.
MARCA = os.environ.get("MARCA_PAGINA", "GKFD")


def pega(caminho, params):
    url = API + caminho + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        try:
            m = json.loads(e.read().decode("utf-8")).get("error", {})
            return None, "%s %s: %s" % (m.get("type"), m.get("code"),
                                        m.get("message"))
        except Exception:
            return None, "HTTP %s" % e.code
    except Exception as e:
        return None, str(e)


def main():
    print("=" * 62)
    print("MONTAR CONFIG — este script nunca imprime o token")
    print("=" * 62)

    if not os.path.exists(CFG):
        if not os.path.exists(MODELO):
            sys.exit("Nao achei nem o config_publicacao.json nem o MODELO.")
        cfg = json.load(open(MODELO, encoding="utf-8"))
        print("Criei o config a partir do MODELO. Cole o token em")
        print("facebook.page_token e rode de novo.")
        json.dump(cfg, open(CFG, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        return

    cfg = json.load(open(CFG, encoding="utf-8"))
    fb = cfg.get("facebook") or {}
    token = str(fb.get("page_token") or "") or str(cfg.get("access_token") or "")

    if not token or token.startswith("COLE_AQUI"):
        sys.exit("Cole o token em facebook.page_token e rode de novo.")

    d, erro = pega("me", {"fields": "id,name", "access_token": token})
    if d is None:
        sys.exit("A Meta recusou o token: %s" % erro)

    quem_id, quem_nome = str(d.get("id")), d.get("name", "")

    # E token de Pagina? Um token de Pagina responde /me com o id da Pagina.
    teste, _ = pega(quem_id, {"fields": "instagram_business_account,name",
                              "access_token": token})
    eh_pagina = bool(teste and "instagram_business_account" in teste) or \
        bool(teste and teste.get("name") == quem_nome and quem_nome)

    if not eh_pagina or teste is None:
        print("O token parece ser de USUARIO (%s). Procurando a Pagina..." % quem_nome)
        lista, erro = pega("me/accounts",
                           {"fields": "id,name,access_token", "limit": "100",
                            "access_token": token})
        if lista is None:
            sys.exit("Nao consegui listar as Paginas: %s\n"
                     "Falta a permissao pages_show_list no token." % erro)
        alvo = None
        for pag in lista.get("data", []):
            if MARCA.lower() in str(pag.get("name", "")).lower():
                alvo = pag
                break
        if not alvo:
            nomes = ", ".join(p.get("name", "?") for p in lista.get("data", []))
            sys.exit("Nao achei Pagina com '%s' no nome. Encontrei: %s" % (MARCA, nomes))
        token = alvo["access_token"]
        quem_id, quem_nome = str(alvo["id"]), alvo["name"]
        print("Peguei o token da Pagina '%s' automaticamente." % quem_nome)

    info, erro = pega(quem_id, {"fields": "name,instagram_business_account{id,username}",
                                "access_token": token})
    if info is None:
        sys.exit("Nao consegui ler a Pagina: %s" % erro)

    ig = info.get("instagram_business_account") or {}
    if not ig.get("id"):
        print("-" * 62)
        print("A Pagina '%s' EXISTE, mas nao tem conta do Instagram" % info.get("name"))
        print("vinculada a ela. Sem isso a API nao publica no Instagram.")
        print()
        print("Conserto: no aplicativo do Instagram, na conta da marca,")
        print("Configuracoes > Central de Contas > Perfis > Adicionar contas")
        print("> Adicionar conta do Facebook, e escolher esta Pagina.")
        print("A conta do Instagram precisa ser PROFISSIONAL.")
        print("-" * 62)
        gravar(cfg, token, quem_id, "")
        sys.exit(1)

    gravar(cfg, token, quem_id, str(ig["id"]))

    print("-" * 62)
    print("Pagina do Facebook : %s  (id %s)" % (info.get("name"), quem_id))
    print("Instagram vinculado: @%s  (id %s)" % (ig.get("username"), ig["id"]))
    print("-" * 62)
    print("config_publicacao.json gravado. A corrente esta fechada.")
    print("Confira com:  py checar_token.py")
    print("=" * 62)


def gravar(cfg, token, page_id, ig_id):
    fb = cfg.get("facebook") or {}
    fb["page_id"] = page_id
    fb["page_token"] = token
    cfg["facebook"] = fb
    cfg["access_token"] = token
    if ig_id:
        cfg["ig_user_id"] = ig_id
    host = cfg.get("host") or {}
    host["tipo"] = "facebook"
    cfg["host"] = host
    json.dump(cfg, open(CFG, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
