import re

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
