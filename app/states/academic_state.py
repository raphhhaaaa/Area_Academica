import reflex as rx
from typing import TypedDict
from app.states.extrator import rodar_extrator, CredenciaisInvalidasError, AnoLetivoInvalidoError
from app.states.config import salvar_credenciais
from datetime import date


class Disciplina(TypedDict):
    id: str
    nome: str
    faltas: int
    limite_faltas: int
    nota1: float
    nota2: float
    nota3: float
    media: float
    status: str  # "Aprovado", "Exame", "Reprovado por Falta", "Reprovado por Nota", "Em andamento"
    em_andamento: bool  # True quando o semestre ainda está em curso (Situação = Matriculado)
    faltas_originais: int  # Faltas vindas do SISAV — valor mínimo imutável
    status_original: str  # Status oficial do SISAV — nunca é alterado, usado para restaurar


class Aluno(TypedDict):
    ra: str
    nome: str
    curso: str
    turno: str
    campus: str
    serie: str
    sit_acad: str


LIMITE_FALTAS_PADRAO = 16


# Mapeamento dos status do SISAV para os nossos labels internos
_MAP_STATUS_SISAV = {
    "Aprovado":   "Aprovado",
    "Aprovada":   "Aprovado",
    "Rep. Nota":  "Reprovado por Nota",
    "Rep. Falta": "Reprovado por Falta",
    "Reprovado":  "Reprovado por Nota",
    "Exame":      "Exame",
    "Em Exame":   "Exame",
}


def _calc_status(media: float, faltas: int, limite: int = LIMITE_FALTAS_PADRAO) -> str:
    """Calcula o status parcial a partir das notas já disponíveis (semestre em andamento)."""
    if faltas >= limite:
        return "Reprovado por Falta"
    if media >= 7.0:
        return "Aprovado"
    if media >= 4.0:
        return "Exame"
    return "Reprovado por Nota"


def _resolver_status(situacao_sisav: str, media: float, faltas: int, limite: int) -> tuple[str, bool]:
    """
    Decide o status final da disciplina:
    - Se o SISAV ainda não encerrou a matéria (situação == Matriculado ou vazia), retorna "Em andamento".
    - Caso contrário, usa o status oficial do SISAV mapeado para nossos labels.
    Retorna (status_display, em_andamento).
    """
    situacao = situacao_sisav.strip() if situacao_sisav else ""

    if situacao == "" or situacao == "Matriculado":
        return "Em andamento", True

    # Usa o mapeamento; se não reconhecer, mantém o texto do SISAV
    status_mapeado = _MAP_STATUS_SISAV.get(situacao, situacao)
    return status_mapeado, False


