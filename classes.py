import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies?employer_id='

    def get_companies_vacancies(self, company_id: int):
        """Полкчает данные через API"""
        try:
            company_vacancy = requests.get(f'{self.url}{company_id}', {'per_page': 50}).json()
            return company_vacancy
        except Exception as error:
            raise Exception(f'Ошибка {error}')


class DBManager:
    """Класс для работы с базой данных PostgreSQL"""

    def get_companies_and_vacancies_count(cur):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        pass
