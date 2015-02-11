import os
import time
from sklearn.externals import joblib
import datetime
from random import randint
import numpy as np
import pandas
import dateutil.relativedelta
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import seaborn
seaborn.set_style("whitegrid")

def predict_nH1B(date=pandas.to_datetime('2015-03'),suffix=''):
    regr = joblib.load('../data/my_model'+suffix+'.pkl')
    (sents_model, sp500_model, empl_model, trend_model) = joblib.load('../data/xdata'+suffix+'.pkl')
    norms = joblib.load('../data/norms'+suffix+'.pkl')
    month_flags = [1,1,1,4,1,1,2,1,1,1,1,1,1]
    timezp = 734500
    
    # ds = []
    # for d in range(30):
    #     ds.append(date+datetime.timedelta(days=d))
    date = [date-dateutil.relativedelta.relativedelta(years=1),date-dateutil.relativedelta.relativedelta(months=1),date]
    time_ordinal = np.array([(d.toordinal()-timezp-norms[2])/norms[3] for d in date])
    
    mult = [0.5,1.0,1.5,0.5]
    
    x1 = sents_model.reindex(date,method='ffill')
    x2 = sp500_model.reindex(date,method='ffill')
    x3 = empl_model.reindex(date,method='ffill')
    x4 = trend_model.reindex(date,method='ffill')
    x5 = x1+mult[0]*time_ordinal
    x6 = x2+mult[1]*time_ordinal
    x7 = x3+mult[2]*time_ordinal
    x8 = x4+mult[3]*time_ordinal
    x9 = [month_flags[d.month] for d in date]
    x10 = time_ordinal
    x_data = np.array([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]).T
    print x_data
    prediction = 0
    prediction = regr.predict(x_data)
    prediction = (norms[1]*prediction + norms[0])
    
    result = prediction, norms[4:]
    print result
    n_h1b, ls = result
    last_month = int((10*n_h1b[2]/n_h1b[1])+0.5)*10
    last_flag = False
    if last_month == 100:
        last_month = 'This is equivalent to {0}'.format(date[1].strftime('%B, %Y')) #'the previous month'
        last_flag = True
    else:
        last_month='This is {0:d}% of {1}'.format(last_month,date[1].strftime('%B, %Y'))
    print last_month
    last_year = int((10*n_h1b[2]/n_h1b[0])+0.5)*10
    if last_year == 100:
        if last_flag:
            last_year = 'and {0}'.format(date[0].strftime('%B, %Y')) #'the same month last year'
        else:
            last_year = 'and equivalent to {0}'.format(date[0].strftime('%B, %Y')) #'the same month last year'
    else:
        last_year='and {0:d}% of {1}'.format(last_year,date[0].strftime('%B, %Y'))
    print last_year
    return [prediction[2],last_month,last_year], norms[4:]

def make_figure(date=pandas.to_datetime('2014-02-01'), pred=80000, suffix=''):
    
    (prediction_series,month_series) = joblib.load('../data/pred'+suffix+'.pkl')
    
    ax0 = None
    fig = plt.figure()
    date += datetime.timedelta(days=15)
    plt.axvline(date,color='black')
    month_series['2005':].plot(label='H1B Rate',color='black')
    ax0 = prediction_series.plot(label='Prediction',color='green')
    plt.xlabel('Date',fontsize=20)
    plt.ylabel('# H1B Applications',fontsize=20)
    plt.legend(loc=9)
    plt.setp(plt.gca().get_legend().get_texts(), fontsize='20')
    figname = 'imgs/dynamicfig'+suffix+str(randint(0,1000))+'.png'
    fig.savefig('../app/static/'+figname)
    return figname

def make_c3_figure(date=pandas.to_datetime('2014-02-01'), pred=80000, suffix=''):
    (prediction_series,month_series) = joblib.load('../data/pred'+suffix+'.pkl')
    #print prediction_series
    pred_dates = [(pandas.to_datetime(str(v))).strftime('%Y-%m-%d') for v in prediction_series.index.values]
    pred_vals = [int(v+0.5) for v in prediction_series.values]
    data_vals = [v for v in month_series['2005':].reindex(prediction_series.index).values]
    for d in range(len(data_vals)):
        if not np.isnan(data_vals[d]):
            data_vals[d] = int(data_vals[d]+0.5)
        else:
            data_vals[d] = 'NaN'
    result_model = {'date': pred_dates, 'Model': pred_vals, 'H-1B': data_vals}
    #print result_model
    return result_model

if __name__ == '__main__':
    #predict_nH1B(date=pandas.to_datetime('2015-03'),suffix='_tech_')
    make_c3_figure()
    
