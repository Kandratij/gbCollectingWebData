## 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).
from pymongo import MongoClient
from pprint import pprint


def print_vacansies(salary):
    client = MongoClient('localhost', 27017)
    db = client['gb']
    db_vacancies = db.vacancies
    vacancy_count = 0
    for vacancy_hh in db_vacancies.find({'$or': [{'min_salary': {'$gte': salary}}, {'max_salary': {'$gte': salary}}]}):
        pprint(vacancy_hh)


print_vacansies(int(input('введите сумму зарплаты:')))
