import requests
import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['Blockchain']
coll = db['filterdata']
coll2 = db['output']
coll3= db['count']
coll4=db['blocks']
coll5=db['hashKeys']



data = coll.find({})
count_block_data=coll3.find({})

for i in count_block_data:
    count=i['count']
count=int(count)
print(count)

count_blocks=count

coll3.delete_many({})

data = coll.find({})

stations = []

reasons = []

for i in data:
    stations.append(i['station'])
    reasons.append(i['reason'])

import csv

blocknumber = 0
main_str=""
for i in range(0, len(stations)):

    with open('../data/tfl-bus-stops.csv') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')

        str1 = ""

        # print stations[i]

        for row in reader:

            # naive bayes classification

            if (stations[i].upper() in row[3]):

                # print row[3]

                str3 = "POSSIBLE DELAY IN ARRIVAL OF SOME BUSES." + " STATION :" + stations[i]

                str2 = ".\n REASON:" + reasons[i]
                ##check region code
                with open('../data/Reasons.csv') as fd:
                    readerC = csv.reader(fd)
                    for rowC in readerC:
                        if (str2.lower().find( str(rowC[1]).lower()) > -1):
                            str2 = str2 + ".\n REASON TYPE:" + rowC[2] + ".\n The affected Buses Details are:"
                            break



                str1 = str3 + str2

                naptan = row[2]

                url = "https://api.tfl.gov.uk/StopPoint/" + "%s" % naptan + "/arrivals"

                req = requests.get(url)

                data = json.loads(req.text)

                count = 0

                for j in data:

                    count += 1

                    if (j[u'direction'].encode('ascii', 'ignore') == "inbound"):
                        str1 += "\n" + str(count) + ".FROM: " + j[u'destinationName'].encode('ascii',
                                                                                             'ignore') + ". TO:" + j[
                                    u'stationName'].encode('ascii', 'ignore') + ". VEHICLE NO:" + j[
                                    u'vehicleId'].encode('ascii', 'ignore') + "." + ".EXPECTED ARRIVAL :" + j[
                                    u'expectedArrival'].encode('ascii', 'ignore')

                    if (j[u'direction'].encode('ascii', 'ignore') == "outbound"):
                        str1 += "\n" + str(count) + ".FROM: " + j[u'stationName'].encode('ascii', 'ignore') + ". TO:" + \
                                j[u'destinationName'].encode('ascii', 'ignore') + ". VEHICLE NO:" + j[
                                    u'vehicleId'].encode('ascii', 'ignore') + "." + ".EXPECTED ARRIVAL :" + j[
                                    u'expectedArrival'].encode('ascii', 'ignore')
                main_str+=str1

                

                break

#print(main_str)
coll4.insert({"block_no":count_blocks+1,"block_content":main_str})
coll3.insert({"count":count_blocks+1})
import hashlib
result = hashlib.sha256(main_str)
print("Current Hash key:")
h_key=str(result.hexdigest()) 
print(h_key)

data=coll5.find({"key_id":count_blocks})
print("Previous Block key:")
for i in data:
    p_key=i["key"]
print(p_key)
print("Current Block's key:")
new_str=h_key+p_key
#print(new_str)
result = hashlib.sha256(new_str)
block_key=result.hexdigest()
print(block_key)
coll5.insert({"key_id":count_blocks+1,"key":block_key})



