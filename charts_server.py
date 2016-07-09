from flask import Flask
#from flask import Markup
from flask import Flask, render_template, jsonify
import pymongo
from datetime import datetime, timedelta

def get_data(topic_name):
    # Set up client for MongoDB
    mongoClient=pymongo.MongoClient()
    db=mongoClient.SensorData
    collection=db.home_data
    yesterday=datetime.today() - timedelta(2)
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

@app.route('/<path:path>')
def catch_all(path):
    
    topic = path.replace("api","Home")
    print(topic)
    labels, values = get_data(topic)

    return jsonify({"measurements":{'labels':labels,'values':values}})
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001,debug=True)
