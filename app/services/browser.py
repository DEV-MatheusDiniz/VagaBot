import os
import logging

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager

from app.core.config import settings


class BrowserService:
    def iniciar_webdrive(self, link: str, modo_oculto: bool = False):
        """
        Criar o websriver do navegador Firefox
        """
        try:
            # Token do GitHub para ser usado
            # nas requisições de intalação do Firefox
            os.environ["GH_TOKEN"] = settings.GITHUB_TOKEN

            # Configuração das opções do Firefox
            firefox_options = Options()

            # Rodar sem interface gráfica
            if modo_oculto:
                firefox_options.add_argument("--headless")

            # Instalar driver
            path_driver = GeckoDriverManager().install()

            # Inicializa o WebDriver com as opções configuradas
            self.browser = webdriver.Firefox(
                service=Service(path_driver), options=firefox_options
            )

            self.browser.get(link)

            return True

        except Exception as erro:
            logging.error(erro)

    def interagir_elemento(
        self,
        elemento_nome: str,
        elemento_tipo: str,
        input: str = None,
        clicar: bool = False,
    ):
        """
        Realizar clicks ou preenchimento de um input
        """
        try:
            # Esperar a localização do elemento
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((elemento_tipo, elemento_nome))
            )

            elemento = self.browser.find_element(elemento_tipo, elemento_nome)

            if input:
                elemento.clear()
                elemento.send_keys(input)

            if clicar:
                elemento.click()

            return elemento

        except Exception as erro:
            logging.error(erro)

    def get_url_atual(self):
        """
        Retorna a URL que o browser estiver aberto
        """
        try:
            return self.browser.current_url
        except Exception as erro:
            logging.error(erro)
    
    def close_browser(self):
        """
        Fechar o browser
        """
        try:
            self.browser.close()
        except Exception as erro:
            logging.error(erro)
    
    def acessar_link(self, link: str):
        """
        Acessa um link
        """
        try:
            self.browser.get(link)
        except Exception as erro:
            logging.error(erro)
