import reflex as rx
from app.states.academic_state import AcademicState
from app.components.summary_cards import summary_cards
from app.components.discipline_list import discipline_list
from app.components.add_modal import add_modal

def header_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Portal do Estudante",
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-xs font-semibold bg-blue-950/40 text-blue-400 border border-blue-900/50 px-3 py-1 rounded-full",
                        "text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-100 px-3 py-1 rounded-full",
                    ),
                ),
                rx.el.h1(
                    "Área Acadêmica",
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-3xl font-extrabold text-gray-100 tracking-tight mt-3",
                        "text-3xl font-extrabold text-gray-900 tracking-tight mt-3",
                    ),
                ),
                rx.el.p(
                    "Gerencie suas disciplinas, acompanhe suas notas periódicas, controle faltas e evite exames.",
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-gray-400 mt-1 text-sm sm:text-base",
                        "text-gray-500 mt-1 text-sm sm:text-base",
                    ),
                ),
                class_name="flex-1",
            ),
            # Theme Toggle & Profile Card Container
            rx.el.div(
                # Profile Card
                rx.el.div(
                    rx.el.img(
                        src=rx.cond(
                            AcademicState.get_nome_aluno != "",
                            "https://api.dicebear.com/9.x/initials/svg?seed=" + AcademicState.get_nome_aluno,
                            "https://api.dicebear.com/9.x/initials/svg?seed=Aluno",
                        ),
                        alt="Foto do Estudante",
                        class_name="size-9 sm:size-11 rounded-full shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            rx.cond(
                                AcademicState.get_nome_aluno != "",
                                AcademicState.get_nome_aluno,
                                "Clique em Sincronizar",
                            ),
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "font-bold text-gray-100 text-xs sm:text-sm whitespace-nowrap",
                                "font-bold text-gray-900 text-xs sm:text-sm whitespace-nowrap",
                            ),
                        ),
                        rx.el.p(
                            AcademicState.get_ra_aluno,
                            class_name="text-[10px] sm:text-xs text-gray-400 font-medium whitespace-nowrap",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "flex items-center gap-2.5 sm:gap-3 bg-gray-900 p-2.5 sm:p-3 rounded-2xl border border-gray-800 shadow-xs",
                        "flex items-center gap-2.5 sm:gap-3 bg-white p-2.5 sm:p-3 rounded-2xl border border-gray-100 shadow-xs",
                    ),
                ),
                # Theme Toggle Button
                rx.el.button(
                    rx.cond(
                        AcademicState.is_dark,
                        rx.icon("sun", class_name="h-5 w-5 text-amber-400"),
                        rx.icon("moon", class_name="h-5 w-5 text-gray-600"),
                    ),
                    on_click=AcademicState.toggle_theme,
                    title="Alternar Tema",
                    aria_label="Alternar Tema (Claro/Escuro)",
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "p-3 rounded-2xl bg-gray-900 border border-gray-800 text-gray-100 hover:bg-gray-800/80 active:scale-95 transition-all shadow-xs flex items-center justify-center",
                        "p-3 rounded-2xl bg-white border border-gray-100 text-gray-800 hover:bg-gray-50 active:scale-95 transition-all shadow-xs flex items-center justify-center",
                    ),
                ),
                class_name="flex items-center justify-between sm:justify-start w-full sm:w-auto gap-2 sm:gap-3 shrink-0",
            ),
            class_name="flex flex-col-reverse sm:flex-row sm:items-center justify-between gap-5 mb-8 w-full",
        ),
        class_name="w-full",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            header_section(),
            summary_cards(),
            discipline_list(),
            add_modal(),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full",
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "font-['Inter'] bg-gray-950 min-h-screen w-screen flex flex-col transition-colors duration-200",
            "font-['Inter'] bg-gray-50 min-h-screen w-screen flex flex-col transition-colors duration-200",
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
    ],
)
app.add_page(index, route="/")