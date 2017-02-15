import boto3
import community
import collections
import networkx as nx
import json

dynamo = boto3.client('dynamodb')
rekog = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        movie_id = json.loads(event['body'])['movie_id']
    except Exception as e:
        print e
        return {
            'statusCode': 422,
            'headers': {},
            'body': 'Specify "movie_id" attribute.'
        }

    res = dynamo.scan(
        Limit=10000,
        TableName="faces",
        ExpressionAttributeValues={
            ':movie_id': {
                'S': movie_id,
            },
        },
        FilterExpression='movie_id = :movie_id',
    )
    
    G = nx.Graph()
    
    for item in res["Items"]:
        G.add_node(item['face_id']["S"])
        res = rekog.search_faces(
            CollectionId=movie_id,
            FaceId=item["face_id"]["S"],
            FaceMatchThreshold=80,
            MaxFaces=500
        )
        G.add_nodes_from(map(lambda x: x['Face']['FaceId'], res['FaceMatches']))
        for pair in res['FaceMatches']:
            G.add_edge(pair['Face']['FaceId'], item['face_id']['S'])
    
    partition = community.best_partition(G)
    
    for face_id, tag in partition.items():
        dynamo.update_item(
            Key={
                "face_id": {
                    "S": face_id
                }
            },
            ExpressionAttributeNames={
                '#T': 'tag',
            },
            ExpressionAttributeValues={
                ':t': {
                    'S': str(tag)
                }
            },
            TableName='faces',
            UpdateExpression="SET #T = :t"
        )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'success'
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
