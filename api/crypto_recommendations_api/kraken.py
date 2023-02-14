"""crypto_recommendations.kraken.py"""

from collections import namedtuple

from .recommendations import RecommendationBroadcaster
from .order_books import PricePoint
from . import logs

WSS = 'wss://ws.kraken.com/'

EXCHANGE_NAME = 'kraken'

KrakenTickerUpdate = namedtuple('KrakenTickerUpdate', [
  'channel_id', 
  'ticker', 
  'channelName', 
  'pair'
])

def format_pair(symbol, fiat='USD'):
  return str(symbol) + '/' + str(fiat)

def get_symbol(pair):
  return pair.split('/')[0]  # (symbol, fiat)[0]

class KrakenBroadcaster(RecommendationBroadcaster):
  """Kraken Client Websocket"""

  def __init__(self, symbols, books):
    super().__init__(WSS, EXCHANGE_NAME, symbols, books)

  def subscribe(self):
    logs.exchange_event('sending subscription messages', self.exchange)
    self.respond(
      event='subscribe',
      subscription = {'name': self.endpoint},
      pair = [format_pair(symbol) for symbol in self.symbols]
    )

  def unsubscribe(self):
    for channel_id in self.get_open_channels():
      self.respond(
        event     = 'unsubscribe',
        channelID = channel_id
      )

  def on_subscription_status(self, msg):
    logs.exchange_event('subscription message', self.exchange, message=msg)
    channel_id = msg['channelID']
    symbol = get_symbol(msg['pair'])
    self.set_channel_symbol(channel_id, symbol)

  def parse_price_point(self, msg):
    logs.exchange_event('ticker message', self.exchange, message=msg)
    tick = KrakenTickerUpdate(*msg)
    symbol = self.get_channel_symbol(tick.channel_id)
    bid = tick.ticker['b'][0]
    ask = tick.ticker['a'][0]
    return PricePoint(symbol, bid, ask)
