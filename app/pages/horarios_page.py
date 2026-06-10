import reflex as rx
from app.states.academic_state import AcademicState
from app.components.header import header_section
from app.components.sidebar import sidebar

def render_celula(celula: dict) -> rx.Component:
    return rx.el.td(
        rx.cond(
            celula.vazio,
            rx.el.div(
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "h-14 w-full rounded-lg bg-gray-800/30 border border-dashed border-gray-800",
                    "h-14 w-full rounded-lg bg-gray-100/50 border border-dashed border-gray-200"
                )
            ),
            rx.el.div(
                rx.el.p(celula.disciplina_nome, class_name=rx.cond(
                    AcademicState.is_dark,
                    "font-semibold text-[11px] leading-tight text-blue-200 line-clamp-2",
                    "font-semibold text-[11px] leading-tight text-white line-clamp-2"
                )),
                rx.el.div(
                    rx.el.span(celula.disciplina_id, class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-[9px] bg-blue-900/50 text-blue-200 px-1 py-0.5 rounded font-bold",
                        "text-[9px] bg-blue-500 text-white px-1 py-0.5 rounded font-bold shadow-sm"
                    )),
                        
                    rx.el.div(
                        rx.el.span("Bloco - Sala", class_name=rx.cond(
                            AcademicState.is_dark,
                            "text-[8px] text-gray-400 italic uppercase tracking-wide",
                            "text-[8px] text-blue-200 italic uppercase tracking-wide"
                        )),
                        rx.el.span(celula.sala, class_name=rx.cond(
                            AcademicState.is_dark,
                            "text-[9px] text-gray-300 font-bold whitespace-nowrap truncate",
                            "text-[9px] text-white font-bold whitespace-nowrap truncate"
                        )),
                        class_name="flex flex-col items-end leading-none gap-0.5"
                    ),
                    class_name="flex items-center justify-between mt-1.5 gap-1"
                ),
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "w-full rounded-lg bg-blue-900/30 border border-blue-800/70 p-2 shadow hover:bg-blue-900/50 transition-colors",
                    "w-full rounded-lg bg-blue-600 border border-blue-700 p-2 shadow-md hover:bg-blue-700 hover:shadow-lg transition-all"
                )
            )
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "px-2 py-2 border-b border-gray-800 min-w-[130px] max-w-[160px] align-top",
            "px-2 py-2 border-b border-gray-200 min-w-[130px] max-w-[160px] align-top"
        )
    )

def render_linha(linha: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            linha.horario,
            class_name=rx.cond(
                AcademicState.is_dark,
                "px-4 py-4 text-xs font-medium text-gray-400 whitespace-nowrap border-b border-gray-800 align-middle",
                "px-4 py-4 text-xs font-medium text-gray-500 whitespace-nowrap border-b border-gray-200 align-middle"
            )
        ),
        render_celula(linha.segunda),
        render_celula(linha.terca),
        render_celula(linha.quarta),
        render_celula(linha.quinta),
        render_celula(linha.sexta),
        render_celula(linha.sabado),
        class_name=rx.cond(
            AcademicState.is_dark,
            "hover:bg-gray-900/30 transition-colors",
            "hover:bg-gray-50/50 transition-colors"
        )
    )

def horarios_table(titulo: str, grade_var) -> rx.Component:
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    
    # Cabecalho da tabela
    thead = rx.el.thead(
        rx.el.tr(
            rx.el.th(
                "Horário",
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "px-4 py-3 text-left text-xs font-semibold text-gray-300 tracking-wider bg-gray-900 border-b border-gray-800",
                    "px-4 py-3 text-left text-xs font-semibold text-gray-600 tracking-wider bg-gray-50 border-b border-gray-200"
                )
            ),
            *[
                rx.el.th(
                    dia,
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "px-4 py-3 text-center text-xs font-semibold text-gray-300 tracking-wider bg-gray-900 border-b border-gray-800",
                        "px-4 py-3 text-center text-xs font-semibold text-gray-600 tracking-wider bg-gray-50 border-b border-gray-200"
                    )
                ) for dia in dias
            ]
        )
    )
    
    # Linhas vazias para skeleton
    linhas_vazias = []
    horarios_ficticios = ["19:30 - 20:20", "20:20 - 21:10", "21:20 - 22:10", "22:10 - 23:00"]
    
    for horario in horarios_ficticios:
        colunas = [
            rx.el.td(
                horario,
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "px-4 py-4 text-xs font-medium text-gray-400 whitespace-nowrap border-b border-gray-800",
                    "px-4 py-4 text-xs font-medium text-gray-500 whitespace-nowrap border-b border-gray-200"
                )
            )
        ]
        
        for _ in dias:
            colunas.append(
                rx.el.td(
                    rx.el.div(
                        class_name=rx.cond(
                            AcademicState.is_dark,
                            "h-10 w-full rounded-lg bg-gray-800/30 border border-dashed border-gray-800",
                            "h-10 w-full rounded-lg bg-gray-100/50 border border-dashed border-gray-200"
                        )
                    ),
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "px-2 py-2 border-b border-gray-800 min-w-[120px]",
                        "px-2 py-2 border-b border-gray-200 min-w-[120px]"
                    )
                )
            )
            
        linhas_vazias.append(
            rx.el.tr(
                *colunas,
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "hover:bg-gray-900/50 transition-colors",
                    "hover:bg-gray-50 transition-colors"
                )
            )
        )

    tbody = rx.el.tbody(
        rx.cond(
            grade_var.length() > 0,
            rx.foreach(grade_var, render_linha),
            rx.fragment(*linhas_vazias)
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "bg-gray-950",
            "bg-white"
        )
    )
    
    return rx.el.div(
        rx.el.h2(titulo, class_name=rx.cond(
            AcademicState.is_dark,
            "text-lg font-bold text-gray-100 mb-4",
            "text-lg font-bold text-gray-800 mb-4"
        )),
        rx.el.div(
            rx.el.table(
                thead,
                tbody,
                class_name="w-full border-collapse"
            ),
            class_name=rx.cond(
                AcademicState.is_dark,
                "w-full overflow-x-auto rounded-xl border border-gray-800 bg-gray-950 shadow-sm",
                "w-full overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm"
            )
        ),
        class_name="w-full mt-8"
    )

def horarios_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="horarios"),
        rx.el.main(
            rx.el.div(
                header_section(
                    title="Horário de Aulas",
                    subtitle="Visualize sua grade de horários da semana.",
                ),
                horarios_table("1º Semestre", AcademicState.grade_horarios_1),
                horarios_table("2º Semestre", AcademicState.grade_horarios_2),
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
