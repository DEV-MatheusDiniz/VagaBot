import logging
import environs


class Settings:
    env = environs.Env()
    env.read_env()

    # Selenium
    GITHUB_TOKEN: str = env.str("GITHUB_TOKEN")

    # Linkedin
    LINKEDIN: dict = {
        "link": "https://www.linkedin.com",
        "link_job_view": "https://www.linkedin.com/jobs/view/",
        "link_job_search": "https://www.linkedin.com/jobs/search/",
        "email": env.str("LINKEDIN_EMAIL"),
        "senha": env.str("LINKEDIN_SENHA"),
    }

    # Telegram
    TELEGRAM: dict = {
        "bot_token": env.str("TELEGRAM_BOT_TOKEN"),
        "url_api": "https://api.telegram.org/bot",
    }

    JOBS_LINKEDIN_VAGAS: list = [
        {
            "tema": "Desenvolvimento de Software",
            "telegram_chatid": env.str("JOBS_LINKEDIN_VAGAS_TELEGRAM_DEV_CHATID"),
            "buscas": [
                """ "java" AND ("junior" OR "jr" OR "pleno" OR "pl") """,
                """ "python" AND ("junior" OR "jr" OR "pleno" OR "pl") """,
            ],
            "filtros": {
                "ordem_mais_recente": True,
                "ultimos_24_horas": False,
                "candidatura_simplificada": False,
                "ate_10_candidaturas": True,
                "remoto": True,
            },
        },
        {
            "tema": "Direito",
            "telegram_chatid": env.str("JOBS_LINKEDIN_VAGAS_TELEGRAM_DIREITO_CHATID"),
            "buscas": [
                """ "Advogado" OR "Direito" AND ("cível" OR "Trabalhista" OR "Junior" OR "jr") """,
            ],
            "filtros": {
                "ordem_mais_recente": True,
                "ultimos_24_horas": False,
                "candidatura_simplificada": True,
                "ate_10_candidaturas": True,
                "remoto": True,
            },
        },
        {
            "tema": "Contabilidade",
            "telegram_chatid": env.str("JOBS_LINKEDIN_VAGAS_TELEGRAM_CONTABIL_CHATID"),
            "buscas": [
                """ "contabilidade" AND ("Pleno" OR "pl") """,
                """ "contabilidade" AND ("Senior" OR "sn") """,
            ],
            "filtros": {
                "ordem_mais_recente": True,
                "ultimos_24_horas": False,
                "candidatura_simplificada": False,
                "ate_10_candidaturas": True,
                "remoto": True,
            },
        },
        {
            "tema": "Empresas",
            "telegram_chatid": env.str("JOBS_LINKEDIN_VAGAS_TELEGRAM_EMPRESAS_CHATID"),
            "buscas": [
                "Sicoob",
                "Hepta",
                "G4F",
                "Ifood",
            ],
            "filtros": {
                "ordem_mais_recente": True,
                "ultimos_24_horas": False,
                "candidatura_simplificada": False,
                "ate_10_candidaturas": True,
                "remoto": False,
            },
        },
    ]

    # Script
    MODO_OCULTO: bool = env.bool("MODO_OCULTO", default=False)

    # Scheduler
    SCHEDULE_HORARIOS: list = [
        "08:00",
        "10:00",
        "12:00",
        "14:00",
        "16:00",
        "18:00",
    ]

    # Config do logs
    logging.basicConfig(
        format="%(levelname)s: %(asctime)s - %(message)s",
        datefmt="%d/%m/%Y | %H:%M",
        level="INFO",
    )


settings: Settings = Settings()
