#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica um carrossel de 3 slides no @integrajud pela API da Meta.

Sem navegador, sem file_upload, sem depender de conversa aberta.
Feito para ser chamado pelo agendador local depois que o machine.py renderizou.

USO
    python3 publicar_instagram.py PASTA_DA_PECA

    onde PASTA_DA_PECA é a subpasta AAAA-MM-DD_tema, contendo:
      *_1.png, *_2.png, *_3.png   os três slides
      legenda.txt                 a legenda pronta

CONFIGURAÇÃO — arquivo `config_publicacao.json` na raiz da pasta do projeto.
Ele guarda segredos: NÃO versionar, NÃO colar em conversa, NÃO mandar para
ninguém. O script lê e nunca imprime o conteúdo.

    {
      "ig_user_id": "178414...",
      "access_token": "EAAG...",
      "host": {
        "tipo": "ftp",
        "servidor": "ftp.integrajud.com.br",
        "usuario": "seu_usuario",
        "senha": "sua_senha",
        "pasta_remota": "/public_html/posts",
        "url_publica": "https://www.integrajud.com.br/posts"
      }
    }

Se preferir subir as imagens por outro meio (painel da hospedagem, rsync,
qualquer coisa), use "tipo": "manual" e o script apenas monta as URLs a partir
de url_publica, presumindo que os arquivos já estão lá.
"""

import json
import re
import io
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0"


# ---------------------------------------------------------------- utilidades

def log(msg):
    print(f"[publicar] {msg}", flush=True)


def carregar_config(raiz):
    p = os.path.join(raiz, "config_publicacao.json")
    if not os.path.exists(p):
        sys.exit(f"ERRO: falta {p}. Veja o cabeçalho deste arquivo.")
    with open(p, encoding="utf-8") as f:
        cfg = json.load(f)
    # TOKEN QUE NAO VENCE — melhoria de 16/08/2026.
    # O token de USUARIO, mesmo estendido, morre em 60 dias. O token da PAGINA,
    # quando nasce de um token de usuario de longa duracao, nao tem data de
    # expiracao (o Depurador mostra "Nunca"). E ele tambem publica no Instagram,
    # porque a conta esta vinculada aquela Pagina.
    # Entao: havendo page_token preenchido, ele tem prioridade sobre o
    # access_token, e a maquina deixa de depender de renovacao.
    _pt = str((cfg.get("facebook") or {}).get("page_token") or "")
    if _pt and not _pt.startswith("COLE_AQUI"):
        if cfg.get("access_token") != _pt:
            log("usando o token da Pagina (nao vence) no lugar do token de usuario")
        cfg["access_token"] = _pt

    for chave in ("ig_user_id", "access_token", "host"):
        if not cfg.get(chave):
            sys.exit(f"ERRO: config_publicacao.json sem '{chave}'.")
    return cfg


def http_post(url, campos):
    dados = urllib.parse.urlencode(campos).encode()
    req = urllib.request.Request(url, data=dados)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def http_get(url, campos):
    q = urllib.parse.urlencode(campos)
    with urllib.request.urlopen(f"{url}?{q}", timeout=60) as r:
        return json.loads(r.read().decode())


def erro_meta(e):
    """Extrai a mensagem útil de um HTTPError da Graph API."""
    try:
        corpo = json.loads(e.read().decode())
        m = corpo.get("error", {})
        return f"{m.get('type')} {m.get('code')}: {m.get('message')}"
    except Exception:
        return str(e)


# ------------------------------------------------------------------ hospedar

def enviar_por_ftp(host, arquivos):
    from ftplib import FTP
    ftp = FTP(host["servidor"], timeout=60)
    ftp.login(host["usuario"], host["senha"])
    try:
        ftp.cwd(host["pasta_remota"])
    except Exception:
        sys.exit(f"ERRO: pasta remota {host['pasta_remota']} não existe no servidor.")
    enviados = []
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        with open(caminho, "rb") as f:
            ftp.storbinary(f"STOR {nome}", f)
        enviados.append(nome)
        log(f"enviado: {nome}")
    ftp.quit()
    return enviados


def enviar_pelo_facebook(cfg, arquivos):
    """Hospeda as imagens na PRÓPRIA Página do Facebook e devolve as URLs.

    Por que isto existe: a API do Instagram não aceita arquivo — ela exige uma
    URL pública de onde BAIXAR a imagem. Isso obrigava a ter FTP e uma pasta
    no site, e era o único item que travava o Instagram por API.

    A saída é usar a Meta como hospedagem: a foto sobe na Página como
    NÃO PUBLICADA e TEMPORÁRIA (não aparece para ninguém, não vira post), e a
    própria Meta devolve uma URL de CDN. Essa URL serve de image_url para o
    contêiner do Instagram. Mesma conta, mesmo app, nenhum terceiro.

    Requer o bloco 'facebook' com page_id. O token da Página é obtido do mesmo
    jeito que no publicar_facebook.py.
    """
    import publicar_facebook as pf

    fb = cfg.get("facebook") or {}
    if not fb.get("page_id") or str(fb["page_id"]).startswith("COLE_AQUI"):
        sys.exit("ERRO: host tipo 'facebook' exige o bloco 'facebook' com page_id.")

    page_token = pf.resolver_page_token(cfg, dict(fb))
    urls = []
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        corpo, content_type = pf.multipart(
            {"published": "false", "temporary": "true",
             "access_token": page_token},
            "source", caminho)
        req = urllib.request.Request(
            f"{pf.API}/{fb['page_id']}/photos", data=corpo)
        req.add_header("Content-Type", content_type)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            sys.exit(f"ERRO ao hospedar {nome} na Meta: {pf.erro_meta(e)}")
        foto_id = resp.get("id")
        if not foto_id:
            sys.exit(f"ERRO: a Meta não devolveu id da foto para {nome}.")
        info = pf.pega(str(foto_id), {"fields": "images",
                                      "access_token": page_token})
        imagens = info.get("images") or []
        if not imagens:
            sys.exit(f"ERRO: a Meta não devolveu URL para {nome}.")
        # a maior versao e a primeira; queremos a de maior largura
        melhor = max(imagens, key=lambda i: i.get("width", 0))
        urls.append(melhor["source"])
        log(f"hospedada na Meta: {nome}")
    return urls


def hospedar(cfg, host, arquivos):
    """Devolve a lista de URLs públicas, na mesma ordem dos arquivos."""
    tipo = host.get("tipo", "ftp")
    if tipo == "facebook":
        return enviar_pelo_facebook(cfg, arquivos)
    if tipo == "ftp":
        nomes = enviar_por_ftp(host, arquivos)
    elif tipo == "manual":
        nomes = [os.path.basename(a) for a in arquivos]
        log("modo manual: presumindo que os arquivos já estão no servidor")
    else:
        sys.exit(f"ERRO: tipo de host desconhecido: {tipo}")
    base = host["url_publica"].rstrip("/")
    return [f"{base}/{n}" for n in nomes]


def conferir_url(url):
    """A Meta precisa BAIXAR a imagem. Se o link não abrir, ela recusa."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


