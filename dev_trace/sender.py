import sys
import json
import queue
import logging
import requests
from threading import Thread

logger = logging.getLogger('zblogger')

class EventPublisher:

    def __init__(self):
        self.event_server_url = None

    def set_event_server_url(self, event_server_url):
        self.event_server_url = event_server_url

    def set_app_name(self, app_name):
        self.app_name = app_name

    def set_client_id(self, client_id):
        self.client_id = client_id

    def set_client_auth_token(self, client_auth_token):
        self.client_auth_token = client_auth_token

    def publish(self, message):
        message["app_name"] = self.app_name
        msg_str = "Got message: {}".format(json.dumps(message))
        logger.debug(msg_str)
        resp = requests.post(self.event_server_url, json=message)
        assert(resp.status_code == 200)

class EventWorker(Thread):

    def __init__(self, q):
        super(EventWorker, self).__init__()
        self.q = q
        self.publisher = EventPublisher()
        self.daemon = True
        self.should_stop = False
        self.start()

    def stop(self):
        self.should_stop = True

    def set_event_server_url(self, event_server_url):
        self.publisher.set_event_server_url(event_server_url)

    def set_app_name(self, app_name):
        self.publisher.set_app_name(app_name)

    def set_client_id(self, client_id):
        self.publisher.set_client_id(client_id)

    def set_client_auth_token(self, client_auth_token):
        self.publisher.set_client_auth_token(client_auth_token)

    def run(self):
        while self.should_stop == False:
            try:
                message = self.q.get()
                try:
                    self.publisher.publish(message)
                except Exception as e1:
                    logger.error("Exception publishing message: {}".format(e1))
                finally:
                    self.q.task_done()
            except Exception as e:
                logger.error("Exception occured: {}".format(e))

class WorkerPool(object):

    def __init__(self, pool_size = 1):
        self.q = queue.Queue()
        self.workers = []
        for _ in range(pool_size):
            w = EventWorker(self.q)
            self.workers.append(w)

    def queue_message(self, message):
        self.q.put(message)

    def set_event_server_url(self, event_server_url):
        for worker in self.workers:
            worker.set_event_server_url(event_server_url)

    def set_app_name(self, app_name):
        for worker in self.workers:
            worker.set_app_name(app_name)

    def set_client_id(self, client_id):
        for worker in self.workers:
            worker.set_client_id(client_id)

    def set_client_auth_token(self, client_auth_token):
        for worker in self.workers:
            worker.set_client_auth_token(client_auth_token)

    def stop(self):
        for worker in self.workers:
            worker.stop()
