import reflex as rx
import os
import requests
from sqlmodel import select
import sqlmodel as sm
from app.models import PerfilAcademico

class AdminState(rx.State):
    is_checking_sisav: bool = False
    sisav_status: str = "Verificando..."
    db_status: str = "Verificando..."
    
    @rx.var
    def is_production(self) -> bool:
        """Verifica se o app está rodando em produção"""
        # Geralmente em produção temos um banco postgresql setado na URL
        db_url = os.environ.get("DB_URL", "")
        if "postgresql" in db_url:
            return True
        return False
        
    @rx.event
    async def check_systems(self):
        """Verifica a saúde dos sistemas em background"""
        self.sisav_status = "Testando..."
        self.db_status = "Testando..."
        yield
        
        # 1. Checar Banco de Dados
        try:
            with rx.session() as sessao:
                # Faz uma query super leve só para ver se o banco responde
                sessao.exec(select(sm.func.count(PerfilAcademico.id))).first()
                self.db_status = "Online"
        except Exception as e:
            print(f"Erro no banco: {e}")
            self.db_status = "Offline"
            
        yield
        
        # 2. checa SISAV (Timeout 15s)
        self.is_checking_sisav = True
        yield
        
        try:
            # faz a requisição para a página de login do SISAV
            response = requests.get("https://sisav.uem.br/", timeout=15)
            if response.status_code == 200:
                self.sisav_status = "Online"
            else:
                self.sisav_status = f"Erro {response.status_code}"
        except requests.exceptions.Timeout:
            self.sisav_status = "Timeout (>15s)"
        except Exception as e:
            print(f"Erro ao checar SISAV: {e}")
            self.sisav_status = "Offline"
        finally:
            self.is_checking_sisav = False
