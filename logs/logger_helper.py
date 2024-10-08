import logging
import os
from pathlib import Path
from datetime import datetime


class LoggerHelper:
    def __init__(self, file: str):
        self.file_name = os.path.basename(os.path.dirname(os.path.abspath(file)))
        self.file_path = f"{Path(file).resolve().parent}/"

    def get_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler = logging.FileHandler(f"{self.file_path}/{self.file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger
