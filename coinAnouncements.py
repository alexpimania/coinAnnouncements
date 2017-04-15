def getSearchTerms():
   import json
   return json.loads(open("searchTerms.txt").read())

def removeLink(text):
   import re
   link = re.search("(?P<url>https?://[^\s]+)", text)
   if link:
      link = link.group("url")
      text = text.replace(link, "").replace("  ", " ")
   return text

def extractTweets(events):
   import pickle
   from datefinder import find_dates as extractDate
   import time
   
   tweets = pickle.loads(open("savedTweets.txt", "rb").read())
   announcements = []
   for tweet in tweets:
      data = tweet._json
      text = removeLink(data["full_text"])
      likes = data["favorite_count"]
      dateText = data["created_at"]
      
      dateTuple = [date for date in extractDate(dateText)][0].timetuple()
      ageDays = (time.time() - time.mktime(dateTuple)) / (24*60*60)
      
      importance = likes
      if any(event in text.lower() for event in events) and not text.lower() in [tweet["tweet"].lower() for tweet in announcements]: 
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
      print(tweet + " || Age: " + str(round(tweets[tweet], 2)) + " days")
   print("\n\n")
