import json
import boto3
import os

# bucketName = 'sc-textract3'

def lambda_handler(event, context):
    # TODO implement
    print (event)
    jobId = event["jobId"]
    fileName = event["fileName"]
    mp3FileName = fileName.split('.')[0]+".mp3"
    txtFileName = '/tmp/' + fileName.split('.')[0]+".txt"
    bucketName = os.environ['BucketName']
    response = getJobResults(jobId)
    
    # Download text from the textract job id
    with open(txtFileName, 'w') as f:
        for resultPage in response:
            for item in resultPage["Blocks"]:
                if item["BlockType"] == "LINE":
                    f.write(item['Text'])

    
    with open(txtFileName, 'r') as f:
        textData = f.read()
        print(bucketName)
        response = convertTextToVoice(bucketName, textData)
        return {"mp3FileName": response['SynthesisTask']['OutputUri'].split('/')[-1],
                "status": response['SynthesisTask']['TaskStatus'],
                "jobId": response['SynthesisTask']['TaskId'],
                "bucketName": bucketName}
        


def getJobResults(jobId):

    pages = []

    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)

    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages
    
def convertTextToVoice(bucketName, textData):
    client = boto3.client('polly')
    response = client.start_speech_synthesis_task(Engine='neural', LexiconNames=[], OutputFormat='mp3', 
                                                    OutputS3BucketName=bucketName, OutputS3KeyPrefix='mp3Files/', 
                                                    Text=textData, TextType='text', VoiceId='Matthew')
            
                
    return response
    