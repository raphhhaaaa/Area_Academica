from playwright.async_api import async_playwright
from app.states.config import INT_FIELDS, DEBUG
from datetime import date
import json


async def busca_aluno(page) -> dict:
    aluno = {}
    dados_aluno = page.locator(".userData td[data-label]")

    count = await dados_aluno.count()

    for i in range(count):
        td = dados_aluno.nth(i)

        label_raw = await td.get_attribute("data-label")
        valor_raw = await td.inner_text()

        label = label_raw.replace(":", "").strip()
        valor = valor_raw.strip()

        ## CONVERTE PARA INTEIRO SE ESTIVER DENTRO DE INT_FIELDS
        if label in INT_FIELDS:
                valor = int(valor)

        aluno[label] = valor

    return aluno


async def buscar_disciplinas(page, limites_faltas):
    materias = []
    tbodies = page.locator("table.masterDetail > tbody")

    count = await tbodies.count()

    for l in range(count):
        tbody = tbodies.nth(l)
        detail = tbody.locator("tr.detail")

        tds = tbody.locator("td[data-label]")

        materia = {}

        count2 = await tds.count()
        for i in range(count2):
            td = tds.nth(i)
            label_raw = await td.get_attribute("data-label")
            valor_raw = await td.inner_text()

            label = label_raw.replace(":", "").strip()
            valor = valor_raw.strip()

            ## CONVERTE PARA INTEIRO SE ESTIVER DENTRO DE INT_FIELDS
            if label in INT_FIELDS:
                valor = int(valor)

            materia[label] = valor

        materia["Notas"] = []

        # Tenta extrair o limite de faltas da carga horária, se disponível
        # O SISAV pode exibir "Carga Horária" ou similar que permite calcular o limite
        # Limite de faltas = 25% da carga horária (regra geral universitária)
        codigo_disciplina = materia.get("Código", "")
        carga = limites_faltas.get(codigo_disciplina)
        if carga:
            try:
                # Ignora casas decimais se vier como "68,0" ou "68.0"
                carga_base = str(carga).split(',')[0].split('.')[0]
                carga_str = ''.join(filter(str.isdigit, carga_base))
                carga_int = int(carga_str)
                # Cada aula = 1 hora, 25% de faltas é o limite padrão
                materia["LimiteFaltas"] = int(carga_int * 0.25)
            except (ValueError, TypeError):
                print(f"Falha ao converter carga horária '{carga}' da matéria {codigo_disciplina}")
                materia["LimiteFaltas"] = 16  # fallback padrão
        else:
            materia["LimiteFaltas"] = 16  # fallback padrão

        count_detail = await detail.count()
        if count_detail > 0:
            avaliacoes = detail.locator("table tbody tr")

            count = await avaliacoes.count()
            
            for a in range(count):
                avaliacao = avaliacoes.nth(a)

                colunas = avaliacao.locator("td")

                nome_avaliacao_raw = await colunas.nth(0).inner_text()
                nota_raw = await colunas.nth(1).inner_text()
                
                nome_avaliacao = nome_avaliacao_raw.strip()
                nota = nota_raw.strip()

                nota = float(nota.replace(",", "."))

                materia["Notas"].append({
                "Avaliação": nome_avaliacao,
                "Nota": nota
            })
                
        if "Código" in materia:  ## tratamento de nulos // json vazios - so adiciona à lista se houver conteudo --- (Se existir "Código" no objeto materia significa que é uma máteria válida e que não está vazio)
            materias.append(materia) 
    
    return materias


def salvar_json(materias, aluno):
    with open("dados.json", "w", encoding="utf-8") as arquivo:
        dados = {   ## formata json com campos separados: 'aluno' e 'disciplinas'
            "aluno": aluno,
            "disciplinas": materias
        }
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)



class CredenciaisInvalidasError(Exception):
    """Lançada quando o SISAV rejeita as credenciais fornecidas."""
    pass


class AnoLetivoInvalidoError(Exception):
    """Lançada quando o ano letivo não está disponível para o aluno no SISAV."""
    pass


