## Notes for myself
Build and tag the erv code on another device, cd into app and run

`docker build --platform linux/arm/v5 -t boxenofdonuts/erv-api:latest .`

You can then push the tag

`docker image push boxenofdonuts/erv-api:latest`

### Next steps
I think if I change the temp_logger to update redis, I can change the api to pull from there, then can use the slim / alpine version of python instead of the fat image

# erv
A simple python RESTful api to interact with my ERV system. Project runs on a Pi Zero with a temperature / humidity sensor and a relay.
When hitting the endpoint, it will open the relay and bridge the connection on the ERV system, kicking the fanspeed up to HIGH to better cycle air.
The payload in the body allows for time in minutes for the realy to open. Another URI allows time to be added.

# logging
Uses pythonjsonlogger library to log json formatted logs for ingestion into splunk

# GPIO
Uses the RPI.GPIO for reading the temperature / humidity sensor, as well as controlling the relay.

# SHT31-D
Has a temperature and humidity sensor attached. Another python script sends it to datadog, but added an endpoint here to allow homebridge to check it