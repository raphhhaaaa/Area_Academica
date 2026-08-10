import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header_section
from app.states.academic_state import AcademicState

# Dados fictícios para prototipação do Feed
POSTS = [
    {
        "id": 1,
        "author": "Ana Souza",
        "campus": "Campus Sede - Maringá",
        "course": "Ciência da Computação",
        "avatar": "Ana",
        "time": "Há 2 horas",
        "content": "Alguém sabe se a biblioteca do bloco C40 está abrindo aos sábados agora no período de provas? Precisava devolver um livro urgente!",
        "image": "",
        "likes": 12,
        "comments": [
            {"author": "Carlos", "text": "Sim, está abrindo das 08h às 12h!"},
            {"author": "Mariana", "text": "Putz, acho que só o bloco central funciona de fds."}
        ]
    },
    {
        "id": 2,
        "author": "Lucas Oliveira",
        "campus": "Campus Regional de Cianorte",
        "course": "Design",
        "avatar": "Lucas",
        "time": "Há 5 horas",
        "content": "Oportunidade de estágio na agência XYZ! Eles estão procurando alguém com noções de UI/UX. Interessados, me mandem DM que eu passo o email de contato do RH. Boa sorte galera! 🎨✨",
        "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&q=80&w=1000",
        "likes": 45,
        "comments": [
            {"author": "Rafael", "text": "Te mandei mensagem!"}
        ]
    },
    {
        "id": 3,
        "author": "Centro Acadêmico",
        "campus": "UEM Geral",
        "course": "Avisos Oficiais",
        "avatar": "CA",
        "time": "Ontem às 14:30",
        "content": "⚠️ ATENÇÃO CALOUROS ⚠️\n\nA recepção oficial dos calouros será na próxima segunda-feira no auditório principal. Teremos palestras, sorteios e a tradicional apresentação da bateria! Não percam.",
        "image": "",
        "likes": 128,
        "comments": []
    }
]

def post_card(post: dict) -> rx.Component:
    return rx.el.article(
        # Cabeçalho do Post
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={post['avatar']}",
                class_name="w-11 h-11 sm:w-12 sm:h-12 rounded-full border border-gray-200 shrink-0"
            ),
            rx.el.div(
                rx.el.h3(post["author"], class_name=rx.cond(AcademicState.is_dark, "font-bold text-gray-100 text-sm sm:text-base leading-tight", "font-bold text-gray-900 text-sm sm:text-base leading-tight")),
                rx.el.p(f"{post['campus']} • {post['course']}", class_name=rx.cond(AcademicState.is_dark, "text-[11px] sm:text-xs text-gray-400 mt-0.5 line-clamp-1", "text-[11px] sm:text-xs text-gray-500 mt-0.5 line-clamp-1")),
                rx.el.p(post["time"], class_name=rx.cond(AcademicState.is_dark, "text-[10px] text-gray-500 mt-0.5", "text-[10px] text-gray-400 mt-0.5")),
                class_name="flex flex-col flex-1"
            ),
            rx.el.button(
                rx.icon("more-horizontal", class_name="w-5 h-5 text-gray-400 hover:text-gray-600"),
                class_name="p-2 -mr-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            ),
            class_name="flex items-start gap-3 mb-4"
        ),
        
        # Conteúdo em Texto
        rx.el.div(
            rx.el.p(post["content"], class_name=rx.cond(AcademicState.is_dark, "text-gray-300 text-sm sm:text-base whitespace-pre-wrap leading-relaxed", "text-gray-800 text-sm sm:text-base whitespace-pre-wrap leading-relaxed")),
            class_name="mb-4"
        ),
        
        # Imagem Opcional
        rx.el.div(
            rx.el.img(src=post["image"], class_name="w-full h-auto object-cover max-h-[500px]"),
            class_name="w-full rounded-xl mb-4 overflow-hidden border border-gray-100 dark:border-gray-800"
        ) if post["image"] != "" else rx.fragment(),
        
        # Barra de Interações (Curtir, Comentar)
        rx.el.div(
            rx.el.button(
                rx.icon("heart", class_name="w-5 h-5"),
                rx.el.span(f"{post['likes']}", class_name="font-medium text-sm"),
                class_name=rx.cond(AcademicState.is_dark, "flex items-center gap-1.5 text-gray-400 hover:text-red-400 transition-colors py-2 pr-4", "flex items-center gap-1.5 text-gray-500 hover:text-red-500 transition-colors py-2 pr-4")
            ),
            
            # Accordion Nativo HTML para os comentários
            rx.el.details(
                rx.el.summary(
                    rx.icon("message-square", class_name="w-5 h-5"),
                    rx.el.span("Comentar", class_name="font-medium text-sm hidden sm:inline"),
                    rx.el.span(f"{len(post['comments'])}", class_name="font-medium text-sm sm:hidden"),
                    class_name=rx.cond(AcademicState.is_dark, "flex items-center gap-1.5 text-gray-400 hover:text-blue-400 transition-colors cursor-pointer list-none py-2 px-4 [&::-webkit-details-marker]:hidden", "flex items-center gap-1.5 text-gray-500 hover:text-blue-500 transition-colors cursor-pointer list-none py-2 px-4 [&::-webkit-details-marker]:hidden")
                ),
                
                # Lista de Comentários
                rx.el.div(
                    (
                        rx.el.div(
                            *[
                                rx.el.div(
                                    rx.el.span(comment["author"], class_name=rx.cond(AcademicState.is_dark, "font-semibold text-gray-200 text-sm block mb-0.5", "font-semibold text-gray-800 text-sm block mb-0.5")),
                                    rx.el.p(comment["text"], class_name=rx.cond(AcademicState.is_dark, "text-gray-300 text-sm", "text-gray-700 text-sm")),
                                    class_name=rx.cond(AcademicState.is_dark, "bg-gray-800/60 p-3 rounded-2xl rounded-tl-none mt-3", "bg-gray-100/80 p-3 rounded-2xl rounded-tl-none mt-3")
                                )
                                for comment in post["comments"]
                            ]
                        )
                    ) if len(post["comments"]) > 0 else (
                        rx.el.p("Nenhum comentário ainda. Seja o primeiro!", class_name="text-sm text-gray-400 italic text-center py-4")
                    ),
                    
                    # Fake Input de Novo Comentário
                    rx.el.div(
                        rx.el.img(
                            src="https://api.dicebear.com/9.x/initials/svg?seed=Eu",
                            class_name="w-8 h-8 rounded-full shrink-0"
                        ),
                        rx.el.input(
                            placeholder="Escreva um comentário...",
                            class_name=rx.cond(AcademicState.is_dark, "w-full bg-gray-900 border border-gray-700 rounded-full px-4 py-2 text-sm text-gray-200 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all", "w-full bg-white border border-gray-200 rounded-full px-4 py-2 text-sm text-gray-800 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all")
                        ),
                        class_name="flex items-center gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-gray-800"
                    ),
                    class_name="pt-2 animate-in fade-in duration-200"
                ),
                class_name="group"
            ),
            
            rx.el.button(
                rx.icon("share-2", class_name="w-5 h-5"),
                class_name=rx.cond(AcademicState.is_dark, "flex items-center text-gray-400 hover:text-gray-200 transition-colors py-2 pl-4 ml-auto", "flex items-center text-gray-500 hover:text-gray-800 transition-colors py-2 pl-4 ml-auto")
            ),
            
            class_name="flex items-center border-t border-gray-100 dark:border-gray-800 pt-2 mt-2"
        ),
        
        class_name=rx.cond(
            AcademicState.is_dark,
            "bg-gray-900 rounded-3xl p-5 sm:p-6 mb-6 shadow-sm border border-gray-800",
            "bg-white rounded-3xl p-5 sm:p-6 mb-6 shadow-sm border border-gray-100"
        )
    )

