# Python SQL toolkit and Object Relational Mapper

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Import flask class

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    print("Server received request for data...")
    return("Welcome. Please view our available routes:<br><br>"
            "/api/v1.0/precipitation<br>"
            "/api/v1.0/stations<br>"
            "/api/v1.0/tobs<br>"
            "/api/v1.0/start<br>"
            "/api/v1.0/start/end")

@app.route('/api/v1.0/precipitation')
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_results = session.query(Measurement.date, Measurement.prcp)\
               .filter(Measurement.date <= '2017-08-23')\
               .filter(Measurement.date >= '2016-08-23').all()
    

    keys = [query_result[0] for query_result in query_results]
    values = [query_result[1] for query_result in query_results]

    precip_dict = dict(zip(keys, values))

    return jsonify(precip_dict)
    
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations = session.query(Measurement.station).distinct()
    station_count = [station[0] for station in stations]

    return jsonify(station_count)

@app.route("/api/v1.0/tobs")
def temperature():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp_results = session.query(Measurement.date, Measurement.tobs)\
               .filter(Measurement.date <= '2017-08-23')\
               .filter(Measurement.date >= '2016-08-23').all()

    date_keys = [temp_result[0] for temp_result in temp_results]
    temp_values = [temp_result[1] for temp_result in temp_results]

    temp_dict = dict(zip(date_keys, temp_values))

    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    
    stats = session.query(*sel)\
        .filter(Measurement.date >= start)\
        .all()

    TMIN = [stat[0] for stat in stats]
    TMAX = [stat[1] for stat in stats]
    TAVG = [stat[2] for stat in stats]

    return jsonify(TMIN[0], TMAX[0], TAVG[0])

@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):

    #Create our session(link/connection) from Python to the DB
    session = Session(engine)

    long_sel = [func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    
    wide_stats = session.query(*long_sel)\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .all()

    TMIN2 = [wide_stat[0] for wide_stat in wide_stats]
    TMAX2 = [wide_stat[1] for wide_stat in wide_stats]
    TAVG2 = [wide_stat[2] for wide_stat in wide_stats]

    return jsonify(TMIN2[0], TMAX2[0], TAVG2[0])

if __name__ == "__main__":
    app.run(debug=True)
