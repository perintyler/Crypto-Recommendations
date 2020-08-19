
from collections import namedtuple
from exchange.client import ExchangeWebsocket
import ws

WSS = 'wss://api-pub.bitfinex.com/ws/2'
TICKER_FIELDS = (
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
)

def format_pair(symbol, fiat='USD'):
  return 't' + str(symbol) + str(fiat)

def parse_symbol(pair):
  return pair[1:4]

class Client(ExchangeWebsocket):

  def __init__(self, endpoint):
    super().__init__(WSS, 'bitfinex', endpoint)

  def subscribe(self):
    for symbol in self.symbols:
      pair = format_pair(symbol)
      subscription = ws.Message.create(
        event = 'subscribe',
        pair = format_pair(symbol),
        channel = self.endpoint, prec="R0",)
      self.respond(subscription)

  def on_subscribed(self, msg):
    channelID = msg['chanId']
    symbol = parse_symbol(msg['symbol'])
    self.channels[channelID] = symbol

  def filter(self, msg):
    print(msg.event == 'data_message' and msg[1] == 'hb', msg)
    return msg.event == 'data_message' and msg[1] == 'hb'

class Ticker(Client):

  Response = namedtuple('BitfinexTicker', TICKER_FIELDS)

  def __init__(self):
    super().__init__('ticker')

  def on_data_message(self, msg):
    channelID, tickerData = msg
    data = Ticker.Response(channelID, *tickerData)
    symbol = self.channels[data.channelID]
    bid,ask = data.bid, data.ask
    self.update_price(symbol, bid, ask)
