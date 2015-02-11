
# coding: utf-8

# In[159]:


import matplotlib
get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot as plt
import numpy as np
import scipy
import pandas
import seaborn
import pymysql as mdb
import re
import time
import emcee
import triangle
import datetime
import cPickle as pickle
from sklearn import datasets, linear_model
from sklearn.externals import joblib
#from scipy import linalg


# In[3]:

con = mdb.connect('localhost', 'anne', '', 'teleborder')


# In[4]:

dates = []
nworkers = []
with con:
    cur = con.cursor()
    cur.execute('select LCA_CASE_SUBMIT, total_workers from H1B;')
    for result in cur:
        gd = datetime.datetime.combine(result[0], datetime.datetime.min.time()) #result[0].toordinal()
        dates.append(gd)
        nworkers.append(result[1])
len(dates)


# In[98]:

date_series = pandas.Series(nworkers, index=dates)


# In[5]:

date_series_1s = pandas.Series(np.ones(len(nworkers)), index=dates)


# In[100]:

#plt.hist(date_series_1s.index.date.toordinal())


# In[ ]:




# In[231]:

month_series = date_series_1s.resample('M', how='sum')
month_series_norm = (month_series - month_series.mean())/month_series.std()
# month_series.plot()
# plt.xlabel('Submission Date')
# plt.ylabel('Number of DOL Applications')


# In[6]:

year_series = date_series_1s.resample('A', how='sum')
year_series_norm = (year_series['2008':] - year_series['2008':].mean())/year_series['2008':].std()
# year_series_norm.plot()


# In[30]:

nbins = int((max(dates)-min(dates))/364.)
hist, edges = np.histogram(dates, bins=nbins)
means = []
for i in range(len(edges)-1):
    means.append(0.5*(edges[i]+edges[i+1]))
# plt.plot(means,hist,'o')


# In[7]:

sp500 = pandas.io.parsers.read_csv('/Users/bauer/insight/teleborder/data/SP500/200001to201501.csv')


# In[8]:

sp500['datetime'] = pandas.to_datetime(sp500['Date'])
sp500_series = pandas.Series( ((sp500['Open']-sp500['Open'].mean())/sp500['Open'].std()).values, index=sp500['datetime'] )
sp500_year = sp500_series.resample('A')


# In[238]:

(article_dates,article_sents) = pickle.load(open('/Users/bauer/insight/teleborder/data/nytimes/sentiment_data_afinn.txt', 'r'))
dates = [datetime.datetime.combine(d, datetime.datetime.min.time()) for d in article_dates]
sentiments = pandas.Series(article_sents, index=dates)
sentiments = sentiments.sort_index()
sentiments_month = sentiments.resample("M")
sentiments_month = (sentiments_month-sentiments_month.mean())/sentiments_month.std()
sentiments_year = sentiments.resample("A")
sentiments_year = (sentiments_year-sentiments_year.mean())/sentiments_year.std()


# In[239]:

# sp500_series['2006':].plot(label='S&P 500')
# #month_series_norm.plot()
# sentiments_month.plot(label='Sentiment by month')
# sentiments_year.plot(label='Sentiment by year')
# plt.legend(loc=2)


# In[85]:

# (sp500_series.reindex(year_series_norm.index) - year_series_norm).plot()


# In[33]:

indices = np.argsort(sp500['gdate'])
x_sorted = sp500['gdate'][indices]
y_sorted = ((sp500['Open']-np.mean(sp500['Open']))/np.std(sp500['Open']))[indices]
sp500_binned = np.interp(means, x_sorted,y_sorted)
# print means
# print sp500_binned


# In[34]:

# plt.plot(means,sp500_binned)
h1b_binned = (hist-np.mean(hist))/np.std(hist)
# plt.plot(means,h1b_binned)


# In[99]:

ordinals = [d.toordinal() for d in sp500_series.index]


# In[54]:


