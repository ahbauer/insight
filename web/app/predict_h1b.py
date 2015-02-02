import os
import time
from sklearn.externals import joblib
import datetime
import numpy as np
import pandas
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import seaborn


def predict_nH1B(date=pandas.to_datetime('2014-02-01')):
    regr = joblib.load('/Users/bauer/insight/teleborder/data/my_model.pkl')
    (sents_model, sp500_model, empl_model, trend_model) = joblib.load('/Users/bauer/insight/teleborder/data/xdata.pkl')
    norms = joblib.load('/Users/bauer/insight/teleborder/data/norms.pkl')
    month_flags = [1,1,4,1,1,2,1,1,1,1,1,1]
    
    # print sents_model
    # print sp500_model
    # print empl_model
    # print trend1_model
    # print trend2_model
    # print trend3_model
    # print trend4_model
    # return 0, np.zeros(9), np.zeros(9)
    time_ordinal = (date.toordinal()-norms[2])/norms[3]
    
    x1 = sents_model.reindex([date],method='ffill')
    x2 = sp500_model.reindex([date],method='ffill')
    x3 = empl_model.reindex([date],method='ffill')
    x4 = trend_model.reindex([date],method='ffill')
    x5 = x1+time_ordinal
    x6 = x2+time_ordinal
    x7 = x3+time_ordinal
    x8 = x4+time_ordinal
    x9 = month_flags[date.month]
    x10 = time_ordinal
    
    prediction = 0
    prediction = regr.predict(np.array([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]).T)
    prediction = (norms[1]*prediction + norms[0])[0]
    
    return prediction, [25.56,22.10,18.80,18.19], norms[4:]

def make_figure(date=pandas.to_datetime('2014-02-01'), pred=80000):
    
    (prediction_series,month_series) = joblib.load('/Users/bauer/insight/teleborder/data/pred.pkl')
    # fig = plt.Figure()
    # ax0 = fig.add_subplot(111)
    # ax0.plot(month_series['2005':].values, month_series['2005':].index,label='H1B Rate')
    # ax0.plot(prediction_series.values,prediction_series.index,label='Model',color='red')
    # ax0.plot([date],[pred],'go')
    #ax0 = prediction_series.plot(label='Prediction',color='red')
    
    point_series = pandas.Series([pred],index=[date + datetime.timedelta(days=30)])
    
    ax0 = None
    fig = plt.figure()
    #ax0 = fig.add_subplot(111)
    month_series['2005':].plot(label='H1B Rate',color='blue')
    prediction_series.plot(label='Prediction',color='red')
    ax0 = point_series.plot(label='Your Date',style='go',markersize=10)
    ax0.set_xlabel('Date')
    ax0.set_ylabel('Number of H1B Applications')
    ax0.legend()
    #fig = ax0.get_figure()
    #os.system('rm /Users/bauer/insight/teleborder/web/app/static/imgs/dynamicfig.png')
    fig.savefig('/Users/bauer/insight/teleborder/web/app/static/imgs/dynamicfig.png')
    #while not os.path.exists('/Users/bauer/insight/teleborder/web/app/static/imgs/dynamicfig.png'):
    #    time.sleep(0.5)
    #time.sleep(1)
    return

if __name__ == '__main__':
    predict_nH1B()