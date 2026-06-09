import asyncio
import json
from playwright.async_api import async_playwright

# Importamos as funções que já funcionam para poupar tempo
from app.states.extrator import login_sisav, acessar_consulta


CODIGOS = ["5170", "9884", "9895", "9896", "9897", "9899", "9911", "9901", "9907", "11917", "11919"]

# Se sua função já estiver no extrator.py, você pode importá-la assim:
# from app.states.extrator import extrair_limites_faltas

async def extrair_limite_faltas(page, codigo_disciplina: str):
    await page.click("#Notas_-_Faltas")
    await page.get_by_text("Frequência da Turma").click()

    select = page.locator("#turma")
    await select.wait_for(timeout=10_000)

    opcoes_disponiveis = await select.locator("option").all_inner_texts()
    opcoes_disponiveis.pop(0)
    for opcao in opcoes_disponiveis:
        cd_dis = opcao[:opcao.find('-')].strip()
        if codigo_disciplina == cd_dis:
            carga_horaria = opcao[opcao.find(':')+1:].strip()
            print(carga_horaria)
            return carga_horaria

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

            print("⚙️ Executando o método 'extrair_limites_faltas'...")
            # Aqui chamamos o seu novo scrapper
            for codigo in CODIGOS:
                await extrair_limite_faltas(page, codigo)
            
            print("\n✅ Resultado retornado pelo seu método:")
            print(json.dumps(resultado, indent=4, ensure_ascii=False))

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
