import scrapy
from scrapy.selector import Selector

class MariaDBpider(scrapy.Spider):
    name = "mariadb"
    start_urls = [
        'https://en.wikipedia.org/wiki/MariaDB',
    ]

    def parse(self, response):
        table_rows = response.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr').getall()
        del table_rows[0]

        result = dict()
        for row in table_rows:
            result['Name'] = Selector(text=row).xpath('.//td[1]/text()').get().strip()
            result['Date'] = Selector(text=row).xpath('.//td[4]/text()').get().strip()
            yield result