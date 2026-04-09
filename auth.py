"""
Gerenciamento de usuários do Editor IA.
Armazena em dados/usuarios.json com senha hasheada (sha256 + salt).

Usuário admin padrão criado automaticamente na primeira execução:
  login: admin  |  senha: admin123
"""
import hashlib
import json
import secrets
from datetime import datetime
from pathlib import Path

USUARIOS_PATH = Path(__file__).parent / "dados" / "usuarios.json"


# ── helpers internos ──────────────────────────────────────────────────────────

def _hash(senha: str, salt: str) -> str:
    return hashlib.sha256((senha + salt).encode()).hexdigest()


def _carregar() -> dict:
    if not USUARIOS_PATH.exists():
        USUARIOS_PATH.parent.mkdir(parents=True, exist_ok=True)
        _salvar({"users": []})
        criar_usuario("admin", "admin123", "admin")
    with open(USUARIOS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _salvar(dados: dict) -> None:
    USUARIOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(USUARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# ── API pública ───────────────────────────────────────────────────────────────

def verificar_login(username: str, password: str) -> bool:
    """Função passada ao auth= do Gradio."""
    dados = _carregar()
    for u in dados["users"]:
        if u["username"] == username:
            return u["password_hash"] == _hash(password, u["salt"])
    return False


def get_role(username: str) -> str:
    """Retorna 'admin' ou 'user'. Retorna '' se não encontrado."""
    dados = _carregar()
    for u in dados["users"]:
        if u["username"] == username:
            return u.get("role", "user")
    return ""


def criar_usuario(username: str, password: str, role: str = "user"):
    """Cria novo usuário. Retorna (ok: bool, msg: str)."""
    username = username.strip()
    if not username or not password:
        return False, "Informe usuário e senha."
    dados = _carregar()
    for u in dados["users"]:
        if u["username"] == username:
            return False, f"Usuário '{username}' já existe."
    salt = secrets.token_hex(16)
    dados["users"].append({
        "username": username,
        "password_hash": _hash(password, salt),
        "salt": salt,
        "role": role,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ultimo_acesso": "—",
        "total_revisoes": 0,
    })
    _salvar(dados)
    return True, f"✅ Usuário '{username}' criado com perfil '{role}'."


def editar_usuario(username: str, nova_senha: str = "", novo_role: str = ""):
    """Atualiza senha e/ou role. Retorna (ok, msg)."""
    username = username.strip()
    dados = _carregar()
    for u in dados["users"]:
        if u["username"] == username:
            if nova_senha.strip():
                u["salt"] = secrets.token_hex(16)
                u["password_hash"] = _hash(nova_senha.strip(), u["salt"])
            if novo_role:
                u["role"] = novo_role
            _salvar(dados)
            return True, f"✅ Usuário '{username}' atualizado."
    return False, f"Usuário '{username}' não encontrado."


def excluir_usuario(username: str):
    """Remove usuário. Não permite excluir o próprio admin logado."""
    username = username.strip()
    dados = _carregar()
    admins = [u for u in dados["users"] if u.get("role") == "admin"]
    alvo = next((u for u in dados["users"] if u["username"] == username), None)
    if alvo is None:
        return False, "Usuário não encontrado."
    if alvo.get("role") == "admin" and len(admins) <= 1:
        return False, "Não é possível excluir o único administrador."
    dados["users"] = [u for u in dados["users"] if u["username"] != username]
    _salvar(dados)
    return True, f"✅ Usuário '{username}' excluído."


def registrar_atividade(username: str) -> None:
    """Incrementa contador e atualiza último acesso."""
    dados = _carregar()
    for u in dados["users"]:
        if u["username"] == username:
            u["ultimo_acesso"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            u["total_revisoes"] = u.get("total_revisoes", 0) + 1
            break
    _salvar(dados)


def listar_usuarios() -> list[dict]:
    """Retorna lista de usuários sem os campos de hash/salt."""
    dados = _carregar()
    return [
        {
            "Usuário": u["username"],
            "Perfil": u.get("role", "user"),
            "Criado em": u.get("criado_em", "—"),
            "Último acesso": u.get("ultimo_acesso", "—"),
            "Revisões": u.get("total_revisoes", 0),
        }
        for u in dados["users"]
    ]
