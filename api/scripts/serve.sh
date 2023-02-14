#!/bin/bash

gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker crypto_recommendations_api.main:app