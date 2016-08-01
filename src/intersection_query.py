#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import os
from couchbase import Couchbase
from couchbase.views.iterator import View
from couchbase.n1ql import N1QLQuery
import sys

if len(sys.argv) <3 :
    print("usage: python3 intersection_query.py <topic A> <topic B> ")
    exit(0)

topicA = sys.argv[1]
topicB = sys.argv[2]
couchbase_host='10.1.192.79'
couchbase_bucket='fbsmc'

couchbucket = Couchbase.connect(bucket=couchbase_bucket, host=couchbase_host)

#print(couchbucket)

#couchbucket.n1ql_query('CREATE PRIMARY INDEX ON fbsmc').execute()
#q = N1QLQuery('SELECT topic, id FROM fbsmc ')
#for row in couchbucket.n1ql_query(q):
#    #print(row)  # {'age': .., 'lname': ..., 'fname': ...}
#    if len(set(row['topic'])) > 1:
#        print(row['topic'])
#        print(row)

def findConnection(ta,tb):
    q = N1QLQuery('SELECT id, message,topic FROM fbsmc where topic="'+ta+'" ')
    result = []
    for row in couchbucket.n1ql_query(q):
        if 'message' in row:
            msg = row['message']
            if msg.lower().count(tb) >0:
                print(row['id'])
                result.append(row['id'])
          #  print(row['message']) 
    return result

print(findConnection(topicA, topicB))

