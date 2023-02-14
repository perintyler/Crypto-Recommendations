#!/bin/bash

gcloud config set project crypto-order-books-376705;
gcloud app deploy --quiet;
gcloud app logs tail -s default;