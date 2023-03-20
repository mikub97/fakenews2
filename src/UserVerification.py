from src.mongoDB.fetcher import Fetcher


def verifyUser(id):
    user = Fetcher().get_user(id)
    out = {'verified' : False,
           'credibility': 0.0}
    if user['verified']==True:
        out['verified']=True
        out['credibility']=1.0
        return out
    else :
        out['verified'] = False
        out['credibility'] = 1.0