# ------------------------------------------------------------------- publicar

def criar_filho(cfg, url, alt=""):
    # TEXTO ALTERNATIVO — 19/08/2026. A API aceita alt_text e a gente nunca
    # preencheu. Serve para leitor de tela e para a propria Meta entender do
    # que a peca trata. Custa zero: o texto sai da headline do slide.
    campos = {
        "image_url": url,
        "is_carousel_item": "true",
        "access_token": cfg["access_token"],
    }
    if alt:
        campos["alt_text"] = alt[:990]
    return http_post(f"{API}/{cfg['ig_user_id']}/media", campos)["id"]


def criar_pai(cfg, filhos, legenda):
    return http_post(f"{API}/{cfg['ig_user_id']}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(filhos),
        "caption": legenda,
        "access_token": cfg["access_token"],
    })["id"]


def esperar_pronto(cfg, container_id, tentativas=20, intervalo=6):
    for i in range(tentativas):
        r = http_get(f"{API}/{container_id}", {
            "fields": "status_code,status",
            "access_token": cfg["access_token"],
        })
        st = r.get("status_code")
        if st == "FINISHED":
            return True
        if st == "ERROR":
            sys.exit(f"ERRO: a Meta recusou o container. {r.get('status')}")
        log(f"container {container_id}: {st} ({i+1}/{tentativas})")
        time.sleep(intervalo)
    sys.exit("ERRO: o container não ficou pronto no tempo esperado.")


