import json
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob
from nltk.tag import pos_tag

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                           "|(\w+:\/\/\S+)",
                           " ",
                           tweet).split())

def getTweetSentiments(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity


def nazwy_wlasne(text):
    text = clean_tweet(text)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tagged_sent = pos_tag(tokens)
    propernouns = [word for word, pos in tagged_sent if pos == 'NNP']
    return propernouns

def getKeyWords(text):
    wlasne = nazwy_wlasne(text)
    strings = ' '.join(wlasne)
    strings = ' '.join(word for word in strings.split() if len(word) > 2)  # dluzsze niz 2 litery
    return strings

def clearTweetJson(json, connected_with_tweet=None,remove_entities=False):
    toDeleteAttr = ['metadata', 'quoted_status', 'id_str', 'user', 'place', 'favorited', 'retweeted',
                    'coordinates', 'contributors', 'source', 'truncated', 'geo', 'in_reply_to_status_id_str',
                    'in_reply_to_user_id', 'in_reply_to_user_id_str', '_id', 'extended_entities', 'retweeted_status',
                    'quoted_status_id_str']
    if remove_entities:
        toDeleteAttr.append('entities')
        toDeleteAttr.append('extended_entities')
    json['user_mentions'] = []
    json['hashtags'] = []
    json['connected_with_tweet'] = connected_with_tweet
    try:
        for user_mention in json['entities']['user_mentions']:
            json['user_mentions'].append(user_mention['screen_name'])
    except:
        pass
    try:
        json['screen_name'] = json['user']['screen_name']
    except:
        pass
    try:
        for hash in json['entities']['hashtags']:
            json['hashtags'].append(hash['text'])
    except:
        pass
    try:
        for user_mention in json['entities']['user_mentions']:
            json['user_mentions'].append(user_mention['screen_name'])
    except:
        pass

    for attr in toDeleteAttr:
        try:
            del json[attr]
        except:
            pass

    return json


def clearUserJson(json):
    toDeleteAttr = ['metadata', 'quoted_status', 'id_str','entities', 'user', 'place', 'favorited', 'retweeted',
                    'coordinates', 'contributors', 'source', 'truncated', 'geo', 'in_reply_to_status_id_str',
                    'in_reply_to_user_id', 'in_reply_to_user_id_str', '_id', 'extended_entities', 'retweeted_status',
                    'quoted_status_id_str', 'default_profile_image', 'status', "notifications",
                    "profile_background_color", "profile_background_image_url", "profile_background_image_url_https",
                    "profile_background_tile", "profile_banner_url", "profile_image_url", "profile_image_url_https",
                    "profile_link_color", "profile_sidebar_border_color", "profile_sidebar_fill_color",
                    "profile_text_color",
                    "profile_use_background_image", "translator_type", "url", "utc_offset", "id", "follow_request_sent",
                    "default_profile"]
    for attr in toDeleteAttr:
        try:
            del json[attr]
        except:
            pass
    return json


def getTweetSubjectivity(text):
    analysis = TextBlob(clean_tweet(text))
    return analysis.sentiment[1]

#
def process_words(text):
    tokenizer = RegexpTokenizer(r'\w+')
    sb_stemmer = SnowballStemmer("english",)
    tokens = tokenizer.tokenize(text)
    stopWords = set(stopwords.words('english'))
    wordsFiltered = []
    for w in tokens:
        if w not in stopWords:
            #w = w.lower()
            w = sb_stemmer.stem(w)
            wordsFiltered.append(w)

    return wordsFiltered


