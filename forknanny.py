# encoding=UTF-8

# Copyright © 2019-2023 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
forbid os.fork() in multi-threaded programs
'''

import errno
import os
import sys
import threading

b''  # Python >= 2.6 is required

_orig_fork = os.fork

def _fail(threads=None):
    err = errno.EDEADLK
    msg = os.strerror(err)
    if threads is not None:
        msg += (
            '\n'
            'Active threads:\n'
            + str.join('\n', ('* ' + repr(t) for t in threads))
        )
    raise OSError(err, msg)

_is_linux = sys.platform.startswith('linux')

def fork():
    threads = threading.enumerate()
    if len(threads) > 1:
        _fail(threads)
    elif _is_linux:
        with open('/proc/self/status', 'rb') as fp:
            for line in fp:
                if line.startswith(b'Threads:'):
                    _, n_threads = line.split(b':', 1)
                    n_threads = int(n_threads)
                    if n_threads > 1:
                        _fail()
    return _orig_fork()

def install():
    os.fork = fork

__all__ = ['install']

# vim:ts=4 sts=4 sw=4 et
