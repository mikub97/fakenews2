from sklearn.naive_bayes import MultinomialNB

import DataLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import  LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, f1_score, classification_report, recall_score,precision_score
import numpy as np
from sklearn.model_selection import GridSearchCV

train_S=DataLoader.train_s
train_L=DataLoader.train_news['Label']

test_S=DataLoader.test_s
test_L=DataLoader.test_news['Label']


pipeline_TlogR= Pipeline ([('LogTfidf',TfidfVectorizer()),
        ('LogR_clf',LogisticRegression())])

parameters_TlogR = {'LogTfidf__ngram_range': [(1, 1),(1,2),(1,3)],
              'LogTfidf__stop_words':['english'],
               'LogTfidf__use_idf': (True, False),
               'LogTfidf__smooth_idf': (True, False),
                'LogR_clf__solver': ['lbfgs', 'liblinear', 'newton-cg']    }
grid_logT = GridSearchCV(pipeline_TlogR, param_grid=parameters_TlogR, cv=4)

grid_logT.fit(train_S, train_L)

pipeline_CVlogR = Pipeline([('LogCV',CountVectorizer()),
        ('LogR_clf',LogisticRegression())])

parameters_CVlogR = {
    'LogCV__ngram_range': [(1, 1), (1, 2),(1,3)],
    'LogCV__stop_words':['english'],
    'LogR_clf__solver': ['lbfgs', 'liblinear', 'newton-cg']
}

grid_CVlogR = GridSearchCV(pipeline_CVlogR, param_grid=parameters_CVlogR, cv=4)

grid_CVlogR.fit(train_S, train_L)

pipeline_CVNB = Pipeline([('NBCV',CountVectorizer()),
        ('nb_clf',MultinomialNB())])

parameters_CVNB = {
    'NBCV__ngram_range': [(1, 1), (1, 2),(1,3)],
    'NBCV__stop_words':['english']
}

grid_CVNB = GridSearchCV(pipeline_CVNB, param_grid=parameters_CVNB, cv=4)

grid_CVNB.fit(train_S, train_L)


pipeline_TNB = Pipeline ([('NBTfidf',TfidfVectorizer()),
        ('NB_clf', MultinomialNB())])

parameters_TNB = {'NBTfidf__ngram_range': [(1, 1),(1,2),(1,3)],
                  'NBTfidf__stop_words':['english'],
                'NBTfidf__use_idf': (True, False),
                'NBTfidf__smooth_idf': (True, False)
                 }

grid_NBT = GridSearchCV(pipeline_TNB, param_grid=parameters_TNB, cv=4)

grid_NBT.fit(train_S, train_L)


predicted_LogR = grid_logT.best_estimator_.predict(test_S)
predicted_NB = grid_NBT.best_estimator_.predict(test_S)
predicted_CVNB = grid_CVNB.best_estimator_.predict(test_S)
predicted_CVlogR = grid_CVlogR.best_estimator_.predict(test_S)

mean_logT = np.mean(predicted_LogR == test_L)
mean_NBT = np.mean(predicted_NB == test_L)
mean_LogCV = np.mean(predicted_CVlogR == test_L)
mean_CVNB = np.mean(predicted_CVNB == test_L)

print(grid_logT.best_params_)


model_file = 'prediction_model.sav'

joblib.dump(grid_logT.best_estimator_,model_file)

print("NBT: ",mean_NBT)
print("logRT: ",mean_logT)
print("NBCV: ",mean_CVNB)
print("logRCV: ",mean_LogCV)

#build_confusion_matrix()