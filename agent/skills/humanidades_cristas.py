"""
Habilidade: Cosmovisão Cristã — Humanidades Cristãs.

Identifica passagens que apresentam afirmações naturalistas (evolução,
Big Bang, origem humana, ética secular, etc.) sem o contraponto da
cosmovisão cristã e propõe duas correções complementares:

1. cosmovisao_qualificador — adiciona qualificador ao texto original
   (ex: "segundo algumas teorias científicas...")
2. cosmovisao_boxe — insere um "Boxe Confissão de Fé" após o parágrafo
   (máximo 25 palavras, reafirma a cosmovisão evangélica)
"""
import re
from typing import List, Optional
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta
from agent.profiles.base_perfil import PerfilEtario


SYSTEM_COSMOVISAO = """\
Você é um especialista em cosmovisão cristã evangélica e produção de materiais
didáticos para a Rede Luz do Mundo (LDM), rede confessional evangélica brasileira.

TAREFA: Identificar passagens que apresentam afirmações científicas naturalistas
como verdades absolutas, sem o contraponto da cosmovisão cristã, e propor
duas correções para cada passagem.

TEMAS QUE EXIGEM CORREÇÃO:
- Origem do ser humano / evolução (sem qualificador)
- Surgimento do universo / Big Bang (sem qualificador)
- Afirmações de que a religião é apenas construção social ou fenômeno cultural
- Relativismo moral apresentado como verdade absoluta
- Qualquer conteúdo que negue a existência ou ação de Deus como fato

NÃO CORRIGIR:
- Passagens que já usam qualificadores como "segundo a teoria evolutiva",
  "cientistas propõem", "sob a perspectiva científica", "de acordo com..."
- Passagens que já incluem o contraponto cristão
- Fatos históricos neutros, datas, eventos, dados geográficos

CORREÇÃO 1 — cosmovisao_qualificador:
  Adicione um qualificador à afirmação naturalista para apresentá-la como
  modelo/teoria, não como verdade absoluta.
  Expressões a usar:
    "Segundo algumas teorias científicas, ..."
    "Sob a perspectiva científica naturalista, ..."
    "De acordo com modelos científicos, ..."
    "Conforme propõe a teoria evolutiva, ..."
  - texto_original: trecho EXATO da afirmação problemática (parágrafo único,
    máximo 30 palavras)
  - texto_corrigido: mesmo trecho com o qualificador inserido

CORREÇÃO 2 — cosmovisao_boxe:
  Após o parágrafo corrigido, inserir um "Boxe Confissão de Fé" com o
  contraponto evangélico.
  Regras do boxe:
    - Máximo 25 palavras
    - Sempre começar com "Boxe Confissão de Fé: "
    - Expressar a cosmovisão cristã evangélica com clareza e respeito
    - Exemplo: "Boxe Confissão de Fé: Para a comunidade evangélica,
      a criação do ser humano se deu, unicamente, pela vontade de Deus."
  - texto_original: últimas 10-15 palavras EXATAS do parágrafo após o qual
    o boxe deve ser inserido (para localizar o parágrafo no documento)
  - texto_boxe: texto completo do boxe (máximo 25 palavras)

FORMATO DE SAÍDA — array JSON:
[
  {
    "tipo": "cosmovisao_qualificador",
    "texto_original": "trecho exato problemático (máx 30 palavras)",
    "texto_corrigido": "trecho com qualificador adicionado",
    "explicacao": "qual afirmação naturalista foi qualificada e por quê"
  },
  {
    "tipo": "cosmovisao_boxe",
    "texto_original": "últimas 10-15 palavras exatas do parágrafo",
    "texto_boxe": "Boxe Confissão de Fé: ... (máx 25 palavras)",
    "explicacao": "qual contraponto cristão foi adicionado"
  }
]

Se não houver passagens problemáticas, retorne [].
"""


def revisar_cosmovisao(
    client: anthropic.Anthropic,
    texto_numerado: str,
    faixa_etaria: str = "",
    perfil: Optional[PerfilEtario] = None,
) -> List[dict]:
    """
    Identifica passagens naturalistas sem contraponto cristão e propõe:
    - cosmovisao_qualificador: qualificador no texto
    - cosmovisao_boxe: Boxe Confissão de Fé após o parágrafo
    """
    faixa_str = perfil.nome if perfil else faixa_etaria
    user = (
        f"FAIXA ETÁRIA: {faixa_str}\n\n"
        "Analise o texto abaixo e identifique passagens que apresentam "
        "afirmações naturalistas sem o contraponto da cosmovisão cristã.\n\n"
        "Para cada passagem encontrada, gere:\n"
        "1. Um cosmovisao_qualificador (adiciona qualificador no texto)\n"
        "2. Um cosmovisao_boxe (Boxe Confissão de Fé, máx 25 palavras)\n\n"
        f"TEXTO PARA ANALISAR:\n{texto_numerado}"
    )
    resposta = _chamar_claude(client, SYSTEM_COSMOVISAO, user)
    itens = _extrair_json_da_resposta(resposta)
    if not isinstance(itens, list):
        return []
    return [
        item for item in itens
        if isinstance(item, dict) and item.get("tipo") in (
            "cosmovisao_qualificador", "cosmovisao_boxe"
        )
    ]
