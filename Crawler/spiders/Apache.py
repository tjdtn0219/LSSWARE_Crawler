import scrapy
from scrapy.selector import Selector
from Crawler.spiders.Wiki_Spider import Wiki_Spider
from scrapy.utils.project import get_project_settings

class ApacheSpider(Wiki_Spider):
    name = "apache"
    settings = get_project_settings()
    start_urls = [
        settings['URLS']['APACHE']
    ]

    # def parse(self, response):
    #     table_rows = response.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr').getall()
    #     del table_rows[0]

    #     result=dict()
    #     for row in table_rows:
    #         version = Selector(text=row).xpath('.//th/text()').get()
    #         if version and version != " ":
    #             result['Version'] = version.strip()
    #         else:
    #             version = result['Name'] = Selector(text=row).xpath('.//th/b/text()').get()
    #             if version:
    #                 result['Version'] = version
    #         result['Date'] = Selector(text=row).xpath('.//td[1]/text()').get()

    #         if version:
    #             yield result