import requests
import logging

from app.core.config import settings
from app.utils.log_manage import LogManager


class TelegramService:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{settings.TELEGRAM['bot_token']}"
        self.logManager = LogManager("TelegramService")

    def enviar_mensagem(self, mensagem: str, imagem: str, chat_id: str):
        """
        Enviar mensagem no chat do telegram
        """
        try:
            if imagem:
                url = f"{self.base_url}/sendPhoto"

                data = {
                    "chat_id": chat_id,
                    "caption": mensagem,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "photo": imagem,
                }
            else:
                url = f"{self.base_url}/sendMessage"

                data = {
                    "chat_id": chat_id,
                    "text": mensagem,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                }

            response = requests.post(url, data=data)

            if response.status_code != 200:
                """Erro"""
                logging.error(f"{response.status_code} {response.text}")

            return response.json()

        except Exception as erro:
            self.logManager.add_row("Erro")
            self.logManager.add_row(erro)
