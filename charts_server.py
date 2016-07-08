from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
from flask import jsonify
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta

def get_data(topic_name):
    # Set up client for MongoDB
    mongoClient=MongoClient()
    db=mongoClient.SensorData
    collection=db.home_data
    yesterday=datetime.today() - timedelta(1)
    cursor = db.home_data.find({"topic":topic_name,"time":{"$gte":yesterday}})

    values = []
    labels = []

    for r in cursor:
        values.append(r['value'])
        timeStr=r['time'].strftime('%d %b %H:%M')
        labels.append(timeStr)

    return labels, values

app = Flask(__name__)

    
@app.route("/")
def index():

    return render_template('index.html')

@app.route("/api/Outdoor/Temperature")
def get_OutdoorTemperature():

    labels, values = get_data("Home/Outdoor/Temperature")

    return jsonify({"measurements":{'labels':labels,'values':values}})

@app.route("/api/GroundFloor/Temperature")
def get_IndoorTemperature():

    labels, values = get_data("Home/GroundFloor/Temperature")

    return jsonify({"measurements":{'labels':labels,'values':values}})

@app.route("/api/Garage/Temperature")
def get_GarageTemperature():

    labels, values = get_data("Home/Garage/Temperature")

    return jsonify({"measurements":{'labels':labels,'values':values}})
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001,debug=True)
