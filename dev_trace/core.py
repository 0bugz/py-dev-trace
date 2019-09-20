import os
import sys
import atexit
import logging
import socket

from .sender import WorkerPool

logger = logging.getLogger('zblogger')

worker_pool = WorkerPool(pool_size=3)
ip_address = "127.0.0.1"
try:
    ip_address = socket.gethostbyname(socket.gethostname())
except:
    pass

class DevTrace:

    def __init__(self, app_name=None, client_id=None, client_auth_token=None, event_server_url=None):
        if event_server_url == None:
            event_server_url = os.getenv('ZBLOGGER_EVENT_SERVER_URL')
        if event_server_url == None:
            raise Exception("Either ZBLOGGER_EVENT_SERVER_URL environmental variable needs to be set or event_server_url parameter needs to be passed")

        if app_name == None:
            app_name = os.getenv("ZBLOGGER_APP_NAME")
        if app_name == None:
            raise Exception("Either ZBLOGGER_APP_NAME environmental variable needs to be set or app_name parameter needs to be passed")

        if client_id == None:
            client_id = os.getenv("ZBLOGGER_CLIENT_ID")
        if client_id == None:
            raise Exception("Either ZBLOGGER_CLIENT_ID environmental variable needs to be set or client_id parameter needs to be passed")

        if client_auth_token == None:
            client_auth_token = os.getenv("ZBLOGGER_CLIENT_AUTH_TOKEN")
        if client_auth_token == None:
            raise Exception("Either ZBLOGGER_CLIENT_AUTH_TOKEN environmental variable needs to be set or client_auth_token parameter needs to be passed")

        worker_pool.set_app_name(app_name)
        worker_pool.set_client_id(client_id)
        worker_pool.set_client_auth_token(client_auth_token)
        worker_pool.set_event_server_url(event_server_url)
        atexit.register(self.stop)

    def stop(self):
        logger.debug("Dev trace stopping ...")
        worker_pool.stop()
