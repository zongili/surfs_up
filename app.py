# from flask import Flask
# app = Flask(__name__)

import app
# @app.route('/')
# def hello_world():
#     return 'Hello world'
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify	
# access and query our SQLite database file.
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect the database into our classes.
Base = automap_base()
# reflect our tables.
Base.prepare(engine, reflect=True)
# create a variable for each of the classes so that we can reference them later,
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python to our database
session = Session(engine)
# define our Flask app
app = Flask(__name__)

	
#  print("example __name__ = %s", __name__)
	
# if __name__ == "__main__":
#  print("example is being run directly.")
# else:
#    print("example is being imported")
# define the welcome route

# add the precipitation, stations, tobs, and temp routes that we'll 
# need for this module into our return statement.
# @app.route("/")
# def welcome():
#     return
# def welcome():
#     return(
    
#     f"Welcome to the Climate Analysis API!<br/>"
#     f"Available Routes:<br/>"
#     f"/api/v1.0/precipitation<br/>"
#     f"/api/v1.0/stations<br/>"
#     f"/api/v1.0/tobs<br/>"
#     f"/api/v1.0/temp/start/end<br/>"
#     )

# def precipitation():
#     session.close()
#     return
# calculates the date one year ago from the most recent date in the database
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#    return
# write a query to get the date and precipitation for the previous 
# year. Add this query to your existing code.
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#    precipitation = session.query(Measurement.date, Measurement.prcp).\
#       filter(Measurement.date >= prev_year).all()
#    session.close()   
#    return
# we'll create a dictionary with the date as the key and the precipitation as the value. To do this, we will "jsonify" our dictionary. Jsonify()
# JSON files are structured text files with attribute-value pairs and 
# rray data types. They have a variety of purposes, especially when 
# downloading information from the internet through API calls. 
# We can also use JSON files for cleaning, filtering, sorting, 
# and visualizing data, among many other tasks. When we are done 
# modifying that data, we can push the data back to a web interface, 
# like Flask.
@app.route("/api/v1.0/precip")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
   filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
#    session.close()
   return jsonify(precip)


@app.route("/api/v1.0/stations")
#    get all of the stations in our database
# unraveling our results into a one-dimensional array.
# convert our unraveled results into a list. 
# To convert the results to a list, we will need to use the list function, 
# which is list(), and then convert that array into a list. 
# Then we'll jsonify the list and return it as JSON
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    # return our list as JSON, we need to add stations=stations. 
    # This formats our list into JSON.
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year. H
    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    # unravel the results into a one-dimensional array and convert that array into a list. 
    # Then jsonify the list and return our results
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# last route will be to report on the minimum, average, and maximum temperatures. 
# However, this route is different from the previous ones in that we will have 
# to provide both a starting and ending date. 
# create a query to select the minimum, average, and maximum temperatures from our 
# SQLite database. We'll start by just creating a list called sel
def stats(start=None, end=None):
 # Since we need to determine the starting and ending date, add an if-not statement
#  to our code. This will help us accomplish a few things. We'll need to query our
#  database using the list that we just made. Then,
#  we'll unravel the results into a one-dimensional array and convert them to a list.

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
# we need to calculate the temperature minimum, average, and maximum with the 
# start and end dates. We'll use the sel list, which is simply the data points 
# we need to collect. 
# Let's create our next query, which will get our statistics data.
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    # After running this code, you'll be able to copy and paste the web 
    # address provided by Flask into a web browser. Open /api/v1.0/temp/start/end 
    # route and check to make sure you get the correct result, which is:
    # [null,null,null]
    # /api/v1.0/temp/2017-06-01/2017-06-30
    return jsonify(temps)
