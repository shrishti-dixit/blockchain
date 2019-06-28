import requests
import json
import hashlib
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['Blockchain']
coll1= db['count']
coll2=db['alteredBlocks']
coll3=db['hashKeys']

data=coll1.find({})
for i in data:
	count=i["count"]

flag=0

curr_count=0

for i in range(count):
	data=coll3.find({"key_id":i})
	for j in data:
		p_key=str(j["key"])
	data=coll2.find({"block_no":i+1})
	for j in data:
		c_data=str(j["block_content"])
	result = hashlib.sha256(c_data)
	c_hashKey=str(result.hexdigest())
	main_str=c_hashKey+p_key
	result = hashlib.sha256(main_str)
	c_key=str(result.hexdigest())
	data=coll3.find({"key_id":i+1})
	for j in data:
		KEY=str(j["key"])
	print("For BLOCK: "+str(i+1))
	print("calculated Key:")
	print(c_key)
	print("Expected Key:")
	print(KEY)
	print("MATCH:")
	if(c_key==KEY):
		print(c_key==KEY)
	else:
		print(c_key==KEY)
		print("Block "+str(i+1)+" is altered")


	