def feed_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="feed"),
        rx.el.main(
            rx.el.div(
                header_section(
                    title="Mural Universitário", 
                    subtitle="Troque ideias, tire dúvidas e acompanhe as novidades da comunidade."
                ),
                
                # Container centralizado para o Feed (estilo Facebook/Instagram)
                rx.el.div(
                    
                    # Caixa de "Criar Publicação"
                    rx.el.div(
                        rx.el.div(
                            rx.el.img(
                                src="https://api.dicebear.com/9.x/initials/svg?seed=Aluno",
                                class_name="w-10 h-10 rounded-full border border-gray-200 dark:border-gray-700"
                            ),
                            rx.el.input(
                                placeholder="No que você está pensando, Estudante?",
                                class_name=rx.cond(
                                    AcademicState.is_dark,
                                    "flex-1 bg-gray-800 border border-transparent rounded-full px-5 py-3 text-gray-200 hover:bg-gray-700/50 focus:bg-gray-900 focus:border-blue-500 transition-all outline-none",
                                    "flex-1 bg-gray-100 border border-transparent rounded-full px-5 py-3 text-gray-800 hover:bg-gray-200/50 focus:bg-white focus:border-blue-500 transition-all outline-none"
                                )
                            ),
                            class_name="flex items-center gap-3 mb-4"
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("image", class_name="w-5 h-5 text-green-500"),
                                rx.el.span("Foto/Vídeo", class_name=rx.cond(AcademicState.is_dark, "text-sm font-medium text-gray-400", "text-sm font-medium text-gray-600")),
                                class_name="flex items-center gap-2 hover:bg-gray-50 dark:hover:bg-gray-800 px-3 py-2 rounded-xl transition-colors"
                            ),
                            rx.el.button(
                                rx.icon("paperclip", class_name="w-5 h-5 text-blue-500"),
                                rx.el.span("Anexo", class_name=rx.cond(AcademicState.is_dark, "text-sm font-medium text-gray-400 hidden sm:inline", "text-sm font-medium text-gray-600 hidden sm:inline")),
                                class_name="flex items-center gap-2 hover:bg-gray-50 dark:hover:bg-gray-800 px-3 py-2 rounded-xl transition-colors"
                            ),
                            rx.el.button(
                                "Publicar",
                                on_click=print("Publicação Criada! (Funcionalidade Futura)"),
                                class_name="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full text-sm font-bold transition-all shadow-md hover:shadow-lg ml-auto active:scale-95"
                            ),
                            class_name="flex items-center border-t border-gray-100 dark:border-gray-800 pt-3"
                        ),
                        class_name=rx.cond(
                            AcademicState.is_dark,
                            "bg-gray-900 rounded-3xl p-5 mb-8 shadow-sm border border-gray-800",
                            "bg-white rounded-3xl p-5 mb-8 shadow-sm border border-gray-100"
                        )
                    ),
                    
                    # Lista de Posts
                    rx.el.div(
                        *[post_card(post) for post in POSTS],
                        class_name="flex flex-col"
                    ),
                    
                    class_name="max-w-2xl mx-auto w-full"
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
