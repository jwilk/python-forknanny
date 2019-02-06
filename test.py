# encoding=UTF-8

# Copyright © 2019 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import os
import sys
import threading
import unittest

if sys.version_info < (2, 7):
    import unittest2 as unittest

import forknanny

class Test(unittest.TestCase):

    def setUp(self):
        forknanny.install()

    def test(self):
        if os.fork() == 0:
            os._exit(0x37)
        (pid, status) = os.wait()
        self.assertEqual(status, 0x3700)
        evt = threading.Event()
        thr = threading.Thread(target=evt.wait)
        thr.start()
        with self.assertRaises(OSError):
            if os.fork() == 0:
                os._exit(0x42)
            (pid, status) = os.wait()
            self.assertEqual(status, 0x4200)
        evt.set()
        thr.join()
        if os.fork() == 0:
            os._exit(0x42)
        (pid, status) = os.wait()
        self.assertEqual(status, 0x4200)

if __name__ == '__main__':
    unittest.main()

# vim:ts=4 sts=4 sw=4 et
