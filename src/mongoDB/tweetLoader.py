import argparse
import json
import json as j
import sys

from tweepy import TweepError

from src.mongoDB.fetcher import Fetcher
from src.static import Cleaner
from src.static.Cleaner import clearTweetJson, clearUserJson
from src.TwitterConncection import TwitterConnection
import tweepy
import pymongo


class TweetLoader:

    def __init__(self, max_reply=1000, restart=True):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.users = self.mydb['users']

        # TwitterConncection object
        self.api = TwitterConnection().api
        if restart:
            self.mydb.drop_collection(name_or_collection="tweets")
            self.mydb.drop_collection(name_or_collection="users")
        self.max_reply = max_reply

    # Zapisuje użytkownika do BD
    def saveUser(self, screen_name, to_print=False):
        user = None
        try:
            user = self.api.get_user(screen_name=screen_name)
        except TweepError:
            print('No user with screen_name = ' + screen_name)
        if (user == None):
            raise Exception('No user with screen_name = ' + screen_name)
        self.users.insert_one(clearUserJson(user._json))
        if (to_print):
            print("User : ")
            print(json.dumps(clearUserJson(user._json), indent=2, sort_keys=True))
            print("is saved")

    # Zapisuje tweeta do BD
    def saveTweet(self, id, to_print=False, with_author=False):
        if (self.tweets.find_one({'id': id}) != None):
            return
        tweet = None
        try:

            tweet = self.api.get_status(id=id, tweet_mode='extended',
                               include_entities=True)
        except Exception:
            print('No tweet with id = ' + id.__str__())
        if tweet == None:
            raise Exception('No tweet with id = ' + id.__str__())
        if tweet.__getattribute__('lang') != 'en':
            return
        tweet = clearTweetJson(tweet._json)
        self.tweets.insert_one(tweet)
        if (to_print):
            print("Tweet :")
            print(tweet)
            print("is saved")
        if (with_author):
            self.saveUser(screen_name=tweet['screen_name'], to_print=to_print)
        return tweet

        # Zapisuje autora Tweetu

    def saveAuthor(self, id):
        tweet = self.api.get_status(id=id, tweet_mode='extended')
        self.users.insert_one(clearUserJson(self.api.get_user(screen_name=tweet.author.screen_name)))

    def saveLastTweetsOfAuthor(self, screen_name,to_print=False,size_for_bot=10):
        timeline =self.api.user_timeline(screen_name=screen_name, count=size_for_bot, tweet_mode='extended',
                               include_entities=True)
        tweets_count = self.tweets.count()
        for tweet in timeline:
            self.tweets.insert_one(clearTweetJson(tweet._json,connected_with_tweet=screen_name))    #connected_with_tweet = screen_name jeżeli to jest 1 z ostatnich tweetów ziomka

        if to_print:
            print("Last " +(self.tweets.count()-tweets_count).__str__() +" last tweets of the user inserted")

    def saveReplies(self, tweet, to_print=False, with_author=False):
        before_count = self.tweets.count()
        i = 0
        cursor = tweepy.Cursor(self.api.search, q='to:' + tweet['screen_name'].__str__(),
                               since_id=tweet['id'],
                               result_type='recent',tweet_mode='extended',
                               include_entities=True,
                               limit=self.max_reply).items()  # Dlaczego tak mało zwraca odpowiedzi !! ?? Przez result_type
        for reply in cursor:
            if i > self.max_reply:
                break
            if (reply._json['in_reply_to_status_id'] == tweet['id']):
                self.saveTweet(reply._json['id'], to_print=to_print, with_author=with_author)
            i = i + 1
        cursor = tweepy.Cursor(self.api.search, q='to:' + tweet['screen_name'].__str__(),
                               since_id=tweet['id'],
                               result_type='popular',tweet_mode='extended',
                               include_entities=True,
                               limit=self.max_reply).items()  # Dlaczego tak mało zwraca odpowiedzi !! ?? Przez result_type
        i = 0
        for reply in cursor:
            if i > self.max_reply:
                break
            if (reply._json['in_reply_to_status_id'] == tweet['id']):
                self.saveTweet(reply._json['id'], to_print=to_print, with_author=with_author)
            i = i + 1

        if (to_print):
            print((self.tweets.count() - before_count).__str__() + ' replies added\n')

    # Zapisuje Tweety, które są poszukując ich na zasadzie wystąpywania słów, można zaostrzyć filtrem tylko zweryfikowani autorzy
    def saveTweetsWithWords(self, words, connected_with_tweet=None,verified_authors_only=False, with_authors=False,
                            to_print=False,limit=10):
        words = words + "-filter:retweets"
        cursor = tweepy.Cursor(self.api.search, q=words, lang='en', result_type='recent',tweet_mode="extended",
                               include_entities=True, timeout=999999).items(limit)
        tweets = []
        i = 0
        while True:
            if i >= self.max_reply:
                return tweets
            try:
                tweet = cursor.next()
                tweet = clearTweetJson(tweet._json, connected_with_tweet)
                if tweet['id'] == connected_with_tweet:
                    break
                user = self.api.get_user(screen_name=tweet['screen_name'])
                user = clearUserJson(user._json)
                if verified_authors_only:
                    if (user['verified']):
                        self.tweets.insert_one(tweet)
                        if (to_print):
                            print("Tweet :")
                            print(tweet["full_text"])
                            print(["screen_name"])
                            print("is saved")
                        if (with_authors):
                            self.users.insert_one(user)
                            if (to_print):
                                print("User :")
                                print(user)
                                print("is saved")

                else:
                    self.tweets.insert_one(tweet)
                    if (to_print):
                        print("Tweet :")
                        print(tweet["full_text"])
                        print("is saved")
                    if (with_authors):
                        self.users.insert_one(user)
                        if (to_print):
                            print("User :")
                            print(user)
                            print("is saved")
                i = i + 1
            except StopIteration:
                return


        # Zapisuje Tweet, replies, author(opcjonalnie),  authors of replies (opcjonalnie)
    def saveTweetWithAllData(self, id=-1, to_print=False, with_author=True, with_authors_of_replies=False,
                                 connected_tweets=False,
                                 verified_authors_only=True,size_for_bot=10):
        tweet_count_before = self.tweets.count()
        user_count_before = self.tweets.count()

        self.saveTweet(id, to_print=to_print, with_author=with_author)
        tweet = self.tweets.find_one({'id': id})
        self.saveReplies(tweet, to_print=to_print, with_author=with_authors_of_replies)
        if tweet !=None :
            if to_print:
                print('Tweet to check, with id ' + id.__str__() + ', is saved')
        else:
            print("Failed do save tweet with all data. There is no post with id " +id.__str__())
            return
        replies_count = self.tweets.count()-tweet_count_before-1
        if connected_tweets:
           text = self.tweets.find_one({'id': id})['full_text']
           self.saveTweetsWithWords(Cleaner.getKeyWords(text), connected_with_tweet=id,
                    verified_authors_only=verified_authors_only, to_print=to_print,with_authors=with_authors_of_replies)
        connected_tweets_count = self.tweets.count() - replies_count-1
        self.saveLastTweetsOfAuthor(screen_name=tweet['screen_name'],size_for_bot=size_for_bot)
        if True:
            print()
            print((self.tweets.count() - tweet_count_before).__str__() + " tweets added into the DB")
            print((self.users.count() - user_count_before).__str__() + " users added into the DB")
            print(connected_tweets_count.__str__() + " connected tweets")



