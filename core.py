import atexit
import logging
import socket

from sender import WorkerPool
from zblogger import ZBLogger

worker_pool = WorkerPool(pool_size=3)
ip_address = "127.0.0.1"
try:
    ip_address = socket.gethostbyname(socket.gethostname())
except:
    pass

class DevTrace:

    def __init__(self):
        logging.setLoggerClass(ZBLogger)
        atexit.register(self.stop)

    def stop(self):
        print("Dev trace stopping ...")
        worker_pool.stop()
