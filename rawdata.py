import requests 

import json 

url="https://api.tfl.gov.uk/road" 

req = requests.get(url) 

data = json.loads(req.text) 

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['Blockchain']

coll = db['rawdata']

coll.delete_many({})

for i in data:
	#print(i['displayName'])
    coll.insert({'displayName':i['displayName'],'statusSeverity':i['statusSeverity']})



