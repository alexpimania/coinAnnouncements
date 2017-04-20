daysToScan = 2


def removeLink(text):
   import re
   while True:
      link = re.search("(?P<url>https?://[^\s]+)", text)
      if link:
         text = text.replace(link.group("url"), "").replace("  ", " ") 
      else: break
   return text
   
   
def getSearchTerms():
   import json
   from poloniex import Poloniex
   polo = Poloniex()
   
   eventNames = ["upgrade", "updates", "releas", "testing", "aplha", "beta", "announce", "interview", "major", "launch", "add", "improve", "v1"]
   coinMarketList = [market[market.index("_") + 1:] for market in polo.return24hVolume().keys() if "BTC_" in market]
   coinList = polo.returnCurrencies()
   coinNames = []
   ignoredCoins = ["burst", "clams", "counterparty", "expanse", "dash", "horizon", "magi", "nem", "nexium", "nxt", "omni", "radium", "ripple", "shadow", "stellar", "tether"]
   for coin in coinList:
      if not coinList[coin]["name"].lower() in ignoredCoins and coin in coinMarketList:
         coinNames.append(coinList[coin]["name"].lower())
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
    
    
def getTwitterTweets(coinNames, period):
   import tweepy
   import time
   from datetime import datetime
   import string
   tweets = []
   usersTweets = {}
   
   twitterKeys = open("twitterKeys.txt").read().strip().split() 
   auth = tweepy.OAuthHandler(twitterKeys[0], twitterKeys[1])
   auth.set_access_token(twitterKeys[2], twitterKeys[3])
   api = tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)
   
   sinceDate = datetime.fromtimestamp(time.time() - period).strftime('%Y-%m-%d')
   for chunk in chunks(coinNames, 10):
      for tweet in tweepy.Cursor(api.search, q=" OR ".join(chunk), tweet_mode="extended", since=sinceDate, lang="en").items(1000):
         tweetText = removeLink(tweet._json["full_text"]).lower()
         translator = str.maketrans('', '', string.punctuation)
         tweetText = tweetText.translate(translator)
         tweet._json["full_text"] = tweetText
         if not tweet._json["user"]["id"] in usersTweets.keys():
            usersTweets[tweet._json["user"]["id"]] = []
         if not tweetText in usersTweets[tweet._json["user"]["id"]]:
            tweets.append(tweet)
            usersTweets[tweet._json["user"]["id"]].append(tweetText)
   return tweets
   
   
def saveTweets(tweets):
   import pickle
   with open("savedTweets.txt", "wb") as tweetsFile:
      tweetsFile.write(pickle.dumps(tweets))
      
               
coinNames, eventNames = getSearchTerms()           
api = initTwitterApi()
tweets = getTwitterTweets(coinNames, daysToScan)
saveTweets(tweets)