def publicar(cfg, pai_id):
    return http_post(f"{API}/{cfg['ig_user_id']}/media_publish", {
        "creation_id": pai_id,
        "access_token": cfg["access_token"],
    })["id"]


# ----------------------------------------------------------------------- main

def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 publicar_instagram.py PASTA_DA_PECA")

    pasta = os.path.abspath(sys.argv[1])
    if not os.path.isdir(pasta):
        sys.exit(f"ERRO: pasta não encontrada: {pasta}")
    raiz = os.path.dirname(pasta)

    # SO OS SLIDES DA PECA — correcao de 18/08/2026.
    # Antes daqui saia `todo .png da pasta`, e isso publicou um carrossel de
    # SEIS imagens na GKFD: o story_916.png, que o extras.py grava na mesma
    # pasta, entrou como sexto slide, esticado no formato 4:5. Slide de peca
    # sempre termina em _<numero>.png; story, reel e qualquer outro arquivo
    # ficam de fora por construcao, e a ordem passa a ser NUMERICA e nao
    # alfabetica (com dez ou mais slides, _10 vinha antes de _2).
    def _num(nome):
        # story_916.png TAMBEM termina em _<numero>.png — a primeira versao
        # desta correcao caiu nessa e deixou o story passar de novo. Slide de
        # peca e numerado de 1 a 20 e nao carrega 'story' nem 'reel' no nome;
        # arquivos internos comecam com sublinhado.
        base = os.path.basename(nome).lower()
        if base.startswith("_") or "story" in base or "reel" in base:
            return None
        m = re.search(r"_(\d+)\.png$", base)
        if not m:
            return None
        n = int(m.group(1))
        return n if 1 <= n <= 20 else None

    pngs = sorted((f for f in os.listdir(pasta) if _num(f) is not None),
                  key=_num)
    _fora = [f for f in os.listdir(pasta)
             if f.lower().endswith(".png") and _num(f) is None]
    if _fora:
        print("[publicar] fora do carrossel (nao sao slides): %s"
              % ", ".join(sorted(_fora)))
    if len(pngs) < 2:
        sys.exit(f"ERRO: preciso de pelo menos 2 imagens, achei {len(pngs)}.")
    if len(pngs) > 10:
        sys.exit("ERRO: o carrossel aceita no máximo 10 imagens.")
    caminhos = [os.path.join(pasta, n) for n in pngs]

    for c in caminhos:
        mb = os.path.getsize(c) / 1048576
        if mb > 8:
            sys.exit(f"ERRO: {os.path.basename(c)} tem {mb:.1f} MB. O limite é 8 MB.")

    leg = os.path.join(pasta, "legenda.txt")
    legenda = open(leg, encoding="utf-8").read().strip() if os.path.exists(leg) else ""
    if len(legenda) > 2200:
        sys.exit(f"ERRO: legenda com {len(legenda)} caracteres. O limite é 2200.")

    cfg = carregar_config(raiz)

    log(f"{len(caminhos)} imagens, legenda com {len(legenda)} caracteres")

    urls = hospedar(cfg, cfg["host"], caminhos)
    for u in urls:
        if not conferir_url(u):
            sys.exit(f"ERRO: {u} não abre publicamente. A Meta não vai conseguir baixar.")
    log("todas as URLs respondem publicamente")

    try:
        # O alt de cada slide sai do proprio arquivo alt.txt, uma linha por
        # slide, se ele existir. Sem o arquivo, publica sem alt e nada quebra.
        _altf = os.path.join(pasta, "alt.txt")
        _alts = []
        if os.path.exists(_altf):
            _alts = [l.strip() for l in io.open(_altf, encoding="utf-8")
                     if l.strip()]
        filhos = [criar_filho(cfg, u, _alts[i] if i < len(_alts) else "")
                  for i, u in enumerate(urls)]
        log(f"containers filhos criados: {len(filhos)}")

        pai = criar_pai(cfg, filhos, legenda)
        log(f"container pai: {pai}")

        esperar_pronto(cfg, pai)
        post_id = publicar(cfg, pai)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO da Meta: {erro_meta(e)}")

    log(f"PUBLICADO. id do post: {post_id}")
    print(post_id)


if __name__ == "__main__":
    main()
