# scrapy crawl getNames1 -o getUSNames.json
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class getNamesOfLeaders(scrapy.Spider):
    name = "getProxyList"

    start_urls = [
        'https://www.us-proxy.org/',
    ]

    def parse(self, response):
        names_of_svr = p.xpath('td[1]/text()').extract_first()
        #names_of_svr = getNames.extract()
        print(names_of_svr)
            
        #next_page_url = response.xpath('//link[contains(@href, "timesofindia.indiatimes.com")]/@href').extract()[4]
        #print("NEXT PAGE URL ===================================",next_page_url)
        #if next_page_url is not None:
        #    yield scrapy.Request(response.urljoin(next_page_url))

            
