from src.masks import get_mask_account, get_mask_card_number

card_number = "1234567890987654"
account_number = "12345678901234567890"

print(get_mask_card_number(card_number))
print(get_mask_account(account_number))
