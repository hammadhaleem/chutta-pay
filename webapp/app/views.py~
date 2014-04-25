import time
import os
from flask import Blueprint, request, jsonify
from werkzeug import secure_filename
from app import app
import kookoo
import pickle
import sys, os, json, urllib2, urllib, time
import requests
import requests, json, os.path
import mechanize, cookielib, urllib2
from bs4 import BeautifulSoup



@app.route('/')
@app.route('/index')
@app.route('/api/', methods=['GET'])
@app.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        json_results = []
        output = {'greetings':'Welcome to api'}
        json_results.append(output)
    return jsonify(items=json_results)

