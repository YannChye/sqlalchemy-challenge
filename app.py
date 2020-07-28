# Import dependencies
import numpy as np
import datetime as dt
from dateutil.parser import parse

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///./Resources/hawaii.sqlite")

# Reflect existing database
Base=automap_base()
# Reflect tables
Base.prepare(engine,reflect=True)

# Save references to tables
Measurement=Base.classes.measurement
Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app=Flask(__name__)

#################################################
# Flask Routes
#################################################

# List all available api routes
@app.route("/")
def welcome():
    return (
        f"<b>Available Routes</b><br/>"
        f"/api/v1.0/precipitation - <i>precipitation by data</i><br/>"
        f"/api/v1.0/stations - <i>all stations</i><br/>"
        f"/api/v1.0/tobs - <i>temperature collected by the most active station in the past year</i><br>"
        f"/api/v1.0/&lt;start&gt; - <i>min, max, and avg daily temperature,where &lt;start&gt; = start date in 'yyyy-mm-dd' format</i><br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; - <i>min, max, and avg daily temperature,where &lt;start&gt; = start date, &lt;end&gt; = end date</i>"
    )

# Return precipitation by date
@app.route("/api/v1.0/precipitation")
def precipitate():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    # Create a dictionary of dates and precipitation
    all_precipitation=[]
    for date,prcp in results:
        precipitation_dict={}
        precipitation_dict["date"]=date
        precipitation_dict["prcp"]=prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

# Return station list
@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    results=session.query(func.distinct(Measurement.station),Station.name)\
        .filter(Measurement.station==Station.station).all()
    session.close()

    all_station=[]
    for id,name in results:
        station_dict={}
        station_dict["station id"]=id
        station_dict["name"]=name
        all_station.append(station_dict)

    return jsonify(all_station)

# Return temperature at most active station for the previous year
@app.route("/api/v1.0/tobs")
def station_temp():
    session=Session(engine)
    
    #getting the start date
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
    lastdate=dt.datetime.strptime(lastdate[0],'%Y-%m-%d')
    #get start date (ie. 12 months before last date point)
    startdate=lastdate-dt.timedelta(days=365)
    
    # getting the most active station of the past year
    most_active_station=session.query(Measurement.station,Station.name)\
        .filter(Measurement.station==Station.station)\
        .filter(Measurement.date>=startdate)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc()).first()    
    
    # getting the temperature
    results=session.query(Measurement.tobs)\
        .filter(Measurement.date>=startdate)\
        .filter(Measurement.station==most_active_station[0]).all()
    
    session.close

    past_year_temp=list(np.ravel(results))
    past_year_dict={
        "date":[startdate.strftime("%Y/%m/%d"),lastdate.strftime("%Y/%m/%d")],
        "station":np.ravel(most_active_station)[0],
        "station name":np.ravel(most_active_station)[1],
        "temp":past_year_temp}
    return jsonify(past_year_dict)

# Return temperature from start date
@app.route("/api/v1.0/<start>")
def summary_temp(start):

    session=Session(engine)
    startdate = parse(start)
    startdate=dt.datetime.strftime(startdate,'%Y-%m-%d')
    results=session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date>=startdate)\
        .group_by(Measurement.date).all()  
    session.close

    summary_temp=[]
    for date,min,avg,max in results:
        temp_dict={}
        temp_dict["Date"]=date
        temp_dict["Temp Min"]=min
        temp_dict["Temp Avg"]=avg
        temp_dict["Temp Max"]=max
        summary_temp.append(temp_dict)

    return jsonify(summary_temp)

# Return temperature between date range
@app.route("/api/v1.0/<start>/<end>")
def summary_temp_range(start,end):
    session=Session(engine)
    startdate = parse(start)
    startdate=dt.datetime.strftime(startdate,'%Y-%m-%d')
    enddate=parse(end)
    enddate=dt.datetime.strftime(enddate,'%Y-%m-%d')
    results=session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date>=startdate)\
        .filter(Measurement.date<=enddate)\
        .group_by(Measurement.date).all()  
    session.close

    summary_temp=[]
    for date,min,avg,max in results:
        temp_dict={}
        temp_dict["Date"]=date
        temp_dict["Temp Min"]=min
        temp_dict["Temp Avg"]=avg
        temp_dict["Temp Max"]=max
        summary_temp.append(temp_dict)

    return jsonify(summary_temp)
 

if __name__ == '__main__':
    app.run(debug=True)