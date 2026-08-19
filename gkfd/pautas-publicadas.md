# PAUTAS PUBLICADAS — GKFD
Contabilidade no Simples para vendedor de marketplace.

Uma linha por peça publicada. Este arquivo é o cérebro da antirrepetição:
toda sessão lê ele inteiro antes de escolher a pauta.

FORMATO DA LINHA:
DATA | HORA | ÁREA | MOMENTO | DOCUMENTO (o da tarja) | FRASE DE EFEITO | TÓPICO | ÂNGULO | HEADLINE | LAYOUT | CENA DA CAPA | PALETA | DESTINO NO SITE

## Peças publicadas

2026-08-18 | 11h25 | A8 ads | M6 investindo em ADS | ADS DA PLATAFORMA | ANTES DE SUBIR O ORÇAMENTO | ACOS lido sem imposto, tarifa e frete | demonstração aritmética do teto de ACOS por SKU | Sua campanha fecha com ACOS bom e a venda dá prejuízo | L1 | doc:planilha/formulario | G05 roxo plataforma | /areas/ads | FB 1336325419554251_122095533615451002 | IG 18368093047243254 | story e reel publicados nos dois destinos

2026-08-18 | 17h35 | A4 retencao | M8 saldo retido ou conta bloqueada | SALDO RETIDO | O DINHEIRO JA E SEU | retencao tributada como receita realizada e capital de giro preso | composicao do indisponivel por motivo, pedido e data, com prazo de liberacao conferido | O saldo ficou retido e o DAS venceu do mesmo jeito | L4 | doc:extrato/dobra | G06 vermelho retido | /areas/retencao | FB 1336325419554251_122095715241451002 | IG 18092647964646980 | story e reel publicados nos dois destinos

## Rodízio — estado atual
- Total do perfil: 2 posts com log. (A peça A3 repasse / REPASSE DO MÊS,
  de 17-18/08, saiu antes do log existir — considerar A3 e o ponto de
  vazamento REPASSE DO MÊS como usados, e a paleta G01 e o layout L2 também.)
- Áreas usadas: A3 repasse, A8 ads, A4 retenção.
- Momentos usados: M7 fechamento do mês, M6 investindo em ADS, M8 saldo retido.
- Pontos de vazamento usados: REPASSE DO MÊS, ADS DA PLATAFORMA, SALDO RETIDO.
- Paletas GKFD: G01 azul painel, G02 verde liberado, G03 laranja embalagem,
  G04 noturno operacional, G05 roxo plataforma, G06 vermelho retido.
  Usadas: G01, G05, G06. Não repetir nas três últimas — próxima peça sai em
  G02, G03 ou G04.
- Frases de efeito usadas: CONFERE UMA COISA, ANTES DE SUBIR O ORÇAMENTO,
  O DINHEIRO JÁ É SEU.
- Layouts: L1 a L6. Usados: L2, L1, L4. Não repetir nos três últimos —
  próxima peça sai em L5 ou L6 (L3 segue vetado por causa do selo).
- Modo demonstração: usado em 18/08 (ADS). A peça de SALDO RETIDO saiu sem
  demonstração, com o slide 4 no formato "o erro que se repete". A PRÓXIMA
  peça leva demonstração aritmética.
- Sem banco de fotos: fundo sempre gerado (documento numérico + superfície
  neutra). Nada de foto.

## LIÇÕES

**18/08/2026 — a família de documento "liquidacao" NÃO serve para a GKFD.**
A capa saiu na primeira tentativa com `doc:liquidacao/dobra` e o fundo veio
cheio de "Horas extras 50%", "Reflexo em DSR", "FGTS + 40%", "Multa 477" —
verbas trabalhistas, universo da perícia, marca errada. O `fundo_numerico.py`
é compartilhado com a IntegraJud e a lista VERBAS é de lá. Para a GKFD, as
famílias seguras são **extrato** (lista LANC: repasse de vendas, retenção por
disputa, reserva de garantia, liberação parcial, chargeback — feita sob
medida), **planilha**, **comparativo**, **apuracao** e **razao**. NUNCA usar
`liquidacao`, e olhar o fundo antes de publicar.

