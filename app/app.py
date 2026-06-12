import reflex as rx
import app.models
from sqlmodel import SQLModel
from app.states.academic_state import AcademicState
from app.components.summary_cards import summary_cards
from app.components.discipline_list import discipline_list
from app.components.add_modal import add_modal
from app.components.sidebar import sidebar
from app.components.header import header_section
from app.pages.horarios_page import horarios_page
from app.pages.login_page import login_page
from app.pages.admin_page import admin_page
from app.states.admin_state import AdminState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                header_section(
                    title="Área Acadêmica", 
                    subtitle="Gerencie suas disciplinas, acompanhe suas notas, controle faltas e evite exames."
                ),
                summary_cards(),
                discipline_list(),
                add_modal(),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full",
            ),
            class_name="flex-1 min-h-screen overflow-y-auto"
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "dark font-['Inter'] bg-gray-950 min-h-screen w-full flex transition-colors duration-200",
            "font-['Inter'] bg-gray-50 min-h-screen w-full flex transition-colors duration-200",
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="manifest",
            href="/manifest.json"
        ),
        rx.el.meta(
            name="theme-color",
            content="#2563eb"
        )
    ],
)
app.add_page(login_page, route="/")
app.add_page(index, route="/dashboard")
app.add_page(horarios_page, route="/horarios")
app.add_page(admin_page, route="/admin-uem", on_load=[AcademicState.verificar_admin, AdminState.check_systems])

def init_db():
    try:
        with rx.session() as sessao:
            SQLModel.metadata.create_all(sessao.bind)
    except Exception as e:
        print(f"Erro ao inicializar tabelas: {e}")

init_db()