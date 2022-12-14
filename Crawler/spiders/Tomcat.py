import scrapy
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from Crawler.Funcs import Funcs

class TomcatSpider(scrapy.Spider):
    name = "tomcat"
    settings = get_project_settings()
    start_urls = [
        settings['URLS']['TOMCAT']
    ]


    def parse(self, response):
        table_rows = response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr').getall()
        del table_rows[0]
        del table_rows[0]
        del table_rows[-1]

        result = dict()
        for row in table_rows:
            version = Selector(text=row).xpath('.//td[1]/@data-sort-value').get().strip()
            date = Selector(text=row).xpath('.//td[5]/text()').get().strip()
            result['Version'] = version
            result['Date'] = Funcs.date_to_str(date)
            yield result