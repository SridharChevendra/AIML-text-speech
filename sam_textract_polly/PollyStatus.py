import json
import boto3

def lambda_handler(event, context):
    jobId = event['jobId']
    return isJobComplete(jobId)


def isJobComplete(jobId):
    client = boto3.client('polly')
    response = client.get_speech_synthesis_task(
    TaskId=jobId
    )
    return {
        "jobStatus": response['SynthesisTask']['TaskStatus']
    }
