from sklearn.externals import joblib
import datetime
import numpy as np
import pandas

def predict_nH1B(date=pandas.to_datetime('2014-02-01')):
    regr = joblib.load('/Users/bauer/insight/teleborder/data/my_model.pkl')
    x1 = joblib.load('/Users/bauer/insight/teleborder/data/x1.pkl')
    x2 = joblib.load('/Users/bauer/insight/teleborder/data/x2.pkl')
    norms = joblib.load('/Users/bauer/insight/teleborder/data/norms.pkl')
    prediction = 0
    try:
        prediction = regr.predict(np.array([x2.reindex([date],method='bfill'),x2.reindex([date],method='bfill'),date.month]).T)
        prediction = (norms[1]*prediction + norms[0])[0]
    except:
        pass
    return prediction, regr.coef_[:3], norms[2:5]

if __name__ == '__main__':
    predict_nH1B()