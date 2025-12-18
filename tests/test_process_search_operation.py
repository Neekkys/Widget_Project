from unittest.mock import patch

from src.process_search_operation import process_bank_description, process_bank_operations


def test_process_bank_description_basic_match(sample_bank_operations):
    """Тест базового поиска по описанию"""
    result = process_bank_description(sample_bank_operations, "Grocery")

    assert len(result) == 2
    assert all("Grocery" in op["description"] for op in result)
    assert result[0]["amount"] == 100.50
    assert result[1]["amount"] == 75.25


def test_process_bank_description_no_matches(sample_bank_operations):
    """Тест когда строка не найдена"""
    result = process_bank_description(sample_bank_operations, "Restaurant")

    assert result == []
    assert len(result) == 0


def test_process_bank_description_missing_description_key():
    """Тест с операциями без ключа description"""
    operations = [
        {"amount": 100},
        {"description": "Grocery", "amount": 50},
        {"other_field": "value"},
        {"description": "", "amount": 25}
    ]

    result = process_bank_description(operations, "Grocery")

    assert len(result) == 1
    assert result[0]["description"] == "Grocery"


def test_process_bank_description_empty_search_string(sample_bank_operations):
    """Тест с пустой строкой поиска"""
    result = process_bank_description(sample_bank_operations, "")

    # Пустая строка должна совпадать со всеми описаниями
    assert len(result) == len(sample_bank_operations)


@patch('re.search')
def test_process_bank_description_exception_handling(mock_search):
    """Тест обработки исключений"""
    mock_search.side_effect = Exception("Regex error")

    operations = [{"description": "Test", "amount": 100}]

    with patch('builtins.print') as mock_print:
        result = process_bank_description(operations, "Test")

        assert result == []
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0]
        assert len(call_args) == 1
        assert isinstance(call_args[0], Exception)
        assert str(call_args[0]) == "Regex error"


def test_process_bank_operations_basic_counting(operations, sample_categories):
    """Тест базового подсчета операций"""
    result = process_bank_operations(operations, sample_categories)
    assert result == {
        "Grocery": 2,
        "Entertainment": 1,
        "Transport": 1,
        "Food": 1
    }


def test_process_bank_operations_with_missing_description_key():
    """Тест с операциями без ключа description"""
    operations = [
        {"amount": 100},  # Нет ключа description
        {"description": "Grocery", "amount": 50},
        {"other_field": "value"},
        {"description": "", "amount": 25}  # Пустое описание
    ]

    categories = ["Grocery", "Food"]

    result = process_bank_operations(operations, categories)

    assert result == {
        "Grocery": 1,
        "Food": 0
    }


def test_process_bank_operations_uses_counter_logic():
    """Тест логики подсчета операций"""
    operations = [
        {"description": "Grocery", "amount": 100},
        {"description": "Grocery", "amount": 50},
        {"description": "Food", "amount": 25},
        {"description": "Transport", "amount": 30}  # Не входит в категории
    ]
    categories = ["Grocery", "Food", "Entertainment"]

    result = process_bank_operations(operations, categories)

    assert result == {
        "Grocery": 2,
        "Food": 1,
        "Entertainment": 0
    }
