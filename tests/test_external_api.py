from unittest.mock import Mock, patch

import pytest
import requests.exceptions

from src.external_api import api_convert


def test_api_convert_usd_success():
    """Успешная конвертация USD в RUB"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.0}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = api_convert("USD", 100.0)

        mock_get.assert_called_once()
        call_args = mock_get.call_args

        assert call_args.kwargs["params"]["from"] == "USD"
        assert call_args.kwargs["params"]["to"] == "RUB"
        assert call_args.kwargs["params"]["amount"] == 100.0
        assert call_args.kwargs["headers"]["apikey"] is not None

        assert result == 7500.0


def test_api_convert_eur_success():
    """Успешная конвертация EUR в RUB"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 8500.0}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = api_convert("EUR", 100.0)

        mock_get.assert_called_once()
        assert result == 8500.0


def test_api_convert_not_supported_currency():
    """Валюты не из списка EUR/USD возвращают 0.0 без вызова API"""
    with patch("requests.get") as mock_get:
        assert api_convert("GBP", 100.0) == 0.0
        assert api_convert("JPY", 100.0) == 0.0
        assert api_convert("KZT", 100.0) == 0.0

        mock_get.assert_not_called()


def test_api_convert_case_sensitive():
    """Проверка чувствительности к регистру кода валюты"""
    with patch("requests.get") as mock_get:
        assert api_convert("usd", 100.0) == 0.0
        assert api_convert("Eur", 100.0) == 0.0
        mock_get.assert_not_called()
        mock_response = Mock()
        mock_response.json.return_value = {"result": 7500.0}
        with patch("requests.get", return_value=mock_response):
            result = api_convert("USD", 100.0)
            assert result == 7500.0


def test_api_convert_amount_as_string():
    """Конвертация суммы, переданной как строка"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.0}

    with patch("requests.get", return_value=mock_response):
        result = api_convert("USD", "100.0")
        assert result == 7500.0


def test_api_convert_api_error(capsys):
    """Обработка ошибки при вызове API"""
    with patch("requests.get", side_effect=Exception("Connection error")):
        result = api_convert("USD", 100.0)

        captured = capsys.readouterr()
        assert "Exception -- Connection error" in captured.out

        assert result == 0.0


def test_api_convert_response_json_error(capsys):
    """Обработка ошибки в JSON ответе"""
    mock_response = Mock()
    mock_response.json.side_effect = Exception("Invalid JSON")

    with patch("requests.get", return_value=mock_response):
        result = api_convert("USD", 100.0)

        captured = capsys.readouterr()
        assert "Exception -- Invalid JSON" in captured.out
        assert result == 0.0


def test_api_convert_response_missing_result_key(capsys):
    """Ответ API не содержит ключ 'result'"""
    mock_response = Mock()
    mock_response.json.return_value = {"error": "Invalid API key"}

    with patch("requests.get", return_value=mock_response):
        result = api_convert("USD", 100.0)

        captured = capsys.readouterr()
        assert "KeyError" in captured.out or "Exception" in captured.out
        assert result == 0.0


def test_api_convert_network_timeout(capsys):
    """Таймаут при сетевом запросе"""
    with patch("requests.get", side_effect=requests.exceptions.Timeout()):
        result = api_convert("USD", 100.0)

        captured = capsys.readouterr()
        assert "Timeout -- " in captured.out or "Exception -- " in captured.out
        assert result == 0.0


def test_api_convert_connection_error(capsys):
    """Ошибка соединения"""
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError()):
        result = api_convert("USD", 100.0)

        captured = capsys.readouterr()
        assert "ConnectionError -- " in captured.out or "Exception -- " in captured.out
        assert result == 0.0


def test_api_convert_headers_contain_api_key():
    """Проверка, что API ключ передается в заголовках"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.0}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = api_convert("USD", 100.0)

        mock_get.assert_called_once()
        call_args = mock_get.call_args

        assert "apikey" in call_args.kwargs["headers"]
        assert result == 7500.0


def test_api_convert_zero_amount():
    """Конвертация нулевой суммы"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 0.0}

    with patch("requests.get", return_value=mock_response):
        result = api_convert("USD", 0.0)
        assert result == 0.0


def test_api_convert_negative_amount():
    """Конвертация отрицательной суммы"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": -7500.0}

    with patch("requests.get", return_value=mock_response):
        result = api_convert("USD", -100.0)
        assert result == -7500.0


@pytest.mark.parametrize(
    "currency, expected_call",
    [
        ("USD", True),
        ("EUR", True),
        ("GBP", False),
        ("JPY", False),
        ("CHF", False),
        ("CNY", False),
    ],
)
def test_api_convert_currency_support(currency, expected_call):
    """Проверка поддержки различных валют"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 100.0}

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = api_convert(currency, 100.0)

        if expected_call:
            mock_get.assert_called_once()
        else:
            mock_get.assert_not_called()
            assert result == 0.0
