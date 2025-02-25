from typing import Dict
import queries as q
from math import ceil

months = {
    'January': 'Януари',
    'February': 'Февруари',
    'March': 'Март',
    'April': 'Април',
    'May': 'Май',
    'June': 'Юни',
    'July': 'Юли',
    'August': 'Август',
    'September': 'Септември',
    'October': 'Октомври',
    'November': 'Ноември',
    'December': 'Декември'
}


# TODO add report_table variable for the check_month_bill and the check_period_bill methods

# Decorator that adds description to functions
def describe(description):
    def decorator(func):
        func.description = description
        return func

    return decorator


class App:
    def __init__(self):
        """
        The dictionary is used to store the available functions of the app
        and their corresponding numbers in the menu. If a new function is added,
        it should be added to the dictionary as well.
        """
        self.available_choices: Dict = {
            1: self.add_month_summary_data,
            2: self.edit_month_summary,
            3: self.check_month_bill,
            4: self.check_year_bill,
            5: self.statistics
        }

    @describe('Добавяне на показания за месеца')
    def add_month_summary_data(self):
        report_date = input('Въведете дата на отчитане на електромера във формат ДД.ММ.ГГГГ: ')
        day_kwh = int(input('Въведете показанията на електромера за дневна тарифа: '))
        night_kwh = int(input('Въведете показанията на електромера за нощна тарифа: '))

        q.insert_in_main_data_table(report_date, day_kwh, night_kwh)
        return '\n' + ("#" * 42) + '\nПромените са запазени успешно!\n' + ("#" * 42) + '\n'

    @describe('Редактиране на отчет за избран месец')
    def edit_month_summary(self):
        pass

    @describe('Проверка на сметка за избран месец')
    def check_month_bill(self):
        """
        EN: Checks the bill for a given month and returns the report as print in the console
        or data for the GUI
        BG: Проверява сметката за избран месец и връща отчета като принт в конзолата
        или като данни за графичния интерфейс
        """
        year = int(input('Въведете година: '))
        month = int(input('Въведете месец: '))

        query = q.view_main_data_table_for_given_month(year, month)  # Returns a list of tuples

        if not query:
            return '\n' + ("#" * 42) + '\nНяма данни за избрания месец!\n' + ("#" * 42) + '\n'

        report_table = ('| {:^20} | {:^10} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |\n'
                        .format('Дата на отчитане', 'Месец', 'Дневни кВтч', 'Нощни кВтч', 'Дневна цена',
                                'Нощна цена', 'Общо кВтч', 'Обща цена'))
        report_table += '-' * 145 + '\n'

        report_date = query[0][0]
        month = months[query[0][1]]
        day_kwh = query[0][2]
        night_kwh = query[0][3]
        day_price = str(round(query[0][4] * query[0][6], 2)) + ' лв.'
        night_price = str(round(query[0][5] * query[0][7], 2)) + ' лв.'
        total_kwh = day_kwh + night_kwh
        total_price = str(round((query[0][4] * query[0][6]) + (query[0][5] * query[0][7]), 2)) + ' лв.'

        report_table += ('| {:^20} | {:^10} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |\n'
                         .format(report_date, month, day_kwh, night_kwh, day_price,
                                 night_price, total_kwh, total_price))
        report_data = [report_date, month, day_kwh, night_kwh, day_price, night_price, total_kwh, total_price]

        print(report_table)

        return report_data

    @describe('Проверка на сметки за избран период')
    def check_year_bill(self):
        year = int(input('Въведете година: '))

        query = q.view_main_data_table_for_given_year(year)  # Returns a list of tuples

        if not query:
            return '\n' + ("#" * 42) + '\nНяма данни за избраната година!\n' + ("#" * 42) + '\n'

        report_table = ('| {:^20} | {:^10} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |\n'
                        .format('Дата на отчитане', 'Месец', 'Дневни кВтч', 'Нощни кВтч', 'Дневна цена',
                                'Нощна цена', 'Общо кВтч', 'Обща цена'))
        report_table += '-' * 145 + '\n'

        previous_month_day_kwh, previous_month_night_kwh = q.get_previous_month_data(year)[0]

        for data in query:
            report_date = data[0]
            month = months[data[1]]
            day_kwh = data[2] - previous_month_day_kwh
            night_kwh = data[3] - previous_month_night_kwh
            day_price = str(round(data[4] * day_kwh, 2)) + ' лв.'
            night_price = str(round(data[5] * night_kwh, 2)) + ' лв.'
            total_kwh = day_kwh + night_kwh
            total_price = str(round(round((data[4] * day_kwh), 2) + round((data[5] * night_kwh), 2), 2)) + ' лв.'

            report_table += ('| {:^20} | {:^10} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |\n'
                             .format(report_date, month, day_kwh, night_kwh, day_price,
                                     night_price, total_kwh, total_price))

            previous_month_day_kwh = data[2]
            previous_month_night_kwh = data[3]

        print(report_table)

    @describe('Статистика за потребление на електроенергия')
    def statistics(self):
        pass
