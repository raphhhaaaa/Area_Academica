import reflex as rx
from typing import TypedDict
from app.states.extrator import rodar_extrator


class Disciplina(TypedDict):
    id: str
    nome: str
    faltas: int
    nota1: float
    nota2: float
    nota3: float
    media: float
    status: (
        str  # "Aprovado", "Exame", "Reprovado por Falta", "Reprovado por Nota"
    )

class Aluno(TypedDict):
    ra: int
    nome: str
    curso: str
    turno: str
    campus: str
    serie: int
    sit_acad: int

LIMITE_FALTAS = 16


def _calc_status(media: float, faltas: int) -> str:
    if faltas >= LIMITE_FALTAS:
        return "Reprovado por Falta"
    if media >= 7.0:
        return "Aprovado"
    if media >= 4.0:
        return "Exame"
    return "Reprovado por Nota"


def formatar_dados_sisav(dados_brutos: dict) -> list[Disciplina]:            # [0] para Disciplinas ; [1] para Aluno
    lista_dados: list[list] = []
    
    lista_bruta_disciplinas = dados_brutos.get("disciplinas", [])
    lista_formatada_disciplina: list[Disciplina] = []

    for dis in lista_bruta_disciplinas:
        lista_notas = dis.get('Notas', [])

        nota1 = lista_notas[0].get("Nota", 0.0) if len(lista_notas) > 0 else 0.0
        nota2 = lista_notas[1].get("Nota", 0.0) if len(lista_notas) > 1 else 0.0
        nota3 = lista_notas[2].get("Nota", 0.0) if len(lista_notas) > 2 else 0.0

        faltas = dis.get('Faltas', 0)
        media = 0.0        
        if len(lista_notas) > 0:
            soma = 0.0
            for nota in lista_notas:
                soma += nota['Nota']
            media = soma / len(lista_notas)

        status_calculado = _calc_status(media, faltas)

        disicplina_tipada = Disciplina = {
            "id": dis.get("Código", "S/N"),
            "nome": dis.get("Disciplina", "Desconhecida"),
            "faltas": faltas,
            "nota1": float(nota1),
            "nota2": float(nota2),
            "nota3": float(nota3),
            "media": round(media, 1),
            "status": status_calculado
        }
        lista_formatada_disciplina.append(disicplina_tipada)

    lista_bruta_aluno = dados_brutos.get("aluno", [])
    lista_formatada_aluno: list[Aluno] = []

    for alu in lista_bruta_aluno:

        aluno_tipado = Aluno = {
            "ra": alu.get("RA", ""),
            "nome": alu.get("Nome", ""),
            "curso": alu.get("Curso", ""),
            "turno": alu.get("Turno", ""),
            "campus": alu.get("Campus/Polo", ""),
            "serie": alu.get("Série", ""),
            "sit_acad": alu.get("Sit. Acad.", "")
        }
        lista_formatada_aluno.append(aluno_tipado)
    
    return lista_dados

class AcademicState(rx.State):
    aluno: Aluno = {"ra": "", "nome": "Carregando...", "curso": ""}
    
    limite_faltas: int = LIMITE_FALTAS
    disciplinas: list[Disciplina] = []
    is_loading: bool = False

    @rx.var
    def get_nome_aluno(self) -> str:
        print(self.aluno)
        return self.aluno.get("nome", "")

    @rx.event
    def disparar_sincronizacao(self):
        self.is_loading = True
        return AcademicState.executar_scraping_sync
    
    async def executar_scraping_sync(self):
        self.is_loading = True
        try:
            dados_brutos = await rodar_extrator()
            self.disciplinas = formatar_dados_sisav(dados_brutos)[0]
            self.aluno = formatar_dados_sisav(dados_brutos)[1]
        except Exception as e:
            return rx.toast(f"Erro ao extrair dados: {str(e)}")
        finally:
            self.is_loading - False

    # Modal trigger state
    show_modal: bool = False

    # Form states (used for adding or editing)
    form_nome: str = ""
    form_faltas: int = 0
    form_nota1: float = 0.0
    form_nota2: float = 0.0
    form_nota3: float = 0.0

    # Search and Filters
    search_query: str = ""
    status_filter: str = "Todas"  # "Todas", "Aprovado", "Exame", "Reprovado"

    # Theme state
    is_dark: bool = False

    @rx.event
    def toggle_theme(self):
        self.is_dark = not self.is_dark

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
        # Reset form values
        if self.show_modal:
            self.form_nome = ""
            self.form_faltas = 0
            self.form_nota1 = 0.0
            self.form_nota2 = 0.0
            self.form_nota3 = 0.0


    def salvar_usuario(self, login, senha):
        return 

    @rx.event
    def handle_submit(self, form_data: dict):
        login = form_data.get("nome", "").strip()
        senha = form_data.get("senha", "")
        if not login:
            return rx.toast(
                "Por favor, preencha o campo de Usuário.", duration=3000
            )
        
        if not senha:
            return rx.toast(
                "Por favor, preencha o campo de Senha", duration=3000
            )

        usuario_login = {
            "usuario": login,
            "senha": senha
        }
        
        self.salvar_usuario(login, senha)
        return 

        try:
            faltas = int(form_data.get("faltas", 0))
            n1 = float(form_data.get("nota1", 0.0))
            n2 = float(form_data.get("nota2", 0.0))
            n3 = float(form_data.get("nota3", 0.0))
        except ValueError:
            return rx.toast(
                "Valores inválidos para notas ou faltas.", duration=3000
            )

        # Cap values
        n1 = max(0.0, min(10.0, n1))
        n2 = max(0.0, min(10.0, n2))
        n3 = max(0.0, min(10.0, n3))
        faltas = max(0, faltas)

        media = round((n1 + n2 + n3) / 3.0, 2)

        # Status calculation rule (Faltas limit: 16)
        if faltas >= 16:
            status = "Reprovado por Falta"
        elif media >= 7.0:
            status = "Aprovado"
        elif media >= 4.0:
            status = "Exame"
        else:
            status = "Reprovado por Nota"

        import uuid

        nova: Disciplina = {
            "id": str(uuid.uuid4()),
            "nome": nome,
            "faltas": faltas,
            "nota1": n1,
            "nota2": n2,
            "nota3": n3,
            "media": media,
            "status": status,
        }

        self.disciplinas.append(nova)
        self.show_modal = False
        return rx.toast(
            f"Disciplina '{nome}' adicionada com sucesso!", duration=3000
        )

    @rx.event
    def remover_disciplina(self, disc_id: str):
        self.disciplinas = [d for d in self.disciplinas if d["id"] != disc_id]
        return rx.toast("Disciplina removida.", duration=2000)

    @rx.event
    def incrementar_falta(self, disc_id: str):
        for d in self.disciplinas:
            if d["id"] == disc_id:
                if d["faltas"] >= LIMITE_FALTAS:
                    return rx.toast(
                        f"Limite de {LIMITE_FALTAS} faltas já atingido.",
                        duration=2000,
                    )
                d["faltas"] = d["faltas"] + 1
                d["status"] = _calc_status(d["media"], d["faltas"])
                break

    @rx.event
    def decrementar_falta(self, disc_id: str):
        for d in self.disciplinas:
            if d["id"] == disc_id:
                if d["faltas"] <= 0:
                    return
                d["faltas"] = d["faltas"] - 1
                d["status"] = _calc_status(d["media"], d["faltas"])
                break