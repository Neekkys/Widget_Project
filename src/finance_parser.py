import logging
from pathlib import Path

import pandas as pd

from src.config import BASE_DIR

logger = logging.getLogger("finance_parser.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    filename=BASE_DIR.joinpath("logs", "finance_parser.log"), mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def csv_reader(path_to_file):
    """Функция принимает путь к csv файлу, читает файл и возвращает
    список словарей"""
    try:
        logger.info("Получили путь к csv файлу")
        file_path = Path(path_to_file)
        if file_path.exists():
            logger.info(f"Путь к файлу {file_path.name} существует")
            if file_path.stat().st_size != 0:
                logger.info("Файл не пустой")
                df = pd.read_csv(path_to_file, sep=";")
                df = df.astype(str)
                logger.info("файл csv успешно обработан в список словарей")
                return df.to_dict(orient="records")
    except Exception as ex:
        logger.error(f"Ошибка {ex}")
        return []


def xlsx_reader(path_to_file):
    """Функция принимает путь к xlsx файлу, читает файл и возвращает
    список словарей"""
    try:
        logger.info("Получили путь к xlsx файлу")
        file_path = Path(path_to_file)
        if file_path.exists():
            logger.info(f"Путь к файлу {file_path.name} существует")
            if file_path.stat().st_size != 0:
                logger.info("Файл не пустой")
                df = pd.read_excel(path_to_file)
                df = df.astype(str)
                logger.info("Файл xlsx успешно обработан в список словарей")
                return df.to_dict(orient="records")
    except Exception as ex:
        logger.error(f"Ошибка {ex}")
        return []
