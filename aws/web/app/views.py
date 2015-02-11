from flask import Flask, render_template, request, make_response
import locale
locale.setlocale(locale.LC_ALL, '')
import numpy as np
import pandas
import datetime
from sklearn.externals import joblib
from a_Model import ModelIt
from predict_h1b import predict_nH1B, make_figure, make_c3_figure
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route("/teleborder")
def teleborder():
    return render_template('teleborder.html')

@app.route('/results')
def teleborder_output():
    date=request.args.get('ID')
    if not date:
        date = '2015-03'
    try:
        date = pandas.to_datetime(date)
        if isinstance(date, basestring):
            return render_template( 'notadate.html' )
    except:
        return render_template( 'notadate.html' )
    if date > pandas.to_datetime('2016-02-01'):
        return render_template( 'future.html' )
    if date < pandas.to_datetime('2005-01-01'):
        return render_template( 'past.html' )
    [n_h1b, ls] = predict_nH1B(date)
    datestring = date.strftime('%B, %Y')
    datereg1 = pandas.to_datetime(str(date)).strftime('%Y-%m-%d')
    datereg2 = pandas.to_datetime(str(date+datetime.timedelta(days=30))).strftime('%Y-%m-%d')
    pred = make_c3_figure(date,n_h1b,'')
    importance = joblib.load('../data/importance.pkl')
    return render_template( 'teleborder_output.html', id=request.args.get('ID'), date = datestring, 
    the_result = locale.format("%d", int(np.floor(n_h1b[0] + 0.5)/100) * 100, grouping=True), last_month=n_h1b[1], 
    last_year=n_h1b[2], prediction=pred, date1 = date, date2 = datereg2 )

@app.route('/tech')
def computer_output():
    date=request.args.get('ID')
    if not date:
        date = '2015-03'
    try:
        date = pandas.to_datetime(date)
        if isinstance(date, basestring):
            return render_template( 'notadate.html' )
    except:
        return render_template( 'notadate.html' )
    date = pandas.to_datetime(date)
    [n_h1b, ls] = predict_nH1B(date,suffix='_tech_')
    datestring = date.strftime('%B, %Y')
    datereg1 = pandas.to_datetime(str(date)).strftime('%Y-%m-%d')
    datereg2 = pandas.to_datetime(str(date+datetime.timedelta(days=30))).strftime('%Y-%m-%d')
    pred = make_c3_figure(date,n_h1b,suffix='_tech_')
    importance = joblib.load('../data/importance.pkl')
    return render_template( 'computers_output.html', id=request.args.get('ID'), date = datestring, 
    the_result = locale.format("%d", int(np.floor(n_h1b[0] + 0.5)/100) * 100, grouping=True), last_month=n_h1b[1], 
    last_year=n_h1b[2], prediction=pred, date1 = date, date2 = datereg2 )

@app.route('/engineering')
def engineering_output():
    date=request.args.get('ID')
    if not date:
        date = '2015-03'
    try:
        date = pandas.to_datetime(date)
        if isinstance(date, basestring):
            return render_template( 'notadate.html' )
    except:
        return render_template( 'notadate.html' )
    date = pandas.to_datetime(date)
    [n_h1b, ls] = predict_nH1B(date,suffix='_eng_')
    datestring = date.strftime('%B, %Y')
    datereg1 = pandas.to_datetime(str(date)).strftime('%Y-%m-%d')
    datereg2 = pandas.to_datetime(str(date+datetime.timedelta(days=30))).strftime('%Y-%m-%d')
    pred = make_c3_figure(date,n_h1b,suffix='_eng_')
    importance = joblib.load('../data/importance.pkl')
    return render_template( 'engineering_output.html', id=request.args.get('ID'), date = datestring, 
    the_result = locale.format("%d", int(np.floor(n_h1b[0] + 0.5)/100) * 100, grouping=True), last_month=n_h1b[1], 
    last_year=n_h1b[2], prediction=pred, date1 = date, date2 = datereg2 )

@app.route('/finance')
def finance_output():
    date=request.args.get('ID')
    if not date:
        date = '2015-03'
    try:
        date = pandas.to_datetime(date)
        if isinstance(date, basestring):
            return render_template( 'notadate.html' )
    except:
        return render_template( 'notadate.html' )
    date = pandas.to_datetime(date)
    [n_h1b, ls] = predict_nH1B(date,suffix='_fin_')
    datestring = date.strftime('%B, %Y')
    datereg1 = pandas.to_datetime(str(date)).strftime('%Y-%m-%d')
    datereg2 = pandas.to_datetime(str(date+datetime.timedelta(days=30))).strftime('%Y-%m-%d')
    pred = make_c3_figure(date,n_h1b,suffix='_fin_')
    importance = joblib.load('../data/importance.pkl')
    return render_template( 'finance_output.html', id=request.args.get('ID'), date = datestring, 
    the_result = locale.format("%d", int(np.floor(n_h1b[0] + 0.5)/100) * 100, grouping=True), last_month=n_h1b[1], 
    last_year=n_h1b[2], prediction=pred, date1 = date, date2 = datereg2 )
    
@app.route('/health')
def health_output():
    date=request.args.get('ID')
    if not date:
        date = '2015-03'
    try:
        date = pandas.to_datetime(date)
        if isinstance(date, basestring):
            return render_template( 'notadate.html' )
    except:
        return render_template( 'notadate.html' )
    date = pandas.to_datetime(date)
    [n_h1b, ls] = predict_nH1B(date,suffix='_med_')
    datestring = date.strftime('%B, %Y')
    datereg1 = pandas.to_datetime(str(date)).strftime('%Y-%m-%d')
    datereg2 = pandas.to_datetime(str(date+datetime.timedelta(days=30))).strftime('%Y-%m-%d')
    pred = make_c3_figure(date,n_h1b,suffix='_med_')
    importance = joblib.load('../data/importance.pkl')
    return render_template( 'health.html', id=request.args.get('ID'), date = datestring, 
    the_result = locale.format("%d", int(np.floor(n_h1b[0] + 0.5)/100) * 100, grouping=True), last_month=n_h1b[1], 
    last_year=n_h1b[2], prediction=pred, date1 = date, date2 = datereg2 )
    
@app.route('/education')
def education_output():
    date=request.args.get('ID')
    if not date:
        date = '2015-03'
    try:
        date = pandas.to_datetime(date)
        if isinstance(date, basestring):
            return render_template( 'notadate.html' )
    except:
        return render_template( 'notadate.html' )
    date = pandas.to_datetime(date)
    [n_h1b, ls] = predict_nH1B(date,suffix='_ed_')
    datestring = date.strftime('%B, %Y')
    datereg1 = pandas.to_datetime(str(date)).strftime('%Y-%m-%d')
    datereg2 = pandas.to_datetime(str(date+datetime.timedelta(days=30))).strftime('%Y-%m-%d')
    pred = make_c3_figure(date,n_h1b,suffix='_ed_')
    importance = joblib.load('../data/importance.pkl')
    return render_template( 'education.html', id=request.args.get('ID'), date = datestring, 
    the_result = locale.format("%d", int(np.floor(n_h1b[0] + 0.5)/100) * 100, grouping=True), last_month=n_h1b[1], 
    last_year=n_h1b[2], prediction=pred, date1 = date, date2 = datereg2 )

# @app.route('/static/imgs/<path:filename>')
# def return_image (filename):
#     response = make_response(app.send_static_file(filename))
#     response.cache_control.max_age = 0
#     return response

@app.route('/slides')
def slides_input():
    #return render_template('slides.html')
    return render_template('slideshare.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


