def get_mask_card_number(card_number: str) -> str:
    """
    Функция маскировки банковской карты.
    Принимает номер карты и возвращает ее маску, где видны первые 6 цифр и последние 4.
    Остальные символы отображаются звездочками. Возвращается блоками по 4 цифры
    """
    CARD_LEN = 16
    card_number = card_number.strip()
    first_block = card_number[:4]
    second_block = card_number[4:6]
    last_block = card_number[-4:]

    if len(card_number) != CARD_LEN or not card_number.isdigit():
        return "Check your card number"
    else:
        return f"{first_block} {second_block}** **** {last_block}"


def get_mask_account(account_number: str) -> str:
    """
    Функция маскировки номера счета.
    Принимает номер счета и возвращает 2 звездочки и последние 4 цифры номера счета.
    """
    ACCOUNT_LEN = 20
    account_number = account_number.strip()
    last_four_number = account_number[-4:]

    if len(account_number) != ACCOUNT_LEN or not account_number.isdigit():
        return "Check your account number"
    else:
        return f"**{last_four_number}"
