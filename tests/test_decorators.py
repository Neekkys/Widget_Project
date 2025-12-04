from src.config import BASE_DIR
from src.decorators import log


def test_log_success_without_file(capsys):
    @log()
    def add(a, b):
        return a + b

    add(2, 3)
    captured = capsys.readouterr()
    assert "add - ok" in captured.out
    assert "error" not in captured.out


def test_log_error_without_file(capsys):
    @log()
    def add(a, b):
        return a / b

    add(2, 0)
    captured = capsys.readouterr()
    assert "add - ok" not in captured.out
    assert "add error: ZeroDivisionError - division by zero" in captured.out


def test_log_error_without_file_type_error(capsys):
    @log()
    def add(a, b):
        return a / b

    add(2, "2")
    captured = capsys.readouterr()
    assert "add - ok" not in captured.out
    assert "error" in captured.out


def test_log_success_write_file():
    @log("test_log.txt")
    def success_test(a, b):
        return a / b

    success_test(2, 1)
    success_test(2, 2)

    base_dir = BASE_DIR.joinpath("data", "test_log.txt")
    assert base_dir.exists()

    content = base_dir.read_text()
    assert "success_test - ok" in content
    assert "error" not in content

    base_dir.unlink()


def test_log_not_success_write_file():
    @log("test_log.txt")
    def not_success_test(a, b):
        return a / b

    not_success_test(2, 0)
    not_success_test(2, "2")

    base_dir = BASE_DIR.joinpath("data", "test_log.txt")
    assert base_dir.exists()

    content = base_dir.read_text()
    assert "not_success_test - ok" not in content
    assert "error" in content

    base_dir.unlink()
