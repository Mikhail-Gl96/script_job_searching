import requests


from custom_utils import predict_rub_salary, get_vacancies_salary_info, create_pretty_table


SUPERJOB_BASE_URL = 'https://api.superjob.ru/2.0/'


def get_vacancies(text, secret_key):
    url = f'{SUPERJOB_BASE_URL}vacancies/'
    payload = {
        'catalogues': 48,
        'town': 'Москва',
        'keyword': text
    }
    headers = {
            'X-Api-App-Id': secret_key
    }

    page = 0
    more_pages = True
    response_objects = []
    response = None

    while more_pages:
        payload.update({'page': page})
        page_response = requests.get(url, params=payload, headers=headers)
        page_response.raise_for_status()

        more_pages = page_response.json()['more']
        page += 1

        response_objects.extend(page_response.json()["objects"])
        response = page_response.json()

    response['objects'] = response_objects
    return response


def predict_rub_salary_for_SuperJob(vacancy):
    salary_currency = vacancy['currency']
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']

    salary_exists = True if (salary_to or salary_from) else False

    if salary_exists:
        answer = {
            'currency': 'RUR' if salary_currency == 'rub' else None,
            'from': salary_from,
            'to': salary_to,
            'salary_exists': salary_exists,
        }
    else:
        answer = {
            'salary_exists': salary_exists,
        }
    return answer


def get_info_vacancies_by_lang_from_superjob(langs, secret_key):
    statistic_langs = []
    for lang in langs:
        temp_response = get_vacancies(text=f"{lang}", secret_key=secret_key)
        vacancies_salary_info = get_vacancies_salary_info(items=temp_response['objects'],
                                                          predict_salary_func=predict_rub_salary_for_SuperJob)
        vacancies_processed = vacancies_salary_info[0]
        average_salary = vacancies_salary_info[1]

        statistic_langs.append(tuple([lang, temp_response['total'], vacancies_processed, average_salary]))

    create_pretty_table(table_data=statistic_langs, title='SuperJob Vacancies Moscow')


