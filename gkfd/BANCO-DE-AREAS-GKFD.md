# BANCO DE ÁREAS — GKFD
### Contabilidade consultiva para marketplace · auditoria de recebíveis · recuperação de valores · inteligência de margem

**Remontado em 18/08/2026, a partir dos 90 tópicos de dor ditados pelo Fábio.**
A versão anterior deste arquivo foi descartada inteira. Ela tinha sido deduzida
por mim, e estava errada no essencial: tratava a GKFD como escritório de
contabilidade que também atende e-commerce. Não é. O que segue vem de quem
opera a plataforma por dentro.

---

## O QUE MUDOU, E POR QUE ISSO GOVERNA TODA PEÇA

A versão velha vendia **apuração correta**. Contador nenhum se diferencia por
isso — todo escritório diz que apura certo.

O eixo verdadeiro é outro, e foi o Fábio quem nomeou:

> **Contabilidade Consultiva para Marketplaces + Auditoria de Recebíveis +
> Recuperação de Valores + Inteligência de Margem.**

Quatro pilares. Os dois do meio não existem no escritório comum, e são os que
fazem o vendedor parar de rolar o feed: **alguém está conferindo se o dinheiro
que era seu chegou, e indo buscar o que não chegou.**

| | escritório comum | GKFD |
|---|---|---|
| o que entrega | guia paga, obrigação cumprida | onde o dinheiro vazou e quanto dá para trazer de volta |
| como olha o repasse | total do mês, uma linha | linha a linha, contra pedido, nota e extrato |
| o que devolve | balancete | margem por SKU e por canal, e memória de cálculo auditável |
| quem é | prestador de obrigação acessória | quem opera a plataforma e sabe onde ela cobra errado |

---

## OS QUATRO PILARES

### PILAR 1 · TRIBUTÁRIO CONSULTIVO
Não é "fazer a apuração". É **decidir o regime e a base com simulação
econômica**, e revisar antes que o erro acumule doze meses.

### PILAR 2 · AUDITORIA DE RECEBÍVEIS
Cruzar pedido → nota → entrega → repasse → banco. É aqui que aparecem os
centavos descontados milhares de vezes, o frete cobrado errado, o saldo retido
sem justificativa, o chargeback que ninguém contestou.

### PILAR 3 · RECUPERAÇÃO DE VALORES
O que a auditoria encontra vira pedido: restituição de tributo pago a maior,
ressarcimento logístico nunca cobrado, cobrança indevida da plataforma. E,
quando o caso vai para o Judiciário, vira **memória de cálculo auditável**.

### PILAR 4 · INTELIGÊNCIA DE MARGEM
DRE por canal e por SKU, ponto de equilíbrio, custo total da venda, ACOS
lido depois de imposto. Responder a pergunta que quase nenhum vendedor sabe
responder: **este produto dá lucro?**

---

## O TERCEIRO EIXO — O PONTO DE VAZAMENTO

Na IntegraJud é a peça processual, e vai na tarja da capa porque o advogado
reconhece o nome do que está aberto na tela dele.

Aqui **não é o documento** — foi esse o erro da versão anterior. É o **ponto
de vazamento**: o lugar exato por onde o dinheiro sai. O vendedor não reconhece
"PGDAS-D"; ele reconhece "SALDO RETIDO", "CHARGEBACK", "ADS", "DEVOLUÇÃO".

Cada linha traz: o ponto de vazamento · a conta que ele exige · **o buraco, que
é de onde sai a headline**.

