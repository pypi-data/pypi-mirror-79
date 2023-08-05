"""
logx: nice print.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2020 Min Latt.
License: MIT, see LICENSE for more details.
"""

import logging

def this(message):
    logging.debug(message)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
this('Logger Ready.')

""" this? maybe I previously play with JS -'D """