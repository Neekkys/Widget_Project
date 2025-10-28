import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_data: str) -> str:
    """ Функция которая принимает одним аргументом тип данных
     и номер данных, а затем маскирует номер данных"""
    pattern = "Счет"
    data_type = bool(re.search(pattern, card_data))

    # Маска для счёта
    if data_type:
        account_list = card_data.split(" ")
        account_type = account_list[0]
        account_number = get_mask_account(account_list[-1])
        return f"{account_type} {account_number}"

    # Маска для карты
    else:
        card_list = card_data.split(" ")
        card_type = card_list[0:-1]
        card_number = get_mask_card_number(card_list[-1])
        return f"{" ".join(card_type)} {card_number}"


def get_date(iso_date: str) -> str:
    """ Функция принимает дату и время в формате ISO преобразует и
    возвращает в привычную человеческому глазу"""
    date = datetime.fromisoformat(iso_date)
    return date.strftime("%d.%m.%Y %H:%M:%S")


if __name__ == "__main__":
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 35383033474447895560"))
    print(mask_account_card("Visa Classic 6831982476737658"))
    print(mask_account_card("Visa Platinum 8990922113665229"))
    print(mask_account_card("Visa Gold 5999414228426353"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
