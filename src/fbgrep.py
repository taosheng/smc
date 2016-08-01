#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import random
import sys
import time

from couchbase.bucket import Bucket
bucket = Bucket('couchbase://localhost/fbsmc')

 
access_token = ''


def getResponse(path, params={}):
    params['access_token'] = access_token
    r = requests.get('https://graph.facebook.com/v2.6/'+path,params=params)
    return json.loads(r.text)

def grepUser(cuser,topic,params={}):
    params['access_token'] = access_token
    oneUser = getResponse('/'+cuser, params)
    print(oneUser)
    user = bucket.get(oneUser['id'],quiet=True)
    print(user)
    if user.value != None:
        if 'topic' in user.value:
            user.value['topic'].append(topic)
        else:
            user.value['topic'] = [topic]
        bucket.upsert(user.value['id'],user.value)
    else:
        oneUser['topic'] = [topic]
        bucket.upsert(oneUser['id'],oneUser)


def grepPost(cuser,params={}):
    params['access_token'] = access_token
    oneUser = getResponse('/'+cuser, params)
    print(oneUser)
    bucket.upsert(oneUser['id'],oneUser)

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
            postDetail = getResponse('/'+post['id'],params)
            if ('message' in postDetail) and (len(postDetail['message']) <= 30) :
                print(postDetail)
            else:
                print("message is too long [skip print].."+ str(postDetail['from']))
            cuser = postDetail['from']['id']
            if handle_user_list.count(cuser) == 0:
                handle_user_list.append(cuser)
                grepUser(cuser,grepValue,params_user)
          #      getTagFriend(cuser)

            comments = getResponse('/'+post['id']+"/comments",params)
            print('------comments start---')
            for comment in comments['data']:
                cuser = comment['from']['id']
                if handle_user_list.count(cuser) == 0:
                    handle_user_list.append(cuser)
            #     #   getTagFriend(cuser)
            #         
            #print('------comments end---')
 

    print(handle_user_list)
    for u in handle_user_list:
        grepUser(u,grepValue,params_user)
       



