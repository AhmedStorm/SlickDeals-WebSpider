import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time
from scrapy.selector import Selector
import pandas as pd


class NewExampleSpider(scrapy.Spider):
    name = 'new_example'
    def start_requests(self):
            yield SeleniumRequest(
                url = "https://www.littelfuse.com/search-results.aspx#t=SeriesTab",
                wait_time=7,
                screenshot=True,
                callback = self.parse,
            )

    def parse(self, response):
        driver = response.meta['driver']
        driver.save_screenshot("Great.png")
        # print(driver.page_source)
        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath('//*[@id="SearchLF"]/div[3]/div/div/div[6]/div[2]/div/div/div/ul/h4/a')
        for link in links:
            yield {
                'URL': f'https://www.littelfuse.com{link.xpath(".//@href").get()}'
            }

        # button = response_obj.xpath('//*[@id="SearchLF"]/div[3]/div/div/div[1]/div[5]/ul/li[3]/a[@title="Next"]')
        # if button:
        #      yield scrapy.Request(url="")
             
        DB = pd.read_csv(r"C:\Users\157718\WEBScrappying\littlefuse\littlefuse\spiders\links.csv")

        for one in DB.values:
            next_page = one[0]
            if next_page:
                yield SeleniumRequest(
                    url = next_page,
                    wait_time=7,
                    callback = self.parse,
                    # dont_filter = True
                )
