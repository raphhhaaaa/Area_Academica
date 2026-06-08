import reflex as rx
from app.states.academic_state import AcademicState


def add_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                # Header do modal
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "cloud_sync",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "h-5 w-5 text-blue-400",
                                    "h-5 w-5 text-blue-600",
                                ),
                            ),
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "p-2.5 rounded-xl bg-blue-950/40 border border-blue-900/50",
                                "p-2.5 rounded-xl bg-blue-50 border border-blue-100",
                            ),
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Sincronizar com SISAV",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "text-base font-bold text-gray-100",
                                    "text-base font-bold text-gray-900",
                                ),
                            ),
                            rx.el.p(
                                "Insira suas credenciais do portal acadêmico",
                                class_name="text-xs text-gray-400 mt-0.5",
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=AcademicState.toggle_modal,
                        disabled=AcademicState.is_loading,
                        class_name=rx.cond(
                            AcademicState.is_dark,
                            "text-gray-500 hover:text-gray-300 hover:bg-gray-800 p-2 rounded-lg transition-all disabled:opacity-30 disabled:cursor-not-allowed",
                            "text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-2 rounded-lg transition-all disabled:opacity-30 disabled:cursor-not-allowed",
                        ),
                    ),
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "flex justify-between items-start pb-5 border-b border-gray-800",
                        "flex justify-between items-start pb-5 border-b border-gray-100",
                    ),
                ),

                # Formulário
                rx.el.form(
                    rx.el.div(
                        # Campo Usuário
                        rx.el.div(
                            rx.el.label(
                                "Usuário (RA)",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "block text-sm font-semibold text-gray-300 mb-2",
                                    "block text-sm font-semibold text-gray-700 mb-2",
                                ),
                            ),
                            rx.el.div(
                                rx.icon(
                                    "user",
                                    class_name="absolute left-3.5 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                rx.el.input(
                                    type="text",
                                    name="nome",
                                    placeholder="Ex: ra147190",
                                    auto_complete="username",
                                    disabled=AcademicState.is_loading,
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "pl-10 w-full px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 text-sm text-gray-100 placeholder-gray-500 transition-all disabled:opacity-50",
                                        "pl-10 w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-900 placeholder-gray-400 transition-all disabled:opacity-50",
                                    ),
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-4",
                        ),

                        # Campo Senha
                        rx.el.div(
                            rx.el.label(
                                "Senha",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "block text-sm font-semibold text-gray-300 mb-2",
                                    "block text-sm font-semibold text-gray-700 mb-2",
                                ),
                            ),
                            rx.el.div(
                                rx.icon(
                                    "lock",
                                    class_name="absolute left-3.5 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                rx.el.input(
                                    type=rx.cond(AcademicState.show_password, "text", "password"),
                                    name="senha",
                                    placeholder="Sua senha do portal SISAV",
                                    auto_complete="current-password",
                                    disabled=AcademicState.is_loading,
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "pl-10 pr-10 w-full py-2.5 bg-gray-800 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 text-sm text-gray-100 placeholder-gray-500 transition-all disabled:opacity-50",
                                        "pl-10 pr-10 w-full py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-900 placeholder-gray-400 transition-all disabled:opacity-50",
                                    ),
                                ),
                                rx.el.button(
                                    rx.icon(
                                        rx.cond(AcademicState.show_password, "eye-off", "eye"),
                                        class_name="h-4 w-4 text-gray-400"
                                    ),
                                    type="button",
                                    on_click=AcademicState.toggle_show_password,
                                    class_name="absolute right-3.5 top-3.5 hover:opacity-70 transition-opacity",
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-4",
                        ),

                        # Campo Ano letivo (opcional)
                        rx.el.div(
                            rx.el.label(
                                "Ano Letivo (opcional)",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "block text-sm font-semibold text-gray-300 mb-2",
                                    "block text-sm font-semibold text-gray-700 mb-2",
                                ),
                            ),
                            rx.el.div(
                                rx.icon(
                                    "calendar",
                                    class_name="absolute left-3.5 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                rx.el.select(
                                    rx.el.option("Selecione o ano", value=""),
                                    rx.el.option("2026", value="2026"),
                                    rx.el.option("2025", value="2025"),
                                    rx.el.option("2024", value="2024"),
                                    rx.el.option("2023", value="2023"),
                                    rx.el.option("2022", value="2022"),
                                    rx.el.option("2021", value="2021"),
                                    rx.el.option("2020", value="2020"),
                                    rx.el.option("2019", value="2019"),
                                    rx.el.option("2018", value="2018"),
                                    name="ano",
                                    placeholder="Ano letivo (ex: 2023)",
                                    disabled=AcademicState.is_loading,
                                    class_name=rx.cond(
                                        AcademicState.is_dark,
                                        "pl-10 w-relative px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 text-sm text-gray-100 placeholder-gray-500 transition-all disabled:opacity-50",
                                        "pl-10 w-relative px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-900 placeholder-gray-400 transition-all disabled:opacity-50",
                                    ),
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-2",
                        ),

                        # Aviso de segurança
                        rx.el.p(
                            rx.icon("shield-check", class_name="h-3.5 w-3.5 inline mr-1 text-emerald-500"),
                            "Suas credenciais são salvas localmente e nunca enviadas para terceiros.",
                            class_name="text-[11px] text-gray-400 mb-5 leading-relaxed",
                        ),

                        # Mensagem de erro
                        rx.cond(
                            AcademicState.error_message != "",
                            rx.el.div(
                                rx.icon("circle-alert", class_name="h-4 w-4 text-red-400 shrink-0 mt-0.5"),
                                rx.el.span(
                                    AcademicState.error_message,
                                    class_name="text-sm text-red-400 leading-snug",
                                ),
                                class_name="flex items-start gap-2 p-3.5 rounded-xl bg-red-950/30 border border-red-900/50 mb-4",
                            ),
                            rx.el.div(),
                        ),

                        # Loading state — mensagem enquanto sincroniza
                        rx.cond(
                            AcademicState.is_loading,
                            rx.el.div(
                                rx.el.div(class_name="h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin shrink-0"),
                                rx.el.div(
                                    rx.el.p(
                                        "Extraindo dados...",
                                        class_name=rx.cond(
                                            AcademicState.is_dark,
                                            "text-sm font-semibold text-gray-200",
                                            "text-sm font-semibold text-gray-800",
                                        ),
                                    ),
                                    rx.el.p(
                                        "Isso pode levar alguns segundos. Não feche esta janela.",
                                        class_name="text-xs text-gray-400 mt-0.5",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "flex items-center gap-3 p-4 rounded-xl bg-blue-950/30 border border-blue-900/50 mb-4",
                                    "flex items-center gap-3 p-4 rounded-xl bg-blue-50 border border-blue-100 mb-4",
                                ),
                            ),
                            rx.el.div(),
                        ),

                        # Botões de ação
                        rx.el.div(
                            rx.el.button(
                                "Cancelar",
                                type="button",
                                on_click=AcademicState.toggle_modal,
                                disabled=AcademicState.is_loading,
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "px-5 py-2.5 rounded-xl border border-gray-700 text-sm font-semibold text-gray-300 hover:bg-gray-800 transition-colors disabled:opacity-30 disabled:cursor-not-allowed",
                                    "px-5 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-50 transition-colors disabled:opacity-30 disabled:cursor-not-allowed",
                                ),
                            ),
                            rx.el.button(
                                rx.cond(
                                    AcademicState.is_loading,
                                    rx.el.div(
                                        rx.el.div(class_name="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"),
                                        "Sincronizando...",
                                        class_name="flex items-center gap-2",
                                    ),
                                    rx.el.div(
                                        rx.icon("cloud_sync", class_name="h-4 w-4"),
                                        "Fazer login e sincronizar",
                                        class_name="flex items-center gap-2",
                                    ),
                                ),
                                type="submit",
                                disabled=AcademicState.is_loading,
                                class_name="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 active:scale-95 text-white text-sm font-semibold shadow-sm transition-all disabled:opacity-60 disabled:cursor-not-allowed disabled:scale-100",
                            ),
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "flex justify-end gap-3 pt-5 border-t border-gray-800",
                                "flex justify-end gap-3 pt-5 border-t border-gray-100",
                            ),
                        ),
                    ),
                    on_submit=AcademicState.handle_submit,
                    reset_on_submit=False,
                ),

                class_name=rx.cond(
                    AcademicState.is_dark,
                    "bg-gray-900 rounded-2xl border border-gray-800 p-6 w-full max-w-md shadow-2xl relative z-50",
                    "bg-white rounded-2xl border border-gray-200/80 p-6 w-full max-w-md shadow-2xl relative z-50",
                ),
            ),
            class_name="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-40",
        ),
        class_name=rx.cond(AcademicState.show_modal, "block", "hidden"),
    )