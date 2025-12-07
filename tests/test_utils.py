import json
from unittest.mock import mock_open, patch

from _pytest.capture import CaptureFixture

from src.utils import extract_transaction_amount, unpacking_json_file


def test_unpacking_json_file_valid_list():
    """Успешная десериализация JSON файла со списком"""
    test_data = [
        {"id": 1, "operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"amount": "200.0", "currency": {"code": "EUR"}}},
    ]
    json_str = json.dumps(test_data)

    with patch("builtins.open", mock_open(read_data=json_str)) as mock_file:
        result = unpacking_json_file("test.json")

        mock_file.assert_called_once()
        # Проверяем путь к файлу
        assert "data" in str(mock_file.call_args[0][0])
        assert "test.json" in str(mock_file.call_args[0][0])
        # Проверяем параметры открытия файла
        assert mock_file.call_args[0][1] == "r"
        assert mock_file.call_args[1]["encoding"] == "utf8"
        assert result == test_data


def test_unpacking_json_file_valid_dict():
    """Успешная десериализация JSON файла со словарем"""
    test_data = {"id": 1, "operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}}
    json_str = json.dumps(test_data)

    with patch("builtins.open", mock_open(read_data=json_str)) as mock_file:  # noqa: F841
        result = unpacking_json_file("test.json")

        mock_file.assert_called_once()
        assert "data" in str(mock_file.call_args[0][0])
        assert "test.json" in str(mock_file.call_args[0][0])
        assert mock_file.call_args[0][1] == "r"
        assert mock_file.call_args[1]["encoding"] == "utf8"
        assert result == test_data


def test_unpacking_json_file_invalid_structure():
    """Некорректная структура JSON (не список и не словарь)"""
    json_str = '"просто строка"'

    with patch("builtins.open", mock_open(read_data=json_str)):
        result = unpacking_json_file("test.json")
        assert result == []


def test_unpacking_json_file_empty():
    """Пустой файл (возвращает пустой список)"""
    with patch("builtins.open", mock_open(read_data="")):
        result = unpacking_json_file("test.json")
        assert result == []


@patch("builtins.open", side_effect=json.JSONDecodeError("Ошибка JSON", "test.json", 0))
def test_unpacking_json_file_json_decode_error(mock_open, capsys: CaptureFixture):
    """Некорректный JSON, возвращает сообщение и []"""
    result = unpacking_json_file("test.json")

    captured = capsys.readouterr()
    assert "JSONDecodeError" in captured.out
    assert "Ошибка JSON" in captured.out
    assert result == []


def test_extract_transaction_amount_empty_list():
    """Пустой список транзакций, возвращает 0.0"""
    result = extract_transaction_amount([])
    assert result == 0.0


def test_extract_transaction_amount_none():
    """None вместо данных, возвращает 0.0"""
    result = extract_transaction_amount(None)
    assert result == 0.0


def test_extract_transaction_amount_invalid_structure():
    """Некорректная структура данных, возвращает 0.0"""
    result = extract_transaction_amount("неверные данные")
    assert result == 0.0


def test_extract_transaction_amount_list_missing_keys(capsys: CaptureFixture):
    """Список транзакций без нужных ключей, возвращает 0.0"""
    data = [{"id": 1}]
    result = extract_transaction_amount(data)

    assert result == 0.0


def test_extract_transaction_amount_dict_missing_keys(capsys: CaptureFixture):
    """Словарь транзакций без нужных ключей, возвращает 0.0"""
    data = {"id": 1}
    result = extract_transaction_amount(data)

    assert result == 0.0
