"""
Habilidade: Análise, Classificação e Reescrita de Atividades
pela Taxonomia de Bloom (Anderson & Krathwohl).

Fluxo:
  1. Identifica TODAS as atividades do capítulo
  2. Classifica cada uma com os 4 campos da planilha:
       verbo | objetivos | processos | resultantes
  3. Diagnostica a progressão do conjunto
  4. Reescreve as atividades que estão estagnadas em níveis baixos,
     propondo versões mais ricas que exijam maior profundidade cognitiva,
     com o verbo de Bloom em **negrito** e norma culta rigorosa.
"""
import json
import re
from typing import List, Optional, Dict
import anthropic
from .base import _chamar_claude
from agent.profiles.base_perfil import PerfilEtario

# Nível máximo recomendado por faixa etária
NIVEL_MAX_FAIXA = {
    "ei_maternal": 1, "ei_infantil_i": 1, "ei_infantil_ii": 2,
    "ei_pre_i": 2, "ei_pre_ii": 3,
    "ef_1ano": 3, "ef_2ano": 3, "ef_3ano": 4,
    "ef_4ano": 4, "ef_5ano": 5,
    "ef_6ano": 4, "ef_7ano": 5, "ef_8ano": 5, "ef_9ano": 6,
    "em_1serie": 6, "em_2serie": 6, "em_3serie": 6,
}

NOMES_NIVEL = {
    1: "Conhecimento", 2: "Compreensão", 3: "Aplicação",
    4: "Análise", 5: "Avaliação", 6: "Criação",
}


