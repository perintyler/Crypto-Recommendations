# Crypto Recommendations Web App

<p align="center">
    <br>
    <a href="https://crypto-books.xyz/">
        <b>www.Crypto-Books.xyz</b>
    </a>
    <br>
    <br>
</p>


Crypto Recommendations is a web-app built with React that displays the best orders (i.e. bids and asks) from 2 different cryptocurrency exchanges and recommends purchases.


## Setup

To run the application locally, both the React app and the Web Socket must be served.

### Requirements

* python3
* Node.js

### Serving the Web Socket

```console
$ cd Crypto-Recommedations-Api
$ python3 -m pip install -r requirements.txt
$ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker crypto_recommendations_api.main:app
```

### Serving the Web App

```console
$ cd Crypto-Recommedations-Web
$ npm install
$ npm start
```

## The Websocket Server

The GCP-hosted backend is a multi-threaded Web Socket server written in Python. The server connects to other public websockets hosted by crypto exchanges, then broadcasts realtime purchase recommendations to all of the server's clients.

* <a href="https://github.com/websocket-client/websocket-client">websocket-client</a>
* <a href="https://github.com/heroku-python/flask-sockets">flask-socket</a>


### Supported Exchanges

* <a href="https://docs.bitfinex.com/reference#rest-public-tickers"> Bitfinex API Docs</a>
* <a href="https://docs.kraken.com/websockets/">Kraken API Docs</a>
