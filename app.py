from typing import Dict
import queries as q

months = {
    1: {'01': 'Януари'},
    2: {'02': 'Февруари'},
    3: {'03': 'Март'},
    4: {'04': 'Април'},
    5: {'05': 'Май'},
    6: {'06': 'Юни'},
    7: {'07': 'Юли'},
    8: {'08': 'Август'},
    9: {'09': 'Септември'},
    10: {'10': 'Октомври'},
    11: {'11': 'Ноември'},
    12: {'12': 'Декември'}
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
        pass

    @describe('Проверка на сметки за избран период')
    def check_period_bill(self):
        pass

    @describe('Статистика за потребление на електроенергия')
    def statistics(self):
        pass
