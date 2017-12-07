#!/usr/bin/python

import sys
import sqlite3
import random
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from sklearn import metrics

def find_conference(db, paper_id):
	conference = ''
	command = '''SELECT conf FROM Papers WHERE paper_id = "{}" LIMIT 1'''.format(paper_id)
	row = db.execute(command)
	for conf in row:
		conference = conf[0]
		if conference == "icdm":
			conference = "idcm"
		break
	return conference


def predict_naive_bayes(db, text_clf, test_set):
	conf_num = {'idcm':0, 'kdd':1,'wsdm':2, 'www':3}
	# Figure out ground truth
	for entity in test_set:
		entity_count = {'idcm':0, 'kdd':0,'wsdm':0, 'www':0}
		command = '''SELECT paper_id FROM Entities WHERE term = "{}"'''.format(entity)
		db.execute(command)
		result = db.fetchall()
		for paper_id in result:
			conf = find_conference(db, paper_id[0])
			entity_count[conf] += 1
		maximum = max(entity_count, key=entity_count.get)
		test_set_targets = [conf_num[maximum]]
		
		test_naive_bayes(text_clf, test_set, test_set_targets)
	return True


def test_naive_bayes(text_clf, test_set, test_set_targets):
	conferences = ['idcm', 'kdd','wsdm', 'www']
	
	# Test Data ------------------------------
	print "Testing on " + str(len(test_set)) + " entities..."
	predicted = text_clf.predict(test_set)

#	print(metrics.classification_report(test_set_targets, predicted, target_names=conferences))

	# Results --------------------------------
	print "DONE.\nSample of 10 results\n"
	count = 0
	for entity, conference in zip(test_set, predicted):
		count += 1
		print('%r => %s' % (entity, conferences[conference]))
		if count > 10:
			break
		
	print "\nCorrectly predicted " + str(np.mean(predicted == test_set_targets)*100)[0:6] + "%"


def train_naive_bayes(train_set, train_set_targets):

	print "Training on " + str(len(train_set)) + " entities..."
	text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
	text_clf.fit(train_set, train_set_targets)
	
	return text_clf

	
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
		conference = find_conference(db, paper_id)
		
		# Populate train data set
		train_set.append(entity)
		train_set_targets.append(conf_num[str(conference)])
		
#		# Populate Train and Test Sets
#		if counter <= num_entities/2:
#			train_set.append(entity)
#			train_set_targets.append(conf_num[str(conference)])
#		elif counter < num_entities - num_entities/4:
#			test_set.append(entity)
#			test_set_targets.append(conf_num[str(conference)])
#		else:
#			break
		counter += 1
		sys.stdout.write("\r%d\t entities added" % counter)
		sys.stdout.flush()
	
	print str(counter) + " entities inserted"
	text_clf = train_naive_bayes(train_set, train_set_targets)
#	test_naive_bayes(text_clf, test_set, test_set_targets)
	predict_naive_bayes(db, text_clf, ["support vector machine"])
