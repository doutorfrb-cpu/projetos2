
## PEÇAS PUBLICADAS

DATA | HORA | EIXO | ÁREA | MOMENTO | PEÇA | FRASE | TÓPICO | ÂNGULO | HEADLINE | LAYOUT | CENA DA CAPA | PALETA | DESTINO

2026-08-22 | 23h | 3 | A10 auditoria e compliance | M4 quesitos | QUESITOS | O PERITO JÁ FOI NOMEADO | amostragem apresentada como universo: plano amostral e critério de extrapolação não declarados no laudo | o perito examina 60 de 1.200 lançamentos e a conclusão cobre os 1.200; o quesito é o último momento em que universo, seleção, extrapolação e margem ainda se fixam | O perito vai examinar 60 lançamentos. E concluir sobre 1.200 | L4 | doc:comparativo/dobra (foto do slide 5: px_16978372) | P03 OFF-WHITE CLÁSSICO | /areas/auditoria
  ig_media_id 18081980822302791 · fb_post_id 1164892873373934_122134412355355676
  slide 4 em MODO DEMONSTRAÇÃO (a das 18h não foi): universo 1.200 lançamentos / R$ 6.000.000,00, média R$ 5.000,00; amostra 60 / R$ 300.000,00 com 6 divergentes / R$ 42.000,00; critério A (itens) 10% → 120 × R$ 5.000,00 = R$ 600.000,00; critério B (valor) 14% × R$ 6.000.000,00 = R$ 840.000,00; diferença R$ 240.000,00. Conta conferida.
  story e reel publicados nos dois destinos (extras.py, placar 4/4). Story ig 18098323223457300 · story página 1754814639180270 · reel ig 18218967754332585 · reel página 1768425247730287. Reel 18,7s; saiu "cortando 1.05s de preto do inicio" e os quadros foram conferidos (abertura, três cenas de miolo e fecho) — sem texto cortado.
  PRIMEIRA TENTATIVA DO postar.py FALHOU NOS DOIS: legenda do Instagram com 2615 caracteres (limite 2200) e, no Facebook, "Please reduce the amount of data you're asking for" na hora de montar o post com as 5 fotos. A legenda foi encurtada para 2123 e a segunda tentativa publicou os dois. O erro do Facebook não voltou — foi transitório, e as 5 fotos são reenviadas a cada tentativa.
  comentar.py FALHOU de novo nos dois, mesmos erros: OAuthException 10 no Instagram e OAuthException 200 no Facebook. QUARTA rodada seguida — a permissão de comentário do app na Meta continua pendente.
  reel gerado pelo envelope _reel23.py, que põe a raiz no PATH antes de chamar o reel.py (o ffmpeg.exe está na raiz e o Windows não o acha sozinho).
  LinkedIn gravado em linkedin/2026-08-22-quesitos-amostragem.md. Sem artigo: o artigo é só quarta, e hoje é sábado.
  SEM revisita nesta rodada: a revisita do dia já rodou na peça das 18h e é uma por dia. Esta rodada foi disparada manualmente às 23h47, fora das duas do agendamento.

2026-08-22 | 18h | 2 | A9 marketplace e plataformas | M1 antes da ação | AÇÃO DE EXIGIR CONTAS | ISSO PASSOU BATIDO? | relatório exportado do painel apresentado como prestação de contas, sem débito, crédito e saldo encadeado | vencida a primeira fase, o documento que chega não permite conferir: rubricas agregadas por competência, nenhuma volta ao pedido de venda | Você exigiu contas. Veio um PDF sem débito, crédito e saldo | L2 | doc:extrato/envelhecido (foto do slide 5: px_30857714) | P06 AZUL PETRÓLEO | /areas/marketplace
  ig_media_id 18124628848696225 · fb_post_id 1164892873373934_122134374213355676
  slide 4 SEM demonstração (a das 18h de 21/08 foi): alternância mantida — o slide 4 traz o erro que se repete (estorno sem pedido de origem, antecipação sobre valor já antecipado, campanha e frete em bloco).
  story e reel publicados nos dois destinos (extras.py, placar 4/4). Reel 17,3s; saíram as duas linhas de correção ("cena(s) reduzida(s) para caber: [96]%" e "cortando 1.17s de preto do inicio") e os quadros foram conferidos.
  comentar.py FALHOU de novo nos dois, mesmos erros: OAuthException 10 no Instagram e OAuthException 200 no Facebook. Terceira rodada seguida — a permissão de comentário do app na Meta continua pendente e é a única coisa que impede deixar link no Instagram.
  revisita: rodou (última rodada da marca) e republicou a capa de 2026-08-15_conciliacao-bancaria como story, id 18169369699455931.
  LinkedIn gravado em linkedin/2026-08-22-exigir-contas-plataforma.md. Sem artigo: hoje é sábado, e o artigo é só quarta.
  Não houve rodada das 12h hoje para a IntegraJud — nenhuma pasta de peça de 22/08 existia antes desta.

