import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to my climate data API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()

    results_dict = dict(results)

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()

    results_list = list(results)

    return jsonify(results_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_id = 'USC00519281'
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-18').filter(Measurement.station == most_active_id).all()
    results_list = list(results)
    return jsonify(results_list)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    results_list = list(results)
    return jsonify(results_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    results_list = list(results)
    return jsonify(results_list)
