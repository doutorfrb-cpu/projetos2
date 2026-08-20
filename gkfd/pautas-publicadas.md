# PAUTAS PUBLICADAS — GKFD
Contabilidade no Simples para vendedor de marketplace.

Uma linha por peça publicada. Este arquivo é o cérebro da antirrepetição:
toda sessão lê ele inteiro antes de escolher a pauta.

FORMATO DA LINHA:
DATA | HORA | ÁREA | MOMENTO | DOCUMENTO (o da tarja) | FRASE DE EFEITO | TÓPICO | ÂNGULO | HEADLINE | LAYOUT | CENA DA CAPA | PALETA | DESTINO NO SITE

## Peças publicadas

2026-08-18 | 11h25 | A8 ads | M6 investindo em ADS | ADS DA PLATAFORMA | ANTES DE SUBIR O ORÇAMENTO | ACOS lido sem imposto, tarifa e frete | demonstração aritmética do teto de ACOS por SKU | Sua campanha fecha com ACOS bom e a venda dá prejuízo | L1 | doc:planilha/formulario | G05 roxo plataforma | /areas/ads | FB 1336325419554251_122095533615451002 | IG 18368093047243254 | story e reel publicados nos dois destinos

2026-08-18 | 17h35 | A4 retencao | M8 saldo retido ou conta bloqueada | SALDO RETIDO | O DINHEIRO JA E SEU | retencao tributada como receita realizada e capital de giro preso | composicao do indisponivel por motivo, pedido e data, com prazo de liberacao conferido | O saldo ficou retido e o DAS venceu do mesmo jeito | L4 | doc:extrato/dobra | G06 vermelho retido | /areas/retencao | FB 1336325419554251_122095715241451002 | IG 18092647964646980 | story e reel publicados nos dois destinos

2026-08-19 | 11h20 | A1 regime | M3 crescendo rápido | ANEXO E FATOR R | A FOLHA DECIDE O ANEXO | Fator R apurado com folha incompleta e janela movel de doze meses | demonstracao aritmetica do mesmo mes no anexo III e no anexo V | Você paga anexo V com uma folha que já dá anexo III | L5 | granito (SUPERFICIE) | G04 noturno operacional | /areas/regime | FB 1336325419554251_122096137107451002 | IG 18144384151503408 | story e reel publicados nos dois destinos

2026-08-19 | 16h13 | G6 devoluções e estornos | M7 fechamento do mês | CHARGEBACK | VENDA DESFEITA | venda desfeita por terceiro que continua viva na apuração do mês | as duas frentes do chargeback (prazo de contestação e competência fiscal) e o erro que se repete | Perdeu a mercadoria, perdeu o valor, e o imposto continuou na base | L2 | doc:extrato/copia (DOCUMENTO) | G03 laranja embalagem | /areas/devolucoes | FB 1336325419554251_122096370201451002 | IG 17978503293072708 | story e reel publicados nos dois destinos

## Rodízio — estado atual
- Total do perfil: 4 posts com log. (A peça A3 repasse / REPASSE DO MÊS,
  de 17-18/08, saiu antes do log existir — considerar A3 e o ponto de
  vazamento REPASSE DO MÊS como usados, e a paleta G01 e o layout L2 também.)
- Áreas usadas: A3/G3 repasse, A8/G5 ads, A4/G9 retenção, A1/G2 regime,
  G6 devoluções e estornos. INTACTAS: G1, G4, G7, G8.
- Momentos usados: M7 fechamento do mês (2x — G3 e G6), M6 investindo em ADS,
  M8 saldo retido, M3 crescendo rápido.
- Pontos de vazamento usados: REPASSE DO MÊS, ADS DA PLATAFORMA, SALDO RETIDO,
  ANEXO E FATOR R, CHARGEBACK.
- Paletas GKFD: G01 azul painel, G02 verde liberado, G03 laranja embalagem,
  G04 noturno operacional, G05 roxo plataforma, G06 vermelho retido.
  Últimas três: G06, G04, G03. Próxima peça sai em G01, G02 ou G05.
- Frases de efeito usadas: CONFERE UMA COISA, ANTES DE SUBIR O ORÇAMENTO,
  O DINHEIRO JÁ É SEU, A FOLHA DECIDE O ANEXO, VENDA DESFEITA.
- Layouts: L1 a L6. Últimos três: L4, L5, L2. Próxima peça sai em L1
  (L3 e L6 seguem vetados por causa do selo de 320px).
