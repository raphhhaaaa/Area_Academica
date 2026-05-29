from playwright.async_api import async_playwright
from app.states.config import INT_FIELDS, USUARIO, SENHA, DEBUG
from app.states.utils.verificacoes import verifica_faltas
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

async def buscar_disciplinas(page):
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

async def login(page):
    await page.fill("#username", USUARIO)
    await page.fill("#password", SENHA)
    await page.click("#cmdEnviar")

async def acessar_consulta(page):
    await page.click("#Consultas")
    await page.get_by_text("Notas e faltas").click()
    await page.select_option("#ano", "2026")
    await page.wait_for_selector("#tabelaDeNotas table")

async def rodar_extrator():
    async with async_playwright() as p:
        # Abre o navegador
        browser = await p.chromium.launch(headless=not DEBUG) ##headless = false mostra o navegador abrindo
        page = await browser.new_page() ## abre nova pagina 'vazia' / nova

        await page.goto("https://npd.uem.br/sav/auth/login")  ## comando para ir para um site / url especifica

        try:
            # 1. autenticação e navegação
            await login(page)
            await acessar_consulta(page)

            # 2. extração de dados
            aluno = await busca_aluno(page)
            disciplinas = await buscar_disciplinas(page)

            # 3. persistência e retorno
            salvar_json(disciplinas, aluno)
            print(f"Dados de {aluno['Nome']} salvos com sucesso.")
            
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