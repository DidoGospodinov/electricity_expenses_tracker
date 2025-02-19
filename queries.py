import os
import sqlite3
import calendar

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
# Table Initial Data                                                                 #
######################################################################################
def create_initial_data(day_kwh, night_kwh):
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

    # TODO: correct the name of the columns!!!
    cursor.execute(f'''
        INSERT INTO initial_data (day_kwhs, night_kwhs)
        VALUES (?, ?)
    ''', (day_kwh, night_kwh))

    conn.commit()

def get_initial_data():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # TODO: correct the name of the columns!!!
    result = cursor.execute('''
        SELECT day_kwhs, night_kwhs
        FROM initial_data
    ''')

    return result.fetchall()

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
            month TEXT NOT NULL,
            day_kwh INTEGER NOT NULL,
            night_kwh INTEGER NOT NULL,
            current_year INTEGER NOT NULL,
            day_price INTEGER NOT NULL,
            night_price INTEGER NOT NULL
            )
    ''')

    conn.commit()



def update_main_data_table(report_id: int, kwh_report_date: str, day_kwh: int, night_kwh: int):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'''
        UPDATE main_data
        SET kwh_report_date = ?, day_kwh = ?, night_kwh = ?
        WHERE id = ?
    ''', (kwh_report_date, day_kwh, night_kwh, report_id))

    conn.commit()


def insert_in_main_data_table(kwh_report_date, day_kwh, night_kwh):
    current_year = get_year()
    day_price, night_price = get_price()[0]
    correct_month = int(kwh_report_date.split('-')[1]) - 1 if int(kwh_report_date.split('-')[1]) > 1 else 12
    month = calendar.month_name[correct_month]


    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO main_data (kwh_report_date, month, day_kwh, night_kwh, current_year, day_price, night_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (kwh_report_date, month, day_kwh, night_kwh, current_year, day_price, night_price))

    conn.commit()


def view_main_data_table_for_given_year(year):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    result = cursor.execute('''
        SELECT id, kwh_report_date, day_kwh, night_kwh
        FROM main_data
        WHERE current_year = ?
    ''', (year,))

    return result.fetchall()

def get_previous_month_data(year, month):
    if month == 1:
        year -= 1
        month = 12

    month_name = calendar.month_name[month]

    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    result = cursor.execute('''
        SELECT day_kwh, night_kwh
        FROM main_data
        WHERE current_year = ? AND month = ?
    ''', (year, month_name))
    print(result.fetchall())
    if not result.fetchall():
        result = get_initial_data()

    return result




def view_main_data_table_for_given_month(year: int, month: int):
    month_name = calendar.month_name[month]
    previous_month_day_kwh, previous_month_night_kwh = get_previous_month_data(year, month)[0]

    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    result = cursor.execute(f'''
        SELECT
            kwh_report_date,
            month,
            day_kwh,
            night_kwh,
            day_kwh - {previous_month_day_kwh} * day_price,
            night_kwh - {previous_month_night_kwh} * night_price
        FROM main_data
        WHERE current_year = ? AND month = ?
    ''', (year, month_name))

    return result.fetchall()

print(view_main_data_table_for_given_month(2025, 1))


######################################################################################


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