**22/08/2026 — O REEL PRECISA DO ffmpeg, E ELE NÃO ESTAVA NO PATH.**
O reel.py renderizou o vídeo pelo Playwright e quebrou em seguida, no
`subprocess.run(["ffmpeg", ...])`, com FileNotFoundError [WinError 2]. Não é
defeito do reel.py: nesta máquina o ffmpeg não está em nenhuma pasta do PATH.
Existia solto em C:\Users\fabio\Downloads e uma cópia já tinha sido feita para
gkfd\work22b — ou seja, o problema já apareceu antes e foi contornado sem ficar
registrado.
RESOLVIDO nesta rodada copiando o ffmpeg.exe para a RAIZ da pasta
(postsintegrajud\ffmpeg.exe, 101 MB) e rodando o reel por um envelope que põe a
raiz no PATH antes de chamar o reel.py:
    py _reel22.py        (os dois arquivos ficaram na raiz)
Colocar o exe na raiz NÃO basta sozinho: o Windows desta máquina não procura
executável no diretório atual. É o PATH que resolve.
O DEFINITIVO seria instalar o ffmpeg e colocá-lo no PATH do sistema, ou o
reel.py aceitar um caminho explícito. Enquanto isso não acontece, toda sessão
que gerar reel precisa do envelope — e sem ele a rodada perde o reel em
silêncio, depois de já ter gasto o render.

2026-08-21 | 18h | 1 | A6 previdenciários | M7 sentença e liquidação | IMPUGNAÇÃO AOS CÁLCULOS | A CONTA VEIO PRONTA | atrasados com termo inicial e critério de correção divergentes do julgado | ganhou a ação e a planilha do executado desloca o marco e aplica índice único; impugnar sem apresentar conta devolve o arbítrio ao juízo | Você ganhou. Os atrasados vieram por outro índice | L1 | doc:liquidacao/formulario (foto do slide 5: px_5807057) | P04 SÉPIA ESCURO | /areas/previdenciarios
  ig_media_id 18016217147942741 · fb_post_id 1164892873373934_122134079625355676
  slide 4 em MODO DEMONSTRAÇÃO (o das 14h não foi): R$ 900,00/mês, 24 comp. → R$ 25.488,00 contra 18 comp. → R$ 17.334,00, diferença R$ 8.154,00. Conta conferida.
  story e reel publicados nos dois destinos (extras.py, placar 4/4). Reel 19,25s; saíram as duas linhas de correção ("cena(s) reduzida(s) para caber: [94]%" e "cortando 1.37s de preto do inicio") e o mp4 foi conferido quadro a quadro.
  comentar.py FALHOU de novo nos dois, mesmos erros de ontem: OAuthException 10 no Instagram e OAuthException 200 no Facebook. Peça publicada, nada desfeito. É permissão do app, e agora são duas rodadas seguidas — vale pedir a permissão de comentário no app da Meta.
  revisita: rodou (é a última rodada da marca) e republicou a capa de 2026-08-15_avaliacao-imovel como story, id 18414317125157582.
  LinkedIn gravado em linkedin/2026-08-21-atrasados-indice-termo-inicial.md. Sem artigo: hoje é sexta, e o artigo é só quarta.

**21/08/2026, rodada das 18h — L3 NÃO SERVE MAIS PARA CAPA COM RODAPÉ DE ANÚNCIO.**
A capa saiu primeiro em L3 e a linha de apoio veio impressa POR BAIXO da faixa de
WhatsApp e da tira de prova, ilegível. Não é tamanho de texto: `.L3 .apoio` é
`position:absolute; bottom:120px`, que é exatamente onde mora o rodapé de anúncio
criado em 19/08. Encurtar headline e apoio não resolveu, e o gerador não avisou —
o medidor ignora quem está fora do fluxo, e aqui os DOIS elementos são absolutos,
então não há sobreposição que ele possa detectar.
Trocado para L1, que deixa o apoio no fluxo, e a capa limpou.
ENQUANTO NÃO FOR CORRIGIDO NO CÓDIGO: não use L3 na capa. E vale conferir L5,
que também pode ter posicionamento próprio de apoio.
É o mesmo padrão de 20/08 no slide 3: elemento absoluto não empurra nada, e por
isso passa pelo medidor e sai riscado. A regra pegou o caso do fluxo; este é o
caso de absoluto contra absoluto, que ela não cobre.

