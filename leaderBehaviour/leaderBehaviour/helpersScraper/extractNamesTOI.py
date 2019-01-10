"""
Please execute this program after executing the scraper 'scrapTOI' for a while.
python extractNamesTOI.py
"""

import scrapy
import json
import sqlite3
import re
print("CHECK THE DIRECTORY PLEASE!!! need to be in the same directory as of the db present!")
# ([A-Z][a-z]+)
conn = sqlite3.connect('newsTOI.sqlite')
cur = conn.cursor()

db_id = 1


# To get the maximum id present in the sqlite3 db
cur.execute('''SELECT * FROM news ORDER BY id DESC LIMIT 1''')
get_max_f = cur.fetchone()
get_max_id = get_max_f[0]       #contains the maximum of the ID present in the database
#print("ID : ",get_max_id)
for i in range(get_max_id+1):
    current_id = i
    #print(current_id)
    # to select the text from the db of the current id
    
    cur.execute(''' SELECT text FROM news where id = ?''',(current_id,))
    get_text_tuple = cur.fetchone() #converts the cursor object to number
    get_text_str_raw = str(get_text_tuple)
    first_cut_garbage = get_text_str_raw[2:]
    sec_cut_garbage = first_cut_garbage[:len(first_cut_garbage)-3]
    print("current ID = ",current_id,' \n TEXT = ',sec_cut_garbage)
    #print("\n",get_text_str[0])

    # Now extracting the names present for each of text
    get_text = sec_cut_garbage      # the text in clean form

    regex_1 = '([A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,2}\s+[A-Z]([a-z]+|\.))'
    names_list = re.findall(regex_1,get_text)
    get_list = [names_list_iter[0] for names_list_iter in names_list]
    print("\n\n Found names : ",get_list)


    

