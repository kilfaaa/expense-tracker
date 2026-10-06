# Expense Tracker

Консольный трекер личных расходов на Python и PostgreSQL.

## Назначение

Приложение хранит категории расходов и сами расходы в базе PostgreSQL.
Позволяет добавлять, просматривать, изменять и удалять расходы,
фильтровать их по категории и получать статистику: общую сумму
расходов и суммы по категориям.

## Структура проекта

```text
expense-tracker/
├── main.py                       # запуск приложения и меню
├── validation.py                 # проверка пользовательского ввода
├── models.py                     # класс Expense
├── repository.py                 # класс ExpenseRepository — доступ к PostgreSQL
├── schema.sql                    # структура базы данных
├── sql_practice.sql              # учебные SQL-запросы
├── requirements.txt
├── .github/workflows/tests.yml   # GitHub Actions: запуск тестов на push и pull request
└── tests/
    ├── test_validation.py        # тесты функций валидации
    └── test_models.py            # тесты класса Expense
```

## Системные требования

- Python 3.14+
- PostgreSQL 18.6

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/kilfaaa/expense-tracker.git
cd expense-tracker
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать базу данных

В PostgreSQL (например, через pgAdmin или psql) создай пустую базу:

```sql
CREATE DATABASE expense_tracker;
```

### 5. Применить схему

```bash
psql -U postgres -d expense_tracker -f schema.sql
```

Либо выполни содержимое `schema.sql` в Query Tool pgAdmin, открыв его
в базе `expense_tracker`.

### 6. Задать переменную окружения DATABASE_URL

```text
DATABASE_URL=postgresql://пользователь:пароль@localhost:5432/expense_tracker
```

В PyCharm: **Run → Edit Configurations → Environment variables**.
В терминале перед запуском: `export DATABASE_URL=...` (Linux/macOS)
или `set DATABASE_URL=...` (Windows).

### 7. Запустить приложение

```bash
python main.py
```

## Использование

При запуске появляется меню:

```text
1. Показать категории
2. Добавить категорию
3. Добавить расход
4. Показать расходы
5. Показать расходы выбранной категории
6. Изменить расход
7. Удалить расход
8. Показать общую сумму расходов
9. Показать суммы по категориям
0. Выход
```

Данные хранятся в PostgreSQL и сохраняются между запусками программы.

## Тесты

Юнит-тесты проверяют функции валидации (`validation.py`) и модель
`Expense` (`models.py`). Они не подключаются к базе данных и не
требуют пароля PostgreSQL — запускаются в полностью изолированном
окружении.

Запуск:

```bash
python -m pytest
```

Подробный вывод (список каждого теста):

```bash
python -m pytest -v
```

### Что проверяют тесты

- `validate_amount` — корректные суммы, суммы с запятой вместо точки,
  отклонение текста, нуля и отрицательных значений
- `validate_date` — корректная дата, отклонение неверного формата
- `validate_id` — корректный числовой ID, отклонение текста и других
  некорректных значений (с использованием `@pytest.mark.parametrize`)
- `validate_category_name` / `validate_description` — непустой текст,
  отклонение пустой строки
- `Expense` — хранение полей, значение `id` по умолчанию, сравнение
  объектов по значениям

### Continuous Integration

При каждом push и pull request GitHub Actions автоматически
устанавливает зависимости и запускает `python -m pytest`
(см. `.github/workflows/tests.yml`).
