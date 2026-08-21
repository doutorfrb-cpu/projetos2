#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAPA DE ARTIGO DO LINKEDIN — 1920x1080, deitada.

    py capa_artigo.py "O titulo do artigo" [paleta]

POR QUE ISTO EXISTE — 21/08/2026.
A capa do artigo do LinkedIn e DEITADA e aparece recortada numa faixa larga.
Slide de carrossel e em pe, 1080x1350: usado como capa, ele e cortado no meio
e perde a manchete. Nao e defeito do LinkedIn, sao formatos diferentes.

Aqui sai 1920x1080 na identidade da marca, com a faixa de marca em cima e o
titulo grande, ja pensado para a faixa estreita que o feed mostra.
"""
import os, sys
import machine as M
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "linkedin")
W, H = 1920, 1080

_n = os.path.basename(BASE).lower()
if "gkfd" in _n:
    ARROBA, DESC, PAL = "@gkfdfisco", "CONTABILIDADE PARA MARKETPLACE E E‑COMMERCE", "G04"
else:
    ARROBA, DESC, PAL = "@integrajud", "INTELIGÊNCIA PERICIAL PARA ADVOCACIA", "P01"


def build(titulo, paleta=None, slug="capa-artigo"):
    fundo, accent, texto, pnome = M.PALETAS[paleta or PAL]
    os.makedirs(OUT, exist_ok=True)
    M.W, M.H = W, H
    tmp = os.path.join(OUT, "_capa_tmp.png")
    frgb = M.hexrgb(fundo)
    dark = sum(frgb) / 3 < 128
    lo = M.mix(frgb, (0, 0, 0), .58 if dark else .40)
    hi = M.mix(frgb, (255, 255, 255), .26 if dark else .20)
    M.surface("granito", 4711, lo, hi).save(tmp, optimize=True)
    bg = M.b64file(tmp)

    html = f"""<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>
*{{margin:0;padding:0;box-sizing:border-box}}{M.FACES}
body{{width:{W}px;height:{H}px;overflow:hidden}}
.s{{position:relative;width:{W}px;height:{H}px;background-color:{fundo};color:{texto};
 font-family:'Plus Jakarta Sans',sans-serif;display:flex;flex-direction:column;
 justify-content:center;padding:0 120px;
 background-image:linear-gradient(100deg,{M.rgba(fundo,.94)} 0%,{M.rgba(fundo,.80)} 55%,{M.rgba(fundo,.62)} 100%),
   url('data:image/png;base64,{bg}');background-size:cover;background-position:center}}
.band{{position:absolute;top:0;left:0;right:0;height:150px;background:{fundo};
 border-bottom:3px solid {accent};display:flex;flex-direction:column;justify-content:center;padding-left:120px}}
.band .a{{font-size:20px;letter-spacing:.28em;font-weight:600;color:{accent};text-transform:uppercase}}
.band .d{{font-size:30px;letter-spacing:.02em;font-weight:800;color:{M.rgba(texto,.95)};
 text-transform:uppercase;margin-top:10px}}
h1{{font-family:'Playfair Display',serif;font-weight:900;font-size:104px;line-height:1.06;
 letter-spacing:-.02em;max-width:1420px;margin-top:60px}}
h1 b{{color:{accent}}}
.rule{{width:180px;height:8px;background:{accent};border-radius:4px;margin-bottom:38px}}
.pe{{position:absolute;bottom:66px;left:120px;font-size:24px;letter-spacing:.16em;
 font-weight:700;color:{M.rgba(texto,.60)};text-transform:uppercase}}
</style></head><body><div class="s">
<div class="band"><div class="a">{ARROBA}</div><div class="d">{DESC}</div></div>
<div class="rule"></div><h1>{titulo}</h1>
<div class="pe">Fábio Rebouças · artigo</div></div></body></html>"""

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.set_content(html, wait_until="load")
        pg.wait_for_timeout(300)
        # o titulo encolhe ate caber, igual as pecas
        for _ in range(9):
            o = pg.evaluate("()=>{const s=document.querySelector('.s');"
                            "return s.scrollHeight - s.clientHeight}")
            if o <= 0:
                break
            pg.evaluate("()=>{const h=document.querySelector('h1');"
                        "h.style.fontSize=(parseFloat(getComputedStyle(h).fontSize)*0.93)+'px'}")
            pg.wait_for_timeout(80)
        out = os.path.join(OUT, "%s.png" % slug)
        pg.screenshot(path=out)
        b.close()
    os.remove(tmp)
    print("%s  (%dx%d)" % (out, W, H))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('uso: py capa_artigo.py "Titulo do artigo" [paleta] [slug]')
    build(sys.argv[1],
          sys.argv[2] if len(sys.argv) > 2 else None,
          sys.argv[3] if len(sys.argv) > 3 else "capa-artigo")
