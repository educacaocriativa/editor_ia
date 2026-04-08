"""
Gerencia a base de materiais de referência.

Fluxo:
1. setup_dados.py processa os PDFs e grava o índice em dados/cache/
2. Esta classe carrega o índice e responde consultas de contexto
   para injeção nos prompts das skills
"""
import json
from pathlib import Path
from typing import List, Dict, Optional

PASTA_CACHE = Path(__file__).parent.parent / "dados" / "cache"
ARQUIVO_INDICE = PASTA_CACHE / "materiais_index.json"


# ── Índice (estrutura salva em JSON) ────────────────────────────────────────
# {
#   "materiais": [
#     {
#       "nome": "nome_arquivo.pdf",
#       "titulo": "...",
#       "faixas_etarias": ["ef_3_5"],
#       "componentes": ["Língua Portuguesa"],
#       "caminho_texto": "dados/cache/nome_arquivo.txt",
#       "resumo": "primeiros 500 chars",
#       "palavras_chave": ["lista", "de", "palavras"],
#       "total_chars": 12345,
#     }
#   ]
# }


class MateriaisReferencia:
    """Interface de acesso à base de materiais de referência."""

    def __init__(self):
        self._indice: List[Dict] = []
        self._carregado = False

    def carregar(self) -> int:
        """Carrega o índice do disco. Retorna número de materiais."""
        if not ARQUIVO_INDICE.exists():
            self._indice = []
            self._carregado = True
            return 0
        try:
            with open(ARQUIVO_INDICE, encoding="utf-8") as f:
                dados = json.load(f)
            self._indice = dados.get("materiais", [])
            self._carregado = True
            return len(self._indice)
        except Exception:
            self._indice = []
            self._carregado = True
            return 0

    def _garantir_carregado(self):
        if not self._carregado:
            self.carregar()

    def total(self) -> int:
        self._garantir_carregado()
        return len(self._indice)

    def listar(self) -> List[Dict]:
        self._garantir_carregado()
        return self._indice

    def _ler_texto(self, caminho_texto: str) -> str:
        """Lê o texto de um material do cache."""
        path = Path(caminho_texto)
        if not path.is_absolute():
            path = Path(__file__).parent.parent / path
        if path.exists():
            try:
                return path.read_text(encoding="utf-8")
            except Exception:
                return ""
        return ""

    # Mapa de agrupamento: chave individual → chaves de grupo compatíveis
    _GRUPO_FAIXAS = {
        "ei_maternal":    ["ei_maternal", "educacao_infantil"],
        "ei_infantil_i":  ["ei_infantil_i", "ei_infantil_ii", "educacao_infantil"],
        "ei_infantil_ii": ["ei_infantil_i", "ei_infantil_ii", "educacao_infantil"],
        "ei_pre_i":       ["ei_pre_i", "ei_pre_ii", "educacao_infantil"],
        "ei_pre_ii":      ["ei_pre_i", "ei_pre_ii", "educacao_infantil"],
        "ef_1ano": ["ef_1ano", "ef_1_2", "ef12"],
        "ef_2ano": ["ef_1ano", "ef_2ano", "ef_1_2", "ef12"],
        "ef_3ano": ["ef_3ano", "ef_3_5", "ef35", "ef15"],
        "ef_4ano": ["ef_3ano", "ef_4ano", "ef_5ano", "ef_3_5", "ef35", "ef15"],
        "ef_5ano": ["ef_4ano", "ef_5ano", "ef_3_5", "ef35", "ef15"],
        "ef_6ano": ["ef_6ano", "ef_6_9", "ef69", "ef67"],
        "ef_7ano": ["ef_6ano", "ef_7ano", "ef_8ano", "ef_6_9", "ef69"],
        "ef_8ano": ["ef_7ano", "ef_8ano", "ef_9ano", "ef_6_9", "ef69", "ef89"],
        "ef_9ano": ["ef_8ano", "ef_9ano", "ef_6_9", "ef69", "ef89"],
        "em_1serie": ["em_1serie", "ensino_medio"],
        "em_2serie": ["em_1serie", "em_2serie", "em_3serie", "ensino_medio"],
        "em_3serie": ["em_2serie", "em_3serie", "ensino_medio"],
    }

    def _score_relevancia(
        self,
        material: Dict,
        faixa_etaria_chave: str,
        termos: List[str],
    ) -> float:
        """
        Pontuação de relevância com prioridade ao ano exato,
        depois ao grupo próximo, depois genérico.
        """
        score = 0.0
        faixas = material.get("faixas_etarias", [])

        if faixas:
            # Correspondência exata ao ano/série
            if faixa_etaria_chave in faixas:
                score += 20.0
            else:
                # Correspondência ao grupo de anos próximos
                grupos = self._GRUPO_FAIXAS.get(faixa_etaria_chave, [])
                for f in faixas:
                    if f in grupos:
                        score += 8.0
                        break
        else:
            score += 2.0  # material genérico: baixa prioridade

        # Palavras-chave temáticas
        palavras_mat = set(
            w.lower() for w in material.get("palavras_chave", [])
        )
        for termo in termos:
            if termo.lower() in palavras_mat:
                score += 1.0

        return score

    def obter_contexto_referencia(
        self,
        faixa_etaria_chave: str,
        termos_relevantes: List[str] = None,
        max_chars: int = 4000,
        max_materiais: int = 3,
        componente: str = "",
    ) -> str:
        """
        Retorna trechos de materiais de referência relevantes para
        injeção nos prompts das skills.

        faixa_etaria_chave: chave do perfil (ex: "ef_3_5")
        termos_relevantes: palavras extraídas do documento em revisão
        max_chars: limite total de caracteres do contexto retornado
        componente: filtra pelo componente curricular (ex: "História")
        """
        self._garantir_carregado()
        if not self._indice:
            return ""

        termos = termos_relevantes or []

        # Filtra por componente se informado
        candidatos = self._indice
        if componente:
            comp_lower = componente.lower()
            filtrados = [
                m for m in candidatos
                if any(
                    comp_lower in c.lower()
                    for c in m.get("componentes", [])
                )
            ]
            # Se não houver materiais da disciplina, usa todos
            candidatos = filtrados if filtrados else candidatos

        # Ordena por relevância
        ordenados = sorted(
            candidatos,
            key=lambda m: self._score_relevancia(
                m, faixa_etaria_chave, termos
            ),
            reverse=True,
        )

        partes = []
        chars_usados = 0

        for mat in ordenados[:max_materiais]:
            texto = self._ler_texto(mat.get("caminho_texto", ""))
            if not texto:
                continue

            # Limita o trecho por material
            chars_por_mat = max_chars // max_materiais
            trecho = texto[:chars_por_mat]
            if len(texto) > chars_por_mat:
                trecho += "\n[...trecho truncado...]"

            nome = mat.get("titulo") or mat.get("nome", "material")
            partes.append(
                f"--- MATERIAL DE REFERÊNCIA: {nome} ---\n{trecho}"
            )
            chars_usados += len(trecho)
            if chars_usados >= max_chars:
                break

        if not partes:
            return ""

        return (
            "=== BASE DE REFERÊNCIA (materiais aprovados) ===\n"
            "Use como parâmetro de estilo, estrutura e nível de linguagem.\n\n"
            + "\n\n".join(partes)
        )

    def obter_exemplos_escrita(
        self,
        faixa_etaria_chave: str,
        max_chars: int = 2000,
        componente: str = "",
    ) -> str:
        """
        Retorna trechos curtos como exemplos de escrita aprovada.
        Usado especificamente nas skills de humanização e pedagógico.
        """
        return self.obter_contexto_referencia(
            faixa_etaria_chave,
            max_chars=max_chars,
            max_materiais=2,
            componente=componente,
        )


# Instância global (singleton) — carregada uma vez
_instancia: Optional[MateriaisReferencia] = None


def obter_materiais() -> MateriaisReferencia:
    """Retorna a instância global, carregando se necessário."""
    global _instancia
    if _instancia is None:
        _instancia = MateriaisReferencia()
        _instancia.carregar()
    return _instancia


def recarregar_materiais() -> int:
    """Força recarregamento do índice (após novo processamento)."""
    global _instancia
    _instancia = MateriaisReferencia()
    return _instancia.carregar()
