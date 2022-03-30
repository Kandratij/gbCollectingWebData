import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&area=232&search_field=name&search_field=company_name&search_field=description&text=Oracle+developer',
                  'https://hh.ru/search/vacancy?area=1&area=1511&search_field=name&search_field=company_name&search_field=description&text=Oracle+developer']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_val = response.css('h1::text').get()
        salary_val = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        salary_min_val = None
        salary_max_val = None
        if len(salary_val)>0:
            if 'от ' in salary_val and ' до ' in salary_val:
                salary_min_val = int(re.sub('\D', '', salary_val[1]))
                salary_max_val = int(re.sub('\D', '', salary_val[3]))
            elif 'от ' in salary_val :
                salary_max_val = int(re.sub('\D', '', salary_val[1]))
            elif 'до ' in salary_val:
                salary_max_val = int(re.sub('\D', '', salary_val[1]))


        url_val = response.url
        yield JobparserItem(name=name_val, salary_min=salary_min_val, salary_max=salary_max_val, url=url_val)
