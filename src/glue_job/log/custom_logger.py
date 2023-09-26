import logging
from logging import Logger


class CustomLog:
    logger: Logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def log_info(self, msg):
        self.logger.info(msg)
