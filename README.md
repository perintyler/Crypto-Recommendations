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

### Requirements

To run the application locally, both the React app and the Web Socket must be served.

* pip3
* npm

---

## The Websocket Server

The GCP-hosted backend is a multi-threaded Web Socket server written in Python. The server connects to other public websockets hosted by crypto exchanges, then broadcasts realtime purchase recommendations to all of the server's clients.

### Locally Hosting the Web Socket Server

```console
$ cd ./api
$ python3 -m pip install -r requirements.txt
$ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker crypto_recommendations_api.main:app
```

### Testing the Websocket Server

To use the server's test suite, install the developer requirements.

```
$ pip3 install -r ./api/dev-requirements.txt
```

Then run the tests using the [pytest](https://docs.pytest.org/en/7.2.x/) framework.

```
$ pytest ./api/tests.py
```

### Deploying the Websocket Server

A deployment script is available to deploy the Web Socket server to `Google App Engine` with a single bash command.

```console
$ cd ./api
$ bash ./scripts/deploy.sh
```

#### Supported Exchanges

* <a href="https://docs.bitfinex.com/reference#rest-public-tickers"> Bitfinex API Docs</a>
* <a href="https://docs.kraken.com/websockets/">Kraken API Docs</a>

#### Web Socket Libraries

* <a href="https://github.com/websocket-client/websocket-client">websocket-client</a>
* <a href="https://github.com/heroku-python/flask-sockets">flask-socket</a>

---

## The Web App

The Web App is built with React and is hosted on Firebase.

### Serving the Web App

To locally serve the React application for development, use the `npm start` command.

```console
$ cd ./web
$ npm install
$ npm start
```

### Testing the Web App

To run the front-end Jest tests:

```console
$ cd ./web
$ npm run test
```

### Deploying the Web App

A deployment script is available to deploy the app to firebase with a single bash command.

```console
$ cd ./web
$ bash ./deploy.sh
```
