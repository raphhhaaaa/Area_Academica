from playwright.sync_api import sync_playwright
from config import INT_FIELDS, USUARIO, SENHA, DEBUG
import json

def busca_aluno(page):
    aluno = {}

    dados_aluno = page.locator(".userData td[data-label]")

    for i in range(dados_aluno.count()):
        td = dados_aluno.nth(i)

        label = td.get_attribute("data-label").replace(":", "").strip()
        valor = td.inner_text().strip()

        ## CONVERTE PARA INTEIRO SE ESTIVER DENTRO DE INT_FIELDS
        if label in INT_FIELDS:
                valor = int(valor)

        aluno[label] = valor

    return aluno

def buscar_materias(page):
    tbodies = page.locator("table.masterDetail > tbody")

    materias = []

    for l in range(tbodies.count()):
        tbody = tbodies.nth(l)
        detail = tbody.locator("tr.detail")

        tds = tbody.locator("td[data-label]")

        materia = {}
        for i in range(tds.count()):
            td = tds.nth(i)
            label = td.get_attribute("data-label").replace(":", "").strip()
            valor = td.inner_text().strip()

            ## CONVERTE PARA INTEIRO SE ESTIVER DENTRO DE INT_FIELDS
            if label in INT_FIELDS:
                valor = int(valor)

            materia[label] = valor

        materia["Notas"] = []

        if detail.count() > 0:
            avaliacoes = detail.locator("table tbody tr")

            for a in range(avaliacoes.count()):
                avaliacao = avaliacoes.nth(a)

                colunas = avaliacao.locator("td")

                nome_avaliacao = colunas.nth(0).inner_text().strip()
                nota = colunas.nth(1).inner_text().strip()

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

def login(page):
    page.fill("#username", USUARIO)
    page.fill("#password", SENHA)
    page.click("#cmdEnviar")

def acessar_consulta(page):
    page.click("#Consultas")
    page.get_by_text("Notas e faltas").click()
    page.select_option("#ano", "2026")
    page.wait_for_selector("#tabelaDeNotas table")

def main():
    with sync_playwright() as p:
        # Abre o navegador
        browser = p.chromium.launch(headless=not DEBUG) ##headless = false mostra o navegador abrindo
        page = browser.new_page() ## abre nova pagina 'vazia' / nova

        page.goto("https://npd.uem.br/sav/auth/login")  ## comando para ir para um site / url especifica

        try:
            login(page)
            acessar_consulta(page)
        except ConnectionError as e:
            print("Erro ao fazer login ou acessar a página de consultas: ", e)

        aluno = busca_aluno(page)
        materias = buscar_materias(page)

        salvar_json(materias, aluno)

if __name__ == "__main__":
    main()