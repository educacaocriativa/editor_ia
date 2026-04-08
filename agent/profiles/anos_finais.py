"""
Perfis individuais do Ensino Fundamental Anos Finais (6º ao 9º ano) — BNCC.
"""
from .base_perfil import PerfilEtario

PERFIL_EF6 = PerfilEtario(
    chave="ef_6ano",
    nome="Ensino Fundamental — 6º Ano (11 anos)",
    faixa_anos="11 anos",
    bncc_prefixos=["EF06", "EF69"],
    max_palavras_frase=20,
    nivel_leitura="fluente",
    perfil_cognitivo="""- Transição para o pensamento formal: início da abstração
- Raciocínio hipotético-dedutivo emergente
- Identidade em formação: pré-adolescência
- Leitura fluente de textos médios com vocabulário diverso
- Escrita argumentativa simples com estrutura clara
- Álgebra e geometria como novos domínios
- Grande interesse por grupos de pares e pertencimento""",
    criterios_linguagem="""- Frases de até 20 palavras
- Vocabulário técnico-disciplinar com definição na primeira ocorrência
- Parágrafos de 5-7 frases; blocos de até 350 palavras
- Conectivos lógicos: portanto, entretanto, ademais, visto que
- Orações subordinadas complexas são adequadas
- Voz passiva e impessoal em textos expositivos""",
    criterios_pedagogicos="""- Transição didática: de concreto para abstrato
- Gêneros: artigo, reportagem, conto, poema, HQ
- Metodologia ativa: debate, seminário, projeto
- Matemática: álgebra, geometria, estatística, probabilidade
- Ciências: método científico, célula, ecossistemas""",
    criterios_humanizacao="""TOM: Respeitoso, desafiador, que reconhece a complexidade
- Reconhecer a pré-adolescência sem infantilizar
- Temas relevantes: identidade, diversidade, tecnologia, meio ambiente
- Abertura para múltiplos pontos de vista""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A fotossíntese é o processo pelo qual as plantas produzem seu próprio alimento
  usando luz solar, água e gás carbônico. Como você explicaria esse processo
  para alguém que nunca ouviu falar dele?"
❌ INADEQUADO:
  "Brinque de descobrir como as plantinhas fazem comida com o solzinho!" """,
    alertas_especificos="""⚠ Não infantilizar — linguagem mais madura é bem-vinda
⚠ Temas sensíveis (puberdade, sexualidade) com linguagem técnica e respeitosa
⚠ Atividades colaborativas: estruturar bem os papéis do grupo""",
)

PERFIL_EF7 = PerfilEtario(
    chave="ef_7ano",
    nome="Ensino Fundamental — 7º Ano (12 anos)",
    faixa_anos="12 anos",
    bncc_prefixos=["EF07", "EF69"],
    max_palavras_frase=22,
    nivel_leitura="fluente",
    perfil_cognitivo="""- Pensamento formal em desenvolvimento: abstração e generalização
- Capacidade de argumentação com evidências
- Identidade e autonomia em construção (adolescência)
- Pensamento crítico incipiente: questiona autoridade e informação
- Produção de textos argumentativos com 4-6 parágrafos
- Álgebra: equações, razão e proporção
- Alto interesse por cultura pop, redes sociais, jogos""",
    criterios_linguagem="""- Frases de até 22 palavras
- Vocabulário técnico-científico sem necessidade de tradução constante
- Parágrafos de 5-8 frases; textos de até 400 palavras por bloco
- Argumentação: tese + argumentos + conclusão
- Ironia e humor inteligente são recursos válidos""",
    criterios_pedagogicos="""- Debate estruturado como metodologia central
- Análise de fontes primárias simples (documentos, imagens históricas)
- Gêneros: editorial, crônica, ensaio curto, análise de obra
- Matemática: equações, funções, geometria analítica básica
- História: Idade Moderna, colonialismo, reformas religiosas""",
    criterios_humanizacao="""TOM: Direto, intelectualmente desafiador, que respeita a opinião
- Questionar o senso comum: "Mas será que é sempre assim?"
- Referências à cultura do adolescente de 12 anos
- Reconhecer a complexidade sem dar todas as respostas""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A Revolução Industrial transformou não só a economia, mas também as relações
  de trabalho e a vida nas cidades. Quais dessas mudanças você identificaria
  como positivas? E quais trariam problemas?"
❌ INADEQUADO:
  "Vamos descobrir juntinhos como as fábricas mudaram o mundinho das pessoas!" """,
    alertas_especificos="""⚠ Respeitar a necessidade de autonomia do adolescente
⚠ Evitar didatismo excessivo — apresentar dilemas, não só respostas
⚠ Temas controversos: apresentar múltiplas perspectivas""",
)

