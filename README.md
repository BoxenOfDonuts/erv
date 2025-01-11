## How To Use
For the climate container, an `.env` file needs to be created at the root of the directory with the following values

- DATADOG_API_KEY=Your_api_key
- DATADOG_APP_KEY=Your_app_key
- ROOM=Room_name

Where the api and app key come from datadog, and the room name is whatever you want. The room name will get tagged in datadog like `room:${value}`

You can optionally send metrics to deno kv by using the `DENO_ENABLED=ENABLED`. If you enable this you will need to pass a username and value to 

- CLIMATE_API_USER
- CLIMATE_API_PW

## Running just the climate container
You can run just the climate container itself by running `docker compose up climate -d`

Or just cd into the `/climate` directory and run `docker compose -f climate.yml --env-file ../.env up`. Optionally if you are only running the climate container, you can move the `.env` file to the `/climate` directory and omit the `--env-file` argument.

## Notes for myself
[ ] You can specify dev / production requirements. Use that to get rid of stuff like uwsgi. Believe I have to switch to UV or use separate requirements.txt file:
[source](https://stackoverflow.com/questions/78902565/how-do-i-install-python-dev-dependencies-using-uv)

Docker compose secrets might be an option as well, think I would need to code for that specifically though

Also could update the erv compose section to have watchers for development like climate does.

Now that secrets are out of the climate section, could also push that up to hub instead of building

Really need to re-architect the erv side a bit more.

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