import socket
import time
import logging
from pythonjsonlogger import jsonlogger
import RPi.GPIO as G
import sys

# Setup Logging
logHandler = logging.FileHandler(filename="/var/log/erv/erv.log")
formatter = jsonlogger.JsonFormatter('%(asctime)s %(message)s')
logHandler.setFormatter(formatter)
logging.getLogger().addHandler(logHandler)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

def listen():
    logger.info("Starting Bind")
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("0.0.0.0", 1443))
    serversocket.listen(5)

    while True:
        # waiting for connection
        logger.info("Waiting for connection")
        connection, addr = serversocket.accept()
        address = addr[0]
        logger.info("Connection from address {}".format(address))
        connection.close()
        leds()


def pincleanup():
    G.setmode(G.BCM)
    G.setup(4, G.OUT, initial=0)
    G.cleanup()
    logger.info('cleanup ran')


def leds():
    #set mode
    G.setmode(G.BCM)

    #setup relay pin
    G.setup(4, G.OUT, initial=0)

    # setup low to flip to NO
    G.output(4, G.HIGH)
    logger.info("Relay switched to NO", extra={'PIN_4': G.input(4)})

    logger.info("Relay opened for 20 minutes")
    time.sleep(1200)

    # close relay
    G.output(4, G.LOW)
    logger.info("Switched off Relay")

    # be a good scout and cleanup after yourself
    G.cleanup()


if __name__=="__main__":
    try:
        pincleanup()
        listen()
    except KeyboardInterrupt:
        G.cleanup()
        logger.info('Keyboard interrupt, exiting')
        sys.exit()
