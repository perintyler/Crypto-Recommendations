#!/bin/bash

pushd ./api && bash ./scripts/serve.sh && popd  &
pushd ./web && npm start && popd;