| tarja | a conta que ela exige | o buraco |
|---|---|---|
| **REPASSE DO MÊS** | venda × tarifa × frete × ADS × líquido creditado | a receita é lançada pelo bruto e o imposto corre sobre valor que nunca foi repassado |
| **SALDO RETIDO** | composição do bloqueado, disponível e a liberar | saldo preso tributado como receita realizada, e capital de giro parado sem prazo |
| **CHARGEBACK** | contestação, prazo e resultado, pedido a pedido | contestação não auditada: perde por decurso de prazo e ninguém registra |
| **DEVOLUÇÃO** | nota de entrada, retorno físico e ajuste financeiro | mercadoria voltou, cliente foi reembolsado, e a receita continua na apuração |
| **ESTORNO** | vínculo entre o estorno e a venda de origem | estorno lançado solto, sem baixar a venda que o originou |
| **TARIFA E COMISSÃO** | percentual contratado × percentual praticado, com vigência | comissão alterada sem data demonstrada, aplicada retroativamente |
| **FRETE** | tabela contratada × valor debitado, por pedido | frete subsidiado debitado sem vínculo com o pedido de origem |
| **ADS DA PLATAFORMA** | custo da campanha × margem líquida do que ela vendeu | ACOS bonito e prejuízo real, porque ninguém tirou imposto e tarifa antes |
| **EXTRAVIO E AVARIA** | ressarcimento devido × ressarcimento pago | indenização paga a preço de custo antigo, ou nunca pedida |
| **ANTECIPAÇÃO DE RECEBÍVEL** | custo financeiro isolado da receita | antecipação lançada como desconto de venda, distorcendo a base de cálculo |
| **DIFAL** | alíquota interestadual e partilha, venda a venda | vende para o Brasil inteiro e apura como se fosse tudo operação interna |
| **ICMS-ST** | o que já veio com imposto retido na entrada | produto com ST tributado de novo na saída, e ressarcimento não pedido |
| **ANEXO E FATOR R** | folha × receita dos últimos doze meses | anexo V pago quando a folha já colocava a empresa no III |
| **REGIME TRIBUTÁRIO** | Simples × Presumido × Real, com simulação | cresceu e ficou no regime errado, pagando a diferença todo mês |
| **INVENTÁRIO** | estoque físico × estoque da plataforma × Bloco H | estoque no papel que não bate com o galpão nem com o fulfillment |
| **DRE POR CANAL** | resultado por plataforma, com tarifa e frete alocados | o canal que mais fatura é o que mais dá prejuízo, e a decisão é tomada pelo faturamento |
| **PREÇO** | custo total da venda, incluindo comissão, imposto, frete, ADS e devolução | preço formado olhando o concorrente, sem saber o próprio piso |
| **BLOQUEIO DE CONTA** | faturamento perdido no período, com base histórica | prejuízo alegado sem cálculo, e por isso não indenizado |
| **CONCILIAÇÃO ERP × PLATAFORMA** | pedido → NF-e → entrega → repasse → banco | quatro sistemas com quatro verdades, e ninguém sabe qual é a certa |
| **MALHA E INTIMAÇÃO** | resposta com memória de cálculo e conciliação | responder sem a conciliação repasse × nota é confessar a diferença |

---

## AS ÁREAS

### A1 · REGIME, ANEXO E CARGA TRIBUTÁRIA
`/areas/regime`
Exposição típica: a empresa cresceu e continua pagando pelo enquadramento de
quando era pequena.

- Simples Nacional enquadrado de forma inadequada para operação de marketplace
- Anexo e alíquota efetiva aplicados sem conferir a atividade real
- Fator R apurado sem considerar pró-labore e encargos dos doze meses
- Simples × Lucro Presumido × Lucro Real decidido sem simulação econômica
- Empresa crescendo e permanecendo no regime errado, mês após mês
- CNAE que não descreve a operação e empurra para o anexo caro
- Ausência de revisão tributária periódica — o erro que se acumula em silêncio
- Sublimite estadual estourado sem ninguém perceber

### A2 · BASE DE CÁLCULO E RECEITA APURADA
`/areas/base-de-calculo`
Exposição típica: o imposto é calculado sobre um número que não é o da empresa.

- Faturamento do marketplace diferente da receita efetivamente recebida
- Imposto pago sobre valores cancelados ou devolvidos
- Tributação sobre vendas estornadas
- Receita lançada pelo painel da plataforma em vez da escrituração
- Notas fiscais divergentes das vendas efetivamente realizadas
- Vendas duplicadas e lançamentos duplicados inflando a base
- Antecipação de recebível lançada como desconto de venda
- Receita de frete cobrado do comprador tratada como receita própria

### A3 · REPASSE, TARIFA E COMISSÃO
`/areas/repasse`
Exposição típica: entre o valor da venda e o valor que cai na conta há uma
diferença que ninguém abre.

- Comissões cobradas pelo marketplace sem nenhuma conferência
- Tarifas e taxas divergentes do que foi contratado
- Fretes cobrados ou descontados incorretamente
- Diferença entre valor vendido, valor liquidado e valor recebido
- Extrato do marketplace que não fecha com a contabilidade
- Conta bancária que não fecha com os relatórios das plataformas
- Valores pequenos descontados milhares de vezes, sem auditoria
- Perdas invisíveis pelo volume: cada uma é irrelevante, a soma não é
- Conciliação de milhares de transações feita manualmente

### A4 · RETENÇÃO, BLOQUEIO E CAPITAL DE GIRO
`/areas/retencao`
Exposição típica: o dinheiro existe, é seu, e você não pode usar.

