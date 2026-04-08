"""
Habilidade: Revisão Pedagógica específica por faixa etária.
Usa o PerfilEtario para injetar critérios precisos de cada fase
de desenvolvimento.
"""
from typing import List, Optional
import anthropic
from .base import (
    _chamar_claude,
    _extrair_json_da_resposta,
    SYSTEM_FORMATO_JSON,
)
from agent.profiles.base_perfil import PerfilEtario


SYSTEM_PEDAGOGICO_BASE = (
    "Você é um especialista em pedagogia, didática e produção de materiais"
    " educacionais para a educação básica brasileira, alinhado à BNCC.\n\n"
    "Sua tarefa é revisar o material didático do ponto de vista PEDAGÓGICO,"
    " aplicando rigorosamente os critérios específicos da faixa etária"
    " fornecida.\n\n"
    "FOCO DESTA REVISÃO:\n"
    "1. Adequação do vocabulário ao desenvolvimento linguístico\n"
    "2. Complexidade sintática compatível com o nível de leitura\n"
    "3. Abordagem didática coerente com o desenvolvimento cognitivo\n"
    "4. Sequência e progressão de conteúdo (scaffolding)\n"
    "5. Tom, registro e engajamento para o público\n"
    "6. Exemplos, analogias e contextualizações adequadas\n"
    "7. Linguagem inclusiva e representativa\n\n"
    "NÃO revisar: ortografia, gramática formal, fatos científicos.\n\n"
    + SYSTEM_FORMATO_JSON
    + '\nCategorias válidas: "vocabulario", "complexidade",'
    ' "abordagem_didatica", "sequencia", "tom_registro",'
    ' "exemplo_analogia", "inclusao", "scaffolding"'
)


def revisar_pedagogico(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str,
    plano_obras: str = "",
    perfil: Optional[PerfilEtario] = None,
    contexto_referencia: str = "",
) -> List[dict]:
    """
    Revisa a adequação pedagógica do texto usando o perfil
    específico da faixa etária.
    """
    bloco_perfil = (
        perfil.bloco_pedagogico()
        if perfil
        else f"FAIXA ETÁRIA: {faixa_etaria}"
    )

    contexto_plano = ""
    if plano_obras.strip():
        contexto_plano = (
            "\nREFERÊNCIA — PLANO DE OBRAS / GUIA DE ESTILO DA EDITORA:\n"
            + plano_obras[:3000]
            + "\n(Use como referência para adequação ao projeto editorial)\n"
        )

    bloco_ref = ""
    if contexto_referencia.strip():
        bloco_ref = f"\n{contexto_referencia}\n"

    instrucao = (
        "Revise o texto abaixo aplicando os critérios pedagógicos"
        " específicos desta faixa etária.\n"
        "Seja cirúrgico: aponte apenas os problemas reais,"
        " não ajustes subjetivos."
    )

    user = (
        f"{bloco_perfil}\n"
        f"{contexto_plano}"
        f"{bloco_ref}\n"
        f"{instrucao}\n\n"
        f"TEXTO PARA REVISAR:\n{texto_numerado}"
    )

    resposta = _chamar_claude(client, SYSTEM_PEDAGOGICO_BASE, user)
    return _extrair_json_da_resposta(resposta)