**18/08/2026 — o selo de 320px também colide no L6.**
Mesmo problema já registrado no L3, por outro motivo: o L6 centraliza a
chamada horizontalmente, e ela passou por baixo do selo ("O DINHEIRO JÁ É
SE▮"). Trocado para **L4**, que alinha tudo à esquerda e centraliza no eixo
vertical — a chamada, a tarja e a cifra ficam bem longe do canto superior
direito. Regra consolidada: com selo de 320px, a capa sai em L1, L2 ou L4.
L3 e L6 estão vetados enquanto o selo estiver nesse tamanho.

**18/08/2026 — a cifra do L4 pode ser um argumento, não uma promessa.**
O L4 pede um número protagonista, e número em peça de contador é terreno
minado. A saída que funcionou: `"R$ 0,00"` com o rótulo "o que a retenção
abate da base do DAS". É afirmação técnica verdadeira, ocupa o lugar da
cifra com força visual e não promete resultado nenhum. Padrão reaproveitável.

**18/08/2026 — três slides de valor transbordaram na primeira renderização.**
1510, 1530 e 1365 contra o limite de 1350. Cada passo do slide de valor
suporta cerca de 3 linhas de texto corrido depois do `<em>`; quatro passos
só cabem se cada um ficar em 2 linhas. Cortar sentença inteira funciona
melhor do que enxugar palavra por palavra.

**18/08/2026 — o reel saía assinado IntegraJud mesmo com o bloco "marca".**
O bloco "marca" da seção 9 da instrução NÃO tem o campo `assinatura`, e o
`reel.py` lê exatamente esse campo para o rodapé da cena final. Sem ele, o
default entra: "Fábio Rebouças — Contador e Perito Contábil · IntegraJud ·
Inteligência pericial para advocacia". O carrossel e o story saíram certos; só
o reel não. Foi pego olhando o último frame do mp4 antes de publicar.
ACRESCENTAR AO BLOCO "marca" DE TODO SPEC DA GKFD:

    "assinatura": "GKFD Contábil · Mercado Líder Platinum<br>Contabilidade no Simples Nacional para vendedor de marketplace"

**18/08/2026 — selo de 320px colide com a headline no layout L3.**
No L3 o texto sobe para o topo e o selo fica em top:56px right:64px. A primeira
linha da headline entrou por baixo do selo. Trocado para L1, que centraliza a
headline, e resolveu. Regra: com selo de 320px, evitar L3 na capa. No slide de
oferta, a "ponte" também precisa de linhas curtas (até ~20 caracteres por
linha) para não passar por baixo do selo.

**18/08/2026 — quadro de demonstração transborda com 10 linhas.**
O layout do slide de valor comporta cerca de 7 linhas de quadro mais kicker,
título de duas linhas e rodapé de duas linhas. Comissão e frete foram fundidos
numa linha só ("Comissão de 14% e frete do vendedor · − R$ 35,80") sem quebrar
a aritmética. Conferir sempre a saída do machine.py: ele avisa TRANSBORDO.

**18/08/2026 — três capas seguidas com a mesma cara, e o motivo não era a paleta.**
As peças de 18/08 usaram G01 azul, G05 roxo e G06 vermelho, com layouts L2, L1 e
L4, e cenas de capa doc:apuracao, doc:planilha e doc:extrato. Tudo diferente no
papel — e as três leram como a mesma peça no feed, porque as três eram TABELA DE
NÚMERO atrás de texto. Família diferente, gênero igual.
A regra "capa SEMPRE documento numérico" veio da IntegraJud, onde o documento é
o processo e faz sentido. Aqui virou monotonia em três dias.
CORRIGIDO na seção 8 da instrução: a capa ALTERNA entre documento e superfície,
e nunca três seguidas do mesmo tipo. Capa de superfície usa overlay leve
(.30,.52,.74), porque não há número para esconder — o que domina é a cor da
paleta com a textura do material.
TIPO DE CAPA DAS ÚLTIMAS TRÊS: documento, documento, documento.
A PRÓXIMA CAPA TEM DE SER SUPERFÍCIE.
