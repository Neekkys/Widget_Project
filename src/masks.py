import logging

from src.config import BASE_DIR

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=BASE_DIR.joinpath("logs", "masks.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Функция маскировки банковской карты.
    Принимает номер карты и возвращает ее маску, где видны первые 6 цифр и последние 4.
    Остальные символы отображаются звездочками. Возвращается блоками по 4 цифры
    """
    try:
        logger.info("Получили номер карты")
        CARD_LEN = 16
        card_number = card_number.strip()
        first_block = card_number[:4]
        second_block = card_number[4:6]
        last_block = card_number[-4:]

        if len(card_number) != CARD_LEN or not card_number.isdigit():
            logger.error("Неверный номер карты, введите заново")
            return "Check your card number"
        else:
            logger.info("Успешный возврат маски номера карты")
            return f"{first_block} {second_block}** **** {last_block}"
    except Exception as ex:
        logger.critical(f"Ошибка {ex}")
        return f"Ошибка {ex}"


def get_mask_account(account_number: str) -> str:
    """
    Функция маскировки номера счета.
    Принимает номер счета и возвращает 2 звездочки и последние 4 цифры номера счета.
    """
    try:
        logger.info("Получили номер счета")
        ACCOUNT_LEN = 20
        account_number = account_number.strip()
        last_four_number = account_number[-4:]

        if len(account_number) != ACCOUNT_LEN or not account_number.isdigit():
            logger.error("Неверный номер счета, введите заново")
            return "Check your account number"
        else:
            logger.info("Успешный возврат маски счета")
            return f"**{last_four_number}"
    except Exception as ex:
        logger.critical(f"Ошибка {ex}")
        return f"Ошибка {ex}"
