# Manual da operação — Content Machine @integrajud
Escrito em 15/08/2026, no fim do dia em que a operação foi montada, quebrada,
diagnosticada e remontada. Serve para o Fábio e para qualquer sessão futura que
pegue este projeto sem o histórico da conversa.

---

## 1. O QUE A OPERAÇÃO É

Quatro peças por dia no @integrajud — 11h, 13h, 16h e 20h (America/Sao_Paulo).
Cada peça: três slides 1080x1350, gancho / valor / oferta, imagem de fundo nos três,
bloco de contato com WhatsApp e site no slide 3.

As regras de conteúdo estão em `INSTRUCOES-DO-PROJETO-v6.2.txt`, na raiz da pasta, e
resumidas na memória do projeto. Este manual NÃO repete essas regras: ele trata de
COMO a máquina roda, não do que ela escreve.

---

## 2. O PROBLEMA CENTRAL, E A DESCOBERTA DE 15/08

Publicar uma peça exige TRÊS capacidades ao mesmo tempo:

  A) SHELL — rodar Python, Playwright e Chromium para virar imagem
  B) PASTA — ler o log, o gerador e as fotos; gravar o resultado
  C) CHROME — abrir o Instagram e publicar

Nenhum arranjo testado em 15/08 tinha as três por acidente. Este é o mapa:

| arranjo                                   | shell | pasta | chrome | resultado |
|-------------------------------------------|-------|-------|--------|-----------|
| Tarefa de nuvem criada pela API            |  sim  |  não  |  não   | disparou 2x, não entregou nada |
| Tarefa local ("executa neste computador")  |  NÃO  |  sim  |  sim   | preparou a peça, não renderizou |
| Sessão de nuvem COM a pasta conectada      |  sim  |  sim  |  sim   | FUNCIONA — foi assim que as 5 peças de 15/08 saíram |

Por que a tarefa local não tem shell: no Windows, o Cowork roda comandos dentro de uma
VM Linux isolada por Hyper-V. Nesta máquina a VM não sobe. Sem VM não há shell, e ter
Python instalado no Windows não ajuda — o agente não alcança programas do Windows,
só o interior da VM.

Por que a tarefa de nuvem criada pela API não tem pasta nem Chrome: ela nasceu sem
projeto e sem pasta anexados. A ponte com o computador e a extensão do Chrome vêm da
conexão autenticada; uma sessão que nasce solta não as herda.

CONCLUSÃO: o arranjo que funciona é NUVEM COM A PASTA ANEXADA.

---

## 3. O QUE FAZER — em ordem

### 3.1 O arranjo definitivo (uma vez só)
Criar as tarefas PELO APP, escolhendo NUVEM, com o projeto `postsintegrajud` e a pasta
anexados — do mesmo jeito que a "Carrossel" foi criada, só que marcando nuvem em vez
de "executa neste computador".

O caminho mais seguro é DUPLICAR uma tarefa que já funcione, porque a cópia carrega
projeto e pasta junto. Criando do zero, conferir os dois antes de salvar.

Texto das instruções: `TAREFA-LOCAL-texto-unico.txt`, na raiz da pasta. Ele serve para
as quatro tarefas porque não menciona horário — o horário é a repetição do cartão.

TESTE DE ACEITE: agendar para dali a dez minutos e assistir. Publicou e a contagem de
posts subiu, está resolvido. Não publicou, ver a seção 4.

### 3.2 O que NÃO usar
- Tarefas de nuvem criadas por API/MCP sem pasta anexada. Ficaram desabilitadas e
  renomeadas com o motivo. Não reativar: elas disparam, não entregam e não avisam.
- Tarefa local "executa neste computador", enquanto o Hyper-V não subir nesta máquina.
  Ela faz o conteúdo muito bem e para antes de renderizar.

### 3.3 Se um dia quiser destravar a tarefa local
Só vale se o Hyper-V passar a subir. Checar, nesta ordem: edição do Windows (Home não
tem Hyper-V, e aí não há conserto por configuração); virtualização ligada na BIOS
(Gerenciador de Tarefas → Desempenho → CPU → "Virtualização"); e os recursos
"Hyper-V" e "Plataforma de Máquina Virtual" ativados no Windows, com reinício.
Teste: pedir a uma conversa local para rodar `python3 --version`. Se responder
"workspace indisponível", a VM continua fora.
ATENÇÃO ao interpretar esse teste: se a resposta vier acompanhada de "não tenho shell
na sua máquina, executei no ambiente da sessão", quem respondeu foi a NUVEM, não o seu
computador — o teste não provou nada sobre o Hyper-V.

