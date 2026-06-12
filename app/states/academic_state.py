import reflex as rx
from typing import TypedDict
import json
from sqlmodel import select
from app.models import PerfilAcademico
from app.security import encrypt_password, decrypt_password
from app.states.extrator import rodar_extrator, CredenciaisInvalidasError, AnoLetivoInvalidoError
from app.states.config import salvar_credenciais
from datetime import date
from pydantic import BaseModel


class Disciplina(TypedDict):
    id: str
    nome: str
    faltas: int
    limite_faltas: int
    nota1: float
    nota2: float
    nota3: float
    media: float
    status: str  # "Aprovado", "Exame", "Reprovado por Falta", "Reprovado por Nota", "Em andamento"
    em_andamento: bool  # True quando o semestre ainda está em curso (Situação = Matriculado)
    faltas_originais: int  # Faltas vindas do SISAV — valor mínimo imutável
    status_original: str  # Status oficial do SISAV — nunca é alterado, usado para restaurar
    horarios: list[dict]

class CelulaHorario(BaseModel):
    disciplina_id: str = ""
    disciplina_nome: str = ""
    sala: str = ""
    vazio: bool = True

class LinhaHorario(BaseModel):
    horario: str = ""
    segunda: CelulaHorario = CelulaHorario()
    terca: CelulaHorario = CelulaHorario()
    quarta: CelulaHorario = CelulaHorario()
    quinta: CelulaHorario = CelulaHorario()
    sexta: CelulaHorario = CelulaHorario()
    sabado: CelulaHorario = CelulaHorario()

class Aluno(TypedDict):
    ra: str
    nome: str
    curso: str
    turno: str
    campus: str
    serie: str
    sit_acad: str


LIMITE_FALTAS_PADRAO = 16


# Mapeamento dos status do SISAV para os nossos labels internos
_MAP_STATUS_SISAV = {
    "Aprovado":   "Aprovado",
    "Aprovada":   "Aprovado",
    "Rep. Nota":  "Reprovado por Nota",
    "Rep. Falta": "Reprovado por Falta",
    "Reprovado":  "Reprovado por Nota",
    "Exame":      "Exame",
    "Em Exame":   "Exame",
}


def _calc_status(media: float, faltas: int, limite: int = LIMITE_FALTAS_PADRAO) -> str:
    """Calcula o status parcial a partir das notas já disponíveis (semestre em andamento)."""
    if faltas >= limite:
        return "Reprovado por Falta"
    if media >= 7.0:
        return "Aprovado"
    if media >= 4.0:
        return "Exame"
    return "Reprovado por Nota"


def _resolver_status(situacao_sisav: str, media: float, faltas: int, limite: int) -> tuple[str, bool]:
    """
    Decide o status final da disciplina:
    - Se o SISAV ainda não encerrou a matéria (situação == Matriculado ou vazia), retorna "Em andamento".
    - Caso contrário, usa o status oficial do SISAV mapeado para nossos labels.
    Retorna (status_display, em_andamento).
    """
    situacao = situacao_sisav.strip() if situacao_sisav else ""

    if situacao == "" or situacao == "Matriculado":
        return "Em andamento", True

    # Usa o mapeamento; se não reconhecer, mantém o texto do SISAV
    status_mapeado = _MAP_STATUS_SISAV.get(situacao, situacao)
    return status_mapeado, False


