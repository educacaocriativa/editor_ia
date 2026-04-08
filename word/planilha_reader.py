"""
Lê e indexa a planilha de habilidades da BNCC (.xlsx ou .csv).

A planilha pode ter qualquer layout — o leitor detecta automaticamente
as colunas de código e descrição. Formatos suportados:
- .xlsx / .xls (Excel)
- .csv (separador detectado automaticamente)
"""
import re
import csv
from pathlib import Path
from typing import Dict, List, Optional

# Padrão de código BNCC
# EF01LP01, EF15MA02, EI03EF01, EM13LGG101, etc.
PATTERN_CODIGO = re.compile(
    r'\b(E[IFM]\d{2,3}[A-Z]{2,3}\d{2,3}[A-Z]?)\b',
    re.IGNORECASE,
)


def _detectar_codigo(valor: str) -> bool:
    """Retorna True se o valor parece ser um código BNCC."""
    if not isinstance(valor, str):
        return False
    return bool(PATTERN_CODIGO.match(valor.strip()))


def _ler_excel(caminho: str) -> List[Dict]:
    """Lê planilha Excel e retorna lista de dicionários."""
    try:
        import openpyxl
    except ImportError:
        raise ImportError(
            "openpyxl não instalado. Execute: pip install openpyxl"
        )

    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    linhas = []
    for sheet in wb.worksheets:
        cabecalho = None
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            valores = [str(v).strip() if v is not None else "" for v in row]
            if i == 0:
                cabecalho = valores
                continue
            if cabecalho and any(valores):
                linhas.append(dict(zip(cabecalho, valores)))
    wb.close()
    return linhas


def _ler_csv(caminho: str) -> List[Dict]:
    """Lê CSV com detecção automática de separador."""
    with open(caminho, encoding="utf-8-sig", errors="replace") as f:
        amostra = f.read(4096)
        f.seek(0)
        try:
            dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t|")
        except csv.Error:
            dialeto = csv.excel  # fallback: vírgula
        reader = csv.DictReader(f, dialect=dialeto)
        return [row for row in reader]


def _encontrar_coluna(cabecalhos: List[str], candidatos: List[str]) -> Optional[str]:
    """Busca o nome de coluna mais próximo de uma lista de candidatos."""
    cabecalhos_lower = {c.lower().strip(): c for c in cabecalhos}
    for cand in candidatos:
        if cand.lower() in cabecalhos_lower:
            return cabecalhos_lower[cand.lower()]
    # busca parcial
    for cand in candidatos:
        for c_lower, c_original in cabecalhos_lower.items():
            if cand.lower() in c_lower:
                return c_original
    return None


def carregar_planilha_bncc(caminho: str) -> Dict[str, dict]:
    """
    Carrega a planilha BNCC e retorna um dicionário indexado pelo código:
    {
        "EF01LP01": {
            "codigo": "EF01LP01",
            "habilidade": "Reconhecer que textos são lidos...",
            "componente": "Língua Portuguesa",
            "ano": "1º ano",
        },
        ...
    }
    """
    if not caminho:
        return {}

    path = Path(caminho)
    if not path.exists():
        return {}

    ext = path.suffix.lower()
    if ext in (".xlsx", ".xls", ".xlsm"):
        linhas = _ler_excel(caminho)
    elif ext in (".csv", ".tsv", ".txt"):
        linhas = _ler_csv(caminho)
    else:
        # Tenta Excel primeiro, depois CSV
        try:
            linhas = _ler_excel(caminho)
        except Exception:
            linhas = _ler_csv(caminho)

    if not linhas:
        return {}

    cabecalhos = list(linhas[0].keys())

    # Detecta colunas pelo nome
    col_codigo = _encontrar_coluna(cabecalhos, [
        "código", "codigo", "code", "cod", "id", "habilidade_codigo",
        "codificação", "codificacao", "cód",
    ])
    col_habilidade = _encontrar_coluna(cabecalhos, [
        "habilidade", "descrição", "descricao", "description", "texto",
        "enunciado", "habilidades", "skill",
    ])
    col_componente = _encontrar_coluna(cabecalhos, [
        "componente", "disciplina", "área", "area", "subject", "matéria", "materia",
    ])
    col_ano = _encontrar_coluna(cabecalhos, [
        "ano", "série", "serie", "etapa", "year", "grade", "ciclo",
    ])

    # Se não achou a coluna de código, procura coluna que contém códigos BNCC
    if not col_codigo:
        for col in cabecalhos:
            amostra = [l.get(col, "") for l in linhas[:20]]
            if sum(1 for v in amostra if _detectar_codigo(str(v))) >= 3:
                col_codigo = col
                break

    if not col_codigo:
        return {}

    # Constrói o índice
    banco: Dict[str, dict] = {}
    for linha in linhas:
        codigo_raw = str(linha.get(col_codigo, "")).strip()
        # Extrai o código da célula (pode vir como "(EF01LP01) texto...")
        match = PATTERN_CODIGO.search(codigo_raw)
        if not match:
            continue
        codigo = match.group(1).upper()

        habilidade = str(linha.get(col_habilidade, "")).strip() if col_habilidade else ""
        componente = str(linha.get(col_componente, "")).strip() if col_componente else ""
        ano = str(linha.get(col_ano, "")).strip() if col_ano else ""

        # Se a habilidade estiver vazia, tenta usar outros campos
        if not habilidade:
            outros = [v for k, v in linha.items() if k not in (col_codigo, col_componente, col_ano)]
            habilidade = " ".join(str(v) for v in outros if v and str(v).strip()).strip()

        banco[codigo] = {
            "codigo": codigo,
            "habilidade": habilidade,
            "componente": componente,
            "ano": ano,
        }

    return banco


def filtrar_por_prefixos(banco: Dict[str, dict], prefixos: List[str]) -> Dict[str, dict]:
    """Filtra o banco de habilidades pelos prefixos do perfil etário."""
    if not prefixos:
        return banco
    resultado = {}
    for codigo, dados in banco.items():
        for pref in prefixos:
            if codigo.upper().startswith(pref.upper()):
                resultado[codigo] = dados
                break
    return resultado


def extrair_codigos_do_texto(texto: str) -> List[str]:
    """Extrai todos os códigos BNCC encontrados em um texto."""
    codigos = PATTERN_CODIGO.findall(texto)
    return list(dict.fromkeys(c.upper() for c in codigos))  # deduplicado, ordem mantida


def formatar_habilidades_para_prompt(habilidades: Dict[str, dict], max_chars: int = 6000) -> str:
    """
    Formata o dicionário de habilidades para inclusão num prompt.
    Respeita o limite de caracteres truncando se necessário.
    """
    if not habilidades:
        return "(nenhuma habilidade carregada)"
    linhas = []
    total = 0
    for codigo, dados in sorted(habilidades.items()):
        linha = f"- {codigo}: {dados.get('habilidade', '')} [{dados.get('componente', '')} / {dados.get('ano', '')}]"
        total += len(linha)
        if total > max_chars:
            linhas.append(f"... (+{len(habilidades) - len(linhas)} habilidades omitidas por limite de espaço)")
            break
        linhas.append(linha)
    return "\n".join(linhas)
