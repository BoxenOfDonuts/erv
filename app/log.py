import logging
import sys
from pythonjsonlogger import jsonlogger

def configure_logging(app):
    if app.debug:
        consoleHandler = logging.StreamHandler(sys.stdout)
        logging.getLogger().addHandler(consoleHandler)
    else:
        logHandler = logging.FileHandler(filename="/var/log/erv/erv.log")
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(message)s')
        logHandler.setFormatter(formatter)
        logging.getLogger().addHandler(logHandler)

    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger()
    return logger