import logging
from logging.handlers import RotatingFileHandler
import datetime

#Logger
log = logging.getLogger('root')
log.setLevel(logging.DEBUG)

fileHandler = RotatingFileHandler('GlitchFilterLog.log', maxBytes=100000)
fileHandler.setLevel(logging.INFO)

log.addHandler(fileHandler)

log.info('******************** {} - Session ********************'.format(datetime.datetime.now()))

formatter = logging.Formatter('%(asctime)s) - %(levelname)s: %(message)s')
fileHandler.setFormatter(formatter)