import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(transactions, transactions_usd):
    assert list(filter_by_currency(transactions, "USD")) == transactions_usd


def test_filter_by_currency_rub(transactions, transactions_rub):
    assert list(filter_by_currency(transactions, "RUB")) == transactions_rub


def test_filter_by_currency_empty(transactions):
    assert list(filter_by_currency(transactions)) == []


def test_filter_by_currency_EUR(transactions):
    assert list(filter_by_currency(transactions, "EUR")) == []


def test_transaction_descriptions(transactions, description):
    assert list(transaction_descriptions(transactions)) == description


def test_transaction_none_descriprions():
    assert (
        list(
            transaction_descriptions(
                [
                    {
                        "id": 649467725,
                        "state": "EXECUTED",
                        "date": "2018-04-14T19:35:28.978265",
                        "operationAmount": {"amount": "96995.73", "currency": {"name": "руб.", "code": "RUB"}},
                        "from": "Счет 27248529432547658655",
                        "to": "Счет 97584898735659638967",
                    }
                ]
            )
        )
        == []
    )


@pytest.mark.parametrize(
    "first, last, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9, 10, ["0000 0000 0000 0009", "0000 0000 0000 0010"]),
        (9999_9999_9999_9998, 9999_9999_9999_9999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
        (-1, 1, "Incorrect range of values"),
        (1, 1_0000_0000_0000_0000, "Incorrect range of values"),
    ],
)
def test_param_card_number_generator(first, last, expected):
    if isinstance(expected, list):
        result = list(card_number_generator(first, last))
        assert result == expected
    else:
        with pytest.raises(ValueError, match="Incorrect range of values"):
            list(card_number_generator(first, last))


def test_card_number_generator_wrong_type():
    with pytest.raises(TypeError):
        list(card_number_generator("15", 16))
