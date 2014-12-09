#!/usr/bin/env python
# encoding: utf-8

import re

CMD_LEN_PATTERN = re.compile(r'^\*\d+\r\n$')
LEN_PATTERN = re.compile(r'^\$\d+\r\n$')

def iter_raw(fp):
    """
    iter Redis AOF log
    Example::

        with open('/path/to/appendonly.aof', 'r') as fp:
            for lines in iter_raw(fp):
                print lines

    """
    # entry = '*cmd_len\r\n$cmd_name_len\r\ncmd\r\n$argv1_len\r\nargv1\r\n...'
    while True:
        lines = [fp.readline()]
        if not CMD_LEN_PATTERN.match(lines[0]):
            raise StopIteration
        cmd_len = int(lines[0][1:-2])
        # print cmdlen
        while len(lines) < cmd_len * 2 + 1:
            line = fp.readline()
            assert LEN_PATTERN.match(line)
            next_len = int(line[1:-2])
            next_line = fp.read(next_len + 2)
            assert next_line.endswith('\r\n')
            lines.extend([line, next_line])
        yield lines

def iter_command(fp):
    for lines in iter_raw(fp):
        yield [_entry[0:-2] for _entry in lines[2:][0::2]]