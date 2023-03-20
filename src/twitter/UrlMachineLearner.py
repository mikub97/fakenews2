import random

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class UrlMachineLearner:
    def __init__(self):
        self.url = 'data.csv'

    def is_url_malicious(self, link):

        url_csv = pd.read_csv(self.url, ',', error_bad_lines=False)
        url_df = pd.DataFrame(url_csv)
        url_df = np.array(url_df)
        random.shuffle(url_df)
        y = [d[1] for d in url_df]
        urls = [d[0] for d in url_df]

        vectorizer = TfidfVectorizer()  # using default tokenizer
        x = vectorizer.fit_transform(urls)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        lgr = LogisticRegression()  # Logistic regression
        lgr.fit(x_train, y_train)
        score = lgr.score(x_test, y_test)

        x_predict = [link]
        x_predict = vectorizer.transform(x_predict)
        y_predict = lgr.predict(x_predict)


        if y_predict[0] == 'bad':
            malicious = True
        else:
            malicious = False

        result = {
            'malicious': malicious,
            'score': score
        }

        return result

# Sample Invoke
if __name__ == '__main__':
    obj = UrlMachineLearner()
    url_malicious = obj.is_url_malicious('www.itidea.it/centroesteticosothys/img/_notes/gum.exe')
    if url_malicious['malicious']:
        result = {
            'Fake': True,
            'Probability': url_malicious['score']
        }
    else:
        result = {
            'Fake': False,
            'Probability': url_malicious['score']
        }
