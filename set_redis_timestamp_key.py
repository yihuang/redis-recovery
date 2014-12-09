'set timestamp every second'
import gevent
import gevent.monkey
gevent.monkey.patch_all()

import traceback
import credis
import time

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
        gevent.spawn(worker)
        time.sleep(1)

if __name__ == '__main__':
    main()
