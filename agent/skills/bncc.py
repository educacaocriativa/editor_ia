"""
Habilidade: Validação de Habilidades da BNCC.

Executa três verificações independentes:
1. ESCRITA — os códigos declarados no material estão grafados corretamente?
2. ALINHAMENTO — o conteúdo da lição realmente trabalha cada habilidade declarada?
3. LACUNAS — há habilidades relevantes não declaradas que estão sendo trabalhadas?
"""
import json
import re
from typing import List, Dict, Tuple
import anthropic
from .base import _chamar_claude, _extrair_json_da_resposta, SYSTEM_FORMATO_JSON
from word.planilha_reader import (
    extrair_codigos_do_texto,
    filtrar_por_prefixos,
    formatar_habilidades_para_prompt,
    PATTERN_CODIGO,
)


# ── Sistema 1: Verificação de escrita dos códigos ────────────────────────────

SYSTEM_VERIFICAR_ESCRITA = f"""Você é um especialista na BNCC (Base Nacional Comum Curricular).

Sua tarefa é verificar se os códigos BNCC declarados num material didático estão
grafados corretamente e se correspondem ao componente, ano e habilidade descritos.

Para cada problema encontrado, forneça:
- O trecho exato onde o erro aparece (inclua o código incorreto + contexto de até 10 palavras)
- A versão corrigida

{SYSTEM_FORMATO_JSON}
Categorias válidas para "tipo": "bncc_codigo_incorreto", "bncc_ano_incompativel", "bncc_componente_errado"
"""

SYSTEM_VERIFICAR_ALINHAMENTO = """Você é um especialista em currículo e BNCC.

Analise se o conteúdo de uma lição didática realmente trabalha cada habilidade BNCC declarada.

Para cada habilidade que NÃO está sendo trabalhada, retorne:
{
  "codigo": "EF01LP01",
  "habilidade": "descrição da habilidade",
  "problema": "explicação do motivo pelo qual a lição não cobre a habilidade",
  "sugestao": "como adaptar o conteúdo para cobrir esta habilidade"
}

Se todas as habilidades estão sendo trabalhadas, retorne: []

Retorne APENAS o array JSON, sem texto adicional.
"""

SYSTEM_IDENTIFICAR_LACUNAS = """Você é um especialista em currículo e BNCC.

Com base no conteúdo de uma lição e nas habilidades disponíveis para a faixa etária,
identifique habilidades que CLARAMENTE estão sendo trabalhadas no conteúdo mas
NÃO foram declaradas na lista de habilidades da lição.

Critérios rigorosos:
- Inclua APENAS quando há correspondência clara e direta (não especulativa)
- Não inclua habilidades marginalmente relacionadas
- Máximo 5 sugestões por análise

Retorne:
[
  {
    "codigo": "EF01LP01",
    "habilidade": "descrição",
    "justificativa": "por que esta habilidade está sendo trabalhada no conteúdo"
  }
]

Se não houver lacunas claras, retorne: []
"""


def _extrair_declaracoes_bncc_do_doc(texto_plano: str) -> Tuple[List[str], List[str]]:
    """
    Extrai os códigos BNCC declarados no documento.
    Retorna (codigos_encontrados, trechos_contexto).
    """
    codigos = extrair_codigos_do_texto(texto_plano)
    trechos = []
    for codigo in codigos:
        # Busca o trecho ao redor do código para contexto
        match = re.search(re.escape(codigo) + r'.{0,100}', texto_plano, re.IGNORECASE)
        if match:
            trechos.append(match.group(0).strip())
        else:
            trechos.append(codigo)
    return codigos, trechos


def verificar_escrita_codigos(
    client: anthropic.Anthropic,
    texto_plano: str,
    banco_bncc: Dict[str, dict],
) -> List[dict]:
    """
    Verifica se os códigos BNCC declarados estão grafados corretamente
    e se correspondem ao banco de habilidades.
    """
    codigos_declarados, trechos = _extrair_declaracoes_bncc_do_doc(texto_plano)

    if not codigos_declarados:
        return []

    # Verifica cada código contra o banco
    erros_simples = []
    for codigo, trecho in zip(codigos_declarados, trechos):
        if codigo not in banco_bncc:
            # Tenta encontrar código similar (typo)
            similares = [c for c in banco_bncc if c[:6].upper() == codigo[:6].upper()]
            erros_simples.append({
                "codigo": codigo,
                "trecho": trecho,
                "existe": False,
                "similares": similares[:3],
            })

    if not erros_simples and not banco_bncc:
        return []

    # Monta contexto para o Claude
    contexto_banco = ""
    if banco_bncc:
        # Filtra apenas os relevantes para os códigos declarados
        relevantes = {}
        for codigo in codigos_declarados:
            if codigo in banco_bncc:
                relevantes[codigo] = banco_bncc[codigo]
        contexto_banco = f"\nHABILIDADES BNCC DE REFERÊNCIA:\n{formatar_habilidades_para_prompt(relevantes)}"

    erros_info = ""
    if erros_simples:
        erros_info = "\nCÓDIGOS NÃO ENCONTRADOS NO BANCO:\n" + "\n".join(
            f"- {e['codigo']}: {'Similares: ' + ', '.join(e['similares']) if e['similares'] else 'sem similar encontrado'}"
            for e in erros_simples
        )

    user = f"""Verifique os códigos BNCC no trecho a seguir.
{contexto_banco}
{erros_info}

TRECHOS DO DOCUMENTO COM CÓDIGOS BNCC:
{chr(10).join(f'[{i+1}] {t}' for i, t in enumerate(trechos))}

Identifique erros de grafia, código inexistente ou incompatível com componente/ano declarado."""

    resposta = _chamar_claude(client, SYSTEM_VERIFICAR_ESCRITA, user)
    return _extrair_json_da_resposta(resposta)


