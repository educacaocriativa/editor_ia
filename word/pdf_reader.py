"""
Extração de texto de arquivos PDF.
Tenta pdfplumber/pypdf primeiro (PDFs digitais).
Se não houver texto, usa OCR via pytesseract (PDFs escaneados).
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

    # Tenta pdfplumber (melhor qualidade de extração — PDFs digitais)
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
        if partes:
            return "\n\n".join(partes)
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback OCR: para PDFs escaneados (imagens)
    return _extrair_texto_ocr(caminho)


def _extrair_texto_ocr(caminho: str) -> str:
    """Converte páginas do PDF em imagens e aplica OCR (português)."""
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError:
        return ""

    try:
        # Limita a 30 páginas por PDF para não travar a VM
        imagens = convert_from_path(caminho, dpi=200, last_page=30)
        partes = []
        for img in imagens:
            texto = pytesseract.image_to_string(img, lang="por")
            if texto.strip():
                partes.append(texto)
        return "\n\n".join(partes)
    except Exception:
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
