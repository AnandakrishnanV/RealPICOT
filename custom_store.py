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
	data["message"]=data["message"].replace('"',"")
	data["topic"]=data["topic"].replace("'","")
	print (data["message"])
	jst = json.dumps(data)
	jst = jst.replace('"',"'")
	
	print (jst)		
	api.publish('stream1',data["sender"],{"json":jst})

	result = datasend.receive_data(data)

	# if result is none then write failed
