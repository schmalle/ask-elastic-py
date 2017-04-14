   
Simple example python script to show basic http requests to Elasticsearch from python
---

Setup
--

You have an index EWS2 with Alert documents and a Alert document structure like this

'''{
"_index": "ews2",
"_type": "Alert",
"_id": "58edb52cb64ad7f7491f518a",
"_version": 1,
"_score": 1,
"_source": {
"country": null,
"originalRequestString": "/cgi-bin/.br/style.css3/444",
"esid": "58edb52cb64ad7f7491f518a",
"sourceEntryAS": null,
"createTime": "20170311T081221+0000",
"peerIdent": "MSTest3",
"locationString": "null, null",
"client": "-",
"location": "41.12, -71.34",
"sourceEntryIp": "192.168.8.1",
"additionalData": "host: www.myhoneypot.de; sqliteid: 3688; ",
"peerType": null,
"targetEntryIp": "1.2.3.4"
}
}`

You can now query individual source locations and the number of occurrence by this CURL
request:

curl -XGET 'localhost:9200/ews2/Alert/_search?pretty' -H 'Content-Type: application/json' -d'
{

    "query": {
        "range" : {
            "createTime" : {
                "gte" : "now-1d/d",
                "lt" :  "now+1d/d"
            }
        }
    },
    "aggs": {
  
    "full_name": {
      "terms": {
        "field": "locationString",
        "size": 10000
      }
    }}'


{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 10,
    "successful" : 10,
    "failed" : 0
  },
  "hits" : {
    "total" : 2,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "ews2",
        "_type" : "Alert",
        "_id" : "58edb52cb64ad7f7491f5188",
        "_score" : 1.0,
        "_source" : {
          "country" : null,
          "originalRequestString" : "/cgi-bin/.br/style.css3/444",
          "esid" : "58edb52cb64ad7f7491f5188",
          "sourceEntryAS" : null,
          "createTime" : "20170411T071221+0000",
          "peerIdent" : "MSTest4",
          "locationString" : "null, null",
          "client" : "-",
          "location" : "41.12, -71.34",
          "sourceEntryIp" : "192.168.8.1",
          "additionalData" : "host: www.myhoneypot.de; sqliteid: 3688; ",
          "peerType" : null,
          "targetEntryIp" : "1.2.3.4"
        }
      },
      {
        "_index" : "ews2",
        "_type" : "Alert",
        "_id" : "58edb52cb64ad7f7491f5187",
        "_score" : 1.0,
        "_source" : {
          "country" : "DE",
          "originalRequestString" : "/cgi-bin/.br/style.css2/2",
          "esid" : "58edb52cb64ad7f7491f5187",
          "sourceEntryAS" : "AS12306",
          "createTime" : "20170411T071021+0000",
          "peerIdent" : "MSTest4",
          "locationString" : "51.0, 9.0",
          "client" : "-",
          "location" : "51.0, 9.0",
          "sourceEntryIp" : "193.99.144.95",
          "additionalData" : "host: www.myhoneypot.de; sqliteid: 3688; ",
          "peerType" : null,
          "targetEntryIp" : "46.29.100.76"
        }
      }
    ]
  },
  "aggregations" : {
    "full_name" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "51.0, 9.0",
          "doc_count" : 1
        },
        {
          "key" : "null, null",
          "doc_count" : 1
        }
      ]
    }
  }
}

Technically this is a query with an aggregation afterwards. As DTAGs Sicherheitstacho uses
internally such a format:

  [
    "2016-10",
    [
      51,9,72552,
      59.894394,30.264206,68928,
      39.928894,116.388306,49394,
      38,-97,48338,
      34.099503,-118.4143,18730,
      47.6801,-122.120605,12501,
      47,29,12254,
      37.386,-122.0838,12219,
      51.533295,0.69999695,9321,
      -31.942795,115.8439,6155
    ]
  ]
  
  the python script converts the output.
  
  Contact: markus_@_mschmall_._de