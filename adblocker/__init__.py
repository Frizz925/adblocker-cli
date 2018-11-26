from six.moves.queue import Queue
from threading import Thread

import multiprocessing
import requests
import os

DEBUG = 'DEBUG' in os.environ and os.environ['DEBUG'] == '1'
HOSTS_FILE = '/etc/hosts'
FILTER_URLS = [
    'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts',
    'https://raw.githubusercontent.com/notracking/hosts-blocklists/master/hostnames.txt'
]


class Worker(Thread):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.daemon = True
        self.queue = queue
        self.result = ''

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            r = requests.get(url)
            r.raise_for_status()
            self.result += r.text + '\n'
            self.queue.task_done()


def fetch_adblock_list():
    queue = Queue()
    for url in FILTER_URLS:
        queue.put(url)

    worker_count = min(len(FILTER_URLS), multiprocessing.cpu_count())
    workers = []
    for _ in range(worker_count):
        worker = Worker(queue)
        worker.start()
        workers.append(worker)

    queue.join()
    hosts_str = '\n'
    for worker in workers:
        hosts_str += worker.result
    return hosts_str