def formatar_dados_sisav(dados_brutos: dict) -> tuple[list, dict]:
    """
    Formata os dados brutos vindos do extrator Playwright.
    Retorna uma tupla: (lista_de_disciplinas, dict_aluno)
    """

    # --- Disciplinas ---
    lista_formatada_disciplina: list[Disciplina] = []
    lista_bruta_disciplinas = dados_brutos.get("disciplinas", [])

    for dis in lista_bruta_disciplinas:
        lista_notas = dis.get('Notas', [])

        nota1 = lista_notas[0].get("Nota", 0.0) if len(lista_notas) > 0 else 0.0
        nota2 = lista_notas[1].get("Nota", 0.0) if len(lista_notas) > 1 else 0.0
        nota3 = lista_notas[2].get("Nota", 0.0) if len(lista_notas) > 2 else 0.0

        faltas = int(dis.get('Faltas', 0))
        limite = int(dis.get('LimiteFaltas', LIMITE_FALTAS_PADRAO))

        media = 0.0
        if len(lista_notas) > 0:
            soma = sum(nota['Nota'] for nota in lista_notas)
            media = soma / len(lista_notas)

        # Usa situação oficial do SISAV quando disponível
        situacao_sisav = str(dis.get('Situação', dis.get('Situacao', '')))
        status, em_andamento = _resolver_status(situacao_sisav, media, faltas, limite)

        disciplina_formatada: Disciplina = {
            "id": dis.get("Código", "S/N"),
            "nome": dis.get("Disciplina", "Desconhecida"),
            "faltas": faltas,
            "faltas_originais": faltas,
            "limite_faltas": limite,
            "nota1": float(nota1),
            "nota2": float(nota2),
            "nota3": float(nota3),
            "media": round(media, 1),
            "status": status,
            "status_original": status,  # espelho imutável do status inicial
            "em_andamento": em_andamento,
        }
        lista_formatada_disciplina.append(disciplina_formatada)

    # --- Aluno ---
    lista_bruta_aluno = dados_brutos.get("aluno", {})

    # O extrator retorna aluno como dict (não lista), tratar ambos os casos
    if isinstance(lista_bruta_aluno, list):
        alu = lista_bruta_aluno[0] if lista_bruta_aluno else {}
    else:
        alu = lista_bruta_aluno

    aluno_formatado: Aluno = {
        "ra": str(alu.get("RA", "")),
        "nome": alu.get("Nome", ""),
        "curso": alu.get("Curso", ""),
        "turno": alu.get("Turno", ""),
        "campus": alu.get("Campus/Polo", ""),
        "serie": str(alu.get("Série", "")),
        "sit_acad": str(alu.get("Sit. Acad.", ""))
    }

    return lista_formatada_disciplina, aluno_formatado


