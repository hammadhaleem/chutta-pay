import MySQLdb, re
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


def db_connect():
  db = MySQLdb.connect(host="localhost", user="root", passwd="kgggdkp1992", db="chuttapay")
  return db

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

@app.route('/api/user/add',methods=['GET','POST'])
def useradd():
	error = "success"
	if request.method == 'GET' or request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		user_id = ""       
		phno = request.values.get("phno")
		passw = request.values.get("passwd")
		data = con.execute("SELECT id FROM users WHERE phnum = "+phno)
		if data == 1:
			error = "fail"
		else:
			query = "INSERT INTO users ( phnum , password ) VALUES ('" +phno+"','"+passw+"')"
			print query
			con.execute(query)
			con.execute("SELECT id FROM users WHERE phnum = "+phno)
			user_id = re.search(r'[0-9]+',str(con.fetchall())).group()
		
		db.commit()
		db.close()
		output = {'phnum':phno,'status': error,'user_id':user_id}
		json_results.append(output)
		return jsonify(items=json_results)

@app.route('/api/transaction/send',methods=['GET','POST'])
def tr_send():
	error = "success"	
	if request.method == 'GET' or request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		#con.execute("INSERT INTO `transaction`(`toid`, `fromid`, `amount`) VALUES ('9995', '99999', '20')")
		amount = request.values.get("amount")
		fromid = request.values.get("from")
		toid = request.values.get("to")
		con.execute("SELECT balance FROM users WHERE phnum = "+fromid)
		
		a = str(con.fetchall())
		balance = int(re.search(r'[0-9]+',a).group())
		
		if balance > amount:
			error="fail"
		else:
			con.execute("UPDATE `users` SET `balance`="+str(balance - int(amount))+" WHERE phnum = "+fromid)
			con.execute("SELECT balance FROM users WHERE phnum = "+toid)
			a = str(con.fetchall())
			balance = int(re.search(r'[0-9]+',a).group())
			con.execute("UPDATE `users` SET `balance`="+str(balance + int(amount))+" WHERE phnum = "+toid)
			query = "INSERT INTO `transaction`(`toid`, `fromid`, `amount`) VALUES ('"+toid+"', '"+fromid+"', '"+amount+"')"
			print query			
			con.execute(query)
		
		db.commit()
		db.close()
		output = {'balance':balance,'status': error}
		json_results.append(output)
		return jsonify(items=json_results)

@app.route('/api/transaction/getall',methods=['GET','POST'])
def tr_get():
	if request.method == 'GET' or request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		tids = []
		user_id = request.values.get("user_id")
		con.execute("SELECT tid FROM `transaction` WHERE toid= "+user_id+" OR fromid = "+user_id)
		data = con.fetchall()
		for tid in data:
			tids.append(re.search(r'[0-9]+',str(tid)).group())
		output = {'transaction':tids}
		json_results.append(output)
		return jsonify(items=json_results)	
			
	

