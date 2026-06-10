import reflex as rx
from app.states.academic_state import AcademicState

def sidebar_item(icon: str, text: str, href: str, is_active: bool = False) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon, 
            class_name=rx.cond(
                is_active,
                rx.cond(
                    AcademicState.is_dark,
                    "h-5 w-5 text-blue-400 shrink-0",
                    "h-5 w-5 text-blue-600 shrink-0"
                ),
                rx.cond(
                    AcademicState.is_dark,
                    "h-5 w-5 text-gray-400 group-hover:text-gray-200 transition-colors shrink-0",
                    "h-5 w-5 text-gray-500 group-hover:text-gray-900 transition-colors shrink-0"
                )
            )
        ),
        rx.cond(
            AcademicState.is_sidebar_open,
            rx.el.span(
                text,
                class_name=rx.cond(
                    is_active,
                    rx.cond(
                        AcademicState.is_dark,
                        "font-semibold text-blue-300 whitespace-nowrap",
                        "font-semibold text-blue-700 whitespace-nowrap"
                    ),
                    rx.cond(
                        AcademicState.is_dark,
                        "font-medium text-gray-300 group-hover:text-gray-100 transition-colors whitespace-nowrap",
                        "font-medium text-gray-700 group-hover:text-gray-900 transition-colors whitespace-nowrap"
                    )
                )
            ),
            rx.fragment()
        ),
        href=href,
        title=rx.cond(~AcademicState.is_sidebar_open, text, ""),
        class_name=rx.cond(
            is_active,
            rx.cond(
                AcademicState.is_dark,
                "flex items-center gap-3 px-3 py-2.5 rounded-xl bg-blue-900/20 border border-blue-800/30 transition-all cursor-pointer",
                "flex items-center gap-3 px-3 py-2.5 rounded-xl bg-blue-50 border border-blue-100 transition-all cursor-pointer"
            ),
            rx.cond(
                AcademicState.is_dark,
                "flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-800 border border-transparent transition-all group cursor-pointer",
                "flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-100 border border-transparent transition-all group cursor-pointer"
            )
        )
    )

def sidebar(current_page: str = "dashboard") -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            # Header com Logo e Botão de Recolher
            rx.el.div(
                rx.cond(
                    AcademicState.is_sidebar_open,
                    rx.el.div(
                        rx.icon("graduation-cap", class_name=rx.cond(
                            AcademicState.is_dark,
                            "h-6 w-6 text-blue-400 shrink-0",
                            "h-6 w-6 text-blue-600 shrink-0"
                        )),
                        rx.el.span(
                            "Área Acadêmica", 
                            class_name=rx.cond(
                                AcademicState.is_dark,
                                "font-bold text-lg text-gray-100 whitespace-nowrap tracking-tight",
                                "font-bold text-lg text-gray-900 whitespace-nowrap tracking-tight"
                            )
                        ),
                        class_name="flex items-center gap-2 overflow-hidden px-1"
                    ),
                    rx.el.div(
                        rx.icon("graduation-cap", class_name=rx.cond(
                            AcademicState.is_dark,
                            "h-6 w-6 text-blue-400 shrink-0",
                            "h-6 w-6 text-blue-600 shrink-0"
                        )),
                        class_name="flex items-center justify-center w-full"
                    )
                ),
                rx.el.button(
                    rx.icon(
                        rx.cond(AcademicState.is_sidebar_open, "chevron-left", "chevron-right"),
                        class_name=rx.cond(
                            AcademicState.is_dark,
                            "h-3.5 w-3.5 text-gray-400",
                            "h-3.5 w-3.5 text-gray-500"
                        )
                    ),
                    on_click=AcademicState.toggle_sidebar,
                    class_name=rx.cond(
                        AcademicState.is_dark,
                        "p-1 rounded-full hover:bg-gray-800 transition-colors absolute -right-3 top-5 bg-gray-950 border border-gray-800 hidden md:flex items-center justify-center z-10 shadow-sm",
                        "p-1 rounded-full hover:bg-gray-100 transition-colors absolute -right-3 top-5 bg-white border border-gray-200 hidden md:flex items-center justify-center z-10 shadow-sm"
                    )
                ),
                class_name="flex items-center justify-between p-4 relative min-h-[72px]"
            ),
            
            # Navegação
            rx.el.nav(
                sidebar_item("layout-dashboard", "Dashboard", "/", is_active=(current_page == "dashboard")),
                sidebar_item("calendar", "Horário de Aulas", "/horarios", is_active=(current_page == "horarios")),
                class_name="flex flex-col gap-1.5 px-3 mt-4"
            ),
            
            class_name=rx.cond(
                AcademicState.is_dark,
                "flex flex-col h-full bg-gray-950 border-r border-gray-800 transition-all duration-300",
                "flex flex-col h-full bg-white border-r border-gray-200 transition-all duration-300"
            )
        ),
        class_name=rx.cond(
            AcademicState.is_sidebar_open,
            "w-64 shrink-0 h-screen sticky top-0 transition-all duration-300 z-40 hidden md:block",
            "w-20 shrink-0 h-screen sticky top-0 transition-all duration-300 z-40 hidden md:block"
        )
    )
