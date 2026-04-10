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
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario      TEXT NOT NULL,
                nome_original TEXT,
                path_revisado TEXT,
                path_relatorio TEXT,
                criado_em    TEXT NOT NULL
            )
        """)


_criar_tabela()


def registrar_arquivo(
    usuario: str,
    nome_original: str,
    path_revisado_tmp: str,
    path_relatorio_tmp: str,
) -> int:
    """
    Copia os arquivos temporários para dados/arquivos/ e registra no banco.
    Retorna o id do registro criado.
    """
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M")
    base = Path(nome_original).stem if nome_original else "documento"

    # Insere primeiro para obter o ID e usá-lo no nome do arquivo
    with _conn() as con:
        cur = con.execute(
            """
            INSERT INTO arquivos
                (usuario, nome_original, path_revisado, path_relatorio, criado_em)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario, base, "", "", criado_em),
        )
        arquivo_id = cur.lastrowid

    dest_rev = PASTA_ARQUIVOS / f"{base}_EDITADO_{arquivo_id}.docx"
    dest_rel = PASTA_ARQUIVOS / f"{base}_RELATORIO_{arquivo_id}.docx"

    if path_revisado_tmp and Path(path_revisado_tmp).exists():
        shutil.copy2(path_revisado_tmp, dest_rev)
    if path_relatorio_tmp and Path(path_relatorio_tmp).exists():
        shutil.copy2(path_relatorio_tmp, dest_rel)

    with _conn() as con:
        con.execute(
            """
            UPDATE arquivos
               SET path_revisado = ?, path_relatorio = ?
             WHERE id = ?
            """,
            (
                str(dest_rev) if dest_rev.exists() else "",
                str(dest_rel) if dest_rel.exists() else "",
                arquivo_id,
            ),
        )

    return arquivo_id


def listar_arquivos(usuario: str = None) -> list[dict]:
    """
    Retorna todos os arquivos. Se usuario informado, filtra por ele.
    Admins passam usuario=None para ver todos.
    """
    with _conn() as con:
        if usuario:
            rows = con.execute(
                "SELECT * FROM arquivos WHERE usuario = ? ORDER BY id DESC",
                (usuario,),
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM arquivos ORDER BY id DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def get_arquivo(arquivo_id: int) -> dict | None:
    """Retorna um registro pelo id."""
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM arquivos WHERE id = ?", (arquivo_id,)
        ).fetchone()
    return dict(row) if row else None


def excluir_arquivo(arquivo_id: int) -> tuple[bool, str]:
    """Remove registro e arquivos do disco."""
    reg = get_arquivo(arquivo_id)
    if not reg:
        return False, "Registro não encontrado."
    for campo in ("path_revisado", "path_relatorio"):
        p = Path(reg[campo]) if reg[campo] else None
        if p and p.exists():
            p.unlink()
    with _conn() as con:
        con.execute("DELETE FROM arquivos WHERE id = ?", (arquivo_id,))
    return True, "Arquivo excluído."
