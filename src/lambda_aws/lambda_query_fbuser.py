#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
import json
import requests


def lambda_handler(even, context):
    app_id = even['app_id']
    client_secret = even['client_secret']
    user_id = even['user_id']
    r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+app_id+'&client_secret='+client_secret)
    access_token = r.text.split('=')[1]

    params = {}
    params['access_token'] = access_token
    params['fields'] = 'id,about,bio,name,link,email,cover,hometown,location'
    r = requests.get('https://graph.facebook.com/v2.6/'+user_id,params=params)
    return json.loads(r.text)


if __name__ == '__main__':
    import sys

    # To try from command line
    s = open('../secret.so')
    client_secret= s.readline().strip()
    s.close()

    grepValue = sys.argv[1]

    params ={}
    params['client_secret'] = client_secret
    app_id = '1091008854278872'
    params['app_id'] =  app_id
#    app_id = '397433603789585'

    params['user_id'] = sys.argv[1]
    print(lambda_handler(params, None))

    
