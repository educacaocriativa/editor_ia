"""
Banco de dados SQLite para histórico de arquivos gerados pelo Editor IA.
Armazena em dados/historico.db e os arquivos em dados/arquivos/.
"""
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "dados" / "historico.db"
PASTA_ARQUIVOS = Path(__file__).parent / "dados" / "arquivos"

MESES_PT = {
    1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO", 4: "ABRIL",
    5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
    9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO",
}


def _data_abreviada(dt: datetime = None) -> str:
    """Retorna string no formato '10ABRIL'."""
    dt = dt or datetime.now()
    return f"{dt.day}{MESES_PT[dt.month]}"


def _nome_unico(pasta: Path, nome: str) -> Path:
    """Garante que não há colisão de nome na pasta — adiciona _2, _3 etc."""
    dest = pasta / nome
    if not dest.exists():
        return dest
    stem = Path(nome).stem
    sufixo = Path(nome).suffix
    contador = 2
    while True:
        dest = pasta / f"{stem}_{contador}{sufixo}"
        if not dest.exists():
            return dest
        contador += 1


def _conn():
    PASTA_ARQUIVOS.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    return con


def _criar_tabela():
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS arquivos (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario       TEXT NOT NULL,
                nome_original TEXT,
                path_revisado TEXT,
                path_relatorio TEXT,
                criado_em     TEXT NOT NULL,
                arquivado     INTEGER NOT NULL DEFAULT 0
            )
        """)
        # Migração segura: adiciona coluna se tabela já existia sem ela
        try:
            con.execute("ALTER TABLE arquivos ADD COLUMN arquivado INTEGER NOT NULL DEFAULT 0")
        except Exception:
            pass


_criar_tabela()


def registrar_arquivo(
    usuario: str,
    nome_original: str,
    path_revisado_tmp: str,
    path_relatorio_tmp: str,
) -> int:
    """
    Copia os arquivos temporários para dados/arquivos/ com nomenclatura:
      NomeOriginal_REVISADO10ABRIL.docx
      NomeOriginal_RELATÓRIO10ABRIL.docx
    Retorna o id do registro criado.
    """
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M")
    data_abrev = _data_abreviada()
    base = Path(nome_original).stem if nome_original else "documento"

    dest_rev = _nome_unico(PASTA_ARQUIVOS, f"{base}_REVISADO{data_abrev}.docx")
    dest_rel = _nome_unico(PASTA_ARQUIVOS, f"{base}_RELATÓRIO{data_abrev}.docx")

    if path_revisado_tmp and Path(path_revisado_tmp).exists():
        shutil.copy2(path_revisado_tmp, dest_rev)
    if path_relatorio_tmp and Path(path_relatorio_tmp).exists():
        shutil.copy2(path_relatorio_tmp, dest_rel)

    with _conn() as con:
        cur = con.execute(
            """
            INSERT INTO arquivos
                (usuario, nome_original, path_revisado, path_relatorio, criado_em, arquivado)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (
                usuario,
                base,
                str(dest_rev) if dest_rev.exists() else "",
                str(dest_rel) if dest_rel.exists() else "",
                criado_em,
            ),
        )
        return cur.lastrowid


def listar_arquivos(usuario: str = None) -> list[dict]:
    """Retorna arquivos ativos (não arquivados)."""
    with _conn() as con:
        if usuario:
            rows = con.execute(
                "SELECT * FROM arquivos WHERE usuario = ? AND arquivado = 0 ORDER BY id DESC",
                (usuario,),
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM arquivos WHERE arquivado = 0 ORDER BY id DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def listar_arquivados() -> list[dict]:
    """Retorna apenas arquivos arquivados (visível só para admins)."""
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM arquivos WHERE arquivado = 1 ORDER BY id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_arquivo(arquivo_id: int) -> dict | None:
    """Retorna um registro pelo id."""
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM arquivos WHERE id = ?", (arquivo_id,)
        ).fetchone()
    return dict(row) if row else None


def arquivar_arquivo(arquivo_id: int) -> tuple[bool, str]:
    """Marca o arquivo como arquivado (não remove do disco)."""
    reg = get_arquivo(arquivo_id)
    if not reg:
        return False, "Registro não encontrado."
    with _conn() as con:
        con.execute(
            "UPDATE arquivos SET arquivado = 1 WHERE id = ?", (arquivo_id,)
        )
    return True, f"✅ Arquivo arquivado."


def restaurar_arquivo(arquivo_id: int) -> tuple[bool, str]:
    """Restaura um arquivo arquivado de volta ao histórico ativo."""
    reg = get_arquivo(arquivo_id)
    if not reg:
        return False, "Registro não encontrado."
    with _conn() as con:
        con.execute(
            "UPDATE arquivos SET arquivado = 0 WHERE id = ?", (arquivo_id,)
        )
    return True, f"✅ Arquivo restaurado para o histórico."


def excluir_arquivo(arquivo_id: int) -> tuple[bool, str]:
    """Remove permanentemente registro e arquivos do disco (apenas admin)."""
    reg = get_arquivo(arquivo_id)
    if not reg:
        return False, "Registro não encontrado."
    for campo in ("path_revisado", "path_relatorio"):
        p = Path(reg[campo]) if reg[campo] else None
        if p and p.exists():
            p.unlink()
    with _conn() as con:
        con.execute("DELETE FROM arquivos WHERE id = ?", (arquivo_id,))
    return True, "🗑 Arquivo excluído permanentemente."
