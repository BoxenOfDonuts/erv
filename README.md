# erv
A simple python RESTful api to interact with my ERV system. Project runs on a Pi Zero with a temperature / humidity sensor and a relay.
When hitting the endpoint, it will open the relay and bridge the connection on the ERV system, kicking the fanspeed up to HIGH to better cycle air.
The payload in the body allows for time in minutes for the realy to open. Another URI allows time to be added.

# logging
Uses pythonjsonlogger library to log json formatted logs for ingestion into splunk

# GPIO
Uses the RPI.GPIO for reading the temperature / humidity sensor, as well as controlling the relay.