class AcademicState(rx.State):
    aluno: Aluno = {"ra": "", "nome": "", "curso": "", "turno": "", "campus": "", "serie": "", "sit_acad": ""}

    limite_faltas: int = LIMITE_FALTAS_PADRAO
    disciplinas: list[Disciplina] = []
    is_loading: bool = False
    ano_letivo: str = str(date.today().year)
    error_message: str = ""

    # Modal trigger state
    show_modal: bool = False

    # Form states (usados no login)
    form_usuario: str = ""
    form_senha: str = ""

    # Search and Filters
    search_query: str = ""
    status_filter: str = "Todas"  # "Todas", "Aprovado", "Exame", "Reprovado"

    # Theme state
    is_dark: bool = False

    @rx.var
    def get_nome_aluno(self) -> str:
        return self.aluno.get("nome", "")

    @rx.var
    def get_ra_aluno(self) -> str:
        ra = self.aluno.get("ra", "")
        return f"Matrícula: #{ra}" if ra else "Sem matrícula"

    @rx.var
    def tem_dados(self) -> bool:
        return len(self.disciplinas) > 0

    @rx.event
    def toggle_theme(self):
        self.is_dark = not self.is_dark

    @rx.var
    def total_faltas(self) -> int:
        return sum(d["faltas"] for d in self.disciplinas)

    @rx.var
    def media_geral(self) -> float:
        if not self.disciplinas:
            return 0.0
        return round(
            sum(d["media"] for d in self.disciplinas) / len(self.disciplinas), 2
        )

    @rx.var
    def total_disciplinas(self) -> int:
        return len(self.disciplinas)

    @rx.var
    def aprovadas_count(self) -> int:
        return len([d for d in self.disciplinas if d["status"] == "Aprovado"])

    @rx.var
    def filtered_disciplinas(self) -> list[Disciplina]:
        result = self.disciplinas
        if self.search_query:
            query = self.search_query.lower()
            result = [d for d in result if query in d["nome"].lower()]

        if self.status_filter != "Todas":
            if self.status_filter == "Reprovado":
                result = [d for d in result if "Reprovado" in d["status"]]
            else:
                result = [
                    d for d in result if d["status"] == self.status_filter
                ]

        return result

    @rx.event
    def set_search_query(self, val: str):
        self.search_query = val

    @rx.event
    def set_status_filter(self, val: str):
        self.status_filter = val

    @rx.event
    def toggle_modal(self):
        self.show_modal = not self.show_modal
        self.error_message = ""

    @rx.event
    async def handle_submit(self, form_data: dict):
        """Recebe credenciais do formulário, dispara o scraping e salva no .env se bem-sucedido."""
        usuario = form_data.get("nome", "").strip()
        senha = form_data.get("senha", "")
        ano = form_data.get("ano", "")

        if not usuario:
            self.error_message = "Por favor, preencha o campo de Usuário."
            return

        if not senha:
            self.error_message = "Por favor, preencha o campo de Senha."
            return

        self.error_message = ""
        self.is_loading = True
        yield  # Flush imediato: envia is_loading=True ao frontend antes do Playwright rodar

        try:
            self.ano_letivo = ano  # Atualiza o ano letivo selecionado
            dados_brutos = await rodar_extrator(
                usuario=usuario,
                senha=senha,
                ano_letivo=form_data.get("ano", "").strip() or None,
            )
            disciplinas, aluno = formatar_dados_sisav(dados_brutos)
            self.disciplinas = disciplinas
            self.aluno = aluno
            self.show_modal = False
            # Só salva credenciais no .env após login bem-sucedido
            try:
                salvar_credenciais(usuario, senha)
            except Exception as e:
                print(f"Aviso: não foi possível salvar credenciais no .env: {e}")

            yield rx.toast.success(
                f"Dados de {aluno.get('nome', 'Aluno')} sincronizados com sucesso!",
                duration=4000,
            )
        except CredenciaisInvalidasError as e:
            # Erro de credenciais: mantém o modal aberto com mensagem clara
            self.error_message = str(e)
        except AnoLetivoInvalidoError as e:
            # Ano não disponível: mantém modal aberto com mensagem clara
            self.error_message = str(e)
        except Exception as e:
            # Erro inesperado (rede, timeout, etc.)
            msg = str(e)
            if "Timeout" in msg or "timeout" in msg:
                self.error_message = "Tempo esgotado ao conectar ao SISAV. Verifique sua internet e tente novamente."
            else:
                self.error_message = f"Erro inesperado: {msg[:120]}"
            yield rx.toast.error(self.error_message, duration=5000)
        finally:
            self.is_loading = False

    @rx.event
    def remover_disciplina(self, disc_id: str):
        self.disciplinas = [d for d in self.disciplinas if d["id"] != disc_id]
        return rx.toast("Disciplina removida.", duration=2000)

    @rx.event
    def incrementar_falta(self, disc_id: str):
        for d in self.disciplinas:
            if d["id"] == disc_id:
                limite = d.get("limite_faltas", LIMITE_FALTAS_PADRAO)
                if d["faltas"] >= limite:
                    return rx.toast(
                        f"Limite de {limite} faltas já atingido.",
                        duration=2000,
                    )
                d["faltas"] = d["faltas"] + 1
                if d["faltas"] >= limite:
                    # Reprovado por falta tem prioridade absoluta
                    d["status"] = "Reprovado por Falta"
                elif d.get("em_andamento", True):
                    # Semestre em curso: recalcula parcialmente
                    d["status"] = _calc_status(d["media"], d["faltas"], limite)
                # Semestre encerrado + faltas < limite: mantém status_original do SISAV
                break

    @rx.event
    def decrementar_falta(self, disc_id: str):
        for d in self.disciplinas:
            if d["id"] == disc_id:
                minimo = d.get("faltas_originais", 0)
                if d["faltas"] <= minimo:
                    return
                d["faltas"] = d["faltas"] - 1
                limite = d.get("limite_faltas", LIMITE_FALTAS_PADRAO)
                if d["faltas"] >= limite:
                    d["status"] = "Reprovado por Falta"
                elif d.get("em_andamento", True):
                    # Semestre em curso: recalcula parcialmente
                    d["status"] = _calc_status(d["media"], d["faltas"], limite)
                else:
                    # Semestre encerrado: restaura status oficial do SISAV
                    d["status"] = d.get("status_original", d["status"])
                break