- Modo demonstração: usada em 18/08 (ADS) e em 19/08 manhã (Fator R). A peça
  de 19/08 tarde saiu SEM demonstração, com o slide 4 no formato "o erro que
  se repete". A PRÓXIMA peça pode voltar a usar demonstração.
- Sem banco de fotos: fundo sempre gerado (documento numérico + superfície
  neutra). Nada de foto.
- TIPO DE CAPA DAS ÚLTIMAS TRÊS: documento, SUPERFÍCIE (granito), documento
  (extrato/copia). A PRÓXIMA CAPA PODE SER QUALQUER UM DOS DOIS — nunca três
  seguidas do mesmo tipo, e as duas últimas foram tipos diferentes.
- Plataforma citada pelo nome: nenhuma nas peças de 19/08 (ambas dizem
  "a plataforma"). A PRÓXIMA pode citar uma, revezando entre as seis.

## LIÇÕES

**19/08/2026 — DOCUMENTO em slide de VALOR não funciona com o overlay padrão.**
Na primeira renderização o slide 3 usou `doc:comparativo/liso` e o overlay do
array cai em `.18,.34` para os slides de valor — valor pensado para SUPERFÍCIE.
Resultado: a tabela de números atravessou o texto inteiro, ilegível, com o
título e os quatro passos brigando com colunas de cifras. O array de overlay só
tem três entradas e a primeira é a da capa; não há como dar wash pesado a um
documento no miolo sem escurecer as superfícies junto. REGRA: documento só na
CAPA, onde o overlay dedicado protege. Slides de valor sempre em superfície —
foi assim que a peça do Fator R funcionou (granito, linho, concreto, couro, duna).

**19/08/2026 — a família `razao` puxa para o universo errado.**
A capa saiu primeiro com `doc:razao/dobra` e o fundo veio com "Parcela vencida",
"Juros remuneratorios", "Correcao monetaria", "Amortizacao", "Multa contratual".
Não é verba trabalhista como a `liquidacao`, mas é vocabulário de financiamento
e de cálculo judicial, não de marketplace. A lista HIST do `fundo_numerico.py`
é genérica; a lista LANC, que só a família `extrato` usa, é a feita sob medida
para a GKFD — nela aparecem "Repasse de vendas", "Tarifa de servico", "Estorno
de pedido", "Retencao - disputa" e literalmente "Chargeback". Trocado para
`doc:extrato/copia` (papel diferente do extrato/dobra de 18/08) e a capa passou
a reforçar a pauta em vez de apenas decorar. REGRA: em peça sobre repasse,
estorno ou retenção, a capa de documento sai em `extrato`. `razao` e
`comparativo` servem para pauta de escrituração e de margem, não para dinheiro
que a plataforma movimenta.

**19/08/2026 — o L2 protege a headline sozinho, e o wash da capa pode continuar alto.**
O L2 põe um bloco sólido (fundo a 94%) atrás do texto, então dá vontade de
baixar o overlay. Não precisou: com `.74,.84,.93` sobre paleta clara o extrato
continua perfeitamente legível nas bordas da capa — as linhas de lançamento
aparecem acima e abaixo do bloco — e o texto tem contraste total. Padrão
reaproveitável: L2 + documento + `.74,.84,.93` em paleta clara.

**19/08/2026 — concreto e couro leem como a mesma textura em slides vizinhos.**
Slides 3 e 4 saíram em `concreto` e `couro` e no par ficaram os dois cinzas e
rugosos, indistinguíveis ao rolar. Trocado o 4 para `madeira`, que renderiza
claro e com veio direcional. A regra "nunca dois seguidos com a mesma textura"
é sobre o que se VÊ, não sobre o nome do material: conferir olhando os dois
lado a lado.

**19/08/2026 — o L5 tem um filete que atravessa o texto, e a conta é simples.**
No L5 o bloco de texto é centralizado verticalmente e o filete de accent fica
fixo em 58% da altura (y≈783). Na primeira renderização a headline de 3 linhas
com apoio de 6 linhas deixou o filete cortando a primeira linha do apoio, como
se fosse texto riscado. A correção que funcionou foi encurtar o APOIO para 4
linhas (~195 caracteres): o bloco encolhe, recentraliza e o filete cai
exatamente no vão entre a headline e o apoio — vira separador, e parece de
propósito. Regra: no L5, apoio de no máximo 4 linhas. Headline de 3 linhas cabe
desde que o apoio seja curto.

