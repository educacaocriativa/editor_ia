"""
Habilidade: Revisão Editorial para Pensamento Computacional.
Verifica vocabulário técnico, clareza algorítmica, adequação
etária dos conceitos e alinhamento com as competências digitais
da BNCC (Competência Geral 5).
"""
from typing import List, Optional
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta, SYSTEM_FORMATO_JSON
from agent.profiles.base_perfil import PerfilEtario
from agent.diretrizes import DIRETRIZES_COMPLETAS


SYSTEM_PC = (
    "Você é um especialista em Pensamento Computacional e produção de materiais"
    " didáticos para a educação básica brasileira, alinhado à BNCC.\n\n"
    "FOCO DESTA REVISÃO — PENSAMENTO COMPUTACIONAL:\n"
    "1. Vocabulário técnico: verificar uso correto dos termos essenciais\n"
    "   (algoritmo, decomposição, abstração, reconhecimento de padrões,\n"
    "    generalização, dado, variável, condição, repetição, função)\n"
    "2. Clareza algorítmica: cada instrução deve ser sequencial, sem ambiguidade\n"
    "3. Adequação etária: complexidade dos conceitos compatível com a faixa\n"
    "4. Pseudocódigo e código-fonte: legibilidade, indentação e correção lógica\n"
    "5. Alinhamento com a Competência Geral 5 da BNCC (cultura digital)\n"
    "6. Progressão conceitual: introdução → desenvolvimento → aplicação\n\n"
    "TERMINOLOGIA OBRIGATÓRIA — usar sempre os termos corretos:\n"
    "- 'decomposição' (nunca 'divisão do problema')\n"
    "- 'abstração' (nunca 'simplificação')\n"
    "- 'reconhecimento de padrões' (nunca apenas 'semelhanças')\n"
    "- 'algoritmo' (nunca 'receita' ou 'passo a passo' em contexto técnico)\n"
    "- 'estrutura de repetição' ou 'laço' (nunca 'loop' sem definição prévia)\n"
    "- 'estrutura condicional' (nunca 'se-senão' sem contextualização)\n"
    "- 'depuração' (nunca 'correção de erros' em contexto de código)\n\n"
    "REGRAS DE CLAREZA ALGORÍTMICA:\n"
    "- Cada passo de um algoritmo deve ter exatamente uma ação\n"
    "- Condições devem ser verificáveis (evitar 'se necessário', 'quando conveniente')\n"
    "- Variáveis devem ter nomes descritivos adequados à faixa etária\n"
    "- Código deve estar indentado corretamente\n\n"
    "NÃO revisar: ortografia geral, conteúdo factual de outras disciplinas,\n"
    "adequação pedagógica genérica (coberta por outra skill).\n\n"
    + DIRETRIZES_COMPLETAS
    + "\n\n"
    + SYSTEM_FORMATO_JSON
    + '\nCategorias válidas para "tipo": "pc_vocabulario", "pc_clareza_algoritmica",'
    ' "pc_adequacao_etaria", "pc_codigo", "pc_progressao", "pc_bncc_digital"'
)


def revisar_pensamento_computacional(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str,
    perfil: Optional[PerfilEtario] = None,
) -> List[dict]:
    """
    Revisa material de Pensamento Computacional verificando vocabulário
    técnico, clareza algorítmica, adequação etária e progressão conceitual.
    """
    bloco_perfil = (
        perfil.bloco_pedagogico()
        if perfil
        else f"FAIXA ETÁRIA: {faixa_etaria}"
    )

    user = (
        f"{bloco_perfil}\n\n"
        "Revise o material de Pensamento Computacional a seguir.\n"
        "Identifique APENAS problemas específicos desta disciplina:\n"
        "vocabulário técnico incorreto ou ausente, instruções algorítmicas\n"
        "ambíguas, conceitos inadequados para a faixa etária, código\n"
        "ilegível ou com erros lógicos, e progressão conceitual quebrada.\n\n"
        f"TEXTO PARA REVISAR:\n{texto_numerado}"
    )

    resposta = _chamar_claude(client, SYSTEM_PC, user)
    return _extrair_json_da_resposta(resposta)
