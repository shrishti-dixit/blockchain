import requests

import json
import csv


def makename2(str1, str2, str3):
    str4 = ""
    if (str1[0] == '['):
        str4 = str2 + " " + str3
    return str4
    str4 = str1 + " " + str2 + " " + str3
    return str4


def makename1(str1, str2):
    return str1 + " " + str2


from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['Blockchain']

coll = db['rawdata']

coll2 = db['filterdata']

coll2.delete_many({})

data = coll.find({})

dict = {}

for i in data:
    # print i
    if (i['statusSeverity'] == "Closure"):
        dn = i['displayName']
        url1 = "https://api.tfl.gov.uk/road/" + "%s" % dn + "/disruption"
        req1 = requests.get(url1)
        data1 = json.loads(req1.text)
        # print data1
        for j in data1:
            name = ""
            if (type(dict) == type(j)):
                # print "in loop"
                str1 = str(j[u'comments'].encode('ascii', 'ignore'))
                print(str1)

                list_try = str1.split(" ")
                for k in range(0, len(list_try)):
                    if (list_try[k] == "Road" or list_try[k] == "Street"):
                        try:
                            name = makename2(list_try[k - 2], list_try[k - 1], list_try[k])
                        except IndexError:
                            name = makename1(list_try[k - 1], list_try[k])
                        break  # print name
            if (len(name) >= 4):
                coll2.insert({'station': name, 'reason': str1})
                print("record added")