- Valores retidos pelo marketplace sem composição demonstrada
- Saldo bloqueado ou indisponível sem justificativa clara nem prazo
- Recebíveis que simplesmente não chegaram à conta
- Capital de giro preso dentro da plataforma
- Dependência de antecipação para manter a operação de pé
- Antecipação de recebíveis com custo financeiro desconhecido
- Empréstimo oferecido pela própria plataforma consumindo a margem
- Ausência de auditoria histórica dos recebíveis

### A5 · DEVOLUÇÃO, ESTORNO E CHARGEBACK
`/areas/devolucao`
Exposição típica: a mercadoria voltou, o dinheiro saiu, e a contabilidade não
soube de nada.

- Devoluções sem conciliação contábil, fiscal e financeira
- Mercadoria devolvida sem o correspondente ajuste financeiro
- Reembolso ao comprador sem conferência do retorno da mercadoria
- NF-e de devolução ausente ou incorreta
- Chargebacks e contestações sem auditoria de prazo e resultado
- Cancelamentos que continuam impactando o financeiro meses depois
- Estornos sem conciliação com a venda de origem
- Pedidos sem correspondência financeira, e recebimentos sem pedido

### A6 · ST, DIFAL E CRÉDITOS
`/areas/st-difal`
Exposição típica: vende para o Brasil inteiro e apura como se fosse tudo local.

- DIFAL calculado ou recolhido incorretamente
- ICMS-ST pago indevidamente, e ressarcimento nunca pedido
- Produto com ST na entrada tributado de novo na saída
- Créditos tributários esquecidos dentro da operação
- Retenções tributárias não recuperadas
- CT-e e custos logísticos fora da apuração
- Identificação de cobranças que fundamentam pedido de restituição

### A7 · MARGEM, PREÇO E PONTO DE EQUILÍBRIO
`/areas/margem`
Exposição típica: fatura alto, e ninguém sabe se sobra.

- Margem real desconhecida depois de impostos e taxas
- Produto que vende muito e dá pouco ou nenhum lucro
- Precificação sem considerar comissão, imposto, frete, ADS e devolução
- Desconhecimento do custo total de cada venda
- Falta de cálculo do ponto de equilíbrio da operação
- Preço definido olhando apenas o concorrente
- Promoções que aumentam faturamento e destroem margem
- Cupons e descontos sem análise do impacto tributário e financeiro
- Falta de indicadores para saber onde a operação perde dinheiro

### A8 · ADS E CUSTO DE MÍDIA
`/areas/ads`
Exposição típica: a campanha parece lucrativa até alguém tirar imposto e tarifa.

- ADS consumindo margem sem cálculo do lucro líquido da campanha
- ACOS e ROAS analisados sem considerar tributação e margem líquida
- Campanha aparentemente lucrativa que gera prejuízo depois dos custos
- Cashback e incentivos sem conciliação
- Bonificações da plataforma não identificadas nem contabilizadas
- Publicidade rateada por faturamento em vez de por origem da venda

### A9 · DRE POR CANAL E POR SKU
`/areas/resultado`
Exposição típica: três plataformas tratadas como se fossem a mesma coisa.

- Falta de DRE específica por marketplace
- Falta de DRE por produto e por SKU
- Falta de rentabilidade individual por canal de venda
- Mercado Livre, Shopee e Amazon tratados contabilmente como iguais
- Falta de conciliação separada por marketplace
- Falta de acompanhamento de margem por SKU
- Tarifa e frete não alocados por canal

### A10 · LOGÍSTICA, ESTOQUE E RESSARCIMENTO
`/areas/logistica`
Exposição típica: o estoque some dentro do fulfillment e ninguém cobra.

- Mercadoria extraviada sem ressarcimento
- Produto avariado dentro da logística da plataforma
- Ressarcimentos logísticos que nunca foram cobrados
- Valores de indenização inferiores ao efetivamente devido
- Estoque físico diferente do estoque apresentado pela plataforma
- Estoque parado consumindo capital de giro
- Inventário e Bloco H sem lastro de entradas e saídas

### A11 · INTEGRAÇÃO E RASTREABILIDADE
`/areas/integracao`
Exposição típica: quatro sistemas, quatro verdades, nenhuma conferida.

- Erros fiscais causados pela integração ERP × marketplace
- Diferenças entre ERP, marketplace, banco e contabilidade
- Falta de rastreabilidade entre pedido → NF-e → entrega → recebimento
- Auditoria de milhares de lançamentos para localizar diferenças
- Cruzamento automatizado de pedidos, notas, extratos e recebíveis

