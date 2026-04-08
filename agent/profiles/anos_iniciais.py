"""
Perfis individuais do Ensino Fundamental Anos Iniciais (1º ao 5º ano) — BNCC.
"""
from .base_perfil import PerfilEtario

PERFIL_EF1 = PerfilEtario(
    chave="ef_1ano",
    nome="Ensino Fundamental — 1º Ano (6 anos)",
    faixa_anos="6 anos",
    bncc_prefixos=["EF01"],
    max_palavras_frase=8,
    nivel_leitura="emergente",
    perfil_cognitivo="""- Alfabetização inicial: fase silábico-alfabética
- Consciência fonológica em desenvolvimento
- Leitura com apoio: palavras e frases simples
- Escrita emergente: letra de forma maiúscula
- Contagem e numerais até 10 com objetos concretos
- Atenção concentrada: 20-25 minutos
- Aprendizado por imitação, repetição e jogo""",
    criterios_linguagem="""- Frases de até 8 palavras, vocabulário do cotidiano imediato
- Palavras com sílabas simples (CV) predominantes
- Repetição intencional de estruturas para fixação
- Uma ideia por frase; parágrafos de 2-3 frases
- Textos curtos: máximo 80 palavras por bloco
- Fontes grandes, espaçamento amplo, ilustrações integradas""",
    criterios_pedagogicos="""- Alfabetização como eixo central de todas as áreas
- Textos funcionais: lista, bilhete, legenda, cantiga
- Jogos de palavras, rimas, parlendas e trava-línguas
- Contagem, adição e subtração com objetos concretos
- Rotina diária como texto didático (calendário, chamada)""",
    criterios_humanizacao="""TOM: Acolhedor, encorajador, cheio de descobertas
- "Você já sabe ler isso!", "Que legal que você descobriu!"
- Personagens infantis que aprendem junto com o leitor
- Conexão com a escola, a família e o bairro""",
    exemplos_linguagem="""✅ ADEQUADO:
  "O gato mia. A Ana viu o gato. Ele é bonito!"
  "Hoje é segunda-feira. Qual é o dia de amanhã?"
❌ INADEQUADO:
  "Os felinos domésticos são mamíferos carnívoros amplamente distribuídos." """,
    alertas_especificos="""⚠ Nunca assumir que a criança já sabe ler — texto deve ter suporte pictórico
⚠ Instruções orais, não escritas
⚠ Atividades de no máximo 3 etapas simples
⚠ Sem leitura silenciosa — sempre leitura compartilhada ou em voz alta""",
)

PERFIL_EF2 = PerfilEtario(
    chave="ef_2ano",
    nome="Ensino Fundamental — 2º Ano (7 anos)",
    faixa_anos="7 anos",
    bncc_prefixos=["EF02"],
    max_palavras_frase=10,
    nivel_leitura="em desenvolvimento",
    perfil_cognitivo="""- Alfabetização consolidando: leitura silábica → fluente simples
- Leitura de palavras e frases com autonomia crescente
- Escrita com erros ortográficos esperados (fase alfabética)
- Adição e subtração com agrupamento de dezenas
- Início da escrita de textos curtos (3-5 frases)
- Compreensão de sequência narrativa: início, meio e fim
- Sociabilidade e trabalho em dupla bem-sucedido""",
    criterios_linguagem="""- Frases de até 10 palavras
- Vocabulário do cotidiano com até 3 palavras novas por página
- Textos de até 120 palavras com quebras visuais (subtítulos, imagens)
- Pontuação básica: ponto, vírgula, interrogação, exclamação
- Parágrafos de 3-4 frases com uma ideia central""",
    criterios_pedagogicos="""- Fluência leitora como objetivo central
- Tipos textuais: conto, fábula, história em quadrinhos, receita
- Matemática com situações-problema do cotidiano
- Produção escrita orientada: completar, reescrever, criar com modelo
- Oralidade estruturada: roda de conversa, reconto""",
    criterios_humanizacao="""TOM: Encorajador, narrativo, próximo
- Protagonismo infantil nas situações-problema
- Humor suave e surpresa nas histórias
- "Você consegue descobrir!", "Vamos pensar juntos?" """,
    exemplos_linguagem="""✅ ADEQUADO:
  "A Bia foi ao mercado comprar frutas. Ela escolheu maçã, banana e uva.
  Quantas frutas a Bia comprou no total?"
❌ INADEQUADO:
  "Resolva as operações matemáticas fundamentais de adição e subtração
  com reagrupamento de unidades e dezenas." """,
    alertas_especificos="""⚠ Erros ortográficos são esperados — não tratar como falha grave no material
⚠ Atividades escritas com no máximo 5 linhas para resposta
⚠ Sempre oferecer modelo ou exemplo antes de pedir produção autônoma""",
)

