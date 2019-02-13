# encoding=UTF-8

# Copyright © 2019 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
*forknanny* monkey-patches os.fork() to forbid it in multi-threaded programs
'''

import distutils.core
import distutils.command.build_py

try:
    import distutils644
except ImportError:
    pass
else:
    distutils644.install()

b''  # Python >= 2.6 is required

classifiers = '''
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: POSIX
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Quality Assurance
'''.strip().splitlines()

distutils.core.setup(
    name='forknanny',
    version='0',  # not released yet
    license='MIT',
    description='forbid os.fork() in multi-threaded programs',
    long_description=__doc__.strip(),
    classifiers=classifiers,
    url='https://github.com/jwilk/python-forknanny',
    author='Jakub Wilk',
    author_email='jwilk@jwilk.net',
    py_modules=['forknanny'],
)

# vim:ts=4 sts=4 sw=4 et
