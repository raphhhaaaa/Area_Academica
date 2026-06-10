import reflex as rx
from app.states.academic_state import AcademicState, Disciplina
from datetime import date

def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            AcademicState.is_dark,
            rx.match(
                status,
                (
                    "Aprovado",
                    "inline-flex items-center gap-1.5 bg-emerald-950/40 text-emerald-400 border border-emerald-900/50 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-emerald-900/30 transition-colors duration-200",
                ),
                (
                    "Exame",
                    "inline-flex items-center gap-1.5 bg-amber-950/40 text-amber-400 border border-amber-900/50 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-amber-900/30 transition-colors duration-200",
                ),
                (
                    "Reprovado por Falta",
                    "inline-flex items-center gap-1.5 bg-rose-950/40 text-rose-400 border border-rose-900/50 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-rose-900/30 transition-colors duration-200",
                ),
                (
                    "Reprovado por Nota",
                    "inline-flex items-center gap-1.5 bg-rose-950/40 text-rose-400 border border-rose-900/50 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-rose-900/30 transition-colors duration-200",
                ),
                (
                    "Em andamento",
                    "inline-flex items-center gap-1.5 bg-blue-950/40 text-blue-400 border border-blue-900/50 text-xs font-semibold px-3 py-1 rounded-full w-fit transition-colors duration-200",
                ),
                "inline-flex items-center gap-1.5 bg-gray-800 text-gray-300 border border-gray-700 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-gray-750 transition-colors duration-200",
            ),
            rx.match(
                status,
                (
                    "Aprovado",
                    "inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-emerald-100/50 transition-colors duration-200",
                ),
                (
                    "Exame",
                    "inline-flex items-center gap-1.5 bg-amber-50 text-amber-700 border border-amber-100 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-amber-100/50 transition-colors duration-200",
                ),
                (
                    "Reprovado por Falta",
                    "inline-flex items-center gap-1.5 bg-rose-50 text-rose-700 border border-rose-100 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-rose-100/50 transition-colors duration-200",
                ),
                (
                    "Reprovado por Nota",
                    "inline-flex items-center gap-1.5 bg-rose-50 text-rose-700 border border-rose-100 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-rose-100/50 transition-colors duration-200",
                ),
                (
                    "Em andamento",
                    "inline-flex items-center gap-1.5 bg-blue-50 text-blue-600 border border-blue-100 text-xs font-semibold px-3 py-1 rounded-full w-fit transition-colors duration-200",
                ),
                "inline-flex items-center gap-1.5 bg-gray-50 text-gray-700 border border-gray-100 text-xs font-semibold px-3 py-1 rounded-full w-fit hover:bg-gray-100/50 transition-colors duration-200",
            ),
        ),
    )


def grade_chip(val: float) -> rx.Component:
    return rx.el.span(
        f"{val:.1f}",
        class_name=rx.cond(
            AcademicState.is_dark,
            rx.cond(
                val >= 7.0,
                "bg-blue-950/40 hover:bg-blue-900/40 text-blue-400 font-semibold px-2.5 py-1 rounded-lg text-xs md:text-sm border border-blue-900/50 transition-colors duration-150",
                "bg-gray-800/80 hover:bg-gray-800 text-gray-300 font-medium px-2.5 py-1 rounded-lg text-xs md:text-sm border border-gray-700 transition-colors duration-150",
            ),
            rx.cond(
                val >= 7.0,
                "bg-blue-50/80 hover:bg-blue-50 text-blue-700 font-semibold px-2.5 py-1 rounded-lg text-xs md:text-sm border border-blue-100 transition-colors duration-150",
                "bg-gray-50/80 hover:bg-gray-50 text-gray-600 font-medium px-2.5 py-1 rounded-lg text-xs md:text-sm border border-gray-100 transition-colors duration-150",
            ),
        ),
    )


