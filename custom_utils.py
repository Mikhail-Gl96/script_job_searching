from __future__ import print_function
from terminaltables import AsciiTable


def predict_rub_salary(salary):
    if not salary['salary_exists']:
        return None

    salary_from = salary['from']
    salary_to = salary['to']

    if salary['currency'] != 'RUR':
        return None

    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        predicted_salary = salary_from * 1.2
    elif not salary_from and salary_to:
        predicted_salary = salary_to * 0.8
    else:
        return None

    return predicted_salary


def get_vacancies_salary_info(items, predict_salary_func):
    salaries = []
    for i in items:
        temp_salary = predict_rub_salary(predict_salary_func(i))
        if temp_salary:
            salaries.append(temp_salary)
    vacancies_processed = len(salaries)
    if not vacancies_processed:
        answer = [vacancies_processed, None]
    else:
        salary = int(sum(salaries) / vacancies_processed)
        answer = [vacancies_processed, salary]
    return answer.copy()


def create_pretty_table(table_data, title):
    table = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    table.extend(table_data)
    TABLE_DATA = tuple([i for i in table])
    table_instance = AsciiTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()
