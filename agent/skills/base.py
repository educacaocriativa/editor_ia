"""
Classe base para todas as habilidades de revisão.
"""
import json
import re
import threading
import time
from typing import Callable
import anthropic
from config import MODEL

# Retry em caso de rate limit (429) ou sobrecarga temporária (529)
_MAX_TENTATIVAS = 6
_ESPERA_PADRAO = 60  # segundos — usado quando a API não retorna retry-after

# Callback de log por thread — definido pelo editor antes de cada revisão
_thread_local = threading.local()


def set_log_callback(fn: Callable[[str], None]) -> None:
    """Registra log para a thread atual (uma revisão = uma thread)."""
    _thread_local.log_fn = fn


def _log_retry(msg: str) -> None:
    """Envia mensagem ao frontend (se callback registrado) e ao terminal."""
    fn = getattr(_thread_local, "log_fn", None)
    if fn:
        fn(msg)
    print(msg)


def _extrair_json_da_resposta(texto: str) -> list:
    """
    Extrai o bloco JSON da resposta do Claude de forma robusta.
    Tenta primeiro JSON puro, depois procura bloco ```json ... ```.
    """
    texto = texto.strip()

    # Tenta JSON direto
    try:
        return json.loads(texto)
    except Exception:
        pass

    # Procura bloco ```json
    match = re.search(r"```json\s*(.*?)```", texto, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    # Procura qualquer bloco [ ... ] ou { ... }
    match = re.search(r"(\[.*\]|\{.*\})", texto, re.DOTALL)
    if match:
        try:
            resultado = json.loads(match.group(1))
            if isinstance(resultado, dict) and "alteracoes" in resultado:
                return resultado["alteracoes"]
            return resultado if isinstance(resultado, list) else []
        except Exception:
            pass

    return []


def _chamar_claude(
    client: anthropic.Anthropic,
    system: str,
    user: str,
    cache_system: bool = True,
) -> str:
    """
    Chama o Claude com streaming e retorna o texto completo.
    Usa cache no system prompt para economizar tokens.
    """
    system_content = [
        {
            "type": "text",
            "text": system,
            **({"cache_control": {"type": "ephemeral"}} if cache_system else {}),
        }
    ]

    for tentativa in range(1, _MAX_TENTATIVAS + 1):
        try:
            msg = client.messages.create(
                model=MODEL,
                max_tokens=10000,
                system=system_content,
                messages=[{"role": "user", "content": user}],
            )
            # Filtra blocos de texto — ignora ThinkingBlock se presente
            texto_blocos = [
                bloco.text
                for bloco in msg.content
                if getattr(bloco, "type", "") == "text" and hasattr(bloco, "text")
            ]
            return "\n".join(texto_blocos)

        except anthropic.RateLimitError as exc:
            if tentativa == _MAX_TENTATIVAS:
                raise
            espera = _ESPERA_PADRAO
            if hasattr(exc, "response") and exc.response is not None:
                ra = exc.response.headers.get("retry-after")
                if ra:
                    try:
                        espera = int(float(ra)) + 2
                    except (ValueError, TypeError):
                        pass
            _log_retry(
                f"⏳ Limite de requisições atingido — aguardando "
                f"{espera}s antes de continuar "
                f"(tentativa {tentativa}/{_MAX_TENTATIVAS})..."
            )
            time.sleep(espera)

        except anthropic.APIStatusError as exc:
            if (
                getattr(exc, "status_code", 0) == 529
                and tentativa < _MAX_TENTATIVAS
            ):
                espera = _ESPERA_PADRAO * tentativa
                _log_retry(
                    f"⏳ API sobrecarregada — aguardando {espera}s "
                    f"(tentativa {tentativa}/{_MAX_TENTATIVAS})..."
                )
                time.sleep(espera)
            else:
                raise


SYSTEM_FORMATO_JSON = """
FORMATO DE SAÍDA OBRIGATÓRIO:
Retorne APENAS um array JSON válido, sem texto antes ou depois, no formato:
[
  {
    "texto_original": "trecho exato do documento como aparece no texto (mínimo 3 palavras, máximo 25 palavras)",
    "texto_corrigido": "versão corrigida do trecho",
    "tipo": "categoria_do_erro",
    "explicacao": "explicação objetiva da correção"
  }
]

REGRAS CRÍTICAS:
1. "texto_original" deve ser o trecho EXATO como aparece no documento (case-sensitive, incluindo pontuação).
2. Nunca invente ou altere o texto original — copie letra por letra.
3. Se não houver erros, retorne: []
4. Não inclua o mesmo trecho em múltiplas entradas.
5. O trecho deve ter contexto suficiente para ser único no documento.
"""
