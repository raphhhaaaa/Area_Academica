# 🎓 Área Acadêmica (UEM)

## O que é?
A "Área Acadêmica" trata-se de uma aplicação web, projetada com uma arquitetura monolítica, desenvolvida puramente com Python. Utilizando as frameworkds Reflex (para o frontend + integração) e Playwritgh (para web-scrapping e automação).

O objetivo central dessa aplicaçaõ é centralizar as informações mais relevantes para o dia a dia do aluno universitário, facilitando o acesso e a visualização intuitiva dessas informações, buscando sanar qualquer tipo de gargalo ou insegurança que o acesso ao sistema legado 
da universidade possa trazer.

Além de oferecer praticidade e comodidade, a Área Acadêmica visa pela segurança e privacidade dos seus usuários. Por se tratar de um sistema "visualizador" de dados, as credenciais de autenticação institucionais do aluno nunca são persistidas em qualquer banco de dados relacionadas ao 
contexto da aplicação.

>Nota: Inicialmente, a Area Academica foi pensada exclusivamente para o domínio da Universidade Estadual de Maringá (UEM).

---

## 1. Visão Geral e Contexto

O sistema funciona como uma camada de interface moderna sobre o portal acadêmico legado da Universidade Estadual de Maringá (SISAV). Ele automatiza o login, navega pelas consultas e extrai notas, faltas e informações de registro de forma transparente para o estudante.

### Princípios de Design:
* **Monolito Funcional (Reflex):** O *frontend* (React) e o *backend* (FastAPI) coexistem em um único projeto Python, comunicando-se nativamente via WebSockets gerenciados pelo estado da aplicação.
* **Automação Assíncrona:** A extração web é realizada via `async_playwright`, isolando a navegação pesada do laço de eventos principal do servidor de interface.
* **Credenciais Voláteis:** O usuário e a senha institucionais trafegam exclusivamente em memória durante o evento de autenticação, sendo descartados logo após a coleta.

---

## 2. Estrutura de Diretórios do Projeto

O código está modularizado e organizado seguindo a separação de responsabilidades recomendada pelo ecossistema Reflex:

* **`rxconfig.py`**: Configurações de ambiente e inicialização do framework.
* **`app.py`**: Ponto de entrada do aplicativo e definição da tabela de rotas (`/` para login, `/dashboard` para painel principal).
* **`app/components/`**: Módulos visuais focados puramente em interface e renderização (ex: formulários de entrada, listagem de matérias, cartões de métricas).
* **`app/states/`**: Camada lógica central que gerencia eventos da interface, variáveis reativas e conexões com o motor do navegador.
* **`app/states/extrator.py`**: Motor de automação assíncrona responsável por gerenciar sessões do Chromium e interações com o portal da universidade.
* **`app/states/config/`**: Variáveis e parâmetros de ambiente globais.
* **`app/states/utils/`**: Funções utilitárias puras focadas em cálculos e verificações secundárias.

---

## 3. O Fluxo de Execução e Ciclo de Dados

O ciclo completo de sincronização de informações obedece a um fluxo unidirecional rígido para assegurar previsibilidade e performance:

1. **Captura na UI:** O estudante preenche o formulário de login na interface. O Reflex vincula esses inputs diretamente a estados em memória por meio de manipuladores de alteração.
2. **Ativação Visual e Automação em Background:** O clique no botão de envio dispara um evento no estado principal que modifica uma flag reativa, acionando instantaneamente o motor assíncrono do navegador, abrindo uma página oculta, realizando login no sistema da universidade e, por fim, extraindo os dados relevantes.
3. **Varredura e Conversão:** Os seletores do navegador localizam as linhas de cabeçalho e detalhe da tabela. O script extrai as strings brutas e as encaminha para conversores que limpam strings, tratam decimais e estruturam dicionários tipados.
4. **Atualização e Redirecionamento:** Os dicionários estruturados atualizam os estados de dados do aluno e das disciplinas. A senha é apagada do estado e o servidor emite um comando de redirecionamento, forçando o navegador a carregar o painel com as novas variáveis ativas.

---

## 4. ...
