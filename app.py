from typing import Dict
import queries as q


def describe(description):
    def decorator(func):
        func.description = description
        return func

    return decorator


class App:
    def __init__(self):
        self.available_choices: Dict = {
            1: self.add_month_data,
            2: self.edit_month_summary,
            3: self.check_month_bill,
            4: self.check_period_bill,
            5: self.statistics
        }

    @describe('Добавяне на показания за месеца')
    def add_month_data(self):
        report_date = input('Въведете дата на отчитане на електромера във формат ДД.ММ.ГГГГ: ')
        day_kwh = int(input('Въведете показанията на електромера за дневна тарифа: '))
        night_kwh = int(input('Въведете показанията на електромера за нощна тарифа: '))

        q.insert_in_main_data_table(report_date, day_kwh, night_kwh)
        return '\n' + ("#" * 42) + '\nПромените са запазени успешно!\n' + ("#" * 42) + '\n'

    @describe('Редактиране на отчет за избран месец')
    def edit_month_summary(self):
        # logic here
        return 'result'

    @describe('Проверка на сметка за избран месец')
    def check_month_bill(self):
        # logic here
        return 'result'

    @describe('Проверка на сметки за избран период')
    def check_period_bill(self):
        # logic here
        return 'result'

    @describe('Статистика за потребление на електроенергия')
    def statistics(self):
        # logic here
        return 'result'

