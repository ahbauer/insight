from flask import render_template, request
from app import app
import pymysql as mdb
import numpy as np
import pandas
from a_Model import ModelIt
from predict_h1b import predict_nH1B

db = mdb.connect(user="anne", host="localhost", db="teleborder", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
        title = 'Home', user = { 'nickname': 'Anne' },
        )

@app.route('/db')
def cities_page():
	with db: 
		cur = db.cursor()
		cur.execute("SELECT VISA_CLASS,LCA_CASE_SUBMIT FROM H1B LIMIT 15;")
		query_results = cur.fetchall()
	vclass = ""
	for result in query_results:
		vclass += result[1].isoformat()
		vclass += "<br>"
	return vclass

@app.route("/db_fancy")
def cities_page_fancy():
	with db:
		cur = db.cursor()
		cur.execute("SELECT VISA_CLASS,LCA_CASE_SUBMIT,total_workers FROM H1B LIMIT 15;")
		query_results = cur.fetchall()
	cities = []
	for result in query_results:
		cities.append(dict(name=result[0], country=result[1].isoformat(), population=result[2]))
	return render_template('cities.html', cities=cities)

@app.route("/teleborder")
def teleborder():
    return render_template('teleborder.html')

@app.route('/teleborder_output')
def teleborder_output():
    date=request.args.get('ID')
    date = pandas.to_datetime(date)
    n_h1b, ws, ls = predict_nH1B(date)
    n_h1b = int(np.floor(n_h1b + 0.5)/100) * 100 # round it to the 100s
    datestring = date.strftime('%B, %Y')
    return render_template( 'teleborder_output.html', date = datestring, the_result = n_h1b, 
    weight1 = '{0:5.3f}'.format(ws[0]), weight2 = '{0:5.3f}'.format(ws[1]), weight3 = '{0:5.3f}'.format(ws[2]),
    lag1 = '{0}'.format(int(ls[0]+0.5)), lag2 = '{0:d}'.format(int(ls[1]+0.5)), lag3 = '{0:d}'.format(int(ls[2]+0.5)) )

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
