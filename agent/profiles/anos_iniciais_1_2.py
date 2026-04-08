from .base_perfil import PerfilEtario

PERFIL_EF_1_2 = PerfilEtario(
    chave="ef_1_2",
    nome="1º ao 2º ano do Ensino Fundamental (6-7 anos)",
    faixa_anos="6-7 anos",
    bncc_prefixos=["EF01", "EF02", "EF12"],
    max_palavras_frase=12,
    nivel_leitura="emergente",

    perfil_cognitivo="""\
- Fase de alfabetização: relação fonema-grafema em consolidação (especialmente no 1º ano)
- No 2º ano, leitura decodificada presente mas fluência ainda limitada
- Pensamento concreto e operatório: classifica, serializa, conserva quantidade
- Noção de tempo: passado próximo e futuro imediato; história linear simples
- Atenção concentrada por 10-15 minutos em atividade dirigida
- Motivação alta por reconhecimento, histórias, personagens e situações familiares
- Operações matemáticas: adição e subtração concretas; contagem até 100
- Escrita: palavras e frases curtas; ainda comete trocas fonêmicas""",

    criterios_linguagem="""\
VOCABULÁRIO:
- Palavras conhecidas do cotidiano e do universo escolar
- Máximo 2 palavras novas por parágrafo, com explicação imediata por contexto
- Preferir palavras curtas (2-3 sílabas); palavras longas só se de uso frequente
- Proibido: sinônimos raros, termos técnicos sem ancora concreta

SINTAXE:
- Frases curtas: SVO simples, máximo 12 palavras
- Orações coordenadas com "e", "mas", "porque", "então" são OK
- Uma oração subordinada por frase, máximo
- Proibido: inversões sintáticas, aposto explicativo longo, voz passiva analítica

REGISTRO:
- Semiformal didático: nem gíria nem acadêmico
- Segunda pessoa ("você", "sua turma")
- Presente do indicativo predominante
- Passado simples para narrativas; futuro simples para instruções""",

    criterios_pedagogicos="""\
ABORDAGEM:
- Concreto → representação → símbolo (sempre nesta ordem)
- Textos curtos com ilustração associada
- Instruções explícitas e numeradas (passo a passo)
- Exemplos antes das generalizações

SEQUÊNCIA DIDÁTICA TÍPICA:
1. Contextualização (situação familiar à criança)
2. Apresentação do novo conteúdo com exemplo concreto
3. Prática guiada (com o professor)
4. Prática autônoma simples

CONSCIÊNCIA FONOLÓGICA (para LP):
- Atividades de rima, segmentação silábica e aliteração são esperadas
- Instrução fônica explícita no 1º ano
- Fluência leitora no 2º ano

MATEMÁTICA CONCRETA:
- Sempre associar número a quantidade concreta
- Material manipulável referenciado no texto""",

    criterios_humanizacao="""\
TOM: Encorajador, caloroso, com humor leve e acessível
RECURSOS:
- Personagens infantis (animais, crianças, objetos animados)
- Histórias curtas como contexto de aprendizagem
- Desafios e mistérios acessíveis: "Você consegue descobrir...?"
- Celebração do esforço: "Já que você chegou até aqui..."
- "A gente", "vamos", "juntos" para criar senso de comunidade
EVITAR: instrução fria, tom avaliativo, textos sem personagem ou narrativa""",

    exemplos_linguagem="""\
✅ ADEQUADO:
  "Mia a gatinha tem três patas. Quantas patas tem dois gatos? Vamos contar juntos!"
  "A letra M faz o som de 'mmm'. Pense em palavras que começam com M: mão, mel, mala."

❌ INADEQUADO:
  "A unidade lexical em questão apresenta correspondência com o fonema bilabial nasal."
  "Determine o numeral que representa a cardinalidade do conjunto dado." """,

    alertas_especificos="""\
⚠ Instrução com mais de 3 etapas deve ser quebrada em tópicos numerados
⚠ Todo exercício deve ter exemplo resolvido antes da solicitação autônoma
⚠ Não use condicional ou subjuntivo sem suporte de exemplo concreto
⚠ Evite textos contínuos com mais de 4 frases sem quebra visual (título, imagem, parágrafo)
⚠ No 1º ano: não exigir leitura fluente; no 2º ano: textos até 80 palavras são adequados""",
)
