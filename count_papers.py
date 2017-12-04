#!/usr/bin/python
import os

DIR = 'data/text/'

total_txt = 0
for root, dirs, files in os.walk(DIR):
	total = 0
	for f in files:
		try:
			if f[-4:] != ".txt":
				continue
		except:
			continue
		total += 1
	total_txt += total
	
print str(total_txt) + " total .txt files found"