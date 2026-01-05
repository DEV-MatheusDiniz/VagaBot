from loguru import logger

from app.jobs.linkedin import AutomacaoLinkedin
from app.core.config import settings


if __name__ == "__main__":
    try:
        automacao_linkedin = AutomacaoLinkedin()
        automacao_linkedin.run(settings.MODO_OCULTO)
    except Exception as erro:
        logger.exception(erro)
