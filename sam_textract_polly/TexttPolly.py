import json
import boto3
import os

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    # TODO implement
    print (event)
    bucketName = event['bucketName']
    objectKey = event['fileName']
    lambdaObjectKey = "/tmp/" + objectKey.split('/')[1]

    # Download S3 file to lambda /tmp 
    s3.meta.client.download_file( bucketName, objectKey, Filename = lambdaObjectKey ) 
    
    with open(lambdaObjectKey, 'r') as f:
        textData = f.read()
        response = convertTextToVoice(bucketName, textData)
   

    return {"mp3FileName": response['SynthesisTask']['OutputUri'].split('/')[-1],
                "status": response['SynthesisTask']['TaskStatus'],
                "jobId": response['SynthesisTask']['TaskId'],
                "bucketName": bucketName}            


def convertTextToVoice(bucketName, textData):
    client = boto3.client('polly')
    response = client.start_speech_synthesis_task(Engine='neural', LexiconNames=[], OutputFormat='mp3', 
                                                    OutputS3BucketName=bucketName, OutputS3KeyPrefix='mp3Files/', 
                                                    Text=textData, TextType='text', VoiceId='Matthew')
            
                
    return response