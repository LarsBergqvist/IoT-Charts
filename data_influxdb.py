from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from dateutil.parser import parse
from repository_base import Repository

class InfluxDBRepository(Repository):
    def get_data(self,topic_name, numdays,utcOffsetInMinutes):
        yesterday=datetime.today() - timedelta(numdays)
        client = InfluxDBClient('192.168.1.16', 8086, 'root', 'root', 'sensordata')
        query='select value from "' + topic_name + '"' + " where time > '" + str(yesterday) + "';"
        result = client.query(query)

        values = []
        labels = []

        utcOffsetInHours=utcOffsetInMinutes/60
        p = list(result.get_points())
        count = 0
        for r in p:
            if count % int( (numdays/10)*(numdays/10) + 1) == 0:
                values.append(r['value'])
                # time is stored as UTC-time
                # adjust returned time with the utc offset that is used from the client
                t = parse(r['time']) - timedelta(hours=utcOffsetInHours)
                labels.append(super(InfluxDBRepository,self).date_formatted(t))
            count = count + 1

        return labels, values

