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

from envyaml import EnvYAML
from passlib.hash import pbkdf2_sha256
env = EnvYAML('env.yaml') # read file env.yaml and parse config
from basicauth import decode #import the simple HTTP basic auth encoder and decoder.
import os
from rejson import Client, Path
import json
from flask import Flask, request, make_response, jsonify
from datetime import datetime # Current date time in local system
from passlib.hash import pbkdf2_sha256
from flask_mail import Mail, Message

import redis
app = Flask(__name__)

mail= Mail(app) # initialize the mail object

# define the mail configuration
# create a temporary gmail app password for testing/evaluation

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mzeriorwuese@gmail.com'
app.config['MAIL_PASSWORD'] = 'xvtusfllhozhmeva'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

environmentVariable = dict(os.environ)
print(environmentVariable)
try:
    print(environmentVariable['GOOGLE_CLOUD_PROJECT'])
    rc = redis.Redis(host=env['redisDBRemote.host'], port=env['redisDBRemote.port'], password=env['redisDBRemote.password'], decode_responses=True)
    host = '0.0.0.0'
except KeyError:
    rc = redis.Redis(host=env['redisDBlocal.host'], port=env['redisDBlocal.port'], decode_responses=env['redisDBlocal.DR'])
    host = '127.0.0.1'
log = app.logger


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    # request.headers is actually an EnvironHeaders object that can be accessed like a dictionary
    # Extract the request headers
    #return environmentVariable['COMPUTERNAME']
    res="Undefined"
    
    headers = dict(request.headers)
    
    
    # To decode an encoded basic auth string:'''
    
    try:
        encoded_str = headers['Authorization']
        username, password = decode(encoded_str)
        hash = pbkdf2_sha256.hash(password)
        
        
        if username != env['config.username'] and pbkdf2_sha256.verify(password, hash):
            res = "You are not allowed to call this API"
            return make_response(jsonify({'fulfillmentText': res}))
    except AttributeError:
        res = 'illegal operation'
        return make_response(jsonify({'fulfillmentText': res}))
  
    
    req = request.get_json(silent=True, force=True)
    
    try:
        action = req.get('queryResult').get('action')
        print('Current action: '+action)
    except AttributeError:
        res =  'json error'
        return make_response(jsonify({'fulfillmentText': res}))

    if action == 'register-truck':
        res = registerTruck(req)
    if action == 'add_user':
        res = add_user(req)
    if action == 'search_truck':
        res = search(req)
    if action == 'auth':
        res = auth(req)
    if action == 'email':
        res = covadMail(req)
    else:
        log.error('Unexpected action.')

    return make_response(jsonify({'fulfillmentText': res}))

"""
Call authentication
on successful authentication, we shall invoke add_user event
via fulfillment by setting the followupEventInput 
field of the WebhookResponse. We shall  set the 
followupEventInput.parameters phone number field to provide parameters to the intent.
this phone number filed shall be used to tell us who loggedin.
"""
def auth(req):
    phone = req['queryResult']['parameters']['phone']
    password = req['queryResult']['parameters']['password']
    user_intent = req['queryResult']['parameters']['user_intent']
    """
    TODO by Iorwuese: 
    1)  Check if phone number exixts
    2)  Check if the phone number below to an admin, if not terminate the throw an error
    3)  If the phone number is that of an admin
        Check if the password hash in redis is similar to the hash of the password variable above
        if they are not similar, then throw an error
        IF the passwords are similar, then return the dict below
    """
    if rc.exists(phone)==1:
        password_hash=rc.hget(phone, 'Password')
        user_role=rc.hget(phone, 'User type')
        if user_role == "Administrator":
            if pbkdf2_sha256.verify(password, password_hash) == False:
                res = "You are not allowed to execute this action"
                return make_response(jsonify({'fulfillmentText': res}))
            else:
                if user_intent == 'add user':
                    return {
                        "followupEventInput": {
                            "name": "add_user",
                            "parameters": {
                            "requested_by": "parameter-value-2"
                            },
                            "languageCode": "en-US"
                        }
                    }
                elif user_intent == 'update trip':
                    return {
                        "followupEventInput": {
                            "name": "update_trip",
                            "parameters": {
                            "requested_by": phone
                            },
                            "languageCode": "en-US"
                        }
                    }
                elif user_intent == 'register truck':
                    return {
                        "followupEventInput": {
                            "name": "register_truck",
                            "parameters": {
                            "requested_by": phone
                            },
                            "languageCode": "en-US"
                        }
                    }
                elif user_intent == 'search truck':
                    return {
                        "followupEventInput": {
                            "name": "search_truck",
                            "parameters": {
                            "requested_by": phone
                            },
                            "languageCode": "en-US"
                        }
                    }

#This function shall be used to convert the hash data types returned from redis to strings
def format_hash(my_hash):
	new_val=''
	for value in my_hash:
		params = (value + ': '+my_hash[value])
		new_val = new_val + params+'\n'
	return new_val
#This function shall be used to convert the hash data types returned from redis to strings
def format_hash(my_hash):
	new_val=''
	for value in my_hash:
		params = (value + ': '+my_hash[value])
		new_val = new_val + params+'\n'
	return new_val

#User registration system    
def create_password(password):
    hash = pbkdf2_sha256.hash(password)
    return hash

def registerTruck(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information
    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """

    license_plate = req['queryResult']['parameters']['license_plate_number']
    full_names = req['queryResult']['parameters']['full_name']
    truck_type = req['queryResult']['parameters']['truck-type']
    consignment_type = req['queryResult']['parameters']['consignment_type']
    start_date = req['queryResult']['parameters']['start_date']
    originating_depot = req['queryResult']['parameters']['originating_depot']
    destination_depot = req['queryResult']['parameters']['destination_depot']
    phon_number = req['queryResult']['parameters']['phon_number']
    consignment_class = req['queryResult']['parameters']['consignment_class']
    pipe = rc.pipeline()
    pipe.hset(license_plate, "Phone number", phon_number)
    pipe.hset(license_plate, "Destination depot", destination_depot)
    pipe.hset(license_plate, "Full name", full_names)
    pipe.hset(license_plate, "Originating depot", originating_depot)
    pipe.hset(license_plate, "Consignment class", consignment_class)
    pipe.hset(license_plate, "Truck type", truck_type)
    pipe.hset(license_plate, "Start date", start_date)
    pipe.hset(license_plate, "Consignment type", consignment_type)

    resp = pipe.execute()
    response = resp
    if all(response) == 1:
        response='Truck data successfully saved.'
    else:
        response='Truck data was not saved. It may already exist.'
    return json.dumps(response, indent=4)

#This is an authentication function    

def add_user(req):
    phone = req['queryResult']['parameters']['inspector_phone']
    user_type = req['queryResult']['parameters']['add_user_type']
    password = req['queryResult']['parameters']['password']
    password=create_password(password)
    full_names = req['queryResult']['parameters']['inspector_full_name']
    lga_ops = req['queryResult']['parameters']['lga_pf_ops']
    state_ops = req['queryResult']['parameters']['state_of_ops']
    created = str(datetime.now())
    
    pipe = rc.pipeline()
    pipe.hset(phone, 'User type', user_type)
    pipe.hset(phone, "Date created", created)
    pipe.hset(phone, "State of ops", lga_ops)
    pipe.hset(phone, "Full name", full_names)
    pipe.hset(phone, "Password", password)
    pipe.hset(phone, "LGA Of ops", lga_ops)
    
    resp = pipe.execute()
    response = resp
    if all(response) == 1:
        response='User data successfully saved.'
    else:
        response='User data was not saved. It may already exist.'
    return json.dumps(response, indent=4)

def search(req):
    license_plate = req['queryResult']['parameters']['license_plate']
    if rc.exists(license_plate) == 1:
        response = rc.hgetall(license_plate)
        response = format_hash(response)
    else:
        response = 'This vehicle is not registered'
    return response

def covadMail(req):
    msg=req['queryResult']['parameters']['msg']
    email=req['queryResult']['parameters']['msg']
    mailMsg = Message(msg, sender = 'mzeriorwuese@gmail.com', recipients = [email])
    mailMsg.body = ("Hello", email, " this is your Covad Bot Password", 'pwd', ". Your user role is:", msg)
    mail.send(mailMsg)
    return "Sent"

if __name__ == '__main__':
    app.run(debug=True, host=host)