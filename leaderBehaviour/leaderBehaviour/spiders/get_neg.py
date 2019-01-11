from tqdm import tqdm
import json
import sqlite3
import re

conn = sqlite3.connect('newsTOI.sqlite')
cur = conn.cursor()
cur.executescript('''
CREATE TABLE IF NOT EXISTS scraped_data (
    id              INTEGER UNIQUE PRIMARY KEY,
    neg_wp          TEXT
);
''')
db_id = 1

f = open('negative-words.txt')
neg_words = []
for word in f.read().split():
    #print(word)
    neg_words.append(word)
#print(neg_words)

#neg_words -> contains all the -ve words that could be present in a file.

# to match every article and get the -ve words present!
# To get the maximum id present in the sqlite3 db
cur.execute('''SELECT * FROM news ORDER BY id DESC LIMIT 1''')
get_max_f = cur.fetchone()
get_max_id = get_max_f[0]       #contains the maximum of the ID present in the database

for i in tqdm(range(get_max_id+1)):
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
    if current_id > 1:
        # Now extracting the names present for each of text
        get_text = sec_cut_garbage      # the text in clean form
        found_words = ""
        for word in neg_words:
            #   word = each word
            if word in get_text:
                print (word, " found in id : ",current_id)
                found_words += ' '+word
        
        cur.execute('''INSERT INTO scraped_data (id, neg_wp )
                VALUES ( ?, ? )''', 
                ( int(current_id), found_words  ) )
        

#conn.commit()
