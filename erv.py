import socket
import time
import logging
import RPi.GPIO as G
import sys
from pythonjsonlogger import jsonlogger
from threading import Thread, Event

# Setup Logging
logHandler = logging.FileHandler(filename="/var/log/erv/erv.log")
formatter = jsonlogger.JsonFormatter('%(asctime)s %(message)s')
logHandler.setFormatter(formatter)
logging.getLogger().addHandler(logHandler)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()


def Timer(*args, **kwargs):
    return _Timer(*args, **kwargs)


class _Timer(Thread):
    """Call a function after a specified number of seconds:

    t = Timer(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.additional_interval = None
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if self.additional_interval:
            logger.info('added {} minutes to running fan'.format(self.additional_interval))
            self.finished.wait(self.additional_interval)
            self.additional_interval = None
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)

        self.finished.set()

    def add(self, interval):
        self.additional_interval = interval


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
        relay()


def checkpinstatus():
    logger.info("Checking pin state")
    G.setmode(G.BCM)
    G.setup(4, G.OUT)

    # retuns 0 for low and 1 for high
    state = G.input(4)
    return state


def pincleanup():
    G.setmode(G.BCM)
    G.setup(4, G.OUT, initial=0)
    G.cleanup()
    logger.info('cleanup ran')


def relay_open(timer):
    #set mode
    G.setmode(G.BCM)

    #setup relay pin
    G.setup(4, G.OUT, initial=0)

    # setup low to flip to NO
    G.output(4, G.HIGH)
    logger.info("Relay switched to NO", extra={'PIN_4': G.input(4)})

    logger.info("Relay opened for {} seconds".format(timer))


def relay_close():
    G.setmode(G.BCM)

    # close relay
    G.output(4, G.LOW)
    logger.info("Switched off Relay")

    # be a good scout and cleanup after yourself
    G.cleanup()


def relay(timer):
    global t
    relay_open(timer)
    t = Timer((timer), relay_close)
    t.start()


def add_time(timer):
    t.add(timer)


if __name__=="__main__":
    try:
        pincleanup()
        listen()
    except KeyboardInterrupt:
        G.cleanup()
        logger.info('Keyboard interrupt, exiting')
        sys.exit()
