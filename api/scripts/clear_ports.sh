#!/bin/bash

kill -9 $(lsof -i:8080 -t) 2> /dev/null