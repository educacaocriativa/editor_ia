"""
Perfis individuais do Ensino Médio (1ª, 2ª e 3ª Série) — BNCC.
"""
from .base_perfil import PerfilEtario

PERFIL_EM1 = PerfilEtario(
    chave="em_1serie",
    nome="Ensino Médio — 1ª Série (15 anos)",
    faixa_anos="15 anos",
    bncc_prefixos=["EM13", "EM"],
    max_palavras_frase=28,
    nivel_leitura="crítico",
    perfil_cognitivo="""- Pensamento formal consolidado com início do pensamento crítico
- Adaptação à nova organização do EM (áreas de conhecimento)
- Capacidade de síntese e articulação entre disciplinas
- Leitura crítica: distingue fato de opinião, detecta argumentos falaciosos
- Escrita dissertativa estruturada (introdução, desenvolvimento, conclusão)
- Início da reflexão sobre projeto de vida
- Alta influência da cultura digital e redes sociais""",
    criterios_linguagem="""- Frases de até 28 palavras
- Linguagem acadêmica como registro padrão
- Blocos de até 600 palavras
- Nominalização, passivização e impessoalização adequadas
- Intertextualidade e referências culturais são esperadas""",
    criterios_pedagogicos="""- Integração entre as áreas de conhecimento (BNCC EM)
- Gêneros: dissertação, artigo científico, projeto de pesquisa
- Projeto de Vida como eixo articulador
- Itinerários formativos: aprofundamento em áreas de interesse
- Preparação para ENEM e acesso ao ensino superior""",
    criterios_humanizacao="""TOM: Intelectualmente exigente, que respeita a autonomia
- Conexão com questões sociais reais e urgentes
- Abertura para divergência e debate fundamentado
- Reconhecer a ansiedade da transição sem minimizá-la""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A análise da conjuntura política do Brasil na década de 1930 permite compreender
  como fatores econômicos, sociais e ideológicos convergiram para a ascensão
  do Estado Novo. Qual o papel das oligarquias regionais nesse processo?"
❌ INADEQUADO:
  "Vamos entender por que o Brasil ficou numa situação difícil nos anos 30!" """,
    alertas_especificos="""⚠ Exigir nível EM — sem condescendência ou simplificação excessiva
⚠ Conectar conteúdo ao ENEM e ao projeto de vida
⚠ Evitar fragmentação — articular conteúdos entre áreas""",
)

PERFIL_EM2 = PerfilEtario(
    chave="em_2serie",
    nome="Ensino Médio — 2ª Série (16 anos)",
    faixa_anos="16 anos",
    bncc_prefixos=["EM13", "EM"],
    max_palavras_frase=30,
    nivel_leitura="crítico",
    perfil_cognitivo="""- Pensamento crítico desenvolvido: análise, síntese, avaliação
- Capacidade de construção de argumentação autônoma e fundamentada
- Leitura de textos altamente especializados
- Escrita dissertativa com argumentação complexa e referências
- Pensamento científico: hipótese, experimento, análise de dados
- Reflexão ética e filosófica sobre questões contemporâneas
- Início da especialização por área de interesse""",
    criterios_linguagem="""- Frases de até 30 palavras
- Linguagem acadêmica plena com terminologia especializada
- Blocos de até 700 palavras
- Argumentação complexa: tese, antítese, síntese
- Citação e referência a fontes como prática esperada""",
    criterios_pedagogicos="""- Aprofundamento nos itinerários formativos
- Pesquisa com metodologia científica
- Gêneros: ensaio filosófico, relatório científico, análise literária
- Conexões interdisciplinares obrigatórias
- Preparação intensiva para ENEM""",
    criterios_humanizacao="""TOM: Acadêmico, que estimula o pensamento próprio
- Questões sem resposta única: dilemas éticos, filosóficos
- Autonomia intelectual como valor central
- Reconhecer a especialização crescente como conquista""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A tensão entre liberdade individual e responsabilidade coletiva permeia as
  discussões contemporâneas sobre cidadania. Como Rousseau e Locke tratariam
  a questão das redes sociais se vivessem hoje?"
❌ INADEQUADO:
  "Pense se é melhor ser livre ou seguir as regras da sociedade. O que você prefere?" """,
    alertas_especificos="""⚠ Exigir rigor metodológico nas produções escritas
⚠ Não simplificar conceitos filosóficos ou científicos complexos
⚠ Atividades avaliativas devem ter critérios explícitos""",
)

PERFIL_EM3 = PerfilEtario(
    chave="em_3serie",
    nome="Ensino Médio — 3ª Série (17 anos)",
    faixa_anos="17 anos",
    bncc_prefixos=["EM13", "EM"],
    max_palavras_frase=30,
    nivel_leitura="crítico",
    perfil_cognitivo="""- Maturidade intelectual plena para a educação básica
- Autonomia de aprendizado: planeja, executa e avalia o próprio estudo
- Síntese de todos os conhecimentos da educação básica
- Leitura e produção de textos altamente especializados
- Pensamento complexo: interdisciplinaridade, transversalidade
- Projeto de vida concreto: escolhas profissionais e acadêmicas
- Transição para a educação superior ou mundo do trabalho""",
    criterios_linguagem="""- Frases de até 30 palavras; linguagem plenamente acadêmica
- Todos os recursos linguísticos da língua culta
- Intertextualidade, polifonia e dialogismo como recursos
- Citações diretas e indiretas com rigor
- Blocos de até 800 palavras""",
    criterios_pedagogicos="""- Integração e síntese de toda a educação básica
- Redação dissertativa-argumentativa no padrão ENEM
- Projeto de conclusão de curso ou iniciação científica
- Gêneros: monografia, artigo científico, TCC
- Transição para o ensino superior ou mercado de trabalho""",
    criterios_humanizacao="""TOM: Entre pares acadêmicos, que prepara para o próximo nível
- Reconhecer a conquista da conclusão da educação básica
- Conectar conteúdo às escolhas e ao futuro próximo
- Equilíbrio entre exigência e motivação""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A redação dissertativa-argumentativa do ENEM exige a articulação de competências
  linguísticas, argumentativas e propositivas. Analise como a estrutura do texto
  dissertativo reflete uma visão de mundo e uma posição ética do autor."
❌ INADEQUADO:
  "Agora que você está quase terminando o colégio, vamos ver como escrever bem!" """,
    alertas_especificos="""⚠ Tratamento como pré-universitário, não como estudante da educação básica menor
⚠ ENEM deve ser referência explícita no nível de exigência
⚠ Projeto de vida: não impor trajetórias, mas ampliar possibilidades""",
)
