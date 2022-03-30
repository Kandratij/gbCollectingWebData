import re

import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['www.superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Oracle&noGeo=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@target='_blank']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_val = response.xpath("//div[contains(@class,'vacancy-base-info')]//h1/text()").get()
        salary_val = response.xpath("//div[contains(@class,'vacancy-base-info')]//span[contains(@class,'_2Wp8I')]/text()").getall()
        salary_min_val = None
        salary_max_val = None
        if len(salary_val)>0:
            if salary_val[0] == 'от':
                salary_min_val = int(re.sub('\D', '', salary_val[2]))
            elif salary_val[0] == 'до':
                salary_max_val = int(re.sub('\D', '', salary_val[2]))
            elif re.sub('\D', '', salary_val[0]):
                salary_min_val = int(re.sub('\D', '', salary_val[0]))
                salary_max_val = int(re.sub('\D', '', salary_val[1]))

        url_val = response.url

        yield JobparserItem(name=name_val, salary_min=salary_min_val, salary_max=salary_max_val, url=url_val)
