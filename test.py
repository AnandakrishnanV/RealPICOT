import logging
logging.basicConfig()
from Savoir import Savoir
rpcuser = 'multichainrpc'
rpcpasswd = 'CTYKR8VwcMD42d7xLuQe1Mt8f4DB9o8s8wVtTjeTfmKi'
rpchost = 'localhost'
rpcport = '9558'
chainname = 'chain1'

api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

b = api.liststreamkeys('stream2')
q = "key3"
f = 0
for i in range(len(b)):
	if q == b[i]["key"]:
		f = 1
if f == 0:
	y= api.getnewaddress()
	api.publish('stream2',q,{"text":y})	
