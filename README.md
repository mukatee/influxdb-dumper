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
For example, "2016-06-07T12:56:00Z". For more format examples, run some dumps from your database.

To get timestamps in the dumps in different formats, change epoch='ms' in the scripts to different unit.
Remove the whole epoch parameter to get textual date strings (such as the example above).

Sometimes if the "show measurements" query does not list all fields returned by a "select *" query,
those will not be included in the dumps. This seems to be the case especially for the "_internal" database.

Long timeframe dumps may be better off split into several separate dumps, as all data to be dumped is
basically loaded to memory.

It is possible to use the filter option to disable dumping of some specific measurements/columns.
For example, to leave out measurements/columns named "C1" and "C2", use a filter value of "C1,C2".
