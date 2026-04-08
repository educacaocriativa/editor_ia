"""
Processa a pasta dados/materiais/ e indexa os PDFs como base de referência.

Uso:
    python3 setup_dados.py                     # processa tudo
    python3 setup_dados.py --pasta outra/pasta # pasta personalizada

O resultado fica em dados/cache/:
  - <nome>.txt      → texto extraído de cada PDF
  - materiais_index.json → índice de busca usado pelo agente
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# Garante que o diretório raiz do projeto está no path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from word.pdf_reader import extrair_texto_pdf, extrair_metadados_pdf  # noqa: E402

PASTA_DADOS = ROOT / "dados"
PASTA_CACHE = PASTA_DADOS / "cache"

# Mapeamento de padrões no nome → chave do perfil
# Ordem importa: mais específico primeiro.
# Detecta padrões como "1 Ano", "2° Ano", "1° anos iniciais", "6° EF2"
MAPA_FAIXAS = [
    (r"educa.{0,4}infantil|EI0[123]", "educacao_infantil"),
    (r"eja|adulto", "eja"),
    (r"ensino.{0,6}m.dio|EM13|\bEM\b|em13|\b1[oº°]\s*EM\b|\b2[oº°]\s*EM\b"
     r"|\b3[oº°]\s*EM\b", "ensino_medio"),
    # EF Anos Finais: 6°, 7°, 8°, 9°
    (r"\b[6-9][oº°]?\s*(ano|EF2?\b)|ef0[6789]\b|ef[_\s-]?6[_\s-]?9\b"
     r"|ef69\b|ef89\b|ef67\b", "ef_6_9"),
    # EF Anos Iniciais 3-5: 3°, 4°, 5°
    (r"\b[345][oº°]?\s*(ano|anos iniciais)|ef0[345]\b|ef[_\s-]?3[_\s-]?5\b"
     r"|ef35\b|ef15\b", "ef_3_5"),
    # EF Anos Iniciais 1-2: 1°, 2°
    (r"\b[12][oº°]?\s*(ano|anos iniciais)|ef0[12]\b|ef[_\s-]?1[_\s-]?2\b"
     r"|ef12\b", "ef_1_2"),
]

# Componentes curriculares comuns
MAPA_COMPONENTES = [
    (r"l.ngua\s+portuguesa|portugu.s", "Língua Portuguesa"),
    (r"matem.tica", "Matemática"),
    (r"hist.ria", "História"),
    (r"geografia", "Geografia"),
    (r"ci.ncias", "Ciências"),
    (r"arte", "Arte"),
    (r"educa.{1,4}f.sica|ed\.?\s*f.sica", "Educação Física"),
    (r"ingl.s|l.ngua\s+inglesa", "Inglês"),
    (r"filosofia", "Filosofia"),
    (r"sociologia", "Sociologia"),
    (r"biologia", "Biologia"),
    (r"qu.mica", "Química"),
    (r"f.sica", "Física"),
]

# Stopwords mínimas em português para extração de palavras-chave
STOPWORDS = {
    "a", "ao", "aos", "as", "com", "da", "das", "de", "do", "dos",
    "e", "em", "é", "na", "nas", "no", "nos", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "que", "se", "um", "uma",
    "uns", "umas", "à", "às", "seu", "sua", "seus", "suas", "ele", "ela",
    "eles", "elas", "nós", "vós", "isso", "este", "essa", "esse", "mais",
    "mas", "já", "não", "ter", "ser", "estar", "também", "como",
}


def _detectar_faixas(nome_arquivo: str, trecho_texto: str) -> List[str]:
    """Detecta faixas etárias a partir do nome do arquivo e início do texto."""
    haystack = (nome_arquivo + " " + trecho_texto[:500]).lower()
    encontradas = []
    for padrao, chave in MAPA_FAIXAS:
        if re.search(padrao, haystack, re.IGNORECASE):
            encontradas.append(chave)
    return encontradas or []


def _detectar_componentes(nome_arquivo: str, trecho_texto: str) -> List[str]:
    """Detecta componentes curriculares."""
    haystack = (nome_arquivo + " " + trecho_texto[:500]).lower()
    encontrados = []
    for padrao, nome in MAPA_COMPONENTES:
        if re.search(padrao, haystack, re.IGNORECASE):
            encontrados.append(nome)
    return encontrados or []


def _extrair_palavras_chave(texto: str, top_n: int = 20) -> List[str]:
    """Extrai as palavras mais frequentes (excluindo stopwords)."""
    palavras = re.findall(r"\b[a-záàâãéèêíïóôõúçüñA-ZÁÀÂÃÉÈÊÍÏÓÔÕÚÇÜ]{4,}\b",
                          texto)
    freq: Dict[str, int] = {}
    for p in palavras:
        p_lower = p.lower()
        if p_lower not in STOPWORDS:
            freq[p_lower] = freq.get(p_lower, 0) + 1
    ordenadas = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [p for p, _ in ordenadas[:top_n]]


def processar_materiais(
    pasta_materiais: Path = None,
    verbose: bool = True,
) -> int:
    """
    Processa todos os PDFs em pasta_materiais e atualiza o índice.
    Retorna o número total de materiais indexados.
    """
    if pasta_materiais is None:
        pasta_materiais = PASTA_DADOS / "materiais"

    pasta_materiais = Path(pasta_materiais)
    PASTA_CACHE.mkdir(parents=True, exist_ok=True)

    if not pasta_materiais.exists():
        pasta_materiais.mkdir(parents=True, exist_ok=True)
        if verbose:
            print(f"[setup] Pasta criada: {pasta_materiais}")
            print("[setup] Coloque PDFs em dados/materiais/ e execute"
                  " novamente.")
        return 0

    pdfs = list(pasta_materiais.rglob("*.pdf"))
    if not pdfs:
        if verbose:
            print(f"[setup] Nenhum PDF encontrado em {pasta_materiais}")
        return 0

    if verbose:
        print(f"[setup] {len(pdfs)} PDF(s) encontrado(s) em {pasta_materiais}")

    materiais = []
    erros = 0

    for pdf_path in sorted(pdfs):
        if verbose:
            print(f"  → Processando: {pdf_path.name} ...", end=" ")

        texto = extrair_texto_pdf(str(pdf_path))
        if not texto.strip():
            if verbose:
                print("⚠ sem texto extraível, pulando.")
            erros += 1
            continue

        meta = extrair_metadados_pdf(str(pdf_path))

        # Nome do arquivo de cache (sem extensão, dentro de dados/cache/)
        nome_cache = pdf_path.stem + ".txt"
        caminho_cache = PASTA_CACHE / nome_cache

        # Salva texto extraído
        caminho_cache.write_text(texto, encoding="utf-8")

        # Caminho relativo ao projeto (para portabilidade)
        caminho_relativo = str(
            caminho_cache.relative_to(ROOT)
        )

        # Metadados derivados
        titulo = meta.get("titulo") or pdf_path.stem.replace("_", " ").title()
        faixas = _detectar_faixas(pdf_path.stem, texto)
        componentes = _detectar_componentes(pdf_path.stem, texto)
        palavras_chave = _extrair_palavras_chave(texto)
        resumo = texto[:500].replace("\n", " ").strip()

        entrada = {
            "nome": pdf_path.name,
            "titulo": titulo,
            "faixas_etarias": faixas,
            "componentes": componentes,
            "caminho_texto": caminho_relativo,
            "resumo": resumo,
            "palavras_chave": palavras_chave,
            "total_chars": len(texto),
        }
        materiais.append(entrada)

        if verbose:
            faixas_str = ", ".join(faixas) if faixas else "genérico"
            print(f"✓ ({len(texto):,} chars · {faixas_str})")

    # Salva índice
    indice = {"materiais": materiais, "total": len(materiais)}
    indice_path = PASTA_CACHE / "materiais_index.json"
    with open(indice_path, "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"\n[setup] ✅ {len(materiais)} material(is) indexado(s)"
              f" ({erros} com erro).")
        print(f"[setup] Índice salvo em: {indice_path}")

    return len(materiais)


def _main():
    parser = argparse.ArgumentParser(
        description="Indexa materiais de referência em PDF."
    )
    parser.add_argument(
        "--pasta",
        default=None,
        help="Pasta com os PDFs (padrão: dados/materiais/)",
    )
    args = parser.parse_args()

    pasta = Path(args.pasta) if args.pasta else None
    total = processar_materiais(pasta_materiais=pasta, verbose=True)
    sys.exit(0 if total >= 0 else 1)


if __name__ == "__main__":
    _main()
