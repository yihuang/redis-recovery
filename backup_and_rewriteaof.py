#!/usr/bin/env python
# encoding: utf-8
"""
Usage:
    backup_and_rewriteaof.py --host=<redis_host> --port=<redis_port> --path=<redis_database_path>
"""

import re
import os
import datetime
import credis
from docopt import docopt
options = docopt(__doc__)

reg = re.compile(r'\*3\r\n\$3\r\n(?:SET|set)\r\n\$19\r\nredis_timestamp_key\r\n\$10\r\n(\d+)\r\n')


def find_last_timestamp(f):
    size = os.stat(f).st_size
    fp = open(f, 'rb')
    if size <= 4096:
        s = fp.read()
        matches = reg.findall(s, re.M)
        if matches:
            return int(matches[-1])
    else:
        offset = -4096
        while True:
            fp.seek(offset, 2)
            s = fp.read(4096)
            matches = reg.findall(s, re.M)
            if matches:
                return int(matches[-1])

            if offset == -size:
                break

            offset -= 4096 - 128  # need some overlap
            if -offset > size:
                offset = -size


def main():
    root = options['--path']
    host = options['--host']
    port = int(options['--port'])

    print 'process redis path %s, %s:%s' % (root, host, port)

    # make hard link
    last_timestamp = find_last_timestamp(os.path.join(root, 'appendonly.aof'))

    print 'found last timestamp', last_timestamp, datetime.datetime.fromtimestamp(last_timestamp)
    os.link(os.path.join(root, 'appendonly.aof'), os.path.join(root, 'appendonly.aof.%s' % last_timestamp))

    # do bgrewriteaof
    print 'do bgrewriteaof', host, port
    credis.Connection(host=host, port=port).execute('bgrewriteaof')

if __name__ == '__main__':
    main()
