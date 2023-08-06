"""
    setup.py

    Copyright (c) 2019-2020 Datacoral. All rights reserved.

    This program is licensed to you under the Apache License Version 2.0,
    and you may not use this file except in compliance with the Apache License
    Version 2.0. You may obtain a copy of the Apache License Version 2.0 at
    http://www.apache.org/licenses/LICENSE-2.0.

    Unless required by applicable law or agreed to in writing,
    software distributed under the Apache License Version 2.0 is distributed on
    an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
    express or implied. See the Apache License Version 2.0 for the specific
    language governing permissions and limitations there under.

    Authors: Avi Ivgi
    Copyright: Copyright (c) 2019-2020 Datacoral
    License: Apache License Version 2.0
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

version_file_path = os.path.join(
    os.path.dirname(__file__),
    'snowplow_tracker',
    '_version.py'
    )
exec(open(version_file_path).read(), {}, locals())

authors_list = ['Datacoral']
authors_str = ', '.join(authors_list)

authors_email_list = ['support@datacoral.co']
authors_email_str = ', '.join(authors_email_list)

setup(
    name='datacoral-tracker-py',
    version=__version__,
    author=authors_str,
    author_email=authors_email_str,
    packages=['snowplow_tracker'],
    url='http://datacoral.com',
    license='Apache License 2.0',
    description='Datacoral\'s Python Instrumentation using Snowplow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python"
    ],

    install_requires = [
        "requests",
        "pycontracts",
        "gevent",
        "redis"
    ],
)
