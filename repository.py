class ExpenseRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all_categories(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM categories ORDER BY id;")
            return cur.fetchall()

    def add_category(self, name):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO categories (name) VALUES (%s);", (name,))
        self.conn.commit()

    def category_exists(self, category_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM categories WHERE id = %s;", (category_id,))
            return cur.fetchone() is not None

    def get_all_expenses(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT expenses.id, description, amount, categories.name, spent_at "
                "FROM expenses "
                "JOIN categories ON expenses.category_id = categories.id "
                "ORDER BY expenses.id;"
            )
            return cur.fetchall()

    def get_expenses_by_category(self, category_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT expenses.id, description, amount, categories.name, spent_at "
                "FROM expenses "
                "JOIN categories ON expenses.category_id = categories.id "
                "WHERE expenses.category_id = %s "
                "ORDER BY expenses.id;",
                (category_id,),
            )
            return cur.fetchall()

    def get_expense_by_id(self, expense_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT description, amount, category_id, spent_at FROM expenses WHERE id = %s;",
                (expense_id,),
            )
            return cur.fetchone()

    def add_expense(self, expense):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO expenses (description, amount, category_id, spent_at) "
                "VALUES (%s, %s, %s, %s);",
                (expense.description, expense.amount, expense.category_id, expense.spent_at),
            )
        self.conn.commit()

    def update_expense(self, expense_id, expense):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE expenses "
                "SET description = %s, amount = %s, category_id = %s, spent_at = %s "
                "WHERE id = %s;",
                (expense.description, expense.amount, expense.category_id, expense.spent_at, expense_id),
            )
            updated_count = cur.rowcount
        self.conn.commit()
        return updated_count

    def delete_expense(self, expense_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM expenses WHERE id = %s;", (expense_id,))
            deleted_count = cur.rowcount
        self.conn.commit()
        return deleted_count

    def get_total_sum(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT SUM(amount) FROM expenses;")
            return cur.fetchone()[0]

    def get_sum_by_category(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT categories.name, SUM(amount) "
                "FROM expenses "
                "JOIN categories ON expenses.category_id = categories.id "
                "GROUP BY categories.name "
                "ORDER BY categories.name;"
            )
            return cur.fetchall()
