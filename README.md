# smc

License: dougchen@talent-service.com

## Social Media Chain
 A Data pipe from source to any possibile destination

## POC
### Environment setting
* ubuntu 14.04 LTS
* couchbase
* neo4j
* python3
* java8
* git

###  grep keywords from fb 
* 1. to couchbase (fbgrep.py)
* 2. to elasticsearch (fbgrep_es.py)
* 3. add sentiment (simple weight for positive or negitave)
      
### from nosql to machine learnning streamming (TODO)
### from nosql to graphic 
* 1. neo4j
* 2. Kibana (TODO)

### Usage
* Prepare
** Launch elasticsearch, couchbase, neo4j...
   Assume all these service are in the same machine

* Gather things from FB
** #python fbgrep_es.py <topic> 
   Grep things of <topic> from facebook and insert into elasticsearch.
   It includes user public profile, facebook post and comments.

** #python python fbgrep.py <topic>
   Grep thing of <topic> from facebook and insert to couchbase

** Create topic in neo4j: every topic gathered need to have a "topic" node in
   neo4j. 
   Use this simple script to create topic node
   #python creat_node.py <topic>
   
** Create link and graphic in neo4j from couchbase resources
   #python build_graphic.py <topic_A> <topic_B>
   This will build link between two topics, via post/message/fbusers
   For example
   #python build_graphic.py brexit bigdata 
   This will search any commments source from brexit and finally ends in bigdata





   
