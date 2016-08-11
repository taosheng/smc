#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
from simple_sentiment import Sentiment
import json

def lambda_handler(even, context):
    m = even['msg']
    s = Sentiment("subjclueslen1-HLTEMNLP05.tff")
    r = s.weight_by_string(m)

    return r


if __name__ == '__main__':
    params = {'msg':"I really hate you, happiness is the enemy"}
    print(lambda_handler(params, None))

    
