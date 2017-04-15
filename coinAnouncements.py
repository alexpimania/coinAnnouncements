def getSearchTerms():
   import json
   coinNames = json.loads(open("coinNames.txt").read())
   eventNames = json.loads(open("eventNames.txt").read())
   return [coinNames, eventNames]

def extractTweets(events):
   import pickle
   import datefinder
   import time
   
   tweets = pickle.loads(open("savedTweets.txt", "rb").read())
   validTweets = []
   for tweet in tweets:
      tweetJson = tweet._json
      userId = tweetJson["id"]
      tweetText = tweetJson["full_text"]
      retweets = tweetJson["retweet_count"]
      usersPosted = []
      
      tweetDateText = tweet._json["created_at"]
      tweetDateTuple = [date for date in datefinder.find_dates(tweetDateText)][0].timetuple()
      tweetDate = time.mktime(tweetDateTuple)
      currentTime = time.time()
      timeSinceTweet = (currentTime - tweetDate) * 0.01
      
      importance = retweets/timeSinceTweet
      if any(event in tweetText for event in events) and not userId in usersPosted and not tweetText in [tweet["tweet"] for tweet in validTweets]: 
         validTweets.append({"tweet":tweetText, "date":"", "importance":importance})
         usersPosted.append(userId) 
           
   return validTweets
   

def categorizeTweets(tweets):
   coinTweets = {}
   for tweet in tweets:
      for coin in coinNames:
         if coin in tweet["tweet"]:
            if not coin in coinTweets.keys():
               coinTweets[coin] = {}
               coinTweets[coin]["tweets"] = []
               coinTweets[coin]["dates"] = []
               coinTweets[coin]["importance"] = 0
               
            coinTweets[coin]["tweets"].append(tweet["tweet"])
            coinTweets[coin]["importance"] += tweet["importance"]
   return coinTweets
   

def extractEventDates(coinTweets):
   import datefinder
   coinEvents = {}
   for coin in coinTweets:
      coinDates = []
      for tweet in coinTweets[coin]["tweets"]:
         coinDates.extend([str(date) for date in datefinder.find_dates(tweet)])
      coinTweets[coin]["dates"] = coinDates
   return coinTweets
         
         
coinNames, eventNames = getSearchTerms() 
validTweets = extractTweets(eventNames)
categorizedTweets = categorizeTweets(validTweets)
coinEvents = extractEventDates(categorizedTweets)
for coin in coinEvents:
   print("Coin: " + coin + "\nTweets: \n" + "\n".join(coinEvents[coin]["tweets"]) + "\nDates: \n" + "\n".join(coinEvents[coin]["dates"]) + "\nImportance: " + str(coinEvents[coin]["importance"]))
   print("\n\n")
