#!/usr/bin/python

import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Global vars ----------------------------
conferences = ['idcm', 'kdd','wsdm', 'www']

# Train Data -----------------------------
training = ['information latent dirichlet information allocation information', 'support vector machine', 'expectation maximization', 'world wide web', 'singular value decomposition']
targets = [0, 1, 2, 3, 2]
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
text_clf.fit(training, targets)

# Test Data ------------------------------
testing = ['information retrieval', 'neural information processing systems']
testing_targets = [0, 0]
predicted = text_clf.predict(testing)

for doc, conference in zip(testing, predicted):
	print('%r => %s' % (doc, conferences[conference]))
	
print np.mean(predicted == testing_targets)

#def conference_has_topic(db, problem, method, conference):
#	
#	return True
##	return False
#	
#if __name__ == "__main__":
#	print "Test"
#	conn = sqlite3.connect('data/database.db')
#	db = conn.cursor()
#
#	command = '''SELECT * FROM Entities'''
#	db.execute(command)
#	result = db.fetchall()
#	
#	types = ['METHOD','PROBLEM','DATASET','METRIC']
#	
#	print conference_has_topic(db, problem, method, conference)