# coding: utf-8

import boto3
import json

dynamo = boto3.client('dynamodb')

def as_json(response):
    retval = []
    for item in response['Items']:
        retval.append(
            {
                'movie_id': item['movie_id']['S'],
                'object_key': item['object_key']['S'],
                'capture_finish_at': item.get('capture_finish_at', { 'S': None })['S'], # item['capture_finish_at']が存在しない時にNoneになるように
                'categorize_finish_at': item.get('categorize_finish_at', { 'S': None })['S']
            }
        )
    return retval

def lambda_handler(event, context):
    res = dynamo.scan(
        TableName='movies'
    )

    return {
        'body': as_json(res),
        'statusCode': 200,
        'headers': {}
    }
