import json
import sys
import numpy as np

from textblob import TextBlob

def loadTweetList(filename):

	tweetList = None
	try:
		inFile = open(filename, 'r')
		tweetList = json.load(inFile)
		inFile.close()
		print(filename + " loaded with a length of " + str(len(tweetList))) + " tweets"
	except:
		print('Error loading file')

	return tweetList

def analysis(Tswitch):

	tweetList = loadTweetList(Tswitch + '_tweets.json')
	pSum = 0
	products = []

	outFile = open(Tswitch + '_tweets_sentiments.csv', 'w')
	outFile.write("polarity,subjectivity,product\n")
	outFile.close()

	outFile = open(Tswitch + '_tweets_sentiments.csv', 'a')

	for tweet in tweetList:

		tbSent = TextBlob(tweet).sentiment
		product = tbSent.polarity * tbSent.subjectivity
		if product != 0:
			products.append(product)
			pSum += product
			outFile.write(str(tbSent.polarity) + ',' + str(tbSent.subjectivity) + ',' + str(product) + '\n')

	outFile.close()

	print(Tswitch + " related tweets have sentiment products with:")
	print("]    Sum: " + str(pSum))
	print("]    Median: " + str(np.median(products)))
	print("]    Mean: " + str(np.mean(products)))
	print("]    Standard deviation: " + str(np.std(products)))
	print("]    Mean of absolutes: " + str(np.std(map(abs, products))))





# Running
analysis('work')
analysis('school')