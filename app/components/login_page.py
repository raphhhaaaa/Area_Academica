# dashboard_uem/login_page.py
import reflex as rx
from app.states.academic_state import AcademicState

def login() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Área Acadêmica UEM", size="6"),
                rx.text("Acesse com suas credenciais do portal SAV", color="gray"),
                
                # Input de Usuário
                rx.input(
                    placeholder="RA ou CPF",
                  #  on_change=AcademicState.set_username,
                   # value=AcademicState.username,
                    width="100%"
                ),
                
                # Input de Senha
                rx.input(
                    placeholder="Senha",
                    type="password",
                 #   on_change=AcademicState.set_password,
                  #  value=AcademicState.password,
                    width="100%"
                ),
                
                # Botão de Login
                rx.button(
                    rx.cond(
                        True,
                   #     AcademicState.is_loading,
                        rx.spinner(size="2"),
                        "Entrar"
                    ),
                 #   on_click=AcademicState.handle_login,
                  #  disabled=AcademicState.is_loading,
                    width="100%",
                    color_scheme="blue"
                ),
                spacing="4",
                width="350px",
            ),
            padding="6",
            border_radius="lg",
            box_shadow="lg"
        ),
        # O rx.center ocupa a tela toda
        height="100vh",
        background_color=rx.color("gray", 2)
    )