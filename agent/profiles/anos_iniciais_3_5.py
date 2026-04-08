from .base_perfil import PerfilEtario

PERFIL_EF_3_5 = PerfilEtario(
    chave="ef_3_5",
    nome="3º ao 5º ano do Ensino Fundamental (8-10 anos)",
    faixa_anos="8-10 anos",
    bncc_prefixos=["EF03", "EF04", "EF05", "EF35", "EF15"],
    max_palavras_frase=18,
    nivel_leitura="em desenvolvimento",

    perfil_cognitivo="""\
- Leitura autônoma consolidando-se: fluência adequada no 4º/5º ano
- Pensamento operatório-concreto avançado: classifica, ordena, reverte operações
- Início do raciocínio hipotético-dedutivo simples (3º→5º progressão)
- Noção de tempo histórico ampliada: antes/depois, décadas, séculos simples
- Produção escrita: parágrafos coerentes; uso de conectivos variados
- Leitura de gráficos simples e tabelas de dados
- Interesse por narrativas de aventura, mistério, humor e super-heróis
- Senso de justiça e regras sociais em formação""",

    criterios_linguagem="""\
VOCABULÁRIO:
- Pode incluir termos técnicos da área, desde que explicados na primeira ocorrência
- Até 4 palavras novas por parágrafo com definição ou glossário lateral
- Sinônimos contextuais para evitar repetição são bem-vindos
- Proibido: jargão acadêmico sem explicação, latinismos desnecessários

SINTAXE:
- Até 18 palavras por frase (ideal: 12-15)
- Orações subordinadas adverbiais e adjetivas são aceitáveis
- Evitar: mais de 2 orações encaixadas em sequência
- Permitido: voz passiva analítica em textos expositivos, com moderação

REGISTRO:
- Semiformal-didático: aproximado, mas não coloquial
- Variação entre 2ª pessoa singular e plural ("você"/"vocês"/"a turma")
- Mix de presente expositivo e passado narrativo conforme tipologia do texto
- Imperativo afirmativo nas instruções: "Leia", "Calcule", "Observe"

TEXTUALIDADE:
- Parágrafos de 3-5 frases
- Títulos e subtítulos orientadores
- Definição de termos em negrito ou caixa lateral""",

    criterios_pedagogicos="""\
ABORDAGEM:
- Concreto ↔ abstrato com ancoras visuais (diagrama, tabela, timeline)
- Resolução de problemas simples como estrutura motivadora
- Trabalho em pares e grupos referenciado no texto
- Conexão com o cotidiano da criança de 8-10 anos (escola, família, vizinhança, tecnologia)

TIPOS DE TEXTO ESPERADOS:
- Narrativo: contos, fábulas, lendas, história em quadrinhos
- Expositivo: verbete, reportagem infantil, infográfico
- Instrucional: receita, regra de jogo, manual
- Argumentativo simples: opinião com 1-2 justificativas

SEQUÊNCIA DIDÁTICA:
1. Problematização (pergunta ou situação-problema acessível)
2. Exploração com suporte (imagem, tabela, texto-base)
3. Sistematização (conceito explicado)
4. Aplicação (exercício com complexidade gradual)
5. Reflexão (o que aprendemos?)

HABILIDADES METACOGNITIVAS:
- Instruções que ensinam estratégias de leitura (prever, verificar, resumir)
- "Antes de ler, observe o título e as imagens"
- "Releia se não entendeu" """,

    criterios_humanizacao="""\
TOM: Curioso, desafiador, respeitoso com a inteligência da criança
RECURSOS:
- Perguntas abertas que instigam: "O que você acha que vai acontecer?"
- Conexão com experiências reais: jogos, apps, escola, amigos, família
- Humor e ironia leve (crianças de 8-10 anos apreciam)
- Protagonismo: "Agora é a sua vez", "Você é o pesquisador"
- Curiosidades e "sabia que...?" para ancorar o interesse
- Mini-desafios e gamificação sutil (pontos, estrelas, missões)
EVITAR: tom condescendente, excesso de diminutivos, textos muito longos sem imagem""",

    exemplos_linguagem="""\
✅ ADEQUADO:
  "As plantas precisam de luz solar para fazer fotossíntese — o processo pelo qual transformam
  luz em alimento. Você saberia dizer o que acontece com uma planta que fica no escuro?"
  "Em 1500, os portugueses chegaram ao Brasil. Como você acha que era a vida dos povos
  que já viviam aqui?"

❌ INADEQUADO:
  "O processo fotossintético constitui a base da cadeia trófica dos ecossistemas terrestres."
  "A chegada da esquadra cabralina ao território americano representa um divisor de águas
  na história da colonização ibérica." """,

    alertas_especificos="""\
⚠ Não assuma que a criança lembra conteúdo de anos anteriores sem retomada
⚠ Mapas e gráficos devem ter legenda e instrução de leitura na primeira vez
⚠ Atividades de múltiplas etapas devem ser numeradas
⚠ Evite ironia ou sarcasmo que possa ser interpretado literalmente
⚠ Textos expositivos: máximo 300 palavras contínuas sem quebra com atividade ou imagem""",
)
