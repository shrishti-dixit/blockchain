import requests
import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['Blockchain']
coll1= db['count']
coll2=db['blocks']
coll3=db['alteredBlocks']

coll3.delete_many({})

data=coll1.find({})
for i in data:
	count=i['count']

print("The Number of blocks present are: "+str(count))

print("Enter the Number of block u want to alter:")
alter_block=input()

if(alter_block>0 and alter_block<=count):
	data=coll2.find({"block_no":alter_block})
	print("The Previous Present Data is:")
	for i in data:
		print(i["block_content"])
        print("\n\nEnter any text to update the block:")
	str=raw_input()
	data=coll2.find({})
	for i in data:
		coll3.insert(i)
	myquery = { "block_no": alter_block }
	newvalues = { "$set": { "block_content": str } }
	coll3.update_one(myquery, newvalues)




