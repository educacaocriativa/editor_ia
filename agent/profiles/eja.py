from .base_perfil import PerfilEtario

PERFIL_EJA = PerfilEtario(
    chave="eja",
    nome="EJA / Adultos",
    faixa_anos="18+ anos",
    bncc_prefixos=["EF", "EM"],  # EJA usa base do EF e EM com adaptações
    max_palavras_frase=22,
    nivel_leitura="variável",

    perfil_cognitivo="""\
- Público heterogêneo: jovens de 18-25 anos excluídos da escola regular; adultos e idosos
- Experiência de vida rica como ponto de partida e legitimação do saber
- Histórico de fracasso escolar ou exclusão: sensibilidade à autoestima e ao pertencimento
- Motivação instrumental forte: trabalho, documentação, promoção, comunicação
- Pensamento prático-concreto predominante, mas com capacidade de abstração quando ancorada
- Aprendizagem significativa: o conteúdo precisa se conectar ao contexto real do estudante
- Disponibilidade de tempo limitada (trabalho, família): objetividade é fundamental
- Letramento digital variável: alguns têm, outros não""",

    criterios_linguagem="""\
VOCABULÁRIO:
- Partir sempre da linguagem que o adulto já usa em seu cotidiano
- Termos técnicos introduzidos com analogia a experiências concretas do mundo do trabalho
- Evitar infantilização do vocabulário: o adulto sabe palavras complexas do cotidiano
- Definição de termos acadêmicos na primeira ocorrência; nunca assumir conhecimento prévio

SINTAXE:
- Frases diretas e objetivas: até 22 palavras
- Estrutura SVO predominante; orações subordinadas com moderação
- Evitar inversões estilísticas que dificultem a compreensão
- Conectivos claros: explicitação das relações lógicas entre ideias

REGISTRO:
- Informal-respeitoso: trate o adulto como par inteligente e experiente
- Nunca use "você sabe como é na escola" — muitos têm relação difícil com a escola
- Referências a contextos adultos: trabalho, saúde, direitos, família, cidadania
- Proibido: qualquer tom que lembre "coisa de criança"  """,

    criterios_pedagogicos="""\
ABORDAGEM (Paulo Freire como referência):
- Partir da realidade concreta do educando (palavra geradora, tema gerador)
- Valorização do saber popular e das experiências de vida como conhecimento legítimo
- Contextualização: todo conteúdo deve ter aplicação prática demonstrada
- Autonomia: o estudante adulto decide e direciona sua aprendizagem

CONEXÕES COM A VIDA DO ADULTO:
- Língua Portuguesa: leitura de contratos, bulas, notícias, formulários
- Matemática: finanças pessoais, medidas, cálculo de troco, porcentagem
- Ciências: saúde, alimentação, meio ambiente próximo
- História/Geografia: história local, direitos civis, mobilidade urbana

PRINCÍPIOS ESPECÍFICOS DA EJA:
1. Respeito à identidade cultural e étnica
2. Não infantilizar: o adulto tem dignidade e experiência
3. Aplicabilidade imediata: "Para que serve isso na minha vida?"
4. Flexibilidade metodológica: nem todos aprendem do mesmo jeito
5. Reconhecimento do saber não-formal como legítimo""",

    criterios_humanizacao="""\
TOM: Horizontal, respeitoso, cúmplice — como parceiro de aprendizagem, não professor autoritário
RECURSOS:
- Diálogo genuíno: "O que você pensa sobre isso?"
- Situações do cotidiano adulto: conta de luz, receita, notícia do bairro, entrevista de emprego
- Valorização explícita da experiência: "Quem já trabalhou em construção sabe que..."
- Humor adulto: leveza sem infantilidade
- Histórias de superação e conquista (sem ser condescendente)
- Referências a contextos brasileiros reais, não abstratos
EVITAR: infantilização, tom de "professor sabe mais", textos escolares típicos da infância""",

    exemplos_linguagem="""\
✅ ADEQUADO:
  "Quem já foi ao banco assinar um contrato sabe que tem muito texto difícil. Aprender
  a ler esse tipo de documento é um direito seu. Vamos entender juntos como ele funciona."
  "3% de R$ 1.000 é R$ 30. Esse é o tipo de cálculo que aparece em parcelas e juros.
  Você já pagou juros sem perceber quanto estava pagando?"

❌ INADEQUADO:
  "Complete as lacunas com as letras corretas, como fez o Pedrinho no exemplo acima."
  "Vamos aprender sobre a natureza! As florestas são muito importantes para os animais
  e para nós." """,

    alertas_especificos="""\
⚠ Nunca use imagens ou exemplos que infantilizem o público (animais fofos, crianças, brinquedos)
⚠ Evite referências a "quando você era aluno" — muitos têm trajetória escolar traumática
⚠ Textos longos precisam de pausas para reflexão e aplicação prática
⚠ Instrução de atividade: sempre explicar o propósito prático do exercício
⚠ Diversidade do público: contemplar diferentes trajetórias (campo, cidade, migrantes, idosos)
⚠ Inclusão: materiais para EJA frequentemente têm público com deficiência visual ou motora""",
)
