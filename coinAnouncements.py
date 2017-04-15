def extractTweets():
   import pickle
   import datefinder
   import time
   
   tweets = pickel.loads(open("savedTweets.txt").read())
   
   for tweet in tweets:
      tweetJson = tweet._json
      userId = tweetJson["id"]
      tweetText = tweetJson["text"]
      retweets = tweetJson["retweet_count"]
      
      tweetDateText = tweet._json["created_at"]
      tweetDateTuple = [date for date in datefinder.find_dates(tweetDate)][0].timetuple()
      tweetDate = time.mktime(dateTimeTweetDate)
      currentTime = time.time()
      timeSinceTweet = (currentTime - currentTime) * 0.01
      
      importance = retweets/timeSinceTweet
      
      for event in events:
         if event in tweetText and not userId in usersPosted:
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
         for date in datefinder.find_dates(tweet):
            coinDates.append(date)
      coinTweets[coin]["dates"] = coinDates
      return coinTweets
         

validTweets = getCoinTweets()
categorizedTweets = categorizeTweets(validTweets)
coinEvents = extractEventDates(categorizedTweets)
for coin in coinEvents:
   print("Coin: \n\n" + coin + "\n\n\nTweets: \n\n" + "\n".join(coin["tweets"]) + "\n\n\nDates: \n\n" + "\n".join(coin["dates"]))
   print("\n\n\n\n")
