import os
import dotenv

from superjob import get_info_vacancies_by_lang_from_superjob
from headhunter import get_info_vacancies_by_lang_from_headhunter


if __name__ == "__main__":
    dotenv.load_dotenv()

    superjob_secret_key = os.getenv('SUPERJOB_SECRET_KEY')

    langs = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift']

    get_info_vacancies_by_lang_from_headhunter(langs=langs)

    get_info_vacancies_by_lang_from_superjob(langs=langs, secret_key=superjob_secret_key)


