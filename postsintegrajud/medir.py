#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MEDIR — fecha o laco que faltava na Content Machine.

    py medir.py
    py medir.py --posts 50

POR QUE ISTO EXISTE — 17/08/2026.
A maquina registra tudo que ela FEZ: area, peca processual, layout, paleta,
frase de efeito, fundo. Nao registra nada sobre o que FUNCIONOU. Ela gira o
rodizio por variedade, no escuro, e vai continuar girando no escuro para
sempre se ninguem trouxer o numero de volta.

Este script traz. Ele pergunta a Meta quantas visualizacoes e quanto alcance
cada post teve, cruza com a linha correspondente do pautas-publicadas.md pelo
ID gravado no log, e responde a pergunta que interessa:

    qual PALETA, qual LAYOUT, qual AREA e qual FRASE DE EFEITO
    estao puxando resultado, e quais estao afundando.

Ele NAO publica nada, NAO altera nenhuma peca e NAO imprime o token.
Rodar este script nao tem como quebrar a maquina.

SAIDA: um resumo no console e o arquivo desempenho.md na raiz da pasta.

PERMISSAO: ler insights exige `instagram_manage_insights` no token. Se o seu
token nao tiver, o script avisa em portugues claro e o que fazer.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(BASE, "config_publicacao.json")
LOG = os.path.join(BASE, "pautas-publicadas.md")
SAIDA = os.path.join(BASE, "desempenho.md")
API = "https://graph.facebook.com/v21.0/"


# ----------------------------------------------------------------- rede

def pega(caminho, params):
    url = API + caminho + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        try:
            corpo = json.loads(e.read().decode("utf-8"))
            err = corpo.get("error", {})
            return None, "%s %s: %s" % (err.get("type", "Erro"),
                                        err.get("code", "?"),
                                        err.get("message", ""))
        except Exception:
            return None, "HTTP %s" % e.code
    except Exception as e:
        return None, str(e)


# ----------------------------------------------------------------- config

def carregar():
    if not os.path.exists(CFG):
        print("Nao achei o config_publicacao.json nesta pasta.")
        sys.exit(1)
    cfg = json.load(open(CFG, encoding="utf-8"))
    fb = cfg.get("facebook") or {}
    tok = str(fb.get("page_token") or "") or str(cfg.get("access_token") or "")
    if not tok or tok.startswith("COLE_AQUI"):
        print("Token ausente no config_publicacao.json.")
        sys.exit(1)
    ig = str(cfg.get("ig_user_id") or "")
    if not ig:
        print("ig_user_id ausente no config_publicacao.json.")
        sys.exit(1)
    return tok, ig


# ----------------------------------------------------------------- log

def ler_log():
    """Devolve {id_do_instagram: {campos da peca}} lido do pautas-publicadas.md."""
    mapa = {}
    if not os.path.exists(LOG):
        return mapa
    for linha in open(LOG, encoding="utf-8", errors="replace"):
        if " IG " not in linha:
            continue
        partes = [p.strip() for p in linha.strip().lstrip("- ").split("|")]
        if len(partes) < 8:
            continue
        ig_id = ""
        for p in partes[-1].split("·"):
            p = p.strip()
            if p.upper().startswith("IG "):
                ig_id = p[3:].strip()
        if not ig_id:
            continue

        paleta = layout = ""
        for p in partes:
            u = p.upper()
            if not paleta and len(u) > 3 and u[0] == "P" and u[1:3].isdigit():
                paleta = p
            if not layout:
                if u.startswith("L") and len(u) > 1 and u[1].isdigit():
                    layout = u.split()[0]
                elif "(L" in u:
                    layout = "L" + u.split("(L", 1)[1][0]
                elif u.startswith("ARRANJO"):
                    layout = p

        mapa[ig_id] = {
            "data": partes[0],
            "hora": partes[1] if len(partes) > 1 else "",
            "eixo": partes[2] if len(partes) > 2 else "",
            "area": partes[3] if len(partes) > 3 else "",
            "momento": partes[4] if len(partes) > 4 else "",
            "peca": partes[5] if len(partes) > 5 else "",
            "frase": partes[6] if len(partes) > 6 else "",
            "paleta": paleta or "(sem paleta no log)",
            "layout": layout or "(sem layout no log)",
        }
    return mapa


# ----------------------------------------------------------------- insights

CONJUNTOS = [
    "views,reach,total_interactions,saved",
    "impressions,reach,engagement,saved",
    "reach,saved",
    "reach",
]


def insights(media_id, token, conjunto_ok):
    ordem = ([conjunto_ok] + CONJUNTOS) if conjunto_ok else CONJUNTOS
    for metricas in ordem:
        d, erro = pega("%s/insights" % media_id,
                       {"metric": metricas, "access_token": token})
        if d is not None:
            saida = {}
            for item in d.get("data", []):
                vals = item.get("values") or [{}]
                saida[item.get("name")] = vals[0].get("value", 0)
            return saida, metricas, None
        ultimo = erro
    return {}, conjunto_ok, ultimo


# ----------------------------------------------------------------- agregacao

def agrupar(itens, campo):
    grupos = defaultdict(list)
    for it in itens:
        chave = (it["peca"] or {}).get(campo)
        if chave:
            grupos[chave].append(it["views"])
    linhas = []
    for chave, vals in grupos.items():
        linhas.append((chave, len(vals), sum(vals) / float(len(vals)), max(vals)))
    linhas.sort(key=lambda x: x[2], reverse=True)
    return linhas


