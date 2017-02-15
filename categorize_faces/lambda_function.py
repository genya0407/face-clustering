import boto3
import networkx

dynamo = boto3.client('dynamodb')
rekog = boto3.client('rekognition')

def lambda_handler(event, context):
    res = dynamo.scan(
        Limit=1500,
        TableName="faces"
    )
    print res['Items'][0]
    """
            res = rekog.search_faces(
                CollectionId="cast_faces",
                FaceId=target_face["face_id"]["S"],
                FaceMatchThreshold=90
            )
        for face_match in res['FaceMatches']:
            dynamo.update_item(
                Key={ 
                    "face_id": {
                        "S": face_match["Face"]["FaceId"]
                    },
                },
                ExpressionAttributeNames={
                    '#T': 'tag',
                },
                ExpressionAttributeValues={
                    ':t': {
                        'N': 'tag'
                    }
                },
                TableName='faces',
                UpdateExpression="SET #T = :t"
            )
    """
