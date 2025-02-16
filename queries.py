import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite')


def create_year_table(year: int):
    """"
    Създава таблица за годината и добавя въведената от потребителя година
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS year (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            )
    ''')

    conn.commit()

    cursor.execute(f'''
        INSERT INTO year (year)
        VALUES ({year})
    ''')

    conn.commit()


def insert_new_year(year: int):
    """
    Добавя въведената от потребителя година в таблицата за годината
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        INSERT INTO year (year)
        VALUES ({year})
    ''')

    conn.commit()


def create_price_table():
    """
    Създава таблица за цените за дневна и нощна тарифа
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_price REAL NOT NULL,
            night_price REAL NOT NULL,
            )
    ''')

    conn.commit()


def update_price_table(day_price: float, night_price: float):
    """
    Обновява цените за дневна и нощна тарифа
    """

    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        UPDATE price
        SET day_price = {day_price}, night_price = {night_price}
    ''')

    conn.commit()


def create_initial_data(day_kwhs, night_kwhs):
    """
    Създава таблица за началните данни, от които да стартират последващите изчисления
    и добавя данни в нея.
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS initial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_kwhs INTEGER NOT NULL,
            night_kwhs INTEGER NOT NULL,
            )
    ''')

    conn.commit()

    cursor.execute(f'''
        INSERT INTO initial_data (day_kwhs, night_kwhs)
        VALUES ({day_kwhs}, {night_kwhs})
    ''')

    conn.commit()


def create_main_data_table():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kwhs_report_date TEXT NOT NULL,
            day_kwhs INTEGER NOT NULL,
            night_kwhs INTEGER NOT NULL,
            year_id INTEGER NOT NULL,
            price_id INTEGER NOT NULL,
            FOREIGN KEY (year_id) REFERENCES year (id),
            FOREIGN KEY (price_id) REFERENCES price (id),
            )
    ''')


def check_if_year_table_exists():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    try:
        result = cursor.execute(f'''
            SELECT * FROM year
        ''')
    except sqlite3.OperationalError:
        result = None

    return result
