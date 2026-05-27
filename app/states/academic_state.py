import reflex as rx
from typing import TypedDict


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


LIMITE_FALTAS = 16


def _calc_status(media: float, faltas: int) -> str:
    if faltas >= LIMITE_FALTAS:
        return "Reprovado por Falta"
    if media >= 7.0:
        return "Aprovado"
    if media >= 4.0:
        return "Exame"
    return "Reprovado por Nota"


class AcademicState(rx.State):
    limite_faltas: int = LIMITE_FALTAS
    # Initial realistic sample data
    disciplinas: list[Disciplina] = [
        {
            "id": "1",
            "nome": "Cálculo Diferencial e Integral I",
            "faltas": 4,
            "nota1": 8.5,
            "nota2": 7.0,
            "nota3": 7.5,
            "media": 7.67,
            "status": "Aprovado",
        },
        {
            "id": "2",
            "nome": "Algoritmos e Estruturas de Dados",
            "faltas": 12,
            "nota1": 9.0,
            "nota2": 8.5,
            "nota3": 9.5,
            "media": 9.00,
            "status": "Aprovado",
        },
        {
            "id": "3",
            "nome": "Física Geral e Experimental I",
            "faltas": 20,
            "nota1": 5.0,
            "nota2": 6.0,
            "nota3": 4.5,
            "media": 5.17,
            "status": "Reprovado por Falta",
        },
        {
            "id": "4",
            "nome": "Álgebra Linear aplicada",
            "faltas": 6,
            "nota1": 4.5,
            "nota2": 5.5,
            "nota3": 6.0,
            "media": 5.33,
            "status": "Exame",
        },
        {
            "id": "5",
            "nome": "Introdução à Engenharia de Software",
            "faltas": 2,
            "nota1": 9.5,
            "nota2": 10.0,
            "nota3": 9.0,
            "media": 9.50,
            "status": "Aprovado",
        },
        {
            "id": "6",
            "nome": "Química Tecnológica Geral",
            "faltas": 8,
            "nota1": 3.0,
            "nota2": 4.0,
            "nota3": 3.5,
            "media": 3.50,
            "status": "Reprovado por Nota",
        },
    ]

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

    @rx.event
    def handle_submit(self, form_data: dict):
        nome = form_data.get("nome", "").strip()
        if not nome:
            return rx.toast(
                "Por favor, preencha o nome da disciplina.", duration=3000
            )

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