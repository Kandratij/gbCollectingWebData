#Сложить собранные новости в БД
from task01 import get_top_news
from pymongo import MongoClient


def save_news():
    top_news = get_top_news()
    client = MongoClient('localhost', 27017)
    db = client['gb']
    db_news = db.news
    news_count = 0
    for news in top_news:
        result = db_news.find_one({'link': news['link']})
        if not result:
            db_news.insert_one(news)
            news_count += 1
    return news_count


print('Добавлено новых новостей: ', save_news())