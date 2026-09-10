"""
API REST do Editor IA — consumida por sistemas externos (ex.: a plataforma de
autoria) para pedir uma revisão editorial e receber as sugestões em JSON.

Roda SEPARADO da UI Gradio (app.py), em processo/porta próprios, sem tocar no
app publicado. Reaproveita todo o pipeline de `agent.editor.revisar_documento`
(regras de ouro, Bloom, cosmovisão, acessibilidade) — o valor pedagógico das
bases curadas fica disponível para a autoria sem duplicar nada.

Execução:
    pip install flask waitress
    set EDITOR_IA_API_TOKEN=<token compartilhado>   (Windows)
    export EDITOR_IA_API_TOKEN=<token compartilhado> (Linux)
    python api.py            # sobe em 0.0.0.0:7870

Autenticação: header  X-Editor-IA-Token: <token>  (igual ao da autoria).
"""

import os
import hmac
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify
import docx

from word.configuracao import carregar_config
from agent.editor import revisar_documento

# Mesma prioridade do app.py: config.json manda sobre env herdado.
_cfg = carregar_config()
if _cfg.get("anthropic_api_key"):
    os.environ["ANTHROPIC_API_KEY"] = _cfg["anthropic_api_key"]

API_TOKEN = os.environ.get("EDITOR_IA_API_TOKEN", "")
API_PORT = int(os.environ.get("EDITOR_IA_API_PORT", "7870"))

app = Flask(__name__)

# Mapeia o ano escolar da prova para a faixa etária esperada pelo pipeline.
# Aceita tanto rótulos livres ("6º ano", "3 ano EF") quanto números soltos.
_FAIXA_PADRAO = "6º ao 9º ano do Ensino Fundamental (11-14 anos)"


def _faixa_etaria(ano_escolar: str) -> str:
    txt = (ano_escolar or "").lower()
    if "infantil" in txt or "maternal" in txt or "pré" in txt or "pre" in txt:
        return "Educação Infantil (3-5 anos)"
    if "médio" in txt or "medio" in txt or "ensino medio" in txt:
        return "Ensino Médio (15-17 anos)"
    if "eja" in txt or "adulto" in txt:
        return "EJA / Adultos"
    # Extrai o primeiro número (ano) do texto.
    numero = None
    atual = ""
    for ch in txt:
        if ch.isdigit():
            atual += ch
        elif atual:
            break
    if atual:
        numero = int(atual)
    if numero is not None:
        if numero <= 2:
            return "1º ao 2º ano do Ensino Fundamental (6-7 anos)"
        if numero <= 5:
            return "3º ao 5º ano do Ensino Fundamental (8-10 anos)"
        if numero <= 9:
            return "6º ao 9º ano do Ensino Fundamental (11-14 anos)"
    return _FAIXA_PADRAO


def _construir_docx(itens: list) -> str:
    """
    Monta um .docx temporário com um parágrafo por 'item' (texto de fluxo ou
    atividade) recebido da autoria. Cada parágrafo carrega só o texto — o
    casamento de volta ao item (target_id) é feito na autoria por substring.
    """
    documento = docx.Document()
    for item in itens:
        texto = (item.get("text") or "").strip()
        if texto:
            documento.add_paragraph(texto)
    tmp = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    tmp.close()
    documento.save(tmp.name)
    return tmp.name


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "anthropic": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "auth_required": bool(API_TOKEN),
    })


