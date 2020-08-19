# -*- coding: utf-8 -*-
"""Server"""

import ws
from ws import app
from exchange import client, kraken, bitfinex

ws.add_listener(kraken.Ticker())
ws.add_listener(bitfinex.Ticker())
