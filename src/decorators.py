from datetime import datetime
from functools import wraps

from src.config import BASE_DIR


def log(filename=None):
    """Декоратор, который записывает в указанный файл логи функции"""

    def _log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Время вызова, имя функции
            call_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            func_name = func.__name__
            try:
                result_func = func(*args, **kwargs)
                log_message = f"{call_time} - {func_name} - ok\n"
            except Exception as e:
                log_message = (
                    f"{call_time} - {func_name} error: {type(e).__name__} - {str(e)}. Inputs: {args}, {kwargs}\n"
                )
                result_func = None
            if filename:
                data_dir = BASE_DIR.joinpath("logs", filename)
                with open(data_dir, "a", encoding="UTF-8") as f:
                    f.write(log_message)
            else:
                print(log_message)
            return result_func

        return wrapper

    return _log
