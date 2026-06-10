import reflex as rx
from app.states.academic_state import AcademicState

def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            # Box do login
            rx.el.div(
                rx.el.div(
                    # Cabeçalho
                    rx.el.div(
                        rx.el.div(
                            rx.icon("graduation-cap", class_name="h-10 w-10 text-blue-600 dark:text-blue-500"),
                            class_name="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-2xl flex items-center justify-center mb-6 shadow-sm mx-auto"
                        ),
                        rx.el.h2("Área Acadêmica - UEM", class_name="text-2xl font-bold text-gray-900 dark:text-white text-center"),
                        rx.el.p("Acesse e controle sua vida acadêmica.", class_name="text-gray-500 dark:text-gray-400 text-sm text-center mt-2"),
                        class_name="mb-8"
                    ),
                    
                    # Formulário
                    rx.el.form(
                        # Usuário / RA
                        rx.el.div(
                            rx.el.label("RA", class_name="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"),
                            rx.el.div(
                                rx.icon("user", class_name="absolute left-3.5 top-3 h-4 w-4 text-gray-400 pointer-events-none"),
                                rx.el.input(
                                    type="text",
                                    name="usuario",
                                    placeholder="Ex: ra123456",
                                    auto_complete="username",
                                    disabled=AcademicState.is_loading,
                                    class_name="pl-10 w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 transition-all disabled:opacity-50"
                                ),
                                class_name="relative"
                            ),
                            class_name="mb-4"
                        ),
                        
                        # Senha
                        rx.el.div(
                            rx.el.label("Senha", class_name="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"),
                            rx.el.div(
                                rx.icon("lock", class_name="absolute left-3.5 top-3 h-4 w-4 text-gray-400 pointer-events-none"),
                                rx.el.input(
                                    type=rx.cond(AcademicState.show_password, "text", "password"),
                                    name="senha",
                                    placeholder="Senha (mesma do SISAV)",
                                    auto_complete="current-password",
                                    disabled=AcademicState.is_loading,
                                    class_name="pl-10 pr-10 w-full px-4 py-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 transition-all disabled:opacity-50"
                                ),
                                rx.el.button(
                                    rx.icon(
                                        rx.cond(AcademicState.show_password, "eye-off", "eye"),
                                        class_name="h-4 w-4 text-gray-400"
                                    ),
                                    type="button",
                                    on_click=AcademicState.toggle_show_password,
                                    class_name="absolute right-3.5 top-3.5 hover:opacity-70 transition-opacity"
                                ),
                                class_name="relative"
                            ),
                            class_name="mb-6"
                        ),
                        
                        # Mensagem de erro
                        rx.cond(
                            AcademicState.error_message != "",
                            rx.el.div(
                                rx.icon("circle-alert", class_name="h-4 w-4 text-red-500 shrink-0 mt-0.5"),
                                rx.el.span(AcademicState.error_message, class_name="text-sm text-red-600 dark:text-red-400 leading-snug"),
                                class_name="flex items-start gap-2 p-3.5 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-900/50 mb-6"
                            ),
                            rx.el.div()
                        ),

                        # Loading
                        rx.cond(
                            AcademicState.is_loading,
                            rx.el.div(
                                rx.el.div(class_name="h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin shrink-0"),
                                rx.el.div(
                                    rx.el.p("Conectando...", class_name="text-sm font-semibold text-gray-800 dark:text-gray-200"),
                                    rx.el.p("Isso pode levar alguns segundos.", class_name="text-xs text-gray-500 dark:text-gray-400 mt-0.5"),
                                    class_name="flex flex-col"
                                ),
                                class_name="flex items-center gap-3 p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-900/50 mb-6"
                            ),
                            rx.el.div()
                        ),

                        # Botão
                        rx.el.button(
                            rx.cond(
                                AcademicState.is_loading,
                                "Aguarde...",
                                "Entrar na Área Acadêmica"
                            ),
                            type="submit",
                            disabled=AcademicState.is_loading,
                            class_name="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-sm transition-all disabled:opacity-70 disabled:cursor-not-allowed"
                        ),
                        on_submit=AcademicState.handle_login,
                        reset_on_submit=False
                    ),
                    class_name="bg-white dark:bg-gray-900 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-800 w-full max-w-md relative z-10"
                ),
                class_name="flex-1 flex flex-col justify-center items-center p-4"
            ),
            rx.el.div(
                rx.icon("shield-check", class_name="h-4 w-4 text-emerald-500"),
                rx.el.span(" dev <", class_name="text-sm text-gray-400"),
                class_name="flex items-center justify-center gap-2 pb-8"
            ),
            class_name="min-h-screen flex flex-col justify-between"
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "dark bg-gray-950 min-h-screen w-full font-['Inter']",
            "bg-gray-800 min-h-screen w-full font-['Inter']"
        )
    )
