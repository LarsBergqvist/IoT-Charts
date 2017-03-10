#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import sys
import data_fake
import data_mongodb
#from logger import logger
import data_influxdb

app = Flask(__name__)

def get_labels_and_values_for_topic(topic_name, numdays):
    if (numdays < 1):
        numdays = 1

    if app.config['FAKE'] == False:
        if app.config['DB'] == 'MongoDB':
            print("Using MongoDB repository")
            repo = data_mongodb.MongoDBRepository
        else:
            print("Using InfluxDB repository")
            repo = data_influxdb.InfluxDBRepository
    else:
        print("Using fake repository")
        repo = data_fake.FakeRepository

    return repo.get_data(repo,topic_name,numdays)
    
@app.route("/ChartData")
def index():
    return render_template('index.html')

@app.route('/ChartData/api/<string:location>/<string:measurement>')
def get_measurements_as_labels_and_values(location,measurement):

    numdays = request.args.get('numdays', default=1, type=int)

    topic = "Home/" + location + "/" + measurement
    # Get all measurements that matches a specific topic from the database
    # Fetch data from today and numdays backwards in time
    # The measurements are split into two arrays, one with measurement times (=labels)
    # and one with the actual values.
    labels, values = get_labels_and_values_for_topic(topic,numdays)

    return jsonify({"measurements":{'labels':labels,'values':values}})


if __name__ == "__main__":
    app.config['FAKE'] = False
    app.config['DB'] = 'InfluxDB'
    for arg in sys.argv:
        if arg.lower() == "--fake":
            app.config['FAKE'] = True
        elif arg.lower() == "--mongodb":
            app.config['DB'] = 'MongoDB'

    app.run(host='0.0.0.0', port=6001,debug=True)
