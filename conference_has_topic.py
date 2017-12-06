#!/usr/bin/python

from sklearn.datasets import fetch_20newsgroups
conferences = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=conferences, shuffle=True, random_state=42)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
docs_new = ['God is love', 'OpenGL on the GPU is fast']

from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
text_clf.fit(twenty_train.data, twenty_train.target)

import numpy as np
twenty_test = fetch_20newsgroups(subset='test',categories=conferences, shuffle=True, random_state=42)
docs_test = twenty_test.data
print len(twenty_test.data)
predicted = text_clf.predict(docs_test)

for doc, conference in zip(docs_test, predicted):
	print('%r => %s' % (doc[0:10], twenty_train.target_names[conference]))

#print len(docs_test)
#print predicted
#print twenty_test.target
#print np.mean(predicted == twenty_test.target)

def conference_has_topic(db, problem, method, conference):
	
	return True
#	return False
	
if __name__ == "__main__":
	print "Test"
	conn = sqlite3.connect('data/database.db')
	db = conn.cursor()

	command = '''SELECT * FROM Entities'''
	db.execute(command)
	result = db.fetchall()
	
	types = ['METHOD','PROBLEM','DATASET','METRIC']
	
	print conference_has_topic(db, problem, method, conference)