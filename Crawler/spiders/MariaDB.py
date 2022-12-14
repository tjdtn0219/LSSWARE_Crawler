import scrapy
from scrapy.selector import Selector
from Crawler.spiders.Wiki_Spider import Wiki_Spider
from scrapy.utils.project import get_project_settings

class MariaDBpider(Wiki_Spider):
    name = "mariadb"
    settings = get_project_settings()
    start_urls = [
        settings['URLS']['MARIADB']
    ]

    # def parse(self, response):
    #     table_rows = response.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr').getall()
    #     del table_rows[0]
    #     del table_rows[-1]

    #     result = dict()
    #     for row in table_rows:
    #         name = Selector(text=row).xpath('.//td[1]/text()').get().strip()
    #         if name == "":
    #             name = Selector(text=row).xpath('.//td[1]/b/text()').get().strip()
    #         result['Version'] = name
    #         result['Date'] = Selector(text=row).xpath('.//td[4]/text()').get()
    #         yield result