import sqlite3

conn = sqlite3.connect('data/database.db')

c = conn.cursor()

c.execute('''CREATE TABLE Papers(paper_id TEXT, title TEXT, year TEXT, paper_text TEXT)''')
c.execute('''CREATE TABLE Authors(author_id TEXT, author_name TEXT, paper_id TEXT)''')
c.execute('''CREATE TABLE Keywords(keyword TEXT, paper_id TEXT, confidence TEXT)''')
conn.commit()
conn.close()