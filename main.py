import psycopg2

from classes import HeadHunterAPI, DBManager
from config import config
from utils import create_database, create_vacancy_table, get_companies_from_json, format_to_postgresql, \
    insert_vacancy_data


def main():
    vacancies = HeadHunterAPI()

    db_name = 'vacancies'

    params = config()
    conn = None

    create_database(params, db_name)

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_vacancy_table(cur)
                print("Таблица vacancies успешно создана")

                for company in get_companies_from_json():
                    company_info = vacancies.get_companies_vacancies(company["id"])
                    company_info_sql = format_to_postgresql(company_info)

                    insert_vacancy_data(cur, company_info_sql)
                    print(f"Данные о {company['name']} в vacancies успешно добавлены")

                database_class = DBManager(conn, cur)

                print(database_class.get_companies_and_vacancies_count())
                print(database_class.get_all_vacancies())
                print(database_class.get_avg_salary())
                print(database_class.get_vacancies_with_higher_salary())
                print(database_class.get_vacancies_with_keyword("инженер"))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
