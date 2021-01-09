from terminaltables import AsciiTable


def get_average_rub_salary(salary):
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
        predicted_salary = None
    return predicted_salary


def get_vacancies_salary_info(vacancies, average_salary_func):
    salaries = []
    for vacancy in vacancies:
        temp_salary = get_average_rub_salary(average_salary_func(vacancy))
        if temp_salary:
            salaries.append(temp_salary)
    vacancies_processed = len(salaries)
    if not vacancies_processed:
        salary = None
    else:
        salary = int(sum(salaries) / vacancies_processed)
    return vacancies_processed, salary


def create_pretty_table(table_data, title):
    table = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    table.extend(table_data)
    table_data = [i for i in table]
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
