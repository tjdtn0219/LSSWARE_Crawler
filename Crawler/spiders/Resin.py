import scrapy
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from selenium import webdriver

class ResinSpider(scrapy.Spider):
    name = 'resin'
    settings = get_project_settings()
    start_urls = [
        settings['URLS']['RESIN']
    ]

    def parse(self, response):
        url = response.url

        driver_path = ResinSpider.settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get(url)
        # driver.implicitly_wait(3)

        iframe_source = driver.page_source

        items = scrapy.Selector(text=iframe_source).xpath('/html/body/table[2]/tbody/tr/td[3]/h2/a/text()').getall()

        result = dict()
        for item in items:
            result['Version'] = item
            result['Date'] = None
            yield result
        driver.quit()