**19/08/2026 — o TRANSBORDO do machine.py não pega tudo.**
O slide 3 saiu dentro do limite (sem aviso de transbordo) e mesmo assim a
segunda linha do rodapé ficou riscada pela barra de progresso do rodapé. O
medidor compara scrollHeight com clientHeight e não enxerga sobreposição de
elementos posicionados. Conferir o rodapé OLHANDO, sempre: título de 2 linhas
mais rodapé de 1 linha é a combinação segura no slide de valor com 4 passos.

**19/08/2026 — capa de superfície em paleta escura resolveu a monotonia.**
Primeira peça em G04 noturno e primeira capa de SUPERFÍCIE (granito), com
overlay .26,.46,.68. Ficou completamente diferente das três capas anteriores,
que eram claras e de documento. A textura continua perceptível sob o wash e o
selo Platinum ganha contraste no fundo escuro. Padrão reaproveitável: quando a
grade estiver clara demais, G04 + superfície + L5.

**19/08/2026 — Fator R exige uma ressalva técnica na própria peça.**
O público da GKFD é vendedor de marketplace, e revenda de mercadoria é Anexo I:
o Fator R não a alcança. A peça só se sustenta se disser isso com todas as
letras — ele decide a receita de SERVIÇO (instalação, montagem, assistência
técnica, gestão de anúncio para terceiros). Entrou no passo 1 do slide 2 e no
rodapé da demonstração. Sem essa linha a peça fica tecnicamente errada para
quem só vende produto.

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


**19/08/2026 — A BASE É O SITE. O banco de áreas foi conformado ao gkfd.com.br.**
Este banco tinha 12 áreas deduzidas por mim. O site oferece 9, com nomes
próprios. Ordem do Fábio: "os sites são a base, não de pitaco, conserte a sua
base". As 12 viraram as 9 do site (G1 a G9), com tabela de correspondência no
banco para o rodízio não perder o histórico. G2, G5 e G9 já rodaram.
DUAS COISAS SAÍRAM: a antiga A12 (prova técnica e disputa com a plataforma) não
consta do site e saiu do rodízio — ela era a ponte para a IntegraJud, e volta se
o Fábio criar a página. E o viés de plataforma: o site atende SEIS (Mercado
Livre, Shopee, Amazon, Magalu e outras) e as peças liam como exclusivas do
Mercado Livre. Regra nova: no máximo uma peça em três cita plataforma pelo nome.
UMA COISA ENTROU: G8 ABERTURA E REGULARIZAÇÃO, que estava no site e faltava aqui.
É a única área que fala com quem AINDA NÃO TEM CONTADOR — todas as outras
pressupõem operação já viciada. Porta de entrada; a peça dela pressupõe dúvida,
não vício.
CHAMADA: passa a ser a do site, "Análise Contábil Inicial Gratuita".
PENDENTE PARA O FÁBIO: a assinatura que ele ditou diz "contabilidade no Simples
Nacional para vendedor de marketplace", e o site diz "contabilidade
especializada em e-commerce", atendendo lojas virtuais além de marketplace. A
assinatura é mais estreita que o site. Não mexi — é palavra dele.


