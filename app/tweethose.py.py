# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 11:12:26 2017

@author: Mike
"""

import os
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import time
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt

sid = SentimentIntensityAnalyzer()
stops = stopwords.words('english')
stemmer = WordNetLemmatizer()


consumer_key = os.environ["TWITTER_API_KEY"]
consumer_secret = os.environ["TWITTER_API_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

# AUTHENTICATE

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# INITIALIZE API CLIENT

api = tweepy.API(auth)

text = []
loc = []
sent = []


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener, self).__init__()
    
    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:
            text.append(status.text)
            sent.append(sid.polarity_scores(status.text)['compound'])
            loc.append(status.user.time_zone)
            #print(time.time() - self.start_time)
        else:
            return False
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
        
    

            
print("----------------------------------------------------")
print("Welcome to TweetHose, an app for visualizing tweets")
print("----------------------------------------------------\n\n")
keyword = input("Keyword to search for: ")
run_time = input("Tweet collection time (in minutes): ")
print("\nListening...")

stream = tweepy.Stream(auth=api.auth, listener = MyStreamListener(time_limit=int(run_time)*60))
stream.filter(track=[keyword])

print('\nDone listening! %s tweets collected.' %len(text))

tweetdata = pd.DataFrame([text, loc, sent]).transpose()
tweetdata.columns = ['text', 'loc', 'sent']

print('\nCreating pie chart of top 10 locations...')
tweetdata['loc'].value_counts()[0:9].plot(kind='pie')
print('\nCreating histogram of tweet sentiment...')
twtsent = tweetdata['sent']
plt.figure(0)
plt.hist(twtsent)
plt.show()
print('\nGenerating wordcloud of tweet texts...')

usernames = re.compile(r'@([A-Za-z0-9_]+)')
alpha = re.compile('[^a-zA-Z]')
stops.append(keyword.lower())
stops = stops + ['rt', 'co', 'com']
def preprocess(tweets):
    tweets = usernames.sub(' ', tweets)
    tweets = alpha.sub(' ', tweets)
    lower = tweets.lower()
    tokens = word_tokenize(lower)
    tokens = [word for word in tokens if word not in stops]
    stemmed = [stemmer.lemmatize(word) for word in tokens]
    return ' '.join(stemmed)
    
    
proc = [preprocess(tweet) for tweet in text]
cloud = wordcloud.WordCloud().generate(' '.join(proc))
plt.figure()
plt.imshow(cloud)
plt.show()
