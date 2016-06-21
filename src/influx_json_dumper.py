__author__ = 'teemu kanstren'

import json
import argparse
import os
from influxdb import InfluxDBClient
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", help="Database name", default="_internal", nargs='?')
parser.add_argument("-ip", "--hostname", help="Database address (ip/url)", default="localhost", nargs='?')
parser.add_argument("-p", "--port", help="Database port", default="8086", nargs='?')
parser.add_argument("-u", "--username", help="DB user name", default="root", nargs='?')
parser.add_argument("-pw", "--password", help="DB password", default="root", nargs='?')
parser.add_argument("-tl", "--timelength", help="Length of time for dump", default="1h", nargs='?')
parser.add_argument("-et", "--endtime", help="End time for dump", default='now()', nargs='?')
parser.add_argument("-f", "--filter", help="List of columns to filter", default='', nargs='?')
args = parser.parse_args()

host = args.hostname
port = args.port
username = args.username
password = args.password
dbname = args.database
time_length = args.timelength
end_time = args.endtime
filtered_str = args.filter
filtered = [x.strip() for x in filtered_str.split(',')]
client = InfluxDBClient(host, port, username, password, dbname)
#first we get list of all measurements in the selected db to dump them
query = 'show measurements'
result = client.query(query)
for measurements in result:
    for measure in measurements:
        measure_name = measure['name']

        filename = "report_json/"+measure_name+'.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        #request all data for given timeframe and dump as json
        with open(filename, 'w') as file:
            query = """select * from "{}" where time > '{}' - {} AND time < '{}' """.format(measure_name, end_time, time_length, end_time)
            result = client.query(query, epoch='ms')
            lines = []
            for point in result:
                for item in point:
                    for col in filtered:
                        if col in item:
                            del item[col]
                    ms = item['time'] / 1000
                    d = datetime.fromtimestamp(ms)
                    item['readable_time'] = d.isoformat('T')+'Z'
                    #first we build a list of dictionaries for each measurement value
                    lines.append(item)
            #finally put the list into a dict and use built-in functionality of "json" module to dump them all at once
            out = {'data': lines}
            print(json.dumps(out), file=file)

