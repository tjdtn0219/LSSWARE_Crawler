import scrapy
from scrapy.selector import Selector
from Crawler.spiders.test_inherit import SpiderTest

class JEUSSpider(SpiderTest):
    name = "jeus"
    start_urls = [
        'https://en.wikipedia.org/wiki/JEUS',
    ]


    # def parse(self, response):
    #     tables = response.xpath('//*[@id="article"]/article/div[3]/div').getall()
    #     del tables[-1]
    #     del tables[0]

    #     result = dict()
    #     for table in tables:
    #         items = Selector(text=table).xpath('.//table/tbody/tr/th/ul/li/text()').getall()
    #         for item in items:
    #             if item.strip():
    #                 result['Version'] = item.strip()
    #                 yield result