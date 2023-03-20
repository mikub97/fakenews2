import joblib
from src.machinelearning import DataLoader
from src.mongoDB.fetcher import Fetcher


class Predictor:

    def __init__(self):
        self.load_model = joblib.load('./machinelearning/prediction_model.sav')

    def predict(self, id):
        fetcher = Fetcher()
        load_model = joblib.load('./machinelearning/prediction_model.sav')
        tweet = fetcher.get_tweet(id)
        input = DataLoader.stem([tweet['full_text']])
        prediction = load_model.predict(input)
        prob = load_model.predict_proba(input)
        answ = {}
        if prediction[0] == 'True':
            answ['description'] = 'ML model DOES NOT classify this as a Fake News.'
        else:
            answ['description'] = 'ML model classifies this as a Fake News.'
        answ['probability'] = prob[0][0]

        return (answ)



