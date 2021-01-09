import os
import dotenv

from superjob import get_vacancies_stats_sj
from headhunter import get_vacancies_stats_hh
from custom_utils import create_pretty_table


if __name__ == "__main__":
    dotenv.load_dotenv()

    superjob_secret_key = os.getenv('SUPERJOB_SECRET_KEY')

    langs = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift']

    # city - 'Moscow': '1'
    # period - one_month_period: '30'
    hh_vacancies_stats = get_vacancies_stats_hh(langs=langs, city=1, period=30)

    hh_salary_table = create_pretty_table(table_data=hh_vacancies_stats, title='HeadHunter Vacancies Moscow')
    print(hh_salary_table)
    print()

    # catalogues - "Разработка, программирование": 48
    sj_salary_table = get_vacancies_stats_sj(langs=langs, secret_key=superjob_secret_key, catalogues=48, city='Москва')
    sj_salary_table = create_pretty_table(table_data=sj_salary_table, title='SuperJob Vacancies Moscow')
    print(sj_salary_table)
    print()

