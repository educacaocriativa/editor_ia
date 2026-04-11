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
duas correções complementares para cada passagem.

TEMAS QUE EXIGEM CORREÇÃO:
- Origem do ser humano / evolução apresentada como fato absoluto
- Surgimento do universo / Big Bang apresentado como fato absoluto
- Afirmações de que a religião é apenas construção social ou fenômeno cultural
- Relativismo moral apresentado como verdade absoluta
- Qualquer conteúdo que negue a existência ou ação de Deus como fato

NÃO CORRIGIR:
- Passagens que já usam qualificadores ("segundo a teoria evolutiva",
  "cientistas propõem", "sob a perspectiva científica", "de acordo com...")
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

CORREÇÃO 2 — cosmovisao_boxe (USE COM CRITÉRIO — MÁXIMO 3 POR ARQUIVO):
  O Boxe Confissão de Fé é reservado para os momentos em que a cosmovisão
  cristã precisa ser EXPLICITAMENTE esclarecida ao leitor — não deve ser
  criado para cada qualificador, apenas quando o tema central do parágrafo
  contradiz diretamente a fé evangélica (ex: origem da vida, criação do
  universo, natureza do ser humano).

  Regras OBRIGATÓRIAS do boxe:
    - Máximo 25 palavras
    - Começar com "Boxe Confissão de Fé: "
    - Expressar a posição evangélica com clareza e respeito
    - PROIBIDO usar citações bíblicas (versículos, referências, textos
      bíblicos) — o boxe deve ser uma afirmação de fé em linguagem própria
    - PROIBIDO criar boxe para passagens onde um qualificador já é suficiente
    - Exemplo correto: "Boxe Confissão de Fé: Para a comunidade evangélica,
      a criação do ser humano se deu, unicamente, pela vontade de Deus."
    - Exemplo incorreto: incluir "Gênesis 1:1", "João 1:3" ou qualquer
      referência bíblica no texto do boxe

  - texto_original: últimas 10-15 palavras EXATAS do parágrafo após o qual
    o boxe deve ser inserido
  - texto_boxe: texto completo do boxe (máximo 25 palavras, sem citação bíblica)

LIMITE GLOBAL: gere no máximo 3 itens do tipo cosmovisao_boxe por resposta.
Priorize os temas de maior impacto na cosmovisão (origem humana, criação,
natureza de Deus). Se houver mais de 3 passagens elegíveis para boxe,
escolha as 3 mais relevantes e use apenas qualificador nas demais.

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
    "texto_boxe": "Boxe Confissão de Fé: ... (máx 25 palavras, sem citação bíblica)",
    "explicacao": "por que este parágrafo justifica um boxe e não apenas um qualificador"
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
