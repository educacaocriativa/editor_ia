"""
Classe base que representa o perfil editorial de uma faixa etária.
Cada perfil encapsula as características específicas do estudante
e gera os blocos de contexto injetados nos prompts das skills.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class PerfilEtario:
    # Identificação
    chave: str
    nome: str
    faixa_anos: str                  # ex: "6-7 anos"
    bncc_prefixos: List[str]         # ex: ["EF01", "EF02", "EF12"]

    # Parâmetros linguísticos
    max_palavras_frase: int          # referência para sentenças ideais
    nivel_leitura: str               # "emergente", "em desenvolvimento", "fluente", "crítico"

    # Blocos de contexto (texto livre, injetado nos prompts)
    perfil_cognitivo: str            # desenvolvimento cognitivo da faixa
    criterios_linguagem: str         # regras de vocabulário, sintaxe, registro
    criterios_pedagogicos: str       # abordagem didática, sequência, scaffolding
    criterios_humanizacao: str       # tom, proximidade, recursos de engajamento
    exemplos_linguagem: str          # exemplos OK / NÃO OK de linguagem
    alertas_especificos: str         # armadilhas comuns para esta faixa

    def bloco_contexto_completo(self) -> str:
        """Retorna o bloco de contexto completo para injeção nos prompts."""
        return f"""
=== PERFIL DO PÚBLICO-ALVO: {self.nome.upper()} ({self.faixa_anos}) ===

DESENVOLVIMENTO COGNITIVO:
{self.perfil_cognitivo}

CRITÉRIOS DE LINGUAGEM (máx. ~{self.max_palavras_frase} palavras/frase):
{self.criterios_linguagem}

CRITÉRIOS PEDAGÓGICOS:
{self.criterios_pedagogicos}

HUMANIZAÇÃO E ENGAJAMENTO:
{self.criterios_humanizacao}

EXEMPLOS DE LINGUAGEM:
{self.exemplos_linguagem}

ALERTAS ESPECÍFICOS DESTA FAIXA:
{self.alertas_especificos}
""".strip()

    def bloco_linguagem(self) -> str:
        return (
            f"PÚBLICO: {self.nome} ({self.faixa_anos}) | "
            f"Nível de leitura: {self.nivel_leitura} | "
            f"Frase ideal: até {self.max_palavras_frase} palavras\n\n"
            f"{self.criterios_linguagem}\n\n"
            f"{self.exemplos_linguagem}"
        )

    def bloco_pedagogico(self) -> str:
        return (
            f"PÚBLICO: {self.nome} ({self.faixa_anos})\n\n"
            f"DESENVOLVIMENTO COGNITIVO:\n{self.perfil_cognitivo}\n\n"
            f"CRITÉRIOS PEDAGÓGICOS:\n{self.criterios_pedagogicos}\n\n"
            f"ALERTAS:\n{self.alertas_especificos}"
        )

    def bloco_humanizacao(self) -> str:
        return (
            f"PÚBLICO: {self.nome} ({self.faixa_anos})\n\n"
            f"{self.criterios_humanizacao}"
        )
