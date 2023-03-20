import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


test_filename = '../data/test.csv'
train_filename = '../data/train.csv'
valid_filename = '../data/valid.csv'

train_news = pd.read_csv(train_filename)
test_news = pd.read_csv(test_filename)
valid_news = pd.read_csv(valid_filename)


stemmer = SnowballStemmer('english')
train_s=[' '.join([stemmer.stem(word) for word in text.split(' ')])
          for text in train_news['Statement']]
test_s=[' '.join([stemmer.stem(word) for word in text.split(' ')])
          for text in test_news['Statement']]



lemmatizer = nltk.stem.WordNetLemmatizer()
train_l=[' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])
          for text in train_news['Statement']]
test_l=[' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])
          for text in test_news['Statement']]

train_sl=[' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])
          for text in train_s]
test_sl=[' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])
          for text in test_s]

def stem (sentence):
    answ = [' '.join([stemmer.stem(word) for word in text.split(' ')])
          for text in sentence]

    return answ

def lemmatize (sentence):
    answ = [' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])
          for text in sentence]

    return answ
