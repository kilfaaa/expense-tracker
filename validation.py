from decimal import Decimal, InvalidOperation
import datetime

def validate_category_name(name):
    name = name.strip()
    if not name:
        raise ValueError("Название категории не может быть пустым")
    return name

def validate_description(description):
    description = description.strip()
    if not description:
        raise ValueError("Описание расхода не может быть пустым")
    return description

def validate_amount(text):
    text = text.strip().replace(",", ".")
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValueError("Сумма должна быть числом.")

    if not amount.is_finite() or amount <= 0:
        raise ValueError("Сумма должна быть больше нуля.")
    return amount

def validate_date(text):
    text = text.strip()
    try:
        spent_text = datetime.datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Неверный формат или несуществующая дата (ГГГГ-ММ-ДД).")
    return spent_text

def validate_id(text):
    text = text.strip()
    if not text.isdigit():
        raise ValueError("Номер должен быть числом.")
    return int(text)

