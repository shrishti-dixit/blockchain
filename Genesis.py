import requests
import json
import hashlib
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['Blockchain']
coll = db['hashKeys']

flag=0

data = coll.find({})

for i in data:
	flag+=1

if(flag==0):
	str = "PROUD TO BE INDIAN"
	result = hashlib.sha256(str)
	coll.insert({"key_id":0,"key":result.hexdigest()})
	print("first Key Inserted")
else:
	print("first Key already present ")