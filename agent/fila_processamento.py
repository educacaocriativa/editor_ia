"""
Fila global de processamento entre processos.

app.py (interface Gradio) e api.py (API Flask consumida pela plataforma de
autoria) rodam como processos separados na mesma instância, compartilhando
a mesma ANTHROPIC_API_KEY. Sem coordenação, os dois processos podem chamar
a API da Anthropic ao mesmo tempo para documentos diferentes, disparando
rate limit em cascata e sobrecarregando a máquina.

Esta fila garante que apenas um documento é processado por vez em toda a
instância, venha a requisição de onde vier. Implementada com SQLite
(dados/fila.db) porque o SQLite já serializa corretamente o acesso
concorrente entre processos no mesmo disco — não precisa de Redis nem de
outro serviço externo.
"""
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Optional

DB_PATH = Path(__file__).parent.parent / "dados" / "fila.db"

_POLL_INTERVAL = 1.0        # segundos entre verificações de vez
_TIMEOUT_PADRAO = 30 * 60   # 30 min — evita espera infinita se algo travar


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH), timeout=30)
    con.row_factory = sqlite3.Row
    return con


def _criar_tabela() -> None:
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS fila (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                origem    TEXT NOT NULL,
                criado_em REAL NOT NULL
            )
        """)


_criar_tabela()


def _posicao(con: sqlite3.Connection, meu_id: int) -> int:
    """Quantos jobs na fila têm id menor que o meu (0 = é a minha vez)."""
    row = con.execute(
        "SELECT COUNT(*) AS n FROM fila WHERE id < ?", (meu_id,)
    ).fetchone()
    return row["n"]


@contextmanager
def entrar_na_fila(
    origem: str,
    log: Optional[Callable[[str], None]] = None,
    timeout: float = _TIMEOUT_PADRAO,
):
    """
    Bloqueia até ser a vez deste job (FIFO entre processos), executa o
    bloco `with`, e libera a vez para o próximo ao sair — mesmo em caso de
    exceção.

    origem: "gradio" ou "api" — apenas para depuração/log.
    log: callback opcional chamado com mensagens de status da fila.
    timeout: segundos máximos de espera antes de desistir com TimeoutError.
    """
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO fila (origem, criado_em) VALUES (?, ?)",
            (origem, time.time()),
        )
        meu_id = cur.lastrowid

    inicio = time.time()
    avisado = False
    try:
        while True:
            with _conn() as con:
                pos = _posicao(con, meu_id)
            if pos == 0:
                break
            if not avisado:
                if log:
                    log(
                        f"⏳ Na fila de processamento — {pos} "
                        f"documento(s) na frente."
                    )
                avisado = True
            if time.time() - inicio > timeout:
                with _conn() as con:
                    con.execute("DELETE FROM fila WHERE id = ?", (meu_id,))
                raise TimeoutError(
                    f"Tempo máximo de espera na fila excedido "
                    f"({timeout:.0f}s). Tente novamente em instantes."
                )
            time.sleep(_POLL_INTERVAL)

        if avisado and log:
            log("▶ Sua vez chegou — iniciando processamento.")
        yield
    finally:
        with _conn() as con:
            con.execute("DELETE FROM fila WHERE id = ?", (meu_id,))
