from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

Last_day = session.execute("SELECT MAX(date) FROM Measurement").fetchall()
Last_date = Last_day[0][0]
Query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

## Flask Setup
app = Flask(__name__)

#List all routes that are available.
@app.route("/")
def Welcome():
    return (
        f"Welcome to Donnie's guide to Hawaii weather!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )

 #Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipation")
def precipation():
    session = Session(engine)
    """ Fetches the station and precipition by date"""
    
    results = session.query(Measurement.date, Measurement.prcp).\
       filter(Measurement.date >= Query_date).\
       order_by(Measurement.date).all()
    session.close()   

    #Return the JSON representation of your dictionary    
    precip_dates = []
    
    for result in results:
       precip_dict = {"Date":result[0],"Precipation":result[1]}
       precip_dates.append(precip_dict)
        
    return jsonify(precip_dates) 

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurement.station)\
              .group_by(Measurement.station).all()
    # Convert list of tuples into normal list   
    all_stations = list(np.ravel(results))
    session.close()
    
    return jsonify(all_stations)

# Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():    
    session = Session(engine)

    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
              filter(Measurement.station == 'USC00519281').\
              group_by(Measurement.date).\
              order_by(Measurement.date).all()
    session.close()

# Return a JSON list of temperature observations (TOBS) for the previous year
    tobs_dates =[]
    for result in results:
       tobs_dict = {"Date":result[1],"Temperature":result[2]}
       tobs_dates.append(tobs_dict)
        
    return jsonify(tobs_dates)

#Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/<start>")
def tstart(start):
    session = Session(engine)
    """ Fetches the station and precipition by date"""
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
              .filter(Measurement.date >= start)/
              .order_by(Measurement.date.desc()).all()
    session.close()   

    #Return the JSON representation of your dictionary    
    #list = []
    
    for result in results:
       temp_dict = {"Min":results[0][0],"Avg":result1[0][1],"Max":[0][2]}
       #list.append(temp_dict)
        
    return jsonify(temp,dict) 


if __name__ == '__main__':
    app.run(debug=True)
