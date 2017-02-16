import boto3
import community
import collections
import networkx as nx
import json
import datetime

dynamo = boto3.client('dynamodb')
rekog = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        movie_id = event['movie_id']
    except Exception as e:
        print e
        return {
            'statusCode': 422,
            'headers': {},
            'body': 'Specify "movie_id" attribute |' + str(event)
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

    dynamo.update_item(
        ExpressionAttributeNames={
            '#TIMESTAMP': 'categorize_finish_at'
        },
	ExpressionAttributeValues={
	    ':t': {
		'S': str(datetime.datetime.now()),
	    },
	},
	Key={
            'movie_id': {
                'S': movie_id
            }
	},
	TableName='movies',
	UpdateExpression='SET #TIMESTAMP = :t'
    )

    return {
        'statusCode': 200,
        'body': {
            'message': 'success'
        },
        'headers': {
            'Content-Type': 'application/json'
        }
    }
