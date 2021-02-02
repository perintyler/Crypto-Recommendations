<h1>Real-time Crypto</h1>

Python multi-threaded websocket server and react web application, which uses the <a href="material-ui.com">material-ui</a> framework. The websocket server is hosted on GCP, and the react app is hosted on firebase.  

<h2>Websocket Server</h2>
The server connects to public websockets hosted by crypto exchanges. Messaged received are filter, parsed, formatted, and then broadcasted on the server.



<h4>Exchanges</h4>

* <a href="https://docs.bitfinex.com/reference#rest-public-tickers"> Bitfinex API Docs</a>
* <a href="https://docs.kraken.com/websockets/">Kraken API Docs</a>

<h4>Websocket Libraries</h4>

* <a href="https://github.com/websocket-client/websocket-client">websocket-client</a>
* <a href="https://github.com/heroku-python/flask-sockets">flask-socket</a>

<h4>Requirements</h4>

* python3
* pip3
* npm

<h3>Setup</h3>

To locally host the python server:
```console
~$ cd api
~/api$ pip3 install -r requirements.txt
~/api$ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app
```

To start the react app:

```console
~$ cd web
~/web$ npm install
~/web$ npm start
```
