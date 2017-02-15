import os
import boto3
import glob
import re

s3 = boto3.client('s3')
rekog = boto3.client('rekognition')
dynamo = boto3.client('dynamodb')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        etag = record['s3']['object']['eTag']
        movie_file = '/tmp/movie.mp4'

        s3.download_file(bucket, key, movie_file)
        os.system(r'./ffmpeg.linux64 -i /tmp/movie.mp4 -r 1 -f image2 /tmp/frame%d.jpg > /dev/null 2>&1')
        try:
            rekog.create_collection(CollectionId=etag)
        except Exception as e:
            rekog.delete_collection(CollectionId=etag)
            rekog.create_collection(CollectionId=etag)
            dynamo.delete_item(
                Key={
                    'movie_id': {
                        'S': etag
                    }
                },
                TableName='faces'
            )
        jpegs = glob.glob('/tmp/*.jpg')
        for jpeg in jpegs:
            time = re.search(r'/tmp/frame(\d+).jpg', jpeg).group(1)
            with open(jpeg, 'rb') as f:
                face_records = rekog.index_faces(
                    CollectionId=etag,
                    Image={
                        'Bytes': f.read()
                    },
                    ExternalImageId=etag
                )['FaceRecords']
                for face_record in face_records:
                    dynamo.put_item(
                        TableName='faces',
                        Item={
                            'face_id': {
                                'S': face_record['Face']['FaceId']
                            },
                            'time': {
                                'N': time
                            },
                            'movie_id': {
                                'S': etag
                            }
                        }
                    )
