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

url = create_node_url

def label_node(node_self, label):
    print("put label:"+label+" in "+node_self)
    label_url = node_self+"/labels"
    label_data = "\""+label+"\""
    label_data_text = json.dumps(label_data)
    resp, content = httpclient.request(label_url,"POST",body=label_data_text, headers=headers)
    print(content)

def create_node(topic):
    node_data= {'topic':topic}
    node_data_text = json.dumps(node_data)
    resp, new_content = httpclient.request(create_node_url,"POST",body=node_data_text, headers=headers)
    return eval(new_content)['self']
    #return new_content

if len(sys.argv) <2 :
    print("usage: python3 create_node.py <topic A>")
    exit(0)

n = create_node(sys.argv[1])
label_node(n,"key_topic")


