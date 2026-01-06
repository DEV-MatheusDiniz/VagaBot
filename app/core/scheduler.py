from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from ..core.config import settings
from ..jobs.linkedin import LinkedinJob
from ..utils.log_util import print_jobs_apscheduler


scheduler = BackgroundScheduler()


def job_listener(event):
    """
    Registra logs de sucesso ou erro após a execução de uma tarefa agendada.

    Parâmetros:
        event: Evento disparado pelo APScheduler após a execução de uma tarefa.
    """
    if event.exception:
        logger.error(f"Tarefa '{event.job_id}' falhou")
    else:
        logger.debug(f"Tarefa '{event.job_id}' foi executado com sucesso")


def start_scheduler():
    """
    Inicia o agendador de tarefas em segundo plano.
    - Adiciona o listener para registrar logs de execução e falhas.
    """
    if not scheduler.running:
        linkedin_job = LinkedinJob()

        # Agendamento das tasks
        scheduler.add_job(
            id="LinkedinJob",
            func=linkedin_job.run,
            kwargs={"modo_oculto": settings.MODO_OCULTO},
            max_instances=1,

            # trigger="cron",
            # hour=settings.SCHEDULE_HORARIOS,
            
            trigger="interval",
            seconds=5,
        )

        # Adiciona listener de logs
        scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        # Só inicia o agendardor se tiver jobs
        if len(scheduler.get_jobs()) == 0:
            logger.critical("Nenhum job a ser processado")
            return

        print_jobs_apscheduler(scheduler)

        # Começa o agendador
        scheduler.start()
        logger.success("Agendador de tarefas iniciado")


def close_scheduler():
    """
    Encerra o agendador de tarefas
    - Adiciona o listener para registrar logs de execução e falhas.
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.success("Agendador de tarefas encerrado")
