"""
Habilidade: Cruzamento de informações entre conteúdo, atividades e gabarito.

Verifica dois alinhamentos críticos:
1. CONTEÚDO → ATIVIDADE: o capítulo fornece base suficiente para
   o aluno responder cada atividade?
2. GABARITO → ATIVIDADE + CONTEÚDO: a resposta fornecida é coerente
   com a pergunta E com o que o capítulo ensinou?
"""
from typing import List, Optional
import anthropic
from .base import (
    _chamar_claude,
    _extrair_json_da_resposta,
    SYSTEM_FORMATO_JSON,
)
from agent.profiles.base_perfil import PerfilEtario
from agent.diretrizes import DIRETRIZES_GERAIS, DIRETRIZES_HUMANIDADES_CRISTAS


SYSTEM_CRUZAMENTO_BASE = (
    "Você é um especialista em design instrucional e análise de materiais "
    "didáticos para a educação básica brasileira.\n\n"
    "Sua tarefa é fazer o CRUZAMENTO entre três elementos do material:\n"
    "  (A) CONTEÚDO EXPOSITIVO — o que o capítulo ensina\n"
    "  (B) ATIVIDADES — o que é pedido ao aluno\n"
    "  (C) GABARITO / RESPOSTAS — as respostas fornecidas (se existirem)\n\n"
    "VERIFICAÇÃO 1 — Cobertura (A → B):\n"
    "Para cada atividade, verifique se o conteúdo expositivo do capítulo "
    "fornece informação suficiente para que o aluno consiga respondê-la.\n"
    "Problemas a detectar:\n"
    "- Atividade exige conhecimento que NÃO foi ensinado no capítulo\n"
    "- Atividade exige inferência impossível a partir do conteúdo disponível\n"
    "- Atividade referencia figura, tabela ou texto que não está presente\n"
    "- Vocabulário da atividade não foi introduzido no conteúdo\n\n"
    "VERIFICAÇÃO 2 — Coerência do gabarito (C → A + B):\n"
    "Para cada gabarito presente, verifique se a resposta é coerente com:\n"
    "  - O enunciado da atividade (responde o que foi perguntado?)\n"
    "  - O conteúdo do capítulo (está alinhada com o que foi ensinado?)\n"
    "Problemas a detectar:\n"
    "- Gabarito contradiz o conteúdo do capítulo\n"
    "- Gabarito responde uma pergunta diferente da formulada\n"
    "- Gabarito está incompleto para o que a atividade exige\n"
    "- Gabarito usa conceitos ou termos não trabalhados no capítulo\n"
    "- Gabarito correto, mas a atividade está mal formulada para chegar "
    "nessa resposta\n\n"
    "IMPORTANTE:\n"
    "- Se não houver gabarito no texto, faça apenas a Verificação 1\n"
    "- Seja preciso: aponte apenas problemas reais, não subjetivos\n"
    "- Cite o trecho exato da atividade E o trecho do conteúdo relevante\n\n"
    + DIRETRIZES_GERAIS
    + "\n"
    + DIRETRIZES_HUMANIDADES_CRISTAS
    + "\n\n"
    + SYSTEM_FORMATO_JSON
    + '\nCategorias válidas para "tipo": "cruzamento_sem_base", '
    '"cruzamento_gabarito_incoerente", "cruzamento_gabarito_incompleto", '
    '"cruzamento_atividade_mal_formulada"'
)


def cruzar_informacoes(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str,
    perfil: Optional[PerfilEtario] = None,
) -> List[dict]:
    """
    Cruza conteúdo, atividades e gabarito do capítulo.
    Detecta atividades sem base no conteúdo e gabaritos incoerentes.
    """
    faixa_str = perfil.nome if perfil else faixa_etaria

    user = (
        f"FAIXA ETÁRIA: {faixa_str}\n\n"
        "Analise o texto abaixo identificando:\n"
        "  - Blocos de CONTEÚDO EXPOSITIVO (teoria, explicações, exemplos)\n"
        "  - Blocos de ATIVIDADES (exercícios, questões, tarefas)\n"
        "  - Blocos de GABARITO ou RESPOSTAS (se presentes)\n\n"
        "Depois faça o cruzamento conforme as instruções.\n\n"
        "Para cada problema encontrado informe:\n"
        "- texto_original: o trecho problemático exato "
        "(atividade ou gabarito)\n"
        "- texto_corrigido: versão corrigida — reformule a atividade para "
        "ter base no conteúdo disponível, ou corrija o gabarito para ser "
        "coerente com a pergunta e o conteúdo\n"
        "- tipo: categoria do problema\n"
        "- explicacao: qual o problema específico, citando o trecho do "
        "conteúdo que falta ou que contradiz\n\n"
        f"TEXTO PARA ANALISAR:\n{texto_numerado}"
    )

    resposta = _chamar_claude(client, SYSTEM_CRUZAMENTO_BASE, user)
    return _extrair_json_da_resposta(resposta)