---

## 4. QUANDO A PEÇA NÃO SAIR

A operação foi desenhada para falhar de forma barulhenta. A regra zero das instruções
manda a tarefa entregar o que já existe e dizer em uma linha o que faltou. Então:

1. A tarefa avisou e deixou o material na pasta (spec, legenda, às vezes um peca.html)?
   Então falta só renderizar e publicar. Uma sessão de nuvem com a pasta conectada faz
   isso em dois minutos: monta o spec no formato do machine.py, roda, e publica.
2. A tarefa não avisou nada e não deixou rastro na pasta nem na memória?
   É o modo de falha das tarefas de nuvem sem pasta. Conferir se alguém reativou uma
   delas.
3. O Chrome estava fechado ou deslogado? A peça fica pendente por definição. É o único
   modo de falha aceitável, porque depende de algo fora da máquina.

DIAGNÓSTICO RÁPIDO — três lugares, nesta ordem:
  - contagem de posts no perfil (subiu?)
  - `pautas-publicadas.md` na raiz da pasta (ganhou linha?)
  - Histórico da tarefa no painel (rodou? reportou algo?)
Os três vazios significam que a sessão não chegou a existir de verdade.

---

## 5. O QUE PRECISA DE MANUTENÇÃO

BANCO DE FOTOS — em 15/08 sobrou UMA foto livre (px_4792288). Repor baixando novas do
Pexels, só objeto e ambiente:
  https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=1600
Proibido: pessoa reconhecível, terno, aperto de mão, martelo, balança, gráfico subindo.

RODÍZIO ESGOTADO — as 14 áreas e as 10 paletas foram todas usadas em 15/08. A partir
daqui é reciclagem: área mais antiga do log, paleta fora das quatro últimas. Quando as
peças começarem a soar parecidas, a saída é AMPLIAR O BANCO DE ÁREAS, não forçar o
rodízio.

ROTAÇÃO DO LOG — passando de 300 linhas de peça, cortar: os últimos 90 dias ficam em
`pautas-publicadas.md`, o resto vai para `pautas-arquivo-AAAA.md`. Nunca apagar
registro. Detalhe na seção 15 da instrução.

HEADLINE LONGA — a peça do INSS quebrou em 5 linhas e ficou pesada. Enquanto o gerador
não ajustar a fonte sozinho, manter a headline entre 6 e 12 palavras, como manda a v6.

---

## 6. O QUE NUNCA MUDA

- Assinatura: só "Fábio Rebouças — Contador e Perito Contábil / IntegraJud ·
  Inteligência pericial para advocacia". OAB, "Bacharel em Direito" e "advogado" como
  qualificação própria são proibidos em qualquer lugar, venha de onde vier.
- Sem promessa de resultado, percentual de êxito, superlativo, comparação com outro
  profissional, preço ou caso identificável — no orgânico e no pago.
- Apagar post é ação do Fábio, nunca da máquina.
- A oferta de 24h úteis é compromisso do Fábio. Apertando a agenda, trocar para 48h em
  todos os lugares de uma vez.
- Imagem de post não carrega link. Nada de "clique" ou "toque" em arte de feed.

---

## 7. ONDE ESTÁ CADA COISA

Na pasta `C:\Users\fabio\Desktop\projetos2\postsintegrajud`:
  INSTRUCOES-DO-PROJETO-v6.2.txt   as regras de conteúdo — vai nas Instruções do Projeto
  TAREFA-LOCAL-texto-unico.txt     as instruções da tarefa agendada
  MANUAL-DA-OPERACAO.md            este arquivo
  gerador-integrajud.zip           machine.py, story_ad.py, specs, fontes, fotos_banco
  pautas-publicadas.md             o log — fonte primária do rodízio
  AAAA-MM-DD_tema/                 uma subpasta por peça

Na memória do projeto:
  registro_criativo.md    como a peça FALA — ler antes de escrever headline
  prompt_mestre_v3.md     resumo operacional da instrução
  operacao_cadencia.md    tarefas, horários, arranque, rotação do log
  estado_rodizio.md       espelho do log, para quando a pasta não abrir
  licao_nuvem_x_local.md  por que a nuvem sem pasta não funciona