def formatar_dados_sisav(dados_brutos: dict) -> tuple[list, dict]:
    """
    Formata os dados brutos vindos do extrator Playwright.
    Retorna uma tupla: (lista_de_disciplinas, dict_aluno)
    """

    # --- Disciplinas ---
    lista_formatada_disciplina: list[Disciplina] = []
    lista_bruta_disciplinas = dados_brutos.get("disciplinas", [])

    for dis in lista_bruta_disciplinas:
        lista_notas = dis.get('Notas', [])

        nota1 = lista_notas[0].get("Nota", 0.0) if len(lista_notas) > 0 else 0.0
        nota2 = lista_notas[1].get("Nota", 0.0) if len(lista_notas) > 1 else 0.0
        nota3 = lista_notas[2].get("Nota", 0.0) if len(lista_notas) > 2 else 0.0

        faltas = int(dis.get('FaltasManuais', dis.get('Faltas', 0)))
        faltas_originais = int(dis.get('FaltasOriginais', dis.get('Faltas', 0)))
        limite = int(dis.get('LimiteFaltas', LIMITE_FALTAS_PADRAO))

        media = 0.0
        if len(lista_notas) > 0:
            soma = sum(nota['Nota'] for nota in lista_notas)
            media = soma / len(lista_notas)

        # Usa situação oficial do SISAV quando disponível
        situacao_sisav = str(dis.get('Situação', dis.get('Situacao', '')))
        status, em_andamento = _resolver_status(situacao_sisav, media, faltas, limite)

        disciplina_formatada: Disciplina = {
            "id": dis.get("Código", "S/N"),
            "nome": dis.get("Disciplina", "Desconhecida"),
            "faltas": faltas,
            "faltas_originais": faltas_originais,
            "limite_faltas": limite,
            "nota1": float(nota1),
            "nota2": float(nota2),
            "nota3": float(nota3),
            "media": round(media, 1),
            "status": status,
            "status_original": status,  # espelho imutável do status inicial
            "em_andamento": em_andamento,
            "horarios": dis.get("Horarios", [])
        }
        lista_formatada_disciplina.append(disciplina_formatada)

    # --- Aluno ---
    lista_bruta_aluno = dados_brutos.get("aluno", {})

    # O extrator retorna aluno como dict (não lista), tratar ambos os casos
    if isinstance(lista_bruta_aluno, list):
        alu = lista_bruta_aluno[0] if lista_bruta_aluno else {}
    else:
        alu = lista_bruta_aluno

    aluno_formatado: Aluno = {
        "ra": str(alu.get("RA", "")),
        "nome": alu.get("Nome", ""),
        "curso": alu.get("Curso", ""),
        "turno": alu.get("Turno", ""),
        "campus": alu.get("Campus/Polo", ""),
        "serie": str(alu.get("Série", "")),
        "sit_acad": str(alu.get("Sit. Acad.", ""))
    }

    return lista_formatada_disciplina, aluno_formatado