def _extrair_json(texto: str):
    texto = texto.strip()
    try:
        return json.loads(texto)
    except Exception:
        pass
    m = re.search(r"```json\s*(.*?)```", texto, re.DOTALL | re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass
    m = re.search(r"(\[.*\])", texto, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    return []


def _bloco_perfil(perfil: Optional[PerfilEtario]) -> str:
    if not perfil:
        return ""
    nivel_max = NIVEL_MAX_FAIXA.get(perfil.chave, 4)
    nome_max = NOMES_NIVEL.get(nivel_max, "")
    return (
        f"FAIXA ETÁRIA: {perfil.nome}\n"
        f"Nível Bloom máximo recomendado: N{nivel_max} ({nome_max})\n"
        f"Progressão ideal: início em N1-N2, meio em N{max(2,nivel_max-2)}-N{max(3,nivel_max-1)}, "
        f"fim em N{nivel_max}."
    )


SYSTEM_FASE1 = """\
Você é um especialista em Taxonomia de Bloom (Anderson & Krathwohl, 2001) \
e design instrucional de materiais didáticos para a educação básica brasileira.

TAREFA — FASE 1: IDENTIFICAR E CLASSIFICAR ATIVIDADES

Atividades são comandos que cobram uma ação do estudante:
  - Itens numerados (1., 2., 3. / a) b) c)) que exigem resposta
  - Comandos como: "Responda", "Complete", "Observe e responda",
    "Leia e faça", "Escreva", "Calcule", "Compare", "Pesquise"
  - Perguntas diretas ao estudante
  - NÃO incluir textos expositivos, títulos, ou instruções sem cobrança

Para cada atividade, classifique com os 4 campos da Taxonomia de Bloom:
  verbo        → nível principal (Conhecimento, Compreensão, Aplicação,
                  Análise, Avaliação, Criação)
  objetivos    → o que o verbo visa alcançar (use termos da planilha)
  processos    → o processo cognitivo principal que o estudante usa
  resultantes  → o produto/entrega esperado do estudante

FORMATO DE SAÍDA — array JSON:
[
  {
    "tipo": "bloom_classificacao",
    "numero": "1",
    "texto_original": "enunciado EXATO da atividade (copie literalmente)",
    "verbo": "Conhecimento",
    "objetivos": "especificar",
    "processos": "reconhecer",
    "resultantes": "nomes",
    "nivel_bloom": 1,
    "nivel_bloom_nome": "Conhecimento",
    "posicao": "início",
    "status": "adequado"
  }
]

Para "posicao": divida o capítulo em terços — "início", "meio", "fim".
Para "status":
  "adequado"  → nível correto para a posição no capítulo
  "abaixo"    → nível baixo para a posição (atividade de fim no N1)
  "estagnado" → mesmo nível da atividade anterior (sem progressão)
  "acima"     → nível alto demais para a posição ou faixa etária

Se não houver atividades, retorne [].
"""

SYSTEM_FASE2 = """\
Você é um especialista em Taxonomia de Bloom (Anderson & Krathwohl, 2001), \
design instrucional e produção de materiais didáticos para a educação básica \
brasileira.

TAREFA — FASE 2: REESCREVER ATIVIDADES COM BAIXA PROFUNDIDADE COGNITIVA

Você receberá:
  1. A classificação das atividades do capítulo (Fase 1)
  2. O texto original do capítulo
  3. O perfil da faixa etária

Reescreva APENAS as atividades com status "abaixo" ou "estagnado" que \
precisam ser elevadas cognitivamente.

COMO REESCREVER:
  - Eleve o nível Bloom conforme a posição no capítulo
  - Use o conteúdo do próprio capítulo como base da nova atividade
  - Crie contextos situacionais reais e próximos da faixa etária
    (problemas concretos, situações do cotidiano, desafios autênticos)
  - O verbo de Bloom principal deve aparecer em **negrito** (marcado com **)
  - A reescrita deve ser rica, estimulante e pedagogicamente superior
  - Mantenha o mesmo tema/conteúdo da atividade original
  - Respeite RIGOROSAMENTE a norma culta da língua portuguesa:
    concordância, regência, pontuação, ortografia e registro adequado

NORMA CULTA — REGRAS INVIOLÁVEIS:
  - Imperativo afirmativo correto: "**Analise**", "**Avalie**", "**Crie**"
  - Concordância verbal e nominal sempre correta
  - Pontuação adequada ao comando instrucional
  - Nível de linguagem compatível com a faixa etária
  - Nunca introduzir erros gramaticais na reescrita

REGRA CRÍTICA PARA "texto_original":
  - Copie APENAS A PRIMEIRA LINHA do enunciado da atividade — o comando
    principal (até o primeiro ponto final, dois-pontos ou quebra de linha).
  - Não inclua sub-itens (a), b), c), i., ii.) nem linhas seguintes.
  - O trecho deve caber em um único parágrafo do Word (máximo ~30 palavras).
  - Esta restrição é obrigatória: ela garante que a substituição seja aplicada
    corretamente no documento Word.

FORMATO DE SAÍDA — array JSON:
[
  {
    "tipo": "bloom_correcao",
    "numero": "2",
    "texto_original": "APENAS a linha de comando principal da atividade (ex: 'Complete as lacunas com as palavras do quadro.')",
    "texto_corrigido": "nova linha de comando com **Verbo** em negrito (mesmo formato de parágrafo único)",
    "verbo_original": "Conhecimento",
    "verbo_novo": "Aplicação",
    "objetivos_novo": "uso de abstrações em situações concretas",
    "processos_novo": "solucionar",
    "resultantes_novo": "relato",
    "nivel_original": 1,
    "nivel_novo": 3,
    "justificativa": "Transforma completar lacunas em situação-problema real que exige aplicar o conhecimento geográfico para resolver uma tarefa concreta."
  }
]

Reescreva apenas o necessário — atividades já adequadas NÃO devem ser alteradas.
Se todas estiverem adequadas, retorne [].
"""


SYSTEM_ADAPTAR_GABARITO = """\
Você é um especialista em design instrucional e produção de materiais didáticos \
para a educação básica brasileira.

TAREFA: Atualizar o gabarito / orientações ao professor para refletir as \
reformulações de atividades que já foram aplicadas no material.

Você receberá:
  1. Lista de atividades que foram REFORMULADAS (novo enunciado elevado em Bloom)
  2. O texto completo do capítulo (que pode conter gabarito ou manual do professor)

Para cada atividade reformulada:
  - Localize o gabarito ou orientação correspondente no texto
  - Verifique se a resposta/orientação ainda é coerente com o NOVO enunciado
  - Se não for coerente (resposta errada, incompleta ou para pergunta diferente),
    proponha a correção

IMPORTANTE:
  - Só proponha mudança se houver real inconsistência com o novo enunciado
  - Mantenha o estilo do gabarito existente (ex: resposta objetiva, orientação
    didática, sugestão de resposta)
  - Se o gabarito estiver ausente ou já for adequado, não proponha nada
  - "texto_original" deve ser o trecho EXATO do gabarito/orientação atual
    (máximo ~30 palavras, parágrafo único)
  - "texto_corrigido" deve ser a versão atualizada desse trecho

FORMATO DE SAÍDA — array JSON:
[
  {
    "tipo": "bloom_gabarito",
    "texto_original": "trecho exato do gabarito/orientação atual",
    "texto_corrigido": "versão atualizada coerente com o novo enunciado",
    "explicacao": "por que o gabarito precisou ser atualizado"
  }
]

Se não houver gabarito ou nenhuma atualização for necessária, retorne [].
"""


def avaliar_bloom(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str,
    perfil: Optional[PerfilEtario] = None,
    contexto_planilha: str = "",
) -> List[dict]:
    """
    Executa as duas fases de análise Bloom.
    Retorna lista com bloom_classificacao e bloom_correcao.
    """
    bloco_perfil = _bloco_perfil(perfil)
    bloco_ref = contexto_planilha or ""

    # ── FASE 1: Classificação ────────────────────────────────────────────────
    user_fase1 = (
        f"{bloco_ref}\n\n"
        f"{bloco_perfil}\n\n"
        f"TEXTO DO CAPÍTULO:\n{texto_numerado}"
    )
    resp1 = _chamar_claude(client, SYSTEM_FASE1, user_fase1)
    classificacoes = _extrair_json(resp1)
    if not isinstance(classificacoes, list):
        classificacoes = []
    classificacoes = [r for r in classificacoes if isinstance(r, dict)]

    if not classificacoes:
        return []

    # ── FASE 2: Reescrita das problemáticas ─────────────────────────────────
    problematicas = [
        c for c in classificacoes
        if c.get("status") in ("abaixo", "estagnado")
    ]

    correcoes = []
    if problematicas:
        resumo_fase1 = json.dumps(classificacoes, ensure_ascii=False, indent=2)
        user_fase2 = (
            f"{bloco_ref}\n\n"
            f"{bloco_perfil}\n\n"
            f"CLASSIFICAÇÃO DAS ATIVIDADES (Fase 1):\n{resumo_fase1}\n\n"
            f"TEXTO ORIGINAL DO CAPÍTULO:\n{texto_numerado}"
        )
        resp2 = _chamar_claude(client, SYSTEM_FASE2, user_fase2)
        correcoes = _extrair_json(resp2)
        if not isinstance(correcoes, list):
            correcoes = []
        correcoes = [r for r in correcoes if isinstance(r, dict)]

    return classificacoes + correcoes


def adaptar_gabarito_bloom(
    client: anthropic.Anthropic,
    correcoes: List[dict],
    texto_numerado: str,
) -> List[dict]:
    """
    FASE 3 (opcional): dado que atividades foram reformuladas pelo Bloom,
    verifica se o gabarito / manual do professor precisa ser atualizado.
    Retorna lista de itens bloom_gabarito (podem ser zero).
    """
    if not correcoes:
        return []

    resumo = json.dumps(
        [
            {
                "numero": c.get("numero"),
                "texto_original": c.get("texto_original"),
                "texto_corrigido": c.get("texto_corrigido"),
                "justificativa": c.get("justificativa"),
            }
            for c in correcoes
        ],
        ensure_ascii=False,
        indent=2,
    )
    user = (
        f"ATIVIDADES REFORMULADAS (Bloom):\n{resumo}\n\n"
        f"TEXTO DO CAPÍTULO (inclui gabarito/manual do professor, se houver):\n"
        f"{texto_numerado}"
    )
    resp = _chamar_claude(client, SYSTEM_ADAPTAR_GABARITO, user)
    result = _extrair_json(resp)
    if not isinstance(result, list):
        return []
    return [r for r in result if isinstance(r, dict)]


def gerar_diagnostico_bloom(itens: List[dict]) -> Dict:
    """Gera diagnóstico consolidado a partir dos itens."""
    classificacoes = [i for i in itens if i.get("tipo") == "bloom_classificacao"]
    correcoes = [i for i in itens if i.get("tipo") == "bloom_correcao"]

    if not classificacoes:
        return {}

    niveis = [i.get("nivel_bloom", 0) for i in classificacoes]
    niveis_unicos = sorted(set(n for n in niveis if n))
    niveis_faltando = [n for n in range(1, 7) if n not in niveis_unicos]

    status_counts: Dict[str, int] = {}
    for i in classificacoes:
        s = i.get("status", "")
        status_counts[s] = status_counts.get(s, 0) + 1

    nivel_min = min(niveis_unicos) if niveis_unicos else 0
    nivel_max_enc = max(niveis_unicos) if niveis_unicos else 0
    amplitude = nivel_max_enc - nivel_min
    n_estagnado = status_counts.get("estagnado", 0)
    n_abaixo = status_counts.get("abaixo", 0)

    if amplitude >= 3 and n_estagnado <= 1 and n_abaixo <= 1:
        julgamento = "BOM — progressão cognitiva adequada"
    elif amplitude >= 2 and (n_estagnado + n_abaixo) <= 3:
        julgamento = "REGULAR — progressão parcial, com oportunidades de melhoria"
    else:
        julgamento = "INSUFICIENTE — atividades concentradas em poucos níveis cognitivos"

    return {
        "total_atividades": len(classificacoes),
        "total_correcoes": len(correcoes),
        "niveis_encontrados": niveis_unicos,
        "niveis_faltando": niveis_faltando,
        "nivel_minimo": nivel_min,
        "nivel_maximo": nivel_max_enc,
        "amplitude": amplitude,
        "julgamento": julgamento,
        "status_counts": status_counts,
    }
