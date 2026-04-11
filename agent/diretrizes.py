"""
Diretrizes editoriais permanentes da Rede Luz do Mundo (LDM).
Extraídas de regrasdeouro.xlsx e injetadas nos prompts de cada skill.

Fonte autoritativa: CLAUDE.md (seções 1–8).
"""

# ── Proibições absolutas e regras de estilo (seções 1 e 2) ──────────────────

DIRETRIZES_GERAIS = """
DIRETRIZES EDITORIAIS OBRIGATÓRIAS — REDE LUZ DO MUNDO (LDM)
Aplique ANTES de qualquer outra correção. Estas regras têm prioridade máxima.

PROIBIÇÕES ABSOLUTAS:
- Diminutivos infantilizantes (feirinha, casinha, livrinho, amiguinho)
  → Substituir pelo substantivo normal (feira, casa, livro, colega)
- 1ª pessoa do plural (nós, nosso, vamos, faremos)
  → Usar 3ª pessoa ou impessoal (o estudante fará, analise)
- Tratamento informal (a gente, você, galera, pessoal)
  → Usar: o estudante, o leitor, a turma, o grupo
- Advérbios de lugar relativo (acima, abaixo, ao lado, lá)
  → Usar: a seguir, anterior, no boxe lateral, na página X
- Vícios de linguagem (tipo assim, né, legal demais, super)
  → Remover ou substituir por adjetivo preciso
- Pleonasmos (subir para cima, encarar de frente, elo de ligação)
  → Subir, encarar, elo
- Palavras vagas em contextos científicos (muito, pouco, bastante)
  → Dados quantitativos ou termos precisos
- Linguagem neutra ideológica (todes, amigues, @, x)
  → Coletivo masculino padrão ou reformulação neutra
- Referências temporais relativas (ano passado, esse mês, hoje em dia)
  → Citar o ano ou o século (em 2024, no século XXI)
- Enunciados negativos (não faça, não responda)
  → Enunciados afirmativos (evite, mude, transforme)

REGRAS ESPECÍFICAS DO EDITOR:
- ED_01: Títulos — maiúscula APENAS em início de frase ou nomes próprios
  ❌ "Investigando O Mundo" → ✅ "Investigando o mundo"
- ED_02: Verbo orientar exige "para que" + subjuntivo
  ❌ "Oriente os estudantes a retornarem" → ✅ "Oriente os estudantes para que retornem"
- ED_03: Ordem direta (Sujeito + Predicado). Sem inversões desnecessárias.
- ED_04: Proibido 1ª pessoa do plural em qualquer contexto.
- ED_05: Substituir advérbios de lugar
  ❌ "Veja na imagem abaixo/acima" → ✅ "Veja na imagem a seguir"
- ED_07: NUNCA remover ou neutralizar a palavra "Deus" em contexto confessional.
- ED_08: Referências bibliográficas — proibido "de" antes do ano
  ❌ "Nome do Site, de 2025" → ✅ "Nome do Site, 2025"
- ED_09: NUNCA remover ou substituir a palavra "cristão" no material.

IDENTIDADE CONFESSIONAL:
- Preservar SEMPRE os termos teológicos: Deus, Criador, Cristão, cristão.
- Não aplicar linguagem neutra de cunho ideológico.
"""

# ── Humanidades Cristãs — cosmovisão (seção 6) ──────────────────────────────

DIRETRIZES_HUMANIDADES_CRISTAS = """
HUMANIDADES CRISTÃS — COSMOVISÃO E CONTEÚDO BNCC:
Conteúdos obrigatórios da BNCC que contradizem a cosmovisão cristã devem ser
incluídos, mas SEMPRE apresentados como visões ou modelos interpretativos,
nunca como verdades absolutas.

REGRAS:
- NUNCA apresentar teorias científicas naturalistas como verdades absolutas.
  Usar sempre: "Segundo a teoria evolutiva...", "Sob a ótica científica...",
  "Cientistas propõem que...", "Este modelo busca explicar..."
- SEMPRE incluir o contraponto da cosmovisão cristã quando o conteúdo negar
  ou ignorar a existência de Deus.
  Usar: "A cosmovisão cristã compreende que...", "Cremos que...",
  "A fé cristã afirma que..."
- NUNCA remover conteúdo obrigatório da BNCC — apenas contextualizar.
- Origem da humanidade: apresentar evolução como "modelo científico de
  interpretação biológica", com contraponto da Criação divina.
- Big Bang: expor como "tentativa de explicar a mecânica da criação",
  mantendo Deus como Causa Primária.
- Relativismo moral: expor diferentes culturas, fundamentando a ética
  nos valores absolutos da Bíblia.
- Religião como construção social (Marx/Durkheim): apresentar como análise
  sociológica, reafirmando a fé como verdade espiritual.
"""

# ── Acessibilidade e neurodivergência — TEA/TDAH (seção 7) ──────────────────

DIRETRIZES_ACESSIBILIDADE = """
ACESSIBILIDADE — NEURODIVERGÊNCIA (TEA/TDAH):
Aplicar em TODO o material, independentemente do público declarado.

REGRAS:
- NUNCA usar metáforas ou expressões idiomáticas
  ❌ "Bate mais forte", "Choveu canivete", "Caiu a ficha"
  ✅ "Aplique mais força", "Choveu muito", "Entendeu o conceito"
- NUNCA usar comandos vagos ou subjetivos
  ❌ "Use sua imaginação", "Faça como quiser"
  ✅ "Desenhe um animal que você conhece", "Siga o passo a passo"
- NUNCA usar rótulos negativos para crianças
  ❌ "Criança endiabrada", "Menino difícil"
  ✅ "Criança com muita energia", "Estudante em desenvolvimento"
- NUNCA inserir elementos de outras religiões (santos católicos, sincretismo)
  ✅ Apenas personagens bíblicos evangélicos ou elementos neutros da natureza
- SEMPRE usar a versão NVI (Nova Versão Internacional) em citações bíblicas.
- SEMPRE preferir listas numeradas a blocos de texto denso em enunciados.
- Ironia e sarcasmo em diálogos são proibidos — usar diálogos honestos e claros.
"""

# ── Bloco combinado para skills que precisam de todas as regras ──────────────

DIRETRIZES_COMPLETAS = (
    DIRETRIZES_GERAIS
    + "\n"
    + DIRETRIZES_HUMANIDADES_CRISTAS
    + "\n"
    + DIRETRIZES_ACESSIBILIDADE
)
