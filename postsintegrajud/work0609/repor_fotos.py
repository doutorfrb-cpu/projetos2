#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mantém o banco fotos_banco/ sempre abastecido, sem intervenção do Fábio.

USO

    python3 repor_fotos.py --status
        Diz quantas fotos existem, quantas estão bloqueadas pela janela de 20
        dias e quantas estão livres para a próxima peça. Código de saída 1
        quando o banco está abaixo do mínimo — é o gatilho da reposição.

    python3 repor_fotos.py 12345 67890 ...
        Baixa esses ids do Pexels para fotos_banco/px_<id>.jpg, valida e
        descarta o que não presta. Já existente é pulado.

COMO OS IDS APARECEM
    A sessão que roda a máquina procura no Pexels por termos de objeto e
    ambiente (autos, arquivo, livro-razão, papel envelhecido, mesa com
    documento) e passa os ids aqui. Este script não navega: ele baixa,
    confere e nomeia. Assim a busca fica com quem sabe julgar a imagem, e o
    trabalho chato fica automatizado.

REGRA DE ACERVO
    Foto usada não repete por 20 dias. O bloqueio sai de pautas-publicadas.md,
    que é a fonte da verdade — este script lê o log, não adivinha.
"""

import os
import re
import sys
import datetime
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(BASE, "fotos_banco")

# minimo de fotos LIVRES para a maquina rodar sem repetir imagem
MINIMO_LIVRES = 8
# alvo ao repor: quantas livres queremos deixar disponiveis
ALVO_LIVRES = 16
# janela de bloqueio, em dias
JANELA = 20

CDN = ("https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg"
       "?auto=compress&cs=tinysrgb&w=1600")

# A capa e 1080x1350 e o corte e em cover. O que importa nao e a dimensao
# bruta, e quanto a foto precisa ser AMPLIADA para preencher o quadro: acima
# de 1.35x a ampliacao aparece. Paisagem larga passa, panoramica nao.
AMPLIACAO_MAX = 1.35
BYTES_MIN = 60_000


def log(msg):
    print(f"[fotos] {msg}", flush=True)


def achar_log():
    """pautas-publicadas.md vive na raiz da pasta do projeto, não aqui."""
    for cand in (
        os.path.join(BASE, "pautas-publicadas.md"),
        os.path.join(os.path.dirname(BASE), "pautas-publicadas.md"),
        os.path.join(BASE, "..", "..", "pautas-publicadas.md"),
    ):
        if os.path.exists(cand):
            return os.path.abspath(cand)
    return None


def bloqueadas(caminho_log, hoje=None):
    """Ids de foto usados dentro da janela de 20 dias, lidos do log."""
    if not caminho_log:
        return set()
    hoje = hoje or datetime.date.today()
    limite = hoje - datetime.timedelta(days=JANELA)
    usadas = set()
    for linha in open(caminho_log, encoding="utf-8"):
        m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})\s*\|", linha)
        if not m:
            continue
        try:
            data = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            continue
        if data < limite:
            continue
        usadas.update(re.findall(r"px_(\d+)", linha))
    return usadas


def existentes():
    if not os.path.isdir(BANCO):
        return set()
    return {m.group(1) for m in
            (re.match(r"px_(\d+)\.jpg$", n) for n in os.listdir(BANCO)) if m}


def status():
    caminho_log = achar_log()
    tem = existentes()
    presas = bloqueadas(caminho_log) & tem
    livres = tem - presas
    log(f"log: {caminho_log or 'NAO ENCONTRADO — sem bloqueio aplicado'}")
    log(f"banco: {len(tem)} fotos | bloqueadas {len(presas)} | livres {len(livres)}")
    if livres:
        log("livres: " + ", ".join("px_" + i for i in sorted(livres)))
    faltam = max(0, ALVO_LIVRES - len(livres))
    if len(livres) < MINIMO_LIVRES:
        log(f"ABAIXO DO MINIMO ({MINIMO_LIVRES}). Repor pelo menos {faltam} fotos novas.")
        return 1
    log("banco em ordem.")
    return 0


def baixar(pid):
    destino = os.path.join(BANCO, f"px_{pid}.jpg")
    if os.path.exists(destino):
        log(f"px_{pid} ja existe, pulando")
        return False
    url = CDN.format(id=pid)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            dados = r.read()
    except Exception as e:
        log(f"px_{pid}: falhou o download ({e})")
        return False
    if len(dados) < BYTES_MIN:
        log(f"px_{pid}: arquivo pequeno demais ({len(dados)} bytes), descartado")
        return False
    os.makedirs(BANCO, exist_ok=True)
    with open(destino, "wb") as f:
        f.write(dados)
    try:
        from PIL import Image
        im = Image.open(destino)
        amp = max(1080 / im.width, 1350 / im.height)
        if amp > AMPLIACAO_MAX:
            log(f"px_{pid}: {im.width}x{im.height} exigiria ampliar {amp:.2f}x, descartada")
            os.remove(destino)
            return False
        log(f"px_{pid}: ok, {im.width}x{im.height} (ampliacao {amp:.2f}x), {len(dados)//1024} KB")
    except ImportError:
        log(f"px_{pid}: salva ({len(dados)//1024} KB) — sem PIL para conferir dimensao")
    except Exception as e:
        log(f"px_{pid}: nao abriu como imagem ({e}), descartada")
        os.remove(destino)
        return False
    return True


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--status", "-s"):
        sys.exit(status())

    ids = [a for a in args if a.isdigit()]
    if not ids:
        sys.exit("uso: repor_fotos.py --status  |  repor_fotos.py <id> <id> ...")

    novas = sum(1 for pid in ids if baixar(pid))
    log(f"{novas} foto(s) nova(s) no banco")
    print()
    status()


if __name__ == "__main__":
    main()
