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
        cur.execute(
            """
        SELECT company_name, COUNT(*) AS vacancies_quantity
        FROM vacancies
        GROUP BY company_name
        ORDER BY vacancies_quantity DESC"""
        )
        rows = cur.fetchall()
        data_info = {}
        for row in rows:
            data_info[row[0]] = row[1]
        return data_info

    def get_all_vacancies(cur):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        cur.execute("SELECT company_name, vacancy_name, salary_to, vacancy_url FROM vacancies")
        rows = cur.fetchall()
        data_info = []
        for row in rows:
            data_info.append(list(row))
        return data_info

    def get_avg_salary(cur):
        """Получает среднюю зарплату по вакансиям"""
        cur.execute(f"SELECT AVG(salary_to) FROM vacancies")
        avg_salary = cur.fetchall()
        return int(avg_salary[0][0])

    def get_vacancies_with_higher_salary(cur):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        cur.execute(
            f"""
                SELECT company_name, vacancy_name, salary_to, vacancy_url FROM vacancies
                WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)
            """
        )
        rows = cur.fetchall()
        data_info = []
        for row in rows:
            data_info.append(list(row))
        return data_info

    def get_vacancies_with_keyword(cur):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        cur.execute(
            f"""
                SELECT company_name, vacancy_name, salary_to, vacancy_url 
                FROM vacancies
                WHERE vacancy_name LIKE '%{word}%'"""
        )
        rows = cur.fetchall()
        data_info = []
        for row in rows:
            data_info.append(list(row))
        return data_info
