"""
Habilidade: Revisão de Ortografia e Gramática.
"""
from typing import List
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta, SYSTEM_FORMATO_JSON


SYSTEM_ORTOGRAFIA = f"""Você é um revisor especialista em língua portuguesa (Brasil), com foco em ortografia e gramática.

ESCOPO DESTA REVISÃO:
- Erros ortográficos (grafia, acentuação, hífen)
- Erros de concordância verbal e nominal
- Erros de regência verbal e nominal
- Pontuação incorreta (vírgula, ponto, dois-pontos, ponto-e-vírgula)
- Uso inadequado de maiúsculas e minúsculas
- Crase

NÃO revisar nesta etapa: coesão, estilo, pedagogia, fatos.

{SYSTEM_FORMATO_JSON}
Categorias válidas para "tipo": "ortografia", "gramatica", "pontuacao", "crase"
"""


def revisar_ortografia(client: anthropic.Anthropic, texto_numerado: str) -> List[dict]:
    """
    Revisa ortografia e gramática do texto.
    Retorna lista de alterações.
    """
    user = f"""Revise o texto abaixo. Identifique SOMENTE erros de ortografia e gramática.

TEXTO PARA REVISAR:
{texto_numerado}"""

    resposta = _chamar_claude(client, SYSTEM_ORTOGRAFIA, user)
    return _extrair_json_da_resposta(resposta)
