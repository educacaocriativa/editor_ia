"""
Extrai conteúdo estruturado de arquivos .docx para análise.
"""
from typing import List, Dict
import docx


def extrair_paragrafos(caminho: str) -> List[Dict]:
    """
    Extrai todos os parágrafos do documento com índice e texto.
    Inclui parágrafos de tabelas.

    Cada parágrafo do corpo principal também carrega
    "linhas_em_branco_apos": quantos parágrafos vazios consecutivos existem
    logo depois dele no documento original — usado para detectar espaço de
    resposta reservado para o aluno (ver agent/skills/espaco_resposta.py).
    """
    doc = docx.Document(caminho)
    paragrafos = []
    branco_pendente = 0

    # Parágrafos do corpo principal
    for i, para in enumerate(doc.paragraphs):
        texto = para.text.strip()
        if texto:
            if paragrafos:
                paragrafos[-1]["linhas_em_branco_apos"] = branco_pendente
            paragrafos.append({
                "indice": i,
                "texto": texto,
                "estilo": para.style.name,
                "fonte": "corpo",
                "linhas_em_branco_apos": 0,
            })
            branco_pendente = 0
        else:
            branco_pendente += 1

    # Parágrafos dentro de tabelas
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for para in celula.paragraphs:
                    texto = para.text.strip()
                    if texto:
                        paragrafos.append({
                            "indice": len(paragrafos),
                            "texto": texto,
                            "estilo": para.style.name,
                            "fonte": "tabela",
                        })

    return paragrafos


def montar_texto_numerado(paragrafos: List[Dict]) -> str:
    """
    Monta o texto completo com parágrafos numerados para envio ao Claude.
    Facilita a referência exata no retorno das alterações.

    Quando um parágrafo tem "linhas_em_branco_apos" > 0, emite um marcador
    "[N linha(s) em branco]" logo em seguida — sinaliza espaço em branco
    reservado (ex.: para o aluno escrever a resposta de uma atividade).
    """
    linhas = []
    for p in paragrafos:
        linhas.append(f"[{p['indice']}] {p['texto']}")
        n_branco = p.get("linhas_em_branco_apos", 0)
        if n_branco:
            linhas.append(f"[{n_branco} linha(s) em branco]")
    return "\n\n".join(linhas)


def extrair_texto_plano(caminho: str) -> str:
    """Extrai o texto completo do documento sem numeração."""
    doc = docx.Document(caminho)
    partes = []
    for para in doc.paragraphs:
        if para.text.strip():
            partes.append(para.text)
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for para in celula.paragraphs:
                    if para.text.strip():
                        partes.append(para.text)
    return "\n\n".join(partes)
