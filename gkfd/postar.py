#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UM COMANDO SO. Publica a peca nos dois destinos.

    py postar.py 2026-08-16_habilitacao-credito

Ou, sem argumento, usa a subpasta de peca MAIS RECENTE da pasta:

    py postar.py

O que ele faz:
  1. Facebook  -> publicar_facebook.py   (nao precisa de hospedagem)
  2. Instagram -> publicar_instagram.py  (so roda se o bloco host estiver
                  preenchido; senao avisa e segue, sem quebrar)

Um destino falhando NAO impede o outro. No fim ele diz o placar.
"""

import json
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable or "python"


def achar_peca(arg):
    if arg:
        p = arg if os.path.isabs(arg) else os.path.join(BASE, arg)
        if not os.path.isdir(p):
            sys.exit(f"ERRO: pasta nao encontrada: {p}")
        return p
    padrao = re.compile(r"^\d{4}-\d{2}-\d{2}_")
    cands = [d for d in os.listdir(BASE)
             if padrao.match(d) and os.path.isdir(os.path.join(BASE, d))]
    if not cands:
        sys.exit("ERRO: nenhuma subpasta AAAA-MM-DD_tema encontrada.")
    cands.sort(key=lambda d: os.path.getmtime(os.path.join(BASE, d)))
    return os.path.join(BASE, cands[-1])


def instagram_configurado():
    cfg = os.path.join(BASE, "config_publicacao.json")
    if not os.path.exists(cfg):
        return False, "config_publicacao.json nao existe"
    try:
        d = json.load(open(cfg, encoding="utf-8"))
    except Exception as e:
        return False, f"config_publicacao.json invalido: {e}"
    for chave in ("ig_user_id", "access_token"):
        v = str(d.get(chave) or "")
        if not v or v.startswith("COLE_AQUI"):
            return False, f"falta {chave}"
    h = d.get("host", {})
    if h.get("tipo") == "facebook":
        fb = d.get("facebook", {})
        v = str(fb.get("page_id") or "")
        if not v or v.startswith("COLE_AQUI"):
            return False, "host tipo facebook exige facebook.page_id"
        return True, ""
    if h.get("tipo") == "ftp":
        for chave in ("usuario", "senha"):
            v = str(h.get(chave) or "")
            if not v or v.startswith("COLE_AQUI"):
                return False, "bloco host (FTP) ainda nao preenchido"
    return True, ""


def rodar(script, pasta):
    caminho = os.path.join(BASE, script)
    if not os.path.exists(caminho):
        print(f"  {script} nao existe nesta pasta.")
        return False
    r = subprocess.run([PY, caminho, pasta])
    return r.returncode == 0


def main():
    pasta = achar_peca(sys.argv[1] if len(sys.argv) > 1 else None)
    nome = os.path.basename(pasta)
    print("=" * 62)
    print(f"PECA: {nome}")
    print("=" * 62)

    print("\n--- FACEBOOK ---")
    ok_fb = rodar("publicar_facebook.py", pasta)

    print("\n--- INSTAGRAM ---")
    pronto, motivo = instagram_configurado()
    if not pronto:
        print(f"  pulado: {motivo}")
        print("  (o Instagram por API precisa das imagens hospedadas numa URL")
        print("   publica; enquanto isso, ele sai pelo navegador)")
        ok_ig = None
    else:
        ok_ig = rodar("publicar_instagram.py", pasta)

    print("\n" + "=" * 62)
    print("PLACAR")
    print(f"  Facebook : {'PUBLICADO' if ok_fb else 'FALHOU'}")
    if ok_ig is None:
        print("  Instagram: nao configurado (pendente)")
    else:
        print(f"  Instagram: {'PUBLICADO' if ok_ig else 'FALHOU'}")
    print("=" * 62)


if __name__ == "__main__":
    main()
