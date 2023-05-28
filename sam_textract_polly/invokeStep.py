import json
import boto3
from botocore.exceptions import ClientError
import os

client = boto3.client('stepfunctions')
#stateMachineArn = 'arn:aws:states:us-east-1:581411711467:stateMachine:MyStateMachine_polly'
stateMachineArn = os.environ['StepFunction']
Table = os.environ['Table']

def lambda_handler(event,context):
    
    # update the records in dynamodb for monitoring - if not exists
    s3_event = json.loads(event['Records'][0]['body'])
    eTag = s3_event['Records'][0]['s3']['object']['eTag']
    fileName = s3_event['Records'][0]['s3']['object']['key'].split('/')[1]    

    response1 = captureFileInfo(eTag, fileName)
    print(response1)
    
    try:
        response = client.start_execution(
            stateMachineArn = stateMachineArn,
            input = json.dumps(s3_event)
            )
        print(response)
        print(response.get('output'))
    except ClientError as e:
        print(e)
    
    
def captureFileInfo(eTag, inputFileName):
    try:
        client = boto3.client('dynamodb')
        response = client.update_item(
            TableName=Table,
            Key = {
                'etag': {
                    'S': eTag
                  }
                },
                UpdateExpression= "SET fileName = :fileName, Cached = :Cached, FailedAttempts = :FailedAttempts",
                ExpressionAttributeValues= {
                    ":fileName" : {
                        'S': inputFileName
                        },
                    ":Cached" : {
                        'N' : '0'
                    },
                    ":FailedAttempts" : {
                        'N' : '0'
                    }
                },
                ConditionExpression = ( 'attribute_not_exists(Cached)' ),
                ReturnValues="UPDATED_NEW"
            )
        return response    
    except ClientError as e:
        print(e)