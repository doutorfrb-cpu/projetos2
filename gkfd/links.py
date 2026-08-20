#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LINKS DE WHATSAPP COM ORIGEM — para saber de onde veio o contato.

    py links.py carrossel instagram "conciliação de repasse"
    py links.py story facebook
    py links.py --todos

POR QUE ISTO EXISTE — 19/08/2026.
As duas marcas usam o mesmo numero: 11 97723-7113. Quando alguem chama, nao
da para saber se veio da GKFD ou da IntegraJud, do carrossel ou do story, do
Instagram ou do Facebook. Sem isso, nenhuma mudanca que a gente faz e
mensuravel — e em 19/08 a capa mudou inteira.

O conserto e barato: o link wa.me aceita uma mensagem ja escrita. A pessoa
abre a conversa com a origem digitada. Voce le na primeira linha, sem
instalar nada, sem painel, sem custo.

A marca sai do nome da pasta. Nao precisa configurar.
"""
import os
import sys
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
NUMERO = "5511977237113"

_nome = os.path.basename(BASE).lower()
MARCA = "GKFD" if "gkfd" in _nome else "IntegraJud"

# A frase muda por marca porque quem escreve e o cliente, e os dois clientes
# falam diferente: o advogado fala de caso, o vendedor fala de operacao.
ABERTURA = {
    "IntegraJud": "Vi o {formato} da IntegraJud no {destino}",
    "GKFD": "Vi o {formato} da GKFD no {destino}",
}
FECHO = {
    "IntegraJud": "e queria falar sobre o cálculo do meu processo.",
    "GKFD": "e queria falar sobre a apuração da minha operação.",
}

FORMATOS = ("carrossel", "story", "reel", "bio", "comentario", "post")
DESTINOS = {"instagram": "Instagram", "facebook": "Facebook",
            "linkedin": "LinkedIn"}


def link(formato, destino, tema=""):
    if formato not in FORMATOS:
        raise ValueError("formato deve ser um de: %s" % ", ".join(FORMATOS))
    if destino not in DESTINOS:
        raise ValueError("destino deve ser instagram, facebook ou linkedin")
    if destino == "linkedin":
        # LINK CURTO — 20/08/2026. A frase inteira codificada gerava uma URL de
        # quatro linhas na caixa do LinkedIn, feia e desconfiavel. Aqui vai so a
        # origem: continua rastreavel e cabe numa linha.
        txt = "Vim do LinkedIn"
        if tema:
            txt += " - %s" % tema
        return "https://wa.me/%s?text=%s" % (NUMERO, urllib.parse.quote(txt))
    if formato == "bio":
        # O link da bio nao vem de peca nenhuma: e quem chegou pelo perfil.
        txt = ("Cheguei pelo perfil da %s no %s "
               % (MARCA, DESTINOS[destino])) + FECHO[MARCA]
        return "https://wa.me/%s?text=%s" % (NUMERO, urllib.parse.quote(txt))
    txt = ABERTURA[MARCA].format(formato=formato, destino=DESTINOS[destino])
    if tema:
        txt += " sobre %s" % tema
    txt += " " + FECHO[MARCA]
    return "https://wa.me/%s?text=%s" % (NUMERO, urllib.parse.quote(txt))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    if a[0] == "--todos":
        print("Marca: %s\n" % MARCA)
        for f in FORMATOS:
            for d in DESTINOS:
                print("%-10s %-10s %s" % (f, d, link(f, d)))
        return
    formato = a[0]
    destino = a[1] if len(a) > 1 else "instagram"
    tema = a[2] if len(a) > 2 else ""
    print(link(formato, destino, tema))


if __name__ == "__main__":
    main()
