# influxdb-dumper
Python scripts to dump InfluxDB contents in JSON and CSV formats.
The scripts are short and single files, so just download them and run.

Examples to get list of parameters:
- python3 influx_csv_dumper.py -h
- python3 influx_json_dumper.py -h

To use, install the InfluxDB Python driver: pip3 install influxdb

For timestamps, the special value of "now()" can be used to define current time.
Data is then dumped for period of time before the given timestamp. By default 1 hour.
Timeframe can be defined as 1s, 1m, 1h, 1d, 7d, whatever the InfluxDB driver supports.

Besides "now()" it is possible to define specific end time for the dump.
For example, "2016-06-07T12:56:00Z". InfluxDB generally uses UTC timestamps, so you probably have to convert to those.
You can get some examples for your data by querying your database using InfluxDB admin interface or this script with some modifications noted below.

Currently, the scripts dump both an epoch timestamp (in milliseconds) but also a "human readable" version at the same time.
This is done by querying for the epoch timestamp and converting this also the a human readable format.
This seems to result in Python converting it to a readable string in your timezone, while the InfluxDB takes UTC timestamps in RFC3339 format.
The dumped "human readable" format should match otherwise, but you may need to add/remove some hours to adjust for your timezone offset.

To get direct timestamps in the dumps in different formats, change epoch='ms' in the scripts to different unit.
Remove the whole epoch parameter to get textual date strings (such as the example above) direct from InfluxDB (in UTC).
But for these mods to work, you need to also modify a bit the timestamp writing and remove the part that adds the "human_readable" key/value.

Sometimes if the "show measurements" query does not list all fields returned by a "select *" query,
those fields will not be included in the dumps. This seems to be the case especially for the "_internal" database.

Long timeframe dumps may be better off split into several separate dumps, as all data to be dumped is
basically loaded to memory.

It is possible to use the filter option to disable dumping of some specific measurements/columns.
For example, to leave out measurements/columns named "C1" and "C2", use a filter value of "C1,C2".
