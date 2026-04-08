"""
Gerencia a configuração persistente do Editor IA.
Salva preferências em dados/configuracao.json para que o usuário
não precise reconfigurar a cada sessão.
"""
import json
from pathlib import Path
from typing import Optional

PASTA_DADOS = Path(__file__).parent.parent / "dados"
ARQUIVO_CONFIG = PASTA_DADOS / "configuracao.json"

# Caminhos padrão procurados automaticamente
BNCC_PADROES = [
    PASTA_DADOS / "bncc.xlsx",
    PASTA_DADOS / "bncc.xls",
    PASTA_DADOS / "bncc.csv",
    PASTA_DADOS / "BNCC.xlsx",
    PASTA_DADOS / "BNCC.csv",
    PASTA_DADOS / "habilidades_bncc.xlsx",
    PASTA_DADOS / "habilidades.xlsx",
]

CONFIG_PADRAO = {
    "caminho_bncc": "",
    "caminho_materiais": str(PASTA_DADOS / "materiais"),
    "perfil_padrao": "ef_3_5",
    "fazer_ortografia": True,
    "fazer_coesao": True,
    "fazer_pedagogico": True,
    "fazer_fatos": True,
    "fazer_humanizacao": True,
    "fazer_bncc": True,
}


def carregar_config() -> dict:
    """Carrega configuração do disco, criando padrão se não existir."""
    config = dict(CONFIG_PADRAO)

    if ARQUIVO_CONFIG.exists():
        try:
            with open(ARQUIVO_CONFIG, encoding="utf-8") as f:
                salvo = json.load(f)
            config.update(salvo)
        except Exception:
            pass

    # Auto-detecção da planilha BNCC se não configurada
    if not config.get("caminho_bncc"):
        for path in BNCC_PADROES:
            if path.exists():
                config["caminho_bncc"] = str(path)
                break

    return config


def salvar_config(config: dict) -> None:
    """Persiste a configuração em disco."""
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    atual = carregar_config()
    atual.update(config)
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(atual, f, ensure_ascii=False, indent=2)


def obter_caminho_bncc() -> str:
    """Retorna o caminho configurado para a planilha BNCC."""
    return carregar_config().get("caminho_bncc", "")


def obter_caminho_materiais() -> str:
    """Retorna o caminho configurado para a pasta de materiais."""
    return carregar_config().get("caminho_materiais", "")


def salvar_caminho_bncc(caminho: str) -> None:
    salvar_config({"caminho_bncc": caminho})


def salvar_caminho_materiais(caminho: str) -> None:
    salvar_config({"caminho_materiais": caminho})
