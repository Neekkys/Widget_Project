def filter_by_state(operation_list: list[dict], state: str = "EXECUTED") -> list[dict] | str:
    """Функция ищет в списке словарей ключ 'state', сравнивает значение ключа с аргументом state
    и возвращает новый список словарей, в которых значение ключа равно аргументу"""
    new_list = [i for i in operation_list if i.get("state", "") == state]
    return new_list


def sort_by_date(operation_list: list[dict], reverse: bool = True) -> list[dict] | str:
    """Функция, которая принимает список словарей, и сортирует их по значению
    ключа 'date', по умолчанию по убыванию"""
    if not operation_list:
        return []
    sorted_list_operation = sorted(operation_list, key=lambda x: x["date"], reverse=reverse)
    return sorted_list_operation
