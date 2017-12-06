#!/usr/bin/python
# create_database.py
#
# Data Science - Final Project
# Zach Janicki and Michael McRoskey

# Imports -------------------------
import sys, sqlite3, string, re
from console_colors import console_colors as cc

# Global vars ---------------------
DEBUG = False
DEBUG_VERBOSE = True

# ------------------ Papers table ---------------------
def paper_already_inserted(db, paper_id):
	command = 'SELECT 1 FROM Papers WHERE paper_id = \'' + paper_id + '\' LIMIT 1'
	for row in db.execute(command):
		if row[0] is 1:
			if DEBUG:
				print cc.OKGREEN + "Paper " + paper_id + " exists in db" + cc.ENDC
			return True
		else:
			if DEBUG:
				print cc.FAIL + "Paper " + paper_id + " does not exist in db" + cc.ENDC
			return False
	

def insert_paper(db, paper_id, title, year, paper_text):
	# Don't insert if already exists
	if paper_already_inserted(db, paper_id):
		return False
	command = 'INSERT INTO Papers VALUES (\"' + paper_id + '\",\"' + title + '\",\"' + year + '\",\"' + paper_text + '\")'
	db.execute(command)
	return True


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
		
		
def extract_content(path):
	full_path = 'data/text/' + path
	with open(full_path) as f:
		return f.read().replace('\n', ' ')


def clean(string):
	# string = string.lower()
	chars_to_remove = ['\"', '\'', '\x00']
	string = re.sub('[' + re.escape(''.join(chars_to_remove)) + ']', '', string)
    # return string.encode('ascii', errors='ignore').decode()
	return string


def populate_papers(db):
	
	index_txt_counter = 0	# number of papers in index.txt
	papers_txt_counter = 0	# number of papers in Papers.txt
	insertion_counter = 0	# number of papers inserted into db
	
	# Create preliminary dictionary with paper_id, file paths, and titles
	# from index.txt
	papers = {}
	with open('data/microsoft/index.txt') as f:
		for line in f:
			line = line.strip("\n")
			content = line.split("\t")
			folder_name = content[0]
			file_name = content[1]
			paper_id = content[2]
			title = content[3]
			path = folder_name + "/" + file_name + ".txt"
			papers[paper_id] = (path, title)
			index_txt_counter += 1
			if DEBUG_VERBOSE:
				print cc.OKBLUE + "Paper " + paper_id + " found in index.txt" + cc.ENDC
	
	# Gather more information from larger Papers.txt file and compare
	with open('data/microsoft/Papers.txt') as f:
		for line in f:
			line = line.strip("\n")
			content = line.split("\t")
			paper_id = content[0]
			title_case = content[1]
			title = content[2]
			year = content[3]
			# date_of_proceeding = content[4]	# not recommended to use
			# doi = content[5]					# not recommended to use
			# conf_full_name = content[6]		# not recommended to use
			conf = content[7]
			# N/A = content[8]
			conf_id = content[9]
			# N/A = content[10]
			papers_txt_counter += 1
			
			if DEBUG_VERBOSE:
				print cc.OKBLUE + "Paper " + paper_id + " found in Papers.txt" + cc.ENDC
			
			# Success
			if paper_id in papers:
				raw_text = extract_content(papers[paper_id][0])
				clean_text = clean(raw_text)
				return_status = insert_paper(db, paper_id, title, year, clean_text)
				if return_status:
					insertion_counter += 1
					if DEBUG:
						print cc.OKBLUE +  "Paper " + paper_id + " inserted" + cc.ENDC
				else:
					if DEBUG:
						print cc.WARNING + "Paper " + paper_id + " not inserted" + cc.ENDC
			# Failure
			else:
				if DEBUG:
					print cc.FAIL + "Paper " + paper_id + " in Papers.txt does not exist in index.txt" + cc.ENDC
	
	return index_txt_counter, papers_txt_counter, insertion_counter


# ------------------ Authors table ---------------------
def author_already_inserted(db, author_id, author_name, paper_id):
	return False
	command = 'SELECT 1 FROM Authors WHERE author_id = "{}" AND author_name = "{}" and paper_id = "{}" LIMIT 1'.format(author_id, author_name, paper_id)
	print command
	for row in db.execute(command):
		if row[0] is 1:
			return True
		else:
			return False

def insert_author(db, author_id, author_name, paper_id):
	if author_already_inserted(db, author_id, author_name, paper_id):
		return False
	command = 'INSERT INTO Authors VALUES ("{}", "{}", "{}")'.format(author_id, author_name, paper_id)
	print author_id, author_name, paper_id
	db.execute(command)
	if DEBUG:
		print "Inserted author \t" + author_name + "\t" + author_id
	return True

def populate_authors(db):
	counter = 0
	with open('data/microsoft/AuthorsCleaned.txt') as f:
		for line in f:
			content = line.split("\t")
			author_name = str(content[0])
			author_id = str(content[1])
			paper_id = str(content[2].strip('\n')) # getting rid of those pesky new lines
			return_status = insert_author(db, author_id, author_name, paper_id)
			if return_status:
				counter += 1
	return counter


# ------------------ Keywords table ---------------------
def keyword_already_inserted(db, keyword):
	command = 'SELECT 1 FROM Keywords WHERE keyword = \'' + keyword + '\' LIMIT 1'
	for row in db.execute(command):
		if row[0] is 1:
			return True
		else:
			return False

def insert_keyword(db, keyword, paper_id, confidence):
	#if keyword_already_inserted(db, keyword):
	#	return False
	command = 'INSERT INTO Keywords VALUES (\"' + keyword + '\",\"' + paper_id + '\",\"' + confidence + '\")'
	db.execute(command)
	if DEBUG:
		print "Inserted keyword \t" + keyword
	return True
	
		
