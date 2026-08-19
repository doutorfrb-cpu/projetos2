#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grava no config_publicacao.json o token da PAGINA, que NAO EXPIRA.

    py fixar_token.py

O QUE ELE FAZ, e por que existe:

O token de USUARIO, mesmo estendido, morre em 60 dias e obriga a renovar o
arquivo de tempos em tempos. O token da PAGINA, quando nasce de um token de
usuario de longa duracao, nao tem data de expiracao — o Depurador da Meta
mostra "Nunca". E ele publica tanto na Pagina quanto no Instagram vinculado
a ela. Ou seja: e o token certo para os dois campos do arquivo.

Este script faz a troca sozinho:
  1. le o token que ja esta no config_publicacao.json
  2. pergunta a Meta qual e o token da sua Pagina
  3. confere se ele e mesmo do tipo PAGE e sem data de expiracao
  4. guarda uma copia de seguranca do arquivo
  5. grava o token novo nos DOIS campos

NADA e impresso na tela alem de nome, tipo e validade. O token nao aparece,
nao vai para a area de transferencia e nao sai do seu computador.
"""

import json
import os
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(BASE, "config_publicacao.json")
API = "https://graph.facebook.com/v21.0"


def get(caminho, params):
    url = f"{API}/{caminho}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=45) as r:
            return json.loads(r.read().decode()), None
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode()).get("error", {})
            return None, f"{err.get('type')} {err.get('code')}: {err.get('message')}"
        except Exception:
            return None, str(e)
    except Exception as e:
        return None, str(e)


def descrever(token):
    """Devolve (tipo, nome, expira_em) sem imprimir o token."""
    d, err = get("debug_token", {"input_token": token, "access_token": token})
    if err:
        return None, None, None
    info = d.get("data", {})
    return info.get("type"), info.get("profile_id"), info.get("expires_at", 0)


def main():
    print("=" * 64)
    print("FIXAR O TOKEN QUE NAO EXPIRA")
    print("Nada de token e impresso aqui. Nada sai deste computador.")
    print("=" * 64)

    if not os.path.exists(CFG):
        sys.exit("ERRO: config_publicacao.json nao esta nesta pasta.")

    cfg = json.load(open(CFG, encoding="utf-8"))
    page_id = str((cfg.get("facebook") or {}).get("page_id") or "")
    if not page_id or page_id.startswith("COLE_AQUI"):
        sys.exit("ERRO: falta facebook.page_id no arquivo.")

    # qualquer token utilizavel que ja esteja no arquivo serve de partida
    partida = ""
    for cand in (cfg.get("access_token"),
                 (cfg.get("facebook") or {}).get("page_token")):
        cand = str(cand or "")
        if cand and not cand.startswith("COLE_AQUI"):
            partida = cand
            break
    if not partida:
        sys.exit("ERRO: nao ha nenhum token no arquivo para partir. Gere um no "
                 "Explorador da Graph API e cole em access_token.")

    tipo, _, exp = descrever(partida)
    print(f"\ntoken atual no arquivo: tipo {tipo or '?'}, "
          f"{'NAO EXPIRA' if exp == 0 else 'com data de expiracao'}")

    if tipo == "PAGE" and exp == 0:
        print("\nJa esta correto. Confirmando que esta nos dois campos...")
        novo = partida
    else:
        print("\nBuscando o token da Pagina...")
        d, err = get("me/accounts", {"fields": "id,name,access_token",
                                     "access_token": partida, "limit": "100"})
        if err:
            sys.exit(f"ERRO ao consultar a Meta: {err}\n"
                     "Se disser que o token expirou, gere um novo no Explorador "
                     "da Graph API, cole em access_token e rode este script de novo.")
        novo = None
        nome = None
        for pag in d.get("data", []):
            if str(pag.get("id")) == page_id:
                novo = pag.get("access_token")
                nome = pag.get("name")
                break
        if not novo:
            sys.exit(f"ERRO: a Pagina {page_id} nao apareceu na sua lista. "
                     "Confira o page_id, ou gere um token com pages_show_list.")
        print(f"  Pagina encontrada: {nome}")

    tipo2, _, exp2 = descrever(novo)
    print(f"  tipo: {tipo2}")
    print(f"  validade: {'NAO EXPIRA' if exp2 == 0 else 'AINDA TEM DATA DE EXPIRACAO'}")

    if tipo2 != "PAGE":
        sys.exit("\nERRO: o token obtido nao e de Pagina. Nada foi gravado.")
    if exp2 != 0:
        print("\nAVISO: este token ainda tem data de expiracao. Isso acontece "
              "quando o token de partida era de CURTA duracao.")
        print("Estenda o token de usuario no Depurador de Token de Acesso "
              "(botao 'Estender token de acesso'), cole o resultado em "
              "access_token e rode este script de novo.")
        resp = input("Gravar assim mesmo? (s/N) ").strip().lower()
        if resp != "s":
            sys.exit("Nada foi gravado.")

    backup = CFG + ".backup"
    shutil.copy2(CFG, backup)

    cfg["access_token"] = novo
    cfg.setdefault("facebook", {})["page_token"] = novo
    with open(CFG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 64)
    print("GRAVADO nos dois campos: access_token e facebook.page_token")
    print(f"copia de seguranca do arquivo anterior: {os.path.basename(backup)}")
    if exp2 == 0:
        print("\nEste token NAO VENCE. Voce nao precisa mais renovar nada.")
        print("Ele so para de funcionar se voce trocar a senha do Facebook,")
        print("remover o app das suas configuracoes, ou a Meta invalidar a sessao.")
    print("\nConfira quando quiser com:  py checar_token.py")
    print("=" * 64)


if __name__ == "__main__":
    main()
