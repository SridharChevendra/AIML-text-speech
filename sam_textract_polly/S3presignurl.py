import json
import boto3
from botocore.exceptions import ClientError
# import bitly_api

def create_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        return response                                            
        
    except ClientError as e:
        print(e)
        return None
    
    # return response
        

def lambda_handler(event, context):
    # TODO implement
    print(event)
    if 'contentOutput' in event.keys(): 
        file_name = event['contentOutput']['mp3FileName']
    elif 'Item' in event['verifyDynamoDB'].keys(): 
        file_name = event['verifyDynamoDB']['Item']['filekey']['S']
    else:
        print('unable to retrive file_name')
        pass
    
    
    object_name = "mp3Files/"+ file_name
    bucket_name = event['s3Payload']['s3Bucket']
    
    return {"s3Url":
             create_presigned_url(bucket_name,object_name)
        }
