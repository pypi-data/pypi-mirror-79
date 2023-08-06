#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging

from osmosis_driver_interface.constants import COMPUTING, DATA
from osmosis_driver_interface.log import setup_logging
from osmosis_driver_interface.utils import start_plugin

setup_logging()
logger = logging.getLogger('Osmosis')


class Osmosis:
    """High-level, plugin-bound Osmosis functions.
    Instantiated with a subclass implementing the ledger plugin
    interface (:class:`~.AbstractPlugin`) that will automatically be
    bound to all top-level functions:
        - :attr:`type` (as a read-only property)
        - :func:`upload`
        - :func:`download`
        - :func:`list`
        - :func:`generate_url`
        - :func:`delete`
    Attributes:
        plugin (Plugin): Bound persistence layer plugin.
    """

    def __init__(self, url, file_path=None):
        self.computing_plugin = start_plugin(COMPUTING, self.parse_url(url), file_path)
        self.data_plugin = start_plugin(DATA, self.parse_url(url), file_path)

    @staticmethod
    def parse_url(url):
        """
        Parse the url to decide which driver should be loaded.

        :param url: str
        :return: Module name, str
        """
        if 'wss://' in url:
            logger.info('It is a streaming url.')
            return 'streaming'
        else:
            logger.info(f'Loading on_premise driver, url={url}.')
            return 'on_premise'
