import logging

from app.services.automacao_linkedin import AutomacaoLinkedin

from app.core.config import settings
from app.services.job_scheduler import JobSchedule


if __name__ == "__main__":
    try:
        automacao_linkedin = AutomacaoLinkedin()

        JobSchedule().run(
            settings.SCHEDULE_HORARIOS,
            automacao_linkedin.run,
            modo_oculto=settings.MODO_OCULTO,
        )

    except Exception as erro:
        logging.error(erro)
