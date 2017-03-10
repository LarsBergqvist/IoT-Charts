
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import time
from dateutil.parser import parse
from dateutil.tz import gettz

# get local timezone    
tzinfos = {"BRST": -10800, "CST": gettz("America/Chicago")}

numdays=1
yesterday=datetime.today() - timedelta(numdays)
client = InfluxDBClient('192.168.1.16', 8086, 'root', 'root', 'sensordata')
query='select value from "Home/GroundFloor/Temperature"'
query2=query + " where time > '" + str(yesterday) + "';"
print(query)
print(query2)
result = client.query(query2)
#print(result[0])
p = list(result.get_points(measurement='Home/GroundFloor/Temperature'))
#print(p[0]['value'])
for v in p:
#    s=v['time'][0:19]
#    print(s)
    ss = parse(v['time'],tzinfos=tzinfos)
    print(ss+timedelta(hours=1))
#    print(local_tz.localize(ss))
#    print(time.strptime(s, "%Y-%m-%dT%H:%M:%S"))

