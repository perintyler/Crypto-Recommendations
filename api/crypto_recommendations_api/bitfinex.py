"""crypto_recommendations.bitfinex.py"""

from collections import namedtuple

from . import broadcast_server
from .recommendations import RecommendationBroadcaster
from .order_books import PricePoint
from . import logs

WSS = 'wss://api-pub.bitfinex.com/ws/2'

EXCHANGE_NAME = 'bitfinex'

BitfinexTickerUpdate = namedtuple('BitfinexTickerUpdate', (
  'channelID',
  'bid',
  'bidSize',
  'ask',
  'askSize',
  'dailyChange',
  'dailyChangeRelative',
  'lastPrice',
  'volume',
  'high',
  'low'
))

def format_pair(symbol, fiat='USD'):
  return 't' + str(symbol) + str(fiat)

def parse_symbol(pair):
  return pair[1:4]

class BitfinexBroadcaster(RecommendationBroadcaster):

  def __init__(self, symbols, books):
    super().__init__(
      WSS, 
      EXCHANGE_NAME, 
      symbols, 
      books
    )

  def subscribe(self):
    logs.exchange_event('sending subscription messages', self.exchange)
    for symbol in self.symbols:
      self.respond(
        event   = 'subscribe',
        pair    = format_pair(symbol),
        channel = self.endpoint, 
        prec    = "R0"
      )

  def unsubscribe(self):
    for channel_id in self.get_open_channels():
      self.respond(
        event  = 'unsubscribe',
        chanId = channel_id
      )

  def on_subscribed(self, msg):
    logs.exchange_event('subscription message', self.exchange, message=msg)
    channel_id = msg['chanId']
    symbol = parse_symbol(msg['symbol'])
    self.set_channel_symbol(channel_id, symbol)

  def message_filter(self, msg):
    return msg.event == 'data_message' and msg[1] == 'hb'

  def parse_price_point(self, msg):
    logs.exchange_event('ticker message', self.exchange, message=msg)
    channel_id, tickerData = msg
    tick = BitfinexTickerUpdate(channel_id, *tickerData)
    symbol = self.get_channel_symbol(channel_id)
    return PricePoint(symbol, tick.bid, tick.ask)
