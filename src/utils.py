import json
from typing import Any, Dict, List, Union

from src.config import BASE_DIR
from src.external_api import api_convert


def unpacking_json_file(file_name: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Функция принимает на вход .json файл и десериализует его"""
    data_dir = BASE_DIR.joinpath("data", file_name)
    try:
        with open(data_dir, "r", encoding="utf8") as f:
            unpacked_json_transactions = json.load(f)
            if isinstance(unpacked_json_transactions, (list, dict)):
                return unpacked_json_transactions
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"{type(e).__name__} - {str(e)}")
        return []


def extract_transaction_amount(unpacked_json_transactions: Union[List[Dict[str, Any]], Dict[str, Any]]) -> float:
    """Функция принимает транзакцию, обрабатывает валюту транзакции и возвращает сумму транзакции в рублях.
    Если сумма транзакции в EUR или USD, функция обращается к апи-конвертору,
    который переводит валюту в рубли и возвращает сумму в рублях"""
    try:
        if isinstance(unpacked_json_transactions, list):
            if not unpacked_json_transactions:
                return 0.0
            current_amount = unpacked_json_transactions[0]["operationAmount"]["amount"]
            code_currency = unpacked_json_transactions[0]["operationAmount"]["currency"]["code"]
        elif isinstance(unpacked_json_transactions, dict):
            current_amount = unpacked_json_transactions["operationAmount"]["amount"]
            code_currency = unpacked_json_transactions["operationAmount"]["currency"]["code"]
        else:
            return 0.0
    except (IndexError, TypeError, KeyError) as e:
        print(f"{type(e).__name__} -- {str(e)}")
        return 0.0
    if code_currency == "RUB":
        return float(current_amount)
    else:
        converter = api_convert(code_currency, current_amount)
        return converter
