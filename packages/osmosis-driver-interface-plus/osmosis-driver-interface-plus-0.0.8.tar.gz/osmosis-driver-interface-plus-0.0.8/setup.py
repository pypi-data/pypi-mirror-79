#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

# Installed by pip install osmosis-driver-interface
# or pip install -e .
install_requirements = [
    'coloredlogs',
    'PyYAML>=4.2b1',
]

# Required to run setup.py:
setup_requirements = ['pytest-runner', ]

test_requirements = [
    'codacy-coverage',
    'coverage',
    'pylint',
    'pytest',
    'pytest-watch',
    'osmosis-on-premise-driver',
    'tox',
]

# Possibly required by developers of osmosis-driver-interface:
dev_requirements = [
    'bumpversion',
    'pkginfo',
    'twine',
    'watchdog',
]

setup(
    author="marcojrfurtado",
    author_email='devops@oceanprotocol.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="💧 Osmosis driver interface. A membrane between the decentralized world and "
                "centralized world. Extended with support for custom drivers.",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='osmosis-driver-interface-plus',
    name='osmosis-driver-interface-plus',
    packages=find_packages(include=['osmosis_driver_interface']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcojrfurtado/osmosis-driver-interface-plus',
    version='0.0.8',
    zip_safe=False,
)
