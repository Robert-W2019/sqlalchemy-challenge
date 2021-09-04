#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

#references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link from py to DB

session = Session(engine)

#Flask
app = Flask(__name__)

#Flask routes

@app.route('/')
def welcome():
    return(
        f'Welcome to the HI Climate API <br/>'
        f'Available Routes: <br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp/start/end'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #precipitation data from prev year
    prev_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
                    
    #Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).        filter(Measurement.date >= prev_year).all()
                        
    precip = {date: prcp for date, prcp in precipitation}
    
    return jsonify (precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    
    stations = list(np.ravel(results))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
    
    return jsonify(temps)
    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >=start).\
        filter(Measurement.date <=end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps)




if __name__ == '__main__':
    app.run()


# In[ ]:




