import scrapy
from scrapy.selector import Selector
from Crawler.spiders.Wiki_Spider import Wiki_Spider
import re
from scrapy.utils.project import get_project_settings

class WebLogicSpider(Wiki_Spider):
    name = "weblogic"
    settings = get_project_settings()
    start_urls = [
        settings['URLS']['WEBLOGIC']
    ]


    # def parse(self, response):
    #     items = response.xpath('//*[@id="mw-content-text"]/div[1]/ul[1]/li/text()').getall()

    #     result = dict()
    #     for item in items:
    #         # item_list = item.split("(")
    #         item_list = re.split(r'-', item)

    #         if len(item_list) == 2:
    #             result['Version'] = item_list[0].strip()
    #             if len(item_list[1].strip()) < 20:
    #                 result['Date'] = item_list[1].strip()
    #             else: result['Date'] = ""
    #             yield result
            