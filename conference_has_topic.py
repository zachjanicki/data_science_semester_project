#!/usr/bin/python

#from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import fetch_20newsgroups
#
conferences = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=conferences, shuffle=True, random_state=42)
#
from sklearn.feature_extraction.text import CountVectorizer
#count_vect = CountVectorizer()
#X_train_counts = count_vect.fit_transform(twenty_train.data)
#print X_train_counts.shape

from sklearn.feature_extraction.text import TfidfTransformer
#tfidf_transformer = TfidfTransformer()
#X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#X_train_tfidf.shape


from sklearn.naive_bayes import MultinomialNB
#clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
#
docs_new = ['God is love', 'OpenGL on the GPU is fast']
#X_new_counts = count_vect.transform(docs_new)
#X_new_tfidf = tfidf_transformer.transform(X_new_counts)
#
#predicted = clf.predict(X_new_tfidf)
#
#for doc, category in zip(docs_new, predicted):
#	print('%r => %s' % (doc, twenty_train.target_names[category]))

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

#def conference_has_topic(db, problem, method, conference):
#	
#	return True
##	return False
#	
#if __name__ == "__main__":
#	print "Test"
##	conn = sqlite3.connect('data/database.db')
##	db = conn.cursor()
##
##	command = '''SELECT * FROM Entities'''
##	db.execute(command)
##	result = db.fetchall()
##	
##	types = ['METHOD','PROBLEM','DATASET','METRIC']
##	
##	print conference_has_topic(db, problem, method, conference)
#
#from sklearn import datasets
#iris = datasets.load_iris()
#
#conferences = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
#
#print len(iris.data)
##print "\n"
#print len(iris.target)
#
#gnb = GaussianNB()
#y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
#print len(y_pred)
#print("Number of mislabeled points out of a total %d points : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))