# -*- coding: utf-8 -*-
"""Pulls from coinbase and bitfinex"""

import ws

EXCHANGES = ('bitfinex', 'kraken')
SYMBOLS = ('ETH', 'BTC')

bidAskTables = {exchange: [] for exchange in EXCHANGES}

def format_price_tables():
  to_dicts = lambda coins: [c.__dict__ for c in coins]
  tables = {exchange: to_dicts(coins) for exchange,coins in bidAskTables.items()}
  return tables

def is_price_table_populated():
  numCoins = len(SYMBOLS)
  return not any(len(coins) != numCoins for coins in bidAskTables.values())

def make_recommendations() -> list:
  if not is_price_table_populated(): return []

  for exchange in bidAskTables.keys():
    bidAskTables[exchange].sort(key=lambda c: c.symbol)

  recs = []
  for i, symbol in enumerate(SYMBOLS):
    btfxCoin = bidAskTables[EXCHANGES[0]][i]
    krakenCoin = bidAskTables[EXCHANGES[1]][i]
    bidDiff = float(btfxCoin.bid - krakenCoin.bid)
    askDiff = float(btfxCoin.ask - krakenCoin.ask)
    bidDiff,askDiff = round(bidDiff, 4), round(askDiff, 4)
    if bidDiff != 0:
      exchange = 'bitfinex' if bidDiff > 0 else 'kraken'
      recs.append(f'Buy {symbol} from {exchange} (+{abs(bidDiff)})')
    if askDiff != 0:
      exchange = 'bitfinex' if askDiff < 0 else 'kraken'
      recs.append(f'Sell {symbol} to {exchange} (-{abs(askDiff)})')
  return recs

class Coin:

  def __init__(self, symbol, bid, ask):
    self.symbol = symbol
    self.bid = bid
    self.ask = ask

  def update(self, bid, ask):
    self.bid,self.ask = bid,ask

  def __hash__(self, other): return self.symbol == other.symbol
  def __eq__(self, other): return self.symbol == other.symbol
  # def __dict__(self): return self.__dict__

class ExchangeWebsocket(ws.Listener):

  def __init__(self, wss, exchange, endpoint, symbols=SYMBOLS):
    super().__init__(wss, on_open=self.subscribe)
    self.exchange = exchange
    self.endpoint = endpoint
    self.symbols = symbols
    self.channels = {}

  def subscribe(self): pass

  def update_price(self, symbol, bid, ask):
    bid,ask = float(bid),float(ask)
    if symbol == 'XBT': symbol = 'BTC'
    coin = Coin(symbol, bid, ask)
    exchangeTable = bidAskTables[self.exchange]
    if coin in exchangeTable:
      oldCoin = exchangeTable[exchangeTable.index(coin)]
      isPriceUpdate = oldCoin.bid != bid or oldCoin.ask != ask
      if not isPriceUpdate: return
      oldCoin.update(bid, ask)
    else:
      exchangeTable.append(coin)

    # if is_price_table_populated():
    msg = ws.Message.create(recommendations=make_recommendations(),
                            **format_price_tables())
    self.broadcast(msg)

  @property
  def subscribed(self):
    return len(self.channels.keys()) == len(self.symbols)

  def format_message(self, msg):
    """ Message that gets sent to clients """
    return {'recommendations': make_recommendations(), **prices}
