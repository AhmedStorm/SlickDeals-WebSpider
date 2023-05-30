import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from scrapy.selector import Selector
class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url = "https://www.intel.com/content/www/us/en/collections/content-type/mdds.html?p=1",
            # url = "https://www.duckduckgo.com",
            wait_time=7,
            screenshot=True,
            callback = self.parse,
        )

    def parse(self, response):
        # i=0
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        driver = response.meta['driver']
        time.sleep(2)
        driver.save_screenshot("screen.png")
        # print(driver.page_source)
        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath('//div[@class="content-table-list-item__headers"]')
        for link in links:
            yield {
                'Name': link.xpath('.//div[1]/div[1]/div[2]/a/text()').get(),
                'URL': f"https://www.intel.com{link.xpath('.//div[1]/div[1]/div[2]/a/@href').get()}",
                'link': link.xpath('.//div[6]/div[1]/button/@data-wap_ref').get()
            }

        next_page = driver.find_element(By.XPATH,'//button[@aria-label="Next"]')
        # next_page.click()
        # WebDriverWait(driver, 10).until(EC.staleness_of(next_page))
        if next_page:
        #     yield SeleniumRequest(callback= self.parse,
        #                           wait_time=5,
        #                           dont_filter = True)
            for i in range(2,209):
                next_page = f'https://www.intel.com/content/www/us/en/collections/content-type/mdds.html?p={str(i)}'
                print(next_page)
                yield SeleniumRequest(
                    url = next_page,
                    wait_time=7,
                    callback = self.parse,
                    dont_filter = True
                    )