def tabela(titulo, linhas, rotulo):
    out = ["", "### %s" % titulo, "",
           "| %s | pecas | media de views | melhor |" % rotulo,
           "|---|---:|---:|---:|"]
    for chave, n, media, melhor in linhas:
        out.append("| %s | %d | %.1f | %d |" % (chave, n, media, melhor))
    return out


# ----------------------------------------------------------------- principal

def main():
    limite = 50
    if "--posts" in sys.argv:
        try:
            limite = int(sys.argv[sys.argv.index("--posts") + 1])
        except Exception:
            pass

    token, ig_user = carregar()
    print("=" * 62)
    print("MEDIDOR DE DESEMPENHO — so leitura, nao publica nada")
    print("=" * 62)

    log = ler_log()
    print("Log: %d pecas com ID do Instagram gravado." % len(log))

    d, erro = pega("%s/media" % ig_user,
                   {"fields": "id,timestamp,permalink,media_type,caption",
                    "limit": str(limite), "access_token": token})
    if d is None:
        print("ERRO ao listar as publicacoes: %s" % erro)
        if "insights" in (erro or "").lower() or "permission" in (erro or "").lower():
            print("\nFalta permissao no token. No Explorador da Graph API,")
            print("marque instagram_manage_insights junto das outras e gere")
            print("de novo o token da Pagina.")
        sys.exit(1)

    posts = d.get("data", [])
    print("Instagram: %d publicacoes encontradas.\n" % len(posts))

    itens = []
    conjunto_ok = None
    falha_permissao = None

    for p in posts:
        mid = p.get("id")
        met, conjunto_ok, erro = insights(mid, token, conjunto_ok)
        if erro and not met:
            falha_permissao = erro
        views = met.get("views", met.get("impressions", 0)) or 0
        alcance = met.get("reach", 0) or 0
        inter = met.get("total_interactions", met.get("engagement", 0)) or 0
        legenda = (p.get("caption") or "").strip().replace("\n", " ")
        itens.append({
            "id": mid,
            "data": (p.get("timestamp") or "")[:10],
            "link": p.get("permalink", ""),
            "views": views,
            "alcance": alcance,
            "inter": inter,
            "titulo": legenda[:70],
            "peca": log.get(mid),
        })

    if falha_permissao and all(i["views"] == 0 and i["alcance"] == 0 for i in itens):
        print("Nao consegui ler nenhuma metrica. A Meta respondeu:")
        print("  %s" % falha_permissao)
        print("\nQuase sempre e falta da permissao instagram_manage_insights.")
        print("No Explorador da Graph API, marque ela junto das outras seis,")
        print("gere o token da Pagina de novo e cole nos dois campos.")
        sys.exit(1)

    itens.sort(key=lambda x: x["views"], reverse=True)
    casados = [i for i in itens if i["peca"]]

    print("-" * 62)
    print("AS DEZ MAIS VISTAS")
    print("-" * 62)
    for i in itens[:10]:
        marca = ""
        if i["peca"]:
            marca = "  [%s / %s / %s]" % (i["peca"]["paleta"],
                                          i["peca"]["layout"],
                                          i["peca"]["area"])
        print("%6d views | %5d alcance | %s | %s%s"
              % (i["views"], i["alcance"], i["data"], i["titulo"][:40], marca))

    total = sum(i["views"] for i in itens) or 0
    media = total / float(len(itens)) if itens else 0
    print("-" * 62)
    print("Total %d views em %d posts. Media %.1f." % (total, len(itens), media))
    print("Cruzados com o log: %d de %d." % (len(casados), len(itens)))

    md = ["# Desempenho do @integrajud", "",
          "Gerado pelo medir.py. So leitura — nenhuma peca foi alterada.", "",
          "- Publicacoes lidas: **%d**" % len(itens),
          "- Cruzadas com o pautas-publicadas.md: **%d**" % len(casados),
          "- Total de visualizacoes: **%d**" % total,
          "- Media por peca: **%.1f**" % media,
          "",
          "> Atencao ao ler: post turbinado tem alcance pago e nao pode ser",
          "> comparado com post organico. Confira no Gerenciador antes de",
          "> concluir que uma paleta ou um layout 'funciona'.",
          "",
          "## Ranking", "",
          "| views | alcance | interacoes | data | area | peca processual | paleta | layout | frase |",
          "|---:|---:|---:|---|---|---|---|---|---|"]
    for i in itens:
        pc = i["peca"] or {}
        md.append("| %d | %d | %d | %s | %s | %s | %s | %s | %s |"
                  % (i["views"], i["alcance"], i["inter"], i["data"],
                     pc.get("area", ""), pc.get("peca", ""),
                     pc.get("paleta", ""), pc.get("layout", ""),
                     pc.get("frase", "")))

    if casados:
        md += ["", "## O que puxa resultado", "",
               "Media de visualizacoes por atributo, so das pecas que o log",
               "conseguiu cruzar. Com poucas pecas por grupo isto e indicio,",
               "nao prova — leia como direcao, nao como veredito."]
        md += tabela("Por paleta", agrupar(casados, "paleta"), "paleta")
        md += tabela("Por layout", agrupar(casados, "layout"), "layout")
        md += tabela("Por area", agrupar(casados, "area"), "area")
        md += tabela("Por peca processual", agrupar(casados, "peca"), "peca")
        md += tabela("Por frase de efeito", agrupar(casados, "frase"), "frase")
        md += tabela("Por horario", agrupar(casados, "hora"), "horario")

    open(SAIDA, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\nGravado: desempenho.md")
    print("=" * 62)


if __name__ == "__main__":
    main()
