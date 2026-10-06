from models import Expense
from decimal import Decimal
from datetime import date

def test_expense_field():
    expense = Expense("Проезд", Decimal("50.45"), 2, date(2020, 9, 14))
    assert expense.description ==  "Проезд"
    assert expense.amount == Decimal("50.45")
    assert expense.category_id == 2
    assert expense.spent_at == date(2020, 9, 14)

def test_expense_without_id():
    expense = Expense("Проезд", Decimal("50.45"), 2, date(2020, 9, 14))
    assert expense.id is None

def test_expense_with_id():
    expense = Expense("Проезд", Decimal("50.45"), 2, date(2020, 9, 14), id=5)
    assert expense.id == 5

def test_two_expenses_with_same_data_are_equal():
    e1 = Expense("Такси", Decimal("430.00"), 2, date(2026, 9, 16))
    e2 = Expense("Такси", Decimal("430.00"), 2, date(2026, 9, 16))
    assert e1 == e2

def test_expense_with_different_data_are_not_equal():
    e1 = Expense("Такси", Decimal("450.00"), 2, date(2025, 9, 16))
    e2 = Expense("Пирог", Decimal("430.00"), 1, date(2026, 9, 16))
    assert e1 != e2


