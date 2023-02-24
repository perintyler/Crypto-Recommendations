"""crypto_recommendations.logs.py"""

from google.oauth2.service_account import Credentials
import google.cloud.logging
from pathlib import Path

from . import settings

USE_STDOUT = True

CLIENT_EVENTS = True

EXCHANGE_EVENTS = True

APPLICATION_EVENTS = True

LOGGER_NAME = 'Websocket-Activity-Logger'

service_file_path = Path(__file__).parent.parent.joinpath('logging-service-key.json')
credentials = Credentials.from_service_account_file(service_file_path)
client = google.cloud.logging.Client(credentials=credentials)
gcp_logger = client.logger(LOGGER_NAME)

def send(messageType, message):
  log = {'type': messageType, 'message': message}
  if settings.DEBUG: 
    print(log)
  if settings.LOG_TO_GCP: 
    gcp_logger.log_struct(log)

def warn(message, **kwargs):
  send('warning', {'message': message, **kwargs})
  
def debug(message, **kwargs):
  send('debug', {'message': message, **kwargs})

def client_event(description, client, **kwargs):
  if not CLIENT_EVENTS: return
  send('clientEvent', {
    'description': description,
    'client': client,
    **kwargs
  })

def exchange_event(description, exchange, **kwargs):
  if not EXCHANGE_EVENTS: return
  send('exchangeEvent', {
    'description': description,
    'exchange': exchange,
    **kwargs
  })

def application_event(description, **kwargs):
  if not APPLICATION_EVENTS: return
  send('applicationEvent', {'description': description, **kwargs})

def use_stdout(): USE_STDOUT = True
