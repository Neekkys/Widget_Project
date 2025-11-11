import re


def filter_by_state(operation_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функцуя ищет в списке словарей ключ 'state', сравнивает значение ключа с аргументом state
    и возвращает новый список словарей, в которых значение ключа равно аргументу"""
    operation_list_required = [
        operation for operation in operation_list if re.search(state, operation.get("state", ""))
    ]
    # Сделано с рассчетом на то, что будет только 2 вида операций "EXECUTED" и "CANCELED"
    return operation_list_required


def sort_by_date(operation_list: list[dict], reverse: bool = True) -> list[dict]:
    """Функция, которая принимает список словарей, и сортирует их по значению
    ключа 'date', по умолчанию по убыванию"""
    sorted_list_operation = sorted(operation_list, key=lambda x: x["date"], reverse=reverse)
    return sorted_list_operation


if __name__ == "__main__":
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            # "CANCELED"
        )
    )

    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
