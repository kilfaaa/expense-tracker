import os
import sys

import psycopg


def main():
    database_url = os.getenv("DATABASE_URL")
    if database_url is None:
        print("Не задана переменная окружения DATABASE_URL")
        return

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM categories;")
            rows = cur.fetchall()

    for category_id, name in rows:
        print(category_id, name)


if __name__ == "__main__":
    main()