import os

import psycopg

from models import Expense
from repository import ExpenseRepository
from validation import (
    validate_category_name,
    validate_description,
    validate_amount,
    validate_date,
    validate_id,
)



def show_category(repo):
    for category_id, name in repo.get_all_categories():
        print(category_id, name)


def add_category(repo):
    category_name = input("Введите название категории: ")
    try:
        category_name = validate_category_name(category_name)
    except ValueError as error:
        print(f"\nОшибка: {error}\n")
        return

    try:
        repo.add_category(category_name)
    except psycopg.errors.UniqueViolation:
        repo.conn.rollback()
        print("\nОшибка: такая категория уже существует.\n")
        return

    print(f"\nКатегория «{category_name}» добавлена.\n")


def add_expense(repo):
    description_text = input("\nВведите описание расхода: ")
    try:
        expense_description = validate_description(description_text)
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return

    amount_text = input("Введите потраченную сумму: ")
    try:
        expense_amount = validate_amount(amount_text)
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return

    print()
    show_category(repo)
    category_text = input("Выберите номер категории расхода: ")
    try:
        category_id = validate_id(category_text)
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return

    date_text = input("Введите дату расхода в формате ГГГГ-ММ-ДД: ")
    try:
        spent_at = validate_date(date_text)
    except ValueError as error:
        print(f"\nОшибка: {error}\n")
        return

    expense = Expense(expense_description, expense_amount, category_id, spent_at)

    try:
        repo.add_expense(expense)
    except psycopg.errors.ForeignKeyViolation:
        repo.conn.rollback()
        print(f"\nОшибка: категории с номером {category_id} не существует.\n")
        return

    print(f"\nРасход «{expense_description}» на сумму {expense_amount} добавлен.\n")

def print_expenses(rows):
    for expense_id, description, amount, category_name, spent_at in rows:
        print(f"Номер {expense_id}. {description}, {amount}, {category_name}, {spent_at}")


def show_expenses(repo):
    rows = repo.get_all_expenses()

    if not rows:
        print("\nСписок расходов пуст.\n")
        return

    print_expenses(rows)


def show_expenses_in_category(repo):
    print()
    show_category(repo)
    category_text = input("Выберите номер категории: ")
    try:
        category_id = validate_id(category_text)
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return

    if not repo.category_exists(category_id):
        print(f"\nОшибка: категории с номером {category_id} не существует.\n")
        return

    rows = repo.get_expenses_by_category(category_id)

    if not rows:
        print("\nВ этой категории пока нет расходов.\n")
        return

    print_expenses(rows)

def change_expense(repo):
    print()
    show_expenses(repo)
    expense_text = input("Введите номер расхода, который хотите изменить: ")
    try:
        expense_id = validate_id(expense_text)
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return

    current = repo.get_expense_by_id(expense_id)

    if current is None:
        print(f"\nРасход с номером {expense_id} не найден.\n")
        return

    old_description, old_amount, old_category_id, old_spent_at = current

    description_text = input(
        f"Описание [{old_description}] (Enter — оставить без изменений): "
    )
    new_description = old_description
    if description_text.strip():
        try:
            new_description = validate_description(description_text)
        except ValueError as e:
            print(f"\nОшибка: {e}\n")
            return

    amount_text = input(
        f"Сумма [{old_amount}] (Enter — оставить без изменений): "
    )
    new_amount = old_amount
    if amount_text.strip():
        try:
            new_amount = validate_amount(amount_text)
        except ValueError as e:
            print(f"\nОшибка: {e}\n")
            return

    print()
    show_category(repo)
    category_text = input(
        f"Номер категории [{old_category_id}] (Enter — оставить без изменений): "
    )
    new_category_id = old_category_id
    if category_text.strip():
        try:
            new_category_id = validate_id(category_text)
        except ValueError as e:
            print(f"\nОшибка: {e}\n")
            return

    date_text = input(
        f"Дата [{old_spent_at}] (Enter — оставить без изменений): "
    )
    new_spent_at = old_spent_at
    if date_text.strip():
        try:
            new_spent_at = validate_date(date_text)
        except ValueError as e:
            print(f"\nОшибка: {e}\n")
            return

    updated_expense = Expense(new_description, new_amount, new_category_id, new_spent_at)

    try:
        updated_count = repo.update_expense(expense_id, updated_expense)
    except psycopg.errors.ForeignKeyViolation:
        repo.conn.rollback()
        print(f"\nОшибка: категории с номером {new_category_id} не существует.\n")
        return

    if updated_count == 0:
        print(f"\nРасход с номером {expense_id} не найден.\n")
        return

    print(f"\nРасход {expense_id} обновлён.\n")

def delete_expense(repo):
    print()
    show_expenses(repo)
    expense_text = input("Введите номер расхода, который хотите удалить: ")
    try:
        expense_id = validate_id(expense_text)
    except ValueError as e:
        print(f"\nОшибка: {e}\n")
        return
    deleted_count = repo.delete_expense(expense_id)

    if deleted_count == 0:
        print(f"\nРасход с номером {expense_id} не найден.\n")
        return

    print(f"\nРасход {expense_id} удалён.\n")


def show_expenses_sum(repo):
    total = repo.get_total_sum()

    if total is None:
        print("\nСписок расходов пуст, сумма отсутствует.\n")
        return

    print(f"\nОбщая сумма расходов: {total}\n")


def show_category_sum(repo):
    rows = repo.get_sum_by_category()

    if not rows:
        print("\nСписок расходов пуст.\n")
        return

    print()
    for category_name, total in rows:
        print(f"{category_name}: {total}")
    print()


def main():
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        print("Не задана переменная окружения DATABASE_URL")
        return

    try:
        with psycopg.connect(database_url) as conn:
            repo = ExpenseRepository(conn)
            while True:
                print("=== Expense - tracker ==="
                      "\n1. Показать категории"
                      "\n2. Добавить категорию"
                      "\n3. Добавить расход"
                      "\n4. Показать расходы"
                      "\n5. Показать расходы выбранной категории"
                      "\n6. Изменить расход"
                      "\n7. Удалить расход"
                      "\n8. Показать общую сумму расходов"
                      "\n9. Показать суммы по категориям"
                      "\n0. Выход")

                choice = input("Выберите пункт: ")
                if choice.isdigit() and 0 <= int(choice) <= 9:
                    if choice == "0":
                        break
                    elif choice == "1":
                        show_category(repo)
                    elif choice == "2":
                        add_category(repo)
                    elif choice == "3":
                        add_expense(repo)
                    elif choice == "4":
                        show_expenses(repo)
                    elif choice == "5":
                        show_expenses_in_category(repo)
                    elif choice == "6":
                        change_expense(repo)
                    elif choice == "7":
                        delete_expense(repo)
                    elif choice == "8":
                        show_expenses_sum(repo)
                    elif choice == "9":
                        show_category_sum(repo)
                else:
                    print("\nОшибка: введите число от 0 до 9.\n")
    except psycopg.OperationalError:
        print("\nНе удалось подключиться к базе данных. Проверьте, что PostgreSQL запущен.\n")


if __name__ == "__main__":
    main()