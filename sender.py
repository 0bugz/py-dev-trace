import queue
import requests
from threading import Thread

class EventPublisher:

    def __init__(self, event_server_url):
        self.event_server_url = event_server_url

    def publish(self, message):
        print("Got message: {}".format(message))

class EventWorker(Thread):

    def __init__(self, q):
        super(EventWorker, self).__init__()
        self.q = q
        self.publisher = EventPublisher("")
        self.daemon = True
        self.should_stop = False
        self.start()

    def stop(self):
        self.should_stop = True

    def run(self):
        while self.should_stop == False:
            try:
                message = self.q.get()
                try:
                    self.publisher.publish(message)
                except Exception as e1:
                    print("Exception publishing message: {}".format(e1))
                finally:
                    self.q.task_done()
            except Exception as e:
                print("Exception occured: {}".format(e))

class WorkerPool(object):

    def __init__(self, pool_size = 1):
        self.q = queue.Queue()
        self.workers = []
        for _ in range(pool_size):
            w = EventWorker(self.q)
            self.workers.append(w)

    def queue_message(self, message):
        self.q.put(message)

    def stop(self):
        for worker in self.workers:
            worker.stop()
