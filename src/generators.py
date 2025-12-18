from typing import Any, Generator, Optional


def filter_by_currency(
    transactions: list[dict], currency: Optional[str] = None
) -> Generator[dict[str, Any], None, None]:
    """Функция, которая принимает на вход список словарей, представляющих транзакции.
    Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""
    for transaction in transactions:
        try:
            if "operationAmount" in transaction:
                json_list = str(transaction["operationAmount"]["currency"]["code"]).upper()
                if json_list == currency:
                    yield transaction
            else:
                csv_xlsx_list = transaction.get("currency_code", "").upper()
                if csv_xlsx_list == currency:
                    yield transaction
        except KeyError:
            continue


def transaction_descriptions(transactions: list[dict]) -> Generator[str, None, None]:
    """Генератор, который принимает список словарей с транзакциями и
    возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        try:
            if transaction["description"]:
                yield transaction["description"]
        except KeyError:
            continue


def card_number_generator(first_value: int, last_value: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX
    в диапазоне от first_value до last_value включительно"""
    if not 0 <= first_value <= last_value <= 9999_9999_9999_9999:
        raise ValueError("Incorrect range of values")

    for card_number in range(first_value, last_value + 1):
        card_str = format(card_number, "016d")
        gen = " ".join(card_str[x:x + 4] for x in range(0, 16, 4))
        yield gen
