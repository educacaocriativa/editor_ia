"""
Habilidade: Humanização da Escrita por faixa etária.
Usa o PerfilEtario para aplicar critérios de tom e engajamento
específicos de cada fase.
"""
from typing import List, Optional
import anthropic
from .base import (
    _chamar_claude,
    _extrair_json_da_resposta,
    SYSTEM_FORMATO_JSON,
)
from agent.profiles.base_perfil import PerfilEtario


SYSTEM_HUMANIZACAO_BASE = (
    "Você é um especialista em comunicação educacional com habilidade de"
    " tornar textos didáticos mais humanos, engajantes e acolhedores,\n"
    " respeitando o nível de desenvolvimento do público-alvo.\n\n"
    "PRINCÍPIOS UNIVERSAIS DA HUMANIZAÇÃO:\n"
    "1. Voz ativa e sujeito agente claro\n"
    "2. Tom de proximidade adequado à faixa etária\n"
    "3. Concretude: substituir abstrações por exemplos do cotidiano\n"
    "4. Ritmo variado: alternar frases curtas e longas\n"
    "5. Conectar o conteúdo à curiosidade e experiência do estudante\n"
    "6. Eliminar jargões acadêmicos sem necessidade\n\n"
    "LIMITES — NÃO alterar:\n"
    "- Termos técnicos necessários ao aprendizado\n"
    "- Conteúdo factual\n"
    "- Precisão conceitual\n"
    "- Adequação ao nível de ensino\n\n"
    + SYSTEM_FORMATO_JSON
    + '\nCategorias válidas para "tipo": "humanizacao"'
)


def humanizar_texto(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str,
    perfil: Optional[PerfilEtario] = None,
    contexto_referencia: str = "",
) -> List[dict]:
    """
    Humaniza a linguagem mantendo rigor didático e respeitando
    as características específicas da faixa etária.
    """
    bloco_hum = (
        perfil.bloco_humanizacao()
        if perfil
        else f"FAIXA ETÁRIA: {faixa_etaria}"
    )

    bloco_ref = ""
    if contexto_referencia.strip():
        bloco_ref = f"\n{contexto_referencia}\n"

    user = (
        f"{bloco_hum}\n"
        f"{bloco_ref}\n"
        "Aplique humanização ao texto abaixo conforme os critérios"
        f" específicos de '{faixa_etaria}'.\n"
        "Foque em tornar a linguagem mais próxima e engajante"
        " SEM alterar o conteúdo.\n\n"
        f"TEXTO PARA REVISAR:\n{texto_numerado}"
    )

    resposta = _chamar_claude(client, SYSTEM_HUMANIZACAO_BASE, user)
    return _extrair_json_da_resposta(resposta)
