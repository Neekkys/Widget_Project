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
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected


@pytest.mark.parametrize("invalid_iso_date", [
    "2023-13-01",          # Несуществующий месяц
    "2023-02-30",          # Несуществующий день
    "2023-06-31",          # Несуществующий день (в июне 30 дней)
    "2023-00-15",          # Нулевой месяц
    "2023-04-00",          # Нулевой день
    "2023/04/15",          # Неправильный разделитель
    "2023-04-15T25:00:00", # Невалидный час
    "2023-04-15T10:60:00", # Невалидная минута
    "2023-04-15T10:00:60", # Невалидная секунда
    "not_a_date",          # Произвольная строка
    "",                    # Пустая строка
])
def test_get_date_invalid(invalid_iso_date):
    with pytest.raises(ValueError):
        get_date(invalid_iso_date)


@pytest.mark.parametrize("invalid_iso_date", [
    # Абсолютно невалидные строки
    "not_a_date",
    "",
    "2023/04/15",
    "15.04.2023",

    # Неправильные форматы дат
    "2023-13-01",
    "2023-00-15",
    "2023-04-00",
    "2023-02-30",
    "2023-04-31",

    # Неправильные форматы времени
    "2023-04-15T25:00:00",
    "2023-04-15T10:60:00",
    "2023-04-15T10:00:60",

    # Неполные даты
    "2023-04",
    "2023",

    # Случаи с лишними символами
    "2023-04-15T10:00:00XYZ",
    "2023-04-15T10:00:00+25:00",

    # Специальные символы
    "2023-04-15T10:00:00\n",
    "2023-04-15T10:00:00 ",
    None,
])
def test_get_date_with_invalid_input(invalid_iso_date):
    with pytest.raises((ValueError, TypeError)):
        get_date(invalid_iso_date)