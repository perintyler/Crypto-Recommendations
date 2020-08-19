
from collections import namedtuple
from exchange.client import ExchangeWebsocket
import ws
WSS = 'wss://ws.kraken.com/'
TICKER_FIELDS = ('channelID', 'ticker', 'channelName', 'pair')

def format_pair(symbol, fiat='USD'):
  return str(symbol) + '/' + str(fiat)

def get_symbol(pair):
  return pair.split('/')[0]  # (symbol, fiat)[0]

class KrakenClient(ExchangeWebsocket):
  """Kraken Client Websocket"""

  def __init__(self, endpoint):
    super().__init__(WSS, 'kraken', endpoint)

  def subscribe(self):
    subscription = ws.Message.create(
      event='subscribe',
      subscription = {'name': self.endpoint},
      pair = [format_pair(symbol) for symbol in self.symbols])
    self.respond(subscription)

  def on_subscription_status(self, msg):
    channelID = msg['channelID']
    symbol = get_symbol(msg['pair'])
    self.channels[channelID] = symbol

class Ticker(KrakenClient):

  Response = namedtuple('KrakenTicker', TICKER_FIELDS)

  def __init__(self):
    super().__init__('ticker')

  def on_data_message(self, msg):
    data = Ticker.Response(*msg)
    symbol = self.channels[data.channelID]
    bid = data.ticker['b'][0]
    ask = data.ticker['a'][0]
    self.update_price(symbol, bid, ask)
