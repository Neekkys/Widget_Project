from src.masks import get_mask_account, get_mask_card_number
from src.utils import extract_transaction_amount, unpacking_json_file


def main(number_card, number_acc):
    get_mask_account(number_acc)
    get_mask_card_number(number_card)

    transaction = unpacking_json_file("tests.json")
    extract_transaction_amount(transaction)

    return


main("555555555554444", 9999999999999999999)
