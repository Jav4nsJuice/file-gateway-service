# Secure Serverless File Gateway

## Project Description
This project provides a secure mechanism to upload and download files using AWS Lambda and S3 Pre-signed URLs.

## Deployment Instructions
1. **Fork** this repository.
2. Ensure you have the **AWS SAM CLI** installed.
3. Run `sam build`.
4. Run `sam deploy --guided`.

## Verification
- **POST /files**: Returns a JSON object with an upload URL.
- **GET /files/{objectKey}**: Returns an HTTP 307 Redirect to a secure download URL.
