from flask import Flask, jsonify

import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func
#import numpy as np
app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

@app.route("/")
def home():
	return (
		f"/api/v1.0/precipitation"
		f"/api/v1.0/stations"
		f"/api/v1.0/tobs"
		f"/api/v1.0/<start>"
		f"/api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def rainfall():
	#session = Session(engine)
	results = session.query(Measurement.prcp, Measurement.date).all()
	session.close()
	all_results = {date:prcp for date,prcp in results}
	#all_results = dict(np.ravel(results, order={'date','prcp'}))
	return jsonify(all_results)


@app.route("/api/v1.0/stations")
def the_stations():
	#session = Session(engine)
	results2 = session.query(Station.station).all()
	session.close()
	return jsonify(results2)
@app.route("/api/v1.0/tobs")
def temps_over_time():
	#session = Session(engine)
	results3 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-23-08', Measurement.station == 'USC00519281').all()
	session.close()
	return jsonify(results3)

@app.route("/api/v1.0/<start>")
def stats_with_start(date):
	#session = Session(engine)
	start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
	session.close()
	return jsonify(start_results)
@app.route("/api/v1.0/<start>/<end>")
def stats_with_start_and_end(start,end):
	#session = Session(engine)
	stats_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	session.close()
	return jsonify(stats_results)

if __name__ == "__main__":
	app.run(debug=True)
