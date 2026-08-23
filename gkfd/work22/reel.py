#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera um REEL 1080x1920 a partir do MESMO spec.json do carrossel.

    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 reel.py spec_v9.json

POR QUE ASSIM, e não com vídeo gerado por IA:
o conteúdo desta operação tem uma vantagem rara — ele tem NÚMERO QUE SE MOVE.
Dois critérios chegando a valores diferentes, uma margem sendo estourada pela
soma. Animar isso é mostrar a competência acontecendo, e é impossível de
falsificar. Vídeo de IA com escritório e advogado tem o mesmo problema do banco
de imagem que a operação já descartou: comunica genérico, e com esse público
sugere que quem fez não tinha o que mostrar.

COMO FUNCIONA
o mesmo sistema visual do carrossel (paleta, tipografia, fundo de documento),
em 9:16, com as linhas entrando por animação de CSS. O Playwright grava a
página em vídeo e o ffmpeg converte para mp4. Sem modelo de vídeo, sem
alucinação: é o design da casa se movendo.

SEM SOM por opção. A maioria assiste no mudo, e voz sintética num conteúdo de
perícia contábil derruba a autoridade que a peça constrói. Querendo narração,
grave a própria voz e monte por cima.
"""

import json
import os
import subprocess
import sys

from machine import (PALETAS, b64file, css, fotocrop, hexrgb, mix, rgba,
                     surface)

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
FPS = 30


def fundo_do_spec(spec, idx, out):
    """Reaproveita a cena do slide idx do carrossel, em 9:16."""
    kinds = spec.get("cenas", ["linho"])
    seeds = spec.get("seeds", [11])
    k = str(kinds[min(idx, len(kinds) - 1)])
    sd = seeds[min(idx, len(seeds) - 1)]
    p = os.path.join(out, f"_reelbg{idx}.png")
    fundo, accent, texto, _ = PALETAS[spec["paleta"]]
    frgb = hexrgb(fundo)
    dark = sum(frgb) / 3 < 128
    lo = mix(frgb, (0, 0, 0), .55 if dark else .38)
    hi = mix(frgb, (255, 255, 255), .30 if dark else .22)
    if k.startswith("doc:"):
        import fundo_numerico as fnum
        fam, _, pap = k[4:].partition("/")
        im, _, _ = fnum.gerar(fam or "auto", spec["paleta"], sd, pap or "auto")
        im = im.resize((W, H))
        im.save(p)
    elif k.startswith("foto:"):
        im = fotocrop(k[5:])
        im.resize((W, H)).save(p)
    else:
        surface(k, sd, lo, hi).resize((W, H)).save(p)
    return b64file(p)


def achar_demonstracao(slides):
    """O slide de números é o coração do reel. Sem ele, usa o primeiro de valor."""
    for s in slides[1:-1]:
        alvo = (str(s.get("kicker", "")) + str(s.get("titulo", ""))).lower()
        if "demonstra" in alvo or "conta" in alvo:
            return s
    return slides[1] if len(slides) > 2 else None


def limpar(t):
    import re
    return re.sub(r"<[^>]+>", "", str(t))


def montar_html(spec, out):
    # MARCA — 18/08/2026. Mesmo motivo do machine.py e do story_ad.py: o
    # gerador serve duas operacoes, e sem isto o reel da GKFD fechava com a
    # assinatura de perito contabil e o site da IntegraJud.
    _m = spec.get("marca") or {}
    MK_ARROBA = _m.get("arroba", "@integrajud").upper()
    MK_SUB = _m.get("cta", "Análise gratuita do seu caso em")
    MK_SITE = _m.get("site", "www.integrajud.com.br")
    MK_ZAP = _m.get("whatsapp", "11 97723-7113")
    # IDENTIDADE E DA EMPRESA — 21/08/2026, determinacao do Fabio.
    # NENHUM nome pessoal na arte. Quem assina e a marca.
    MK_ASSIN = _m.get("assinatura",
                      "IntegraJud<br>"
                      "Inteligência pericial para advocacia")
    # SELO DA MARCA — 18/08/2026. No reel ele fica FIXO sobre o palco, visivel
    # nas tres cenas: e credencial, e credencial some junto com a cena nao
    # cumpre a funcao. Fora do .cena de proposito, para nao entrar na animacao.
    MK_SELO = _m.get("selo", "")
    _selo_html = ""
    if MK_SELO:
        _sp = MK_SELO if os.path.isabs(MK_SELO) else os.path.join(BASE, MK_SELO)
        if os.path.exists(_sp):
            _selo_html = ('<img src="data:image/png;base64,%s" style="position:absolute;'
                          'top:120px;right:80px;width:%dpx;height:auto;z-index:20;'
                          'filter:drop-shadow(0 6px 18px rgba(0,0,0,.30))">'
                          % (b64file(_sp), int(_m.get('selo_largura', 190))))
        else:
            print("  !! selo nao encontrado: %s" % _sp)
    fundo, accent, texto, _ = PALETAS[spec["paleta"]]
    dark = sum(hexrgb(fundo)) / 3 < 128
    s = spec["slides"]
    capa = s[0]
    demo = achar_demonstracao(s)
    oferta = s[-1]

    bg0 = fundo_do_spec(spec, 0, out)
    bg1 = fundo_do_spec(spec, 1, out)

    passos = [limpar(x) for x in (demo.get("passos", []) if demo else [])]
    # a ultima linha e o desfecho: entra sozinha, em destaque
    fecho = passos[-1] if passos else ""
    corpo = passos[:-1] if len(passos) > 1 else passos

    # --- linha do tempo, em segundos
    t_gancho = 0.4
    t_tarja = 1.0
    t_head = 1.5
    t_sai1 = 5.2
    t_kick = 5.6
    passo_dur = 1.35
    t_p0 = 6.2
    t_fecho = t_p0 + passo_dur * len(corpo) + 0.5
    t_sai2 = t_fecho + 3.4
    t_cta = t_sai2 + 0.3
    TOTAL = t_cta + 4.2

    linhas_html = "".join(
        f'<div class="ln" style="animation-delay:{t_p0 + i*passo_dur:.2f}s">{p}</div>'
        for i, p in enumerate(corpo))

    ac = accent
    base = css(fundo, accent, texto, dark)

    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
{base}
html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:{fundo}}}
body.medindo *{{animation:none!important;opacity:1!important;transform:none!important}}
body.medindo .palco{{visibility:hidden}}
.palco{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.cena{{position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:center;padding:110px 90px;box-sizing:border-box;opacity:0}}
.cena.c1{{background-image:linear-gradient({rgba(fundo,.82)} 0%,{rgba(fundo,.88)} 45%,{rgba(fundo,.96)} 100%),url('data:image/png;base64,{bg0}');background-size:cover;background-position:center;
  animation:entra .6s {t_gancho}s both, some .5s {t_sai1}s forwards}}
.cena.c2{{background-image:linear-gradient({rgba(fundo,.80)},{rgba(fundo,.92)}),url('data:image/png;base64,{bg1}');background-size:cover;background-position:center;
  animation:entra .6s {t_kick}s both, some .5s {t_sai2}s forwards}}
.cena.c3{{background:{fundo};animation:entra .6s {t_cta}s both}}

@keyframes entra{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes some{{from{{opacity:1}}to{{opacity:0}}}}
@keyframes sobe{{from{{opacity:0;transform:translateY(38px)}}to{{opacity:1;transform:none}}}}
@keyframes cresce{{from{{opacity:0;transform:scale(.86)}}to{{opacity:1;transform:none}}}}

.frase{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:44px;
  letter-spacing:.14em;text-transform:uppercase;color:{ac};line-height:1.2;
  padding-bottom:20px;border-bottom:5px solid {rgba(ac,.55)};align-self:flex-start;
  opacity:0;animation:sobe .6s {t_gancho}s both}}
.tarja{{display:inline-block;align-self:flex-start;background:{ac};
  color:{fundo if not dark else '#111'};font-family:'Plus Jakarta Sans',sans-serif;
  font-weight:800;font-size:42px;letter-spacing:.10em;text-transform:uppercase;
  padding:22px 34px 18px;margin:34px 0 44px;line-height:1;
  opacity:0;animation:sobe .6s {t_tarja}s both}}
.head{{font-family:'Playfair Display',serif;font-weight:900;font-size:104px;
  line-height:1.02;color:{texto};text-transform:uppercase;
  opacity:0;animation:sobe .7s {t_head}s both}}
.head b{{color:{ac}}}

.kick{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:40px;
  letter-spacing:.16em;text-transform:uppercase;color:{ac};margin-bottom:36px;
  opacity:0;animation:sobe .5s {t_kick + .2:.2f}s both}}
.tit{{font-family:'Playfair Display',serif;font-weight:900;font-size:76px;
  line-height:1.06;color:{texto};margin-bottom:64px;
  opacity:0;animation:sobe .5s {t_kick + .45:.2f}s both}}
.ln{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;font-size:46px;
  line-height:1.34;color:{texto};margin-bottom:34px;padding-left:30px;
  border-left:7px solid {rgba(ac,.65)};opacity:0;animation:sobe .55s both}}
.fecho{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:60px;
  line-height:1.22;color:{ac};margin-top:26px;padding:34px 0 0;
  border-top:5px solid {rgba(ac,.5)};
  opacity:0;animation:cresce .7s {t_fecho:.2f}s both}}

.cta-marca{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:40px;
  letter-spacing:.24em;color:{ac};margin-bottom:60px}}
.cta-of{{font-family:'Playfair Display',serif;font-weight:900;font-size:80px;
  line-height:1.08;color:{texto};margin-bottom:70px}}
.cta-site{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:56px;
  color:{ac};letter-spacing:.02em}}
.cta-sub{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;font-size:40px;
  color:{texto};opacity:.85;margin-bottom:14px}}
.cta-wa{{margin-top:70px;background:{ac};color:{fundo if not dark else '#111'};
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:56px;
  padding:30px 44px;border-radius:16px;align-self:flex-start}}
.assin{{position:absolute;left:90px;right:90px;bottom:96px;
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;font-size:32px;
  color:{texto};opacity:.7;line-height:1.4}}
</style></head><body class="medindo"><div class="palco">
{_selo_html}

<div class="cena c1">
  <div class="frase">{capa.get('chamada','')}</div>
  <div class="tarja">{capa.get('peca','')}</div>
  <div class="head">{capa.get('headline','')}</div>
</div>

<div class="cena c2">
  <div class="kick">{limpar(demo.get('kicker','')) if demo else ''}</div>
  <div class="tit">{limpar(demo.get('titulo','')) if demo else ''}</div>
  {linhas_html}
  <div class="fecho">{fecho}</div>
</div>

<div class="cena c3">
  <div class="cta-marca">{MK_ARROBA}</div>
  <div class="cta-of">{limpar(oferta.get('oferta',''))}</div>
  <div class="cta-sub">{MK_SUB}</div>
  <div class="cta-site">{MK_SITE}</div>
  <div class="cta-wa">{MK_ZAP}</div>
  <div class="assin">{MK_ASSIN}</div>
</div>

</div></body></html>"""
    return html, TOTAL


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 reel.py <spec.json>")
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.join(BASE, spec["outdir"])
    os.makedirs(out, exist_ok=True)

    html, total = montar_html(spec, out)
    dur_ms = int(total * 1000) + 400
    print(f"[reel] duração {total:.1f}s")

    from playwright.sync_api import sync_playwright
    vdir = os.path.join(out, "_video")
    os.makedirs(vdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-device-scale-factor=1"])
        ctx = b.new_context(viewport={"width": W, "height": H},
                            record_video_dir=vdir,
                            record_video_size={"width": W, "height": H})
        pg = ctx.new_page()
        pg.set_content(html, wait_until="load")
        # AJUSTE AUTOMATICO DE CAIXA — 17/08/2026.
        # A cena 2 carrega o argumento inteiro e, em peca densa, o texto
        # transbordava os 1920px e saia cortado no video. Aqui cada cena
        # encolhe sozinha ate caber, antes de a animacao comecar.
        pg.wait_for_timeout(600)
        encolhidas = pg.evaluate("""() => {
            const fora = [];
            for (const c of document.querySelectorAll('.cena')) {
                const cabe = () => {
                    const cr = c.getBoundingClientRect();
                    let baixo = 0;
                    for (const f of c.children) {
                        const r = f.getBoundingClientRect();
                        if (r.bottom > baixo) baixo = r.bottom;
                    }
                    return baixo <= cr.bottom - 40;
                };
                let z = 1.0;
                while (!cabe() && z > 0.45) { z -= 0.02; c.style.zoom = z; }
                if (z < 0.995) fora.push(Math.round(z * 100));
            }
            return fora;
        }""")
        if encolhidas:
            print(f"[reel] cena(s) reduzida(s) para caber: {encolhidas}%")
        pg.evaluate("() => document.body.classList.remove('medindo')")
        pg.wait_for_timeout(dur_ms)
        ctx.close()
        b.close()

    webm = [os.path.join(vdir, f) for f in os.listdir(vdir) if f.endswith(".webm")]
    if not webm:
        sys.exit("ERRO: o Playwright não gravou o vídeo.")
    origem = webm[0]
    destino = os.path.join(out, f"{spec['slug']}_reel.mp4")

    # O Playwright comeca a gravar quando o contexto abre, ANTES de a pagina
    # montar. Isso deixava ~2s de preto no inicio — e num reel os primeiros
    # segundos sao tudo. Aqui a gente descobre onde o preto acaba e corta.
    # A entrada morta nem sempre e PRETA: com paleta clara, ou enquanto o
    # Chromium ainda nao pintou, ela e BRANCA. Rodamos a deteccao duas vezes,
    # a segunda com o video invertido, e cortamos pelo que durar mais.
    def _entrada_morta(filtro):
        det = subprocess.run(
            ["ffmpeg", "-i", origem, "-vf", filtro,
             "-an", "-f", "null", "-"], capture_output=True)
        for linha in det.stderr.decode(errors="ignore").splitlines():
            if "black_start:0" in linha and "black_end:" in linha:
                try:
                    return float(linha.split("black_end:")[1].split()[0])
                except Exception:
                    return 0.0
        return 0.0

    corte = max(_entrada_morta("blackdetect=d=0.15:pix_th=0.06"),
                _entrada_morta("negate,blackdetect=d=0.15:pix_th=0.06"))
    if corte > 0.05:
        # Somamos a duracao do fade de entrada: sem isso o reel ABRE no meio
        # do escurecimento, e o primeiro quadro — que e a capa do reel na
        # grade do perfil — sai quase preto.
        corte = corte + 0.45
        print(f"[reel] cortando {corte:.2f}s de preto do inicio")

    # h264 + faixa de audio silenciosa: o Instagram aceita melhor assim
    cmd = ["ffmpeg", "-y"] + (["-ss", f"{corte:.3f}"] if corte > 0.05 else []) + ["-i", origem,
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
           "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                  f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2",
           "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", destino]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print(r.stderr.decode()[-1500:])
        sys.exit("ERRO no ffmpeg.")

    for f in os.listdir(out):
        if f.startswith("_reelbg"):
            os.remove(os.path.join(out, f))
    import shutil
    shutil.rmtree(vdir, ignore_errors=True)
    mb = os.path.getsize(destino) / 1e6
    print(f"[reel] {destino}  ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
