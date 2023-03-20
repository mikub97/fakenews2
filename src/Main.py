import sys
import csv
import joblib

from src.machinelearning import DataLoader
from src.machinelearning.Predictor import Predictor
from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader
from src.postCredibility import postCredibility
from src.static.Cleaner import clearTweetJson
from src.twitter.BotChecket import BotChecker
import argparse





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pass an id of a tweet to check')
    parser.add_argument('-id', dest='id', default=-112,
                        help='id of tweet for analysis')
    parser.add_argument('--restart', dest='restart', action='store_const',
                        const=True, default=False,
                        help='restarts mongoDB')
    parser.add_argument('--only-anal', dest='anal', action='store_const',
                        const=True, default=False,
                        help='if set there will be no more tweets loaded from twitter')
    anal = parser.parse_args().anal
    f = open("test.txt", "r")
    restart = parser.parse_args().restart
    id = int(parser.parse_args().id)
    fetcher = Fetcher()
    pC = postCredibility()
    predictor = Predictor()
    bot_checker = BotChecker()
    """
    if id==-112 :
        parser.print_usage()
        sys.exit()
    if (not anal):
        mongo=TweetLoader(restart=restart,max_reply=100)
        mongo.saveTweetWithAllData(id, to_print=False,with_authors_of_replies=True, connected_tweets=True,verified_authors_only=True,size_for_bot=15)
    """
    TrueNegative = 0;
    FalsePositive = 0;
    FalseNegative = 0;
    TruePositive = 0;
    for line in f:

        line = line.split(" ")
        x = line[0]
        y = int(line[1])
        print(x,y)
        x = int(x)

        mongo = TweetLoader(restart=restart, max_reply=10)
        mongo.saveTweetWithAllData(id=x, to_print=False, with_authors_of_replies=True, connected_tweets=True,
                                   verified_authors_only=True, size_for_bot=15)
        result = pC.evaluate(x)
        # print(result)
        Label_and_truth_prob = predictor.predict(x)
        # print(Label_and_truth_prob)
        #is_bot_result = bot_checker.is_fake_based_on_user(id)
        malicious_urls_machine_learning = bot_checker.is_fake_based_on_external_urls(x, True)
        #malicious_urls = bot_checker.is_fake_based_on_external_urls(id, False)
        load_model = joblib.load('judger.sav')
        input = [[result["probability"],Label_and_truth_prob["probability"],malicious_urls_machine_learning["probability"]]]
        prediction = load_model.predict(input)
        #prob = load_model.predict_proba(input)
        print(prediction[0])
        if prediction[0] == 1 and y == 0:
            TrueNegative+=1
            print('True negative.', TrueNegative)
        elif prediction[0] == 1 and y == 1:
            TruePositive+=1
            print('True positive.', TruePositive)
        elif prediction[0] == 0 and y == 1:
            FalseNegative+=1
            print('False negative.', FalseNegative)
        else:
            FalsePositive+=1
            print('False positive.', FalsePositive)



   
    
    #info = result["description"] +"\n"+ Label_and_truth_prob["description"] + "\n" +  malicious_urls_machine_learning["description"]
    #print(info)
    
    # print('\nGłówny tweet:')
    # print(clearTweetJson(fetcher.get_tweet(id=id),remove_entities=True))
    # print('\nAutora:')
    # print(fetcher.get_author_of_tweet(id=id))
    # print('\n')
    # # fetcher.print_users()


    """
    with open('true.csv', mode='w', newline='') as onion:
        onion_writer = csv.writer(onion, delimiter='|')

        for x in f:
            x=int(x)
            mongo = TweetLoader(restart=restart, max_reply=10)
            mongo.saveTweetWithAllData(id=x, to_print=False, with_authors_of_replies=True, connected_tweets=True,
                                       verified_authors_only=True, size_for_bot=15)
            result = pC.evaluate(x)
            #print(result)
            Label_and_truth_prob = predictor.predict(x)
            #print(Label_and_truth_prob)
            is_bot_result = bot_checker.is_fake_based_on_user(x)
            malicious_urls_machine_learning = bot_checker.is_fake_based_on_external_urls(x, True)
            malicious_urls = bot_checker.is_fake_based_on_external_urls(x, False)
            #print(malicious_urls_machine_learning)
            tweet = fetcher.get_tweet(x)
            onion_writer.writerow([tweet["full_text"],result["probability"],
                                   Label_and_truth_prob["probability"],
                                   malicious_urls_machine_learning["probability"]])
            print("saved to csv")
    """

