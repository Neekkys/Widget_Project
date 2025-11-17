import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "type_number, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(type_number, expected):
    assert mask_account_card(type_number) == expected


def test_mask_account_card_empty():
    assert mask_account_card("") == "Check your card number"


@pytest.mark.parametrize(
    "date, expected",
    [
        # Правильные даты
        ("2024-03-15T10:30:45", "15.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-02-29_14:25:00", "29.02.2024"),
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-06-15 08:45:30+03:00", "15.06.2024"),
        # Неправильные даты
        ("2024-13-45T25:61:61", "Incorrect date format"),
        ("2024-02-30T10:30:45", "Incorrect date format"),
        ("2026/03/15T10:30:45", "Incorrect date format"),
        ("20-03-2024T10:30:45", "Incorrect date format"),
        ("2024-03T10:30:45", "Incorrect date format"),
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected
