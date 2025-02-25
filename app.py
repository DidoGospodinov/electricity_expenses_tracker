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
            4: self.check_period_bill,
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
        year = int(input('Въведете година: '))
        month = int(input('Въведете месец: '))

        query = q.view_main_data_table_for_given_month(year, month) # Returns a list of tuples

        if not query:
            return '\n' + ("#" * 42) + '\nНяма данни за избрания месец!\n' + ("#" * 42) + '\n'

        result = '| {:^20} | {:^10} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |\n'.format('Дата на отчитане', 'Месец', 'Дневни кВтч', 'Нощни кВтч', 'Дневна цена', 'Нощна цена', 'Общо кВтч', 'Обща цена')
        result += '-' * 145 + '\n'
        # result = f'\n{"Дата на отчитане":^20}{"Месец":^10}{"Дневни кВтч":^15}{"Нощни кВтч":^15}{"Дневна цена":^15}{"Нощна цена":^15}\n'
        report_date = query[0][0]
        month = months[query[0][1]]
        day_kwh = query[0][2]
        night_kwh = query[0][3]
        day_price = str(round(query[0][4] * query[0][6], 2)) + ' лв.'
        night_price = str(round(query[0][5] * query[0][7], 2)) + ' лв.'
        total_kwh = day_kwh + night_kwh
        total_price = str(round((query[0][4] * query[0][6]) + (query[0][5] * query[0][7]), 2)) + ' лв.'
        # result += f'{report_date:<20}{month:<10}{day_kwh:<15}{night_kwh:<15}{day_price:<15}{night_price:<15}\n'
        result += '| {:^20} | {:^10} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |\n'.format(report_date, month, day_kwh, night_kwh, day_price, night_price, total_kwh, total_price)

        return result

    @describe('Проверка на сметки за избран период')
    def check_period_bill(self):
        pass

    @describe('Статистика за потребление на електроенергия')
    def statistics(self):
        pass

app = App()
print(app.check_month_bill())