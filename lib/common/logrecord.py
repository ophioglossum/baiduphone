import logging
from config import app
def log(message,level='debug'):
    if app.LOGIC_DEBUG:
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        if app.LOGIC_DEBUG_FILE:
            logging.basicConfig(level=logging.DEBUG,filename=app.LOGIC_DEBUG_FILE,format=LOG_FORMAT)
        else:
            logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT)
        record = getattr(logging, level)
        record(message)