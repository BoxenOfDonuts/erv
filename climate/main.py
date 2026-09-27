import board
import busio
import adafruit_sht31d
import datetime
import time
import os
import sys
import signal
from datadog import initialize, api
from urllib3.util import Retry
import requests
import logging

# Handle SIGTERM gracefully when running as PID 1 in Docker
signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

# Logging configuration
logging.basicConfig(level=logging.INFO)
logging.getLogger("datadog.api").setLevel(logging.WARNING)

class ClimateMonitor:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_sht31d.SHT31D(self.i2c)
        self.api_key = os.getenv('DATADOG_API_KEY')
        self.app_key = os.getenv('DATADOG_APP_KEY')
        self.deno_enabled = os.getenv('DENO_ENABLED', 'DISABLED').upper() == 'ENABLED'
        self.current_room = os.getenv('ROOM')
        self.user = os.getenv('CLIMATE_API_USER')
        self.password = os.getenv('CLIMATE_API_PW')
        self.climate_url = os.getenv('CLIMATE_API_URL')
        self.humidity_offset = float(os.getenv('HUMIDITY_OFFSET', 0))
        self.loops = 0

        # Retry configuration
        self.max_retries = int(os.getenv('DD_MAX_RETRIES', 3))
        self.retry_backoff = float(os.getenv('DD_RETRY_BACKOFF', 2.0))

        self._validate_env_variables()
        self._initialize_datadog()

    def _validate_env_variables(self):
        if not self.api_key or not self.app_key or not self.current_room:
            logging.error("Missing essential environment variables")
            sys.exit(1)
        if self.deno_enabled and (not self.user or not self.password or not self.climate_url):
            logging.error("Missing Deno environment variables")
            sys.exit(1)

    def _initialize_datadog(self):
        try:
            retry_strategy = Retry(
                total=self.max_retries,
                backoff_factor=self.retry_backoff,
                status_forcelist=[429, 500, 502, 503, 504],
                raise_on_status=False
            )
            options = {
                'api_key': self.api_key,
                'app_key': self.app_key,
                'max_retries': retry_strategy
            }
            initialize(**options)
        except Exception as e:
            logging.error(f"Error initializing Datadog API: {e}")
            sys.exit(1)

    @staticmethod
    def c2f(temp):
        return (1.8 * temp) + 32

    def send_to_dd(self, temp, humidity):
        response = api.Metric.send([
            {'metric': 'current.temp', 'points': temp, 'tags': [f'room:{self.current_room}']},
            {'metric': 'current.humidity', 'points': humidity, 'tags': [f'room:{self.current_room}']}
        ])

        if response and isinstance(response, dict) and 'errors' in response:
            logging.critical(
                f"Datadog metric send failed after retries: {response['errors']}. Exiting to trigger container restart."
            )
            sys.exit(1)

    def send_to_deno(self, temp, humidity, update_date):
        payload = {'temperature': temp, 'humidity': humidity, 'lastUpdateDate': update_date}
        auth = (self.user, self.password)

        try:
            r = requests.put(f'http://{self.climate_url}/rooms/{self.current_room}/climate', auth=auth, json=payload, timeout=15)
            r.raise_for_status()
        except requests.RequestException as err:
            logging.error(f"Unexpected error: {err}")

    def toggle_heater(self):
        self.sensor.heater = True
        time.sleep(1)
        self.sensor.heater = False

    def run(self):
        while True:
            start_time = time.time()
            dt = datetime.datetime.now()

            try:
                degrees = self.sensor.temperature
                fdegrees = self.c2f(degrees)
                humidity = self.sensor.relative_humidity + self.humidity_offset
            except Exception as e:
                logging.error(f"Sensor error: {e}")
                continue

            self.send_to_dd(fdegrees, humidity)

            if self.deno_enabled:
                self.send_to_deno(degrees, humidity, dt.strftime("%m/%d/%Y, %H:%M:%S"))

            self.loops += 1
            if self.loops == 2:
                self.toggle_heater()
                self.loops = 0

            end_time = time.time()
            elapsed_time = end_time - start_time
            sleep_time = max(0, 30 - elapsed_time)
            time.sleep(sleep_time)

if __name__ == '__main__':
    monitor = ClimateMonitor()
    monitor.run()