def verificar_alinhamento_conteudo(
    client: anthropic.Anthropic,
    texto_numerado: str,
    codigos_declarados: List[str],
    banco_bncc: Dict[str, dict],
) -> List[dict]:
    """
    Verifica se o conteúdo da lição realmente trabalha cada habilidade declarada.
    Retorna lista de desalinhamentos.
    """
    if not codigos_declarados:
        return []

    # Monta a lista de habilidades declaradas com descrição
    habilidades_declaradas = []
    for codigo in codigos_declarados:
        if codigo in banco_bncc:
            dados = banco_bncc[codigo]
            habilidades_declaradas.append(
                f"{codigo}: {dados['habilidade']} [{dados.get('componente', '')}]"
            )
        else:
            habilidades_declaradas.append(f"{codigo}: (não encontrado no banco)")

    if not habilidades_declaradas:
        return []

    user = f"""HABILIDADES BNCC DECLARADAS NA LIÇÃO:
{chr(10).join(habilidades_declaradas)}

CONTEÚDO DA LIÇÃO:
{texto_numerado[:6000]}

Verifique se o conteúdo REALMENTE trabalha cada habilidade declarada.
Para habilidades não trabalhadas, retorne o array JSON solicitado."""

    resposta = _chamar_claude(client, SYSTEM_VERIFICAR_ALINHAMENTO, user)
    desalinhamentos = _extrair_json_da_resposta(resposta)

    # Converte para formato padrão do sistema
    alteracoes = []
    for d in desalinhamentos:
        if isinstance(d, dict) and d.get("codigo"):
            alteracoes.append({
                "texto_original": d.get("codigo", ""),
                "texto_corrigido": d.get("codigo", ""),  # sem alteração no doc
                "tipo": "bncc_nao_trabalhada",
                "explicacao": f"[{d.get('codigo')}] {d.get('problema', '')} | Sugestão: {d.get('sugestao', '')}",
            })
    return alteracoes


def identificar_lacunas_bncc(
    client: anthropic.Anthropic,
    texto_numerado: str,
    codigos_declarados: List[str],
    banco_filtrado: Dict[str, dict],
) -> List[dict]:
    """
    Identifica habilidades trabalhadas mas não declaradas.
    Retorna como sugestões (sem alteração no documento).
    """
    if not banco_filtrado:
        return []

    # Remove os já declarados do banco para análise
    banco_nao_declarado = {
        k: v for k, v in banco_filtrado.items()
        if k not in codigos_declarados
    }

    if not banco_nao_declarado:
        return []

    user = f"""HABILIDADES JÁ DECLARADAS NA LIÇÃO: {', '.join(codigos_declarados) or 'nenhuma'}

HABILIDADES DISPONÍVEIS PARA ESTA FAIXA ETÁRIA (ainda não declaradas):
{formatar_habilidades_para_prompt(banco_nao_declarado, max_chars=5000)}

CONTEÚDO DA LIÇÃO:
{texto_numerado[:5000]}

Identifique quais habilidades da lista estão CLARAMENTE sendo trabalhadas no conteúdo
mas não foram declaradas. Máximo 5 sugestões, apenas com correspondência direta."""

    resposta = _chamar_claude(client, SYSTEM_IDENTIFICAR_LACUNAS, user)
    sugestoes = _extrair_json_da_resposta(resposta)

    # Converte para formato padrão — são sugestões, não erros
    alteracoes = []
    for s in sugestoes:
        if isinstance(s, dict) and s.get("codigo"):
            alteracoes.append({
                "texto_original": s.get("codigo", ""),
                "texto_corrigido": s.get("codigo", ""),
                "tipo": "bncc_lacuna_sugerida",
                "explicacao": f"Habilidade trabalhada mas não declarada: {s.get('codigo')} — {s.get('habilidade', '')} | {s.get('justificativa', '')}",
            })
    return alteracoes


def validar_bncc_completo(
    client: anthropic.Anthropic,
    texto_plano: str,
    texto_numerado: str,
    banco_bncc: Dict[str, dict],
    prefixos_faixa: List[str],
) -> List[dict]:
    """
    Ponto de entrada: executa as 3 verificações BNCC.
    Retorna lista consolidada de alterações/alertas.
    """
    codigos_declarados, _ = _extrair_declaracoes_bncc_do_doc(texto_plano)
    banco_filtrado = filtrar_por_prefixos(banco_bncc, prefixos_faixa)

    todas = []

    # 1. Verificação de escrita dos códigos
    if banco_bncc:
        erros_escrita = verificar_escrita_codigos(client, texto_plano, banco_bncc)
        todas.extend(erros_escrita)

    # 2. Alinhamento conteúdo × habilidades declaradas
    if codigos_declarados:
        desalinhamentos = verificar_alinhamento_conteudo(
            client, texto_numerado, codigos_declarados, banco_bncc
        )
        todas.extend(desalinhamentos)

    # 3. Identificação de lacunas (habilidades trabalhadas mas não declaradas)
    if banco_filtrado:
        lacunas = identificar_lacunas_bncc(
            client, texto_numerado, codigos_declarados, banco_filtrado
        )
        todas.extend(lacunas)

    return todas
