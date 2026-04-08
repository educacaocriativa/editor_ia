"""
Registro central de todos os perfis etários — BNCC.
17 perfis individuais por ano/série.
"""
from .educacao_infantil import (
    PERFIL_EI_MATERNAL,
    PERFIL_EI_INFANTIL_I,
    PERFIL_EI_INFANTIL_II,
    PERFIL_EI_PRE_I,
    PERFIL_EI_PRE_II,
)
from .anos_iniciais import (
    PERFIL_EF1, PERFIL_EF2, PERFIL_EF3, PERFIL_EF4, PERFIL_EF5,
)
from .anos_finais import (
    PERFIL_EF6, PERFIL_EF7, PERFIL_EF8, PERFIL_EF9,
)
from .ensino_medio import (
    PERFIL_EM1, PERFIL_EM2, PERFIL_EM3,
)
from .base_perfil import PerfilEtario

# Dicionário ordenado por etapa/ano — chave = perfil.chave
PERFIS: dict[str, PerfilEtario] = {
    p.chave: p for p in [
        # Educação Infantil
        PERFIL_EI_MATERNAL,
        PERFIL_EI_INFANTIL_I,
        PERFIL_EI_INFANTIL_II,
        PERFIL_EI_PRE_I,
        PERFIL_EI_PRE_II,
        # EF Anos Iniciais
        PERFIL_EF1,
        PERFIL_EF2,
        PERFIL_EF3,
        PERFIL_EF4,
        PERFIL_EF5,
        # EF Anos Finais
        PERFIL_EF6,
        PERFIL_EF7,
        PERFIL_EF8,
        PERFIL_EF9,
        # Ensino Médio
        PERFIL_EM1,
        PERFIL_EM2,
        PERFIL_EM3,
    ]
}


def obter_perfil(faixa_etaria: str) -> PerfilEtario:
    """
    Retorna o perfil correspondente à chave ou nome informado.
    Aceita: chave exata, nome completo ou correspondência parcial.
    """
    if not faixa_etaria:
        return PERFIS["ef_4ano"]  # padrão

    # Busca por chave exata
    if faixa_etaria in PERFIS:
        return PERFIS[faixa_etaria]

    # Busca por nome exato
    for p in PERFIS.values():
        if p.nome == faixa_etaria:
            return p

    # Busca parcial (case-insensitive) no nome
    faixa_lower = faixa_etaria.lower()
    for p in PERFIS.values():
        if faixa_lower in p.nome.lower():
            return p

    # Busca parcial na chave
    for chave, p in PERFIS.items():
        if faixa_lower in chave:
            return p

    # Fallback: 4º ano
    return PERFIS["ef_4ano"]
