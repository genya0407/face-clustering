import boto3
import json

dynamo = boto3.client('dynamodb')

def lambda_handler(event, context):
    movie_id = event['movie_id']
    return dynamo.scan(
        ExpressionAttributeValues={
            ':movie_id': {
                'S': movie_id,
            },
        },
        FilterExpression='movie_id = :movie_id',
        TableName='faces'
    )
