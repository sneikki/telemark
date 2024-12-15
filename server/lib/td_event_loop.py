from threading import Thread
from queue import Queue
from lib.td_client import receive_result
from lib.result_object import parse_result_data


class TDEventLoop(Thread):
    registered_queries: Queue

    def run(self):
        self.registered_queries = Queue()

        while True:
            result_object = parse_result_data(receive_result())
