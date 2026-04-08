"""
Orquestrador principal do pipeline de revisão editorial.
"""
import os
import tempfile
from typing import List, Callable, Optional
from datetime import datetime

import anthropic
import docx

from config import AUTOR_REVISAO, VERIFICACOES_FATOS
from word.extractor import (
    extrair_paragrafos,
    montar_texto_numerado,
    extrair_texto_plano,
)
from word.track_changes import aplicar_todas_as_mudancas
from word.planilha_reader import carregar_planilha_bncc
from word.configuracao import obter_caminho_bncc
from word.materiais_referencia import obter_materiais
from agent.profiles import obter_perfil
from agent.skills.ortografia import revisar_ortografia
from agent.skills.coesao_estilo import revisar_coesao_estilo
from agent.skills.pedagogico import revisar_pedagogico
from agent.skills.verificador_fatos import verificar_fatos
from agent.skills.humanizacao import humanizar_texto
from agent.skills.bncc import validar_bncc_completo
from agent.skills.bloom import avaliar_bloom, gerar_diagnostico_bloom
from word.bloom_reader import montar_contexto_bloom
from agent.skills.cruzamento import cruzar_informacoes
from report.generator import gerar_relatorio


def revisar_documento(
    caminho_docx: str,
    faixa_etaria: str,
    plano_obras_texto: str = "",
    caminho_planilha_bncc: str = "",
    componente_curricular: str = "",
    fazer_ortografia: bool = True,
    fazer_coesao: bool = True,
    fazer_pedagogico: bool = True,
    fazer_fatos: bool = True,
    fazer_humanizacao: bool = True,
    fazer_bncc: bool = True,
    fazer_bloom: bool = True,
    fazer_cruzamento: bool = True,
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    """
    Pipeline completo de revisão editorial.

    Retorna dict com:
      docx_revisado, docx_relatorio, total_alteracoes, resumo
    """

    def log(msg: str, pct: float = 0.0):
        if progress_callback:
            progress_callback(msg, pct)
        print(f"[{pct:.0%}] {msg}")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY não configurada.")

    client = anthropic.Anthropic(api_key=api_key)

    # ── Carrega o perfil da faixa etária ─────────────────────────────────────
    perfil = obter_perfil(faixa_etaria)
    log(f"Perfil carregado: {perfil.nome}", 0.01)

    # ── Carrega planilha BNCC ────────────────────────────────────────────────
    banco_bncc = {}
    if fazer_bncc:
        bncc_path = caminho_planilha_bncc or obter_caminho_bncc()
        if bncc_path:
            log("Carregando planilha BNCC...", 0.02)
            try:
                banco_bncc = carregar_planilha_bncc(bncc_path)
                log(f"  → {len(banco_bncc)} habilidades carregadas.", 0.03)
            except Exception as e:
                log(f"  ⚠ Erro ao carregar planilha BNCC: {e}", 0.03)
        else:
            log(
                "  ℹ Planilha BNCC não configurada"
                " (validação sem banco de referência).",
                0.03,
            )

    # ── Carrega materiais de referência ──────────────────────────────────────
    materiais = obter_materiais()
    n_materiais = materiais.total()
    comp = componente_curricular.strip()
    if n_materiais:
        comp_str = f" [{comp}]" if comp else ""
        log(
            f"Base de referência: {n_materiais} material(is)"
            f" carregado(s){comp_str}.",
            0.035,
        )

    # ── Carrega planilha Taxonomia de Bloom ──────────────────────────────
    contexto_bloom = montar_contexto_bloom()
    if contexto_bloom:
        log("Taxonomia de Bloom carregada da planilha.", 0.038)

    # ── Extrai conteúdo do documento ─────────────────────────────────────────
    log("Extraindo conteúdo do documento...", 0.04)
    paragrafos = extrair_paragrafos(caminho_docx)
    texto_numerado = montar_texto_numerado(paragrafos)
    texto_plano = extrair_texto_plano(caminho_docx)

    if not texto_plano.strip():
        raise ValueError("O documento está vazio ou sem texto legível.")

    todas_as_mudancas: List[dict] = []
    etapas_concluidas = []

    flags = [
        fazer_ortografia, fazer_coesao, fazer_pedagogico,
        fazer_fatos, fazer_humanizacao, fazer_bncc, fazer_bloom,
        fazer_cruzamento,
    ]
    total_etapas = max(sum(flags), 1)
    etapa_atual = 0

    def pct(frac: float) -> float:
        base = 0.05 + (etapa_atual / total_etapas) * 0.85
        return base + frac * (0.85 / total_etapas)

    # ── Ortografia e Gramática ───────────────────────────────────────────
    if fazer_ortografia:
        log("Revisando ortografia e gramática...", pct(0.1))
        try:
            m = revisar_ortografia(client, texto_numerado)
            m = [x for x in m if isinstance(x, dict)]
            todas_as_mudancas.extend(m)
            etapas_concluidas.append(
                {"tipo": "ortografia_gramatica", "total": len(m)}
            )
            log(f"  → {len(m)} correções encontradas.", pct(1.0))
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Coesão e Estilo ──────────────────────────────────────────────────
    if fazer_coesao:
        log("Revisando coesão e estilo...", pct(0.1))
        try:
            m = revisar_coesao_estilo(client, texto_numerado)
            m = [x for x in m if isinstance(x, dict)]
            todas_as_mudancas.extend(m)
            etapas_concluidas.append(
                {"tipo": "coesao_estilo", "total": len(m)}
            )
            log(f"  → {len(m)} ajustes encontrados.", pct(1.0))
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Revisão Pedagógica (com perfil específico) ──────────────────────
    if fazer_pedagogico:
        log(
            f"Revisando adequação pedagógica"
            f" [{perfil.nome}]...",
            pct(0.1),
        )
        try:
            ctx_ped = materiais.obter_exemplos_escrita(
                perfil.chave, max_chars=2000, componente=comp
            )
            m = revisar_pedagogico(
                client,
                texto_numerado,
                faixa_etaria,
                plano_obras_texto,
                perfil=perfil,
                contexto_referencia=ctx_ped,
            )
            m = [x for x in m if isinstance(x, dict)]
            todas_as_mudancas.extend(m)
            etapas_concluidas.append(
                {"tipo": "pedagogico", "total": len(m)}
            )
            log(f"  → {len(m)} ajustes pedagógicos encontrados.", pct(1.0))
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Verificação de Fatos (5×) ────────────────────────────────────────
    if fazer_fatos:
        log(
            f"Verificando fatos ({VERIFICACOES_FATOS}×)..."
            " (pode demorar alguns minutos)",
            pct(0.1),
        )
        try:
            m = verificar_fatos(client, texto_plano, VERIFICACOES_FATOS, faixa_etaria)
            m = [x for x in m if isinstance(x, dict)]
            fatos_reais = [x for x in m if x.get("tipo") == "factual"]
            incertos = [x for x in m if x.get("tipo") == "factual_incerto"]
            todas_as_mudancas.extend(fatos_reais)
            etapas_concluidas.append({
                "tipo": "verificacao_fatos",
                "total": len(fatos_reais),
                "incertos": len(incertos),
                "detalhes": m,
            })
            log(
                f"  → {len(fatos_reais)} erros factuais,"
                f" {len(incertos)} incertos.",
                pct(1.0),
            )
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Humanização (com perfil específico) ─────────────────────────────
    if fazer_humanizacao:
        log("Humanizando a linguagem...", pct(0.1))
        try:
            ctx_hum = materiais.obter_exemplos_escrita(
                perfil.chave, max_chars=2000, componente=comp
            )
            m = humanizar_texto(
                client, texto_numerado, faixa_etaria,
                perfil=perfil, contexto_referencia=ctx_hum,
            )
            m = [x for x in m if isinstance(x, dict)]
            todas_as_mudancas.extend(m)
            etapas_concluidas.append(
                {"tipo": "humanizacao", "total": len(m)}
            )
            log(f"  → {len(m)} ajustes de humanização.", pct(1.0))
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Validação BNCC ───────────────────────────────────────────────────
    if fazer_bncc:
        log("Validando habilidades BNCC...", pct(0.1))
        try:
            m = validar_bncc_completo(
                client,
                texto_plano,
                texto_numerado,
                banco_bncc,
                perfil.bncc_prefixos,
            )
            m = [x for x in m if isinstance(x, dict)]
            # Apenas erros de escrita e desalinhamentos alteram o doc
            m_doc = [
                x for x in m
                if x.get("tipo") in (
                    "bncc_codigo_incorreto",
                    "bncc_ano_incompativel",
                    "bncc_componente_errado",
                )
            ]
            # Alertas e sugestões vão apenas para o relatório
            m_alertas = [x for x in m if x not in m_doc]
            todas_as_mudancas.extend(m_doc)
            etapas_concluidas.append({
                "tipo": "bncc",
                "total": len(m_doc),
                "alertas": len(m_alertas),
                "detalhes_bncc": m,
            })
            log(
                f"  → {len(m_doc)} erros BNCC,"
                f" {len(m_alertas)} alertas/sugestões.",
                pct(1.0),
            )
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1


    # ── Taxonomia de Bloom ──────────────────────────────────────────────
    if fazer_bloom:
        log("Classificando e corrigindo atividades (Bloom)...", pct(0.1))
        try:
            bloom_itens = avaliar_bloom(
                client, texto_numerado, faixa_etaria,
                perfil=perfil,
                contexto_planilha=contexto_bloom,
            )
            bloom_itens = [x for x in bloom_itens if isinstance(x, dict)]
            # Correções vão para o documento
            bloom_correcoes = [
                x for x in bloom_itens
                if x.get("tipo") == "bloom_correcao"
            ]
            # Classificações vão apenas para o relatório
            bloom_classificacoes = [
                x for x in bloom_itens
                if x.get("tipo") == "bloom_classificacao"
            ]
            todas_as_mudancas.extend(bloom_correcoes)
            diagnostico = gerar_diagnostico_bloom(bloom_itens)
            etapas_concluidas.append({
                "tipo": "bloom",
                "total": len(bloom_correcoes),
                "classificacoes": bloom_classificacoes,
                "diagnostico": diagnostico,
                "_todos_itens": bloom_itens,
            })
            log(
                f"  → {len(bloom_classificacoes)} atividades classificadas,"
                f" {len(bloom_correcoes)} correções propostas.",
                pct(1.0),
            )
            if diagnostico.get("julgamento"):
                log(f"  → Diagnóstico: {diagnostico['julgamento']}", pct(1.0))
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Cruzamento de informações ────────────────────────────────────────
    if fazer_cruzamento:
        log("Cruzando conteúdo, atividades e gabarito...", pct(0.1))
        try:
            m = cruzar_informacoes(
                client, texto_numerado, faixa_etaria, perfil=perfil
            )
            m = [x for x in m if isinstance(x, dict)]
            todas_as_mudancas.extend(m)
            etapas_concluidas.append(
                {"tipo": "cruzamento", "total": len(m)}
            )
            log(f"  → {len(m)} inconsistências encontradas.", pct(1.0))
        except Exception as e:
            log(f"  ⚠ Erro: {e}", pct(1.0))
        etapa_atual += 1

    # ── Aplica alterações no Word ────────────────────────────────────────
    log("Aplicando controle de alterações no Word...", 0.91)
    doc_revisado = docx.Document(caminho_docx)

    vistos: set = set()
    mudancas_unicas = []
    for m in todas_as_mudancas:
        chave = m.get("texto_original", "")
        if chave and chave not in vistos:
            vistos.add(chave)
            mudancas_unicas.append(m)

    # Diagnóstico: verifica quantas mudanças são encontradas no documento
    # Lê XML direto para capturar texto fragmentado por formatação
    def _extrair_texto_xml(doc):
        from lxml import etree
        W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        partes = []
        for elem in doc.element.body.iter(f"{{{W}}}t"):
            if elem.text:
                partes.append(elem.text)
        return " ".join(partes)

    texto_doc_completo = _extrair_texto_xml(doc_revisado)

    encontradas = [
        m for m in mudancas_unicas
        if m.get("texto_original", "") in texto_doc_completo
    ]
    nao_encontradas = [
        m for m in mudancas_unicas
        if m.get("texto_original", "") not in texto_doc_completo
    ]
    log(
        f"  {len(encontradas)}/{len(mudancas_unicas)} mudanças"
        f" localizadas no documento.",
        0.93,
    )
    for m in nao_encontradas[:5]:
        orig = m.get("texto_original", "")[:70]
        log(f"  ✗ Texto não encontrado: '{orig}'", 0.93)

    aplicar_todas_as_mudancas(
        doc_revisado, mudancas_unicas, author=AUTOR_REVISAO
    )

    tmp_dir = tempfile.mkdtemp()
    nome_base = os.path.splitext(os.path.basename(caminho_docx))[0]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_revisado = os.path.join(
        tmp_dir, f"{nome_base}_REVISADO_{ts}.docx"
    )
    doc_revisado.save(caminho_revisado)

    # ── Gera relatório ───────────────────────────────────────────────────
    log("Gerando relatório de revisão...", 0.95)
    caminho_relatorio = os.path.join(
        tmp_dir, f"{nome_base}_RELATORIO_{ts}.docx"
    )
    gerar_relatorio(
        caminho_saida=caminho_relatorio,
        nome_documento=os.path.basename(caminho_docx),
        faixa_etaria=faixa_etaria,
        perfil_nome=perfil.nome,
        todas_as_mudancas=mudancas_unicas,
        etapas=etapas_concluidas,
    )

    log("Revisão concluída com sucesso!", 1.0)

    return {
        "docx_revisado": caminho_revisado,
        "docx_relatorio": caminho_relatorio,
        "total_alteracoes": len(mudancas_unicas),
        "resumo": {e["tipo"]: e.get("total", 0) for e in etapas_concluidas},
    }
