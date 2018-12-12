import json

tweetList = None
try:
	inFile = open('work_tweets.json', 'r')
	tweetList = json.load(inFile)
	inFile.close()
	print("work_tweets.json contains " + str(len(tweetList))) + " tweets"
except:
	print('Error loading file work_tweets.json')


tweetList = None
try:
	inFile = open('school_tweets.json', 'r')
	tweetList = json.load(inFile)
	inFile.close()
	print("school_tweets.json contains " + str(len(tweetList))) + " tweets"
except:
	print('Error loading file school_tweets.json')