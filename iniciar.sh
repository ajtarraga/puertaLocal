#!/bin/bash

source auth/bin/activate
export FLASK_APP=project
export FLASK_DEBUG=0
flask run --host=192.168.0.26 --port=5000