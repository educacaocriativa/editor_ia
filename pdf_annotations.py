"""
Adiciona anotações (comentários) em PDFs usando pymupdf (fitz).
Cada mudança editorial vira uma nota sticky no local do texto original.
"""
from typing import List, Dict
import os

# Cores por tipo de alteração (RGB 0–1)
_CORES: Dict[str, tuple] = {
    "ortografia":           (0.9, 0.1, 0.1),
    "gramatica":            (0.9, 0.1, 0.1),
    "ortografia_gramatica": (0.9, 0.1, 0.1),
    "coesao_estilo":        (0.1, 0.6, 0.1),
    "pedagogico":           (0.1, 0.3, 0.9),
    "factual":              (0.8, 0.4, 0.0),
    "factual_incerto":      (0.8, 0.4, 0.0),
    "humanizacao":          (0.5, 0.0, 0.8),
    "bncc":                 (0.0, 0.5, 0.6),
    "bloom_correcao":       (0.8, 0.5, 0.0),
    "cosmovisao_qualificador": (0.2, 0.5, 0.2),
    "cruzamento":           (0.4, 0.4, 0.4),
}
_COR_PADRAO = (0.3, 0.3, 0.3)

# Rótulos legíveis para o tipo
_ROTULOS: Dict[str, str] = {
    "ortografia":           "Ortografia",
    "gramatica":            "Gramática",
    "ortografia_gramatica": "Ortografia/Gramática",
    "coesao_estilo":        "Coesão e Estilo",
    "pedagogico":           "Pedagógico",
    "factual":              "Verificação de Fatos",
    "factual_incerto":      "Fato Incerto",
    "humanizacao":          "Humanização",
    "bncc":                 "BNCC",
    "bloom_correcao":       "Taxonomia de Bloom",
    "cosmovisao_qualificador": "Cosmovisão Cristã",
    "cruzamento":           "Cruzamento",
}


def anotar_pdf(
    caminho_entrada: str,
    caminho_saida: str,
    mudancas: List[Dict],
) -> int:
    """
    Abre o PDF, busca cada texto_original e insere uma nota com a sugestão.
    Retorna o número de anotações inseridas.
    """
    try:
        import fitz  # pymupdf
    except ImportError:
        raise RuntimeError(
            "pymupdf não instalado. Execute: pip install pymupdf"
        )

    doc = fitz.open(caminho_entrada)
    total_anotacoes = 0

    for mudanca in mudancas:
        texto_orig = mudanca.get("texto_original", "").strip()
        texto_corr = mudanca.get("texto_corrigido", "").strip()
        explicacao = mudanca.get("explicacao", "").strip()
        tipo = mudanca.get("tipo", "")

        if not texto_orig:
            continue

        rotulo = _ROTULOS.get(tipo, tipo.replace("_", " ").title())
        cor = _CORES.get(tipo, _COR_PADRAO)

        conteudo_nota = f"[{rotulo}]\n"
        if texto_corr and texto_corr != texto_orig:
            conteudo_nota += f"Sugestão: {texto_corr}\n"
        if explicacao:
            conteudo_nota += f"Motivo: {explicacao}"

        # Busca o texto em todas as páginas; anota na primeira ocorrência
        anotado = False
        trecho_busca = texto_orig[:80]  # limita para maior chance de match
        for page in doc:
            resultados = page.search_for(trecho_busca, quads=False)
            if resultados:
                rect = resultados[0]
                # Highlight no trecho
                hl = page.add_highlight_annot(rect)
                hl.set_colors(stroke=cor)
                hl.update()
                # Nota sticky no canto superior esquerdo do trecho
                nota = page.add_text_annot(rect.tl, conteudo_nota)
                nota.set_colors(stroke=cor)
                nota.update()
                total_anotacoes += 1
                anotado = True
                break

    doc.save(caminho_saida, garbage=4, deflate=True)
    doc.close()
    return total_anotacoes
