#!/usr/bin/env python
# encoding: utf-8

"""
Usage:
    build_recovery_aof.py --input=<redis_directory> --output=<output_file> --timestamp=<timestamp>
"""

import os
import glob
from docopt import docopt
from aof import iter_raw
options = docopt(__doc__)
print options

MAGIC_KEY = 'redis_timestamp_key'


def find_backup_file(root, timestamp):
    backups = [int(f.rsplit('.', 1)[-1]) for f in glob.glob(os.path.join(root, 'appendonly.aof.*'))]
    for ts in sorted(backups):
        if ts >= timestamp:
            return os.path.join(root, 'appendonly.aof.%s' % ts)
    # use most recent file
    return os.path.join(root, 'appendonly.aof')


def main():
    timestamp = int(options['--timestamp'])
    total = 0

    input_file = find_backup_file(options['--input'], timestamp)
    print 'use appendonly file', input_file

    with open(options['--output'], 'wb') as output:
        with open(input_file, 'rb') as fp:
            for lines in iter_raw(fp):
                total += 1
                map(output.write, lines)
                if lines[2].lower() == 'set\r\n' and lines[4][0:-2] == MAGIC_KEY and int(lines[-1][0:-2]) >= timestamp:
                    # 找到匹配点，完成任务
                    print 'found the best match timestamp', int(lines[-1][0:-2])
                    break
            else:
                print 'Can not find a timestamp for', timestamp

    print '{} entries.'.format(total)

if __name__ == '__main__':
    main()
