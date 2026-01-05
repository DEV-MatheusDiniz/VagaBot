from loguru import logger
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler


def print_jobs_apscheduler(scheduler: BackgroundScheduler):
    """
    Printar no log as informações do jobs agendados no apscheduler
    """
    jobs = scheduler.get_jobs()

    if jobs:
        logger.info("#" * 15 + " Tasks Agendadas")

        for job in jobs:
            job: Job
            logger.info(" " * 5 + f"Nome: {job.id}")
            logger.info(" " * 5 + f"Função: {job.name}")
            logger.info(" " * 5 + f"Qtd. instancias: {job.max_instances}")
            logger.info(" " * 5 + f"Período: {job.trigger}")
            logger.info("")

        logger.info("#" * 35)