def populate_keywords(db):
	counter = 0
	with open('data/microsoft/PaperKeywords.txt') as f:
		for line in f:
			content = line.split("\t")
			paper_id = content[0]
			keyword = content[1]
			# keyword_id = content[2] 	# not recommended to use
			confidence = "0" 			# not sure what confidence refers to
			print counter, paper_id, keyword
			return_status = insert_keyword(db, keyword, paper_id, confidence)
			if return_status:
				counter += 1
	return counter

# ---------------- Affiliations table ---------------------
def affiliation_already_inserted(db, paper_id, author_id, author_sequence_id):
	return False
	command = 'SELECT 1 FROM Affiliations WHERE paper_id = "{}" AND author_id = "{}" AND sid = "{}"'.format(paper_id, author_id, author_sequence_id)
	for row in db.execute(command):
		if row[0] is 1:
			return True
		else:
			return False

def insert_affiliation(db, paper_id, author_id, author_sequence_id):
	if affiliation_already_inserted(db, paper_id, author_id, author_sequence_id):
		return False
	command = 'INSERT INTO Affiliations VALUES ("{}", "{}", "{}")'.format(paper_id, author_id, author_sequence_id)
	db.execute(command)
	if DEBUG:
		print "Inserted [{}, {}, {}]".format(paper_id, author_id, author_sequence_id)
	return True

def populate_affiliations(db):
	counter = 0
	with open('data/microsoft/AffilsCleaned.txt') as f:
		for line in f:
			content = line.split('\t')
			paper_id = str(content[0])
			author_id = str(content[1])
			author_sequence_id = str(content[2].strip('\n')) # getting rid of those pesky new lines
			return_status = insert_affiliation(db, paper_id, author_id, author_sequence_id)
			print counter, paper_id, author_id, author_sequence_id
			if return_status:
				counter += 1
	return counter
	
	
def display_table(db, table):
	print "\n================== " + table + " =================="
	command = 'SELECT * FROM ' + table
	for row in db.execute(command):
		string = ""
		for item in row:
			string += item + "\t"
		print string


def clean_affiliations(db):
	authors_f = open('data/microsoft/Authors.txt')
	affils_f = open('data/microsoft/PaperAuthorAffiliations.txt')
	cleaned_affils_f = open('data/microsoft/AffilsCleaned.txt', 'w')
	command = 'SELECT paper_id FROM papers'
	paper_ids = []
	aff_number = 0
	for item in db.execute(command):
		paper_ids.append(str(item[0]))
	print len(paper_ids)
	for line in affils_f:
		print 'Checking Affiliation file line number {}'.format(aff_number)
		author_affiliation = line.split('\t')
		aff_pid = str(author_affiliation[0])
		aid = str(author_affiliation[1])
		fid = str(author_affiliation[2])
		# aff_org = str(author_affiliation[3]) not recommended to use
		aff = str(author_affiliation[4])
		sid = str(author_affiliation[5])

		for pid in paper_ids:
			#print pid
			#print '==========='
			#print aff_pid, aid, pid
			if pid == aff_pid:
				cleaned_affils_f.write('{}\t{}\t{}\t{}\t{}'.format(aff_pid, aid, fid, aff, sid))
		aff_number += 1
	authors_f.close()
	affils_f.close()
	cleaned_affils_f.close()

def clean_authors(db):
	authors_f = open('data/microsoft/Authors.txt')
	cleaned_affils_f = open('data/microsoft/AffilsCleaned.txt')
	authors_cleaned_f = open('data/microsoft/AuthorsCleaned.txt', 'w')
	command = 'SELECT paper_id FROM papers'
	paper_ids = []
	aut_number = 0
	aff_author_list = [] # list of author IDs
	for line in cleaned_affils_f:
		aff_author_list.append(line)
	for item in db.execute(command):
		paper_ids.append(str(item[0]))
	for line in authors_f:
		print 'Checking Author file line number {}'.format(aff_number)
		items = line.split('\t')
		author_id = str(items[0])
		author_name = str(items[1]).strip()
		for pid_aid_pair in aff_author_list:
			if str(pid_aid_pair.split('\t')[1].strip()) == author_id:
				authors_cleaned_f.write('{}\t{}\t{}\n'.format(author_name, author_id, str(pid_aid_pair.split('\t')[0].strip())))
		aut_number += 1
	authors_f.close()
	cleaned_affils_f.close()
	authors_cleaned_f.close()


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
		c.execute('''CREATE TABLE Affiliations(paper_id TEXT, author_id TEXT, sid TEXT)''')
	except:
		print "Already created SQL tables\n"
	
	# Populate Papers table
	
	index_txt_counter, papers_txt_counter, insertion_counter = populate_papers(c)
	print cc.OKGREEN + str(insertion_counter) + "\t papers inserted" + cc.ENDC
	print str(index_txt_counter) + "\t papers in index.txt"
	print str(papers_txt_counter) + "\t papers in Papers.txt"
	conn.commit()
	
	# clean_affiliations(c)
	# clean_authors(c)

	# Populate Authors table
	authors_inserted = populate_authors(c)
	print cc.OKGREEN + str(authors_inserted) + "\t authors inserted" + cc.ENDC
	
	# Populate Keywords table
	keywords_inserted = populate_keywords(c)
	print cc.OKGREEN + str(keywords_inserted) + "\t keywords inserted" + cc.ENDC
	
	affiliations_inserted = populate_affiliations(c)
	print cc.OKGREEN + str(affiliations_inserted) + "\t affiliations inserted" + cc.ENDC

	conn.commit()
	conn.close()