PERFIL_EF3 = PerfilEtario(
    chave="ef_3ano",
    nome="Ensino Fundamental — 3º Ano (8 anos)",
    faixa_anos="8 anos",
    bncc_prefixos=["EF03", "EF15"],
    max_palavras_frase=14,
    nivel_leitura="em desenvolvimento",
    perfil_cognitivo="""- Alfabetização consolidada: leitura fluente de textos simples
- Ortografia em desenvolvimento: regras básicas adquiridas
- Início do pensamento operatório-concreto pleno
- Multiplicação e divisão como conceitos emergentes
- Noção de espaço e tempo histórico básica
- Produção de textos curtos com coerência
- Interesse por aventura, humor e histórias do cotidiano""",
    criterios_linguagem="""- Frases de até 14 palavras
- Vocabulário disciplinar introduzido com definição
- Parágrafos de 3-5 frases; textos de até 200 palavras por bloco
- Conectivos básicos: porque, então, mas, e, também
- Orações subordinadas simples são aceitáveis""",
    criterios_pedagogicos="""- Leitura autônoma como prática diária
- Gêneros: conto, lenda, notícia infantil, verbete, poesia
- Matemática: multiplicação, divisão, frações simples
- Ciências: observação, registro, hipótese elementar
- Pesquisa simples com orientação do professor""",
    criterios_humanizacao="""TOM: Curioso, desafiador, com conexão ao cotidiano
- Perguntas que provocam reflexão: "O que você faria se...?"
- Situações do universo de 8 anos: escola, amigos, esportes, games
- Valorização da opinião do estudante""",
    exemplos_linguagem="""✅ ADEQUADO:
  "As plantas fazem fotossíntese para se alimentar. Você sabe o que elas precisam
  para fazer isso? Pense: o que uma planta precisa para crescer?"
❌ INADEQUADO:
  "O processo metabólico de fotossíntese converte energia luminosa em energia química." """,
    alertas_especificos="""⚠ Não assumir que a multiplicação já está automatizada
⚠ Textos expositivos: máximo 200 palavras antes de uma atividade
⚠ Mapas e gráficos: sempre com legenda e instrução de leitura""",
)

PERFIL_EF4 = PerfilEtario(
    chave="ef_4ano",
    nome="Ensino Fundamental — 4º Ano (9 anos)",
    faixa_anos="9 anos",
    bncc_prefixos=["EF04", "EF35", "EF15"],
    max_palavras_frase=16,
    nivel_leitura="em desenvolvimento",
    perfil_cognitivo="""- Leitura fluente com compreensão inferencial básica
- Ortografia: regras consolidadas, erros residuais
- Pensamento lógico: classifica, ordena, relaciona causas
- Frações, decimais simples e geometria básica
- Noção de tempo histórico: séculos e décadas
- Produção de textos com 2-3 parágrafos coesos
- Interesse por humor, aventura, mistério e tecnologia""",
    criterios_linguagem="""- Frases de até 16 palavras
- Vocabulário disciplinar com glossário integrado
- Parágrafos de 4-6 frases; blocos de até 250 palavras
- Uso correto de conectivos de causa, consequência e oposição
- Voz passiva analítica em contextos expositivos""",
    criterios_pedagogicos="""- Inferência e interpretação como habilidades centrais
- Gêneros: reportagem, artigo de opinião simples, conto de mistério
- Matemática: frações equivalentes, geometria, probabilidade elementar
- História: Brasil colonial, diversidade cultural
- Projetos interdisciplinares com produto final""",
    criterios_humanizacao="""TOM: Investigativo, respeitoso, com humor inteligente
- Desafios cognitivos: "Descubra o padrão", "Prove sua hipótese"
- Referências ao universo digital e pop da criança de 9 anos
- Autonomia crescente: "Pesquise e traga para a roda" """,
    exemplos_linguagem="""✅ ADEQUADO:
  "Durante o período colonial, o Brasil exportava principalmente açúcar para a Europa.
  Por que você acha que o açúcar era tão valioso naquela época?"
❌ INADEQUADO:
  "Analise criticamente as relações de produção no Brasil Colônia sob a perspectiva
  do materialismo histórico." """,
    alertas_especificos="""⚠ Atividades de múltiplas etapas devem ser numeradas
⚠ Glossário ou notas de rodapé para termos técnicos novos
⚠ Evitar texto contínuo acima de 250 palavras sem atividade intermediária""",
)

PERFIL_EF5 = PerfilEtario(
    chave="ef_5ano",
    nome="Ensino Fundamental — 5º Ano (10 anos)",
    faixa_anos="10 anos",
    bncc_prefixos=["EF05", "EF35", "EF15"],
    max_palavras_frase=18,
    nivel_leitura="em desenvolvimento",
    perfil_cognitivo="""- Leitura autônoma com compreensão de textos médios
- Início do raciocínio hipotético-dedutivo simples
- Escrita com coesão e coerência em 3-5 parágrafos
- Operações com números decimais e frações
- Noção de tempo histórico: linha do tempo e contexto
- Pensamento científico elementar: observar, registrar, concluir
- Transição para os Anos Finais: maior abstração""",
    criterios_linguagem="""- Frases de até 18 palavras
- Vocabulário técnico-científico introduzido com exemplos concretos
- Parágrafos de 4-6 frases; textos de até 300 palavras por bloco
- Conectivos de causa, consequência, concessão e finalidade
- Figuras de linguagem simples: comparação, metáfora""",
    criterios_pedagogicos="""- Pesquisa orientada com fonte e registro
- Argumentação simples com 2-3 justificativas
- Gêneros: artigo de opinião, conto de ficção científica, verbete
- Matemática: álgebra elementar, geometria, estatística básica
- Preparação gradual para a transição aos Anos Finais""",
    criterios_humanizacao="""TOM: Desafiador, protagonista, com conexão com o mundo real
- Temas do cotidiano expandido: meio ambiente, tecnologia, diversidade
- Autonomia intelectual: "O que você pensa sobre isso?"
- Referências a fenômenos reais próximos""",
    exemplos_linguagem="""✅ ADEQUADO:
  "O desmatamento da Amazônia afeta o clima de todo o Brasil. Você saberia
  explicar como isso acontece? Pense nas chuvas da sua cidade."
❌ INADEQUADO:
  "Correlacione as variáveis socioeconômicas do desmatamento amazônico com
  os índices pluviométricos das regiões Centro-Oeste e Sudeste." """,
    alertas_especificos="""⚠ Ainda não é Anos Finais: evitar excesso de abstração
⚠ Atividades de pesquisa precisam de roteiro claro
⚠ Preparar o estudante para mudanças de metodologia no 6º ano""",
)
