# create_database.py
#
# Data Science - Final Project
# Zach Janicki and Michael McRoskey

DEBUG = False

import sqlite3

# ------------------ Papers table ---------------------
def insert_paper(db, paper_id, title, year, paper_text):
	command = 'INSERT INTO Papers VALUES (\"' + paper_id + '\",\"' + title + '\",\"' + year + '\",\"' + paper_text + '\")'
	db.execute(command)
	if DEBUG:
		print "Inserted paper \t" + paper_id

def delete_paper(db, paper_id):
	command = "DELETE FROM Papers WHERE paper_id=\'" + paper_id + "\';"
	db.execute(command)
	if DEBUG:
		print "Deleted paper \t" + paper_id
	
def update_paper(db, paper_id, field, value):
	command = "UPDATE Papers SET " + field + " = " + value + " WHERE paper_id = \"" + paper_id + "\""
	db.execute(command)
	if DEBUG:
		print "Updated paper \t" + paper_id + "\t with " + field + " = " + value
		
def populate_papers():
	pass
#	with open('data/microsoft/PaperKeywords.txt') as f:
#		for line in f:
#			content = line.split("\t")
#			paper_id = content[0]
#			keyword = content[1]
#			# keyword_id = content[2] 	# not recommended to use
#			confidence = "0" 			# not sure what confidence refers to
#			insert_keyword(c, keyword, paper_id, confidence)

# ------------------ Authors table ---------------------
def insert_author(db, author_id, author_name, paper_id):
	command = 'INSERT INTO Authors VALUES (\"' + author_id + '\",\"' + author_name + '\",\"' + paper_id + '\")'
	db.execute(command)
	if DEBUG:
		print "Inserted author \t" + author_name + "\t" + author_id

def populate_authors():
	with open('data/microsoft/Authors.txt') as f:
		for line in f:
			content = line.split("\t")
			author_id = content[0]
			author_name = content[1]
			paper_id = "0"
			insert_author(c, author_id, author_name, paper_id)


# ------------------ Keywords table ---------------------
def insert_keyword(db, keyword, paper_id, confidence):
	command = 'INSERT INTO Keywords VALUES (\"' + keyword + '\",\"' + paper_id + '\",\"' + confidence + '\")'
	db.execute(command)
	if DEBUG:
		print "Inserted keyword \t" + keyword
		
def populate_keywords():
	with open('data/microsoft/PaperKeywords.txt') as f:
		for line in f:
			content = line.split("\t")
			paper_id = content[0]
			keyword = content[1]
			# keyword_id = content[2] 	# not recommended to use
			confidence = "0" 			# not sure what confidence refers to
			insert_keyword(c, keyword, paper_id, confidence)
	
def display_table(db, table):
	print "\n================== " + table + " =================="
	command = 'SELECT * FROM ' + table
	for row in db.execute(command):
		string = ""
		for item in row:
			string += item + "\t"
		print string


# ------------------ Main Execution ---------------------
if __name__ == "__main__":
	
	# Create the database
	conn = sqlite3.connect('data/database.db')
	c = conn.cursor()
	
	# Try to create blank Papers, Authors, Keywords tables (if first run)
	try:
		c.execute('''CREATE TABLE Papers(paper_id TEXT, title TEXT, year TEXT, paper_text TEXT)''')
		c.execute('''CREATE TABLE Authors(author_id TEXT, author_name TEXT, paper_id TEXT)''')
		c.execute('''CREATE TABLE Keywords(keyword TEXT, paper_id TEXT, confidence TEXT)''')
	except:
		print "Already created SQL tables\n"
	
	# Populate Papers table
	populate_papers()
	
	# Populate Authors table
	populate_authors()
	
	# Populate Keywords table
	populate_keywords()
		
	conn.commit()
	conn.close()