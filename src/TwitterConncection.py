import datetime
import json
import os
import re

import tweepy
from mechanize import urlopen
from textblob import TextBlob


class TwitterConnection:

    def __init__(self):
        # Load credentials
        with open("twitter-credentials.json") as file:
            credentials = json.load(file)
        try:
            self.auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
            self.auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
            self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
        except:
            print("Error: Authentication failed")
