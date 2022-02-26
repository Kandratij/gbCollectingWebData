import requests

login = 'oracle'
rq = requests.get(f'https://api.github.com/users/{login}/repos')

if rq.status_code == 200 :
    with open(f'{login}.json', mode='w', encoding='UTF-8') as f:
        f.write(rq.text)
else:
    print(f'ошибка получения данных для пользователя "{login}" (code:{rq.status_code} reason:{rq.reason})')
