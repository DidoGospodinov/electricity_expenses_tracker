import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite')


#####################################################################################
# Table Year                                                                        #
#####################################################################################
def create_year_table(calendar_year: int):
    """
    Създава таблица за годината и добавя въведената от потребителя година
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS year (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calendar_year INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        INSERT INTO year (calendar_year) VALUES (?)
    ''', (calendar_year,))

    conn.commit()


def update_year_table(year: int):
    """
    Добавя въведената от потребителя година в таблицата за годината
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        UPDATE year
        SET calendar_year = ?
    ''', (year,))

    conn.commit()


def get_year():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT calendar_year FROM year
    ''')

    return cursor.fetchone()[0]


######################################################################################
######################################################################################
# Table Price                                                                        #
######################################################################################
def create_price_table(day_price, night_price):
    """
    EN: Creates a table for day and night tariff prices
    BG: Създава таблица за цените за дневна и нощна тарифа
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_price REAL NOT NULL,
            night_price REAL NOT NULL
            )
    ''')

    conn.commit()

    cursor.execute('''
        INSERT INTO price (day_price, night_price)
        VALUES (?, ?)
    ''', (day_price, night_price))

    conn.commit()


def update_price_table(day_price: float, night_price: float):
    """
    EN: Updates the day and night tariff prices
    BG: Обновява цените за дневна и нощна тарифа
    """

    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        UPDATE price
        SET day_price = ?, night_price = ?
    ''', (day_price, night_price))

    conn.commit()


def get_price():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    result = cursor.execute('''
        SELECT day_price, night_price
        FROM price
    ''')

    return result.fetchall()


######################################################################################
######################################################################################
# Table Main Data                                                                    #
######################################################################################

def create_main_data_table():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kwh_report_date TEXT NOT NULL,
            day_kwh INTEGER NOT NULL,
            night_kwh INTEGER NOT NULL,
            current_year INTEGER NOT NULL,
            day_price INTEGER NOT NULL,
            night_price INTEGER NOT NULL
            )
    ''')

    conn.commit()


def insert_in_main_data_table(kwh_report_date, day_kwh, night_kwh):
    current_year = get_year()
    day_price, night_price = get_price()[0]

    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO main_data (kwh_report_date, day_kwh, night_kwh, current_year, day_price, night_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (kwh_report_date, day_kwh, night_kwh, current_year, day_price, night_price))

    conn.commit()


######################################################################################

def create_initial_data(day_kwhs, night_kwhs):
    """
    EN: Creates a table for the initial data from which subsequent calculations will start
    and inserts data into it.
    BG: Създава таблица за началните данни, от които да стартират последващите изчисления
    и добавя данни в нея.
    """
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS initial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_kwhs INTEGER NOT NULL,
            night_kwhs INTEGER NOT NULL
            )
    ''')

    conn.commit()

    cursor.execute(f'''
        INSERT INTO initial_data (day_kwhs, night_kwhs)
        VALUES (?, ?)
    ''', (day_kwhs, night_kwhs))

    conn.commit()


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
