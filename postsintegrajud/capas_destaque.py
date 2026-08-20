#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAPAS DE DESTAQUE do Instagram — uma por area.

    py capas_destaque.py

POR QUE ISTO EXISTE — 19/08/2026.
Todo story publicado some em 24h. Salvo num destaque, ele vira menu permanente
no perfil: o advogado abre e ve "Trabalhistas", "Bancarios", "Liquidacao".
O material ja e produzido todo dia e estava sendo jogado fora.

A Graph API NAO cria destaque — nao existe endpoint. A parte automatizavel e a
arte, e e o que este script faz. O resto e no aplicativo, uma vez por area:
  story da area > Destacar > criar o destaque com o nome da area >
  Editar destaque > Editar capa > escolher o arquivo.
Da segunda vez em diante e so somar o story do dia ao destaque que ja existe.

Saida: capas-destaque/<slug>.png, 1080x1920. O app recorta um circulo do centro.
Marca e paleta saem do nome da pasta. Nao publica nada.
"""
import os
import sys
import machine as M
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "capas-destaque")

AREAS = {
    "integrajud": ("P01", "@integrajud", [
        ("civeis", "CÍVEIS"), ("contabeis", "CONTÁBEIS"),
        ("financeiros", "FINANCEIROS"), ("bancarios", "BANCÁRIOS"),
        ("trabalhistas", "TRABALHISTAS"), ("previdenciarios", "PREVIDÊNCIA"),
        ("tributarios", "TRIBUTÁRIOS"), ("empresariais", "EMPRESARIAIS"),
        ("marketplace", "MARKETPLACE"), ("auditoria", "AUDITORIA"),
        ("seguros", "SEGUROS"), ("imobiliarios", "IMOBILIÁRIOS"),
        ("agrarios", "AGRÁRIOS"), ("sob-medida", "SOB MEDIDA")]),
    "gkfd": ("G04", "@gkfdfisco", [
        ("contabilidade", "CONTABILIDADE"), ("fiscal", "FISCAL"),
        ("repasses", "REPASSES"), ("estoque", "ESTOQUE"),
        ("tarifas-ads", "TARIFAS E ADS"), ("devolucoes", "DEVOLUÇÕES"),
        ("rentabilidade", "RENTABILIDADE"), ("abertura", "ABERTURA"),
        ("retencoes", "RETENÇÕES")]),
}


def main():
    marca = sys.argv[1] if len(sys.argv) > 1 else None
    if not marca:
        nome = os.path.basename(BASE).lower()
        marca = "gkfd" if "gkfd" in nome else "integrajud"
    if marca not in AREAS:
        sys.exit("Marca desconhecida: %s (use integrajud ou gkfd)" % marca)

    paleta, arroba, itens = AREAS[marca]
    fundo, accent, texto, pnome = M.PALETAS[paleta]
    os.makedirs(OUT, exist_ok=True)
    print("=" * 58)
    print("CAPAS DE DESTAQUE — %s [%s %s]" % (marca, paleta, pnome))
    print("=" * 58)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920},
                        device_scale_factor=1)
        for slug, rotulo in itens:
            html = f"""<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>
*{{margin:0;padding:0;box-sizing:border-box}}{M.FACES}
body{{width:1080px;height:1920px;background:{fundo};overflow:hidden}}
.c{{width:1080px;height:1920px;display:flex;flex-direction:column;
 align-items:center;justify-content:center;gap:30px;
 background:radial-gradient(circle at 50% 50%,{M.rgba(accent,.13)} 0%,{M.rgba(fundo,0)} 58%)}}
.r{{width:210px;height:6px;background:{accent};border-radius:3px}}
h1{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:74px;
 line-height:1.04;letter-spacing:.01em;color:{texto};text-transform:uppercase;
 text-align:center;max-width:840px}}
.m{{font-family:'Plus Jakarta Sans',sans-serif;font-size:30px;letter-spacing:.3em;
 font-weight:700;color:{M.rgba(accent,.9)};text-transform:uppercase}}
</style></head><body><div class="c">
<div class="r"></div><h1>{rotulo}</h1><div class="m">{arroba}</div></div></body></html>"""
            pg.set_content(html, wait_until="load")
            pg.wait_for_timeout(180)
            pg.screenshot(path=os.path.join(OUT, "%s.png" % slug))
            print("  %-16s %s" % (slug, rotulo))
        b.close()

    print("-" * 58)
    print("%d capas em %s" % (len(itens), OUT))
    print("No aplicativo: story da area > Destacar > nomear >")
    print("Editar destaque > Editar capa > escolher o arquivo.")
    print("=" * 58)


if __name__ == "__main__":
    main()
