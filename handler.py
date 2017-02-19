# -*- coding: utf-8 -*-
# !/usr/bin/python

import json
import logging

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor')

import line.line as line

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def lambda_handler(event, context):
    print(json.dumps(event, indent=4, separators=(',', ': ')))
    content = event.get("result")[0].get("content") # 本当は複数resultきます。lambdaならとりあえずマルチスレッドで。（SQSに入れてもいいけど）
    line.set_return_text(content)
    line.send_to_line(content)


