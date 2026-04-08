"""
Habilidade: Verificação de Fatos (5 rodadas independentes).

Cada afirmação factual é verificada 5 vezes de forma independente.
Apenas afirmações com maioria de "incorretas" (3+/5) são sinalizadas.
"""
import json
from typing import List, Dict, Tuple
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta


SYSTEM_EXTRAIR_FATOS = """Você é um especialista em verificação de fatos em materiais educacionais.

Sua tarefa é EXTRAIR afirmações factuais verificáveis do texto fornecido.

Foco em:
- Datas e períodos históricos
- Nomes de pessoas, lugares e organizações
- Dados numéricos (quantidades, porcentagens, distâncias, etc.)
- Afirmações científicas (leis, fórmulas, processos)
- Afirmações geográficas
- Eventos históricos

NÃO incluir:
- Opiniões ou interpretações
- Definições de conceitos genéricos
- Instruções pedagógicas

FORMATO DE SAÍDA — array JSON:
[
  {
    "afirmacao": "a afirmação factual exata como aparece no texto",
    "contexto": "parágrafo ou trecho de contexto"
  }
]

Se não houver afirmações verificáveis, retorne: []
"""

SYSTEM_VERIFICAR_FATO = """Você é um verificador de fatos rigoroso e imparcial especializado em conteúdo educacional brasileiro.

Analise a afirmação factual fornecida e determine se ela é CORRETA ou INCORRETA.

RESPONDA APENAS com um JSON no formato:
{
  "veredicto": "CORRETO" ou "INCORRETO" ou "INCERTO",
  "confianca": 1-5,
  "justificativa": "explicação breve e objetiva",
  "texto_reescrito": "reescrita completa da frase original com a informação correta incorporada naturalmente (apenas se INCORRETO)"
}

REGRAS PARA texto_reescrito:
- Reescreva a frase/trecho COMPLETO, não apenas o trecho errado
- Incorpore a informação correta de forma natural, como se o texto sempre estivesse certo
- Mantenha o tom, vocabulário e nível de linguagem do texto original
- NÃO escreva frases como "Na verdade..." ou "O correto é..." — apenas reescreva
- A reescrita deve ser pedagogicamente adequada ao nível do material

Seja conservador: use "INCERTO" quando não tiver certeza absoluta.
"""


def _extrair_afirmacoes_factuais(client: anthropic.Anthropic, texto: str) -> List[Dict]:
    """Extrai afirmações factuais verificáveis do texto."""
    user = f"Extraia as afirmações factuais verificáveis do texto a seguir:\n\n{texto}"
    resposta = _chamar_claude(client, SYSTEM_EXTRAIR_FATOS, user)
    return _extrair_json_da_resposta(resposta)


def _verificar_afirmacao_uma_vez(
    client: anthropic.Anthropic,
    afirmacao: str,
    contexto: str,
    faixa_etaria: str = "",
) -> Dict:
    """Verifica uma única afirmação factual."""
    faixa_str = f"\nFAIXA ETÁRIA DO MATERIAL: {faixa_etaria}" if faixa_etaria else ""
    user = f"""AFIRMAÇÃO: {afirmacao}

CONTEXTO (trecho original completo): {contexto}{faixa_str}

Verifique se esta afirmação é factualmente correta.
Se incorreta, reescreva o CONTEXTO completo com a informação correta incorporada naturalmente."""

    resposta = _chamar_claude(client, SYSTEM_VERIFICAR_FATO, user, cache_system=False)
    resultados = _extrair_json_da_resposta(resposta)
    if isinstance(resultados, dict):
        return resultados
    if isinstance(resultados, list) and resultados:
        return resultados[0]
    return {"veredicto": "INCERTO", "confianca": 1, "justificativa": "Falha na análise", "correcao": ""}


def _verificar_com_maioria(
    client: anthropic.Anthropic,
    afirmacao: str,
    contexto: str,
    n_verificacoes: int = 5,
    faixa_etaria: str = "",
) -> Tuple[str, str, List[Dict]]:
    """
    Verifica uma afirmação N vezes e retorna o veredicto por maioria.
    Retorna (veredicto_final, texto_reescrito, todas_as_verificacoes).
    """
    resultados = []
    for _ in range(n_verificacoes):
        r = _verificar_afirmacao_uma_vez(
            client, afirmacao, contexto, faixa_etaria
        )
        resultados.append(r)

    incorretos = [r for r in resultados if r.get("veredicto") == "INCORRETO"]
    corretos = [r for r in resultados if r.get("veredicto") == "CORRETO"]

    if len(incorretos) >= 3:
        # Maioria diz incorreto — usa a reescrita com maior confiança
        melhor = max(incorretos, key=lambda r: r.get("confianca", 0))
        reescrito = melhor.get("texto_reescrito", "") or melhor.get("correcao", "")
        return "INCORRETO", reescrito, resultados
    elif len(corretos) >= 3:
        return "CORRETO", "", resultados
    else:
        return "INCERTO", "", resultados


def verificar_fatos(
    client: anthropic.Anthropic,
    texto_plano: str,
    n_verificacoes: int = 5,
    faixa_etaria: str = "",
) -> List[dict]:
    """
    Verifica todos os fatos do texto com múltiplas rodadas.
    Retorna lista de alterações no formato padrão do sistema.
    """
    afirmacoes = _extrair_afirmacoes_factuais(client, texto_plano)
    alteracoes = []

    for item in afirmacoes:
        afirmacao = item.get("afirmacao", "").strip()
        contexto = item.get("contexto", "").strip()

        if not afirmacao:
            continue

        veredicto, reescrito, todas = _verificar_com_maioria(
            client, afirmacao, contexto, n_verificacoes, faixa_etaria
        )

        if veredicto == "INCORRETO" and reescrito:
            n_incorretos = sum(
                1 for r in todas if r.get("veredicto") == "INCORRETO"
            )
            justificativas = [
                r.get("justificativa", "") for r in todas
                if r.get("veredicto") == "INCORRETO"
            ]
            justificativa = (
                justificativas[0] if justificativas
                else "Informação factualmente incorreta."
            )
            # texto_original = contexto completo para localizar no doc
            # texto_corrigido = reescrita pedagógica do mesmo trecho
            alteracoes.append({
                "texto_original": contexto or afirmacao,
                "texto_corrigido": reescrito,
                "tipo": "factual",
                "explicacao": (
                    f"[{n_incorretos}/{n_verificacoes} verificações]"
                    f" {justificativa}"
                ),
            })
        elif veredicto == "INCERTO":
            # Sinaliza como incerto mas sem propor correção automática
            alteracoes.append({
                "texto_original": afirmacao,
                "texto_corrigido": afirmacao,  # sem alteração
                "tipo": "factual_incerto",
                "explicacao": f"Afirmação com credibilidade incerta após {n_verificacoes} verificações. Requer revisão humana.",
            })

    return alteracoes
