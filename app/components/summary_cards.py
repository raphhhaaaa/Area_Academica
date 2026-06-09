import reflex as rx
from app.states.academic_state import AcademicState


def card_stat(
    title: str, value: rx.Var, subtitle: str, icon_name: str, color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    title,
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-xs font-bold text-gray-500 uppercase tracking-widest",
                        "text-xs font-bold text-gray-400 uppercase tracking-widest",
                    ),
                ),
                rx.el.p(
                    value,
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-3xl font-extrabold text-gray-100 mt-2.5 tracking-tight group-hover:text-blue-400 transition-colors duration-200",
                        "text-3xl font-extrabold text-gray-900 mt-2.5 tracking-tight group-hover:text-blue-600 transition-colors duration-200",
                    ),
                ),
                rx.el.p(
                    subtitle,
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "text-xs text-gray-400 mt-1.5 font-medium",
                        "text-xs text-gray-500 mt-1.5 font-medium",
                    ),
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.icon(
                    icon_name,
                    class_name=f"h-6 w-6 {color_class} transition-transform duration-300 group-hover:scale-110",
                ),
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "p-3 bg-gray-800 rounded-xl group-hover:bg-blue-950/40 transition-colors duration-300",
                    "p-3 bg-gray-50 rounded-xl group-hover:bg-blue-50/50 transition-colors duration-300",
                ),
            ),
            class_name="flex items-start justify-between",
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-xs hover:shadow-md hover:border-blue-900/50 transition-all duration-300 group cursor-default",
            "bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs hover:shadow-md hover:border-blue-100 transition-all duration-300 group cursor-default",
        ),
    )


def summary_cards() -> rx.Component:
    return rx.el.div(
        card_stat(
            "Média Geral",
            AcademicState.media_geral.to(str),
            "Média ponderada do período",
            "award",
            "text-blue-600",
        ),
        card_stat(
            "Disciplinas",
            AcademicState.total_disciplinas.to(str),
            "Grade curricular ativa",
            "book-open",
            "text-indigo-600",
        ),
        card_stat(
            "Total de Faltas",
            AcademicState.total_faltas.to(str),
            "O limite é calculado por: 25% da C.H",
            "calendar-x",
            "text-amber-600",
        ),
        card_stat(
            "Aprovadas",
            AcademicState.aprovadas_count.to(str),
            "Critério de aprovação: Nota ≥ 6.0",
            "message_circle_check",
            "text-emerald-600",
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full mb-8",
    )