#the Twitter API was hard, so I opted for Twython: https://twython.readthedocs.org/en/latest/

from twython import Twython

import csv

#this part sucks, getting all your secret keys and such from Twitter API: https://dev.twitter.com/docs/auth/tokens-devtwittercom

APP_KEY = "app key here, a bunch of numbers"
APP_SECRET = "app secret here, a bunch more numbers"
OAUTH_TOKEN = "more numbers for your oauth token"
OAUTH_TOKEN_SECRET = "last secret token"

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#make a list of friends
allfriendsIDs = []
sn = "your_twitter_username"

#get your friends_ids first 
response = twitter.get_friends_ids(screen_name = sn)
friends = response['ids']
allfriendsIDs += friends

#now get their information, in batches of 100 because someone told me Twitter doesn't like you to get lots of people at once (what do i know though) 
def getUserDetails(ids):
	userDetails = []
	if len(ids) > 100:
		response = twitter.lookup_user(user_id = ','.join(str(a) for a in ids[0:99]))
		userDetails += response
		return getUserDetails(ids[100:]) + userDetails
	else:
		response = twitter.lookup_user(user_id = ','.join(str(a) for a in ids))
		userDetails += response
		return userDetails

details = getUserDetails(allfriendsIDs)
keys = details[0].keys()

#spit this all into a csv so i can manually go through and mark MALE or FEMALE
csvout = open("my_twitter_friends.csv","wb")
writer = csv.writer(csvout)
friends = ['name', 'screen_name', 'following'] #you can put even more parameters in here if you want 
writer.writerow(friends)

#unicode shit fight
import unicodedata
for detail in details:
	tmp = []
	for key in friends:
		try:
			tmp.append(unicodedata.normalize('NFKD', detail[key]).encode('ascii','ignore'))
		except:
			tmp.append(str(detail[key]))
			writer.writerow(tmp)
csvout.close()
