"""crypto_recommendations.recommendations.py"""

from . import broadcast_server
from .settings import SYMBOLS, EXCHANGES, BITFINEX, KRAKEN
from . import logs

class Recommendation:

  def __init__(self, order_type, exchange, profit):
    self.order_type = order_type
    self.exchange = exchange
    self.profit = profit

  def as_dict(self):
    return {
      'order': self.order_type, 
      'exchange': self.exchange,
      'profit': round(self.profit, 4)
    }

def get_recommendations_legacy(books) -> list:
  recommendations = []

  if not books.is_compiled(SYMBOLS, EXCHANGES):
    return recommendations # TODO: i think i can get rid of this

  for symbol in SYMBOLS:
   
    bitfinexPricePoint = books.get_price_point(BITFINEX, symbol)
    krakenPricePoint = books.get_price_point(KRAKEN, symbol)
    bidDiff = float(bitfinexPricePoint.bid - krakenPricePoint.bid)
    askDiff = float(bitfinexPricePoint.ask - krakenPricePoint.ask)
    bidDiff, askDiff = round(bidDiff, 4), round(askDiff, 4)
    
    if bidDiff != 0:
      exchange = 'bitfinex' if bidDiff > 0 else 'kraken'
      recommendations.append(f'Buy {symbol} from {exchange} (+${abs(bidDiff)})')
    if askDiff != 0:
      exchange = 'bitfinex' if askDiff < 0 else 'kraken'
      recommendations.append(f'Sell {symbol} to {exchange} (-${abs(askDiff)})')
  
  return recommendations

def get_recommendations(books) -> list:
  recommendations = []

  if books.num_exchanges() < 2:
    return recommendations

  for symbol in SYMBOLS:
    
    bitfinexPricePoint = books.get_price_point(BITFINEX, symbol)
    krakenPricePoint  = books.get_price_point(KRAKEN, symbol)
    
    if bitfinexPricePoint.bid != krakenPricePoint.bid:
      profit = float(bitfinexPricePoint.bid - krakenPricePoint.bid)
      recommendations.append(Recommendation(
        'bid', 
        'bitfinex' if profit > 0 else 'kraken',
        profit
      ))

    if bitfinexPricePoint.ask != krakenPricePoint.ask:
      profit = float(bitfinexPricePoint.ask - krakenPricePoint.ask)
      recommendations.append(Recommendation(
        'ask', 
        'bitfinex' if profit > 0 else 'kraken',
        profit
      ))

  return sorted(recommendations, key=lambda rec: rec.profit)

class RecommendationBroadcaster(broadcast_server.Broadcaster):
  """Listens to bids and asks from an exchange's websocket
  and repackages the data as recommendations to be broadcasted"""

  def __init__(self, wss, exchange, symbols, books):
    super().__init__(wss, on_open=self.subscribe)
    self.exchange = exchange
    self.symbols = symbols
    self.books = books
    self.endpoint = 'ticker'
    self.channels = {}

  def add_client(self, client):
    logs.exchange_event('adding client', self.exchange, client=client.origin)
    super().add_client(client)
    if self.books.num_exchanges() >= 2:
      self.broadcast_recommendations()

  def parse_price_point(self, msg):
    """Returns a `order_books.PricePoint`. This function is designed
    to be overriden"""
    pass
    
  def subscribe(self):
    pass

  def unsubscribe(self):
    pass

  def broadcast_recommendations(self):
    self.broadcast(
      event             = 'recommendations',
      recommendations   = get_recommendations_legacy(self.books),
      recommendationsV2 = [rec.as_dict() for rec in get_recommendations(self.books)],
      prices            = self.books.as_dict(),
    )

  def on_data_message(self, msg):
    """update order books and broadcast recommendations"""
    price_point = self.parse_price_point(msg)
    logs.exchange_event('recieved price point', self.exchange, price_point=price_point.as_dict())
    self.books.handle_price_point(self.exchange, price_point)
    self.broadcast_recommendations()

  def set_channel_symbol(self, channel_id, symbol):
    self.channels[channel_id] = symbol

  def get_channel_symbol(self, channel_id):
    assert channel_id in self.channels
    return self.channels[channel_id]

  def get_open_channels(self):
    return self.channels.keys()

  def clear_channels(self):
    self.channels.clear()

  def is_subscribed(self):
    """a subscription requires an open channel each supported cryptocurrency"""
    return len(self.channels.keys()) == len(self.symbols)

  def stop(self):
    logs.exchange_event('unsubscribing from exchange', self.exchange)
    # self.unsubscribe()

  def start(self):
    logs.exchange_event('subscribing to exchange', self.exchange)
    # self.subscribe()

  def __repr__(self):
    return f'<RecommendationBroadcaster exchange="{self.exchange}" channels={self.channels}>'

