import os

# Anthropic
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-opus-4-6"

# Autor das revisões no controle de alterações do Word
AUTOR_REVISAO = "Editor IA"

# Número de verificações de fatos
VERIFICACOES_FATOS = 5

# Faixas etárias disponíveis
FAIXAS_ETARIAS = [
    "Educação Infantil (3-5 anos)",
    "1º ao 2º ano do Ensino Fundamental (6-7 anos)",
    "3º ao 5º ano do Ensino Fundamental (8-10 anos)",
    "6º ao 9º ano do Ensino Fundamental (11-14 anos)",
    "Ensino Médio (15-17 anos)",
    "EJA / Adultos",
]

# Tipos de revisão disponíveis
TIPOS_REVISAO = [
    "ortografia",
    "gramatica",
    "coesao_estilo",
    "pedagogico",
    "verificacao_fatos",
    "humanizacao",
]
