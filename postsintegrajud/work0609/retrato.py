#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara o retrato do Fábio para entrar na peça, em quatro modos.

O arquivo-fonte fica em fotos/fabio.jpg (ou fotos_banco/fabio.jpg).

MODOS
  selo     recorte quadrado do rosto, circular, para o rodapé da capa
  faixa    recorte vertical para ocupar uma coluna lateral
  fundo    retrato escurecido e dessaturado, para camada de fundo
  contato  recorte para o slide 3, ao lado do bloco de contato

Todos devolvem PNG com transparência quando faz sentido (selo redondo).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
FONTES = ["fotos/fabio.jpg", "fotos_banco/fabio.jpg", "fabio.jpg"]

# onde está o rosto na foto original, em fração da largura/altura.
# medido na foto enviada em 16/08/2026 (1122x1402): rosto no terço superior,
# ligeiramente à esquerda do centro.
ROSTO_X, ROSTO_Y = 0.47, 0.20


def carregar():
    for rel in FONTES:
        p = os.path.join(BASE, rel)
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    sys.exit("ERRO: fabio.jpg não encontrado em fotos/ nem em fotos_banco/.")


def _janela(im, cx, cy, largura_frac, aspecto, saida):
    """Recorta uma JANELA do original e só depois redimensiona.

    largura_frac: quanto da largura original a janela ocupa (0-1).
                  Valor pequeno = enquadramento fechado.
    aspecto:      altura / largura da janela.
    Isso permite fechar no rosto — o corte cover, sozinho, sempre
    devolvia o torso inteiro numa foto de corpo.
    """
    jw = max(8, int(im.width * largura_frac))
    jh = max(8, int(jw * aspecto))
    if jh > im.height:
        jh = im.height
        jw = max(8, int(jh / aspecto))
    l = int(cx * im.width - jw / 2)
    t = int(cy * im.height - jh / 2)
    l = max(0, min(l, im.width - jw))
    t = max(0, min(t, im.height - jh))
    return im.crop((l, t, l + jw, t + jh)).resize(saida, Image.LANCZOS)


def selo(im, lado=260, borda=None):
    """Rosto em recorte circular, com anel na cor de destaque."""
    d = lado * 3  # renderiza grande e reduz, para a borda sair limpa
    face = _janela(im, ROSTO_X, ROSTO_Y, 0.46, 1.0, (d, d))
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, d, d], fill=255)
    out = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    out.paste(face, (0, 0), mask)
    if borda:
        anel = ImageDraw.Draw(out)
        anel.ellipse([4, 4, d - 5, d - 5], outline=borda, width=14)
    return out.resize((lado, lado), Image.LANCZOS)


def faixa(im, larg=380, alt=1350, escurecer=0.30):
    """Coluna vertical, para a lateral da capa."""
    col = _janela(im, ROSTO_X, 0.44, 0.66, alt / larg, (larg, alt))
    col = ImageEnhance.Color(col).enhance(1 - escurecer)
    col = ImageEnhance.Brightness(col).enhance(1 - escurecer * .55)
    return col


def fundo(im, larg=1080, alt=1350, forca=0.72):
    """Camada de fundo: bem escura e dessaturada, para o texto assentar."""
    f = _janela(im, ROSTO_X, 0.42, 1.0, alt / larg, (larg, alt))
    f = ImageEnhance.Color(f).enhance(0.18)
    f = ImageEnhance.Brightness(f).enhance(1 - forca)
    return f.filter(ImageFilter.GaussianBlur(1.2))


def fundo_capa(im, larg=1080, alt=1350, forca=0.70, lado="direita",
               ocupa=0.60):
    """Retrato como CAMADA DE FUNDO, com o texto por cima.

    A figura é recortada numa COLUNA e colada encostada na borda escolhida.
    Colar em posição explícita, em vez de confiar no recorte, é o que garante
    que o rosto fique do lado visível — tentar acertar isso movendo a janela
    do corte já jogou a cara para dentro da área do documento uma vez.

    ocupa: fração da largura que a figura ocupa.
    forca: 0 = foto crua · 1 = quase preto.
    """
    cw = int(larg * ocupa)
    figura = _janela(im, ROSTO_X, 0.42, 0.72, alt / cw, (cw, alt))
    figura = ImageEnhance.Color(figura).enhance(0.60)

    base = ImageEnhance.Brightness(
        ImageEnhance.Color(
            _janela(im, ROSTO_X, 0.42, 1.0, alt / larg, (larg, alt))
        ).enhance(0.20)).enhance(0.28)

    quadro = base.copy()
    quadro.paste(figura, (larg - cw if lado == "direita" else 0, 0))

    # degrade em duas direções: topo limpo (o rosto), base e lado do texto escuros
    grad = Image.new("L", (larg, alt))
    px = grad.load()
    for y in range(alt):
        v = y / (alt - 1)
        baixo = max(0.0, (v - 0.36) / 0.64) ** 1.15
        for x in range(larg):
            u = x / (larg - 1)
            h = (1.0 - u) if lado == "direita" else u
            h = max(0.0, (h - 0.28) / 0.72) ** 0.85
            a = min(1.0, max(baixo, h * 0.92, baixo * 0.6 + h * 0.6))
            px[x, y] = int(255 * (0.14 + 0.86 * a))

    escuro = Image.new("RGB", (larg, alt), (0, 0, 0))
    out = Image.composite(escuro, quadro,
                          Image.eval(grad, lambda v: int(v * forca)))
    return ImageEnhance.Brightness(out).enhance(1 - forca * 0.10)


def mistura_doc(retrato_im, doc_im, lado="direita", corte=0.40, suavidade=0.13):
    """Combina o RETRATO com o DOCUMENTO numérico na mesma capa.

    A figura fica de um lado, o documento aparece do outro — que é justamente
    o lado escuro, onde o texto vive. Assim a peça mantém a identidade do
    autor E continua girando as 8 famílias de documento, os 5 papéis e as 10
    paletas. Sem isso, toda capa com retrato seria a mesma imagem.
    """
    larg, alt = retrato_im.size
    mask = Image.new("L", (larg, 1))
    px = mask.load()
    for x in range(larg):
        u = x / (larg - 1)
        d = (u - corte) / suavidade if lado == "direita" else (corte - u) / suavidade
        px[x, 0] = int(255 * max(0.0, min(1.0, d * 0.5 + 0.5)))
    mask = mask.resize((larg, alt))
    return Image.composite(retrato_im, doc_im.resize((larg, alt)), mask)


def contato(im, larg=430, alt=560):
    """Retrato para o slide 3, do peito para cima."""
    return _janela(im, ROSTO_X, 0.26, 0.62, alt / larg, (larg, alt))


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "selo"
    saida = sys.argv[2] if len(sys.argv) > 2 else f"retrato_{modo}.png"
    cor = sys.argv[3] if len(sys.argv) > 3 else "#C9A227"
    im = carregar()
    if modo == "selo":
        r = selo(im, 260, cor)
    elif modo == "faixa":
        r = faixa(im)
    elif modo == "fundo":
        r = fundo(im)
    elif modo == "contato":
        r = contato(im)
    else:
        sys.exit(f"modo desconhecido: {modo}")
    r.save(saida)
    print(f"{modo} -> {saida} {r.size}")


if __name__ == "__main__":
    main()
