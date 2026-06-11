import reflex as rx
from app.states.academic_state import AcademicState
from app.states.admin_state import AdminState

def admin_page() -> rx.Component:
    return rx.el.div(
        # Sidebar/Navigation
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="h-5 w-5 text-gray-500 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"),
                    href="/dashboard",
                    title="Voltar ao Dashboard",
                    class_name="mb-6 block"
                ),
                rx.el.h1("Painel do Administrador", class_name="text-2xl font-bold text-gray-900 dark:text-white mb-2"),
                rx.el.p("Visão geral e métricas do sistema.", class_name="text-gray-500 dark:text-gray-400"),
                class_name="mb-8"
            ),
            
            # Dashboard Cards
            rx.el.div(
                # Card de Usuários
                rx.el.div(
                    rx.el.div(
                        rx.icon("users", class_name="h-6 w-6 text-blue-500"),
                        class_name="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-xl w-fit mb-4"
                    ),
                    rx.el.h3("Usuários Cadastrados", class_name="text-gray-500 dark:text-gray-400 text-sm font-medium"),
                    rx.el.p(
                        AcademicState.contar_usuarios_registrados, 
                        class_name="text-3xl font-bold text-gray-900 dark:text-white mt-1"
                    ),
                    class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800"
                ),
                
                # Card de Produção
                rx.el.div(
                    rx.el.div(
                        rx.icon("server", class_name="h-6 w-6 text-purple-500"),
                        class_name="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-xl w-fit mb-4"
                    ),
                    rx.el.h3("Ambiente", class_name="text-gray-500 dark:text-gray-400 text-sm font-medium"),
                    rx.el.p(
                        rx.cond(AdminState.is_production, "Produção", "Local (Dev)"), 
                        class_name="text-2xl font-bold text-gray-900 dark:text-white mt-1"
                    ),
                    class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800"
                ),

                # Card Banco de Dados
                rx.el.div(
                    rx.el.div(
                        rx.icon("database", class_name="h-6 w-6 text-emerald-500"),
                        class_name="p-3 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl w-fit mb-4"
                    ),
                    rx.el.h3("PostgreSQL / SQLite", class_name="text-gray-500 dark:text-gray-400 text-sm font-medium"),
                    rx.el.p(
                        AdminState.db_status, 
                        class_name=rx.cond(
                            AdminState.db_status == "Online",
                            "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1",
                            "text-2xl font-bold text-red-600 dark:text-red-400 mt-1"
                        )
                    ),
                    class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800"
                ),

                # Card SISAV
                rx.el.div(
                    rx.el.div(
                        rx.icon("globe", class_name="h-6 w-6 text-orange-500"),
                        rx.cond(
                            AdminState.is_checking_sisav,
                            rx.icon("loader-2", class_name="h-4 w-4 text-orange-500 animate-spin absolute -top-1 -right-1"),
                            rx.fragment()
                        ),
                        class_name="p-3 bg-orange-100 dark:bg-orange-900/30 rounded-xl w-fit mb-4 relative"
                    ),
                    rx.el.h3("Status SISAV (uem.br)", class_name="text-gray-500 dark:text-gray-400 text-sm font-medium"),
                    rx.el.p(
                        AdminState.sisav_status, 
                        class_name=rx.cond(
                            AdminState.sisav_status == "Online",
                            "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1",
                            rx.cond(
                                AdminState.sisav_status == "Testando...",
                                "text-2xl font-bold text-gray-500 dark:text-gray-400 mt-1",
                                "text-2xl font-bold text-red-600 dark:text-red-400 mt-1"
                            )
                        )
                    ),
                    class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800"
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            ),
            
            class_name="max-w-5xl mx-auto p-6 md:p-10"
        ),
        class_name=rx.cond(
            AcademicState.is_dark,
            "dark bg-gray-950 min-h-screen w-full font-['Inter']",
            "bg-gray-50 min-h-screen w-full font-['Inter']"
        )
    )
