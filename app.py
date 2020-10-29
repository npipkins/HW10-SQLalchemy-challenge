import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/stations")
def stations():
    results = session.query(Station.name).all()

    results_list = list(results)

    return jsonify(results_list)
    

@app.route("/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()

    results_dict = dict(results)

    return jsonify(results_dict)



@app.route("/tobs")
def tobs():
    most_active_id = 'USC00519281'
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-18').filter(Measurement.station == most_active_id).all()
    
    results_list = list(results)
    
    return jsonify(results_list)




