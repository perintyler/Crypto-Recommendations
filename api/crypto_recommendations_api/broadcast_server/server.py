"""broadcast_server.server"""

import _thread
import threading
import gevent

from .. import logs

__broadcasters__ = []

def add_broadcaster(broadcaster):
  __broadcasters__.append(broadcaster)
  def thread(*args): broadcaster.run_forever()
  _thread.start_new_thread(thread, ())
  gevent.sleep(0.1)
  broadcaster.start()

def remove_broadcaster(broadcaster):
  if broadcaster.is_broadcasting(): 
    broadcaster.close()
  __broadcasters__.remove(broadcaster)

def has_broadcaster(): 
  return len(__broadcasters__) != 0

def num_clients():
  return 0 if not __broadcasters__ else __broadcasters__[0].num_clients()

def start_broadcasting():
  for broadcaster in __broadcasters__:
    broadcaster.start()

def stop_broadcasting():
  """called when all connections are closed"""
  for broadcaster in __broadcasters__:
    broadcaster.stop()

def connect_client(websocket):
  for broadcaster in __broadcasters__:
    broadcaster.add_client(websocket)

  while not websocket.closed:
    message = websocket.receive()
    logs.application_event('recieved client message', message=message)
     # Sleep to prevent constant context-switches. This does
     # not affect update speed, which happens on another thread
    gevent.sleep(0.1)

  for broadcaster in __broadcasters__:
    broadcaster.remove_client(websocket)

