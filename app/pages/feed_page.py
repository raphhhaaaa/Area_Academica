import reflex as rx
from app.pages.horarios_page import horarios_table
from app.states.academic_state import AcademicState
from app.components.header import header_section
from app.components.sidebar import sidebar

def feed_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="feed"),
        rx.el.main(
            rx.el.div(
                header_section(
                    title="Mural de Feed",
                    subtitle="Acompanhe as novidades e avisos.",
                ),
                rx.el.div(
                    rx.el.p("(EM CONSTRUÇÃO)", class_name="text-gray-500"),
                    class_name="mt-8"
                ),
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
