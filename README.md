Secure Serverless File Gateway (AWS Lab 4)
Project Overview
This project implements a secure, serverless "File Gateway" using AWS SAM (Serverless Application Model). It allows users to upload and download files to a Private S3 Bucket via time-limited, cryptographically signed URLs.

The architecture maintains 100% bucket privacy while offloading heavy data transfers directly to Amazon S3, using AWS Lambda only for logic and authorization.

Architecture Diagram
Key Achievements (Rubric Compliance)
Infrastructure as Code (IaC): 100% of resources (S3, Lambda, IAM, API Gateway) are defined in template.yaml.

Security: S3 bucket has PublicAccessBlockConfiguration enabled. No public access is permitted.

Protocol Semantics: Implements HTTP 307 Temporary Redirect for the download flow to preserve request integrity.

Regional Robustness: Specifically configured for the us-east-2 (Ohio) region using Signature Version 4 (SigV4).

Prerequisites
Before deploying, ensure you have the following:

AWS Account: Active credentials configured locally.

AWS SAM CLI: Installed and updated.

Python 3.9: Installed (matches the Lambda runtime).

Target Region: Optimized for us-east-2 to handle specific S3 regional signature requirements.

Deployment Instructions
1. Fork and Clone
Fork this repository to your GitHub account and clone it:

Bash

git clone https://github.com/YOUR_USERNAME/file-gateway-service.git
cd file-gateway-service
2. Build the Application
Bash

sam build
3. Deploy (Guided)
Use the guided mode to set the region to us-east-2:

Bash

sam deploy --guided
Configuration Settings:

Stack Name: file-gateway-service

AWS Region: us-east-2

Allow SAM CLI to create IAM roles: Yes

Allow SAM CLI to create API: Yes

Save arguments to configuration file: Yes

Functionality Verification
Endpoint A: POST /files (Upload)
This endpoint generates a pre-signed URL for a direct S3 upload.

Bash

curl -X POST <ApiEndpoint>/files \
     -H "Content-Type: application/json" \
     -d '{"filename": "test-file.txt"}'
Expected Result: A JSON response containing uploadUrl.

Execution: Use the uploadUrl with a PUT request:

Bash

curl -X PUT -T "test-file.txt" "<UPLOAD_URL>"
Endpoint B: GET /files/{objectKey} (Download)
This endpoint demonstrates the Redirect Logic.

Bash

curl -i <ApiEndpoint>/files/test-file.txt
Expected Result: HTTP/2 307 Temporary Redirect.

Location Header: Contains the S3 pre-signed URL valid for 1 hour.

Follow Redirect: Use curl -L to automatically follow the redirect and download the file content:

Bash

curl -L <ApiEndpoint>/files/test-file.txt
Technical Implementation Notes
Redirect Logic: Used HTTP 307 to ensure that a browser or client does not change the GET method to any other method during the redirect.

Boto3 Configuration: The Lambda handlers explicitly use an endpoint_url for s3.us-east-2.amazonaws.com and signature_version='s3v4' to ensure compatibility with regional S3 signature requirements.

Least Privilege: IAM roles for the Lambda functions are restricted to only the necessary S3 actions (PutObject for uploads and GetObject for downloads).