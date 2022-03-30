from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    #crawler_process.crawl(HhruSpider)
    crawler_process.crawl(SuperjobruSpider)

    crawler_process.start()


