"""
Interface web do Editor IA.
Execute com: python app.py
"""
import os
import traceback

import gradio as gr

from agent.editor import revisar_documento
from agent.profiles import PERFIS
from word.extractor import extrair_texto_plano
from word.configuracao import (
    carregar_config,
    salvar_caminho_bncc,
    salvar_caminho_materiais,
)

# Carrega a chave da API na inicialização, se estiver salva na config
_cfg_init = carregar_config()
if _cfg_init.get('anthropic_api_key') and not os.environ.get('ANTHROPIC_API_KEY'):
    os.environ['ANTHROPIC_API_KEY'] = _cfg_init['anthropic_api_key']
from word.planilha_reader import carregar_planilha_bncc
from word.materiais_referencia import recarregar_materiais
from setup_dados import processar_materiais
from pathlib import Path

CSS = """
#titulo { text-align: center; margin-bottom: 0.3em; }
#subtitulo { text-align: center; color: #666; margin-bottom: 1.5em; }
.status-box { font-family: monospace; font-size: 0.88em; }
"""

OPCOES_PERFIL = [p.nome for p in PERFIS.values()]


def _ler_plano(arquivo) -> str:
    if arquivo is None:
        return ""
    try:
        return extrair_texto_plano(arquivo.name)
    except Exception:
        return ""


def _revisar(
    arquivo_principal,
    arquivo_plano,
    arquivo_bncc,
    perfil_nome,
    componente_curricular,
    fazer_ortografia,
    fazer_coesao,
    fazer_pedagogico,
    fazer_fatos,
    fazer_humanizacao,
    fazer_bncc,
    fazer_bloom,
    fazer_cruzamento,
    api_key,
    progress=gr.Progress(track_tqdm=True),
):
    if arquivo_principal is None:
        return None, None, "⚠ Envie um arquivo .docx para revisar."

    if not api_key.strip() and not os.environ.get("ANTHROPIC_API_KEY"):
        return (
            None, None,
            "⚠ Informe sua ANTHROPIC_API_KEY (ou configure via variável de"
            " ambiente).",
        )

    if api_key.strip():
        os.environ["ANTHROPIC_API_KEY"] = api_key.strip()

    # Persiste a planilha BNCC se enviada nesta sessão
    if arquivo_bncc:
        salvar_caminho_bncc(arquivo_bncc.name)

    log_msgs = []

    def cb(msg: str, pct: float):
        log_msgs.append(f"[{pct:.0%}] {msg}")
        progress(pct, desc=msg)

    try:
        plano_texto = _ler_plano(arquivo_plano)
        caminho_bncc = arquivo_bncc.name if arquivo_bncc else ""

        resultado = revisar_documento(
            caminho_docx=arquivo_principal.name,
            faixa_etaria=perfil_nome,
            plano_obras_texto=plano_texto,
            caminho_planilha_bncc=caminho_bncc,
            componente_curricular=componente_curricular,
            fazer_ortografia=fazer_ortografia,
            fazer_coesao=fazer_coesao,
            fazer_pedagogico=fazer_pedagogico,
            fazer_fatos=fazer_fatos,
            fazer_humanizacao=fazer_humanizacao,
            fazer_bncc=fazer_bncc,
            fazer_bloom=fazer_bloom,
            fazer_cruzamento=fazer_cruzamento,
            progress_callback=cb,
        )

        total = resultado["total_alteracoes"]
        linhas = [
            f"✅ Revisão concluída — {total} alteração(ões) registrada(s).\n"
        ]
        for tipo, qtd in resultado["resumo"].items():
            linhas.append(f"  • {tipo}: {qtd}")

        return (
            resultado["docx_revisado"],
            resultado["docx_relatorio"],
            "\n".join(linhas + [""] + log_msgs),
        )

    except Exception as exc:
        return (
            None, None,
            f"❌ Erro:\n{exc}\n\n{traceback.format_exc()}",
        )


# ── Configurações ────────────────────────────────────────────────────────────

