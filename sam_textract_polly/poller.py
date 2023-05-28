import json
import boto3
import botocore
import os
import urllib.parse

client = boto3.client('stepfunctions')

# activityWorker = "arn:aws:states:us-east-1:581411711467:activity:ManualApproval"
activityWorker = os.environ["ActivityArn"]
url = os.environ['APIUrlEndpoint']

def lambda_handler(event, context):
    try:
        response = client.get_activity_task(
            activityArn= activityWorker
            )
        print (response)
        
        if response:
            urls = generate_links(response['taskToken'])
            print(urls)
            resp_email = emailNotification(urls['Approve_url'], urls['Reject_url'])
            
            print(resp_email)
            
    except botocore.exceptions.ClientError as error:
        raise error
    
    # print(url)
    
    #print(response)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def generate_links(token):
    token = urllib.parse.quote(token)
    return {
        "Approve_url": url + "/succeed" + "?taskToken=" + token,
        "Reject_url": url + "/fail" + "?taskToken=" + token
        }
        
def emailNotification(Approve_url, Reject_url):
    client = boto3.client('ses')
    response = client.send_email(
        Source='sricheve@amazon.com',
        Destination={
            'ToAddresses': ['chevendra@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': 'Approval email for processing'
                    },
                    'Body': {
                        'Html': {
                            'Data': 
                            '''
                            <!DOCTYPE html>
                            <html>
                            <body>
                            <p><a href={0}>Approve!</a></p>
                            </br>
                            <p><a href={1}>Reject!</a></p>
                            </body>
                            </html>
                             '''.format(Approve_url, Reject_url)
                            }
                        }
                    }
                )
    return response
    