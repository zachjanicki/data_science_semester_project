#!/usr/bin/python
# encoding: utf-8

import sqlite3

n_type = 4
s_method = 'method algorithm model approach framework process scheme implementation procedure strategy architecture'
s_problem = 'problem technique process system application task evaluation tool paradigm benchmark software'
s_dataset = 'data dataset database'
s_metric = 'value score measure metric function parameter space'
types = ['METHOD','PROBLEM','DATASET','METRIC']
wordsets = [set(s_method.split(' ')),set(s_problem.split(' ')),set(s_dataset.split(' ')),set(s_metric.split(' '))]

conn = sqlite3.connect('data/database.db')
db = conn.cursor()

command = '''SELECT * FROM Entities'''
db.execute(command)
result = db.fetchall()

for paper_id, term, n, count, e_type in result:
	terms = term.split()
	for word in terms:
		for i, entity_types in enumerate(wordsets):
			if word in entity_types: 
				command = 'UPDATE Entities SET type = "{}" WHERE paper_id = "{}" AND term = "{}"'.format(types[i], paper_id, term)
				db.execute(command)
				conn.commit()

#command = '''SELECT paper_id, term, type FROM Entities WHERE type != ""'''
#db.execute(command)
#result = db.fetchall()