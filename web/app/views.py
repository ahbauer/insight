from flask import render_template, request, make_response
from app import app
#import pymysql as mdb
import numpy as np
import pandas
import datetime
from sklearn.externals import joblib
from a_Model import ModelIt
from predict_h1b import predict_nH1B, make_figure

#db = mdb.connect(user="anne", host="localhost", db="teleborder", charset='utf8')

@app.route('/')
@app.route('/index')
@app.route("/teleborder")
def teleborder():
    return render_template('teleborder.html')

@app.route('/teleborder_output')
def teleborder_output():
    date=request.args.get('ID')
    date = pandas.to_datetime(date)
    n_h1b, ls = predict_nH1B(date)
    n_h1b = int(np.floor(n_h1b + 0.5)/100) * 100 # round it to the 100s
    datestring = date.strftime('%B, %Y')
    make_figure(date, n_h1b)
    importance = joblib.load('/Users/bauer/insight/teleborder/web/data/importance.pkl')
    return render_template( 'teleborder_output.html', id=request.args.get('ID'), date = datestring, the_result = n_h1b, 
    w1 = '{0:5.1f}'.format(100.*importance[0,0]), w2 = '{0:5.1f}'.format(100.*importance[0,1]), 
    w3 = '{0:5.1f}'.format(100.*importance[0,2]), w4 = '{0:5.1f}'.format(100.*importance[0,3]), 
    #w7 = '{0:5.1f}'.format(ws[6]), w8 = '{0:5.1f}'.format(ws[7]), w9 = '{0:5.1f}'.format(ws[8]),
    l1 = '{0:d}'.format(int(ls[0]+0.5)), l2 = '{0:d}'.format(int(ls[1]+0.5)), l3 = '{0:d}'.format(int(ls[2]+0.5)),
    l4 = '{0:d}'.format(int(ls[3]+0.5)) )
    #l7 = '{0:d}'.format(int(ls[6]+0.5)), l8 = '{0:d}'.format(int(ls[7]+0.5)), l9 = '{0:d}'.format(int(ls[8]+0.5)) )

@app.route('/computers')
def computer_output():
    date=request.args.get('ID')
    date = pandas.to_datetime(date)
    n_h1b, ls = predict_nH1B(date)
    n_h1b = int(np.floor(n_h1b + 0.5)/100) * 100 # round it to the 100s
    datestring = date.strftime('%B, %Y')
    make_figure(date, n_h1b)
    importance = joblib.load('/Users/bauer/insight/teleborder/web/data/importance.pkl')
    return render_template( 'computers_output.html', id=request.args.get('ID'), date = datestring, the_result = n_h1b, 
    w1 = '{0:5.1f}'.format(100.*importance[0,0]), w2 = '{0:5.1f}'.format(100.*importance[0,1]), 
    w3 = '{0:5.1f}'.format(100.*importance[0,2]), w4 = '{0:5.1f}'.format(100.*importance[0,3]), 
    #w7 = '{0:5.1f}'.format(ws[6]), w8 = '{0:5.1f}'.format(ws[7]), w9 = '{0:5.1f}'.format(ws[8]),
    l1 = '{0:d}'.format(int(ls[0]+0.5)), l2 = '{0:d}'.format(int(ls[1]+0.5)), l3 = '{0:d}'.format(int(ls[2]+0.5)),
    l4 = '{0:d}'.format(int(ls[3]+0.5)) )


@app.route('/engineering')
def engineering_output():
    date=request.args.get('ID')
    date = pandas.to_datetime(date)
    n_h1b, ls = predict_nH1B(date)
    n_h1b = int(np.floor(n_h1b + 0.5)/100) * 100 # round it to the 100s
    datestring = date.strftime('%B, %Y')
    make_figure(date, n_h1b)
    importance = joblib.load('/Users/bauer/insight/teleborder/web/data/importance.pkl')
    return render_template( 'engineering_output.html', id=request.args.get('ID'), date = datestring, the_result = n_h1b, 
    w1 = '{0:5.1f}'.format(100.*importance[0,0]), w2 = '{0:5.1f}'.format(100.*importance[0,1]), 
    w3 = '{0:5.1f}'.format(100.*importance[0,2]), w4 = '{0:5.1f}'.format(100.*importance[0,3]), 
    l1 = '{0:d}'.format(int(ls[0]+0.5)), l2 = '{0:d}'.format(int(ls[1]+0.5)), l3 = '{0:d}'.format(int(ls[2]+0.5)),
    l4 = '{0:d}'.format(int(ls[3]+0.5)) )

@app.route('/finance')
def finance_output():
    date=request.args.get('ID')
    date = pandas.to_datetime(date)
    n_h1b, ls = predict_nH1B(date)
    n_h1b = int(np.floor(n_h1b + 0.5)/100) * 100 # round it to the 100s
    datestring = date.strftime('%B, %Y')
    make_figure(date, n_h1b)
    importance = joblib.load('/Users/bauer/insight/teleborder/web/data/importance.pkl')
    return render_template( 'finance_output.html', id=request.args.get('ID'), date = datestring, the_result = n_h1b, 
    w1 = '{0:5.1f}'.format(100.*importance[0,0]), w2 = '{0:5.1f}'.format(100.*importance[0,1]), 
    w3 = '{0:5.1f}'.format(100.*importance[0,2]), w4 = '{0:5.1f}'.format(100.*importance[0,3]), 
    l1 = '{0:d}'.format(int(ls[0]+0.5)), l2 = '{0:d}'.format(int(ls[1]+0.5)), l3 = '{0:d}'.format(int(ls[2]+0.5)),
    l4 = '{0:d}'.format(int(ls[3]+0.5)) )


@app.route('/static/imgs/<path:filename>')
def return_image (filename):
    response = make_response(app.send_static_file(filename))
    response.cache_control.max_age = 0
    return response

@app.route('/input')
def cities_input():
    return render_template('input.html')

@app.route('/output')
def cities_output():
    # pull 'ID' from input field and store it
    city = request.args.get('ID')

    with db:
        cur = db.cursor()
        #just select the city from the world_innodb that the user inputs
        cur.execute("SELECT Name, CountryCode,  Population FROM City WHERE Name='%s';" % city)
        query_results = cur.fetchall()

    cities = []
    for result in query_results:
        cities.append(dict(name=result[0], country=result[1], population=result[2]))
        
        #call a function from a_Model package. note we are only pulling one result in the query
        pop_input = cities[0]['population']
        the_result = ModelIt(city, pop_input)
    
    return render_template("output.html", cities = cities, the_result = the_result)