class AcademicState(rx.State):
    aluno: Aluno = {"ra": "", "nome": "", "curso": "", "turno": "", "campus": "", "serie": "", "sit_acad": ""}

    limite_faltas: int = LIMITE_FALTAS_PADRAO
    disciplinas: list[Disciplina] = []
    is_loading: bool = False
    ano_letivo: str = str(date.today().year)
    error_message: str = ""

    # Modal trigger state
    show_modal: bool = False

    # Form states (usados no login)
    form_usuario: str = ""
    form_senha: str = ""
    show_password: bool = False

    # Sidebar state
    is_sidebar_open: bool = True

    @rx.event
    def toggle_show_password(self):
        self.show_password = not self.show_password

    # Search and Filters
    search_query: str = ""
    status_filter: str = "Todas"  # "Todas", "Aprovado", "Exame", "Reprovado"

    # Theme state
    is_dark: bool = True

    @rx.var
    def get_nome_aluno(self) -> str:
        return self.aluno.get("nome", "")

    @rx.var
    def get_ra_aluno(self) -> str:
        ra = self.aluno.get("ra", "")[2:]
        return f"RA: {ra}" if ra else "Sem matrícula"

    @rx.var
    def tem_dados(self) -> bool:
        return len(self.disciplinas) > 0

    @rx.event
    def toggle_theme(self):
        self.is_dark = not self.is_dark

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.var
    def total_faltas(self) -> int:
        return sum(d["faltas"] for d in self.disciplinas)

    @rx.var
    def media_geral(self) -> float:
        if not self.disciplinas:
            return 0.0
        return round(
            sum(d["media"] for d in self.disciplinas) / len(self.disciplinas), 2
        )

    @rx.var
    def total_disciplinas(self) -> int:
        return len(self.disciplinas)

    @rx.var
    def materias_na_grade(self) -> int:
        return sum(1 for d in self.disciplinas if d["em_andamento"])

    def _gerar_grade(self, semestre_alvo: int) -> list[LinhaHorario]:
        if not self.disciplinas:
            return []
            
        horarios_unicos = set()
        for d in self.disciplinas:
            for h in d.get("horarios", []):
                if h.get("semestre", 1) == semestre_alvo:
                    horarios_unicos.add(h.get("horario"))
                
        if not horarios_unicos:
            return []
            
        horarios_ordenados = sorted(list(horarios_unicos))
        linhas = []
        
        for horario in horarios_ordenados:
            linha = LinhaHorario(horario=horario)
            
            # Mapeamento do nome do dia para o atributo da classe
            mapa_dias = {
                "Segunda": "segunda",
                "Terça": "terca",
                "Quarta": "quarta",
                "Quinta": "quinta",
                "Sexta": "sexta",
                "Sábado": "sabado"
            }
            
            for d in self.disciplinas:
                for h in d.get("horarios", []):
                    if h.get("semestre", 1) == semestre_alvo and h.get("horario") == horario:
                        dia_str = h.get("dia")
                        attr_dia = mapa_dias.get(dia_str)
                        if attr_dia:
                            celula = CelulaHorario(
                                disciplina_id=d.get("id", ""),
                                disciplina_nome=d.get("nome", ""),
                                sala=h.get("sala", ""),
                                vazio=False
                            )
                            setattr(linha, attr_dia, celula)
                            
            linhas.append(linha)
            
        return linhas

    @rx.var
    def grade_horarios_1(self) -> list[LinhaHorario]:
        return self._gerar_grade(1)

    @rx.var
    def grade_horarios_2(self) -> list[LinhaHorario]:
        return self._gerar_grade(2)

    @rx.var
    def aprovadas_count(self) -> int:
        return len([d for d in self.disciplinas if d["status"] == "Aprovado"])

    @rx.var
    def filtered_disciplinas(self) -> list[Disciplina]:
        result = self.disciplinas
        if self.search_query:
            query = self.search_query.lower()
            result = [d for d in result if query in d["nome"].lower()]

        if self.status_filter != "Todas":
            if self.status_filter == "Reprovado":
                result = [d for d in result if "Reprovado" in d["status"]]
            else:
                result = [
                    d for d in result if d["status"] == self.status_filter
                ]

        return result

    @rx.event
    def set_search_query(self, val: str):
        self.search_query = val

    @rx.event
    def set_status_filter(self, val: str):
        self.status_filter = val

    @rx.event
    def toggle_modal(self):
        self.show_modal = not self.show_modal
        self.error_message = ""

    @rx.event
    async def handle_login(self, form_data: dict):
        usuario = form_data.get("usuario", "").strip()
        senha = form_data.get("senha", "")
        
        if not usuario or not senha:
            self.error_message = "Por favor, preencha RA e Senha."
            return

        self.error_message = ""
        self.is_loading = True
        yield

        try:
            with rx.session() as sessao:
                perfil = sessao.exec(select(PerfilAcademico).where(PerfilAcademico.ra == usuario)).first()
                if perfil:
                    senha_salva = decrypt_password(perfil.senha_criptografada)
                    if senha_salva == senha:
                        # Login bem-sucedido via banco local
                        dados_brutos = json.loads(perfil.dados_json)
                        disciplinas, aluno = formatar_dados_sisav(dados_brutos)
                        self.disciplinas = disciplinas
                        self.aluno = aluno
                        self.form_usuario = usuario
                        self.form_senha = "" # Limpar senha do form em memória
                        self.is_loading = False
                        yield rx.redirect("/dashboard")
                        return
                    else:
                        # Senha não confere com o banco local
                        self.error_message = "Credenciais inválidas no banco de dados local."
                        self.is_loading = False
                        return
                        
            # Se chegou aqui, não tem perfil, primeira extração
            self.ano_letivo = str(date.today().year)
            dados_brutos = await rodar_extrator(
                usuario=usuario,
                senha=senha,
                ano_letivo=None,
            )
            
            with rx.session() as sessao:
                perfil = PerfilAcademico(
                    ra=usuario, 
                    senha_criptografada=encrypt_password(senha),
                    dados_json=json.dumps(dados_brutos)
                )
                sessao.add(perfil)
                sessao.commit()
                
            disciplinas, aluno = formatar_dados_sisav(dados_brutos)
            self.disciplinas = disciplinas
            self.aluno = aluno
            self.form_usuario = usuario
            self.form_senha = ""
            
            yield rx.redirect("/dashboard")

        except CredenciaisInvalidasError as e:
            self.error_message = str(e)
        except Exception as e:
            import traceback
            tb_str = traceback.format_exc()
            print(tb_str)
            
            ultima_linha = tb_str.strip().split('\n')[-1]
            self.error_message = f"Falha inesperada: {ultima_linha[:150]}"
        finally:
            self.is_loading = False

    @rx.event
    async def handle_sync(self, form_data: dict):
        ano = form_data.get("ano", "").strip()
        usuario = self.form_usuario

        if not usuario:
            self.error_message = "Usuário não logado. Por favor, volte ao login."
            return

        self.error_message = ""
        self.is_loading = True
        yield

        try:
            # Recupera senha criptografada do banco
            with rx.session() as sessao:
                perfil = sessao.exec(select(PerfilAcademico).where(PerfilAcademico.ra == usuario)).first()
                if not perfil:
                    raise Exception("Perfil não encontrado no banco de dados.")
                senha = decrypt_password(perfil.senha_criptografada)

            self.ano_letivo = ano
            dados_brutos = await rodar_extrator(
                usuario=usuario,
                senha=senha,
                ano_letivo=ano or None,
            )
            
            with rx.session() as sessao:
                perfil = sessao.exec(select(PerfilAcademico).where(PerfilAcademico.ra == usuario)).first()
                if perfil:
                    perfil.dados_json = json.dumps(dados_brutos)
                    sessao.commit()
                
            disciplinas, aluno = formatar_dados_sisav(dados_brutos)
            self.disciplinas = disciplinas
            self.aluno = aluno
            self.show_modal = False
            
            yield rx.toast.success(f"Dados atualizados com sucesso (Ano: {ano or 'atual'})", duration=4000)

        except CredenciaisInvalidasError as e:
            self.error_message = "A senha do portal foi alterada. Atualize seu login."
        except AnoLetivoInvalidoError as e:
            self.error_message = str(e)
        except Exception as e:
            import traceback
            tb_str = traceback.format_exc()
            print(tb_str)
            
            ultima_linha = tb_str.strip().split('\n')[-1]
            self.error_message = f"Falha ao sincronizar: {ultima_linha[:150]}"
        finally:
            self.is_loading = False

    @rx.event
    def carregar_do_banco(self, ra: str):
        """Tenta buscar os dados de um aluno direto do banco SQLite sem precisar rodar o scraper."""
        if not ra:
            return
            
        with rx.session() as sessao:
            perfil = sessao.exec(select(PerfilAcademico).where(PerfilAcademico.ra == ra)).first()
            if perfil:
                dados_brutos = json.loads(perfil.dados_json)
                disciplinas, aluno = formatar_dados_sisav(dados_brutos)
                self.disciplinas = disciplinas
                self.aluno = aluno
                self.form_usuario = ra
                return rx.toast.success("Dados resgatados do banco de dados local!", duration=3000)
            else:
                return rx.toast.warning("Usuário não encontrado no banco. Sincronize com o SISAV.", duration=3000)

    @rx.var
    def contar_usuarios_registrados(self) -> int:
        """Conta quantos usuários registrados existem no banco"""
        try: 
            with rx.session() as sessao:
                import sqlmodel as sm
                # O sessao.exec vai ao banco rodar o select, e o .one() pega o número exato
                usuarios = sessao.exec(select(sm.func.count(PerfilAcademico.id))).one()
                return usuarios
        except Exception as e:
            print(f"Erro ao contar usuários registrados: {e}")
            return 0

    @rx.event
    def remover_disciplina(self, disc_id: str):
        self.disciplinas = [d for d in self.disciplinas if d["id"] != disc_id]
        return rx.toast("Disciplina removida.", duration=2000)

    @rx.event
    def incrementar_falta(self, disc_id: str):
        for d in self.disciplinas:
            if d["id"] == disc_id:
                limite = d.get("limite_faltas", LIMITE_FALTAS_PADRAO)
                if d["faltas"] >= limite:
                    return rx.toast(
                        f"Limite de {limite} faltas já atingido.",
                        duration=2000,
                    )
                d["faltas"] = d["faltas"] + 1
                if d["faltas"] >= limite:
                    # Reprovado por falta tem prioridade absoluta
                    d["status"] = "Reprovado por Falta"
                else:
                    # Restaura status original do SISAV se faltas < limite
                    d["status"] = d.get("status_original", d["status"])
                self._update_db_faltas(disc_id, d["faltas"])
                break

    @rx.event
    def decrementar_falta(self, disc_id: str):
        for d in self.disciplinas:
            if d["id"] == disc_id:
                minimo = d.get("faltas_originais", 0)
                if d["faltas"] <= minimo:
                    return
                d["faltas"] = d["faltas"] - 1
                limite = d.get("limite_faltas", LIMITE_FALTAS_PADRAO)
                if d["faltas"] >= limite:
                    d["status"] = "Reprovado por Falta"
                else:
                    # Restaura status original do SISAV se faltas < limite
                    d["status"] = d.get("status_original", d["status"])
                self._update_db_faltas(disc_id, d["faltas"])
                break

    def _update_db_faltas(self, disc_id: str, new_faltas: int):
        """Atualiza a quantidade de faltas manuais diretamente no banco de dados"""
        if not self.form_usuario:
            return
            
        with rx.session() as sessao:
            perfil = sessao.exec(select(PerfilAcademico).where(PerfilAcademico.ra == self.form_usuario)).first()
            if perfil:
                dados_brutos = json.loads(perfil.dados_json)
                for dis in dados_brutos.get("disciplinas", []):
                    if str(dis.get("Código", "")) == disc_id:
                        if "FaltasOriginais" not in dis:
                            dis["FaltasOriginais"] = dis.get("Faltas", 0)
                        dis["FaltasManuais"] = new_faltas
                        break
                perfil.dados_json = json.dumps(dados_brutos)
                sessao.commit()

    @rx.var
    def ano_diferente(self) -> bool:
        if self.ano_letivo is not None and self.ano_letivo != "":
            current_year = date.today().year
            return int(self.ano_letivo) != date.today().year
        return False

    @rx.event
    def logout(self):
        """Limpa o estado da sessão atual e redireciona para o login."""
        self.form_usuario = ""
        self.form_senha = ""
        self.disciplinas = []
        self.aluno = {"ra": "", "nome": "", "curso": "", "turno": "", "campus": "", "serie": "", "sit_acad": ""}
        self.ano_letivo = str(date.today().year)
        self.is_loading = False
        return rx.redirect("/")

    @rx.event
    def verificar_admin(self):
        """Verifica se o usuário pode acessar rotas protegidas do admin."""
        if self.form_usuario == "":
            return rx.redirect("/")
        # Como o usuário optou por não colocar o RA "chumbado", deixaremos 
        # aberto por enquanto, mas com redirecionamento de anônimos para a login page.
        # Descomente a linha abaixo e adicione o RA correto para restringir totalmente:
        if not self.isAdmin:
            return rx.redirect("/dashboard")
        
    @rx.var
    def isAdmin(self) -> bool:
        return not self.form_usuario != "ra147190"