def faltas_control(item: Disciplina) -> rx.Component:
    current_year = date.today().year
    limite = item["limite_faltas"].to(int)
    percent = (item["faltas"].to(float) / limite.to(float)) * 100
    restantes = limite - item["faltas"].to(int)
    msg = rx.cond(
        item["faltas"] >= limite,
        "Limite de faltas excedido",
        rx.cond(
            restantes == 1,
            "Você ainda pode faltar 1 aula",
            f"Você ainda pode faltar {restantes} aulas",
        ),
    )
    return rx.el.div(
        rx.el.div(
            rx.cond(
                item["faltas"] > item["faltas_originais"].to(int),
                # Botão visível quando há faltas manuais para remover
                rx.el.button(
                    rx.icon("minus", class_name="h-3.5 w-3.5"),
                    on_click=lambda: AcademicState.decrementar_falta(item["id"]),
                    type="button",
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "size-7 flex items-center justify-center rounded-lg border border-red-700/40 bg-red-700/40 text-red-300 hover:bg-red-900 hover:border-red-600 active:scale-90 transition-all duration-150 shadow-xs",
                        "size-7 flex items-center justify-center rounded-lg border border-red-200 bg-red-100/50 text-red-600 hover:bg-red-300/40 hover:border-red-300 active:scale-90 transition-all duration-150 shadow-xs",
                    ),
                ),
                # Placeholder invisível para manter o layout estável
                rx.el.div(class_name="size-7"),
            ),
            rx.el.div(
                rx.el.span(
                    item["faltas"].to(str),
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "font-extrabold text-gray-100 text-sm tabular-nums transition-all",
                        "font-extrabold text-gray-900 text-sm tabular-nums transition-all",
                    ),
                ),
                rx.cond(
                    ~AcademicState.ano_diferente,
                    rx.el.span(
                        "/" + item["limite_faltas"].to(str),
                        class_name="text-gray-400 text-xs font-semibold tabular-nums",
                    ),
                ),
                class_name="min-w-[44px] flex items-baseline justify-center gap-0.5",
            ),

            rx.cond(
                ~AcademicState.ano_diferente,
                # botão vísivel apenas quando o ano é igual
                rx.el.button(
                    rx.icon("plus", class_name="h-3.5 w-3.5"),
                    on_click=lambda: AcademicState.incrementar_falta(item["id"]),
                    disabled=(item["faltas"] >= item["limite_faltas"].to(int)),
                    type="button",
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "size-7 flex items-center justify-center rounded-lg border border-blue-900 bg-blue-950/40 text-blue-400 hover:bg-blue-900 hover:border-blue-800 active:scale-90 transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed shadow-xs",
                        "size-7 flex items-center justify-center rounded-lg border border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100 hover:border-blue-300 active:scale-90 transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed shadow-xs",
                    ),
                ),
            ),
            class_name="flex items-center gap-2.5",
        ),
        rx.cond(
            ~AcademicState.ano_diferente,
            rx.fragment(
                rx.el.div(
                    rx.el.div(
                        class_name=rx.cond(
                            item["faltas"] >= item["limite_faltas"].to(int),
                            "bg-rose-500 h-1.5 rounded-full transition-all duration-300 ease-out",
                            rx.cond(
                                item["faltas"] >= (item["limite_faltas"].to(float) * 0.75).to(int),
                                "bg-rose-400 h-1.5 rounded-full transition-all duration-300 ease-out",
                                rx.cond(
                                    item["faltas"] >= (item["limite_faltas"].to(float) * 0.5).to(int),
                                    "bg-amber-400 h-1.5 rounded-full transition-all duration-300 ease-out",
                                    "bg-emerald-500 h-1.5 rounded-full transition-all duration-300 ease-out",
                                ),
                            ),
                        ),
                        style={"width": f"{percent}%"},
                    ),
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "w-full bg-gray-800 rounded-full h-1.5 mt-2 overflow-hidden",
                        "w-full bg-gray-100 rounded-full h-1.5 mt-2 overflow-hidden",
                    ),
                ),
                rx.el.div(
                    rx.el.span(
                        msg,
                        class_name=rx.cond(
                            item["faltas"] >= item["limite_faltas"].to(int),
                            "text-[11px] font-bold text-rose-500",
                            rx.cond(
                                item["faltas"] >= (item["limite_faltas"].to(float) * 0.75).to(int),
                                "text-[11px] font-semibold text-rose-400",
                                rx.cond(
                                    item["faltas"] >= (item["limite_faltas"].to(float) * 0.5).to(int),
                                    "text-[11px] font-semibold text-amber-500",
                                    "text-[11px] font-semibold text-emerald-500",
                                ),
                            ),
                        ),
                    ),
                    rx.el.span(
                        f"{percent:.0f}%",
                        class_name="text-[11px] font-bold text-gray-400 tabular-nums",
                    ),
                    class_name="flex items-center justify-between mt-1.5",
                ),
            ),
        ),
        class_name="min-w-[190px]",
    )


def list_row(item: Disciplina) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    item["nome"],
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "font-semibold text-gray-100 text-sm md:text-base leading-tight group-hover:text-blue-400 transition-colors duration-150",
                        "font-semibold text-gray-900 text-sm md:text-base leading-tight group-hover:text-blue-600 transition-colors duration-150",
                    ),
                ),
                class_name="max-w-xs md:max-w-sm",
            ),
            class_name="px-6 py-5 align-middle",
        ),
        rx.el.td(
            faltas_control(item),
            class_name="px-6 py-5 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                grade_chip(item["nota1"]),
                grade_chip(item["nota2"]),
                grade_chip(item["nota3"]),
                class_name="flex items-center gap-1.5",
            ),
            class_name="px-6 py-5 align-middle",
        ),
        rx.el.td(
            rx.el.span(
                f"{item['media']:.2f}",
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "font-extrabold text-gray-100 text-sm md:text-base tabular-nums",
                    "font-extrabold text-gray-900 text-sm md:text-base tabular-nums",
                ),
            ),
            class_name="px-6 py-5 align-middle",
        ),
        rx.el.td(
            status_badge(item["status"]), class_name="px-6 py-5 align-middle"
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: AcademicState.remover_disciplina(item["id"]),
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "text-gray-500 hover:text-red-400 hover:bg-red-950/45 p-2.5 rounded-xl transition-all duration-200 active:scale-95",
                    "text-gray-400 hover:text-red-500 hover:bg-red-50 p-2.5 rounded-xl transition-all duration-200 active:scale-95",
                ),
            ),
            class_name="px-6 py-5 align-middle text-right",
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "border-b border-gray-800 hover:bg-gray-800/40 transition-colors duration-150 group",
            "border-b border-gray-100 hover:bg-gray-50/40 transition-colors duration-150 group",
        ),
    )