def _carregar_status_config():
    """Retorna (status_bncc, status_materiais, caminho_bncc, pasta_mat)."""
    cfg = carregar_config()
    bncc_path = cfg.get("caminho_bncc", "")
    mat_path = cfg.get("caminho_materiais", "")

    # Status BNCC
    if bncc_path and Path(bncc_path).exists():
        try:
            banco = carregar_planilha_bncc(bncc_path)
            s_bncc = (
                f"✅ Planilha BNCC carregada: {Path(bncc_path).name}"
                f" ({len(banco)} habilidades)"
            )
        except Exception as e:
            s_bncc = f"⚠ Planilha BNCC com erro: {e}"
    elif bncc_path:
        s_bncc = f"⚠ Arquivo não encontrado: {bncc_path}"
    else:
        s_bncc = "ℹ Planilha BNCC não configurada (coloque em dados/bncc.xlsx)"

    # Status materiais
    from word.materiais_referencia import obter_materiais
    mats = obter_materiais()
    n = mats.total()
    if n:
        s_mat = f"✅ {n} material(is) de referência indexado(s)"
    elif Path(mat_path).exists():
        pdfs = list(Path(mat_path).rglob("*.pdf"))
        if pdfs:
            s_mat = (
                f"ℹ {len(pdfs)} PDF(s) em {mat_path}"
                " — clique em 'Processar' para indexar"
            )
        else:
            s_mat = f"ℹ Nenhum PDF em {mat_path}"
    else:
        s_mat = "ℹ Pasta de materiais não encontrada"

    return s_bncc, s_mat, bncc_path, mat_path


def _salvar_bncc_upload(arquivo):
    """Recebe upload da planilha BNCC e persiste o caminho."""
    if arquivo is None:
        return "⚠ Nenhum arquivo enviado."
    salvar_caminho_bncc(arquivo.name)
    try:
        banco = carregar_planilha_bncc(arquivo.name)
        return (
            f"✅ Planilha salva: {Path(arquivo.name).name}"
            f" ({len(banco)} habilidades)"
        )
    except Exception as e:
        return f"⚠ Erro ao ler planilha: {e}"


def _salvar_pasta_materiais(pasta: str):
    """Persiste o caminho da pasta de materiais."""
    pasta = pasta.strip()
    if not pasta:
        return "⚠ Informe o caminho da pasta."
    salvar_caminho_materiais(pasta)
    if Path(pasta).exists():
        pdfs = list(Path(pasta).rglob("*.pdf"))
        return (
            f"✅ Pasta salva: {pasta}"
            f" ({len(pdfs)} PDF(s) encontrado(s))"
        )
    return f"⚠ Pasta não encontrada: {pasta} (será criada ao processar)"


def _processar_materiais(pasta: str):
    """Executa o processamento dos PDFs de referência."""
    pasta = pasta.strip() if pasta.strip() else None
    pasta_path = Path(pasta) if pasta else None
    try:
        total = processar_materiais(pasta_materiais=pasta_path, verbose=False)
        recarregar_materiais()
        if total == 0:
            return (
                "ℹ Nenhum PDF encontrado para processar.\n"
                "Coloque arquivos .pdf na pasta de materiais"
                " e tente novamente."
            )
        return (
            f"✅ {total} material(is) processado(s)"
            " e indexado(s) com sucesso."
        )
    except Exception as e:
        return (
            f"❌ Erro ao processar materiais:\n{e}"
            f"\n\n{traceback.format_exc()}"
        )


def _salvar_api_key(chave: str):
    chave = chave.strip()
    if not chave:
        return "⚠ Informe a chave."
    from word.configuracao import salvar_config
    salvar_config({"anthropic_api_key": chave})
    os.environ["ANTHROPIC_API_KEY"] = chave
    return "✅ Chave salva e ativa nesta sessão."


# ── UI ───────────────────────────────────────────────────────────────────────

