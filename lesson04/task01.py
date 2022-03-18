# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
import requests
import datetime
from lxml import html
from pprint import pprint

def get_top_news():
    lenta_url = 'https://lenta.ru'
    news_url  = lenta_url+'/parts/news'
    client_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

    response = requests.get(news_url, headers=client_header)

    dom = html.fromstring(response.text)

    all_news = dom.xpath('//li[contains(@class,"parts-page__item")]/a[contains(@class,"card-full-news")]')
    list_news = []
    for element in all_news:
        news = {}

        news['title'] = element.xpath('./h3/text()')[0]
        href = element.xpath('./@href')[0]
        if href[0] == '/':
            news['source'] = lenta_url
            news['link'] = lenta_url+href
        else:
            news['source'] = href[0:href.find('/', 8)]
            news['link'] = href

        date = element.xpath('.//time/text()')[0]
        if len(date) > 5:
            #полная дата
            news['date'] = date
        else:
            #только время
            now = datetime.datetime.now()
            news['date'] = date+', '+now.strftime('%d %B %Y')
        list_news.append(news)
    return list_news


if __name__ == "__main__":
    pprint(get_top_news())
