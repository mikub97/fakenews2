# import os
import pandas as pd
import csv
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
import seaborn as sb

sb_stemmer = SnowballStemmer("english",)
# before reading the files, setup the working directory to point to project repo
# reading data files


test_filename = '../../data/test.csv'
train_filename = '../../data/train.csv'
valid_filename = '../../data/valid.csv'

train_news = pd.read_csv(train_filename)
test_news = pd.read_csv(test_filename)
valid_news = pd.read_csv(valid_filename)

def process_words():
    a = np.asarray(test_news)
    tokens = []

    for row in a:
        tokens.append(tokenizer.tokenize(row[0]))

    print(tokens[1])
    stopWords = set(stopwords.words('english'))
    tokens2 = []

    a = np.asarray(tokens)
    for row in a:
        wordsFiltered = []
        for w in row:
            if w not in stopWords:
                w = w.lower()
                w = sb_stemmer.stem(w)
                wordsFiltered.append(w)
                #print(row)
        tokens2.append(wordsFiltered)
    print(tokens2[1])