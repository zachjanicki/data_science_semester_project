#!/usr/bin/python

import sqlite3
import random
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def conference_has_topic(db, problem, method, conference):
	return True

def naive_bayes(db, train_set, train_set_targets, test_set, test_set_targets):

	conferences = ['idcm', 'kdd','wsdm', 'www']

	# Train Data -----------------------------
	print "Training on " + str(len(train_set)) + " entities..."
	text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
	text_clf.fit(train_set, train_set_targets)

	# Test Data ------------------------------
	print "Testing on " + str(len(test_set)) + " entities..."
	predicted = text_clf.predict(test_set)

	# Results --------------------------------
	print "DONE.\nSample of 10 results\n"
	count = 0
	for doc, conference in zip(test_set, predicted):
		count += 1
		print('%r => %s' % (doc, conferences[conference]))
		if count > 10:
			break
		
	print "\nCorrectly predicted " + str(np.mean(predicted == test_set_targets))[0:6] + "%"
	
	
if __name__ == "__main__":

	conn = sqlite3.connect('data/database.db')
	db = conn.cursor()
	
	command = '''SELECT COUNT(*) FROM Entities'''
	db.execute(command)
	result = db.fetchall()
	num_entities = int(result[0][0])

	command = '''SELECT * FROM Entities'''
	db.execute(command)
	result = db.fetchall()
	
	train_set = []
	train_set_targets = []
	test_set = []
	test_set_targets = []
	
	conf_num = {'idcm':0, 'kdd':1,'wsdm':2, 'www':3}
	
	random.shuffle(result)
	
	counter = 0
	for paper_id, entity, n, count, e_type, abbr in result:
		
		# Determine conference of paper
		conference = ''
		command = '''SELECT conf FROM Papers WHERE paper_id = "{}" LIMIT 1'''.format(paper_id)
		row = db.execute(command)
		for conf in row:
			conference = conf[0]
			if conference == "icdm":
				conference = "idcm"
			break
		
		# Populate Train and Test Sets
		if counter <= num_entities/2:
			train_set.append(entity)
			train_set_targets.append(conf_num[str(conference)])
		elif counter < num_entities - num_entities/4:
			test_set.append(entity)
			test_set_targets.append(conf_num[str(conference)])
		else:
			break
		counter += 1
			
	print str(counter) + " entities inserted"
	naive_bayes(db, train_set, train_set_targets, test_set, test_set_targets)
