import re
import pymongo

class Fetcher():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.users = self.mydb['users']

    def get_tweet(self,id):
        return self.tweets.find_one({'id':id})


    def get_user(self,screen_name):
        return self.users.find_one({'screen_name':screen_name})

    def get_users_last_tweets(self,screename):
        cursor = self.tweets.find({"connected_with_tweet": screename})
        connected = []
        while True:
            try:
                connected.append(cursor.next())
            except StopIteration:
                return connected

    def get_author_of_tweet(self,id):
        id=int(id)
        tweet = self.get_tweet(id)
        if (tweet == None):
            return None
        return self.users.find_one({'screen_name':tweet['screen_name']})

    def get_connected(self,id):
        cursor =  self.tweets.find({"connected_with_tweet":id})
        connected=[]
        while True:
            try:
                connected.append(cursor.next())
            except StopIteration:
                    return connected

    def get_replies(self, id,verified_authors_only=False):
        cursor =  self.tweets.find({'in_reply_to_status_id':id})
        replies=[]
        verified_replies=[]
        while True:
            try:
                replies.append(cursor.next())
            except StopIteration:
                if verified_authors_only:
                    for reply in replies:
                        if self.get_author_of_tweet(id=reply['id'])['verified'] == True:
                            verified_replies.append(reply)
                    return verified_replies
                else:
                    return replies

    def print_stats(self,id=None):
        print("There are " + self.users.count().__str__() + " users in db")
        print("There are " + self.tweets.count().__str__() + " tweets in db")
        if id != None:
            print("With number of " + self.tweets.find({'connected_with_tweet':id}).count().__str__() + " connected to " + id.__str__())
            print("With number of " + self.tweets.find({'connected_with_tweet':id}).count().__str__() + " connected to " + id.__str__())




    def print_tweets(self):
        i=1
        print("TWEETS:")
        for x in self.tweets.find():
            print(i.__str__()+".")
            print(x)
            print('\n')
            i=i+1
    def print_users(self):
        i=1
        print("USERS:")
        for x in self.users.find():
            print(i.__str__()+".")
            print(x)
            print('\n')
            i=i+1

if __name__ == '__main__':
    fetch = Fetcher()
