CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR (100) UNIQUE NOT NULL
);

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
	description TEXT NOT NULL,
	amount DECIMAL (18, 2) NOT NULL,
	category_id INTEGER NOT NULL,
	spent_at DATE NOT NULL,

	CONSTRAINT category_id_fk FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE RESTRICT,
	CONSTRAINT amount_positive CHECK (amount > 0)
);