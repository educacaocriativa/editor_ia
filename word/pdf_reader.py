"""
Extração de texto de arquivos PDF.
Tenta pypdf primeiro (já instalado); usa pdfplumber se disponível
para maior qualidade.
"""
from pathlib import Path
from typing import Optional


def extrair_texto_pdf(caminho: str) -> str:
    """
    Extrai todo o texto de um PDF, página por página.
    Retorna string vazia se o arquivo não puder ser lido.
    """
    path = Path(caminho)
    if not path.exists() or path.suffix.lower() != ".pdf":
        return ""

    # Tenta pdfplumber (melhor qualidade de extração)
    try:
        import pdfplumber
        partes = []
        with pdfplumber.open(caminho) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    partes.append(texto)
        if partes:
            return "\n\n".join(partes)
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: pypdf
    try:
        import pypdf
        partes = []
        with open(caminho, "rb") as f:
            reader = pypdf.PdfReader(f)
            for pagina in reader.pages:
                texto = pagina.extract_text()
                if texto:
                    partes.append(texto)
        return "\n\n".join(partes)
    except ImportError:
        pass
    except Exception:
        pass

    return ""


def extrair_metadados_pdf(caminho: str) -> dict:
    """Extrai metadados básicos (título, autor, criação)."""
    try:
        import pypdf
        with open(caminho, "rb") as f:
            reader = pypdf.PdfReader(f)
            meta = reader.metadata or {}
            return {
                "titulo": str(meta.get("/Title", "")),
                "autor": str(meta.get("/Author", "")),
                "paginas": len(reader.pages),
            }
    except Exception:
        return {"titulo": "", "autor": "", "paginas": 0}
