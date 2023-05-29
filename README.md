# AIML-text-speech
Use AWS AI/ML and serverless services to build text to speech
## Overview
This solution enables users to upload .pdf files and provides .mp3 files with a pre-signed url.The following uses AWS SAM(Serverless Application Model) to deploy the resources.

Solution outlined here uses the following AWS services.
* AWS Lambda - Compute Engine to kickoff the respective AIML and orchestration Service
* S3 Bucket - User uploads the files into `PdfFiles` and generates artifacts `mp3files`
* DynamoDB - Database to track meta data, manage duplicate uploads
* SQS - Captures the uploads as messages for downstream processing
* Textract - Extract the Text from .pdf files
* Polly - Converts the Text to Speech
* StepFunctions - Orchestrates the workflow 
* AWS Cloudformation - When SAM deployed, it deployes the resources using AWS cloudformation
* 
#### High Level Architecture
![AIML_Text_Speech](https://github.com/SridharChevendra/AIML-text-speech/assets/32348488/c849554b-7e0a-4852-aae3-74e7bdcf4ce0)

## Getting Started
### Pre-requisites
* AWS Account
* AWS Cloud9 IDE
Note: If using non-cloud9 IDE, follow the steps to install AWS SAM(Serverless Application Model)
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

#### Build Steps
#### 1. Clone GitRepo
Open the new Terminal with in the Cloud9 IDE environment.

Create and Change to folder named "AIML"
```
mkdir AIML && cd AIML
```
Clone the GitRepo to your local machine.
```
git clone https://github.com/SridharChevendra/AIML-text-speech.git
cd AIML-text-speech
```

#### 2. Prepare SAM Locally
With 'sam build', sam creates environment and dependencies in .aws-sam folder.  
Note: re-run 'sam build' command for any updates to the code or template.yaml
```
# SAM template envrionment is set to Python 3.8. To ensure the code and dependecies are prepared for python3.8 use the parameter --use-container
sam build --use-container
```
#### 3. Deploy Cloud Resources
Once the sam build completed successfully, it creates a folder locally .aws-sam with all the code and depdencies defined in requirements.txt
```
sam deploy --guided
```
with the sam deploy,provide the following details
* applciation name
* AWS S3 bucket name(This is a unique name across AWS)
Then use all the defaults. Once completed, it will generate a file 'samconfig.toml' locally that captures all the response.

AWS Cloudformation creates a changeset and then the resources.

#### 4.Test
Go to S3 bucket you created part of Step 3, and create a folder with in the S3 bucket "pdfFiles".

Upload a .pdf file using GUI or CLI.

Go to AWS Step functions to see the workflow. Once completed, on the S3url step, grab the pre-signedurl to play in your browser.





