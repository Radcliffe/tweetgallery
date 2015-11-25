import sqlite3
conn = sqlite3.connect('tweets.db')
conn.execute('create table tweets (searchterm text, timestamp integer, 
             'username text, body text, media text, approved integer)') 

# conn.execute('alter table tweets add searchterm text')             