# 1133284566632787969
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pass an id of a tweet to check')
    parser.add_argument('-id', dest='id', default=-112,
                        help='id of tweet for analysis')
    parser.add_argument('--restart', dest='restart', action='store_const',
                        const=True, default=False,
                        help='restarts mongoDB')
    restart = parser.parse_args().restart
    id = int(parser.parse_args().id)
    if id==-112 :
        parser.print_usage()
        sys.exit()
    mongo=TweetLoader(restart=restart,max_reply=100)
    mongo.saveTweetWithAllData(id, to_print=False,with_authors_of_replies=True, connected_tweets=True,verified_authors_only=True,size_for_bot=15)


    # Pobieranie konkretnego tweeta, bez autora
    # mongo.saveTweet(id=1133184409127989248,to_print=True,with_author=False)

    # Pobieranie konkretnego użytkonika
    # mongo.saveUser(screen_name='potus',to_print=True)
    # Pobieranie konkretnego tweetu, jego autora, odpowiedziami do tweetu i ich autorami
    # mongo.saveTweetWithAllData(id=1133184409127989248,with_authors_of_replies=True,to_print=True)

    # Działanie pobierania tweetów powiązanych
    # mongo.saveTweetsWithWords(['Oklahoma','Japan'],connected_with_tweet='z tym ID',limit=100,verified_authors_only=True,to_print=True,with_authors=True)
