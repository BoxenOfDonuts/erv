from threading import Thread, Event
from log import logger
from gpiozero import OutputDevice

# Initialize GPIO pin
pin = OutputDevice(4)

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
            logger.info('added {} minutes to running fan'.format(self.additional_interval / 60))
            self.finished.wait(self.additional_interval)
            self.additional_interval = None
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)

        self.finished.set()

    def add(self, interval):
        self.additional_interval = interval


def checkpinstatus():
    logger.info("Checking pin state")
    # retuns 0 for low and 1 for high
    state = pin.value
    return state


def pincleanup():
    pin.off()
    pin.close()
    logger.info('cleanup ran')


def relay(timer):
    global t
    relay_open(timer)
    t = Timer((timer), relay_close)
    t.start()


def relay_open(timer):
    pin.on()
    logger.info("Relay switched to NO", extra={'PIN_4': pin.value})
    logger.info("Relay opened for {} minutes".format(timer / 60))


def relay_close():
    logger.info("Close function starting")
    pin.off()
    logger.info("Switched off Relay")


def add_time(timer):
    logger.info("Added {} minutes".format(timer / 60))
    t.add(timer)


def stop_fan():
    logger.info("Stopping fan")
    pin.off()
