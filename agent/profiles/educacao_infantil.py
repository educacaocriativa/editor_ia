"""
Perfis individuais da Educação Infantil conforme BNCC.
Maternal (0-1), Infantil I (1-2), Infantil II (2-3), Pré I (3-4), Pré II (4-5).
"""
from .base_perfil import PerfilEtario

PERFIL_EI_MATERNAL = PerfilEtario(
    chave="ei_maternal",
    nome="Educação Infantil — Maternal (0-1 ano)",
    faixa_anos="0-1 ano",
    bncc_prefixos=["EI01"],
    max_palavras_frase=4,
    nivel_leitura="emergente",
    perfil_cognitivo="""- Comunicação pré-verbal: choro, sorriso, balbucio
- Aprendizado por estimulação sensorial (tato, som, visão, paladar, olfato)
- Início do vínculo afetivo com cuidadores (apego seguro)
- Coordenação motora global em desenvolvimento
- Reconhece rostos familiares e vozes""",
    criterios_linguagem="""- Material direcionado exclusivamente ao educador/cuidador
- Linguagem instrucional clara e direta para o adulto
- Frases de até 4 palavras nas sugestões de fala ao bebê
- Recursos: cantigas, sons onomatopeicos, repetição rítmica
- Vocabulário afetivo e sensorial predominante""",
    criterios_pedagogicos="""- Foco em experiências sensoriais e de movimento
- Rotinas de cuidado como momentos pedagógicos
- Exploração livre de materiais seguros
- Vínculo afetivo como base do aprendizado
- Campo de experiência central: O eu, o outro e o nós""",
    criterios_humanizacao="""TOM: Acolhedor, seguro, carinhoso
- Dirigido ao educador, com sugestões de fala ao bebê
- Linguagem que valoriza o cuidado e o afeto
- Destaque para a importância de nomear emoções e objetos""",
    exemplos_linguagem="""✅ ADEQUADO (fala sugerida ao bebê):
  "Olha a bolinha! Pega, pega!"
  "Que cheiro gostoso! Hmm..."
❌ INADEQUADO:
  "Observe atentamente o objeto e descreva suas características."
  "Realize a atividade proposta com autonomia." """,
    alertas_especificos="""⚠ Todo conteúdo deve ser mediado pelo educador
⚠ Nunca sugira atividade sem supervisão adulta
⚠ Não usar vocabulário abstrato ou conceitos complexos""",
)

PERFIL_EI_INFANTIL_I = PerfilEtario(
    chave="ei_infantil_i",
    nome="Educação Infantil — Infantil I (1-2 anos)",
    faixa_anos="1-2 anos",
    bncc_prefixos=["EI01", "EI02"],
    max_palavras_frase=5,
    nivel_leitura="emergente",
    perfil_cognitivo="""- Surgimento das primeiras palavras (10-15 palavras até os 18 meses)
- Imitação de gestos e ações do adulto
- Exploração por ensaio e erro
- Início da marcha e exploração do espaço
- Reconhece objetos pelo nome
- Brinca sozinha com objetos simples""",
    criterios_linguagem="""- Frases simples de até 5 palavras
- Vocabulário concreto e do cotidiano imediato
- Repetição de palavras e sons como recurso pedagógico
- Uso de onomatopeias e sons da natureza
- Direcionado ao educador com sugestões de mediação""",
    criterios_pedagogicos="""- Exploração sensorial ampliada (água, areia, massa, tinta)
- Imitação e faz-de-conta simples
- Linguagem oral como prioridade
- Músicas, ritmos e movimentos corporais
- Campos de experiência: corpo, gestos e movimentos; traços, sons, cores e formas""",
    criterios_humanizacao="""TOM: Lúdico, musical, repetitivo e afetivo
- Cantigas e brincadeiras de colo referenciadas
- Sugestões de fala que ampliem o vocabulário
- Celebração das descobertas da criança""",
    exemplos_linguagem="""✅ ADEQUADO:
  "Cachorro faz 'au au'! Que barulho o cachorro faz?"
  "Vamos bater palmas! Um, dois, três!"
❌ INADEQUADO:
  "Identifique os animais domésticos e seus sons característicos." """,
    alertas_especificos="""⚠ Toda atividade requer presença e mediação do educador
⚠ Materiais devem ser não tóxicos e sem peças pequenas
⚠ Tempo de concentração muito curto: atividades de 2-5 minutos""",
)