def discipline_list() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Desempenho Acadêmico",
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "text-xl font-bold text-gray-100 tracking-tight",
                                "text-xl font-bold text-gray-900 tracking-tight",
                            ),
                        ),
                        rx.cond(
                            AcademicState.ano_letivo != "",
                            rx.el.span(
                                "Ano: ",
                                AcademicState.ano_letivo,
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/50 text-blue-300 border border-blue-800/50",
                                    "px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-700 border border-blue-200"
                                )
                            ),
                            rx.el.div()
                        ),
                        class_name="flex items-center gap-3"
                    ),
                    rx.el.p(
                        "Visão geral de notas, faltas e situação atual do semestre",
                        class_name="text-xs md:text-sm text-gray-400 mt-1",
                    ),
                    class_name="mb-5 md:mb-0",
                ),
                rx.el.div(
                    # Search Input
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3.5 top-3.5 h-4 w-4 text-gray-400",
                        ),
                        rx.el.input(
                            type="text",
                            placeholder="Buscar disciplina...",
                            on_change=AcademicState.set_search_query.debounce(
                                500
                            ),
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "pl-10 pr-4 py-2.5 w-full md:w-64 bg-gray-800 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-100 placeholder-gray-500 transition-all",
                                "pl-10 pr-4 py-2.5 w-full md:w-64 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-900 placeholder-gray-400 transition-all",
                            ),
                        ),
                        class_name="relative w-full md:w-auto",
                    ),
                    # Status Filter Select
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Todos os Status", value="Todas"),
                            rx.el.option("Em andamento", value="Em andamento"),
                            rx.el.option("Aprovado", value="Aprovado"),
                            rx.el.option("Exame", value="Exame"),
                            rx.el.option("Reprovado", value="Reprovado"),
                            value=AcademicState.status_filter,
                            on_change=AcademicState.set_status_filter,
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "appearance-none w-full md:w-auto border rounded-xl px-4 py-2.5 pr-10 text-sm font-semibold cursor-pointer transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-gray-800 border-gray-700 text-gray-100",
                                "appearance-none w-full md:w-auto border rounded-xl px-4 py-2.5 pr-10 text-sm font-semibold cursor-pointer transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-gray-50 border-gray-200 text-gray-700",
                            ),
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3.5 top-3.5 h-4 w-4 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative w-full md:w-auto",
                    ),
                    # Add Grade Button
                    rx.el.button(
                        rx.icon("cloud_sync", class_name="h-4 w-4"),
                        "Sincronizar",
                        on_click=AcademicState.toggle_modal,
                        class_name="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 active:scale-98 text-white font-bold text-sm px-5 py-2.5 rounded-xl shadow-xs transition-all w-full md:w-auto",
                    ),
                    class_name="flex flex-col sm:flex-row items-center gap-3.5 w-full md:w-auto",
                ),
                class_name="flex flex-col md:flex-row md:items-center md:justify-between pb-6 border-b border-gray-100 gap-4",
            ),
            # Table Element inside responsive wrapper with styling polish
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Disciplina",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest bg-gray-850/40",
                                    "px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-widest bg-gray-50/40",
                                ),
                            ),
                            rx.el.th(
                                "Controle de Faltas",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest bg-gray-850/40",
                                    "px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-widest bg-gray-50/40",
                                ),
                            ),
                            rx.el.th(
                                "Notas (N1, N2, N3)",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest bg-gray-850/40",
                                    "px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-widest bg-gray-50/40",
                                ),
                            ),
                            rx.el.th(
                                "Média",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest bg-gray-850/40",
                                    "px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-widest bg-gray-50/40",
                                ),
                            ),
                            rx.el.th(
                                "Situação",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest bg-gray-850/40",
                                    "px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-widest bg-gray-50/40",
                                ),
                            ),
                            rx.el.th(
                                "",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-6 py-4 text-right bg-gray-850/40",
                                    "px-6 py-4 text-right bg-gray-50/40",
                                ),
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AcademicState.filtered_disciplinas, list_row
                        ),
                        class_name=rx.cond(
                            AcademicState.is_dark,
                            "divide-y divide-gray-800 bg-gray-900",
                            "divide-y divide-gray-100 bg-white",
                        ),
                    ),
                    class_name="min-w-full table-auto border-collapse",
                ),
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "overflow-x-auto rounded-xl border border-gray-800 mt-6",
                    "overflow-x-auto rounded-xl border border-gray-100 mt-6",
                ),
            ),
            class_name=rx.cond(
                AcademicState.is_dark,
                "bg-gray-900 p-6 sm:p-8 rounded-2xl border border-gray-800 shadow-xs",
                "bg-white p-6 sm:p-8 rounded-2xl border border-gray-200/80 shadow-xs",
            ),
        ),
        class_name="w-full mb-8",
    )