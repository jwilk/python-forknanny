# encoding=UTF-8

# Copyright © 2019 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
forbid os.fork() in multi-threaded programs
'''

import errno
import os
import threading

_orig_fork = os.fork

def _fail(threads=None):
    err = errno.EDEADLK
    msg = os.strerror(err)
    if threads is not None:
        msg += (
            '\n'
            'Active threads:\n'
            + '\n'.join('* ' + repr(t) for t in threads)
        )
    raise OSError(err, msg)

def fork():
    threads = threading.enumerate()
    if len(threads) > 1:
        _fail(threads)
    return _orig_fork()

def install():
    os.fork = fork

__all__ = ['install']

# vim:ts=4 sts=4 sw=4 et
