"""
This script rearranges the id from the database in case if some error occurs!
"""

import scrapy
import json
import sqlite3

print("CHECK THE DIRECTORY PLEASE!!! need to be in the same directory as of the db present!")
from newsplease import NewsPlease

conn = sqlite3.connect('newsTOI.sqlite')
cur = conn.cursor()
cur.execute('''SELECT COUNT(*) FROM news ''')
get_max_f = cur.fetchone()
#print(get_max_f)
max_id = int(get_max_f[0])

current_id = 0
data_fetch = cur.execute(''' SELECT * FROM news''')
print(data_fetch)

list_a = []
for item in data_fetch:
    #print(item)
    current_id += 1
    key_p = item[15]
    #print(key_p)
    list_a.append((current_id,key_p))
    # number/ id then url
#print(list_a)

for item_1 in list_a:
    def update_Sl(current_id1,key_p1):
        print("Updating ... url  : ",key_p1," and id : ",current_id1)
        cur.execute(''' UPDATE news SET id = ? WHERE url = ?''',(current_id1,key_p1,))
    a, b = item_1
    update_Sl(a,b)
conn.commit()

