"""crypto_recommendations.app"""

from flask import Flask
from flask_sockets import Sockets
import gevent
import sentry_sdk

from . import broadcast_server
from . import logs
from . import settings
from . import recommendations
from .order_books import OrderBooks
from .kraken import KrakenBroadcaster
from .bitfinex import BitfinexBroadcaster

logs.application_event('starting server')

sentry_sdk.init(
  dsn="https://95c656ef4dfb4741bd11728ebb022857@o4504612748328960.ingest.sentry.io/4504614504497152", 
  traces_sample_rate=1.0
)

app = Flask(__name__)
sockets = Sockets(app)

if settings.DEBUG: 
  broadcast_server.enable_trace()

books = OrderBooks()
krakenWebsocket = KrakenBroadcaster(settings.SYMBOLS, books)
bitfinexWebsocket = BitfinexBroadcaster(settings.SYMBOLS, books)
broadcast_server.add_broadcaster(krakenWebsocket)
broadcast_server.add_broadcaster(bitfinexWebsocket)

@sockets.route('/')
def on_connection(ws):
  """called whenever a user connects to the server"""
  logs.application_event('new connection', websocket=str(ws))
  broadcast_server.connect_client(ws)
