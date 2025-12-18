from unittest.mock import MagicMock, patch


# Тесты для csv_reader
@patch('pandas.read_csv')
@patch('pathlib.Path')
def test_csv_reader_success(mock_path_class, mock_read_csv):
    """Тест успешного чтения CSV файла"""
    # Мокаем Path
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.stat.return_value.st_size = 100
    mock_path.name = 'test.csv'
    mock_path_class.return_value = mock_path

    # Мокаем pandas
    mock_df = MagicMock()
    mock_df.astype.return_value = mock_df
    mock_df.to_dict.return_value = [{'col1': 'val1', 'col2': 'val2'}]
    mock_read_csv.return_value = mock_df

    # Импортируем функцию
    from src.finance_parser import csv_reader

    result = csv_reader('/path/to/file.csv')

    assert result == [{'col1': 'val1', 'col2': 'val2'}]
    mock_read_csv.assert_called_once_with('/path/to/file.csv', sep=';')
    mock_df.astype.assert_called_once_with(str)


@patch('pathlib.Path')
def test_csv_reader_file_not_exists(mock_path_class):
    """Тест когда файл не существует"""
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path_class.return_value = mock_path

    from src.finance_parser import csv_reader

    result = csv_reader('/path/to/nonexistent.csv')

    assert result == []


@patch('pathlib.Path')
def test_csv_reader_file_not_exist(mock_path_class):
    """Тест когда файл не существует"""
    mock_path = MagicMock()
    mock_path.exists.return_value = False
    mock_path_class.return_value = mock_path

    from src.finance_parser import csv_reader

    result = csv_reader('/path/to/nonexistent.csv')

    assert result == []


@patch('pandas.read_excel')
@patch('pathlib.Path')
def test_xlsx_reader_success(mock_path_class, mock_read_excel):
    """Тест успешного чтения XLSX файла"""
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.stat.return_value.st_size = 100
    mock_path.name = 'test.xlsx'
    mock_path_class.return_value = mock_path

    mock_df = MagicMock()
    mock_df.astype.return_value = mock_df
    mock_df.to_dict.return_value = [{'col1': 'val1', 'col2': 'val2'}]
    mock_read_excel.return_value = mock_df

    from src.finance_parser import xlsx_reader

    result = xlsx_reader('/path/to/file.xlsx')

    assert result == [{'col1': 'val1', 'col2': 'val2'}]
    mock_read_excel.assert_called_once_with('/path/to/file.xlsx')
    mock_df.astype.assert_called_once_with(str)


@patch('pathlib.Path')
def test_xlsx_reader_file_not_exists(mock_path_class):
    """Тест когда файл XLSX не существует"""
    mock_path = MagicMock()
    mock_path.exists.return_value = False
    mock_path_class.return_value = mock_path

    from src.finance_parser import xlsx_reader

    result = xlsx_reader('/path/to/nonexistent.xlsx')

    assert result == []


@patch('pathlib.Path')
def test_xlsx_reader_empty_file(mock_path_class):
    """Тест когда файл XLSX существует но пустой"""
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.stat.return_value.st_size = 0
    mock_path_class.return_value = mock_path

    from src.finance_parser import xlsx_reader

    result = xlsx_reader('/path/to/empty.xlsx')

    assert result == []