**19/08/2026 — FAIXA DE MARCA NA CAPA, REEL NAS QUATRO, E O QUE MAIS MUDOU.**
Reclamação do Fábio: a peça lia como INFORMAÇÃO e não como serviço. Diagnóstico:
o nome da marca não estava fazendo o trabalho. "GKFD" não diz nada; "IntegraJud"
diz o mundo (jurídico) e não o serviço (perícia contábil).
CONSERTO: a capa ganhou uma FAIXA DE MARCA no topo, largura inteira, com o @ em
cima e o DESCRITOR grande (34px) embaixo — igual ao cabeçalho do site.
A PRIMEIRA TENTATIVA FALHOU e vale registrar: texto solto no canto superior
esquerdo, pequeno (16px). O Fábio: "aumentar a fonte, ninguém enxerga". Ao
aumentar, o texto COBRIU a chamada nos layouts de bloco alto (.retfundo e L2 com
headline de 7 linhas), porque nesses o conteúdo sobe até o topo. Texto solto não
aguenta tamanho. Por isso virou FAIXA ESTRUTURAL: o conteúdo começa abaixo dela
e não existe colisão possível.
TRAVA NOVA: a headline se mede contra a faixa e ENCOLHE sozinha (até 8 passos de
7%) até limpar. Sem isso, uma manchete comprida numa rodada autônoma de domingo
cobriria a chamada e ninguém veria antes de publicar. Falhando, imprime
"capa nao limpou a faixa de marca".
REEL: passa a sair nas QUATRO faixas. Não existe mais faixa sem reel.
BLINDAGEM JUNTO: reel que falhar NÃO derruba a rodada — carrossel e story ficam
publicados, o log recebe "reel falhou", e a ordem passa a ser carrossel, story,
reel por último. O reel é a peça mais frágil e agora está no fim da fila.
BACKUP: machine.py.antes-da-faixa, nas duas pastas.
DESCRITOR DA GKFD: "CONTABILIDADE PARA MARKETPLACE E E\u2011COMMERCE", com hífen
não separável — com hífen comum, "E-COMMERCE" quebrava em duas linhas.
O selo Platinum ficou sobreposto à faixa, como selo aplicado no cabeçalho.
E o descritor CONSERTA o selo: sozinho, o Platinum dizia "vendedor falando com
vendedor"; com o descritor ao lado, lê "contador que também é Mercado Líder
Platinum" — que é a combinação que nenhum concorrente copia.
ASSINATURA ALARGADA (SIM do Fábio): era "contabilidade no Simples Nacional para
vendedor de marketplace", virou "contabilidade especializada em e-commerce e
marketplace". A anterior era mais estreita que o site, que atende loja virtual.


**19/08/2026 — GRAMÁTICA DE ANÚNCIO NA CAPA E NA OFERTA. Miolo intocado.**
Pedido do Fábio, com as palavras dele: "gramática de anúncio, com informação
documental no miolo". Ele mandou dois exemplos de peça comercial e perguntou
se dava para aplicar considerando as paletas. Dava.
O QUE ENTROU NA CAPA: a chamada e a tarja fundiram numa PÍLULA com gradiente e
brilho — dois elementos soltos eram duas vozes, juntos viram selo de pauta.
Rodapé novo com faixa de WhatsApp e tira de três provas. Campo "prova" no
bloco marca.
O QUE ENTROU NO SLIDE 5: a mesma tira de prova, a faixa de marca no topo, e o
selo em tamanho reduzido DENTRO da faixa — em tamanho de capa ele cobria a
ponte, defeito que existia e ninguém tinha visto.
O QUE NÃO MUDOU, DE PROPÓSITO: slides 2, 3 e 4. É lá que mora a densidade que
filtra. A capa para o dedo; o miolo convence. Encurtar o miolo para a peça
ficar mais leve destrói o filtro — quem chega no slide 4 é do nicho.
RUÍDO CORTADO: o exemplo tinha nove blocos na capa. Ficaram cinco. A 400
pixels, que é o tamanho real no feed, o resto vira textura.
AUTOAJUSTE AMPLIADO: a manchete agora se mede contra a faixa em cima E contra
o rodapé embaixo, e encolhe até caber entre os dois. Sem isso, na primeira
rodada autônoma o apoio passaria por baixo da faixa de WhatsApp — aconteceu no
teste e foi assim que o problema apareceu.
LIMITE HONESTO: o visual de anúncio nasce de fundo escuro. Nas paletas claras
ele fica discreto — sem brilho, só borda e contraste. Não é defeito, é física.
Se o Fábio quiser o impacto do exemplo em toda peça, as capas teriam de ficar
só nas paletas escuras, e aí se perde metade da variação que evita monotonia.
NÃO FEITO, E É O MAIOR GANHO QUE FALTA: a foto RECORTADA, com fundo removido,
que existe nos exemplos dele. Isso não sai de CSS — precisa de um PNG com
transparência. Com o arquivo na mão, posicionar é trivial.
BACKUPS: machine.py.antes-da-faixa e machine.py.antes-do-anuncio.

**19/08/2026 — NENHUMA MENÇÃO A CRC. Determinação do Fábio.**
A tira de prova da capa trazia "CONTADOR · CRC". Saiu. Não se escreve CRC,
número de registro nem sigla de conselho em nenhuma peça. Substituído por
"25 ANOS DE EXPERIÊNCIA", que consta do site e é verificável.
É a mesma lógica já aplicada à IntegraJud quanto a credencial jurídica:
registro em conselho não entra na arte.

