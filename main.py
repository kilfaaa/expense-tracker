import os

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
            cur.execute("INSERT INTO categories (name) VALUES (%s);", (category_name,),)
        conn.commit()
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        print("\nОшибка: такая категория уже существует.\n")
        return

    print(f"\nКатегория «{category_name}» добавлена.\n")


def add_expense(conn):
    print ("в разработке")

def  show_expenses(conn):
    print ("в разработке")

def show_expenses_in_category(conn):
    print ("in process")

def  change_expense(conn):
    print ("in process")

def  delete_expense(conn):
    print ("in process")

def show_expenses_sum(conn):
    print ("in process")

def show_category_sum(conn):
    print ("in process")

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
                  "\n8. ППоказать общую сумму расходов"
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