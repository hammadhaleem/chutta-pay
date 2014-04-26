import MySQLdb, re
import time
import os
from flask import Blueprint, request, jsonify
from werkzeug import secure_filename
from app import app
import pickle
import sys, os, json, urllib2, urllib, time
import requests
import requests, json, os.path
import mechanize, cookielib, urllib2
from bs4 import BeautifulSoup

def buildHTML(text):
	var = "<html><head><title> Hello! </title><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><meta name='txtweb-appkey' content='4abf3150-754e-46de-998e-42a2b99605df' /></head><body>"
	var =var + str(text)
	var = var+ "</body></html>"
	return var 


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


@app.route('/api/msg',methods=['GET'] )

def RegMsg():
	if request.method == 'GET' :
		try :
			text = request.values.get("txtweb-message")
			data = text.split(" ")
		except :
			return buildHTML("Error")
		if data[0] == 'register':
			return buildHTML("Register")
		elif data[0] == 'my-id':
			return  buildHTML(str( request.values.get("txtweb-id")))
		elif data[0] == 'transfer':
			return buildHTML(str("transfer"))
		else :
			return buildHTML("Error")

	



@app.route('/api/user/add',methods=['GET','POST'])
def useradd():
	error = "success"
	if request.method == 'GET' :
		return jsonify({'Method':'Get:not supported'})

	if request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		user_id = ""       
		phno = request.values.get("phno")
		passw = request.values.get("passwd")
		data = con.execute("SELECT id FROM users WHERE phnum = "+phno)
		if data == 1:
			error = "fail"  # user already exist , just return his id
			a = str(con.fetchall())
			user_id = int(re.search(r'[0-9]+',a).group())
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

@app.route('/api/user/amount',methods=['GET','POST'])
def useradd():
	error = "success"
	if request.method == 'GET':
		return jsonify({'Method':'Get:not supported'})

	if request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		
		user_id = request.values.get("user_id")
		
		con.execute("SELECT balance FROM users WHERE id = "+user_id)
		balance = str(con.fetchall()[0][0])
		db.close()
		output = {'user_id':user_id,'balance':balance}
		json_results.append(output)
		return jsonify(items=json_results)

@app.route('/api/transaction/send',methods=['GET','POST'])
def tr_send():
	stat = True
	error = "ok"	

	if request.method == 'GET' :
		return jsonify( {'Method':'Get:not supported'})

	if request.method == 'POST':

		db = db_connect()
		con = db.cursor()
		json_results = []
		newbalance = 0
		amount = request.values.get("amount")
		fromid = request.values.get("from_user_id")
		toid = request.values.get("to_user_id")
		passwd = request.values.get("passwd")
		con.execute("SELECT balance FROM users WHERE id = "+fromid)
		a = str(con.fetchall())
		
		if len(a)>2:
			balance = int(re.search(r'[0-9]+',a).group())
		else:
			balance = 0
		if balance < int(amount):
			stat = False
		
		toexist = con.execute("SELECT id FROM `users` WHERE id ="+toid)
		if toexist != 1:
			stat = False
		
		fromexist = con.execute("SELECT id FROM `users` WHERE id ="+fromid)
		if fromexist != 1:
			stat = False
		
		con.execute("SELECT password from `users` WHERE id = "+fromid)
		
		if passwd != con.fetchall()[0][0]:
			stat = False;
		
		
		if stat == False:
			error="fail"
		else:
			
			newbalance = str(balance - int(amount))
			con.execute("UPDATE `users` SET `balance`="+newbalance+" WHERE id = "+fromid)
			con.execute("SELECT balance FROM users WHERE id = "+toid)
			a = str(con.fetchall())
			balance = int(re.search(r'[0-9]+',a).group())
			con.execute("UPDATE `users` SET `balance`="+str(balance + int(amount))+" WHERE id = "+toid)
			query = "INSERT INTO `transaction`(`toid`, `fromid`, `amount`) VALUES ('"+toid+"', '"+fromid+"', '"+amount+"')"
			print query			
			con.execute(query)
		
		db.commit()
		db.close()
		output = {'balance':newbalance,'status': error}
		json_results.append(output)
		return jsonify(items=json_results)

@app.route('/api/transaction/getall',methods=['GET','POST'])
def tr_get():
	if request.method == 'GET' :
		return jsonify({'Method':'Get:not supported'})
	if request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		tids = []
		user_id = request.values.get("user_id")
		con.execute("SELECT * FROM `transaction` WHERE toid= "+user_id+" OR fromid = "+user_id)
		data = con.fetchall()
		for row in data:
			tids.append({"tid":str(row[0]),"to":str(row[1]),"from":str(row[2]),"amount":str(row[3]),"timestamp":str(row[4])})
		output = {'transaction':tids}
		json_results.append(output)
		return jsonify(items=json_results)	
			
@app.route('/api/transaction/getinfo',methods=['GET','POST'])
def tr_info():
	if request.method == 'GET' :
		return jsonify({'Method':'Get:not supported'})
	if  request.method == 'POST':
		db = db_connect()
		con = db.cursor()
		json_results = []
		tid = request.values.get("tid")		
		con.execute("SELECT * FROM `transaction` where `tid`="+tid)
		data = con.fetchall()
		data = data[0]
		output = {"transaction":{"to":str(data[1]),"from":str(data[2]),"amount":str(data[3]),"timestamp":str(data[4])}}
		json_results.append(output)
		return jsonify(items=json_results)
		return str(data[0][0])
		return str(data)
