#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a versão 9:16 (story / criativo de anúncio) do gancho de cada peça.

uso: python3 story_ad.py spec1.json spec2.json ...
Lê o mesmo JSON de spec do machine.py e usa o slide 1 (gancho).
"""
import os, sys, json
import machine as M
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "kit_anuncios")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

ZAP = ('<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
       '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.13h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.36c0-4.54 3.7-8.23 8.25-8.23 2.2 0 4.27.86 5.83 2.41a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.21-8.24 8.21Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.22.24-.85.83-.85 2.03s.87 2.35.99 2.51c.12.16 1.71 2.61 4.14 3.66.58.25 1.03.4 1.38.51.58.19 1.11.16 1.53.1.47-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.11-.22-.17-.47-.29Z"/>'
       '</svg>')


def build(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    fundo, accent, texto, pnome = M.PALETAS[spec["paleta"]]
    frgb = M.hexrgb(fundo)
    dark = sum(frgb) / 3 < 128
    lo = M.mix(frgb, (0, 0, 0), .55 if dark else .38)
    hi = M.mix(frgb, (255, 255, 255), .30 if dark else .22)
    ar, ag, ab = M.hexrgb(accent)
    cta_fg = "#12100a" if (ar * .299 + ag * .587 + ab * .114) > 150 else "#FFFFFF"

    M.W, M.H = W, H
    tmp = os.path.join(OUT, "_f.png")
    M.surface(spec["cenas"][0], spec["seeds"][0] + 7, lo, hi).save(tmp, optimize=True)
    bg = M.b64file(tmp)

    s1 = spec["slides"][0]
    css = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
{M.FACES}
body{{width:{W}px;height:{H}px;overflow:hidden;-webkit-font-smoothing:antialiased}}
.s{{position:relative;width:{W}px;height:{H}px;background-color:{fundo};color:{texto};
 font-family:'Plus Jakarta Sans',sans-serif;display:flex;flex-direction:column;
 padding:250px 90px 330px;
 background-image:linear-gradient({M.rgba(fundo,.12)} 0%,{M.rgba(fundo,.42)} 46%,{M.rgba(fundo,.80)} 100%),
   url('data:image/png;base64,{bg}');background-size:cover;background-position:center}}
.accentbar{{position:absolute;top:0;left:0;right:0;height:12px;background:{accent}}}
.brand{{position:absolute;top:190px;left:90px;font-size:26px;letter-spacing:.24em;
 font-weight:600;color:{accent};text-transform:uppercase}}
h1{{font-family:'Playfair Display',serif;font-weight:900;text-transform:uppercase;
 font-size:100px;line-height:1.04;letter-spacing:-.015em;margin-top:auto}}
h1 b{{color:{accent}}}
.apoio{{font-size:38px;line-height:1.45;margin-top:44px;font-weight:400;
 color:{M.rgba(texto,.78)};max-width:860px}}
.cred{{margin-top:auto;font-size:26px;line-height:1.5;color:{M.rgba(texto,.60)};font-weight:400}}
.faixa{{margin-top:44px;width:82%;background:{accent};border-radius:16px;padding:34px 36px;
 display:flex;align-items:center;justify-content:center;gap:22px}}
.faixa svg{{width:60px;height:60px;fill:{cta_fg}}}
.faixa span{{font-size:60px;font-weight:800;color:{cta_fg};white-space:nowrap}}
.reserva{{position:absolute;left:90px;right:90px;bottom:110px;height:140px;
 border:2px dashed {M.rgba(accent,.42)};border-radius:18px;display:flex;
 align-items:center;justify-content:center;font-size:25px;color:{M.rgba(texto,.42)};
 font-weight:500;letter-spacing:.04em}}
"""
    body = f"""<div class="s"><div class="accentbar"></div><div class="brand">@integrajud</div>
<h1>{s1['headline']}</h1>
<div class="apoio">{s1['apoio']}</div>
<div class="cred">Perícia, auditoria, cálculos judiciais e inteligência de dados · atendimento nacional</div>
<div class="faixa">{ZAP}<span>11 97723-7113</span></div>
<div class="reserva">reservado: sticker de link (story) ou botão do anúncio</div></div>"""

    html = (f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
            f"<style>{css}</style></head><body>{body}</body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.set_content(html, wait_until="load")
        pg.wait_for_timeout(350)
        out = os.path.join(OUT, f"{spec['slug']}_916.png")
        pg.screenshot(path=out)
        o = pg.evaluate("()=>{const e=document.querySelector('.s');return {a:e.scrollHeight,b:e.clientHeight}}")
        if o["a"] > o["b"] + 1:
            print(f"  !! {spec['slug']} TRANSBORDO {o['a']}/{o['b']}")
        b.close()
    os.remove(tmp)
    print(f"{spec['slug']}_916.png [{spec['paleta']} {pnome}]")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        build(a)
