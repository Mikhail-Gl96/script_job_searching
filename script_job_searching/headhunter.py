import requests


from custom_utils import get_average_rub_salary, get_vacancies_salary_info


HEADHUNTER_BASE_URL = 'https://api.hh.ru/'


def get_vacancies(text):
    url = f'{HEADHUNTER_BASE_URL}vacancies'
    one_month_period = '30'
    city = {
        'Moscow': '1'
    }

    payload = {
        'text': text,
        'area': city['Moscow'],
        'period': one_month_period
    }

    page = 0
    pages_number = 1
    vacancies = []
    response = None

    while page < pages_number:
        payload.update({'page': page})
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()

        pages_number = page_response.json()['pages']
        page += 1

        vacancies.extend(page_response.json()["items"])
        response = page_response.json()
    vacancies_amount = response['found']
    return vacancies.copy(), vacancies_amount


def get_average_rub_salary_hh(vacancy):
    salary_exists = True if vacancy['salary'] else False
    if salary_exists:
        salary = vacancy['salary']
        salary_currency = salary['currency']
        salary_from = salary['from']
        salary_to = salary['to']

        salary_info = {
            'currency': salary_currency,
            'from': salary_from,
            'to': salary_to,
            'salary_exists': salary_exists,
        }
    else:
        salary_info = {
            'salary_exists': salary_exists,
        }
    return salary_info


def get_vacancies_stats_hh(langs):
    langs_statistic = []
    for lang in langs:
        vacancies, vacancies_amount = get_vacancies(text=f"программист {lang}")
        vacancies_processed, average_salary = get_vacancies_salary_info(vacancies=vacancies,
                                                                        average_salary_func=get_average_rub_salary_hh)
        langs_statistic.append([lang, vacancies_amount, vacancies_processed, average_salary])
    return langs_statistic






