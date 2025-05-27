from urllib.parse import urlparse, parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from loguru import logger

from app.services.browser import BrowserService
from app.services.telegram import TelegramService
from app.core.config import settings
from app.utils.log_manage import LogManager


class AutomacaoLinkedin:
    def __init__(self):
        self.CONFIGURACAO = settings
        self.browser_service = BrowserService()
        self.telegram_service = TelegramService()

    def run(self, modo_oculto: bool = True):
        """
        Fluxo da automação do Linkedin
        """
        try:
            # Abrir browser e acessar o link
            self.browser_service.iniciar_webdrive(
                self.CONFIGURACAO.LINKEDIN["link"], modo_oculto
            )
            self.__autenticacao()
            self.__acessar_aba_vagas()

            for job in self.CONFIGURACAO.JOBS_LINKEDIN_VAGAS:
                # Log
                logManager = LogManager("AutomacaoLinkedin::run")
                logManager.add_row(f"Tema: {job['tema']}")
                logManager.add_row(f"Filtros: {job['filtros']}")

                self.__aplicar_filtro(**job["filtros"])

                for busca in job["buscas"]:
                    self.__buscar_vagas(busca)
                    possui_vagas = self.__verificar_resultado_filtro()

                    lista_vagas_filtrada = []

                    if possui_vagas:
                        lista_vagas = self.__coletar_vagas()
                        lista_vagas_filtrada = self.__organizar_vagas_coletadas(
                            lista_vagas
                        )
                        self.__enviar_vagas_telegram(
                            lista_vagas_filtrada, job["telegram_chatid"]
                        )

                    logManager.add_row(f"Busca: {busca}")
                    logManager.add_row(
                        f"Quantidade de vagas: {len(lista_vagas_filtrada)}"
                    )

                logManager.print_log()

            self.browser_service.close_browser()

        except Exception:
            logger.exception("Erro na execução do job")

    def __autenticacao(self):
        """
        Realizar a autenticação
        """
        try:
            # Abrir formuário de login
            self.browser_service.interagir_elemento(
                "sign-in-form__sign-in-cta", By.CLASS_NAME, clicar=True
            )

            # Input Email
            self.browser_service.interagir_elemento(
                "username", By.ID, self.CONFIGURACAO.LINKEDIN["email"]
            )

            # Input Senha
            self.browser_service.interagir_elemento(
                "password", By.ID, self.CONFIGURACAO.LINKEDIN["senha"]
            )

            # Botão login
            self.browser_service.interagir_elemento(
                "login__form_action_container", By.CLASS_NAME, clicar=True
            )

        except Exception:
            logger.exception("Erro na autenticação do linkedin")

    def __acessar_aba_vagas(self):
        """
        Acessar a aba de vagas
        """
        try:
            self.browser_service.acessar_link(settings.LINKEDIN["link_job_search"])

        except Exception:
            logger.exception("Erro em acessar a aba de vagas")

    def __buscar_vagas(self, texto_busca: str):
        """
        Realizar a busca pelas vagas
        """
        try:
            # Input Busca Vagas - Texto
            self.browser_service.interagir_elemento(
                "jobs-search-box__keyboard-text-input",
                By.CLASS_NAME,
                f"{texto_busca} {Keys.ENTER}",
            )

        except Exception:
            logger.exception(f"Erro ao buscar vagas, texo de busca: '{texto_busca}'")

    def __aplicar_filtro(
        self,
        ordem_mais_recente: bool = True,
        ultimos_24_horas: bool = True,
        candidatura_simplificada: bool = True,
        ate_10_candidaturas: bool = True,
        remoto: bool = True,
    ):
        """
        Adicionar filtro na busca das vagas
        """
        try:
            # Botão para redefinir os filtros
            self.browser_service.interagir_elemento(
                """/html/body/div[6]/div[3]/div[4]/section/div/section/div/div/div/div/button""",
                By.XPATH,
                clicar=True,
            )

            # Botão Todos os Filtros
            self.browser_service.interagir_elemento(
                """//*[@id="search-reusables__filters-bar"]/div/div""",
                By.XPATH,
                clicar=True,
            )

            if ordem_mais_recente:
                # Botão Ordenação por Mais Recentes
                self.browser_service.interagir_elemento(
                    "search-reusables__value-label", By.CLASS_NAME, clicar=True
                )

            if ultimos_24_horas:
                # Botão Data de Anuncio Ultimo 24 horas
                self.browser_service.interagir_elemento(
                    """/html/body/div[4]/div/div/div[2]/ul/li[3]/fieldset/div/ul/li[4]/label""",
                    By.XPATH,
                    clicar=True,
                )

            if candidatura_simplificada:
                # Botão Candidatura simplificada
                self.browser_service.interagir_elemento(
                    """/html/body/div[4]/div/div/div[2]/ul/li[8]/fieldset/div""",
                    By.XPATH,
                    clicar=True,
                )

            if ate_10_candidaturas:
                # Botão Menos de 10 candidaturas
                self.browser_service.interagir_elemento(
                    """/html/body/div[4]/div/div/div[2]/ul/li[14]/fieldset/div""",
                    By.XPATH,
                    clicar=True,
                )

            if remoto:
                # Vagas remotas
                self.browser_service.interagir_elemento(
                    """/html/body/div[4]/div/div/div[2]/ul/li[7]/fieldset/div/ul/li[3]/label/p/span[1]""",
                    By.XPATH,
                    clicar=True,
                )

            # Botão Submit filtro
            self.browser_service.interagir_elemento(
                """/html/body/div[4]/div/div/div[3]/div/button[2]/span""",
                By.XPATH,
                clicar=True,
            )

        except Exception:
            logger.exception("Erro ao aplicar filtro")

    def __verificar_resultado_filtro(self) -> bool:
        """
        Verificar se o filtro aplicado, possui alguma vaga
        """
        try:
            # Informativo de que não encontrou nenhuma vaga
            nao_possui_vagas = self.browser_service.interagir_elemento(
                """/html/body/div[6]/div[3]/div[4]/div/div[1]/div/p""",
                By.XPATH,
            )

            if nao_possui_vagas:
                return False  # Não possui vagas

            return True  # Possui vagas

        except Exception:
            logger.exception("Erro em verificar resultado do filtro")

    def __coletar_vagas(self):
        """
        Pecorre cada vaga(li) da ul
        """
        try:
            contador = 0
            lista_vagas = []

            while True:
                try:
                    vaga = {}

                    # Vagas
                    ul_vagas = self.browser_service.interagir_elemento(
                        "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul",
                        By.XPATH,
                    )

                    # Pecorrer cada vaga
                    li_vagas = ul_vagas.find_elements(By.TAG_NAME, "li")

                    quantidade_vagas = len(li_vagas)

                    # Sair do loop
                    if contador >= quantidade_vagas - 1:
                        break

                    if li_vagas[contador].is_displayed():
                        # Clicar na vaga da lista
                        li_vagas[contador].click()

                        # Pegar nome da empresa
                        nome_empresa = self.browser_service.interagir_elemento(
                            "job-details-jobs-unified-top-card__company-name",
                            By.CLASS_NAME,
                        )
                        vaga["empresa"] = nome_empresa.text

                        # Pegar titulo da vaga
                        titulo_vaga = self.browser_service.interagir_elemento(
                            "job-details-jobs-unified-top-card__job-title",
                            By.CLASS_NAME,
                        )
                        vaga["titulo"] = titulo_vaga.text

                        # Pegar Localidade, Data postagem
                        # e quantidade de candidaturas
                        detalhes_vaga = self.browser_service.interagir_elemento(
                            """job-details-jobs-unified-top-card__primary-description-container""",
                            By.CLASS_NAME,
                        )
                        vaga["detalhes"] = detalhes_vaga.text

                        # Pegar Tipo da Vaga
                        tipo_vaga_textos = self.browser_service.interagir_elemento(
                            "job-details-jobs-unified-top-card__job-insight--highlight",
                            By.CLASS_NAME,
                        )
                        tipo_vaga_textos = tipo_vaga_textos.text.split("\n")
                        vaga["tipo"] = f"{tipo_vaga_textos[0]} - {tipo_vaga_textos[2]}"

                        # Pegar URL da vaga
                        vaga["url"] = self.__pegar_url_vaga(
                            self.browser_service.get_url_atual()
                        )

                        # Pegar logo da empresa
                        logo_empresa = self.browser_service.interagir_elemento(
                            """//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/a/div/div""",
                            By.XPATH,
                        )
                        logo_empresa_img = logo_empresa.find_elements(
                            By.TAG_NAME, "img"
                        )
                        if len(logo_empresa_img) != 0:
                            link_logo_empresa_img = logo_empresa_img[0].get_attribute(
                                "src"
                            )
                        else:
                            link_logo_empresa_img = None

                        vaga["logo_empresa"] = link_logo_empresa_img

                        lista_vagas.append(vaga)

                    contador += 1
                except Exception:
                    contador += 1

            return lista_vagas

        except Exception:
            logger.exception("Erro ao coletar as vagas")

    def __organizar_vagas_coletadas(self, lista_vagas: list):
        """
        Remove vagas duplicadas e vagas com dados nulos.
        """
        try:
            # Remove vagas que tenham valores vazios
            lista_vagas_filtrada = [
                vaga
                for vaga in lista_vagas
                if not any(valor == "" for valor in vaga.values())
            ]

            # Remove duplicatas convertendo a lista para um conjunto e depois
            # de volta para lista
            lista_vagas_filtrada = list(
                {tuple(vaga.items()): vaga for vaga in lista_vagas_filtrada}.values()
            )

            return lista_vagas_filtrada

        except Exception:
            logger.exception("Erro na organização das vagas coletadas")

    def __enviar_vagas_telegram(self, lista_vagas_filtrada: list, telegram_chatid: str):
        """
        Enviar as vagas no chat do telegram
        """
        try:
            for vaga in lista_vagas_filtrada:
                titulo = vaga["titulo"]
                empresa = vaga["empresa"]
                detalhes = vaga["detalhes"]
                tipo = vaga["tipo"]
                url = vaga["url"]
                logo_empresa = vaga["logo_empresa"]

                mensagem = (
                    f"<a href='{url}'>{titulo}</a> \n\n"
                    + f"<b>Empresa:</b> {empresa} \n"
                    + f"<b>Tipo:</b> {tipo} \n\n"
                    + detalhes
                )

                self.telegram_service.enviar_mensagem(
                    mensagem, logo_empresa, telegram_chatid
                )

        except Exception:
            logger.exception("Erro em enviar vagas no telegram")

    def __pegar_url_vaga(self, link_atual: str) -> str:
        """
        Montar url da vaga
        """
        try:
            # Faz o parsing da URL
            parsed_url = urlparse(link_atual)

            # Extrai os parâmetros da query string
            query_params = parse_qs(parsed_url.query)

            # Pega um parâmetro específico (por exemplo, "produto")
            current_job_id = query_params.get("currentJobId", None)[0]

            if current_job_id:
                return self.CONFIGURACAO.LINKEDIN["link_job_view"] + current_job_id
            else:
                return link_atual

        except Exception:
            logger.exception(f"Erro ao pegar URL da vaga, link: '{link_atual}'")
