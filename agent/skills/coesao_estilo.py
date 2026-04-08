"""
Habilidade: Revisão de Coesão, Coerência e Estilo Linguístico.
"""
from typing import List
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta, SYSTEM_FORMATO_JSON


SYSTEM_COESAO = f"""Você é um editor especialista em língua portuguesa (Brasil), com foco em coesão textual, coerência e estilo.

ESCOPO DESTA REVISÃO:
- Coesão: uso inadequado de conectivos, pronomes e referências
- Coerência: contradições internas, sequência lógica quebrada
- Estilo: repetição desnecessária de palavras, frases truncadas, ambiguidade
- Registro linguístico: adequação ao contexto formal/didático
- Clareza: frases excessivamente longas ou confusas

NÃO revisar: ortografia, gramática básica, conteúdo pedagógico, fatos.

{SYSTEM_FORMATO_JSON}
Categorias válidas para "tipo": "coesao", "coerencia", "estilo", "clareza", "registro"
"""


def revisar_coesao_estilo(client: anthropic.Anthropic, texto_numerado: str) -> List[dict]:
    """
    Revisa coesão, coerência e estilo do texto.
    Retorna lista de alterações.
    """
    user = f"""Revise o texto abaixo. Identifique SOMENTE problemas de coesão, coerência e estilo.

TEXTO PARA REVISAR:
{texto_numerado}"""

    resposta = _chamar_claude(client, SYSTEM_COESAO, user)
    return _extrair_json_da_resposta(resposta)
