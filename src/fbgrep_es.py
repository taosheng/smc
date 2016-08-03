#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from elasticsearch import Elasticsearch
import json
import requests
import random
import sys
import time

es = Elasticsearch()
access_token = ''


def hasUser(cuser,indexTopic):
    q = { "query": { "bool": { "must": [ { "match": { "id": cuser }} ] } } }
    res = es.search(index=indexTopic, body=q )
    hits = res['hits']['total']
    if hits <=0:
        return False
    else:
        return True

def getResponse(path, params={}):
    params['access_token'] = access_token
    r = requests.get('https://graph.facebook.com/v2.6/'+path,params=params)
    return json.loads(r.text)

def grepUser(cuser,topic,params={}):
    indexTopic = "topic-"+topic
    params['access_token'] = access_token
    oneUser = getResponse('/'+cuser, params)
    if hasUser(cuser, indexTopic):
        q = { "query": { "bool": { "must": [ { "match": { "id": cuser }} ] } } }
        res = es.search(index=indexTopic, body=q )
        u = res['hits']['hits'][0]['_source']
        print(u)
    else:
        res = es.create(index=indexTopic, doc_type='fbuser',  body=oneUser)
        es.indices.refresh(index=indexTopic)



def grepPost(cpost,topic,params={}):
    params['access_token'] = access_token
    onePost = getResponse('/'+cpost, params)
    onePost['topic'] = topic
    indexTopic = "topic-"+topic
    res = es.create(index=indexTopic, doc_type='fbmsg',  body=onePost)
    es.indices.refresh(index=indexTopic)
    return onePost

if __name__ == '__main__':

    s = open('secret.so')
    client_secret= s.readline().strip()
    s.close()

    grepValue = sys.argv[1]

    app_id = '1091008854278872'
#    app_id = '397433603789585'

    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+app_id+'&client_secret='+client_secret)
    print(r.text)
    access_token = r.text.split('=')[1]
    print(access_token)
    params_user={'fields':'id,about,bio,name,link'}
    print("====== handle all user =======")
    
    #user_token = 'EAAPgREs0wtgBAJ2MmLu4RvfnZBsKZAhyZB1yjUgtkDJcNuZBGzXHdwcWn7HgbtZBPfW9ES9zcWVFLOWKCxZAhyqhs1skclGpWyLRMvpZCjxE9MEjZAjPDDDZAPZAhlFp2wMTRH8rFwxNPAF6mNR5THhveLRlzoKPIw2KZAFMfCaiUJ2jUi7CD9VXRHR'
    r = getResponse('search',params={'access_token':access_token,'q':grepValue, 'type':'page'})
    handle_user_list=[]
    for item in r['data']:
        print(item)
        page_id = item['id']
        pager = getResponse("/"+page_id+"/posts")
#        print(pager)
        for post in pager['data']:
            time.sleep(random.randint(1, 3))
            print(post['id']) 
            params={'fields':'id,from,message'}
            #postDetail = getResponse('/'+post['id'],params)
            postDetail = grepPost(post['id'], grepValue, params )
            if ('message' in postDetail) and (len(postDetail['message']) <= 30) :
                print(postDetail)
            else:
                print("[skip print].."+ str(postDetail['from']))
            cuser = postDetail['from']['id']
            if handle_user_list.count(cuser) == 0:
                handle_user_list.append(cuser)
                grepUser(cuser,grepValue,params_user)
          #      getTagFriend(cuser)

            comments = getResponse('/'+post['id']+"/comments",params)
            print('------comments start---')
            for comment in comments['data']:
                cuser = comment['from']['id']
                postDetail = grepPost(comment['id'], grepValue, params )
                print("grep comment ...done")
                if handle_user_list.count(cuser) == 0:
                    handle_user_list.append(cuser)
                    grepUser(cuser,grepValue, params_user)
            #         
            #print('------comments end---')
 

#    print(handle_user_list)
#    for u in handle_user_list:
#        grepUser(u,grepValue,params_user)
       



