import logging
import os


class LogFactory:
    @staticmethod
    def get_logger(name: str):
        log_level = os.environ.get("LOG_LEVEL")
        if not log_level:
            log_level = logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s:%(name)s.%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S')

        return logging.getLogger(name)
