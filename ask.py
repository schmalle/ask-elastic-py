import requests
import os.path
import configparser
import base64
import datetime
import time

#
# variable area
#
index = "ews2"
document = "Alert"
host = "http://localhost:9200/"
server = host + index + "/" + document + "/_search?pretty"

#
#
#


#
# helper classes
#

class Location(object):
    def __init__(self, **kwargs):
        for keyword in ["key", "doc_count"]:
            setattr(self, keyword, kwargs[keyword])
        self.code = 0
        self.coordinates = []
        self.population = 0

    def __str__(self):
        fields = ['  {}={!r}'.format(k,v)
                    for k, v in self.__dict__.items() if not k.startswith("_")]
        return "{}(\n{})".format(self.__class__.__name__, '\n'.join(fields))


#
# functiom area
#

#
# return mm
#
def getCurrentMonth():
    localtime = time.localtime(time.time())
    month = str(localtime.tm_mon)
    if (len(month) == 1):
        month = "0" + month

    return month

#
# return yyyy
#
def getCurrentYear():
    localtime = time.localtime(time.time())
    return str(localtime.tm_year)



def generateQueryData(host, index):
    query = "{ \"query\": { \"range\" : { \"createTime\" : { \"gte\" : \"20170401T00001+0000\", \"lt\" : \"now+1d/d\" } } }, \"aggs\": { \"full_name\": { \"terms\": { \"field\": \"locationString\", \"size\": 10000 } } } }"
    return query

#
# startup block
#

headers = {'Content-Type': 'application/json'}

r = requests.post(server, data=generateQueryData(host, index), headers=headers, verify=False)


jsonData = r.json()
locations = jsonData['aggregations']['full_name']['buckets']
print (locations)

json_obj = jsonData['aggregations']['full_name']
#print (json_obj)

buckets = [Location(**metro_info) for metro_info in json_obj["buckets"]]


output = "["
output+= "\""+getCurrentYear()+"-"+getCurrentMonth()+",["

for location in buckets:
    output += location.key + "," + str(location.doc_count) + ","

output+="]]"


print (output)