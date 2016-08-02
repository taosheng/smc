from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'joe',
    'id': '7777777',
    'text': 'lalal',
    'timestamp': datetime.now(),
}
res = es.create(index="test-index", doc_type='fb',  body=doc)
print(res['created'])

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

q = {
  "query": { 
    "bool": { 
      "must": [
        { "match": { "id": "1234566"        }}
      ]
    }
  }
}

#res = es.search(index="test-index", body={"query": {"match_all": {}}})
res = es.search(index="test-index", body=q)
print("Got %d Hits:" % res['hits']['total'])
print(res['hits']['hits'])
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(id)s: %(text)s" % hit["_source"])
