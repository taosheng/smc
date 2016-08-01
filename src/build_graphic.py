#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback
import httplib2
import json
import hashlib
import sys
from couchbase import Couchbase
from couchbase.views.iterator import View
from couchbase.n1ql import N1QLQuery

httpclient = httplib2.Http()


headers = {"Content-type": "application/json", "Accept": "application/json; charset=UTF-8","Authorization":"bmVvNGo6ZG91ZzAwMDAwMA=="}
neo_host = "http://10.1.192.79:7474/"
#neo4j_host='http://10.1.192.79:7474/db/data/node/'
create_node_url = neo_host + "db/data/node"
cypher_query_url= neo_host + "db/data/cypher"
cypher_url= cypher_query_url

#topic_nodes=['brexit','bigdata','startup']
couchbase_host='10.1.192.79'
couchbase_bucket='fbsmc'

couchbucket = Couchbase.connect(bucket=couchbase_bucket, host=couchbase_host)

def createMsgNode(msg):
    node_data= msg
    node_data_text = json.dumps(node_data)
    resp, new_content = httpclient.request(create_node_url,"POST",body=node_data_text, headers=headers)
    return eval(new_content)['self']


def label_node(node_self, label):
    print("put label:"+label+" in "+node_self)
    label_url = node_self+"/labels"
    label_data = "\""+label+"\""
    label_data_text = json.dumps(label_data)
    resp, content = httpclient.request(label_url,"POST",body=label_data_text, headers=headers)


def getRelation(t):
    q = N1QLQuery('SELECT id, message,topic FROM fbsmc where topic="'+t+'" ')
    ta_node_query = "Match(node) where node.topic = '"+t+"' return node; "
    cypher_query = { "query" : ta_node_query, "params" : {} }
    cypher_query_text = json.dumps(cypher_query)
    resp, content = httpclient.request(cypher_url,"POST",body=cypher_query_text, headers=headers)
    return_nodes = eval(content)
    ta_relation = return_nodes['data'][0][0]['self']
    return ta_relation


def create_relation(fromnode, tonode, relation):
    print("from:"+fromnode)
    print(tonode)
    print(relation)
    fromnode = fromnode + "/relationships"
    requestdata = { "to" : tonode, "type" : relation }
    build_relation_query = json.dumps(requestdata)
    resp, content = httpclient.request(fromnode,"POST",body=build_relation_query, headers=headers)
    print(content)


def BuildConnection(ta,tb):
#    if len(return_nodes['topic']) != 0:
#        print(return_nodes)
    ta_node = getRelation(ta)
    tb_node = getRelation(tb)

    q = N1QLQuery('SELECT id, message,topic FROM fbsmc where topic="'+ta+'" ')

    result = []
    for row in couchbucket.n1ql_query(q):
        if 'message' in row:
            msg = row['message']
            if msg.lower().count(tb) >0:
                print(row['id'])
                msg_node = createMsgNode(row)
                label_node(msg_node,"facebook_msg")
                create_relation(ta_node,msg_node,"message_to")
                create_relation(msg_node,tb_node,"message_from")
                result.append(row['id'])
          #  print(row['message']) 
    return result


if len(sys.argv) <3 :
    print("usage: python3 intersection_query.py <topic A> <topic B> ")
    exit(0)

topicA = sys.argv[1]
topicB = sys.argv[2]
print(BuildConnection(topicA, topicB))

