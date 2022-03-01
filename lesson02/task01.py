import requests
from bs4 import BeautifulSoup
import re
import pandas

vacancy_name = input('введите название вакансии:')
page_count = int(input('кол-во страниц для анализа:'))
hh_url = 'https://hh.ru'
client_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
params = {'text': vacancy_name, 'clusters': True, 'area': 1, 'ored_clusters': True, 'enable_snippets': True, 'hhtmFrom':'vacancy_search_list','customDomain': 1, 'from':'suggest_post'}
url = f'{hh_url}/search/vacancy'

vacancies_list = []

for page in range(page_count):
    params['page']= page
    response = requests.get(url, headers=client_header, params=params)
    if not (200 <= response.status_code < 300):
        raise NameError('ResponseReturnNotSuccess')
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies_class = dom.find_all('div', {'class': 'vacancy-serp-item-body'})
    for vacancy in vacancies_class:
        vacancy_data = {}
        info = vacancy.find('a', {'class': 'bloko-link'})
        # Наименование вакансии.
        vacancy_data['name'] = info.getText()
        # Ссылку на саму вакансию.
        vacancy_data['href'] = info['href']
        # Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
        salary_info = vacancy.find('span', {'class': 'bloko-header-section-3'})
        salary = {}
        if salary_info:
            if salary_info.text[0:2] == 'от':
                vacancy_data['min_salary'] = re.sub(r'[а-я.\s]', "", salary_info.text)
            elif salary_info.text[0:2] == 'до':
                vacancy_data['max_salary'] = re.sub(r'[а-я.\s]', "", salary_info.text)
            else:
                vacancy_data['min_salary'], vacancy_data['max_salary'] = re.sub(r'[а-я.\s]', "", salary_info.text).split('–')
            vacancy_data['salary_valuta'] = re.sub('от|до|\s+|\d+|–', "", salary_info.text)
        # Сайт, откуда собрана вакансия.
        employer = vacancy.find('a', {'class': 'bloko-link_kind-tertiary'})
        if employer:
            emp_response = requests.get(hh_url+employer['href'], headers=client_header)
            emp_dom = BeautifulSoup(emp_response.text, 'html.parser')
            emp_info = emp_dom.find('a', {'data-qa': 'sidebar-company-site'})
            if emp_info:
                vacancy_data['site'] = emp_info['href']
        vacancies_list.append(vacancy_data)

pd_cols = ['name', 'href', 'site', 'min_salary', 'max_salary', 'salary_valuta']
print(pandas.DataFrame(vacancies_list, columns=pd_cols).to_csv(vacancy_name+'.csv'))



