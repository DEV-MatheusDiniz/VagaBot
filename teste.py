import logging

from app.services.automacao_linkedin import AutomacaoLinkedin

from app.core.config import settings


if __name__ == "__main__":
    try:
        automacao_linkedin = AutomacaoLinkedin()
        automacao_linkedin.run(settings.MODO_OCULTO)

    except Exception as erro:
        logging.error(erro)