PERFIL_EF8 = PerfilEtario(
    chave="ef_8ano",
    nome="Ensino Fundamental — 8º Ano (13 anos)",
    faixa_anos="13 anos",
    bncc_prefixos=["EF08", "EF69"],
    max_palavras_frase=25,
    nivel_leitura="fluente",
    perfil_cognitivo="""- Pensamento formal consolidado: raciocínio abstrato e hipotético
- Argumentação com contra-argumentos e refutação
- Identidade em crise criativa: busca de valores próprios
- Leitura crítica: identifica viés, implícito, ponto de vista
- Escrita argumentativa estruturada com introdução, desenvolvimento e conclusão
- Física, Química e Biologia como campos de abstração
- Forte influência do grupo social nas escolhas""",
    criterios_linguagem="""- Frases de até 25 palavras
- Vocabulário científico e técnico sem definição obrigatória para termos do currículo
- Blocos de até 450 palavras
- Linguagem formal-acadêmica introduzida progressivamente
- Nominalização e passivização em contextos acadêmicos""",
    criterios_pedagogicos="""- Análise crítica de textos e fontes
- Gêneros: ensaio, artigo científico simplificado, resenha
- Ciências: reações químicas, leis físicas, genética básica
- História: Revoluções burguesas, Imperialismo
- Projetos de pesquisa com metodologia básica""",
    criterios_humanizacao="""TOM: Acadêmico acessível, que desafia sem intimidar
- Apresentar problemas reais sem solução fácil
- Conectar ciência e tecnologia ao cotidiano do adolescente
- Respeitar a complexidade emocional da fase""",
    exemplos_linguagem="""✅ ADEQUADO:
  "As reações de oxirredução estão presentes no nosso cotidiano: quando o ferro enferruja
  ou quando respiramos. Como você explicaria esse processo usando o conceito de
  transferência de elétrons?"
❌ INADEQUADO:
  "Que legal descobrir como o ferro fica vermelho quando fica na chuva!" """,
    alertas_especificos="""⚠ Não subestimar a capacidade de abstração — podem lidar com complexidade real
⚠ Questões existenciais e sociais são parte do conteúdo, não distração
⚠ Atividades colaborativas: papéis claros para evitar parasitismo""",
)

PERFIL_EF9 = PerfilEtario(
    chave="ef_9ano",
    nome="Ensino Fundamental — 9º Ano (14 anos)",
    faixa_anos="14 anos",
    bncc_prefixos=["EF09", "EF69"],
    max_palavras_frase=25,
    nivel_leitura="fluente",
    perfil_cognitivo="""- Pensamento formal pleno: abstração, generalização, metacognição
- Argumentação sofisticada com evidências e refutação
- Preparação para o Ensino Médio: maior autonomia intelectual
- Leitura de textos complexos com vocabulário especializado
- Projetos autorais com planejamento e execução
- Consciência política e social em formação
- Transição para o EM: maior responsabilidade pelo próprio aprendizado""",
    criterios_linguagem="""- Frases de até 25 palavras
- Vocabulário formal-científico plenamente inserido
- Blocos de até 500 palavras
- Linguagem acadêmica como preparação para o EM
- Uso pleno de conectivos lógicos e argumentativos""",
    criterios_pedagogicos="""- Preparação explícita para o Ensino Médio
- Síntese e análise de múltiplas fontes
- Gêneros: dissertação, artigo de opinião, análise literária
- Matemática: funções, geometria analítica, trigonometria básica
- História: século XX, Brasil República, geopolítica""",
    criterios_humanizacao="""TOM: Entre pares, respeitoso, que prepara para o mundo
- Conexão com o vestibular e o futuro sem gerar ansiedade
- Protagonismo em projetos reais com impacto
- Reconhecer a transição como um momento de crescimento""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A crise de 1929 evidenciou as contradições estruturais do capitalismo liberal.
  Analise como esse evento impactou o Brasil e quais foram as consequências
  para a política nacional nos anos seguintes."
❌ INADEQUADO:
  "Vamos ver o que aconteceu lá em 1929 e por que foi ruim para todo mundo!" """,
    alertas_especificos="""⚠ Transição para o EM: introduzir linguagem e metodologia do nível seguinte
⚠ Não tratar como adolescente mais novo — exigir maturidade intelectual
⚠ Projetos finais: critérios claros de avaliação""",
)
