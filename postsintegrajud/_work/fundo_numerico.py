#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fundos que PARECEM o produto: documento com conta.

Decidido em 16/08/2026, depois de o Fábio perguntar se foto de arquivo antigo
chamava a atenção de advogado. Não chamava. Foto de papel velho comunica
HISTÓRIA; o advogado que procura assistente técnico está atrás de NÚMERO.

Oito famílias de documento, cor herdada da paleta da peça, acabamento de papel
sorteado. Nenhum dado real: os números são gerados e não formam caso nenhum.

USO DIRETO
    python3 fundo_numerico.py extrato P05 11 papel_envelhecido saida.jpg

USO PELO GERADOR (é o normal)
    no spec:  "cenas": ["doc:extrato", "linho", "foto:algo.jpg"]
    o machine.py chama daqui passando a paleta da peça.
"""

import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
BASE = os.path.dirname(os.path.abspath(__file__))

FAMILIAS = ["memoria", "extrato", "planilha", "razao",
            "evolucao", "comparativo", "apuracao", "liquidacao"]

PAPEIS = ["liso", "envelhecido", "formulario", "dobra", "copia"]

# fundo, destaque, texto — espelha PALETAS do machine.py
PALETAS = {
    "P01": ("#0B0B0B", "#C9A227", "#F2EFE6"),
    "P02": ("#16181A", "#D9A441", "#ECEAE4"),
    "P03": ("#F5F2EA", "#A8862B", "#14140F"),
    "P04": ("#14100B", "#D4AF37", "#F5EEDC"),
    "P05": ("#0E1F1B", "#C9A227", "#EAF2EE"),
    "P06": ("#0C1D2B", "#D6A85A", "#E9F0F5"),
    "P07": ("#1B0F13", "#C9A227", "#F3E9EA"),
    "P08": ("#E6E4DF", "#7A6320", "#191919"),
    "P09": ("#10141F", "#B9BFC8", "#F0F2F5"),
    "P10": ("#EDE6D8", "#8C6E1F", "#171310"),
}


# ------------------------------------------------------------------ utilidades

def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _fonte(tam, negrito=False):
    cands = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if negrito
             else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return ImageFont.load_default()


def _moeda(v):
    s = f"{abs(v):,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    return ("-" if v < 0 else "") + s


NEGATIVO = {"claro": (150, 46, 38), "escuro": (206, 92, 78)}


class Tela:
    """Superfície do documento, já com as cores da paleta resolvidas."""

    def __init__(self, paleta, rnd):
        bg, acc, fg = (_rgb(c) for c in PALETAS[paleta])
        claro = sum(bg) / 3 > 128
        # o papel não é a cor chapada da paleta: puxa levemente para o neutro
        self.bg = _mix(bg, (255, 255, 255) if claro else (0, 0, 0), .12)
        self.fg = fg
        self.acc = acc
        self.soft = _mix(fg, self.bg, .52)
        self.neg = NEGATIVO["claro" if claro else "escuro"]
        self.linha = _mix(fg, self.bg, .74)
        self.claro = claro
        self.rnd = rnd
        self.im = Image.new("RGB", (W, H), self.bg)
        self.d = ImageDraw.Draw(self.im)


# ---------------------------------------------------------------- as famílias

HIST = ["Parcela vencida", "Encargo do periodo", "Amortizacao", "Correcao monetaria",
        "Juros remuneratorios", "Tarifa contratada", "Estorno lancado",
        "Retencao por disputa", "Multa contratual", "Saldo transportado",
        "Ajuste de competencia", "Repasse liquido"]

LANC = ["Repasse de vendas", "Tarifa de servico", "Estorno de pedido",
        "Retencao - disputa", "Antecipacao", "Chargeback", "Frete subsidiado",
        "Reserva de garantia", "Liberacao parcial", "Deposito judicial",
        "Debito automatico", "Transferencia"]

VERBAS = ["Horas extras 50%", "Reflexo em DSR", "Adicional noturno",
          "Ferias + 1/3", "13o proporcional", "FGTS + 40%", "Aviso previo",
          "Insalubridade", "Intervalo suprimido", "Multa 477"]


def _cabecalho(t, cols, y=118):
    f = _fonte(20, True)
    for texto, px, anc in cols:
        t.d.text((px, y), texto, font=f, fill=t.soft, anchor=anc)
    t.d.line([(60, y + 32), (W - 60, y + 32)], fill=t.soft, width=1)
    return y + 60


def _linhas(t, y, montar, n=32, alt=41, destaques=(4, 12, 21)):
    """Percorre as linhas chamando montar(i, y, cor, cor_suave)."""
    for i in range(n):
        if y > H - 80:
            break
        d = i in destaques
        montar(i, y, t.acc if d else t.fg, t.acc if d else t.soft)
        if d:
            t.d.rectangle([56, y - 9, W - 56, y + 32], outline=t.acc, width=2)
        y += alt


def memoria(t):
    f, fb = _fonte(23), _fonte(24, True)
    x = [70, 240, 600, 770, 1015]
    y = _cabecalho(t, [("COMPETENCIA", x[0], "la"), ("HISTORICO", x[1], "la"),
                       ("BASE", x[2], "ra"), ("INDICE", x[3], "ra"),
                       ("CORRIGIDO", x[4], "ra")])
    b0 = t.rnd.uniform(9000, 210000)

    def m(i, yy, c, cs):
        b = b0 * t.rnd.uniform(.35, 1.6)
        idx = t.rnd.uniform(1.0012, 1.0912)
        t.d.text((x[0], yy), f"{t.rnd.randint(1,12):02d}/20{t.rnd.randint(18,25)}", font=f, fill=cs, anchor="la")
        t.d.text((x[1], yy), HIST[i % len(HIST)][:19], font=f, fill=cs, anchor="la")
        t.d.text((x[2], yy), _moeda(b), font=f, fill=c, anchor="ra")
        t.d.text((x[3], yy), f"{idx:.6f}", font=f, fill=cs, anchor="ra")
        t.d.text((x[4], yy), _moeda(b * idx), font=fb, fill=c, anchor="ra")

    _linhas(t, y, m)


def extrato(t):
    f, fb = _fonte(23), _fonte(24, True)
    y = _cabecalho(t, [("DATA", 70, "la"), ("LANCAMENTO", 195, "la"),
                       ("DOC", 640, "ra"), ("VALOR", 840, "ra"), ("SALDO", 1015, "ra")])
    saldo = [t.rnd.uniform(80000, 340000)]

    def m(i, yy, c, cs):
        v = t.rnd.uniform(400, 26000) * (1 if t.rnd.random() < .34 else -1)
        saldo[0] += v
        t.d.text((70, yy), f"{t.rnd.randint(1,28):02d}/{t.rnd.randint(1,12):02d}", font=f, fill=cs, anchor="la")
        t.d.text((195, yy), LANC[i % len(LANC)][:21], font=f, fill=cs, anchor="la")
        t.d.text((640, yy), f"{t.rnd.randint(100000,999999)}", font=f, fill=cs, anchor="ra")
        t.d.text((840, yy), _moeda(v), font=f,
                 fill=(t.neg if v < 0 else c), anchor="ra")
        t.d.text((1015, yy), _moeda(saldo[0]), font=fb, fill=c, anchor="ra")

    _linhas(t, y, m)


def razao(t):
    f, fb = _fonte(23), _fonte(24, True)
    y = _cabecalho(t, [("DATA", 70, "la"), ("HISTORICO", 195, "la"),
                       ("DEBITO", 700, "ra"), ("CREDITO", 880, "ra"), ("SALDO", 1015, "ra")])
    saldo = [t.rnd.uniform(20000, 180000)]

    def m(i, yy, c, cs):
        deb = t.rnd.random() < .5
        v = t.rnd.uniform(300, 42000)
        saldo[0] += v if deb else -v
        t.d.text((70, yy), f"{t.rnd.randint(1,28):02d}/{t.rnd.randint(1,12):02d}", font=f, fill=cs, anchor="la")
        t.d.text((195, yy), HIST[(i + 3) % len(HIST)][:21], font=f, fill=cs, anchor="la")
        t.d.text((700, yy), _moeda(v) if deb else "", font=f, fill=c, anchor="ra")
        t.d.text((880, yy), "" if deb else _moeda(v), font=f, fill=c, anchor="ra")
        t.d.text((1015, yy), _moeda(saldo[0]), font=fb, fill=c, anchor="ra")

    _linhas(t, y, m)


def evolucao(t):
    f, fb = _fonte(23), _fonte(24, True)
    y = _cabecalho(t, [("PARC", 70, "la"), ("PRESTACAO", 380, "ra"),
                       ("JUROS", 600, "ra"), ("AMORT", 810, "ra"), ("SALDO DEV.", 1015, "ra")])
    sd = [t.rnd.uniform(120000, 620000)]
    i_m = t.rnd.uniform(.008, .021)

    def m(i, yy, c, cs):
        j = sd[0] * i_m
        p = sd[0] * (i_m / (1 - (1 + i_m) ** -(60 - i))) if i < 55 else j * 1.4
        a = p - j
        sd[0] = max(0, sd[0] - a)
        t.d.text((70, yy), f"{i+1:03d}/060", font=f, fill=cs, anchor="la")
        t.d.text((380, yy), _moeda(p), font=f, fill=c, anchor="ra")
        t.d.text((600, yy), _moeda(j), font=f, fill=cs, anchor="ra")
        t.d.text((810, yy), _moeda(a), font=f, fill=cs, anchor="ra")
        t.d.text((1015, yy), _moeda(sd[0]), font=fb, fill=c, anchor="ra")

    _linhas(t, y, m)


def comparativo(t):
    f, fb = _fonte(23), _fonte(25, True)
    y = _cabecalho(t, [("COMPETENCIA", 70, "la"), ("CRITERIO A", 520, "ra"),
                       ("CRITERIO B", 790, "ra"), ("DIFERENCA", 1015, "ra")])
    t.d.line([(600, y - 24), (600, H - 70)], fill=t.linha, width=1)

    def m(i, yy, c, cs):
        a = t.rnd.uniform(12000, 380000)
        b = a * t.rnd.uniform(.78, .97)
        t.d.text((70, yy), f"{t.rnd.randint(1,12):02d}/20{t.rnd.randint(18,25)}", font=f, fill=cs, anchor="la")
        t.d.text((520, yy), _moeda(a), font=f, fill=c, anchor="ra")
        t.d.text((790, yy), _moeda(b), font=f, fill=cs, anchor="ra")
        t.d.text((1015, yy), _moeda(a - b), font=fb, fill=t.acc, anchor="ra")

    _linhas(t, y, m)


def apuracao(t):
    f, fb = _fonte(23), _fonte(24, True)
    y = _cabecalho(t, [("CONTA", 70, "la"), ("DECLARADO", 620, "ra"),
                       ("APURADO", 830, "ra"), ("AJUSTE", 1015, "ra")])
    contas = ["Receita bruta", "Deducoes", "Receita liquida", "CMV",
              "Lucro bruto", "Despesas comerciais", "Despesas administrativas",
              "Resultado financeiro", "Depreciacao", "EBITDA", "IRPJ e CSLL",
              "Lucro liquido", "Distribuicao", "Reserva legal"]

    def m(i, yy, c, cs):
        d1 = t.rnd.uniform(30000, 900000)
        d2 = d1 * t.rnd.uniform(.82, 1.14)
        t.d.text((70, yy), contas[i % len(contas)][:26], font=f, fill=cs, anchor="la")
        t.d.text((620, yy), _moeda(d1), font=f, fill=cs, anchor="ra")
        t.d.text((830, yy), _moeda(d2), font=f, fill=c, anchor="ra")
        t.d.text((1015, yy), _moeda(d2 - d1), font=fb,
                 fill=(t.neg if d2 - d1 < 0 else c), anchor="ra")

    _linhas(t, y, m, destaques=(2, 9, 18))


def liquidacao(t):
    f, fb = _fonte(23), _fonte(24, True)
    y = _cabecalho(t, [("VERBA", 70, "la"), ("BASE", 600, "ra"),
                       ("REFLEXO", 810, "ra"), ("TOTAL", 1015, "ra")])

    def m(i, yy, c, cs):
        b = t.rnd.uniform(800, 46000)
        r = b * t.rnd.uniform(.08, .42)
        t.d.text((70, yy), VERBAS[i % len(VERBAS)][:26], font=f, fill=cs, anchor="la")
        t.d.text((600, yy), _moeda(b), font=f, fill=cs, anchor="ra")
        t.d.text((810, yy), _moeda(r), font=f, fill=cs, anchor="ra")
        t.d.text((1015, yy), _moeda(b + r), font=fb, fill=c, anchor="ra")

    _linhas(t, y, m, destaques=(3, 11, 20))


def planilha(t):
    f, fb = _fonte(23), _fonte(23, True)
    cols = [60, 262, 464, 666, 868, 1020]
    lh, y0 = 46, 92
    n = int((H - 150) / lh)
    for r in range(n + 1):
        t.d.line([(50, y0 + r * lh), (W - 50, y0 + r * lh)], fill=t.linha, width=1)
    for c in cols:
        t.d.line([(c, y0), (c, y0 + n * lh)], fill=t.linha, width=1)
    for r in range(n):
        yy = y0 + r * lh + 10
        for ci in range(1, len(cols)):
            if t.rnd.random() < .13:
                continue
            div = t.rnd.random() < .055
            t.d.text((cols[ci] - 12, yy), _moeda(t.rnd.uniform(90, 470000)),
                     font=fb if div else f, fill=t.acc if div else t.fg, anchor="ra")
            if div:
                t.d.rectangle([cols[ci - 1] + 4, yy - 9, cols[ci] - 4, yy + 30],
                              outline=t.acc, width=2)


FN = {"memoria": memoria, "extrato": extrato, "planilha": planilha, "razao": razao,
      "evolucao": evolucao, "comparativo": comparativo, "apuracao": apuracao,
      "liquidacao": liquidacao}


# ----------------------------------------------------------- acabamento de papel

def acabar(t, papel):
    im = t.im
    rnd = t.rnd

    if papel == "envelhecido":
        gr = Image.effect_noise((W, H), 26).convert("L").filter(ImageFilter.GaussianBlur(.6))
        im = Image.blend(im, Image.merge("RGB", (gr, gr, gr)), .10 if not t.claro else .07)
        v = Image.new("L", (W, H), 0)
        ImageDraw.Draw(v).ellipse([-W * .35, -H * .28, W * 1.35, H * 1.28], fill=255)
        v = v.filter(ImageFilter.GaussianBlur(190))
        escuro = Image.new("RGB", (W, H), _mix(t.bg, (0, 0, 0), .34))
        im = Image.composite(im, escuro, v)

    elif papel == "formulario":
        ov = im.copy()
        d = ImageDraw.Draw(ov)
        faixa = _mix(t.bg, t.fg, .07)
        y, alt = 150, 82
        while y < H:
            d.rectangle([50, y, W - 50, y + alt], fill=faixa)
            y += alt * 2
        im = Image.blend(im, ov, .55)
        d = ImageDraw.Draw(im)
        for x in (30, W - 30):
            for yy in range(60, H - 40, 62):
                d.ellipse([x - 7, yy - 7, x + 7, yy + 7], outline=t.linha, width=2)

    elif papel == "dobra":
        yf = int(H * rnd.uniform(.36, .62))
        som = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(som)
        d.rectangle([0, yf - 26, W, yf], fill=90)
        d.rectangle([0, yf, W, yf + 26], fill=40)
        som = som.filter(ImageFilter.GaussianBlur(16))
        im = Image.composite(Image.new("RGB", (W, H), _mix(t.bg, (0, 0, 0), .5)), im, som)

    elif papel == "copia":
        im = im.rotate(rnd.uniform(-.7, .7), resample=Image.BICUBIC,
                       fillcolor=t.bg, expand=False)
        im = im.filter(ImageFilter.GaussianBlur(.5))
        gr = Image.effect_noise((W, H), 16).convert("L")
        im = Image.blend(im, Image.merge("RGB", (gr, gr, gr)), .06)

    return im


# --------------------------------------------------------------------- fachada

def gerar(familia, paleta, semente=7, papel=None):
    rnd = random.Random(semente)
    if familia in ("auto", None, ""):
        familia = rnd.choice(FAMILIAS)
    if papel in ("auto", None, ""):
        papel = rnd.choice(PAPEIS)
    t = Tela(paleta, rnd)
    FN[familia](t)
    return acabar(t, papel), familia, papel


def main():
    a = sys.argv[1:]
    familia = a[0] if len(a) > 0 else "auto"
    paleta = a[1] if len(a) > 1 else "P01"
    semente = int(a[2]) if len(a) > 2 else 7
    papel = a[3] if len(a) > 3 else "auto"
    saida = a[4] if len(a) > 4 else f"doc_{familia}_{paleta}.jpg"
    im, fam, pap = gerar(familia, paleta, semente, papel)
    im.save(saida, quality=93)
    print(f"{fam} · {paleta} · papel {pap} -> {saida}")


if __name__ == "__main__":
    main()
