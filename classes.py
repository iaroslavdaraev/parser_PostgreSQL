import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies?employer_id='

    def get_companies_vacancies(self, company_id: int):
        """Получает данные через API"""
        try:
            company_vacancy = requests.get(f'{self.url}{company_id}', {'per_page': 50}).json()
            return company_vacancy
        except Exception as error:
            raise Exception(f'Ошибка {error}')


class DBManager:
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute("""SELECT company_name, COUNT(*) AS vacancies_quantity
        FROM vacancies
        GROUP BY company_name
        ORDER BY vacancies_quantity DESC"""
                         )
        rows = self.cur.fetchall()
        data_info = {}
        for row in rows:
            data_info[row[0]] = row[1]
        return data_info

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute("SELECT company_name, vacancy_name, salary_to, vacancy_url FROM vacancies")
        rows = self.cur.fetchall()
        data_info = []
        for row in rows:
            data_info.append(list(row))
        return data_info

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cur.execute(f"SELECT AVG(salary_to) FROM vacancies")
        avg_salary = self.cur.fetchall()
        return int(avg_salary[0][0])

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute(
            f"""
                SELECT company_name, vacancy_name, salary_to, vacancy_url FROM vacancies
                WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)
            """
        )
        rows = self.cur.fetchall()
        data_info = []
        for row in rows:
            data_info.append(list(row))
        return data_info

    def get_vacancies_with_keyword(self, word):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        self.cur.execute(
            f"""
                SELECT company_name, vacancy_name, salary_to, vacancy_url 
                FROM vacancies
                WHERE vacancy_name LIKE '%{word}%'"""
        )
        rows = self.cur.fetchall()
        data_info = []
        for row in rows:
            data_info.append(list(row))
        return data_info
