#!/usr/bin/env python
'set timestamp every second'
import traceback
import credis
import time
from threading import Thread

JOBS = [
    ('127.0.0.1', 6379),
]


def worker():
    for host, port in JOBS:
        try:
            credis.Connection(host=host, port=port).execute('set', 'redis_timestamp_key', int(time.time()))
        except:
            traceback.print_exc()


def main():
    while True:
        Thread(target=worker).run()
        time.sleep(1)

if __name__ == '__main__':
    main()