**19/08/2026 — CAPAS DE DESTAQUE. O story parava de existir em 24h.**
Todo story publicado sumia. Salvo num destaque por área, vira menu
permanente no perfil. O material já era produzido todo dia e ia para o lixo.
A Graph API NÃO cria destaque — não existe endpoint, confirmado. O que dava
para automatizar era a arte: 23 capas, 14 na IntegraJud (P01 preto e ouro) e
9 na GKFD (G04 noturno operacional), uma por área do site.
Arquivos em capas-destaque.zip; o gerador é capas_destaque.py e roda de novo
quando as quatro áreas novas da IntegraJud ganharem página.
ERRO NO CAMINHO: usei hífen não separável para quebrar palavra longa e saiu
"EMPRESA-RIAIS", "PREVIDEN-CIÁRIOS" na arte. Hífen não separável NÃO quebra
linha, ele impede a quebra. Corrigido baixando a fonte de 96 para 74px e
deixando a palavra inteira; PREVIDENCIÁRIOS virou PREVIDÊNCIA.
O RESTO É NO APLICATIVO, uma vez por área: story da área > Destacar > nomear
> Editar destaque > Editar capa > escolher o arquivo. Depois é só somar o
story do dia ao destaque que já existe.

**19/08/2026 — LINK COM ORIGEM, COMENTÁRIO, PRIMEIRA LINHA E ARTIGO.**
Quatro buracos fechados de uma vez, todos de custo zero.
LINKS.PY: as duas marcas usam o mesmo WhatsApp, então nenhum contato era
rastreável. Agora o wa.me leva a mensagem já digitada com marca, formato e
destino. Sem isso a mudança de capa de hoje seria imensurável — e era
justamente o que ia acontecer.
COMENTAR.PY: imagem de feed não clica, e a instrução proíbe "clique" e seta na
arte por isso mesmo. Só que ninguém tinha reparado que a gente publicava sem
deixar link em lugar NENHUM no Instagram. O primeiro comentário resolve.
Fixar não tem endpoint — é no aplicativo, e só nas peças que engrenarem.
PRIMEIRA LINHA DA LEGENDA: é a única que aparece no feed antes do "mais", e
vinha sendo escrita como aquecimento. Regra nova: informação nova e concreta,
escrita por último.
ARTIGO.MD: o texto dos slides 2, 3 e 4 já é um artigo. Passa a ser gravado na
pasta da peça. Quem busca no Google é 100% do nicho e o artigo não expira.

**19/08/2026 — ALT TEXT E REVISITA DE ARQUIVO.**
ALT: a API sempre aceitou alt_text e a gente nunca preencheu. Agora o
publicar_instagram.py lê alt.txt (uma linha por slide) e manda junto. Backup
em publicar_instagram.py.antes-do-alt.
REVISITA: cada peça vivia 48h e morria. revisitar.py republica a capa da peça
mais antiga ainda não revisitada como story, uma por dia, e marca em
.revisitados.txt. Hoje há 25 peças de arquivo na IntegraJud e 5 na GKFD — um
mês de story de graça sobre material já produzido e já revisado.
O story vai para quem JÁ segue, que é o público mais qualificado que existe.
LINKS.PY ganhou o formato "bio", para o link do perfil também ter origem.

**19/08/2026 — PASTA LINKEDIN, substituindo o artigo.md.**
O artigo.md ia nascer dentro da pasta de cada peça. O Fábio pediu pasta
própria, e ele tem razão: uma pasta só, em ordem, sem caçar dentro de pasta
datada. Fica em linkedin/AAAA-MM-DD-tema.md na raiz da marca.
DECISÃO: um texto só, não dois. Post de LinkedIn e artigo de blog são formatos
diferentes, e produzir os dois seria trabalho dobrado sobre o mesmo conteúdo.
O texto sai no formato do LinkedIn e serve para blog com ajuste mínimo.
MOTIVO DE FUNDO: hoje somamos seis itens à rotina. Cada rodada já faz
carrossel, story, reel, duas legendas, alt, comentário, revisita e log. Existe
um ponto em que a rodada fica longa e passa a pular etapa no fim da fila.
Daqui pra frente, TROCAR em vez de empilhar.
REGRA QUE SURPREENDE: sem link no corpo do post. Link externo derruba alcance
no LinkedIn — vai no primeiro comentário, na mão.
As quatro peças de 19/08 já foram escritas e estão na pasta.

