# Fila Global de Processamento entre Processos — Design

## Problema

`app.py` (interface Gradio) e `api.py` (API Flask consumida pela plataforma
de autoria) rodam como processos separados, gerenciados por PM2, na mesma
instância AWS, compartilhando a mesma `ANTHROPIC_API_KEY` e os mesmos
recursos de CPU/RAM. Cada processo tem sua própria noção de concorrência
(`demo.queue()` no Gradio; nenhuma no Flask), então nada impede os dois
processos de chamarem a API da Anthropic ao mesmo tempo para documentos
diferentes. Sob uso simultâneo, isso derruba a aplicação e degrada a chave
de API (rate limit em cascata, cada chamada já tentando de novo sozinha até
6 vezes).

Além disso, `api.py` roda com o servidor de desenvolvimento do Flask
(`app.run`), não recomendado para produção.

## Escopo

- Fila FIFO entre processos, cobrindo tanto `app.py` quanto `api.py`, sem
  exigir infraestrutura nova (Redis etc.) — implementada com SQLite, que já
  serializa corretamente acesso concorrente entre processos no mesmo disco.
- Timeout de espera máxima na fila, para nunca travar uma requisição pra
  sempre.
- Troca do servidor do `api.py` para `waitress` (produção real, mesma linha
  de comando do PM2).
- Fora de escopo: balanceamento entre múltiplas instâncias EC2, filas
  distribuídas (Redis/SQS), rate limiting por usuário.

## Mudanças

### 1. `agent/fila_processamento.py` (novo)

Context manager `entrar_na_fila(origem, log=None, timeout=1800)`:
- Insere uma linha em `dados/fila.db` (tabela `fila`, `id` autoincremento).
- Bloqueia (polling a cada 1s) até que o `id` inserido seja o menor da
  tabela — ou seja, até ser a vez do job.
- Loga posição na fila via callback (reaproveita o `log()` já usado no
  progresso do Editor IA).
- Se exceder `timeout`, remove a própria entrada e levanta `TimeoutError`
  com mensagem clara.
- Sempre remove a própria entrada da fila ao sair (`finally`), mesmo em
  caso de exceção — libera a vez do próximo job.

### 2. `agent/editor.py`

`revisar_documento` passa a envolver o trabalho pesado (a partir da
validação da API key até a geração do relatório) em
`with entrar_na_fila(origem="gradio"|"api", log=log):`. Como a fila é
process-agnostic (SQLite em disco), tanto `app.py` quanto `api.py` entram
na mesma fila.

### 3. `api.py`

- Adiciona `waitress` a `requirements.txt`.
- Troca `app.run(host="0.0.0.0", port=API_PORT)` por
  `waitress.serve(app, host="0.0.0.0", port=API_PORT, threads=8)` no bloco
  `if __name__ == "__main__":`. Threads extras só ficam bloqueadas
  aguardando a vez na fila SQLite — não chamam a API da Anthropic em
  paralelo.
- Trata `TimeoutError` da fila devolvendo HTTP 503 com mensagem clara em
  vez de a requisição ficar pendurada.

### 4. `app.py`

- Trata `TimeoutError` da fila no log de progresso da mesma forma que os
  outros erros já tratados no `_worker`.

## Fora de escopo (explicitamente)

- Múltiplas instâncias EC2 / balanceamento de carga entre máquinas.
- Fila distribuída (Redis, SQS).
- Rate limiting por usuário/IP.
- Priorização de jobs (a fila é estritamente FIFO).
