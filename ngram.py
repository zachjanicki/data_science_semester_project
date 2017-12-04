#!/usr/bin/python
# create_database.py
#
# Data Science - Final Project
# Zach Janicki and Michael McRoskey

def remove_stop_words():

def ngram(string, n):
	string = string.split(' ')
	output = {}
	for i in range(len(string)-n+1):
		g = ' '.join(string[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
	return output

result = ngram('totally useless information totally useless useless information', 2) # {'a a': 3}

col_width = (max(len(key) for key in result))
for key, value in reversed(sorted(result.iteritems(), key=lambda (k,v): (v,k))):
	spaces = col_width - len(key) + 3
	print key + " "*spaces + str(value)