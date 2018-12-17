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


def statisticalAnalysisHelper(dataset):
	datasetStats = statGroup(len(dataset), dataset)

	print("]    N: " + str(datasetStats.n))
	datasetStats.sum = sum(dataset)
	print("]    Sum: " + str(datasetStats.sum))
	datasetStats.median = np.median(dataset)
	print("]    Median: " + str(datasetStats.median))
	datasetStats.mean = np.mean(dataset)
	print("]    Mean: " + str(datasetStats.mean))
	datasetStats.stdev = np.std(dataset)
	print("]    Standard deviation: " + str(datasetStats.stdev))
	datasetStats.meanOfAbs = np.std(map(abs, dataset))
	print("]    Mean of absolutes: " + str(datasetStats.meanOfAbs))

	return datasetStats


def statisticalAnalysis(Tswitch, datasets):
	retStats = {}

	print('\n' + Tswitch + " related tweets have polarities with:")
	retStats['polarities'] = statisticalAnalysisHelper(datasets['polarities'])

	print('\n' + Tswitch + " related tweets have sentiments with:")
	retStats['subjectivities'] = statisticalAnalysisHelper(datasets['subjectivities'])

	print('\n' + Tswitch + " related tweets have products with:")
	retStats['products'] = statisticalAnalysisHelper(datasets['products'])

	return retStats



def loadLists(filename):
	outLists = {'polarities': [], 'subjectivities': [], 'products': []}

	with open(filename, 'rb') as f:
			reader = csv.reader(f)
			full_list = list(reader)
	f.close()
	for elem in full_list:
		outLists['polarities'].append(float(elem[0]))
		outLists['subjectivities'].append(float(elem[1]))
		outLists['products'].append(float(elem[2]))

	return outLists

def calcStats(work_stats, school_stats):
	t_value, p_value = stats.ttest_ind(work_stats.list, school_stats.list, equal_var=False)

	print("]    t-value: " + str(t_value))
	print("]    p-value: " + str(p_value))


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

		work_lists = loadLists('work_tweets_sentiments.csv')
		school_lists = loadLists('school_tweets_sentiments.csv')

		work_stats = statisticalAnalysis('work', work_lists)
		school_stats = statisticalAnalysis('school', school_lists)

	except Exception as e:
		print("Error opening file:")
		print(e)
		exit()
else:
	exit()


### Stats

print("\nPolarities: Two-sided test for the null hypothesis yeilds: ")
calcStats(work_stats['polarities'], school_stats['polarities'])

print("\nSubjectivities: Two-sided test for the null hypothesis yeilds: ")
calcStats(work_stats['subjectivities'], school_stats['subjectivities'])


print("\nProducts: Two-sided test for the null hypothesis yeilds: ")
calcStats(work_stats['products'], school_stats['products'])









