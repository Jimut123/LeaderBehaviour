# scrapy crawl getNames

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import sqlite3

conn = sqlite3.connect('getRawNames.sqlite')
cur = conn.cursor()

# [A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,2}\s+[A-Z]([a-z]+|\.) --> to get the names present in a article
cur.executescript('''
CREATE TABLE IF NOT EXISTS namesOfLeader (
    name   TEXT UNIQUE PRIMARY KEY
);
''')

class getNamesOfLeaders(scrapy.Spider):
    name = "getNames"

    start_urls = [
        'https://www.indiatoday.in/india/story/cabinet-reshuffle-narendra-modi-union-council-of-ministers-1036996-2017-09-03',
    ]

    def parse(self, response):
        divs = response.xpath('//div')
        for b,p in zip(divs.xpath('//b/text()'),divs.xpath('//p/text()')):
            get_names = b.extract()
            
            print(get_names)
            if get_names is not None and get_names is not " ":
                #get_desc = p.extract()
                yield{
                    'names':get_names,
                }
                print(get_names)
                cur.execute('''INSERT OR IGNORE INTO namesOfLeader (name)
					VALUES ( ? )''', ( get_names, ) ) # stacks the link found at the bottom
            conn.commit()
                


            