with gr.Blocks(title="Editor IA") as demo:

    gr.Markdown("# Editor IA", elem_id="titulo")
    gr.Markdown(
        "Revisão editorial inteligente de materiais didáticos —"
        " controle de alterações nativo do Word + validação BNCC.",
        elem_id="subtitulo",
    )

    with gr.Tabs():

        # ── Aba Revisão ──────────────────────────────────────────────────────
        with gr.Tab("📝 Revisão"):

            with gr.Row():
                # Entradas
                with gr.Column(scale=1):
                    gr.Markdown("### 📄 Documentos")
                    arquivo_principal = gr.File(
                        label="Arquivo .docx para revisão",
                        file_types=[".docx"],
                    )
                    arquivo_plano = gr.File(
                        label=(
                            "Plano de Obras / Guia de Estilo"
                            " (opcional, .docx)"
                        ),
                        file_types=[".docx"],
                    )
                    arquivo_bncc = gr.File(
                        label=(
                            "Planilha BNCC (opcional — se já configurada em"
                            " ⚙ Configurações, deixe em branco)"
                        ),
                        file_types=[".xlsx", ".xls", ".csv"],
                    )

                    gr.Markdown("### 👤 Perfil do Público-Alvo")
                    perfil_nome = gr.Dropdown(
                        choices=OPCOES_PERFIL,
                        value=OPCOES_PERFIL[8],  # 4º ano como padrão
                        label="Ano / Série (conforme BNCC)",
                    )
                    componente_curricular = gr.Dropdown(
                        choices=[
                            "",
                            "Arte",
                            "Ciências",
                            "Educação Física",
                            "Filosofia",
                            "Geografia",
                            "História",
                            "Inglês",
                            "Língua Portuguesa",
                            "Matemática",
                            "Sociologia",
                        ],
                        value="",
                        label=(
                            "Componente curricular (disciplina)"
                            " — filtra os materiais de referência"
                        ),
                    )

                    gr.Markdown("### 🔍 Tipos de Revisão")
                    fazer_ortografia = gr.Checkbox(
                        value=True, label="Ortografia e Gramática"
                    )
                    fazer_coesao = gr.Checkbox(
                        value=True, label="Coesão e Estilo Linguístico"
                    )
                    fazer_pedagogico = gr.Checkbox(
                        value=True,
                        label=(
                            "Adequação Pedagógica"
                            " (perfil específico por faixa)"
                        ),
                    )
                    fazer_fatos = gr.Checkbox(
                        value=True, label="Verificação de Fatos (5×)"
                    )
                    fazer_humanizacao = gr.Checkbox(
                        value=True,
                        label="Humanização da Escrita (perfil específico)",
                    )
                    fazer_bncc = gr.Checkbox(
                        value=True,
                        label=(
                            "Validação BNCC —"
                            " escrita, alinhamento e lacunas"
                        ),
                    )
                    fazer_bloom = gr.Checkbox(
                        value=True,
                        label=(
                            "Taxonomia de Bloom —"
                            " progressão cognitiva das atividades"
                        ),
                    )
                    fazer_cruzamento = gr.Checkbox(
                        value=True,
                        label=(
                            "Cruzamento de informações —"
                            " conteúdo, atividades e gabarito"
                        ),
                    )

                    gr.Markdown("### 🔑 Chave de API")
                    api_key = gr.Textbox(
                        label="ANTHROPIC_API_KEY",
                        placeholder=(
                            "sk-ant-... (ou deixe vazio se já está"
                            " no ambiente)"
                        ),
                        type="password",
                    )

                    btn = gr.Button(
                        "▶ Revisar Documento", variant="primary", size="lg"
                    )

                # Saídas
                with gr.Column(scale=1):
                    gr.Markdown("### 📥 Resultados")
                    saida_docx = gr.File(
                        label=(
                            "📝 Documento Revisado"
                            " (com controle de alterações)"
                        ),
                        interactive=False,
                    )
                    saida_relatorio = gr.File(
                        label="📊 Relatório de Revisão (.docx)",
                        interactive=False,
                    )
                    gr.Markdown("### 📋 Log de Progresso")
                    log_box = gr.Textbox(
                        label="",
                        lines=20,
                        interactive=False,
                        elem_classes=["status-box"],
                    )

            btn.click(
                fn=_revisar,
                inputs=[
                    arquivo_principal,
                    arquivo_plano,
                    arquivo_bncc,
                    perfil_nome,
                    componente_curricular,
                    fazer_ortografia,
                    fazer_coesao,
                    fazer_pedagogico,
                    fazer_fatos,
                    fazer_humanizacao,
                    fazer_bncc,
                    fazer_bloom,
                    fazer_cruzamento,
                    api_key,
                ],
                outputs=[saida_docx, saida_relatorio, log_box],
            )

        # ── Aba Configurações ────────────────────────────────────────────────
        with gr.Tab("⚙ Configurações"):

            gr.Markdown(
                "Configure os dados persistentes do Editor IA.\n"
                "Estes ajustes são salvos em `dados/configuracao.json`"
                " e carregados automaticamente a cada sessão."
            )

            # ── BNCC ────────────────────────────────────────────────────────
            with gr.Group():
                gr.Markdown("### 📊 Planilha BNCC")
                gr.Markdown(
                    "Faça upload uma vez — o caminho fica salvo e a planilha"
                    " é carregada automaticamente em todas as revisões."
                    " Formatos aceitos: `.xlsx`, `.xls`, `.csv`."
                )
                bncc_upload = gr.File(
                    label="Enviar planilha BNCC",
                    file_types=[".xlsx", ".xls", ".csv"],
                )
                bncc_status = gr.Textbox(
                    label="Status da Planilha BNCC",
                    interactive=False,
                    lines=2,
                )
                bncc_upload.upload(
                    fn=_salvar_bncc_upload,
                    inputs=[bncc_upload],
                    outputs=[bncc_status],
                )

            # ── Materiais de Referência ──────────────────────────────────────
            with gr.Group():
                gr.Markdown("### 📚 Materiais de Referência (PDFs)")
                gr.Markdown(
                    "Coloque os PDFs aprovados na pasta `dados/materiais/`"
                    " (ou em subpastas por série/componente)."
                    " Depois clique em **Processar** para indexá-los.\n\n"
                    "O agente usará esses materiais como parâmetro de estilo"
                    " e nível de linguagem durante as revisões pedagógicas"
                    " e de humanização."
                )
                pasta_mat_input = gr.Textbox(
                    label="Pasta de materiais",
                    placeholder="dados/materiais",
                    lines=1,
                )
                with gr.Row():
                    btn_salvar_pasta = gr.Button("💾 Salvar Pasta")
                    btn_processar = gr.Button(
                        "⚙ Processar Materiais", variant="primary"
                    )
                mat_status = gr.Textbox(
                    label="Status dos Materiais",
                    interactive=False,
                    lines=3,
                )
                btn_salvar_pasta.click(
                    fn=_salvar_pasta_materiais,
                    inputs=[pasta_mat_input],
                    outputs=[mat_status],
                )
                btn_processar.click(
                    fn=_processar_materiais,
                    inputs=[pasta_mat_input],
                    outputs=[mat_status],
                )

            # ── Status geral ─────────────────────────────────────────────────
            with gr.Group():
                gr.Markdown("### 🔎 Status Atual")
                with gr.Row():
                    btn_refresh = gr.Button("↻ Atualizar Status")
                status_bncc_box = gr.Textbox(
                    label="Planilha BNCC", interactive=False, lines=2
                )
                status_mat_box = gr.Textbox(
                    label="Materiais de Referência", interactive=False, lines=2
                )

                def _atualizar_status():
                    s_bncc, s_mat, _, _ = _carregar_status_config()
                    return s_bncc, s_mat

                btn_refresh.click(
                    fn=_atualizar_status,
                    inputs=[],
                    outputs=[status_bncc_box, status_mat_box],
                )

            # ── Chave de API ─────────────────────────────────────────────────
            with gr.Group():
                gr.Markdown("### 🔑 Chave de API Anthropic")
                gr.Markdown(
                    "Salve aqui sua chave para não precisar informá-la"
                    " a cada revisão. Fica armazenada localmente em"
                    " `dados/configuracao.json`."
                )
                api_key_cfg = gr.Textbox(
                    label="ANTHROPIC_API_KEY",
                    placeholder="sk-ant-...",
                    type="password",
                    value=(
                        "••••••••"
                        if carregar_config().get("anthropic_api_key")
                        else ""
                    ),
                )
                btn_salvar_key = gr.Button("💾 Salvar Chave")
                api_key_status = gr.Textbox(
                    label="Status", interactive=False, lines=1
                )
                btn_salvar_key.click(
                    fn=_salvar_api_key,
                    inputs=[api_key_cfg],
                    outputs=[api_key_status],
                )

            # Carrega status ao iniciar
            demo.load(
                fn=_atualizar_status,
                inputs=[],
                outputs=[status_bncc_box, status_mat_box],
            )

    gr.Markdown(
        "---\n> **Editor IA** · Claude Opus 4.6 · Perfis específicos por"
        " faixa etária · BNCC integrada · Processamento 100% local."
    )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
    )
