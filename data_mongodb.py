import pymongo
from datetime import datetime, timedelta
from repository_base import Repository

class MongoDBRepository(Repository):
    def get_data(self,topic_name, numdays):
        mongoClient=pymongo.MongoClient()
        db=mongoClient.SensorData
        yesterday=datetime.today() - timedelta(numdays)
        cursor = db.home_data.find({"topic":topic_name,"time":{"$gte":yesterday}}).sort("time",pymongo.ASCENDING)

        values = []
        labels = []

        for r in cursor:
            values.append(r['value'])
            labels.append(super(MongoDBRepository,self).date_formatted(r['time']))

        return labels, values
