# scrapy crawl getNames1 -o getUSNames.json
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import sqlite3

conn = sqlite3.connect('getRawNames1.sqlite')
cur = conn.cursor()

# [A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,2}\s+[A-Z]([a-z]+|\.) --> to get the names present in a article
cur.executescript('''
CREATE TABLE IF NOT EXISTS namesOfLeader (
    name   TEXT UNIQUE PRIMARY KEY
);
''')

class getNamesOfLeaders(scrapy.Spider):
    name = "getNames1"

    start_urls = [
        'https://www.house.gov/representatives',
    ]

    def parse(self, response):
        for  getNames in response.xpath('//a/text()'):
            #print(getDetails.extract())
            names_of_rep = getNames.extract()
            print(names_of_rep)
            yield{
                'names':names_of_rep,
            }
            cur.execute('''INSERT OR IGNORE INTO namesOfLeader (name)
					VALUES ( ? )''', ( names_of_rep, ) ) # stacks the link found at the bottom
        conn.commit()


            
