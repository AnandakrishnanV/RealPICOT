#!/usr/bin/python2.7

################################################################
# @Bevywise.com IOT Initiative. All rights reserved 
# www.bevywise.com Email - support@bevywise.com
#
# custom_store.py
#
# The custom data store hook for the Big Data Storage. 
# The Custom data hook can be enabled in the broker.conf 
# inside conf/ folder.
# 
# The parameter data will be in dict format and the keys are 'sender','topic', 'message', 'unixtime', 'timestamp'
#
################################################################

import os, sys

global datasend

sys.path.append(os.getcwd()+'/../extensions')

# Importing the custom class into the handler

from customimpl import DataReceiver

datasend = DataReceiver()

def handle_Received_Payload(data):

	#
	# Write your code here. Use your connection object to 
	# Send data to your data store
	#dat = open("/home/hbg/test.txt","a")
	#dat.write("Rcvd: %s \n" % data)
	#dat.close
	
	import json	
	
	from Savoir import Savoir
	rpcuser = 'multichainrpc'
	rpcpasswd = 'CTYKR8VwcMD42d7xLuQe1Mt8f4DB9o8s8wVtTjeTfmKi'
	rpchost = 'localhost'
	rpcport = '9558'
	chainname = 'chain1'

	api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
	b = api.liststreamkeys('stream2')
	q = data["sender"]
	f = 0
	for i in range(len(b)):
		if q == b[i]["key"]:
			f = 1
	if f == 0:
		y= api.getnewaddress()
		api.publish('stream2',q,{"text":y})


	c = api.liststreamkeys('stream3')
	f1 = 0
	for j in range(len(c)):
		if q == c[j]["key"]:
			f1 = 1
	if f1 == 0:
		api.publish('stream3',q,{"text":data["topic"]})			

	data["message"]=data["message"].replace('"',"")
	data["topic"]=data["topic"].replace("'","")
	print (data["message"])
	jst = json.dumps(data)
	jst = jst.replace('"',"'")
	
			
	api.publish('stream1',data["sender"],{"json":jst})

	result = datasend.receive_data(data)

	# if result is none then write failed
