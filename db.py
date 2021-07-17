
import sqlite3
DATABASE_NAME = "products.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                productname TEXT NOT NULL,
				companyname VARCHAR(255) NOT NULL,
				rate REAL NOT NULL,
				mfgdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
