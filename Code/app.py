import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/anirbanmukherjee/Desktop/Anaconda/sqlalchemy-challenge/Code/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
max_date = list(np.ravel(max_date))[0]
max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
max_year = int(dt.datetime.strftime(max_date,"%Y"))
max_month = int(dt.datetime.strftime(max_date,"%m"))
max_day = int(dt.datetime.strftime(max_date,"%d"))
min_date = dt.date(max_year,max_month, max_day) - dt.timedelta(days=365)
#print(max_date)
#print(min_date)
#print(max_year)
#print(max_day)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################



@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2015-04-30><br/>"
        f"/api/v1.0/2015-04-30/2016-03-31><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all passengers
    
    results = (session.query(Measurement.prcp,Measurement.date).
                filter(Measurement.date > min_date).
                order_by(Measurement.date).all())

    session.close()

    # Convert list of tuples into normal list
    
    prec_data= []

    for result in results: 
        prec_dict = {result.date: result.prcp}
        prec_data.append(prec_dict)
    
    return jsonify(prec_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all passengers
    
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))

    session.close()

    # Convert list of tuples into normal list
        
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all passengers
    
    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
                      .filter(Measurement.date > min_date)
                      .order_by(Measurement.date)
                      .all())

    tempdata = []
    for result in results:
        tempdict = {result.date: result.tobs}
        tempdata.append(tempdict)


    session.close()

    # Convert list of tuples into normal list
        
    return jsonify(tempdata)

@app.route("/api/v1.0/<startdate>")
def start(startdate):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate)
                       .group_by(Measurement.date)
                       .all())

    dates_data = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = round(result[2],2)
        date_dict["High Temp"] = result[3]
        dates_data.append(date_dict)

    session.close()

    # Convert list of tuples into normal list
        
    return jsonify(dates_data)

@app.route("/api/v1.0/<startdate>/<enddate>")
def startend(startdate, enddate):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) <= enddate)
                       .group_by(Measurement.date)
                       .all())

    dates_data = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = round(result[2],2)
        date_dict["High Temp"] = result[3]
        dates_data.append(date_dict)

    session.close()

    # Convert list of tuples into normal list
        
    return jsonify(dates_data)





# @app.route("/api/v1.0/stations")
# def passengers():

#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""

#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# @app.route("/api/v1.0/tobs")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# @app.route("/api/v1.0/<start>")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run()
