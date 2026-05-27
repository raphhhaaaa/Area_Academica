import reflex as rx
from app.states.academic_state import AcademicState


def add_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Adicionar Nova Disciplina",
                        class_name=rx.cond(
                            AcademicState.is_dark,
                            "text-lg font-bold text-gray-100",
                            "text-lg font-bold text-gray-900",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=AcademicState.toggle_modal,
                        class_name="text-gray-400 hover:text-gray-300 transition-colors",
                    ),
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "flex justify-between items-center pb-4 border-b border-gray-850",
                        "flex justify-between items-center pb-4 border-b border-gray-100",
                    ),
                ),
                rx.el.form(
                    rx.el.div(
                        # Name Input
                        rx.el.div(
                            rx.el.label(
                                "Nome da Disciplina",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "block text-sm font-semibold text-gray-300 mb-1.5",
                                    "block text-sm font-semibold text-gray-700 mb-1.5",
                                ),
                            ),
                            rx.el.input(
                                type="text",
                                name="nome",
                                placeholder="Ex: Cálculo III, Banco de Dados...",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "w-full px-4 py-2.5 bg-gray-800 border border-gray-750 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-100 placeholder-gray-500",
                                    "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-900",
                                ),
                            ),
                            class_name="mb-4",
                        ),
                        # Grid for Faltas & Notes
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Quantidade de Faltas",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "block text-sm font-semibold text-gray-300 mb-1.5",
                                        "block text-sm font-semibold text-gray-700 mb-1.5",
                                    ),
                                ),
                                rx.el.input(
                                    type="number",
                                    name="faltas",
                                    default_value="0",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "w-full px-4 py-2.5 bg-gray-800 border border-gray-750 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-100",
                                        "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-900",
                                    ),
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nota Avaliação 1",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "block text-sm font-semibold text-gray-300 mb-1.5",
                                        "block text-sm font-semibold text-gray-700 mb-1.5",
                                    ),
                                ),
                                rx.el.input(
                                    type="number",
                                    name="nota1",
                                    step="0.1",
                                    placeholder="0.0 a 10.0",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "w-full px-4 py-2.5 bg-gray-800 border border-gray-750 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-100 placeholder-gray-500",
                                        "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-900",
                                    ),
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nota Avaliação 2",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "block text-sm font-semibold text-gray-300 mb-1.5",
                                        "block text-sm font-semibold text-gray-700 mb-1.5",
                                    ),
                                ),
                                rx.el.input(
                                    type="number",
                                    name="nota2",
                                    step="0.1",
                                    placeholder="0.0 a 10.0",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "w-full px-4 py-2.5 bg-gray-800 border border-gray-750 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-100 placeholder-gray-500",
                                        "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-900",
                                    ),
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nota Avaliação 3",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "block text-sm font-semibold text-gray-300 mb-1.5",
                                        "block text-sm font-semibold text-gray-700 mb-1.5",
                                    ),
                                ),
                                rx.el.input(
                                    type="number",
                                    name="nota3",
                                    step="0.1",
                                    placeholder="0.0 a 10.0",
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "w-full px-4 py-2.5 bg-gray-800 border border-gray-750 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-100 placeholder-gray-500",
                                        "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-900",
                                    ),
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-4 mb-6",
                        ),
                        # Actions
                        rx.el.div(
                            rx.el.button(
                                "Cancelar",
                                type="button",
                                on_click=AcademicState.toggle_modal,
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-4 py-2.5 rounded-xl border border-gray-750 text-sm font-semibold text-gray-300 hover:bg-gray-800 transition-colors",
                                    "px-4 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-50 transition-colors",
                                ),
                            ),
                            rx.el.button(
                                "Salvar Disciplina",
                                type="submit",
                                class_name="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow-sm transition-colors",
                            ),
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "flex justify-end gap-3 pt-4 border-t border-gray-850",
                                "flex justify-end gap-3 pt-4 border-t border-gray-100",
                            ),
                        ),
                    ),
                    on_submit=AcademicState.handle_submit,
                    reset_on_submit=True,
                ),
                class_name=rx.cond(
                    AcademicState.is_dark,
                    "bg-gray-900 rounded-2xl border border-gray-800 p-6 w-full max-w-lg shadow-xl relative z-50 animate-fade-in",
                    "bg-white rounded-2xl border border-gray-100 p-6 w-full max-w-lg shadow-xl relative z-50 animate-fade-in",
                ),
            ),
            class_name="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4 z-40",
        ),
        class_name=rx.cond(AcademicState.show_modal, "block", "hidden"),
    )