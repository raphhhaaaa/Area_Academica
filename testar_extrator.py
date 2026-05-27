# testar_extrator.py

import pprint
from app.states.extrator import rodar_extrator
from app.states.academic_state import formatar_dados_sisav

def testar_fluxo_completo():
    print("1. Iniciando o robô do Playwright...")
    
    try:
        # Roda o scraping real
        dados_brutos = rodar_extrator()
        
        print("\n=== 2. DADOS BRUTOS (JSON DO SCRAPER) ===")
        # Imprime o dicionário formatado com indentação
        pprint.pprint(dados_brutos)
        
        print("\n=== 3. FORMATANDO DADOS PARA O REFLEX ===")
        dados_formatados = formatar_dados_sisav(dados_brutos)
        
        print("\n=== 4. RESULTADO FINAL (O QUE A UI VAI RECEBER) ===")
        pprint.pprint(dados_formatados)
        
        print("\nSucesso! O fluxo está funcionando.")
        
    except Exception as e:
        print(f"\n❌ ERRO NO FLUXO: {e}")

if __name__ == "__main__":
    testar_fluxo_completo()