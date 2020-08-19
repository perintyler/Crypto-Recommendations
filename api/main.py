# -*- coding: utf-8 -*-
"""Server"""

import ws
from ws import app
from exchange import client, kraken, bitfinex

DEBUG = False

ws.add_listener(kraken.Ticker())
ws.add_listener(bitfinex.Ticker())

if DEBUG:
  ws.start_server()
