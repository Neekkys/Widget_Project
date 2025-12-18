from src.config import BASE_DIR
from src.decorators import log
from src.finance_parser import csv_reader, xlsx_reader
from src.generators import filter_by_currency
from src.process_search_operation import process_bank_description
from src.processing import filter_by_state, sort_by_date
from src.utils import unpacking_json_file
from src.widget import get_date, mask_account_card


def ask_yes_no(question: str) -> bool:
    """Задает вопрос Да/Нет и возвращает True/False"""
    while True:
        answer = input(f"{question} (Да/Нет): ").lower().strip()
        if answer in [
            "да",
        ]:
            return True
        elif answer in [
            "нет",
        ]:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def filter_transaction(transaction_dict: dict) -> str:
    """Форматирует транзакции вывода для пользователя"""
    try:
        transaction_date = get_date(transaction_dict.get("date", ""))
    except (ValueError, TypeError):
        transaction_date = "Время неизвестно"

    transaction_description = transaction_dict.get("description", "Без описания")

    from_info = transaction_dict.get("from", "")
    to_info = transaction_dict.get("to", "")

    from_mask = mask_account_card(from_info) if from_info else ""
    to_mask = mask_account_card(to_info) if to_info else ""

    direction = f"{from_mask} -> {to_mask}" if from_mask else to_mask

    if "operationAmount" in transaction_dict:
        op_amount = transaction_dict["operationAmount"]
        amount = op_amount.get("amount", "Сумма неизвестна.")
        currency_name = op_amount.get("currency", {}).get("name", "Валюта неизвестна")
    else:
        amount = str(transaction_dict.get("amount", "Сумма неизвестна."))
        currency_name = transaction_dict.get("currency_name", "Валюта неизвестна")

    result = f"""{transaction_date} {transaction_description}
{direction}
Сумма: {amount} {currency_name}"""
    return result


@log("main.log")
def main():
    """Основная логика"""

    # Приветствуем пользователя, просим выбрать с каким файлом будем работать
    print(
        """Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:"""
    )
    while True:
        try:
            first_user_answer = int(
                input(
                    """1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла\n"""
                )
            )

            # Пользователь выбрал какой файл будет обрабатывать
            if 1 <= first_user_answer <= 3:
                if first_user_answer == 1:
                    print("Для обработки выбран JSON-файл")
                elif first_user_answer == 2:
                    print("Для обработки выбран CSV-файл")
                else:
                    print("Для обработки выбран XLSX-файл")
                break
            else:
                print(f"\nПункта {first_user_answer} не существует. Повторите попытку\n")

        except ValueError:
            print("\nОшибка! Введите число от 1 до 3.\n")

    # Просим выбрать статус по которому будем выполнять фильтрацию
    while True:
        second_user_answer = (
            input(
                """
Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"""
            )
            .upper()
            .strip()
        )
        if second_user_answer in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Операции отфильтрованы по статусу {second_user_answer}\n")
            break
        else:
            print(f'Статус операции "{second_user_answer}" недоступен.')

    # Пользователь ввел все необходимые данные для фильтрации. Теперь фильтруем по этим данным
    data_dir_csv = BASE_DIR.joinpath("data", "transactions.csv")
    data_dir_xlsx = BASE_DIR.joinpath("data", "transactions_excel.xlsx")
    if first_user_answer == 1:
        unpacked_file = unpacking_json_file("operations.json")
    elif first_user_answer == 2:
        unpacked_file = csv_reader(data_dir_csv)
    else:
        unpacked_file = xlsx_reader(data_dir_xlsx)

    filtered_file = filter_by_state(unpacked_file, second_user_answer)
    if not filtered_file:
        print(f"Не найдено ни одной транзакции со статусом {second_user_answer}")

    # Задаем у пользователя вопросы, какие ему нужны параметры сортировки

    # Сортировка по дате
    answer_sort_by_date = ask_yes_no("Отсортировать операции по дате?\n")

    # Уточняем в каком порядке будет сортировка, если выбрал сортировку по дате:
    reverse_by_date = True
    if answer_sort_by_date:
        while True:
            answer_sort_by_reverse = input("Отсортировать по возрастанию или по убыванию?\n").lower().strip()
            if answer_sort_by_reverse.split(" ")[-1] in ["возрастанию", "убыванию"]:
                if answer_sort_by_reverse.split(" ")[-1] == "возрастанию":
                    reverse_by_date = False
                else:
                    reverse_by_date = True
                break
            else:
                print("Такого варианта ответа нет")

    # Спрашиваем транзакции каких валют нужно выводить
    answer_rub_transactions = ask_yes_no("Выводить только рублевые транзакции?")

    # Спрашиваем нужно ли фильтровать по определенному слову в описании
    answer_filter_by_word = ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?")
    word_for_descriptions = ""
    if answer_filter_by_word:
        word_for_descriptions = input("Введите слово по которому нужно фильтровать: ").lower().strip()

    # Обрабатываем запрос пользователя

    # Фильтруем по дате
    if answer_sort_by_date:
        if reverse_by_date:  # <- Если True, то по убыванию (по умолчанию)
            filtered_file = sort_by_date(filtered_file)
        else:  # <- Если False, то по возрастанию
            filtered_file = sort_by_date(filtered_file, reverse_by_date)

    # Выводим только рублевые транзакции, если пользователь указал на это
    if answer_rub_transactions:
        filtered_file = list(filter_by_currency(filtered_file, "RUB"))

    # Фильтруем по определенному слову в описании
    if answer_filter_by_word:
        filtered_file = process_bank_description(filtered_file, word_for_descriptions)

    print("Распечатываю итоговый список транзакций...\n")

    if filtered_file:
        print(f"Всего банковских операций в выборке: {len(filtered_file)}\n")
        for transaction in filtered_file:
            print(f"{filter_transaction(transaction)}\n")
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == '__main__':
    main()
