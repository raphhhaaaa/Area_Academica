import asyncio
import json
from playwright.async_api import async_playwright

# Importamos as funções que já funcionam para poupar tempo
from app.states.extrator import login_sisav, acessar_consulta


CODIGOS = ["5170", "9884", "9895", "9896", "9897", "9899", "9911", "9901", "9907", "11917", "11919"]

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
        print(f"Encontradas {count_tabelas} tabelas de horários na página.")
        
        for t in range(count_tabelas):
            tabela = tabelas.nth(t)
            
            # Pegando todas as linhas do corpo da tabela
            linhas = tabela.locator("tbody tr")
            count_linhas = await linhas.count()
            
            for l in range(count_linhas):
                linha = linhas.nth(l)
                colunas = linha.locator("td")
                
                # Certifica de que a linha tem as 8 colunas (hr + 6 dias + hr extra possivel)
                if await colunas.count() >= 8:
                    horario_raw = await colunas.nth(1).inner_text()
                    horario = horario_raw.replace('\n', ' - ').strip()
                    
                    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
                    
                    for i_dia, dia in enumerate(dias):
                        celula_texto = await colunas.nth(i_dia + 2).inner_text()
                        celula_texto = celula_texto.strip()
                        
                        if celula_texto:
                            # celula_texto: "9897 - 31\nD67 - 103"
                            partes = celula_texto.split('\n')
                            if len(partes) >= 2:
                                codigo_turma = partes[0].strip()
                                bloco_sala = partes[1].strip()
                                
                                # Pega só os números antes do hífen (ex: "9897")
                                codigo_materia = codigo_turma.split('-')[0].strip()
                                
                                # Se o código encontrado for uma das matérias que o aluno tem na grade atual
                                if codigo_materia in codigos_alvo:
                                    print(f"📚 Horário Encontrado -> {codigo_materia} | {dia} | {horario} | {bloco_sala}")
                                    
                                    if codigo_materia not in horarios:
                                        horarios[codigo_materia] = []
                                        
                                    horarios[codigo_materia].append({
                                        "dia": dia,
                                        "horario": horario,
                                        "sala": bloco_sala
                                    })

    except Exception as e:
        print(f"❌ Erro ao extrair horários: {e}")
        
    return horarios

async def teste_isolado():
    # Coloque suas credenciais reais aqui APENAS para testar localmente
    usuario = "ra147190"
    senha = "52461598"
    # ano_letivo = "2024" # Mude para o ano que deseja inspecionar

    print("🚀 Iniciando o teste isolado...")
    async with async_playwright() as p:
        # headless=False é essencial para você ver o navegador e poder debugar
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()

        try:
            print("🌐 Acessando página de login...")
            await page.goto("https://npd.uem.br/sav/auth/login")

            print("🔑 Realizando login...")
            await login_sisav(page, usuario, senha)

            print("⚙️ Executando o método 'extrair_horarios_aula'...")
            # Passamos a lista de códigos alvo
            horarios_extraidos = await extrair_horarios_aula(page, CODIGOS)
            
            # print("\n✅ Resultado retornado pelo seu método:")
            # print(json.dumps(resultado, indent=4, ensure_ascii=False))

            # Essa pausa é útil para você abrir o DevTools (F12) no navegador
            # que abriu, inspecionar o HTML e ajustar seus seletores no Playwright.
            input("\n⏸️ Pressione Enter no terminal para fechar o navegador e encerrar...")

        except Exception as e:
            print(f"\n❌ Erro durante o teste: {e}")
        finally:
            print("🛑 Fechando o navegador...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(teste_isolado())
