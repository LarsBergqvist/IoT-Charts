from flask import Flask, render_template, jsonify
import pymongo
from datetime import datetime, timedelta

def get_data(topic_name, numdays):
    if (numdays < 1):
        numdays = 1

    mongoClient=pymongo.MongoClient()
    db=mongoClient.SensorData
    collection=db.home_data
    yesterday=datetime.today() - timedelta(numdays)
    cursor = db.home_data.find({"topic":topic_name,"time":{"$gte":yesterday}}).sort("time",pymongo.ASCENDING)

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

@app.route('/api/<string:location>/<string:measurement>/<int:numdays>')
def get_measurements(location,measurement,numdays):

    topic = "Home/" + location + "/" + measurement  
    labels, values = get_data(topic,numdays)

    return jsonify({"measurements":{'labels':labels,'values':values}})
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001,debug=True)