async def login_sisav(page, usuario: str, senha: str):
    """
    Preenche e envia o formulário de login do SISAV.
    Lança CredenciaisInvalidasError imediatamente se o login falhar,
    sem esperar o timeout do Playwright.
    """
    await page.fill("#username", usuario)
    await page.fill("#password", senha)

    # Clica e aguarda a navegação em paralelo (max 10s)
    async with page.expect_navigation(timeout=10_000, wait_until="domcontentloaded"):
        await page.click("#cmdEnviar")

    url_atual = page.url

    # Se ainda estiver na página de login, as credenciais foram rejeitadas
    if "/auth/login" in url_atual or "/auth/signIn" in url_atual:
        # Tenta capturar a mensagem de erro exibida pelo SISAV
        mensagem_erro = ""
        for seletor in [".errors", ".alert", ".flash", ".error", "p.error", ".mensagem-erro", "#mensagem"]:
            try:
                el = page.locator(seletor).first
                if await el.count() > 0:
                    mensagem_erro = (await el.inner_text()).strip()
                    break
            except Exception:
                pass

        if not mensagem_erro:
            mensagem_erro = "Usuário ou senha incorretos. Verifique suas credenciais do SISAV."

        raise CredenciaisInvalidasError(mensagem_erro)


async def acessar_consulta(page, ano_letivo: str):
    await page.click("#Consultas")
    await page.get_by_text("Notas e faltas").click()

    # Verifica se o ano existe nas opções do select antes de selecionar
    select = page.locator("#ano")
    await select.wait_for(timeout=10_000)

    opcoes_disponiveis = await select.locator("option").all_inner_texts()
    opcoes_valores = await select.evaluate("el => [...el.options].map(o => o.value)")

    if ano_letivo not in opcoes_valores:
        anos_str = ", ".join(v for v in opcoes_valores if v)  # exclui option vazia
        raise AnoLetivoInvalidoError(
            f"O ano {ano_letivo} não está disponível para sua matrícula. "
            f"Anos disponíveis: {anos_str}."
        )

    await select.select_option(ano_letivo)
    await page.wait_for_selector("#tabelaDeNotas table", timeout=15_000)


async def extrair_limite_faltas(page) -> dict:
    limites = {}
    try:
        await page.click("#Notas_-_Faltas")
        await page.get_by_text("Frequência da Turma").click()

        select = page.locator("#turma")
        await select.wait_for(timeout=10_000)

        opcoes_disponiveis = await select.locator("option").all_inner_texts()
        for opcao in opcoes_disponiveis:
            if '-' in opcao and ':' in opcao:
                cd_dis = opcao[:opcao.find('-')].strip()
                carga_horaria = opcao[opcao.find(':')+1:].strip()
                limites[cd_dis] = carga_horaria
        print(f"Limites de faltas extraídos (Brutos): {limites}")
    except Exception as e:
        print(f"Erro ao extrair limites (Frequência da Turma): {e}")
    
    return limites

