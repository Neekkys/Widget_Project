import re


def filter_by_state(operation_list: list[dict], state: str = "EXECUTED") -> list[dict] | str:
    """Функцуя ищет в списке словарей ключ 'state', сравнивает значение ключа с аргументом state
    и возвращает новый список словарей, в которых значение ключа равно аргументу"""
    if not operation_list:
        return "Error, the list is empty"
    operation_list_required = [
        operation for operation in operation_list if re.search(state, operation.get("state", ""))
    ]
    if not operation_list_required:
        return "Error, operation not found"
    # Сделано с рассчетом на то, что будет только 2 вида операций "EXECUTED" и "CANCELED"
    return operation_list_required


def sort_by_date(operation_list: list[dict], reverse: bool = True) -> list[dict] | str:
    """Функция, которая принимает список словарей, и сортирует их по значению
    ключа 'date', по умолчанию по убыванию"""
    if not operation_list:
        return "Error, the list is empty"
    sorted_list_operation = sorted(operation_list, key=lambda x: x["date"], reverse=reverse)
    return sorted_list_operation
