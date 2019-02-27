#!/usr/bin/env python2.7

#Importing MQTTClient Library
import py_mqtt_client

import sys
import time

#Getting Connection Information

#Set portno_value to 8883 for Secured connection
SERVER_NAME="localhost"
SERVER_PORT=int(1883)


#MQTT Connect Details
MQClientID="JID01"
timeout=60
clean_session=0
willflag=True
willqos=0
willretain=True
willtopic="Laptop_Status"
willmessage="Laptop_is_Shutdown"


#MQTTClient Instance Creation
Client=py_mqtt_client.MQTTclient(MQClientID,SERVER_PORT,timeout,SERVER_NAME,clean_session,willflag=willflag,willqos=willqos,willretain=willretain,willtopic=willtopic,willmessage=willmessage)


##### Verification Prints	###################
print "#####\tDevice Details\t#####\n Device_Name: %s\t Willtopic: %s \tWillMessage: %s\n"%(MQClientID,willtopic,willmessage)
print "#####\tConnection Details\t#####\nServerName: %s\t ServerPort: %s \n"%(SERVER_NAME,SERVER_PORT)
raw_input("********->\tPlease see if your confs are correct and Press Enter to connect\t<-*******")



#Connecting MQTTClient With Broker
if not Client.connect():
	print "Error While Connecting"
	sys.exit(0)
else:
	print "******\tMQTT Client Connected\t******\n"


#Subscribe To Topic With Qos1
Subscribe_Topic_Name = "Bulb_Con"
Subscribe_Topic_Qos = 1
Client.subscribe(Subscribe_Topic_Name,Subscribe_Topic_Qos)


while 1:
	#Publish To a Topic With Retain  and QOS0
	a=input("")
	if a == 1:
		Publish_Topic_Name = "Bulb_Con"
		Publish_Message = "ON"
		Publish_Retain = 1
		Publish_Qos = 0
		Client.publish(Publish_Topic_Name,Publish_Message,Publish_Retain,Publish_Qos)
		time.sleep(5)
	elif a == 2:
		Publish_Topic_Name = "Bulb_Con"
		Publish_Message = "OFF"
		Publish_Retain = 1
		Publish_Qos = 0
		Client.publish(Publish_Topic_Name,Publish_Message,Publish_Retain,Publish_Qos)
		time.sleep(3)



#Disconnect The Client
Client.disconnect()

