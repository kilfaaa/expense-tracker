-- 01. Добавить категории (5 запросов)
INSERT INTO categories (name) VALUES ('Продукты');
INSERT INTO categories (name) VALUES ('Транспорт');
INSERT INTO categories (name) VALUES ('Развлечения');
INSERT INTO categories (name) VALUES ('Дом');
INSERT INTO categories (name) VALUES ('Здоровье');

-- 02. Добавить расходы (10 запросов)
INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Проезд на троллейбусе', 40, 2, '2026-09-14');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Аквапарк', 2500, 3, '2026-09-15');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Диван', 10999.99, 4, '2026-09-10');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Витамины', 700, 5, '2026-09-12');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Магнит', 1404.45, 1, '2026-09-14');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Клуб симуляторов', 900, 3, '2026-09-16');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Табрис', 2708.56, 1, '2026-09-16');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Бензин на автомобиль', 3014.40, 2, '2026-09-14');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Магнит', 560, 1, '2026-09-14');

INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Оплата аренды квартиры', 30000, 4, '2026-09-14');

-- 03. Получить все расходы (5.2)
SELECT * FROM expenses;

-- 04. Получить только выбранные столбцы (5.2)
SELECT description, amount FROM expenses;

-- 05. Расходы дороже заданной суммы (5.3)
SELECT * FROM expenses
WHERE amount > 15000;

-- 06. Расходы выбранной категории (5.3)
SELECT * FROM expenses
WHERE category_id = 1;

-- 07. Ещё одно условие по своему выбору (5.3)
SELECT * FROM expenses
WHERE category_id = 1 AND amount > 1000;

-- 08. Отсортировать расходы от самого дорогого к самому дешёвому (5.4)
SELECT * FROM expenses
ORDER BY amount DESC;

-- 09. Получить три самых дорогих расхода (5.4)
SELECT * FROM expenses
ORDER BY amount DESC LIMIT 3;

-- 10. Изменить данные одного конкретного расхода по его id (5.5)
UPDATE expenses SET
description = 'Диван в прихожей'
WHERE id = 3;

-- 11. Удалить один конкретный расход по условию (5.6)
DELETE FROM expenses
WHERE id = 3;

-- 12. Получить расходы вместе с названиями категорий (5.7)
SELECT expenses.id, description, amount, categories.name, spent_at from expenses
JOIN categories on expenses.category_id = categories.id;

-- 13. Количество расходов через COUNT (5.8)
SELECT COUNT(*) FROM expenses;

-- 14. Общая сумма через SUM (5.8)
SELECT SUM(amount) FROM expenses;

-- 15. Средняя сумма через AVG (5.8)
SELECT AVG(amount) FROM expenses;

-- 16. Сумма расходов по каждой категории: JOIN + SUM + GROUP BY (5.9)
SELECT categories.name, SUM(amount) FROM expenses
JOIN categories ON category_id = categories.id
GROUP BY categories.name;

-- 17. Проверка внешнего ключа: категории с id = 999 нет, вставка должна завершиться ошибкой
INSERT INTO expenses (description, amount, category_id, spent_at)
VALUES ('Тест внешнего ключа', 100, 999, '2026-09-15');