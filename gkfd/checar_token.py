#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diz QUEM e o token que esta no config_publicacao.json, sem mostrar o token.

    python checar_token.py
"""
import json, os, sys, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
API = "https://graph.facebook.com/v21.0"


def get(caminho, params):
    url = f"{API}/{caminho}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode()), None
    except urllib.error.HTTPError as e:
        try:
            corpo = json.loads(e.read().decode())
            err = corpo.get("error", {})
            return None, f"{err.get('type')} {err.get('code')}: {err.get('message')}"
        except Exception:
            return None, str(e)
    except Exception as e:
        return None, str(e)


def examinar(rotulo, token):
    if not token or "COLE_AQUI" in token:
        print(f"{rotulo}: vazio ou ainda com placeholder")
        return
    print(f"\n{rotulo}  ({len(token)} caracteres)")

    d, err = get("me", {"fields": "id,name", "access_token": token})
    if err:
        print(f"  /me falhou -> {err}")
        return
    print(f"  este token fala como: {d.get('name')}  (id {d.get('id')})")

    d2, err2 = get("debug_token", {"input_token": token, "access_token": token})
    if not err2:
        info = d2.get("data", {})
        tipo = info.get("type", "?")
        exp = info.get("expires_at", 0)
        scopes = info.get("scopes", [])
        print(f"  tipo: {tipo}")
        print(f"  validade: {'NAO EXPIRA' if exp == 0 else 'expira (timestamp ' + str(exp) + ')'}")
        falta = [p for p in ("pages_manage_posts", "pages_show_list",
                             "instagram_basic", "instagram_content_publish")
                 if p not in scopes]
        print(f"  permissoes presentes: {len(scopes)}")
        if falta:
            print(f"  FALTANDO: {', '.join(falta)}")
        else:
            print("  todas as permissoes necessarias estao presentes")


def main():
    cfg = os.path.join(BASE, "config_publicacao.json")
    if not os.path.exists(cfg):
        sys.exit("config_publicacao.json nao encontrado nesta pasta.")
    d = json.load(open(cfg, encoding="utf-8"))

    print("=" * 60)
    print("O QUE ESTE SCRIPT FAZ: pergunta a Meta quem e cada token.")
    print("Ele NAO imprime o token em lugar nenhum.")
    print("=" * 60)

    examinar("page_token (bloco facebook)", d.get("facebook", {}).get("page_token", ""))
    examinar("access_token (Instagram)", d.get("access_token", ""))

    print("\n" + "-" * 60)
    print("O QUE VOCE QUER VER nos DOIS campos:")
    print("  fala como: IntegraJud")
    print("  tipo: PAGE")
    print("  validade: NAO EXPIRA")
    print()
    print("Token de PAGINA nascido de um token de usuario de longa duracao nao")
    print("tem data de expiracao. Com ele nos dois campos, a maquina nao precisa")
    print("de renovacao. Ele so morre se voce trocar a senha do Facebook, remover")
    print("o app, ou a Meta invalidar a sessao.")
    print()
    print("Se disser 'fala como: Fabio ...' e 'tipo: USER', esse vence em 60 dias:")
    print("  Explorador > selecione a Pagina em 'Usuario ou Pagina' > copie o")
    print("  token que aparecer > cole em access_token E em page_token.")
    print("-" * 60)


if __name__ == "__main__":
    main()
