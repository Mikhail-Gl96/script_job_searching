import requests


from custom_utils import get_average_rub_salary, get_vacancies_salary_info


SUPERJOB_BASE_URL = 'https://api.superjob.ru/2.0/'


def get_vacancies(text, secret_key, catalogues, city='Москва'):
    url = f'{SUPERJOB_BASE_URL}vacancies/'

    payload = {
        'catalogues': catalogues,
        'town': city,
        'keyword': text
    }
    headers = {
            'X-Api-App-Id': secret_key
    }

    page = 0
    more_pages = True
    vacancies = []
    response = None

    while more_pages:
        payload.update({'page': page})
        page_response = requests.get(url, params=payload, headers=headers)
        page_response.raise_for_status()

        more_pages = page_response.json()['more']
        page += 1

        vacancies.extend(page_response.json()["objects"])
        response = page_response.json()
    vacancies_amount = response['total']
    return vacancies.copy(), vacancies_amount


def get_average_rub_salary_sj(vacancy):
    salary_currency = vacancy['currency']
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']

    salary_exists = True if (salary_to or salary_from) else False

    if salary_exists:
        salary_info = {
            'currency': 'RUR' if salary_currency == 'rub' else None,
            'from': salary_from,
            'to': salary_to,
            'salary_exists': salary_exists,
        }
    else:
        salary_info = {
            'salary_exists': salary_exists,
        }
    return salary_info


def get_vacancies_stats_sj(langs, secret_key, catalogues=48, city='Москва'):
    # catalogues - "Разработка, программирование": 48
    langs_statistic = []
    for lang in langs:
        vacancies, vacancies_amount = get_vacancies(text=f"{lang}", secret_key=secret_key,
                                                    catalogues=catalogues, city=city)
        vacancies_processed, average_salary = \
            get_vacancies_salary_info(vacancies=vacancies,
                                      average_salary_func=get_average_rub_salary_sj)
        langs_statistic.append([lang, vacancies_amount, vacancies_processed, average_salary])
    return langs_statistic


