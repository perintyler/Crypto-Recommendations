"""api/tests.js"""
import sys
import json
import asyncio
import pytest
import pytest_asyncio
import _thread
import threading

import crypto_recommendations_api
from crypto_recommendations_api.settings import SYMBOLS, EXCHANGES
from crypto_recommendations_api.order_books import OrderBooks
from crypto_recommendations_api.bitfinex import BitfinexBroadcaster
from crypto_recommendations_api.kraken import KrakenBroadcaster

WSS = 'ws://127.0.0.1:8080'

class FakeClient:

  def __init__(self, name='fake client'):
    self.origin = name
    self.messages = []
    self.closed = False

  def close(self):
    self.closed = True

  def is_open(self):
    return self.closed is False

  def receive(self):
    client_message = 'test message from fake client'
    return client_message

  def send(self, msg):
    self.messages.append(msg)

  def has_message(self):
    return self.num_messages() > 0

  def num_messages(self):
    return len(self.messages)

  def get_message(self, index=0):
    if len(self.messages) == 0: return None
    return json.loads(self.messages[index])

  def delete_message(self, index):
    self.messages.pop(index)

order_books = OrderBooks()
bitfinex = BitfinexBroadcaster(SYMBOLS, order_books)
kraken = KrakenBroadcaster(SYMBOLS, order_books)
client = FakeClient()

def is_subscribed(broadcaster):
  return len(broadcaster.channels) == len(SYMBOLS)

def start(ws):
  def thread(*args): ws.run_forever() # reconnect=None (delay interval when reconnecting)
  _thread.start_new_thread(thread, ())

def websocket_test(cls):
  def open_and_close_websocket(f):
    def test_wrapper():
      # if 'off' in kwargs and kwargs['off'] is True: return
      client = cls()
      def thread(*args): client.run_forever() # reconnect=None (delay interval when reconnecting)
      _thread.start_new_thread(thread, ())
      returned = f(client)
      client.close()
      return returned
    return pytest.mark.asyncio(test_wrapper)
  return open_and_close_websocket

@pytest.mark.asyncio
async def test_bitfinex_subscription():
  start(bitfinex)
  await asyncio.sleep(1)
  bitfinex.subscribe()
  await asyncio.sleep(2)
  assert is_subscribed(bitfinex)

@pytest.mark.asyncio
async def test_kraken_subscription():
  start(kraken)
  await asyncio.sleep(1)
  kraken.subscribe()
  await asyncio.sleep(2)
  assert is_subscribed(kraken)

@pytest.mark.asyncio
async def test_bitfinex_order_book_compiling():
  await asyncio.sleep(1)
  assert order_books.has_exchange('bitfinex')
  assert order_books.tickers['bitfinex'].num_price_points() == len(SYMBOLS)

@pytest.mark.asyncio
async def test_kraken_order_book_compiling():
  assert order_books.has_exchange('kraken')
  assert order_books.tickers['kraken'].num_price_points() == len(SYMBOLS)

@pytest.mark.asyncio
async def test_recommendations_websocket():
  bitfinex.add_client(client)
  kraken.add_client(client)
  await asyncio.sleep(1)
  assert client.is_open()
  assert client.num_messages() >= 2
  subscriptionMessage1 = client.get_message(0)
  assert subscriptionMessage1['event'] == 'subscribed'
  assert subscriptionMessage1['exchange'] in EXCHANGES
  subscriptionMessage2 = client.get_message(1)
  assert subscriptionMessage2['event'] == 'subscribed'
  assert subscriptionMessage2['exchange'] in EXCHANGES
  assert subscriptionMessage1['exchange'] != subscriptionMessage2['exchange']

  await asyncio.sleep(2)

  # recommendations are only broadcasted when the exchanges' best
  # prices change, so it's possible that there's a delay between the
  # subscription message and the first recommendations message
  for _ in range(3):
    if client.num_messages() == 2: await asyncio.sleep(3)
    else: break

  async def assert_that_client_recieves_recommendations():
    assert client.num_messages() >= 3
    message = client.get_message(2)
    assert message['event'] == 'recommendations'
    assert 'recommendations' in message
    recommendations = message['recommendations']
    assert len(recommendations) == len(SYMBOLS)*len(EXCHANGES)
    for rec in message['recommendations']:
      assert rec.startswith('Buy') or rec.startswith('Sell')

  async def assert_that_client_recieves_price_points():
    assert client.is_open()
    assert client.num_messages() >= 3
    message = client.get_message(2)
    for exchange in EXCHANGES:
      assert exchange in message['prices']
      symbols = [price_point['symbol'] for price_point in message['prices'][exchange]]
      assert set(symbols) == set(SYMBOLS)

      for price_point in message['prices'][exchange]:
        for saleType in ('bid', 'ask'):
          assert saleType in price_point
          assert type(price_point[saleType]) is float

  await assert_that_client_recieves_recommendations()
  await assert_that_client_recieves_price_points()

@pytest.mark.asyncio
async def test_closing():
  client.close()
  bitfinex.close()
  kraken.close()
  assert not bitfinex.is_broadcasting()
  assert not kraken.is_broadcasting()

