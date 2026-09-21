import datetime
import os
from decimal import Decimal, InvalidOperation

import psycopg


def show_category(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM categories ORDER BY id;")
        for category_id, name in cur.fetchall():
            print(category_id, name)


def add_category(conn):
    category_name = input("Введите название категории: ").strip()
    if not category_name:
        print("\nОшибка: название категории не может быть пустым.\n")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO categories (name) VALUES (%s);", (category_name,))
        conn.commit()
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        print("\nОшибка: такая категория уже существует.\n")
        return

    print(f"\nКатегория «{category_name}» добавлена.\n")


def add_expense(conn):
    expense_description = input("\nВведите описание расхода: ").strip()
    if not expense_description:
        print("\nОшибка: описание расхода не может быть пустым.\n")
        return

    amount_text = input("Введите потраченную сумму: ").strip().replace(",", ".")
    try:
        expense_amount = Decimal(amount_text)
    except InvalidOperation:
        print("\nОшибка: сумма должна быть числом.\n")
        return

    if not expense_amount.is_finite() or expense_amount <= 0:
        print("\nОшибка: сумма должна быть больше нуля.\n")
        return

    print()
    show_category(conn)
    category_text = input("Выберите номер категории расхода: ").strip()
    if not category_text.isdigit():
        print("\nОшибка: номер категории должен быть числом.\n")
        return
    category_id = int(category_text)

    date_text = input("Введите дату расхода в формате ГГГГ-ММ-ДД: ").strip()
    try:
        spent_at = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        print("\nОшибка: неверный формат или несуществующая дата (ГГГГ-ММ-ДД).\n")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO expenses (description, amount, category_id, spent_at) "
                "VALUES (%s, %s, %s, %s);",
                (expense_description, expense_amount, category_id, spent_at),
            )
        conn.commit()
    except psycopg.errors.ForeignKeyViolation:
        conn.rollback()
        print(f"\nОшибка: категории с номером {category_id} не существует.\n")
        return

    print(f"\nРасход «{expense_description}» на сумму {expense_amount} добавлен.\n")


def print_expenses(rows):
    for expense_id, description, amount, category_name, spent_at in rows:
        print(f"Номер {expense_id}. {description}, {amount}, {category_name}, {spent_at}")


def show_expenses(conn):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT expenses.id, description, amount, categories.name, spent_at "
            "FROM expenses "
            "JOIN categories ON expenses.category_id = categories.id "
            "ORDER BY expenses.id;"
        )
        rows = cur.fetchall()

    if not rows:
        print("\nСписок расходов пуст.\n")
        return

    print_expenses(rows)


def show_expenses_in_category(conn):
    print()
    show_category(conn)
    category_text = input("Выберите номер категории: ").strip()
    if not category_text.isdigit():
        print("\nОшибка: номер категории должен быть числом.\n")
        return
    category_id = int(category_text)

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM categories WHERE id = %s;", (category_id,))
        if cur.fetchone() is None:
            print(f"\nОшибка: категории с номером {category_id} не существует.\n")
            return

        cur.execute(
            "SELECT expenses.id, description, amount, categories.name, spent_at "
            "FROM expenses "
            "JOIN categories ON expenses.category_id = categories.id "
            "WHERE expenses.category_id = %s "
            "ORDER BY expenses.id;",
            (category_id,),
        )
        rows = cur.fetchall()

    if not rows:
        print("\nВ этой категории пока нет расходов.\n")
        return

    print_expenses(rows)


def change_expense(conn):
    print("в разработке")


def delete_expense(conn):
    print("в разработке")


def show_expenses_sum(conn):
    print("в разработке")


def show_category_sum(conn):
    print("в разработке")


def main():
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        print("Не задана переменная окружения DATABASE_URL")
        return

    with psycopg.connect(database_url) as conn:
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
                    show_category(conn)
                elif choice == "2":
                    add_category(conn)
                elif choice == "3":
                    add_expense(conn)
                elif choice == "4":
                    show_expenses(conn)
                elif choice == "5":
                    show_expenses_in_category(conn)
                elif choice == "6":
                    change_expense(conn)
                elif choice == "7":
                    delete_expense(conn)
                elif choice == "8":
                    show_expenses_sum(conn)
                elif choice == "9":
                    show_category_sum(conn)
            else:
                print("\nОшибка: введите число от 0 до 9.\n")


if __name__ == "__main__":
    main()