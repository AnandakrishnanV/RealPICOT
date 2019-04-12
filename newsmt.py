import threading
import time
import json
import requests
import pickle
import yaml
from simple_websocket_server import WebSocketServer, WebSocket

url = "http://localhost:8080/api/login"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'Authorization': "",
    'cache-control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers)

q = json.loads(response.content) #token to dict

l = ["plc"]

from Savoir import Savoir
rpcuser = 'multichainrpc'
rpcpasswd = 'CTYKR8VwcMD42d7xLuQe1Mt8f4DB9o8s8wVtTjeTfmKi'
rpchost = 'localhost'
rpcport = '9558'
chainname = 'chain1'

ap = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

class SimpleEcho(WebSocket):

        def handle(self):
                # echo message back to client
                l[0] = self.data
                print l[0][2]

        def connected(self):
                print(self.address, 'connected')

        def handle_close(self):
                print(self.address, 'closed')


server = WebSocketServer('', 8000, SimpleEcho)
def srvr():
    server.serve_forever()

def engine():
        while True:
                if l[0][2] == "R":
                        
                        tmp = l[0]
                        tmp = tmp.encode('latin1')
                        js = yaml.safe_load(tmp)
                        a = list(js["Events"].keys())
                        NoE = len(js["Events"])
                        
                        #Check blockchain for change
                        flag = 0
                        z = 0
                        info = ap.liststreamitems('stream1',False,1)
                        while True:
                                
                                c = ap.liststreamitems('stream1',False,1)
                                if c == info :
                                        flag = 1
                                else : 
                                        flag = 0
                                        info = c
                                        z = z+1
                                        p = info[0]
                                        y = p["data"]["json"]
                                        y = y.encode('latin1')
                                        d = yaml.safe_load(y) 
                                        if js["RootDevice"] == p["keys"][0] and d["message"] == js["RootAction"]:

                                                for x in a:

                                                        n = ap.liststreamkeyitems('stream3',a[0])
                                                        m = n[0]

                                                        url = "http://localhost:8080/clientsend"

                                                        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"clientid\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"topic\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"message\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"QoS\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"retain\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (x,m["data"]["text"],js["Events"][x])
                                                        headers = {
                                                        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                                                        'Authorization': q["access_token"],
                                                        'cache-control': "no-cache",
                                                        }

                                                        response1 = requests.request("POST", url, data=payload, headers=headers)

                                                        print(response1.text)
                                                                                                                                                                                                                                                                                      


t1 = threading.Thread(target=srvr)
t2 = threading.Thread(target=engine)

t1.start()
t2.start()