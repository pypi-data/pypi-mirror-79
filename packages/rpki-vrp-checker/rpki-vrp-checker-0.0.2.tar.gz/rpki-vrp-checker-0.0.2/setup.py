#!/usr/bin/env python
# Copyright (C) 2020 Job Snijders <job@ntt.net>
#
# This file is part of rpki-vrp-checker
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF  THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from setuptools import setup
from rpki_vrp_checker import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='rpki-vrp-checker',
    version=__version__,
    author='Job Snijders',
    author_email='job@ntt.net',
    description='A simple utility to perform business logic tests on a '
                'collection of RPKI-based VRPs.',
    long_description=long_description,
    url='https://github.com/job/rpki-vrp-checker',
    python_requires='>=3.8',
    install_requires=[
        'pyyaml',
        'py-radix==0.10.0',
    ],
    license='BSD',
    entry_points={
        'console_scripts': [
            'rpki-vrp-checker = rpki_vrp_checker.main:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        ],
)
