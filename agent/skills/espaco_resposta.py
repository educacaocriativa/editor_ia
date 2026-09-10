"""
Habilidade: Verificação do espaço de resposta reservado nas atividades.

O texto numerado enviado ao Claude contém marcadores "[N linha(s) em
branco]" (ver word/extractor.py) indicando quantas linhas em branco
consecutivas existem em determinado ponto do documento original — o
espaço físico reservado para o aluno escrever a resposta.

Esta skill identifica quais desses blocos são espaço de resposta de
atividade (e não apenas espaçamento decorativo entre seções) e avalia se
a quantidade de linhas é suficiente para o tipo de resposta esperado,
considerando a faixa etária.

Não propõe texto_corrigido — é um alerta para o relatório, não uma edição
do documento (a decisão de adicionar linhas cabe ao revisor humano).
"""
from typing import List, Optional
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta
from agent.profiles.base_perfil import PerfilEtario
from agent.diretrizes import DIRETRIZES_GERAIS


SYSTEM_ESPACO_RESPOSTA = (
    "Você é um especialista em design instrucional de materiais didáticos "
    "para a educação básica brasileira, focado na usabilidade física do "
    "material impresso.\n\n"
    "O texto numerado contém marcadores \"[N linha(s) em branco]\" indicando "
    "quantas linhas em branco existem naquele ponto do documento — esse é o "
    "espaço físico reservado para o aluno escrever.\n\n"
    "SUA TAREFA:\n"
    "1. Identifique quais marcadores de linhas em branco são espaço de "
    "resposta de uma atividade — aparecem logo após um enunciado, "
    "pergunta ou comando que pede resposta escrita do aluno.\n"
    "   - IGNORE linhas em branco que são apenas espaçamento decorativo "
    "entre seções, títulos ou parágrafos de conteúdo expositivo — essas "
    "não são espaço de resposta e não devem ser reportadas.\n"
    "2. Para cada espaço de resposta identificado, avalie se a quantidade "
    "de linhas é SUFICIENTE para o tipo de resposta esperado pela "
    "pergunta (ex.: uma palavra ou número precisa de menos espaço que uma "
    "resposta dissertativa de um parágrafo, ou uma lista de vários itens), "
    "considerando a faixa etária informada (crianças menores escrevem "
    "letra maior e precisam de mais linhas para a mesma quantidade de "
    "texto).\n"
    "3. Reporte APENAS os casos em que o espaço está EVIDENTEMENTE "
    "insuficiente. Seja conservador — não reporte espaço adequado, "
    "excessivo, ou casos duvidosos.\n\n"
    "IMPORTANTE:\n"
    "- Nunca invente perguntas, atividades ou marcadores que não existem "
    "no texto.\n"
    "- Copie o enunciado da atividade letra por letra em texto_original.\n\n"
    + DIRETRIZES_GERAIS
    + "\n\n"
    "FORMATO DE SAÍDA OBRIGATÓRIO:\n"
    "Retorne APENAS um array JSON válido, sem texto antes ou depois:\n"
    "[\n"
    "  {\n"
    "    \"texto_original\": \"enunciado exato da atividade, como aparece "
    "no documento (mínimo 3 palavras, máximo 25 palavras)\",\n"
    "    \"linhas_disponiveis\": 1,\n"
    "    \"linhas_sugeridas\": 4,\n"
    "    \"explicacao\": \"por que o espaço é insuficiente para esse tipo "
    "de resposta, nessa faixa etária\",\n"
    "    \"tipo\": \"espaco_resposta_insuficiente\"\n"
    "  }\n"
    "]\n\n"
    "REGRAS CRÍTICAS:\n"
    "1. Não inclua o campo \"texto_corrigido\" — este é um alerta, não uma "
    "edição de texto.\n"
    "2. Se não houver nenhum caso de espaço insuficiente, retorne: []\n"
    "3. Não inclua o mesmo enunciado em múltiplas entradas.\n"
)


def verificar_espaco_resposta(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str,
    perfil: Optional[PerfilEtario] = None,
) -> List[dict]:
    """
    Analisa o texto numerado (com marcadores de linhas em branco) e retorna
    a lista de atividades cujo espaço de resposta reservado é insuficiente.
    """
    faixa_str = perfil.nome if perfil else faixa_etaria

    user = (
        f"FAIXA ETÁRIA: {faixa_str}\n\n"
        "Analise o texto abaixo (com marcadores de linhas em branco) e "
        "identifique atividades cujo espaço de resposta reservado é "
        "insuficiente, conforme as instruções.\n\n"
        f"TEXTO PARA ANALISAR:\n{texto_numerado}"
    )

    resposta = _chamar_claude(client, SYSTEM_ESPACO_RESPOSTA, user)
    itens = _extrair_json_da_resposta(resposta)

    # Funde linhas_disponiveis/linhas_sugeridas na explicação — assim o
    # item passa pela tabela genérica do relatório sem precisar de coluna
    # extra, e nunca carrega texto_corrigido (garante que não vira edição
    # do documento em word/track_changes.py).
    resultado = []
    for item in itens:
        if not isinstance(item, dict) or not item.get("texto_original"):
            continue
        disponiveis = item.get("linhas_disponiveis", "?")
        sugeridas = item.get("linhas_sugeridas", "?")
        explicacao = item.get("explicacao", "").strip()
        resultado.append({
            "texto_original": item["texto_original"],
            "explicacao": (
                f"Há {disponiveis} linha(s) em branco reservada(s); "
                f"o adequado seria cerca de {sugeridas}. {explicacao}"
            ).strip(),
            "tipo": "espaco_resposta_insuficiente",
        })
    return resultado
