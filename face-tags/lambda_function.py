import boto3
import json

dynamo = boto3.client('dynamodb')

def lambda_handler(event, context):
    movie_id = event['movie_id']
    res = dynamo.scan(
        ExpressionAttributeValues={
            ':movie_id': {
                'S': movie_id,
            },
        },
        FilterExpression='movie_id = :movie_id',
        TableName='faces'
    )

    max_time = max(map(lambda item: int(item['time']['N']), res['Items']))

    time_to_faces = {}
    for t in range(1, max_time+1):
        index = str(t)
        time_to_faces[index] = []
        for item in res['Items']:
            if item['time']['N'] == index:
                time_to_faces[index].append(int(item['tag']['S']))

    return {
        'statusCode': 200,
        'headers': {},
        'body': time_to_faces
    }
