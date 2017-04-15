daysToScan = 3

def getSearchTerms():
   import json
   coinNames = json.loads(open("coinNames.txt").read())
   eventNames = json.loads(open("eventNames.txt").read())
   return [coinNames, eventNames]


def chunks(listToCut, maxLength):
    for i in range(0, len(listToCut), maxLength):
        yield listToCut[i:i+maxLength]
        
        
def initTwitterApi():
   import tweepy
   twitterKeys = open("twitterKeys.txt").read().strip().split() 
   auth = tweepy.OAuthHandler(twitterKeys[0], twitterKeys[1])
   auth.set_access_token(twitterKeys[2], twitterKeys[3])
   api = tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)
   return api
    
def downloadTweets(daysToScan):s
   import tweepy
   import time
   from datetime import datetime
   
   tweets = []
   sinceDate=datetime.fromtimestamp(time.time() - 60*60*24 * daysToScan).strftime('%Y-%m-%d')
   for chunk in chunks(coinNames, 10):
      print(chunk)
      coinsQuery = " OR ".join(chunk)
      for tweet in tweepy.Cursor(api.search, q=coinsQuery, since=sinceDate, lang="en").items(1000):
         tweets.append(tweet)
   return tweets
   
def saveTweets(tweets):
   import pickle
   with open("savedTweets.txt", "w+") as tweetsFile:
      tweetsFile.write(pickle.dumps(tweets))
      

   
               
coinNames, eventNames = getSearchTerms()           
api = initTwitterApi()
tweets = downloadTweets(daysToScan)
saveTweets(tweets)
