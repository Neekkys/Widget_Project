import re
from collections import Counter


def process_bank_description(bank_operations: list[dict], description: str) -> list[dict]:
    """Функция принимает список словарей и строку которую надо найти.
    Возвращает список словарей, у которых в описании есть данная строка"""
    try:
        filtered_list = [
            operation
            for operation in bank_operations
            if re.search(description, operation.get("description", ""), re.IGNORECASE)
        ]
        return filtered_list
    except Exception as ex:
        print(ex)
        return []


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Функция, которая принимает на вход список словарей с банковскими операциями и
    список категорий операций. Возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории."""
    # Создаем список категорий, где описание операции ТОЧНО совпадает с категорией
    found_categories = [
        cat for operation in data for cat in categories if operation.get("description", "").lower() == cat.lower()
    ]
    counter_dict = Counter(found_categories)

    result = {cat: counter_dict.get(cat, 0) for cat in categories}
    return result
