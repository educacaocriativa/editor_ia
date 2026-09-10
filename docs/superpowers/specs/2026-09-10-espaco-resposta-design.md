# Verificação do Espaço de Resposta — Design

## Problema

O Editor IA não verifica se o espaço reservado para o aluno responder uma
atividade (linhas em branco após o enunciado) é suficiente para o tipo de
resposta esperado. Essa informação nunca chega à camada de revisão porque
`word/extractor.py` descarta todo parágrafo vazio ao montar o texto que é
enviado à IA.

## Escopo

- Aplica-se apenas a arquivos `.docx` (PDFs não preservam parágrafos vazios
  de forma confiável na extração atual e ficam fora deste escopo).
- Considera apenas o formato de espaço de resposta confirmado pelo usuário:
  linhas em branco (parágrafos vazios) após o enunciado. Caixas de texto e
  células de tabela com altura fixa ficam fora do escopo por ora.
- Reporta apenas espaço **insuficiente**. Espaço excessivo não é sinalizado
  nesta primeira versão (menor risco, ninguém reportou esse caso).
- É uma verificação de **alerta no relatório**, não edita o `.docx` revisado
  automaticamente — cabe ao revisor humano decidir se adiciona linhas.
- Julgamento de "quantas linhas são suficientes" é contextual pela IA (tipo
  de pergunta + faixa etária do perfil), sem tabela fixa de regras.

## Mudanças

### 1. `word/extractor.py`

`extrair_paragrafos()` passa a rastrear quantos parágrafos vazios
consecutivos existem imediatamente após cada parágrafo com texto, guardando
em `linhas_em_branco_apos` (int, default 0). Mantém `indice` com a mesma
semântica de hoje (posição original no `doc.paragraphs`) para não quebrar
nada que dependa dela.

`montar_texto_numerado()` passa a emitir uma linha extra
`[N linha(s) em branco]` logo após o parágrafo, quando
`linhas_em_branco_apos > 0`. Parágrafos de tabela e de PDF (que não têm essa
chave) não são afetados — `dict.get(..., 0)` cobre a ausência da chave.

### 2. `agent/skills/espaco_resposta.py` (novo)

Segue o mesmo padrão das demais skills (`cruzamento.py` como referência mais
próxima). Função `verificar_espaco_resposta(client, texto_numerado,
faixa_etaria, perfil=None) -> List[dict]`.

Prompt do sistema instrui o modelo a:
1. Identificar, entre os marcadores `[N linha(s) em branco]`, quais são
   espaço de resposta de atividade (após um enunciado/pergunta/comando) —
   ignorando espaçamento decorativo entre seções ou títulos.
2. Avaliar se a quantidade de linhas é suficiente para o tipo de resposta
   esperado, considerando a faixa etária (letra maior/mais linhas para anos
   iniciais, conforme os perfis já existentes em `agent/profiles`).
3. Reportar apenas os casos insuficientes, de forma conservadora (só quando
   a insuficiência for evidente).

Cada item retornado tem:
- `texto_original`: trecho exato do enunciado da atividade (âncora)
- `explicacao`: inclui quantas linhas existem, quantas seriam adequadas, e
  o motivo
- `tipo`: `"espaco_resposta_insuficiente"`
- **sem** `texto_corrigido` — isso é o que faz o item não gerar edição no
  `.docx` (ver seção 3)

### 3. `agent/editor.py`

- Novo parâmetro `fazer_espaco_resposta: bool = True` em `revisar_documento`.
- Nova etapa opcional, só roda se `not is_pdf` (escopo só docx), chamando
  `verificar_espaco_resposta` e estendendo `todas_as_mudancas` com o
  resultado.
- Como os itens não têm `texto_corrigido`, o filtro existente em
  `word/track_changes.py::aplicar_todas_as_mudancas` (`mudancas_validas`,
  que exige `texto_original` E `texto_corrigido` diferentes) já os exclui
  automaticamente da edição do documento — nenhuma mudança necessária em
  `track_changes.py`.
- Entrada correspondente em `etapas_concluidas` para aparecer no resumo da
  UI, seguindo o padrão das outras etapas.

### 4. `app.py`

Novo `gr.Checkbox` "Espaço de Resposta — linhas em branco suficientes para a
atividade", valor padrão `True`, na mesma seção "🔍 Tipos de Revisão",
encadeado nos `inputs`/`outputs` de `_revisar` e na chamada a
`revisar_documento`.

### 5. `report/generator.py`

Adiciona `"espaco_resposta_insuficiente"` a `CORES_TIPO` e `NOMES_TIPO`
(mesmo padrão usado para as 13 categorias corrigidas no bug do grifo preto).
Sem mudança estrutural — o item passa pela tabela genérica por tipo já
existente; a coluna "Corrigido" fica vazia (não há `texto_corrigido`), o que
é o comportamento correto para um alerta.

## Fora de escopo (explicitamente)

- Espaço de resposta em caixas de texto ou células de tabela com altura
  fixa.
- Sinalização de espaço excessivo.
- Inserção automática de linhas no `.docx`.
- Verificação de espaço de resposta em PDFs.