PERFIL_EI_INFANTIL_II = PerfilEtario(
    chave="ei_infantil_ii",
    nome="Educação Infantil — Infantil II (2-3 anos)",
    faixa_anos="2-3 anos",
    bncc_prefixos=["EI02"],
    max_palavras_frase=6,
    nivel_leitura="emergente",
    perfil_cognitivo="""- Explosão vocabular: 200-300 palavras, frases de 2-3 palavras
- Jogo simbólico emergente (faz-de-conta, "casinha")
- Percepção de si como indivíduo (fase do "não" e autonomia)
- Interesse em livros de imagens e histórias curtas
- Coordenação motora fina em desenvolvimento (rabiscos, encaixes)
- Início da compreensão de sequências simples""",
    criterios_linguagem="""- Frases de até 6 palavras nos textos destinados à criança
- Vocabulário concreto, com muita repetição intencional
- Rimas, ritmos e aliterações como recursos
- Perguntas simples de sim/não ou escolha binária
- Direcionado ao educador com mediação sugerida""",
    criterios_pedagogicos="""- Faz-de-conta e dramatização simples
- Histórias com 3-5 cenas sequenciadas
- Música e movimento integrados ao conteúdo
- Autonomia nos cuidados pessoais como conteúdo pedagógico
- Campos: escuta, fala, pensamento e imaginação""",
    criterios_humanizacao="""TOM: Mágico, narrativo, acolhedor
- Personagens próximos ao universo da criança (animais, crianças, família)
- Repetição de refrões e falas dos personagens
- Surpresa e descoberta como motores da narrativa""",
    exemplos_linguagem="""✅ ADEQUADO:
  "O urso estava com fome. Muito fome! O que ele vai comer?"
  "Quem mora na casinha? Bate, bate na porta..."
❌ INADEQUADO:
  "Os animais selvagens habitam diferentes biomas brasileiros." """,
    alertas_especificos="""⚠ Atividades de no máximo 10-15 minutos
⚠ Regras simples, com no máximo 2 etapas
⚠ Evitar competição — foco em participação e exploração""",
)

PERFIL_EI_PRE_I = PerfilEtario(
    chave="ei_pre_i",
    nome="Educação Infantil — Pré I (3-4 anos)",
    faixa_anos="3-4 anos",
    bncc_prefixos=["EI02", "EI03"],
    max_palavras_frase=8,
    nivel_leitura="emergente",
    perfil_cognitivo="""- Linguagem oral fluente: frases completas, narrativas simples
- Pensamento mágico e animismo (objetos têm vida)
- Curiosidade intensa: fase do "por quê?"
- Jogo simbólico elaborado (papéis e cenários complexos)
- Início da percepção de letras e números como símbolos
- Atenção concentrada de 15-20 minutos em atividades lúdicas
- Sociabilidade crescente: brinca com outras crianças""",
    criterios_linguagem="""- Frases de até 8 palavras
- Vocabulário expandido: até 3 palavras novas por texto com suporte visual
- Perguntas abertas simples: "O que você acha?", "Por que será?"
- Histórias com início, meio e fim identificáveis
- Instruções com no máximo 3 etapas sequenciais""",
    criterios_pedagogicos="""- Exploração de hipóteses: "O que acontece se...?"
- Projetos temáticos curtos (1-2 semanas)
- Letra de imprensa em destaque, sem exigência de escrita
- Culinária, natureza e arte como eixos integradores
- Campos: espaços, tempos, quantidades, relações e transformações""",
    criterios_humanizacao="""TOM: Curioso, aventureiro, com abertura para o "por quê"
- Convite à investigação e descoberta
- Personagens que erram e aprendem
- Celebração da tentativa, não só do acerto""",
    exemplos_linguagem="""✅ ADEQUADO:
  "A lagarta comeu muito, muito mesmo! O que você acha que vai acontecer com ela?"
  "Vamos descobrir de onde vem a chuva? Que mistério!"
❌ INADEQUADO:
  "O ciclo da água envolve evaporação, condensação e precipitação." """,
    alertas_especificos="""⚠ Não exigir leitura ou escrita — apenas reconhecimento lúdico
⚠ Atividades com mais de 3 etapas devem ser mediadas pelo educador
⚠ Evitar comparação entre crianças""",
)

PERFIL_EI_PRE_II = PerfilEtario(
    chave="ei_pre_ii",
    nome="Educação Infantil — Pré II (4-5 anos)",
    faixa_anos="4-5 anos",
    bncc_prefixos=["EI03"],
    max_palavras_frase=10,
    nivel_leitura="emergente",
    perfil_cognitivo="""- Pré-alfabetização: reconhece letras, escreve o próprio nome
- Hipóteses sobre escrita: fase silábica emergente
- Narrativas orais elaboradas com causa e consequência
- Início do pensamento lógico: classificação e seriação simples
- Noções de número: contagem até 10 com correspondência
- Autonomia e autocontrole em desenvolvimento
- Prazer em jogos com regras simples""",
    criterios_linguagem="""- Frases de até 10 palavras
- Vocabulário que inclui antônimos, sinônimos simples e comparações
- Textos com sequência temporal clara: primeiro, depois, por fim
- Perguntas de inferência simples: "Por que o personagem fez isso?"
- Início de leitura compartilhada com acompanhamento de dedo""",
    criterios_pedagogicos="""- Letramento emergente: nome próprio, listas, receitas, bilhetes
- Contagem, classificação e padrões matemáticos lúdicos
- Projetos de investigação com registro pictórico
- Dramatização de histórias conhecidas
- Transição para o Ensino Fundamental como tema integrador""",
    criterios_humanizacao="""TOM: Desafiador, protagonista, celebrativo
- A criança como pesquisadora e descobridora
- "Você consegue!", "Que ideia incrível!"
- Conexão com a vida real: mercado, família, natureza, escola""",
    exemplos_linguagem="""✅ ADEQUADO:
  "Primeiro o João plantou a semente. Depois regou todo dia. Por fim, a flor nasceu!
  O que você acha que a flor precisou para crescer?"
❌ INADEQUADO:
  "Descreva o processo de germinação das angiospermas." """,
    alertas_especificos="""⚠ Não exigir leitura convencional — só letramento emergente
⚠ Atividades de escrita: traçado, não cópia mecânica
⚠ Preparação para o EF deve ser gradual, sem antecipação de conteúdos""",
)
