import json
import time

import tweepy
from textblob import TextBlob


#Credentials
inFile = open("credentials.json", 'r')
credentials = json.load(inFile)
inFile.close()

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = credentials['twitter']['access_token']
ACCESS_SECRET = credentials['twitter']['access_token_secret']
CONSUMER_KEY = credentials['twitter']['consumer_key']
CONSUMER_SECRET = credentials['twitter']['consumer_secret']	

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#-------------------------------------------------------------------------------------------------






# Starting the stream
#workStream.filter(track=['job'])
#schoolStream.filter(track=['school'], async=True)

keywords = None
logfile = None
print("Select stream:\n  1: Work related\n  2: School related")
selection = input()
if selection == 1:
	keywords = ['work', 'job', 'business', 'career', 'contract', 'labour', 'hire', 'employ', 'boss']
	logfile = 'work_tweets.json'
elif selection == 2:
	keywords = ['school', 'education', 'university', 'academy', 'college', 'teacher', 'classroom', 'education']
	logfile = 'school_tweets.json'
else:
	exit()
print('Stream for how long? (in seconds)')
runTime = input()
if type(runTime) != int:
	exit()


class TweetOutput:

	def __init__(self, filename):
		self.saveFile = filename
		try:
			gFile = open(filename, 'r')
			self.tweetList = json.load(gFile)
			gFile.close()
		except:
			self.tweetList = []

	def add(self, text):
		self.tweetList.append(text)

	def close(self):
		wFile = open(self.saveFile, 'w')
		json.dump(self.tweetList, wFile)
		wFile.close()


class MyStreamListener(tweepy.StreamListener):

	def __init__(self, time_limit, filename):
		self.start_time = time.time()
		self.limit = time_limit
		self.saveTweets = TweetOutput(filename)
		super(MyStreamListener, self).__init__()

	def on_status(self, status):
		if (time.time() - self.start_time) < self.limit:
			self.saveTweets.add(status.text.encode("utf-8"))
			return True
		else:
			self.saveTweets.close()
			print('\nTime limit of ' + str(self.limit) + ' seconds reached, stopping.\n')
			return False

	def on_error(self, status_code):
		if status_code == 420:
			print("\n### Rate Limited ###\n")
			#returning False in on_data disconnects the stream
			return False

	def on_limit(self, status):
		print('Limit threshold exceeded', status)

	def on_timeout(self, status):
		print('Stream disconnected; continuing...')


# Creating the stream
myStreamListener = MyStreamListener(runTime, logfile)
tStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)


# Starting the stream
tStream.filter(track=keywords)