def lnlike(params, t_e, economy, t_h, h1b):
    [lag, m, b] = params
    econ_shifted = np.interp(t_h, t_e+lag, economy+(m*t_e + b))
    chi2 = np.sum((econ_shifted-h1b)**2)
    return -0.5*chi2

def lnprob(params, t_e, economy, t_h, h1b):
    lp = 0. #lnprior_v(theta)
    [lag, m, b] = params
    if lag < -0.0 or lag > 1000.0 or m < 0.:
        return -np.inf
    return lp + lnlike(params, t_e, economy, t_h, h1b)

guess = [365.0, 0.0, 0.0] # time lag
# nll = lambda *args: -lnlike(*args)
# #results = optimize.fmin(nll, guess, args=(x_sorted, y_sorted, np.array(means)-500, h1b_binned), xtol=5., ftol=0.001, full_output=True)
# results_ml = scipy.optimize.minimize(nll, guess, args=(x_sorted, y_sorted, np.array(means), h1b_binned), tol=0.01, bounds=[(-1000.0, 1000.0)])
# print results_ml.x[0]

ndim, nwalkers = len(guess), 100
pos = [1e-4*np.random.randn(ndim) for i in range(nwalkers)]
timezp = 734500
myargs =(np.array([d.toordinal()-timezp for d in sp500_year.index]), sp500_year.values, np.array([d.toordinal()-timezp for d in year_series_norm.index]), year_series_norm.values)
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=myargs)
pos, prob, state = sampler.run_mcmc(pos, 500)
nsteps = 500
print 'Burned in 500 steps, resetting and running {0} more.'.format(nsteps)
sampler.reset()
sampler.run_mcmc(pos, nsteps)
print 'Finished running the sampler'
print("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction)))
# flatten the walkers
samples = sampler.chain[:, :, :].reshape((-1, ndim))


# In[55]:

# print samples.shape
lags = samples[:,0]
ms = samples[:,1]
bs = samples[:,2]
print 'lag mean {0}, median {1}, stddev {2}'.format(np.mean(lags),np.median(lags),np.std(lags))
print 'm mean {0}, median {1}, stddev {2}'.format(np.mean(ms),np.median(ms),np.std(ms))
print 'b mean {0}, median {1}, stddev {2}'.format(np.mean(bs),np.median(bs),np.std(bs))
plt.hist(lags)
plt.yscale('log', nonposy='clip')


# In[227]:

sp500_series = sp500_series.sort_index()
sp500_series['2006':'2015'].plot(label='S&P 500')
line_shift = pandas.Series(np.mean(ms)*np.array([d.toordinal()-timezp for d in sp500_series.index]) + np.mean(bs), index=sp500_series.index)
sp500_shifted = sp500_series.shift(np.mean(lags), freq='D')
sp500_model = (sp500_shifted + line_shift.reindex(sp500_shifted.index, method='ffill'))
#sp500_model['2006':'2015'].plot(label='S&P 500 Shifted',alpha=0.5)
#sp500_model['2015':'2006'].resample('A').plot(label = 'S&P 500 Shifted, Resampled')
year_series_norm[:'2014-01'].plot(label='H1B Applications')
plt.legend(loc=2)
#sentiments_month.plot()
#sentiments_year.plot()


# In[240]:

guess = [100.0, 0.0, 0.0] # time lag

ndim, nwalkers = len(guess), 100
pos = [1e-4*np.random.randn(ndim) for i in range(nwalkers)]
timezp = 734500
myargs =(np.array([d.toordinal()-timezp for d in sentiments_month.index]), sentiments_month.values, np.array([d.toordinal()-timezp for d in year_series_norm.index]), year_series_norm.values)
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=myargs)
pos, prob, state = sampler.run_mcmc(pos, 500)
nsteps = 500
print 'Burned in 500 steps, resetting and running {0} more.'.format(nsteps)
sampler.reset()
sampler.run_mcmc(pos, nsteps)
print 'Finished running the sampler'
print("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction)))
# flatten the walkers
samples_sentiment = sampler.chain[:, :, :].reshape((-1, ndim))


# In[170]:

# print samples_sentiment.shape
lags_sentiment = samples_sentiment[:,0]
ms_sentiment = samples_sentiment[:,1]
bs_sentiment = samples_sentiment[:,2]
print 'lag mean {0}, median {1}, stddev {2}'.format(np.mean(lags_sentiment),np.median(lags_sentiment),np.std(lags_sentiment))
print 'm mean {0}, median {1}, stddev {2}'.format(np.mean(ms_sentiment),np.median(ms_sentiment),np.std(ms_sentiment))
print 'b mean {0}, median {1}, stddev {2}'.format(np.mean(bs_sentiment),np.median(bs_sentiment),np.std(bs_sentiment))
# plt.hist(lags_sentiment)
# plt.yscale('log', nonposy='clip')


# In[241]:

# sentiments_month.plot(label='Sentiments')
sents_shifted = sentiments.shift(np.mean(lags_sentiment), freq='D')
line_shift = pandas.Series(np.mean(ms)*np.array([d.toordinal()-timezp for d in sents_shifted.index]) + np.mean(bs), index=sents_shifted.index)
sents_model = (sents_shifted + line_shift).resample('M')
sents_model = (sents_model - sents_model.mean())/sents_model.std()
# sents_model.plot(label='Sentiments Shifted',alpha=0.5)
# year_series_norm[:'2014-01'].plot(label='H1B Applications')
# plt.legend(loc=2)


# In[242]:

# h1b_model = linear_regression(shifted_vals)
regr = linear_model.LinearRegression()
indices = sentiments_month['2008-01':'2014-01'].index
#print indices
y_data = np.array(month_series_norm.reindex(indices).values)
#print y_data
month_array = indices.month
month_array[month_array<=1] = 0
month_array[(month_array<5) & (month_array>1)] = 1
month_array[month_array>=5] = 0
# print month_array
x_data = np.vstack(([sents_model.reindex(indices,method='bfill').values],[sp500_model.reindex(indices, method='bfill').values],month_array)).T
#print x_data
regr.fit(x_data, y_data)
#print regr.get_params()
joblib.dump(regr, '/Users/bauer/insight/teleborder/data/my_model.pkl', compress=9)
joblib.dump(sents_model, '/Users/bauer/insight/teleborder/data/x1.pkl', compress=9)
joblib.dump(sp500_model, '/Users/bauer/insight/teleborder/data/x2.pkl', compress=9)
joblib.dump([month_series.mean(),month_series.std(),lags_sentiment.mean(),lags.mean(),0.0], '/Users/bauer/insight/teleborder/data/norms.pkl', compress=9)
plt.plot(y_data, regr.predict(x_data), 'o', color='blue', linewidth=3)
predict_date = pandas.to_datetime('2015-04')
prediction = regr.predict(np.array([sents_model.reindex([predict_date],method='ffill'),sp500_model.reindex([predict_date],method='ffill'),predict_date.month]).T)
prediction = (month_series.std()*prediction + month_series.mean())[0]
#norm = (month_series - month_series.mean())/month_series.std()
# print prediction
# print month_series.reindex([predict_date],method='bfill').values[0]


# In[243]:

month_input = month_series.index.month
month_input[month_input<=1] = 0
month_input[(month_input<5) & (month_input>1)] = 1
month_input[month_input>=5] = 0
prediction = regr.predict(np.array([sents_model.reindex(predict_dates,method='bfill'),sp500_model.reindex(predict_dates,method='bfill'),month_input]).T)
prediction = (month_series.std()*prediction + month_series.mean())
prediction_series = pandas.Series(prediction,index=month_series.index)
prediction_series[:'2013-09-01'].plot()
month_series.plot()
plt.xlabel('Date')
plt.ylabel('Number of H1B Applications')
# sp500_model.reindex(predict_dates,method='bfill').plot()


# In[ ]:



