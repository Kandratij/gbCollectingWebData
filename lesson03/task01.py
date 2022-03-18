## 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.
from pymongo import MongoClient
import gather_vacancies


def vacancies_to_db(vacancy_name, pages):
    vacancies_hh = gather_vacancies.collection(vacancy_name, pages)
    client = MongoClient('localhost', 27017)
    db = client['gb']
    db_vacancies = db.vacancies
    vacancy_count = 0
    for vacancy_hh in vacancies_hh:
        result = db_vacancies.find_one({'_id': vacancy_hh['_id']})
        if not result:
            db_vacancies.insert_one(vacancy_hh)
            vacancy_count+=1
    return vacancy_count


vacancy = input('введите название вакансии:')
pages = int(input('кол-во страниц для анализа:'))

print(f'добавлено {vacancies_to_db(vacancy, pages)} вакансий')