### A12 · PROVA TÉCNICA E DISPUTA COM A PLATAFORMA
`/areas/prova-tecnica`
Exposição típica: sabe que perdeu dinheiro, e não consegue provar quanto.

- Bloqueio de conta causando perda de faturamento mensurável
- Suspensão de anúncio ou queda de reputação com prejuízo real
- Ausência de cálculo técnico do prejuízo causado por bloqueios
- Falta de documentação técnica para contestar cobranças da plataforma
- Falta de prova contábil para processos contra plataformas
- Lucros cessantes sem cálculo técnico
- Danos emergentes sem documentação contábil organizada
- Auditoria de contratos e condições comerciais das plataformas
- Quantificação técnica de valores para eventual cobrança judicial
- Produção de memória de cálculo para o jurídico
- Transformação de milhares de lançamentos em prova técnica auditável

**Esta área é a ponte com a IntegraJud, e vale entender a diferença:** aqui o
cliente é o **vendedor**, e o advogado dele é quem recebe a memória de cálculo.
Na IntegraJud o cliente é o **advogado**. Mesma competência técnica, dois
compradores diferentes. Nunca misturar as duas marcas na mesma peça.

---

## MOMENTOS DO VENDEDOR

Área × momento = pauta diferente. É o segundo eixo do rodízio.

| # | Momento | O que está em jogo |
|---|---|---|
| M1 | Antes de abrir | o enquadramento que define o custo dos próximos anos |
| M2 | Primeiro mês vendendo | a nota e a apuração inaugurais |
| M3 | Crescendo rápido | a faixa que muda e a alíquota que sobe junto |
| M4 | Entrando no fulfillment | estoque em poder de terceiro, extravio e avaria |
| M5 | Abrindo em segunda plataforma | conciliação separada, e canal que dá prejuízo |
| M6 | Investindo em ADS | margem líquida da campanha, não o ROAS da tela |
| M7 | Fechamento do mês | conciliação antes do DAS |
| M8 | Saldo retido ou conta bloqueada | capital preso e prejuízo a quantificar |
| M9 | Caiu na malha | responder com memória de cálculo, não com alegação |
| M10 | Trocando de contador | o que herda, o que refaz e o que dá para recuperar do passado |

**Regra numérica:** não repetir a mesma combinação área × momento em menos de
20 peças, nem o mesmo ponto de vazamento em menos de 8.

---

## O QUE NUNCA ENTRA

Contador tem regra de publicidade profissional, e aqui há um agravante: parte
do que a GKFD faz toca matéria jurídica.

- percentual de economia tributária, ainda que médio ou "de até"
- "reduza seus impostos", "pague menos imposto legalmente"
- comparação com o contador atual do cliente, mesmo indireta
- preço, tabela ou mensalidade em arte de post
- print de cliente, faturamento de cliente, caso identificável
- promessa de resultado em fiscalização, em disputa ou em recuperação

### A REGRA DA RESTITUIÇÃO EM DOBRO — determinada pelo Fábio

**Nunca anunciar "devolução em dobro" como resultado garantido.** É forte
comercialmente e é justamente por isso que é perigoso.

A formulação autorizada, e é para usar esta:

> "Identificamos cobranças e retenções indevidas e produzimos a apuração
> técnica necessária para buscar restituição, inclusive em dobro quando houver
> fundamento jurídico aplicável."

Repare no que ela faz: promete o **trabalho técnico**, que é o que a GKFD
entrega de fato, e devolve ao Direito o que é do Direito. A GKFD apura; quem
diz se cabe dobro é o advogado do cliente, no caso concreto.

**O que entrega o mesmo sem prometer nada:** a demonstração aritmética. Em vez
de "economize até 30%", mostrar que a mesma receita, no anexo III e no V, dá
dois DAS diferentes — e a diferença é conta, não promessa.

---

## A ASSINATURA

    GKFD Contábil — contabilidade no Simples Nacional para vendedor de marketplace
    Fábio Rebouças — Contador · Mercado Líder Platinum

O selo Mercado Líder Platinum entra em toda peça, conforme a seção 8-B da
instrução. É a única credencial desta operação que nenhum concorrente pode
copiar: qualquer escritório diz que atende e-commerce, nenhum exibe reputação
de vendedor.

Nunca usar a assinatura da IntegraJud aqui, nem a palavra "perícia".
