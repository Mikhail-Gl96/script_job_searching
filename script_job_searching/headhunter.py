import requests


from custom_utils import predict_rub_salary, get_vacancies_salary_info, create_pretty_table


HEADHUNTER_BASE_URL = 'https://api.hh.ru/'


def get_vacancies(text):
    url = f'{HEADHUNTER_BASE_URL}vacancies'

    payload = {
        'text': text,
        'area': '1',
        'period': '30'
    }

    page = 0
    pages_number = 1
    response_items = []
    response = None

    while page < pages_number:
        payload.update({'page': page})
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()

        pages_number = page_response.json()['pages']
        page += 1

        response_items.extend(page_response.json()["items"])
        response = page_response.json()

    response['items'] = response_items
    return response


def predict_rub_salary_hh(vacancy):
    salary_exists = True if vacancy['salary'] else False
    if salary_exists:
        salary = vacancy['salary']
        salary_currency = salary['currency']
        salary_from = salary['from']
        salary_to = salary['to']

        answer = {
            'currency': salary_currency,
            'from': salary_from,
            'to': salary_to,
            'salary_exists': salary_exists,
        }
    else:
        answer = {
            'salary_exists': salary_exists,
        }
    return answer


def get_info_vacancies_by_lang_from_headhunter(langs):
    statistic_langs = []
    for lang in langs:
        temp_response = get_vacancies(text=f"программист {lang}")
        vacancies_salary_info = get_vacancies_salary_info(items=temp_response['items'],
                                                          predict_salary_func=predict_rub_salary_hh)
        vacancies_processed = vacancies_salary_info[0]
        average_salary = vacancies_salary_info[1]

        statistic_langs.append(tuple([lang, temp_response['found'], vacancies_processed, average_salary]))

    table = create_pretty_table(table_data=statistic_langs, title='HeadHunter Vacancies Moscow')
    return table






