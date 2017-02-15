import boto3
import json

dynamo = boto3.client('dynamodb')

def lambda_handler(event, context):
    params = json.loads(event['body'])
    return dynamo.scan(
        FilterExpression=boto3.Attr('movie_id').eq(params['movie_id']),
        TableName='faces'
    )
