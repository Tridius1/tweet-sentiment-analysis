import json
import sys
import csv

import numpy as np
from textblob import TextBlob
from scipy import stats



class statGroup:

	def __init__(self, N, pList):
		self.n = N
		self.list = pList
		self.sum = None
		self.median = None
		self.mean = None
		self.stdev = None
		self.meanOfAbs = None



def loadTweetList(filename):

	tweetList = None
	try:
		inFile = open(filename, 'r')
		tweetList = json.load(inFile)
		inFile.close()
		print("\n" + filename + " loaded with a length of " + str(len(tweetList))) + " tweets"
	except:
		print('Error loading file')

	return tweetList

def sentimentAnalysis(Tswitch):

	tweetList = loadTweetList(Tswitch + '_tweets.json')
	products = []

	outFile = open(Tswitch + '_tweets_sentiments.csv', 'w')
	outFile.close()

	outFile = open(Tswitch + '_tweets_sentiments.csv', 'a')

	for tweet in tweetList:

		tbSent = TextBlob(tweet).sentiment
		product = tbSent.polarity * tbSent.subjectivity
		if product != 0:
			products.append(product)
			outFile.write(str(tbSent.polarity) + ',' + str(tbSent.subjectivity) + ',' + str(product) + '\n')

	outFile.close()

	return products


def statisticalAnalysis(Tswitch, products):
	ProdStats = statGroup(len(products), products)

	print(Tswitch + " related tweets have sentiment products with:")
	ProdStats.sum = sum(products)
	print("]    Sum: " + str(ProdStats.sum))
	ProdStats.median = np.median(products)
	print("]    Median: " + str(ProdStats.median))
	ProdStats.mean = np.mean(products)
	print("]    Mean: " + str(ProdStats.mean))
	ProdStats.stdev = np.std(products)
	print("]    Standard deviation: " + str(ProdStats.stdev))
	ProdStats.meanOfAbs = np.std(map(abs, products))
	print("]    Mean of absolutes: " + str(ProdStats.meanOfAbs))

	return ProdStats





# Running

print("Analyze sentiment? (y/n)")
ans = str(raw_input())

work_stats = None
school_stats = None

if ans[0].lower() == 'y':
	work_stats = statisticalAnalysis('work', sentimentAnalysis('work'))
	school_stats = statisticalAnalysis('school', sentimentAnalysis('school'))
elif ans[0].lower() == 'n':
	try:
		with open('work_tweets_sentiments.csv', 'rb') as f:
			reader = csv.reader(f)
			full_list = list(reader)
		f.close()
		work_list = []
		for elem in full_list:
			work_list.append(float(elem[2]))

		with open('school_tweets_sentiments.csv', 'rb') as f:
			reader = csv.reader(f)
			full_list = list(reader)
		f.close()
		school_list = []
		for elem in full_list:
			school_list.append(float(elem[2]))

		work_stats = statisticalAnalysis('work', work_list)
		school_stats = statisticalAnalysis('school', school_list)

	except Exception as e:
		print("Error opening file:")
		print(e)
		exit()
else:
	exit()


### Stats

t_value, p_value = stats.ttest_ind(work_stats.list, school_stats.list, equal_var=False)

print("\nTwo-sided test for the null hypothesis yeilds: ")
print("]    t-value: " + str(t_value))
print("]    p-value: " + str(p_value))






