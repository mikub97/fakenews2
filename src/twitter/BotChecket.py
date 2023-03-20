import datetime

import requests

from mongoDB.fetcher import Fetcher
from src.TwitterConncection import TwitterConnection
from src.twitter.UrlMachineLearner import UrlMachineLearner


class BotChecker:

    def __init__(self):
        self.api = TwitterConnection().api
        self.fetcher = Fetcher()

    # Checking if tweet is fake based on frequency of posting the tweets
    def isBot(self, tweet):
        retweet = tweet['retweet_count']
        if retweet > 0:
            result = {
                # nie fake
                'probability': 1,
                'description': 'Tweet był retweetowany - to nie jest bot'
            }
            return result
        else:
            user = tweet['user']
            user_name = user['screen_name']
            # last_tweets = self.api.user_timeline(screen_name=user_name, count=10, tweet_mode='extended',
            #                                      include_entities=True)

            last_tweets = self.fetcher.get_users_last_tweets(user_name)

            if len(last_tweets) < 10:
                result = {
                    # fake
                    'probability': 0.3,
                    'description': 'User nie opublikowal 10 tweetow - uznajemy za bota'
                }
                return result
            else:
                result = {
                    'probability': -1,
                    'description': 'default value'
                }
                for idx, tweet in enumerate(last_tweets):
                    if idx > 0:
                        current_tweet_date = last_tweets[idx].created_at
                        tweet_date = last_tweets[idx - 1].created_at
                        two_days = datetime.timedelta(days=2)
                        five_days = datetime.timedelta(days=5)
                        if (tweet_date - current_tweet_date) < two_days:
                            # nie fake
                            result['probability'] = 1
                            result['description'] = 'User publikuje z czestotliwoscia wieksza niz dwa dni - to nie ' \
                                                    'jest bot '
                        elif two_days < (tweet_date - current_tweet_date) < five_days:
                            # fake
                            result['probability'] = 0.4
                            result['description'] = 'User nie publikowal nic przez 3,4 lub 5 dni - uzanje za bota z ' \
                                                    'prawd.=0.6 '
                        else:
                            # fake
                            result['probability'] = 0.1
                            result['description'] = 'User ma odstep miedzy tweetami wiekszy niz 5 dni - uznaje ' \
                                                    'za bota z prawd.=0.8 '
            return result

    # Checking if tweet is fake based on external urls provided in a tweet
    def is_fake_external_urls(self, tweet, useMachineLearning):
        entities = tweet['entities']
        urls = entities['urls']
        # urls = tweet.entities['urls']
        result = {
            'probability': -1,
            'description': 'default value'
        }
        if len(urls) <= 0:
            result['probability'] = -1
            result['description'] = 'Brak URLi w tweecie'
            return result
        for url in urls:
            full_url = url['expanded_url']
            if not useMachineLearning:
                try:
                    headers = requests.utils.default_headers()
                    headers.update(
                        {
                            'User-Agent': 'My User Agent 1.0',
                        }
                    )
                    response = requests.get(full_url, headers=headers)
                    http_code = response.status_code
                    if (http_code / 100) >= 4:
                        # fake
                        result['probability'] = 0
                        result['description'] = 'Wylaczono machine learning, kod HTTP jest nieprawidlowy'
                        return result
                    else:
                        # nie fake
                        result['probability'] = 1
                        result['description'] = 'Wylaczono machine learning, kod HTTP jest prawidlowy'
                except:
                    # fake
                    result['probability'] = 0
                    result[
                        'description'] = 'Wylaczono machine learning, Url nie rzuca bledem ale nieznany jest content url'
                    return result
                return result
            else:
                data_machine_learner = UrlMachineLearner()
                url_malicious = data_machine_learner.is_url_malicious(full_url)

                if url_malicious['malicious']:
                    # fake
                    score = 1 - url_malicious['score']
                    result['probability'] = score
                    result['description'] = 'wlaczono machine learning'
                    return result
                else:
                    # nie fake
                    result['probability'] = url_malicious['score']
                    result['description'] = 'wlaczono machine learning'
            return result

    # method to be used by other modules
    def is_fake_based_on_user(self, tweetId):
        tweet = self.fetcher.get_tweet(tweetId)
        return self.isBot(tweet)

    # method to be used by other modules
    def is_fake_based_on_external_urls(self, tweetId, isMachineLearning):
        tweet = self.fetcher.get_tweet(tweetId)
        return self.is_fake_external_urls(tweet, isMachineLearning)
