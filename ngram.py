#!/usr/bin/python
# encoding: utf-8
# create_database.py
#
# Data Science - Final Project
# Zach Janicki and Michael McRoskey

import sqlite3, string, re, unicodedata

def ngram(string, n):
	string = string.split(' ')
	output = {}
	for i in range(len(string)-n+1):
		g = ' '.join(string[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
	return output

def print_dict(ngram_dict):
	col_width = (max(len(key) for key in ngram_dict))
	for key, value in reversed(sorted(ngram_dict.iteritems(), key=lambda (k,v): (v,k))):
		spaces = col_width - len(key) + 3
		print key + " "*spaces + str(value)
		
def clean(s):
	s = s.lower()
	return s
#	s = re.sub('[^A-Za-z0-9]+', '', s)
#	s = " ".join(s.split())
#	return s.encode('ascii', 'ignore').decode('ascii')
		
def strip_punct(s):
	s = re.sub('[^A-Za-z0-9]+', '', s)
	s = " ".join(s.split())
	return s.encode('ascii', 'ignore').decode('ascii')
#	s = " ".join(s.split())
#	return re.sub('[^A-Za-z0-9]+', '', s)
#	punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
#	return ''.join(x for x in s if unicodedata.category(x) not in punctutation_cats)
#	return re.sub(ur"\p{P}+", "", s)
#	return s.translate(None, string.punctuation)

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
	

if __name__ == "__main__":
	# Reference Database
	conn = sqlite3.connect('data/database.db')
	c = conn.cursor()
	
	grams = {}
	
	command = '''SELECT paper_text FROM Papers'''
	for paper in c.execute(command):
		cleaned_paper = clean(paper[0])
		for n in range(2,5+1):
			name = str(n) + "-gram"
			raw_ngram = ngram(cleaned_paper, n)
			cleaned_ngram = clean_stopwords(raw_ngram, n)
			for k,v in cleaned_ngram.items():
				if int(v) < 5:
				   del cleaned_ngram[k]
			grams[name] = cleaned_ngram
		break

	try:
		print "====================2===================="
		print grams["2-gram"]
	except:
		print "error 2"
	try:
		print "====================3===================="
		print grams["3-gram"]
	except:
		print "error 3"
	try:
		print "====================4===================="
		print grams["4-gram"]
	except:
		print "error 4"
	try:
		print "====================5===================="
		print grams["5-gram"]
	except:
		print "error 5"
