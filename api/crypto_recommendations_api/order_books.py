"""crypto_recommendations.order_books.order_books"""

class PricePoint:

  def __init__(self, symbol, bid, ask):
    self.symbol = symbol if symbol != 'XBT' else 'BTC'
    self.bid = float(bid)
    self.ask = float(ask)

  def as_dict(self):
    return {'symbol': self.symbol, 'bid': self.bid, 'ask': self.ask}

  def __hash__(self, other): return self.symbol == other.symbol
  
  def __eq__(self, other): 
    return self.symbol == other.symbol \
        and self.bid == other.bid and self.ask == other.ask

  def __repr__(self):
    return f'<PricePoint symbol="{self.symbol}" bid={self.bid} ask={self.ask}>'

class ExchangeTicker:
  """A 'tick' is any change in the price of a security"""

  def __init__(self, exchange):
    self.exchange = exchange
    self.price_points = {}

  def has_symbol(self, symbol):
    return symbol in self.price_points

  def get_price_point(self, symbol):
    return self.price_points[symbol] if self.has_symbol(symbol) else None

  def is_update(self, symbol, bid, ask):
    if not self.has_symbol(symbol): return True
    oldPricePoint = self.price_points[symbol]
    return oldPricePoint.bid != bid or oldPricePoint.ask != ask
  
  # rename to update
  def handle_price_point(self, price_point):
    symbol = price_point.symbol
    if not self.has_symbol(symbol): 
      self.price_points[symbol] = price_point
    elif price_point != self.get_price_point(symbol):
      self.price_points[symbol] = price_point

  def as_dict(self):
    return [price_point.as_dict() for price_point in self.price_points.values()]

  def num_price_points(self):
    return len(self.price_points)

  def __repr__(self):
    return f'<ExchangeTicker price_point={self.as_dict()}'

class OrderBooks:

  def __init__(self):
    self.tickers = {}

  def has_exchange(self, exchange):
    return exchange in self.tickers

  def get_price_point(self, exchange, symbol):
    if not self.has_exchange(exchange): return None
    return self.tickers[exchange].get_price_point(symbol)

  # move this to test file
  def is_compiled(self, all_symbols, all_exchanges):
    for ticker in self.tickers.values():
      if ticker.num_price_points() != len(all_symbols):
        return False
    return self.num_exchanges() == len(all_exchanges)

  def handle_price_point(self, exchange, price_point):
    if exchange not in self.tickers: 
      self.tickers[exchange] = ExchangeTicker(exchange)
    self.tickers[exchange].handle_price_point(price_point)

  def as_dict(self):
    return {ticker.exchange: ticker.as_dict() for ticker in self.tickers.values()}

  def num_exchanges(self):
    return len(self.tickers)

  def is_empty(self):
    return self.num_exchanges() == 0

  @property
  def exchanges(self):
    return [ticker.exchange for ticker in self.ticker.values()]


