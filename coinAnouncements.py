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

def extractTweets(events):
   import pickle
   from datefinder import find_dates as extractDate
   import time
   
   tweets = pickle.loads(open("savedTweets.txt", "rb").read())
   announcements = []
   for tweet in tweets:
      data = tweet._json
      text = data["full_text"]
      likes = data["favorite_count"]
      dateText = data["created_at"]
      
      dateTuple = [date for date in extractDate(dateText)][0].timetuple()
      ageDays = (time.time() - time.mktime(dateTuple)) / (24*60*60)
      importance = likes
      if any(event in text for event in events):
         announcements.append({"tweet" : text, "importance" : importance, "ageDays" : ageDays})
   return announcements
   

def getCoinTweets(tweets):
   coinTweets = {}
   for tweet in tweets:
      for coin in coinNames:
         if coin in tweet["tweet"]:
            if not coin in coinTweets.keys():
               coinTweets[coin] = {}
               coinTweets[coin]["tweets"] = {}
               coinTweets[coin]["importance"] = 0
               
            coinTweets[coin]["tweets"][tweet["tweet"]] = tweet["ageDays"]
            coinTweets[coin]["importance"] += tweet["importance"]
   return coinTweets

         
         
coinNames, eventNames = getSearchTerms() 
validTweets = extractTweets(eventNames)
coinTweets = getCoinTweets(validTweets)
for coin in sorted(coinTweets, key=lambda k: 0 - coinTweets[k]["importance"]):
   tweets = coinTweets[coin]["tweets"]
   print("Coin: " + coin)
   print("Importance: " + str(coinTweets[coin]["importance"]))
   for tweet in tweets:
      print(tweet.strip() + " || Age: " + str(round(tweets[tweet], 2)) + " days")
   print("\n\n")
