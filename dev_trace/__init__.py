import logging
from .zblogger import ZBLogger

logging.setLoggerClass(ZBLogger)
logger = logging.getLogger('zblogger')
logger.addHandler(logging.NullHandler())

from .core import DevTrace
