import json
import boto3

def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract', region_name='us-east-1')
    response = client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
     }
    )
    return response

def lambda_handler(event, context):
    print(event)
    # TODO implement
    s3BucketName = event["Records"]["s3Bucket"]
    objectName = event["Records"]["s3Object"]
    
    #print(s3BucketName, objectName)
    
    response = startJob(s3BucketName, objectName)
    
    return {
        "jobId": response["JobId"],
        "fileName": objectName.split('/')[1]
        }
