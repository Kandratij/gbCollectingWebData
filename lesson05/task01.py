# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from datetime import datetime, timedelta
import re



def format_date(date_str):
    months = {1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня',
              7: 'Июля', 8: 'Августа', 9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'}
    dat = datetime.now()
    frm_date_str = date_str.replace(',', f' {dat.year},')
    if 'Вчера' in date_str:
        dat = dat - timedelta(days=1)
        frm_date_str = frm_date_str.replace('Вчера', f'{dat.day} {months[dat.month]}')
    elif 'Сегодня' in date_str:
        frm_date_str = frm_date_str.replace('Сегодня', f'{dat.day} {months[dat.month]}' )
    return frm_date_str

s = Service('./chromedriver')

driver = webdriver.Chrome(service=s)
driver.implicitly_wait(10)

driver.get('https://mail.ru')
wait = WebDriverWait(driver, 30)

driver.find_element(By.XPATH, "//button[contains(@class,'ph-login')]").click()
driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[contains(@class,'ag-popup__frame')]"))
elem = driver.find_element(By.NAME, "username")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
elem = driver.find_element(By.NAME, "password")
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

driver.switch_to.default_content()

elem = driver.find_element(By.XPATH, "//div[contains(@class, 'ReactVirtualized__Grid ReactVirtualized__List')]")

links = []

while True:
    mails = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class,"letter-list-item")]')))

    if len(mails) == 0:
        break

    if len(links) > 0 and links[-1] == mails[-1].get_attribute("href"):
        break

    for mail in mails:
        try:
            href = mail.get_attribute('href')
            if href:
                links.append(href)
        except:
            pass
    try:
        actions = ActionChains(driver)
        actions.move_to_element(mails[-1])
        actions.perform()
    except:
        pass

client = MongoClient('localhost', 27017)
db = client['gb']
db_mails = db.mails
mails_count = 0

mail = {}
for link in links:
    if link:
        driver.get(link)
        mail['_id'] = re.findall("/0:(.*):0/", link)[0]
        elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "letter-contact")))
        mail['contact'] = elem.get_attribute('title')

        elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "thread-subject")))
        mail['subject'] = elem.text

        elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "letter__date")))
        mail['date'] = format_date(elem.text)

        elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "letter-body__body-content")))
        mail['body'] = elem.text

        result = db_mails.find_one({'_id': mail['_id']})
        if not result:
            print(f"From: {mail['contact']}; Date: {mail['date']}; Subject: {mail['subject']}")
            db_mails.insert_one(mail)
            mails_count += 1

print(f'Added New Mails: {mails_count}')

driver.close()
driver.quit()
