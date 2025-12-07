import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
url = "https://api.apilayer.com/exchangerates_data/convert"


def api_convert(currency_code: str, amount: str | float) -> float:
    """Конвертирует сумму из указанной валюты в рубли"""
    payload = {"to": "RUB", "from": currency_code, "amount": amount}
    headers = {"apikey": api_key}
    if currency_code not in ["EUR", "USD"]:
        return 0.0
    else:
        try:
            response = requests.get(url, headers=headers, params=payload)
            amount_rub_json = response.json()
            result = amount_rub_json["result"]
            return float(result)
        except Exception as e:
            print(f"{type(e).__name__} -- {str(e)}")
            return 0.0
