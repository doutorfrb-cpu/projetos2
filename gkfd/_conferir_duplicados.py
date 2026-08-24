#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lista os posts recentes da Pagina e as midias recentes do Instagram.

Nao imprime token nenhum: le o config sozinho e mostra so id, hora e o comeco
da legenda. Serve para achar as republicacoes acidentais de 23/08/2026.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(BASE, "config_publicacao.json"), encoding="utf-8"))
TOK = cfg["facebook"]["page_token"]
PAGE = cfg["facebook"]["page_id"]
IGU = cfg["ig_user_id"]


def get(path, params):
    params = dict(params)
    params["access_token"] = TOK
    url = f"https://graph.facebook.com/v21.0/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")
        # nunca imprime a URL, que carrega o token
        print(f"[erro] {path}: HTTP {e.code} -> {corpo[:400]}")
        return {}


print("=" * 70)
print("POSTS DA PAGINA (mais recentes primeiro)")
print("=" * 70)
for edge in ("published_posts", "posts", "feed"):
    d = get(f"{PAGE}/{edge}", {"fields": "id,created_time,message", "limit": 25})
    if d.get("data"):
        print(f"-- edge: {edge}")
        for p in d["data"]:
            msg = (p.get("message") or "").replace("\n", " ")[:70]
            print(f"{p['created_time']}  {p['id']}\n    {msg}")
        break

print()
print("=" * 70)
print("MIDIAS DO INSTAGRAM (mais recentes primeiro)")
print("=" * 70)
d = get(f"{IGU}/media", {"fields": "id,timestamp,media_type,caption", "limit": 25})
for m in d.get("data", []):
    cap = (m.get("caption") or "").replace("\n", " ")[:70]
    print(f"{m['timestamp']}  {m['id']}  {m.get('media_type')}\n    {cap}")