@app.route("/api/revisao-prova", methods=["POST"])
def revisao_prova():
    # Autenticação por token compartilhado (comparação em tempo constante).
    if not API_TOKEN:
        return jsonify({"error": "EDITOR_IA_API_TOKEN nao configurado no servidor"}), 503
    recebido = request.headers.get("X-Editor-IA-Token", "")
    if not hmac.compare_digest(recebido, API_TOKEN):
        return jsonify({"error": "Token invalido"}), 401

    data = request.get_json(silent=True) or {}
    itens = data.get("items") or []
    if not isinstance(itens, list) or not any((i.get("text") or "").strip() for i in itens):
        return jsonify({"error": "Nenhum conteudo para revisar"}), 400

    opcoes = data.get("options") or {}
    faixa = _faixa_etaria(str(data.get("school_year") or ""))
    componente = str(data.get("discipline") or "")

    # Mapeia as opções que o professor marcou na autoria para as skills do
    # pipeline. Sempre roda ortografia (correção de Língua Portuguesa base).
    fazer_ortografia = True
    fazer_coesao = bool(opcoes.get("language", True))
    fazer_pedagogico = bool(opcoes.get("neurodiversity_language", False)) or bool(
        opcoes.get("pedagogy", False)
    )
    fazer_humanizacao = bool(opcoes.get("neurodiversity_language", False))
    fazer_bloom = bool(opcoes.get("bloom", True))
    fazer_cosmovisao = bool(opcoes.get("christian_worldview", False))

    caminho = _construir_docx(itens)
    # Captura erros de chamada ao modelo (créditos/limite/timeout da Anthropic).
    # As skills engolem esses erros e seguem; sem isso o pipeline devolveria
    # "sucesso vazio" e a autoria cobraria por uma revisão que não aconteceu.
    erros_modelo: list[str] = []

    def _cb(msg, pct=None):
        texto = str(msg)
        if "Erro" in texto or "⚠" in texto:
            erros_modelo.append(texto)

    try:
        resultado = revisar_documento(
            caminho_docx=caminho,
            faixa_etaria=faixa,
            componente_curricular=componente,
            fazer_ortografia=fazer_ortografia,
            fazer_coesao=fazer_coesao,
            fazer_pedagogico=fazer_pedagogico,
            fazer_fatos=False,       # fato-checking é caro; fora do escopo da prova
            fazer_humanizacao=fazer_humanizacao,
            fazer_bncc=False,        # sem banco BNCC no fluxo de prova
            fazer_bloom=fazer_bloom,
            fazer_cosmovisao=fazer_cosmovisao,
            fazer_cruzamento=False,
            fazer_pc=False,
            progress_callback=_cb,
            origem="api",
        )
    except TimeoutError as exc:
        return jsonify({"error": f"Fila de processamento cheia: {exc}"}), 503
    except Exception as exc:  # noqa: BLE001 — devolve erro tratado pra autoria
        return jsonify({"error": f"Falha na revisao: {exc}"}), 502
    finally:
        Path(caminho).unlink(missing_ok=True)

    # Falha real do modelo: houve erro nas chamadas E nada foi produzido. Devolve
    # 502 (não "sucesso vazio") pra autoria marcar a revisão como falha e NÃO
    # cobrar. Se o modelo respondeu mas não achou ajustes, segue como sucesso.
    if erros_modelo and int(resultado.get("total_alteracoes", 0) or 0) == 0:
        return jsonify({
            "error": "Falha nas chamadas ao modelo de IA (verifique credito/limite da chave Anthropic). "
            + erros_modelo[0][:200],
        }), 502

    return jsonify({
        "suggestions": resultado.get("mudancas_unicas", []),
        "summary": resultado.get("resumo", {}),
        "total": resultado.get("total_alteracoes", 0),
        "faixa_etaria": faixa,
    })


if __name__ == "__main__":
    print(f"[editor-ia-api] porta {API_PORT} · auth {'ON' if API_TOKEN else 'OFF'}")
    # waitress: servidor WSGI de produção (o servidor de desenvolvimento do
    # Flask não aguenta conexões concorrentes). As threads extras só ficam
    # bloqueadas aguardando a vez na fila global (agent/fila_processamento.py)
    # — não chamam a API da Anthropic em paralelo.
    from waitress import serve
    serve(app, host="0.0.0.0", port=API_PORT, threads=8)
