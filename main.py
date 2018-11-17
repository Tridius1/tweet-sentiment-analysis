import json

import twitter
from textblob import TextBlob


#Credentials
inFile = open("credentials.json", 'r')
credentials = json.load(inFile)
inFile.close()

#Declaring API Object
TwAPI = twitter.Api(consumer_key=credentials['twitter']['consumer_key'],
	consumer_secret=credentials['twitter']['consumer_secret'],
	access_token_key=credentials['twitter']['access_token'],
	access_token_secret=credentials['twitter']['access_token_secret'])



#Testing
def searchSentiment():
	print("Enter query:")
	query = str(raw_input()).replace(" ", "%20")
	print("How many tweets?")
	num = str(raw_input())

	results = TwAPI.GetSearch(
	    raw_query="l=en&result_type=popular&q=" + query + "&count=" + num)

	print("l=en&result_type=popular&q=" + query + "&count=" + num + "\n")

	for status in results:
		tb = TextBlob(status.text)
		out = '[\n' + status.created_at + '\n'
		out += "User: " + status.user.name + " (" + status.user.screen_name + ") \n"
		out += "\n     | " + status.text.replace("\n", "\n     | ") + '\n\n'
		out += "(  RTs: " + str(status.retweet_count) + "  Likes: " + str(status.favorite_count) + "  )\n"
		out += str(tb.sentiment) + '\n]\n'

		print(out)
