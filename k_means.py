#!/usr/bin/python
# encoding: utf-8

import sqlite3, sys, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

def document_similarity(papers_text, papers_conf):
	#define vectorizer parameters
	tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
												min_df=0.1, stop_words='english',
												use_idf=True, ngram_range=(1,3))							

	tfidf_matrix = tfidf_vectorizer.fit_transform(papers_text)
#	print(tfidf_matrix.shape)
#	terms = tfidf_vectorizer.get_feature_names()
#	dist = 1 - cosine_similarity(tfidf_matrix)
	return tfidf_matrix

def k_means(num_clusters, tfidf_matrix):
	km = KMeans(n_clusters=num_clusters)
	km.fit(tfidf_matrix)
	clusters = km.labels_.tolist()
	
	return clusters

if __name__ == "__main__":
	
	conn = sqlite3.connect('data/database.db')
	db = conn.cursor()
	
	# Load papers locally into table
	print "Loading SQL query results into local storage"
	command = '''SELECT paper_id, title, year, paper_text, conf FROM Papers'''
	db.execute(command)
	result = db.fetchall()
	random.shuffle(result)
	
	conf_num = {'idcm':0, 'kdd':1,'wsdm':2, 'www':3}
	conf_str = {0:'idcm', 1:'kdd',2:'wsdm', 3:'www'}
	papers_ids = []
	papers_text = []
	papers_conf = []
	
	paper_counter = 0
	for paper_id, title, year, paper_text, conf in result:
		papers_ids.append(paper_id)
		papers_text.append(title)
		if conf == "icdm":
			conf = "idcm"
		papers_conf.append(conf_num[conf])
		if paper_counter > 300:
			break
		paper_counter += 1
		sys.stdout.write("\r%d\t papers clustered" % paper_counter)
		sys.stdout.flush()
	print ""
	
	# Tf-idf and document similarity
	tfidf_matrix = document_similarity(papers_text, papers_conf)
	
	# K-means clustering
	num_clusters = 4
	clusters = k_means(num_clusters, tfidf_matrix)
	
	# Arrays represent counts for each conference
	conferences_predicted = [0,0,0,0]
	conferences_actual = [0,0,0,0]
	for p in papers_conf:
		conferences_actual[p] += 1
			
	for i, cluster in enumerate(clusters):
		conferences_predicted[cluster] += 1
		
#	print str(conferences_predicted[0]) + " papers in conference A"
#	print str(conferences_predicted[1]) + " papers in conference B"
#	print str(conferences_predicted[2]) + " papers in conference C"
#	print str(conferences_predicted[3]) + " papers in conference D"
#	print ""
#	print str(conferences_actual[0]) + " papers in conference idcm"
#	print str(conferences_actual[1]) + " papers in conference kdd"
#	print str(conferences_actual[2]) + " papers in conference wsdm"
#	print str(conferences_actual[3]) + " papers in conference www"
	
	# Need to Re-map cluster numbers to conferences given ground truth
	re_map = ['','','','']
	
	for i in range(0, num_clusters):
		max_predicted = conferences_predicted.index(max(conferences_predicted))
		max_actual = conferences_actual.index(max(conferences_actual))
#		print str(max_predicted) + "==>" + str(max_actual) + "==>" + conf_str[max_actual]
		re_map[max_predicted] = conf_str[max_actual]
		conferences_predicted[max_predicted] = 0
		conferences_actual[max_actual] = 0
	
	final_prediction = []
	
	# Display results
	for i, cluster in enumerate(clusters):
#		print papers_ids[i] + " => " + re_map[cluster]
		final_prediction.append(conf_num[re_map[cluster]])
		
	# Check accuracy
	num_right = 0
	num_wrong = 0
	for i, predicted_cluster in enumerate(final_prediction):
		if papers_conf[i] != final_prediction[i]:
			num_wrong += 1
		else:
			num_right += 1
	
	print "Accuracy: " + str(float(num_wrong)*100 / float((num_right + num_wrong)))[0:6] + "%"
		
	