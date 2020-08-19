# -*- coding: utf-8 -*-
"""Websocket Server

The server processes data from external websockets, then repackages
the data to be sent to clients. This module can be customized by
subclassing Listener to create custom data pipelines.
"""

import _thread
import json
import time
from inflection import underscore
from websocket import WebSocketApp
from flask import Flask
from flask_sockets import Sockets

clients   = [] # connected client
listeners = [] # external clients

app = Flask(__name__)
sockets = Sockets(app)

def add_listener(ws):    listeners.append(ws)
def remove_listener(ws): listeners.remove(ws)

def listen():
  for ws in listeners:
    if not ws.is_idle(): continue
    def thread(*args): ws.run_forever()
    _thread.start_new_thread(thread, ())
    time.sleep(0.1)

def stop_listening():
  for ws in listeners:
    print(ws.is_idle())
    if ws.is_idle(): continue
    ws.close()
  threading.active_count()

@sockets.route('/')
def on_connection(ws):
  print('client connected', ws)
  clients.append(ws)
  listen()
  while not ws.closed:
    message = ws.receive()
     # Sleep to prevent constant context-switches. This does
     # not affect update speed, which happens on another thread
    gevent.sleep(0.1)

  print('client disconnected', ws)
  clients.remove(ws)
  if not clients:
    stop_listening()

class Message:

  def __init__(self, jsonStr, speaker=None):
    self.contents = json.loads(jsonStr)
    self.speaker = speaker

  @property
  def event(self):
    if self.is_list():
      return 'data_message'
    return self.contents.get('event', 'data_message')

  def is_list(self):
    return isinstance(self.contents, list)

  def stringify(self):
    return json.dumps(self.contents)

  def __getitem__(self, key):
    return self.contents[key]

  def __str__(self):
    return str(self.contents)

  def __repr__(self):
    return f'<Message event={self.event} speaker={self.speaker}>'

  @classmethod
  def create(cls, **props):
    msg = json.dumps({**props})
    return cls(msg)

class Listener(WebSocketApp):
  """Filters, formats, and broadcasts Messages

  A Client Websocket App that connects to an external websocket
  server to forward messages through this server. To create an
  event callback for event 'eventName', define a function named
  on_event_name, and it will automatically be called.
  """

  def __init__(self, wss, **kwargs):
    super().__init__(wss, on_message=self.on_message,
                          on_error=lambda e: print(e),
                          on_close=lambda c: print(f'closing {wss}'),
                          **kwargs)

  def on_message(self, jsonStr):
    """Calls event handler if defined"""
    msg = Message(jsonStr, self.url)
    if not self.filter(msg):
      callbackName = f'on_{underscore(msg.event)}' # 'eventName' -> 'on_event_name'
      event_handler = getattr(self, callbackName, None)
      if callable(event_handler):
        event_handler(msg.contents)

  def broadcast(self, msg):
    """Sends data to all server clients"""
    print('broadcast', msg)
    jsonStr = msg.stringify()
    for ws in clients:
      ws.send(jsonStr)

  def respond(self, msg):
    """Sends data to the external websocket server"""
    self.send(msg.stringify())

  def is_idle(self):
    return not self.sock

  # subclass functions
  def on_data_message(self, msg): pass
  def format_message(self, data): pass
  def filter(self, msg): pass
