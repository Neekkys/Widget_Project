import json
import logging
from typing import Any, Dict, List, Union

from src.config import BASE_DIR
from src.external_api import api_convert

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=BASE_DIR.joinpath("logs", "utils.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def unpacking_json_file(file_name: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Функция принимает на вход .json файл и десериализует его"""
    data_dir = BASE_DIR.joinpath("data", file_name)
    try:
        logger.info("Открываем файл")
        with open(data_dir, "r", encoding="utf8") as f:
            unpacked_json_transactions = json.load(f)
            if isinstance(unpacked_json_transactions, (list, dict)):
                logger.info("Успешно десериализовали файл")
                return unpacked_json_transactions
            else:
                logger.error("Произошла ошибка при десериализации")
                return []
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        logger.critical(f"Произошла ошибка при открытии файла: {type(e).__name__} - {str(e)}")
        return []


def extract_transaction_amount(unpacked_json_transactions: Union[List[Dict[str, Any]], Dict[str, Any]]) -> float:
    """Функция принимает транзакцию в виде списка или словаря, обрабатывает валюту транзакции
    и возвращает сумму транзакции в рублях.
    Если сумма транзакции в EUR или USD, функция обращается к апи-конвертору,
    который переводит валюту в рубли и возвращает сумму в рублях"""
    try:
        logger.info("Принимаем транзакцию")
        if isinstance(unpacked_json_transactions, list):
            if not unpacked_json_transactions:
                logger.error("Произошла ошибка: список пустой")
                return 0.0
            current_amount = unpacked_json_transactions[0]["operationAmount"]["amount"]
            code_currency = unpacked_json_transactions[0]["operationAmount"]["currency"]["code"]
            logger.info("Данные о сумме транзакции и валюте собраны из списка")
        elif isinstance(unpacked_json_transactions, dict):
            current_amount = unpacked_json_transactions["operationAmount"]["amount"]
            code_currency = unpacked_json_transactions["operationAmount"]["currency"]["code"]
            logger.info("Данные о сумме транзакции и валюте собраны из словаря")
        else:
            logger.error("Данные не собраны")
            return 0.0

        logger.info("Сверяем код валюты")
        if code_currency == "RUB":
            logger.info("Код валюты - российский рубль. Возврат суммы")
            return float(current_amount)
        else:
            logger.info(f"Код валюты: {code_currency}, обращаемся к API для конвертации")
            converter = api_convert(code_currency, current_amount)
            if converter == 0.0:
                logger.error("Ошибка - валюта конвертировалась некорректно")
                return 0.0
            logger.info("Валюта конвертировалась корректно")
            return converter
    except (IndexError, TypeError, KeyError, Exception) as e:
        logger.critical(f"Ошибка: {type(e).__name__} -- {str(e)}")
    return 0.0