async def extrair_horarios_aula(page, codigos_alvo: list) -> dict:
    horarios = {}
    try:
        await page.click("#Consultas")
        await page.get_by_text("Horário de Aulas").click()

        # Aguarda a estrutura principal de horários ser renderizada
        await page.wait_for_selector(".horarios-aula", timeout=15000)

        # Localiza TODAS as tabelas de horários, ignorando se é Tarde, Noite ou qual semestre
        tabelas = page.locator("table.horario-aula")
        
        count_tabelas = await tabelas.count()
        
        for t in range(count_tabelas):
            tabela = tabelas.nth(t)
            
            # Pegando todas as linhas do corpo da tabela
            linhas = tabela.locator("tbody tr")
            count_linhas = await linhas.count()
            
            for l in range(count_linhas):
                linha = linhas.nth(l)
                colunas = linha.locator("td")
                
                # Encontra o semestre (1 ou 2) olhando para o <h2> anterior ao fieldset
                semestre_raw = await tabela.evaluate("""
                    el => {
                        let fieldset = el.closest('fieldset');
                        if (!fieldset) return '1';
                        let prev = fieldset.previousElementSibling;
                        while(prev) {
                            if(prev.tagName === 'H2') return prev.innerText;
                            prev = prev.previousElementSibling;
                        }
                        return '1';
                    }
                """)
                semestre_num = 1 if "1" in semestre_raw else 2
                
                # Certifica de que a linha tem as 8 colunas (hr + 6 dias + hr extra possivel)
                if await colunas.count() >= 8:
                    horario_raw = await colunas.nth(1).inner_text()
                    horario = horario_raw.replace('\n', ' - ').strip()
                    
                    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
                    
                    for i_dia, dia in enumerate(dias):
                        celula_texto = await colunas.nth(i_dia + 2).inner_text()
                        celula_texto = celula_texto.strip()
                        
                        if celula_texto:
                            partes = celula_texto.split('\n')
                            if len(partes) >= 2:
                                codigo_turma = partes[0].strip()
                                bloco_sala = partes[1].strip()
                                
                                # Pega só os números antes do hífen (ex: "9897")
                                codigo_materia = codigo_turma.split('-')[0].strip()
                                
                                # Se o código encontrado for uma das matérias que o aluno tem na grade atual
                                if codigo_materia in codigos_alvo:
                                    if codigo_materia not in horarios:
                                        horarios[codigo_materia] = []
                                        
                                    horarios[codigo_materia].append({
                                        "dia": dia,
                                        "horario": horario,
                                        "sala": bloco_sala,
                                        "semestre": semestre_num
                                    })

    except Exception as e:
        print(f"Erro ao extrair horários: {e}")
        
    return horarios

async def rodar_extrator(usuario: str = None, senha: str = None, ano_letivo: str = None):
    """
    Executa o scraping no SISAV.
    Se usuario/senha forem fornecidos, usa eles.
    Caso contrário, lê do config (variáveis de ambiente).
    """
    import app.states.config as cfg

    _usuario = usuario or cfg.USUARIO
    _senha = senha or cfg.SENHA

    # Fallback para ano atual se não informado ou vazio
    ano_str = str(ano_letivo).strip() if ano_letivo else ""
    _ano_letivo = ano_str if ano_str else str(date.today().year)

    if not _usuario or not _senha:
        raise ValueError("Credenciais não fornecidas. Faça login primeiro.")

    async with async_playwright() as p:
        # Abre o navegador
        browser = await p.chromium.launch(headless=not DEBUG) ##headless = false mostra o navegador abrindo
        page = await browser.new_page() ## abre nova pagina 'vazia' / nova

        await page.goto("https://npd.uem.br/sav/auth/login")  ## comando para ir para um site / url especifica

        try:
            # 1. autenticação e navegação
            await login_sisav(page, _usuario, _senha)
            
            # Extrai os limites de todas as disciplinas de uma vez antes de ir para as notas
            limites_faltas = await extrair_limite_faltas(page)
            
            await acessar_consulta(page, _ano_letivo)

            # 2. extração de dados
            aluno = await busca_aluno(page)
            disciplinas = await buscar_disciplinas(page, limites_faltas)

            # Extração de horários de aula para as disciplinas encontradas
            codigos_alvo = [d.get("Código", "") for d in disciplinas if d.get("Código")]
            horarios = await extrair_horarios_aula(page, codigos_alvo)
            
            for d in disciplinas:
                codigo = d.get("Código", "")
                d["Horarios"] = horarios.get(codigo, [])

            # 3. persistência e retorno
            salvar_json(disciplinas, aluno)
            print(f"Dados de {aluno.get('Nome', 'Aluno')} salvos com sucesso.")
            
            dados_finais = {
                "aluno": aluno,
                "disciplinas": disciplinas
            }
            return dados_finais
        
        except Exception as e:
            print(f"Erro crítico ao rodar o extrator: {e}")  
            raise e

        finally:
            await browser.close()



if __name__ == "__main__":
    import asyncio
    asyncio.run(rodar_extrator())