import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    jobStatus = "IN_PROGRESS"
    jobId = event['jobId']
    fileName = event['fileName']
    if (isJobComplete(jobId) == "SUCCEEDED"): jobStatus = "SUCCEEDED"
    
    return {"jobId": jobId,
        "fileName": fileName,
        "jobStatus": jobStatus}
    

def isJobComplete(jobId):
    # For production use cases, use SNS based notification 
    # Details at: https://docs.aws.amazon.com/textract/latest/dg/api-async.html
    # time.sleep(5)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    '''
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    '''    

    return status