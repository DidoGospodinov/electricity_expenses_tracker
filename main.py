import queries as q
from app import App


def main():
    if q.check_if_year_table_exists() is None:
        """
        EN: Checks if the application is started for the first time and if not,
        requires the user to enter the year and prices for day and night tariffs,
        then creates a table with initial data for the consumed kilowatts during the day
        and night and finally creates tables for the year and tariffs.
        
        BG: Проверява дали приложението е стартирано за първи път и ако не е,
        изисква от потребителя да въведе година и цените за дневна и нощна тарифа,
        след това създава таблица с първоначалните данни за изразходваните киловати през деня и нощта
        и накрая създава таблиците за годината и за тарифите.
        """
        try:
            year = int(input('За да започнете да използвате приложението, въведете година: '))
            day_price = float(input('Въведете цена за дневна тарифа: '))
            night_price = float(input('Въведете цена за нощна тарифа: '))
            initial_day_kwh = int(input('Въведете начална стойност на дневните показания на електромера: '))
            initial_night_kwh = int(input('Въведете начална стойност на нощните показания на електромера: '))

            q.create_initial_data(initial_day_kwh, initial_night_kwh)
            q.create_year_table(year)
            q.create_price_table(day_price, night_price)
            q.create_main_data_table()

        except ValueError:
            print('Въведените данни са невалидни!\nИзползвайте само числа при въвеждането на годината,'
                  ' цените за тарифите и началните стойности на дневните и нощните показания на електромера!')
            input('Натиснете Enter, за да започнете отначало...')
            return main()

    app = App()

    # Creates and visualizes the menu. The for loop iterates through the available options for the app and prints them.
    print('Изберете опция от менюто:\n')
    for key, value in app.available_choices.items():
        print(f"[{key}] {value.description}")
    print(f'[{len(app.available_choices) + 1}] Изход')

    while True:
        try:
            choice = int(input())
            if choice == len(app.available_choices) + 1:
                break
            elif 1 <= choice <= len(app.available_choices):
                print(app.available_choices[choice]())
            else:
                print(('#' * 42) + '\nЗа да продължите въведете число от 1 до 6!\n' + ('#' * 42) + '\n')
        except ValueError:
            print(('#' * 42) + '\nЗа да продължите въведете число от 1 до 6!\n' + ('#' * 42) + '\n')

        return main()


if __name__ == '__main__':
    main()
