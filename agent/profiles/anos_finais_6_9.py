from .base_perfil import PerfilEtario

PERFIL_EF_6_9 = PerfilEtario(
    chave="ef_6_9",
    nome="6º ao 9º ano do Ensino Fundamental (11-14 anos)",
    faixa_anos="11-14 anos",
    bncc_prefixos=["EF06", "EF07", "EF08", "EF09", "EF69", "EF67", "EF89"],
    max_palavras_frase=25,
    nivel_leitura="fluente",

    perfil_cognitivo="""\
- Pensamento formal em desenvolvimento: hipóteses, generalizações, raciocínio dedutivo
- Identidade em construção: forte senso crítico em relação a adultos e instituições
- Leitura fluente; capacidade de inferência e leitura nas entrelinhas
- Escrita argumentativa emergindo (6º/7º) → consolidando (8º/9º)
- Interesse crescente por questões sociais, injustiças, dilemas éticos
- Pensamento abstrato: álgebra, probabilidade, história global, língua como sistema
- Memória de trabalho ampliada: suporta textos mais longos e densos
- Alta sensibilidade a autenticidade: percebem facilmente linguagem "forçada" ou patronizante""",

    criterios_linguagem="""\
VOCABULÁRIO:
- Termos técnicos da disciplina com definição na primeira ocorrência
- Linguagem formal-didática sem ser rebuscada
- Sinônimos e paráfrases para evitar repetição
- Glossários e notas de rodapé para termos especializados

SINTAXE:
- Até 25 palavras por frase; ideal: 15-20
- Orações subordinadas múltiplas são aceitáveis
- Voz passiva usada com critério (não como default)
- Nominalizações (uso de substantivos onde verbos seriam mais claros) devem ser evitadas

REGISTRO:
- Formal-didático com abertura para registro reflexivo
- Evitar gírias forçadas que tentem "se aproximar" dos jovens artificialmente
- Pode usar 2ª pessoa ("você") ou 3ª pessoa mais formal dependendo do gênero textual
- Imperativo e indicativo alternados; subjuntivo em hipóteses e condições""",

    criterios_pedagogicos="""\
ABORDAGEM:
- Problematização real: situações do mundo contemporâneo, notícias, dilemas
- Leitura crítica: textos que exigem posicionamento do estudante
- Interdisciplinaridade: conexões entre componentes curriculares
- Pesquisa e curadoria de informação como habilidade explícita

TIPOLOGIA TEXTUAL ESPERADA:
- Argumentativo: artigo de opinião, carta de leitor, debate
- Expositivo-argumentativo: relatório, seminário, ensaio
- Literário: conto, crônica, poema, romance juvenil
- Multimodal: infográfico, mapa, gráfico, podcast, vídeo

MEDIAÇÃO PEDAGÓGICA:
- "Antes de responder, pense nos argumentos a favor e contra"
- Tabelas de análise comparativa
- Roteiro de pesquisa explícito
- Debate estruturado como estratégia recorrente

COMPETÊNCIAS GERAIS BNCC RELEVANTES:
- Pensamento científico, crítico e criativo
- Comunicação (oralidade, escrita, leitura multimodal)
- Argumentação ética e cidadã
- Empatia e cooperação""",

    criterios_humanizacao="""\
TOM: Respeitoso com a inteligência crítica do adolescente; provocativo sem ser ansioso
RECURSOS:
- Conexão com cultura jovem: redes sociais, música, jogos, séries — sem forçar
- Perguntas genuinamente abertas: sem resposta certa óbvia
- Dilemas éticos reais: "E se você fosse...?", "O que você faria?"
- Protagonismo intelectual: "Defenda sua posição", "Investigue e apresente"
- Humor inteligente: ironia, paródia, absurdo bem construído
- Vozes diversas: textos de autores variados, perspectivas múltiplas
EVITAR: tom professoral ou moralista, textos com "lição óbvia", linguagem patronizante""",

    exemplos_linguagem="""\
✅ ADEQUADO:
  "Em 1888, a escravidão foi oficialmente abolida no Brasil — mas será que isso
  significou liberdade real para os ex-escravizados? Leia o trecho a seguir e reflita."
  "A variação linguística mostra que não existe uma 'língua certa': o que existe são
  contextos diferentes para usos diferentes. Você já foi corrigido por falar de um jeito
  que era perfeitamente adequado para aquela situação?"

❌ INADEQUADO:
  "A promulgação da Lei Áurea representou o ápice do movimento abolicionista no contexto
  das relações produtivas do Segundo Reinado."
  "A variação diatópica constitui fenômeno de heterogeneidade estrutural inerente aos
  sistemas linguísticos naturais." """,

    alertas_especificos="""\
⚠ Evite toda forma de didatismo excessivo ou infantilização — o adolescente percebe e rejeita
⚠ Questões de identidade, raça, gênero e diversidade devem ser abordadas com seriedade e sem estereótipos
⚠ Não use exemplos desatualizados ou distantes da realidade digital do adolescente
⚠ Textos literários: preservar a linguagem original do autor mesmo que complexa
⚠ Atividades avaliativas: deixar critérios explícitos; rubrica é bem-vinda""",
)
