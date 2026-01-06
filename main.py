import time

from loguru import logger

from app.core.scheduler import start_scheduler, close_scheduler
from app.services.browser import BrowserService


if __name__ == "__main__":
    try:
        start_scheduler()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        close_scheduler()
