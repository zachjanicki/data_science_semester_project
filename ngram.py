#!/usr/bin/python
# encoding: utf-8
# create_database.py
#
# Data Science - Final Project
# Zach Janicki and Michael McRoskey

import sqlite3, re, sys


def ngram(string, n):
	string = string.split(' ')
	output = {}
	for i in range(len(string)-n+1):
		g = ' '.join(string[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
	return output
	

def print_dict(ngram_dict):
	try:
		col_width = (max(len(key) for key in ngram_dict))
	except:
		col_width = 0
	for key, value in reversed(sorted(ngram_dict.iteritems(), key=lambda (k,v): (v,k))):
		spaces = col_width - len(key) + 3
		print key + " "*spaces + str(value)
		
		
def clean(s):
	s = s.lower()
	return s
	
		
def strip_punct(s):
	s = re.sub('[^A-Za-z0-9]+', '', s)
	s = " ".join(s.split())
	return s.encode('ascii', 'ignore').decode('ascii')
	

def clean_stopwords(ngram_dict, n):
	# Load in stopwords
	stopwords = set()
	with open('stopwords.txt') as f:
		for line in f:
			content = line.strip("\n")
			stopwords.add(content)
	
	# Check if ngram contains stopwords		
	for key, value in reversed(sorted(ngram_dict.iteritems(), key=lambda (k,v): (v,k))):
		# Example				# key   = "Divergence minimization."
		words = key.split()		# words = [u'divergence', u'minimization...']
		has_stopword = False
		# For loop deletes key if any of the conditions are met
		for i in range(0, n):	# n = 2
			# Figure out if actually n terms
			try:
				word = words[i]
			except:
				has_stopword = True
				break
			# Strip punctuation			= [u'divergence', u'minimization']
			stripped_word = strip_punct(word)
			# If empty string, throw out
			if not stripped_word:
				has_stopword = True
				break
			# If "div/3erg^encE" ==> "divergence", it has punctuation in it
			if word != stripped_word:
				has_stopword = True
				break
			# If the word is a stopword
			if word in stopwords:
				has_stopword = True
				break
		# Delete entire phrase if found
		if has_stopword:
			del ngram_dict[key]
	
	return ngram_dict
	
	
def insert_term(db, paper_id, term, n, count):
	command = 'INSERT INTO Entities VALUES ("{}", "{}", {}, {})'.format(paper_id, term, str(n), str(count))
	db.execute(command)	


def populate_ngrams(db, minimum_support, max_n_gram):
	terms_inserted = 0
	papers_affected = 0
	
	command = '''SELECT paper_id, paper_text FROM Papers'''
	db.execute(command)
	result = db.fetchall()

	for paper_id, paper_text in result:
		grams = {}
		cleaned_paper = clean(paper_text)
		for n in range(2, max_n_gram+1):
			raw_ngram = ngram(cleaned_paper, n)
			cleaned_ngram = clean_stopwords(raw_ngram, n)
			for k,v in cleaned_ngram.items():
				if int(v) < minimum_support:
					del cleaned_ngram[k]
				else:
					insert_term(db, paper_id, k, n, v)
					terms_inserted += 1
					# sys.stdout.write("\r%d\t terms inserted" % terms_inserted)
					# sys.stdout.flush()
		papers_affected += 1
		sys.stdout.write("\r%d\t papers affected" % papers_affected)
		sys.stdout.flush()
		
	return terms_inserted, papers_affected
	

if __name__ == "__main__":
	# Reference Database
	conn = sqlite3.connect('data/database.db')
	c = conn.cursor()
		
	try:
		c.execute('''CREATE TABLE Entities(paper_id TEXT, term TEXT, n INT, count INT)''')
	except:
		print "Already created SQL tables\n"
	
	minimum_support = 5
	max_n_gram = 5
	
	terms_inserted, papers_affected = populate_ngrams(c, minimum_support, max_n_gram)
	print "\n\n" + str(terms_inserted) + "\t terms inserted"
	print str(papers_affected) + "\t papers affected"
	
#	command = '''SELECT * FROM Entities'''
#	for row in c.execute(command): 
#		print row

	conn.commit()
	conn.close()
