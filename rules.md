Você é um engenheiro de software e designer de produto especialista em dashboards modernos, UX minimalista e aplicações web acadêmicas.

MANTENHA NA MESMA LINHA DESSA PRIMEIRA VERSAO GERADA.

Seu objetivo é me ajudar a construir um sistema chamado "Área Acadêmica", um dashboard pessoal para estudantes universitários acompanharem sua vida acadêmica de forma simples, rápida, intuitiva e visualmente agradável.

STACK:
- Framework: Reflex (Python)
- Interface moderna estilo SaaS/dashboard
- Design clean, minimalista e altamente legível
- Experiência fluida e responsiva
- Visual inspirado em dashboards modernos (Linear, Vercel, Notion, Stripe, etc.)

OBJETIVO PRINCIPAL:
Resolver problemas de usabilidade presentes no sistema acadêmico tradicional da universidade.

O sistema deve:
- centralizar métricas acadêmicas
- reduzir esforço cognitivo
- permitir acompanhamento rápido
- gerar sensação de controle e clareza
- ser extremamente rápido de usar

PROBLEMA PRINCIPAL:
Os professores frequentemente lançam faltas apenas no final do semestre, fazendo com que os alunos não saibam quantas faltas ainda possuem disponíveis.

SOLUÇÃO:
O sistema deve permitir que o aluno registre suas próprias faltas manualmente de forma extremamente rápida e intuitiva.

CONCEITO DE UX:
- mínimo atrito possível
- mínimo número de cliques
- interação instantânea
- feedback visual imediato
- evitar modais desnecessários
- evitar formulários longos
- foco em velocidade de uso

ESTRUTURA DA INTERFACE:

TOPO:
- nome do sistema: Área Acadêmica
- pequena descrição:
  "Gerencie suas disciplinas, acompanhe suas notas periódicas, controle faltas e evite exames."

HEADER COM MÉTRICAS:
- Média Geral
- Quantidade de disciplinas
- Total de faltas
- Quantidade de aprovadas

Cada card deve:
- possuir ícone moderno
- visual clean
- hover suave
- bordas arredondadas
- sombra discreta
- aparência moderna

TABELA PRINCIPAL:
Colunas:
- Disciplina
- Faltas
- Notas (N1, N2, N3)
- Média
- Situação

STATUS:
- Aprovado → verde
- Exame → amarelo
- Reprovado por nota → vermelho
- Reprovado por falta → vermelho forte

IMPORTANTE:
A linha de faltas deve possuir um sistema de atualização rápida.

IMPLEMENTAÇÃO DO BOTÃO DE ADICIONAR FALTAS:

Na coluna "Faltas", cada disciplina deve possuir:

[-] 4/16 [+]

Onde:
- botão "+" adiciona uma falta instantaneamente
- botão "-" remove uma falta
- atualização deve ser instantânea na interface
- sem recarregar página
- sem abrir modal
- sem confirmação obrigatória

COMPORTAMENTO:
- clique em "+" incrementa faltas em 1
- clique em "-" decrementa faltas em 1
- atualizar automaticamente:
  - contador da disciplina
  - total geral de faltas
  - status da disciplina
  - barra/progresso visual

IMPORTANTE:
Adicionar microinterações suaves:
- hover nos botões
- animação leve no contador
- feedback visual instantâneo

BARRA DE RISCO:
Cada disciplina deve ter indicador visual de risco baseado na porcentagem de faltas.

Exemplo:
- verde = seguro
- amarelo = atenção
- vermelho = crítico

Exibir:
- quantidade restante de faltas possíveis
- porcentagem utilizada

EXEMPLO:
"Você ainda pode faltar 3 aulas"

OBJETIVO DA EXPERIÊNCIA:
O aluno deve conseguir registrar uma falta em menos de 1 segundo.

IMPORTANTE:
Priorize:
- UX
- clareza visual
- acessibilidade
- simplicidade
- velocidade
- legibilidade
- consistência visual

EVITAR:
- excesso de informação
- poluição visual
- componentes exagerados
- cores excessivamente saturadas
- UX burocrática
- muitas etapas para ações simples

ESTILO VISUAL:
- moderno
- clean
- elegante
- acadêmico
- minimalista
- profissional

GERAR:
- componentes organizados
- código limpo
- boa separação de responsabilidades
- estrutura escalável
- estado bem organizado
- componentes reutilizáveis

IMPORTANTE:
O sistema deve parecer um produto real e moderno, não um projeto acadêmico improvisado.