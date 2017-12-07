#!/usr/bin/python
# encoding: utf-8

import sqlite3
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def visualize(text):
	# Generate a word cloud image
	wordcloud = WordCloud(background_color="white").generate(text)

#	# Display the generated image:
#	plt.imshow(wordcloud, interpolation='bilinear')
#	plt.axis("off")

	# lower max_font_size
	wordcloud = WordCloud(background_color="white",max_font_size=40).generate(text)
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

if __name__ == "__main__":

	conn = sqlite3.connect('data/database.db')
	db = conn.cursor()
	
	command = '''SELECT *, COUNT(term) as term_count
	FROM Entities
	GROUP BY term
	ORDER BY term_count DESC'''
	db.execute(command)
	result = db.fetchall()
	
	text = ''
	
	for a, b, c, d, e, f, g in result:
		for i in range(0,int(g)):
			text += str(b) + " "
	
	visualize(text)