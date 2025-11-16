import pytest

from src.masks import get_mask_account, get_mask_card_number


# Функция get_mask_card_number
def test_get_mask_card_number(card_number):
    assert get_mask_card_number(card_number) == "4111 11** **** 1111"


def test_empty_get_mask_card_number():
    assert get_mask_card_number("") == "Check your card number"


# Функция get_mask_account
def test_get_mask_account(account_number):
    assert get_mask_account(account_number) == "**7890"


def test_empty_get_mask_account():
    assert get_mask_account("") == "Check your account number"


# Параметризация обоих функций
@pytest.mark.parametrize(
    "card_num, expected",
    [
        ("5555555555554444", "5555 55** **** 4444"),
        ("371449635398431", "Check your card number"),
        ("6011-1111-1111-1117", "Check your card number"),
        ("  3530111333300000  ", "3530 11** **** 0000"),
        ("4111111111111111 ", "4111 11** **** 1111"),
        ("510510510b105100", "Check your card number"),
        ("30569309025904", "Check your card number"),
        ("3566002020360505", "3566 00** **** 0505"),
        ("6200000000000005", "6200 00** **** 0005"),
        ("1234567812345670", "1234 56** **** 5670"),
    ],
)
def test_get_mask_card_number_param(card_num, expected):
    assert get_mask_card_number(card_num) == expected


@pytest.mark.parametrize(
    "account_num, expected",
    [
        ("12345678901234567890", "**7890"),
        ("00000000000000000000", "**0000"),
        ("99999999999999999999", "**9999"),
        ("11111111111111111111", "**1111"),
        ("55555555555555555555", "**5555"),
        ("  22222222222222222222  ", "**2222"),
        ("5555555555555555555", "Check your account number"),
        ("123123123123123123123123123123", "Check your account number"),
        ("1111111111111111111h", "Check your account number"),
    ],
)
def test_get_mask_account_param(account_num, expected):
    assert get_mask_account(account_num) == expected