**19/08/2026 — LINKEDIN EM PARÁGRAFOS AGRUPADOS. Pedido do Fábio.**
A primeira versão saiu espalhada, com linha em branco entre cada frase. Ele
pediu agrupado e sem espaços. Regravado: blocos densos, cada um fechando uma
ideia, separados por quebra simples. As listas viraram texto corrido.
TEXTO JUSTIFICADO NÃO EXISTE no LinkedIn — a plataforma não tem formatação
nenhuma, é texto puro alinhado à esquerda. Ele pediu, eu não consigo, e isso
fica registrado para nenhuma sessão futura prometer.
Também tirei o acento das hashtags: hashtag acentuada quebra a indexação lá.
As quatro peças de 19/08 foram regravadas no formato novo.

**19/08/2026 — LINKEDIN COM TÍTULO E LINK NO FIM. Requisito do Fábio.**
Título em caixa alta na primeira linha, e o link do WhatsApp fechando o post,
antes das hashtags. Ele decidiu assim e a decisão está tomada — não reabrir.
RESSALVA, que fica registrada e não vira discussão a cada rodada: link no
corpo derruba o alcance no LinkedIn, porque a plataforma não quer tirar gente
de lá. O Fábio foi avisado e escolheu mesmo assim.
O links.py ganhou o destino "linkedin" e o formato "post", então o contato
que vier de lá chega identificado. As quatro peças de 19/08 foram regravadas.

**20/08/2026 — LINK CURTO NO LINKEDIN.**
A mensagem pré-preenchida inteira, codificada, virou uma URL de quatro linhas
na caixa de publicação. Ficou feia e com cara de link suspeito — o Fábio
mandou print. No LinkedIn o texto passa a ser só "Vim do LinkedIn - <tema>":
cabe numa linha e continua rastreável. Nos outros destinos segue a frase longa,
que lá não aparece para ninguém.
O aviso do LinkedIn de que não conseguiu exibir pré-visualização é NORMAL:
ele não gera cartão para link de WhatsApp com parâmetro. Não é erro.

**20/08/2026 — LINKEDIN: LINK VAI NO COMENTÁRIO, NÃO NO POST.**
O Fábio pediu o link no fim do post, viu na tela como ficava, e mudou de
ideia. Decisão final: post limpo, link no primeiro comentário.
O arquivo em linkedin/ passa a sair com DUAS partes separadas por uma linha de
traços: o POST em cima, o COMENTÁRIO embaixo. Ele copia um, publica, copia o
outro, comenta no próprio post. Pode fixar o comentário depois.
DÚVIDA QUE ELE TEVE, e vale registrar: não se "transforma" o endereço em link
no LinkedIn. Cola cru e ele vira clicável sozinho, desde que comece com
https://. Link com texto embutido não existe naquela plataforma.

**20/08/2026 — GRADE NOVA: 14h, 16h, 18h e 20h.**
Definida pelo Fábio. Intercalada: 14h IntegraJud, 16h GKFD, 18h IntegraJud,
20h GKFD. Reel nos quatro.
FAIXAS com 1h45 de tolerância cada: 13h45–15h44 IJ, 15h45–17h44 GKFD,
17h45–19h44 IJ, 19h45–22h00 GKFD. A grade anterior dava só 1h29 na faixa da
tarde, e em 18/08 uma rodada atrasada quase saiu com a marca trocada.
O PAINEL E AS FAIXAS TÊM DE MUDAR JUNTOS. Enquanto o Fábio não trocar os
quatro horários no painel, as tarefas antigas (11h, 12h, 16h, 18h) vão acordar
fora de faixa e PARAR sem produzir. Isso é proposital: parar é melhor do que
publicar na marca errada.
A manhã ficou vazia de propósito. Se um dia incomodar, a alternativa discutida
foi 11-14-17-20, mesma quantidade com o dia mais espalhado.

**20/08/2026 — A TABELA SAIU DO PAINEL. Lição cara.**
A tabela de horários morava dentro do texto colado nas quatro tarefas. Quando
a grade mudou, o arquivo no disco mudou e o painel continuou com a tabela
velha — uma tarefa ainda mandava produzir SEM REEL, regra revogada horas
antes. O Fábio percebeu; eu tinha dito a ele que não precisava mexer no texto,
e estava errado.
CAUSA: texto colado em painel CONGELA. Não recebe correção.
CONSERTO ESTRUTURAL: a tabela virou RELOGIO.txt, idêntico nas duas pastas
(precisa estar nas duas porque é lido ANTES de saber qual marca é). O texto do
painel virou um apontador curto que não contém nenhuma regra que possa mudar.
REGRA PERMANENTE: nada que muda mora no painel. O painel aponta; a verdade
fica no disco.
