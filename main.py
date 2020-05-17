# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample for a weather fulfillment webhook for an Dialogflow agent
This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather

This sample uses the WWO Weather Forecast API and requires an WWO API key
Get a WWO API key here: https://developer.worldweatheronline.com/api/
"""
from flask_redis import FlaskRedis
from envyaml import EnvYAML

# read file env.yaml and parse config
env = EnvYAML('env.yaml')
#import the simple HTTP basic auth encoder and decoder.
from basicauth import decode
#from dotenv import load_dotenv
#load_dotenv()
import os

from rejson import Client, Path

import json

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
log = app.logger


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    # request.headers is actually an EnvironHeaders object that can be accessed like a dictionary
    # Extract the request headers
    
    headers = dict(request.headers)
    
    
    # To decode an encoded basic auth string:
    
    try:
        encoded_str = headers['Authorization']
        username, password = decode(encoded_str)
        print (username, password)
        print(env['project.name'])
       
    except AttributeError:
        return 'illegal operation'
  
    
    res="Undefined"
    req = request.get_json(silent=True, force=True)
    return req
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'weather':
        res = weather(req)    
    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


def weather(req):
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