2026-08-21 | 14h | 1 | A3 financeiros | M3 contestação | CONTESTAÇÃO | LEIA O DEMONSTRATIVO | amortização negativa: parcela inferior ao juro do período | pagou em dia e o saldo subiu; contestação alega excesso sem apontar o valor certo | Pagou em dia. E o saldo devedor subiu | L6 | doc:razao/copia (foto do slide 5: px_9852063) | P02 GRAFITE E ÂMBAR | /areas/financeiros
  ig_media_id 18101334917580364 · fb_post_id 1164892873373934_122133995769355676
  story e reel publicados nos dois destinos (extras.py, placar 4/4)
  comentar.py FALHOU nos dois: OAuthException 10 no Instagram ("Application does not have permission for this action") e OAuthException 200 no Facebook. Peça publicada, nada desfeito. É permissão do app, não do post.
  LinkedIn gravado em linkedin/2026-08-21-amortizacao-negativa.md
  Sem revisita e sem artigo: revisita é da ÚLTIMA rodada da marca (18h) e o artigo é só quarta.

**21/08/2026 — ATENÇÃO: este arquivo perdeu as linhas de peça.**
Ao ler o log hoje, a seção de peças estava vazia — só decisões. A versão commitada
em 20/08 às 23h50 já estava assim, então a perda é anterior e não veio desta
rodada. A antirrepetição desta peça foi reconstruída pelos spec.json das
subpastas datadas (que guardam layout, paleta, frase, peça e cenas) e pelo
_work/_LIXO-log-antigo-NAO-USAR.md, que é histórico e está desatualizado.
Vale reconstruir a lista completa: sem ela, headline repetida vira questão de tempo.

**21/08/2026 — o artigo semanal passa para QUARTA, decisão do Fábio.**
Era sexta, virou quarta, na mesma rodada das 18h. Meio de semana é dia mais
forte de leitura profissional no LinkedIn que sexta — a escolha dele foi
melhor que a minha.
A capa deitada foi aprovada por ele: "ficou ótima".

**21/08/2026 — A IDENTIDADE É DA EMPRESA. NENHUM NOME PESSOAL NA ARTE.**
Determinação do Fábio, e ele já tinha dito antes: "a identidade é da empresa".

O QUE SAÍA ERRADO, em seis lugares vivos:
  reel.py .......... assinatura padrão com nome e cargo pessoais
  machine.py ....... MK_NOME e MK_CARGO ao lado do retrato
  capa_artigo.py ... rodapé fixo com o nome
  bloco marca GKFD . campo "site" com o NOME dentro
  assinatura GKFD .. segunda linha com nome e cargo
  assinatura IJ .... primeira linha com nome e cargo

AGORA: a assinatura é só a marca, nas duas.
  IntegraJud / Inteligência pericial para advocacia
  GKFD Contábil / Contabilidade especializada em e-commerce e marketplace

CONTINUAM, porque são credencial da casa e não nome de pessoa: o selo Mercado
Líder Platinum e o "25 anos de experiência" da tira de prova.

O PIOR DELES, e vale entender a mecânica: o campo "site" da GKFD estava com
"Fábio Rebouças — Contador" dentro. Foi improviso meu de quando a GKFD ainda
não tinha site conhecido — eu preenchi para não deixar vazio. Depois
descobrimos o gkfd.com.br, analisamos o site inteiro, conformamos os dois
bancos de área a ele — e ninguém voltou nesse campo.
Resultado: o reel e o slide de oferta imprimiam o NOME em negrito, 56px, no
lugar do ENDEREÇO. E ainda repetiam o nome logo abaixo, na assinatura.
Agora o campo é www.gkfd.com.br e o cta é "Análise contábil inicial gratuita
em", que é a chamada do próprio site.

LIÇÃO: campo preenchido por improviso vira defeito permanente quando ninguém
revisita. Toda vez que uma informação nova entrar na operação — um site, um
endereço, uma credencial — varrer os campos que foram preenchidos ANTES dela
existir. É a terceira vez esta semana que um resto de improviso aparece:
o log copiado no _work, as fontes só no rascunho, e agora este.

BACKUPS: *.antes-do-nome nos três scripts de cada marca.
