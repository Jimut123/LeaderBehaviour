# -*- coding: utf-8 -*-
#  scrapy crawl scrapTOI  -> in the same directory
"""
This program scraps the TOI website. First time it takes the url of an article page, then it automates itself, scraping
all the details of the article and storing it in newsTOI.sqlite. Run the scraper in the directory where this program is
stored. It will automate, collecting unique articles.
"""
import scrapy
import json
import sqlite3


from newsplease import NewsPlease

conn = sqlite3.connect('newsTOI.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS news (
    id              INTEGER,
    authors         TEXT,
    date_download   TEXT,
    date_modify     TEXT,
    date_publish    TEXT,
    description     TEXT,
    filename        TEXT,
    image_url       TEXT,
    language        TEXT,
    localpath       TEXT,
    source_domain   TEXT,
    text            TEXT,
    title           TEXT,
    title_page      TEXT,
    title_rss       TEXT,
    url             TEXT UNIQUE PRIMARY KEY
);
''')

int_id = 1
class ToScrapeCSSSpider(scrapy.Spider):
    name = "scrapTOI"
    global int_id
    custom_url = input("Enter custom url ? Y/n :\n")
    if custom_url == 'n' or custom_url == 'N': 
        cur.execute('''SELECT * FROM news ORDER BY id DESC LIMIT 1''')
        get_max_f = cur.fetchone()
        if get_max_f is not None:
            get_max_id = get_max_f[0]
            print("ID : ",get_max_id)
            cur.execute(''' SELECT url FROM news where id = ?''',(get_max_id,))
            next_page_url = cur.fetchone()[0] #converts the cursor object to number
            print("MAX ID = ",get_max_id,' \n URL FOUND = ',next_page_url)
            url_start = next_page_url
            
            int_id = get_max_id+1       # to continue the next entry id
        else:
            print("SORRY NO PREVIOUS RECORD FOUND!!!   \n USING A DEFAULT LINK ...")
            url_start = input("Enter the starting URL : ")
    else:
        url_start = input("\n Enter a custom url : ")
        
        cur.execute('''SELECT * FROM news ORDER BY id DESC LIMIT 1''')
        get_max_f = cur.fetchone()
        if get_max_f is not None:
            get_max_id = get_max_f[0]
            int_id = get_max_id+1

        
    start_urls = [
    url_start,
    ]

    def parse(self, response):
        global int_id
        # using newsplease to scrap the details

        #next_page_url = response.xpath("//link/rel/@href").extract()
        current_url = response.url
        article = NewsPlease.from_url(current_url)
        print("\033[0;37;46m ARTICLE NUMBER : ------------------------------------>  ",int_id,"\033[0;37;46m")
        print("\033[1;33;40m AUTHOR   : \n ",article.authors,"\033[0;33;40m")
        print("DATE OF DOWNLOAD : \n",article.date_download)
        print("DATE MODIFIED : \n",article.date_modify)
        print("DATE PUBLISHED : \n",article.date_publish)
        print("DESCRIPTION : \n",article.description)
        print("FILENAME : \n",article.filename)
        print("\033[0;31;47m IMAGE URL : \n  ",article.image_url,"\033[0;31;47m")
        print("LANGUAGE : \n",article.language)
        print("LOCALPATH : \n",article.localpath)
        print("SOURCE DOMAIN : \n",article.source_domain)
        print("\033[0;34;47m TEXT : \n ",article.text,"\033[0;34;47m")
        print("\033[0;32;47m TITLE : \n ",article.title,"\033[0;32;47m")
        print(" \033[0;35;47m TITLE PAGE : \n",article.title_page," \033[0;35;47m")
        print("TITLE RSS : \n",article.title_rss)
        print("\033[0;37;40m URL : \n ",article.url,"\033[0;37;40m")

        
        # TO INSERT THE VALUES IN SQLITE3 DATABASE
        try:
            cur.execute('''INSERT INTO news (id, authors, date_download, date_modify, date_publish, description, filename, image_url, language, localpath, source_domain, text, title, title_page, title_rss, url )
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', 
            ( int_id, str(article.authors), str(article.date_download), str(article.date_modify), str(article.date_publish), str(article.description), str(article.filename), str(article.image_url), str(article.language), str(article.localpath), str(article.source_domain), str(article.text), str(article.title), str(article.title_page), str(article.title_rss), str(article.url) ) ) 
            int_id += 1
        except:
            print("Already duplicate values!  cannot commit : ",article.url )
            pass
        if int_id%5 == 0:
            print(" \033[5;37;40m ************************* COMITTING **************************** \033[0;37;40m")
            conn.commit()
        next_page_url = response.css('link[rel="next"]::attr(href)').extract_first()
        #next_page_url = response.xpath('//link[contains(@href, "timesofindia.indiatimes.com/india")]/@href').extract_first()
        print("NEXT PAGE URL ===================================",next_page_url)
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

