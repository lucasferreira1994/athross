import os
import logging


class TestLogger:
    def __init__(self, tag: str):
        self.tag = tag
        self.logger = logging.getLogger(tag)
        self.logger.setLevel(logging.INFO)

        self._create_dir()

        log_path = os.path.join("test_logs", "test_document_types.log")

        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

            file_handler = logging.FileHandler(log_path, mode='a')
            file_handler.setFormatter(formatter)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def _create_dir(self):
        if not os.path.exists("test_logs"):
            os.makedirs("test_logs")

    def info(self, message: str):
        self.logger.info(f"{self.tag} {message}")

    def warning(self, message: str):
        self.logger.warning(f"{self.tag} {message}")

    def error(self, message: str):
        self.logger.error(f"{self.tag} {message}")

    def debug(self, message: str):
        self.logger.debug(f"{self.tag} {message}")