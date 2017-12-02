# create_database.py
#
# Data Science - Final Project
# Zach Janicki and Michael McRoskey

DEBUG = True

import sqlite3

def insert_paper(db, paper_id, title, year, paper_text):
	command = 'INSERT INTO Papers VALUES (\"' + paper_id + '\",\"' + title + '\",\"' + year + '\",\"' + paper_text + '\")'
	db.execute(command)
	if DEBUG:
		print "Inserted paper " + paper_id

def delete_paper(db, paper_id):
	command = "DELETE FROM Papers WHERE paper_id=\'" + paper_id + "\';"
	db.execute(command)
	if DEBUG:
		print "Deleted paper " + paper_id
	
def update_paper(db, paper_id, field, value):
	command = "UPDATE Papers SET " + field + " = " + value + " WHERE paper_id = \"" + paper_id + "\""
	db.execute(command)
	if DEBUG:
		print "Updated paper " + paper_id + " with " + field + " = " + value
	
def display_table(db, table):
	print "\n========= " + table + " ========="
	command = 'SELECT * FROM ' + table
	for row in db.execute(command):
		print row

if __name__ == "__main__":

	conn = sqlite3.connect('data/database.db')
	c = conn.cursor()
	
	try:
		c.execute('''CREATE TABLE Papers(paper_id TEXT, title TEXT, year TEXT, paper_text TEXT)''')
		c.execute('''CREATE TABLE Authors(author_id TEXT, author_name TEXT, paper_id TEXT)''')
		c.execute('''CREATE TABLE Keywords(keyword TEXT, paper_id TEXT, confidence TEXT)''')
	except:
		print("Already created SQL tables")
	
	insert_paper(c, "456", "Testing", "2017", "TESADFKASDJF ASKFDJ")
	insert_paper(c, "875", "Testing", "2017", "TESADFKASDJF ASKFDJ")
	delete_paper(c, "875")
	
	update_paper(c, "875", "year", "2019")
	
	display_table(c, "Papers")
		
	conn.commit()
	conn.close()
	
